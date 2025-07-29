"""Kernel Provisioner for Jupyter that uses HTTP(S) to launch kernels on remote machines, 
and SSH tunnels to connect to it."""
import logging
import secrets
import asyncio
import socket
import getpass
import hmac
import hashlib
from dataclasses import dataclass
import httpx # pylint: disable=import-error
from jupyter_client import KernelProvisionerBase # pylint: disable=import-error

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)

@dataclass
class HTTPConfig:
    """Configuration for HTTP connection."""
    url: str        # url of the api
    api_key: str    # api_key to ensure the instance is authorized to call the api
    secret: str     # secret to ensure the api hasn't been impersonated

@dataclass
class SSHConfig:
    """Configuration for ssh connection"""
    username:str    # username of the host to ssh to
    hostname:str    # host to ssh to
    port:str

ports_legend = ("shell_port","iopub_port","stdin_port","control_port","hb_port")

class SlurmHTTPProvisioner(KernelProvisionerBase):
    """
    A Kernel Provisioner that creates a kernel in a remote Slurm job and connects to it.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        config = kwargs.get('config', {})

        # If no config is provided, try to get it from the kernel_spec metadata
        if not config:
            kernel_spec = kwargs.get('kernel_spec', {})
            metadata = getattr(kernel_spec,'metadata', {})
            kp = metadata.get('kernel_provisioner', {})
            config = kp.get('config', {})

        _log.info("using config %s",config)

        self._http_config = HTTPConfig(
            url=config.get("url","").strip("/"),
            api_key=config.get("api_key",""),
            secret=config.get("secret",""))
        self._ssh_config = SSHConfig(
            username=config.get("username"),
            hostname=config.get("hostname"),
            port=config.get("port","22"))

        self._auth_token = None
        self._remote_public_key = None
        self._connection_info = {} # Dictionary to hold connection info for the Jupyter kernels
        self._available_ports = []
        _log.info("SlurmHTTPProvisioner initialized")


    async def pre_launch(self, **kwargs): # pylint: disable=missing-function-docstring
        kwargs = await super().pre_launch(**kwargs)
        kwargs.setdefault('cmd', None)
        return kwargs


    async def launch_kernel(self, cmd, **kwargs): # pylint: disable=unused-argument
        """ Launches a Jupyter kernel on a remote machine using Slurm and HTTPS."""
        try:
            # ----- GETTING THE REMOTE PUBLIC KEY -----
            # Send a get request to the remote machine to retrieve its public key
            _log.info("Fetching the public key of the remote machine...")
            await self._fetch_public_key()
            _log.info("Public key retrieved successfully.")

            # Adding the public key to the SSH config
            _log.info("Adding the public key to the SSH config...")
            await self._authorize_public_key()
            _log.info("Public key added successfully.")


            # ----- SUBMITTING THE SLURM JOB -----
            # Starts a Slurm job to run the Jupyter kernel
            _log.info("Submitting Slurm job to start the Jupyter kernel...")
            await self._submit_slurm_job()
            _log.info("Slurm job is now pending.")

            # Waiting for the Slurm job to start + getting connection info
            _log.info("Waiting for the Slurm job to start...")
            await self._wait_slurm_rdy()
            _log.info("Slurm job is now running.")


            # ----- CONNECTING TO THE REMOTE KERNEL -----
            # Find 5 available ports, to which the remote kernel will bind its ports
            _log.error("Finding available ports for SSH tunneling...")
            await self._find_unassigned_ports()
            _log.error("Available ports found successfully: %s", self._available_ports)

            # Telling the remote machine to establish ssh tunnels
            _log.info("Awaiting for the remote machine to establish SSH tunnels...")
            await self._ask_for_tunnels()
            _log.info("SSH tunnels established successfully.")

            # jupyter_client expects the value of "key" to be bytes.
            self._connection_info["key"] = self._connection_info["key"].encode()
            for i, port_name in enumerate(ports_legend):
                self._connection_info[port_name] = self._available_ports[i]
            self._connection_info["ip"] = "127.0.0.1"
            return self._connection_info

        except Exception as e:
            _log.error("Failed to launch kernel: %s", e)
            await self.cleanup(False)
            raise e


    async def _fetch_api(self,method,endpoint,payload=None):
        headers = {
            "Authorization": f"Bearer {self._auth_token or self._http_config.api_key}",
            "Content-Type": "application/json"
        }
        async with httpx.AsyncClient() as client:
            if method.lower() == "get":
                response = await client.get(
                    f"{self._http_config.url}/{endpoint}",
                    params=payload,
                    headers=headers,
                    timeout=10
                )
            elif method.lower() == "post":
                response = await client.post(
                    f"{self._http_config.url}/{endpoint}",
                    json=payload,
                    headers=headers,
                    timeout=10
                )
            elif method.lower() == "delete":
                response = await client.delete(
                    f"{self._http_config.url}/{endpoint}",
                    headers=headers,
                    timeout=10
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        return response


    async def _fetch_public_key(self):
        challenge = secrets.token_hex(16)
        payload = {"challenge": challenge}
        response = await self._fetch_api("get","pub_key",payload)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch public key: {response.text}")

        parsed_response = response.json()
        received_challenge = parsed_response.get("hashChallenge")

        def words_to_bytes(words):
            b = bytearray()
            for word in words:
                # Handle negative numbers like JavaScript/Java would (2's complement 32-bit)
                word = word & 0xFFFFFFFF
                b.extend(word.to_bytes(4, byteorder='big'))
            return bytes(b)

        received_hmac = words_to_bytes(
            received_challenge["words"])[:received_challenge["sigBytes"]]
        expected_hmac = hmac.new(
            self._http_config.secret.encode(), challenge.encode(), hashlib.sha256).digest()

        if not parsed_response.get("sshKey"):
            raise RuntimeError("No public key received from remote server.")
        if not hmac.compare_digest(received_hmac, expected_hmac):
            raise RuntimeError("Possible impersonation")
        if not parsed_response.get("token"):
            raise RuntimeError("Invalid response from the api: missing api")
        self._auth_token = parsed_response.get("token")
        self._remote_public_key = parsed_response.get("sshKey")


    async def _authorize_public_key(self):
        user = getpass.getuser()
        authorized_keys_path = f"/home/{user}/.ssh/authorized_keys"
        with open(authorized_keys_path, "a", encoding="utf-8") as f:
            f.write(self._remote_public_key.strip() + "\n")


    async def _submit_slurm_job(self):
        response = await self._fetch_api("post","launch_kernel")
        if response.status_code != 200:
            raise RuntimeError(f"Failed to submit Slurm job: {response.text}")


    async def _wait_slurm_rdy(self):
        i = 0
        consecutive_failed = 0
        while True:
            result = await self._fetch_api("get","ready")
            if result.status_code != 200:
                consecutive_failed += 1
                _log.warning("Failed to check Slurm job status: %s", result.text)
                if consecutive_failed > 10:
                    raise RuntimeError("Failed to get Slurm job status after multiple attempts.")
            else:
                consecutive_failed = 0
                data = result.json()
                if data.get("JOBSTATE") == "RUNNING":
                    _log.info("Slurm job is ready.")
                    break
            await asyncio.sleep(0.5 if i < 20 else min(i/10,30))
            i += 1

        if not data.get("ConnectionFile"):
            raise RuntimeError("No connection_info received from remote server.")
        self._connection_info = data.get("ConnectionFile")


    async def _find_unassigned_ports(self):
        ports = []
        start_port = 9000
        needed_ports = len(ports_legend)

        def is_port_free(port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(("", port))
                    return True
                except OSError:
                    return False

        port = start_port
        while len(ports) < needed_ports:
            if is_port_free(port):
                ports.append(port)
            port += 1

        self._available_ports = ports


    async def _ask_for_tunnels(self):
        payload = {}
        for i, port_name in enumerate(ports_legend):
            payload[port_name] = self._available_ports[i]
        payload["user"] = self._ssh_config.username
        payload["host"] = self._ssh_config.hostname
        payload["port"] = self._ssh_config.port
        result = await self._fetch_api("post","start_tunnels",payload)
        if result.status_code != 200:
            raise RuntimeError(f"Failed to start SSH tunnels: {result.text}")


    async def _ask_for_cleanup(self):
        await self._fetch_api("delete","tunnels")


    @property
    def has_process(self) -> bool: # pylint: disable=missing-function-docstring
        return True

    async def poll(self): # pylint: disable=missing-function-docstring
        pass

    async def wait(self): # pylint: disable=missing-function-docstring
        pass

    async def send_signal(self, signum: int): # pylint: disable=missing-function-docstring
        _log.warning("Cannot send signal: %s.", signum)

    async def kill(self, restart=False): # pylint: disable=missing-function-docstring
        if restart:
            _log.warning("Cannot restart existing kernel.")
        await self.cleanup(restart)

    async def terminate(self, restart=False): # pylint: disable=missing-function-docstring
        if restart:
            _log.warning("Cannot terminate existing kernel.")
        await self.cleanup(restart)

    async def cleanup(self, restart=False): # pylint: disable=missing-function-docstring, unused-argument
        _log.info("Cleaning up")
        try:
            await self._ask_for_cleanup()
        except Exception as e: # pylint: disable=broad-exception-caught
            _log.error("Error during cleanup: %s", e)
        _log.info("Cleanup completed.")

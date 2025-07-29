# Slurm HTTP Provisioner

## What is this package

This package is a Jupyter Kernel Provisioner.

It uses an http(s) api to launch a remote kernel in a slurm job and ssh tunnels to connect to it.

Once configured, on the Jupyter Notebook / Lab interface, you can just select a kernel using this provisioner and it will set up everything accordingly.

## Setup

### 1 - Build a remote wrapper script

This remote wrapper will be called when we want to launch the kernel.
Thus, it should:

- Start a slurm job that will start a kernel (the connection file should be named .../kernel-{slurm_job_id}.json, thus the command inside a batch script could be `python -m ipykernel_launcher -f=/tmp/kernel-${SLURM_JOB_ID}.json`)
- Wait for the job to start
- Return the slurm job id

See the example file

### 2 - Setup a kernel

This is the kernel that will use the slurm-http-provisioner. It will be displayed in the Notebook / Lab interface.

```
#~/.local/share/jupyter/kernels/slurm-http/kernel.json
{
  "display_name": "Python 3 (Slurm HTTP)",
  "language": "python",
  "metadata": {
    "kernel_provisioner": {
      "provisioner_name": "slurm-http-provisioner",
      "config": {
        "url": "http://example.com",
        "api_key": "1234",
        "secret": "123456789",
        "username": "debian",
        "hostname": "xxx.xxx.xxx.xxx"
      }
    }
  }
}

```

See the example file

### 3 - Voilà

You should now be able to use this new kernel.

Use `jupyter kernelspec list` to check your kernel is detected.
Use `jupyter kernelspec provisioners` to check that slurm-http-provisioner is installed.

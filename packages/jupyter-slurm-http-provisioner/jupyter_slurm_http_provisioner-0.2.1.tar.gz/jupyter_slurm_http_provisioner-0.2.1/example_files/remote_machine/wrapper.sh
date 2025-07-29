{
  # Everything inside this block is logged
  source ./venv/bin/activate

  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  SLURM_SCRIPT="${SCRIPT_DIR}/slurm.sh"
  JOB_SUBMIT_OUTPUT=$(sbatch "$SLURM_SCRIPT")
  JOB_ID=$(echo "$JOB_SUBMIT_OUTPUT" | awk '{print $4}')
  CONN_FILE="/tmp/kernel-${JOB_ID}.json"
} > /tmp/wrapper.log 2>&1

# Only this line goes to stdout
echo "$JOB_ID"
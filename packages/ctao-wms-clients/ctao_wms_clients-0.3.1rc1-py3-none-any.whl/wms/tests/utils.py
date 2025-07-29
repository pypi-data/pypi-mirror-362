"""Helping to run WMS tests."""

import logging
import os
import time
from pathlib import Path

TEST_TIMEOUT = float(os.getenv("DIRAC_TEST_JOB_TIMEOUT", "180"))


log = logging.getLogger(__name__)


def wait_for_status(
    dirac,
    job_id,
    status,
    error_on: None | set[str] = None,
    timeout=TEST_TIMEOUT,
    poll=5.0,
    job_output_dir=None,
):
    """Wait for Dirac job status."""
    start = time.perf_counter()

    current_status = None

    error_on = set(error_on) if error_on is not None else set()

    while (time.perf_counter() - start) < timeout:
        res = dirac.getJobStatus(job_id)
        current_status = res["Value"][job_id]["Status"]
        log.info(
            "Waiting for job %d to reach status '%s', current status '%s'",
            job_id,
            status,
            current_status,
        )

        if job_output_dir is not None and (
            current_status == status or current_status in error_on
        ):
            dirac.getOutputSandbox(job_id, job_output_dir, noJobDir=True)

        if current_status == status:
            return res

        if current_status in error_on:
            msg = f"Job entered error state '{current_status}': {res!r}"
            if job_output_dir is not None:
                for ext in ("log", "out", "err"):
                    for path in Path(job_output_dir).glob(f"*.{ext}"):
                        msg += f"\nOutput in {path}:\n"
                        msg += path.read_text()
            raise ValueError(msg)

        time.sleep(poll)

    msg = (
        f"Job {job_id} did not reach status '{status}' within {timeout} seconds."
        f" Current status is '{current_status}'."
    )
    raise TimeoutError(msg)

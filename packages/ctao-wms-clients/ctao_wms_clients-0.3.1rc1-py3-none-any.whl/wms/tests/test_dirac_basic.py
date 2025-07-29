"""Test job status."""

import logging
from pathlib import Path

import pytest

from wms.tests.utils import wait_for_status

pytestmark = [
    pytest.mark.wms,
    pytest.mark.dirac_client,
]


# missing "Run a single-job workflow" UC ID
# @pytest.mark.verifies_usecase("DPPS-UC-110-????")
@pytest.mark.usefixtures("_init_dirac")
def test_simple_job(tmp_path):
    from DIRAC.Interfaces.API.Dirac import Dirac
    from DIRAC.Interfaces.API.Job import Job

    dirac = Dirac()

    job = Job()
    job.setExecutable("echo", arguments="Hello world")
    job.setName("testjob")
    job.setDestination("CTAO.CI.de")
    res = dirac.submitJob(job)
    assert res["OK"]
    job_id = res["Value"]

    # wait for job to succeed, will error in case of timeout or job failure
    result = wait_for_status(
        dirac,
        job_id=job_id,
        status="Done",
        error_on={"Failed"},
        timeout=300,
        job_output_dir=tmp_path,
    )
    print(result)


@pytest.mark.usefixtures("_init_dirac")
def test_cvmfs_available_on_ce(tmp_path):
    from DIRAC.Interfaces.API.Dirac import Dirac
    from DIRAC.Interfaces.API.Job import Job

    dirac = Dirac()

    job = Job()
    job.setExecutable("ls", "/cvmfs/ctao.dpps.test/")
    job.setExecutable("cat", "/cvmfs/ctao.dpps.test/new_repository")
    job.setName("cvmfs_job")
    job.setDestination("CTAO.CI.de")
    res = dirac.submitJob(job)
    assert res["OK"]
    job_id = res["Value"]

    # wait for job to succeed, will error in case of timeout or job failure
    result = wait_for_status(
        dirac,
        job_id=job_id,
        status="Done",
        error_on={"Failed"},
        timeout=300,
        job_output_dir=tmp_path,
    )
    print(result)


@pytest.mark.verifies_usecase("DPPS-UC-100-2")
@pytest.mark.usefixtures("_init_dirac")
def test_cwl_job(tmp_path):
    from CTADIRAC.Interfaces.API.CWLJob import CWLJob
    from DIRAC.Interfaces.API.Dirac import Dirac

    log = logging.getLogger(__name__)

    dirac = Dirac()
    cwl_workflow = Path("src/wms/tests/cwl/hello_world/container_example.cwl")
    cwl_inputs = Path("src/wms/tests/cwl/hello_world/container_example_inputs.yaml")
    cvmfs_path = Path("/cvmfs/ctao.dpps.test/")
    job = CWLJob(
        cwl_workflow=cwl_workflow, cwl_inputs=cwl_inputs, cvmfs_base_path=cvmfs_path
    )
    res = job.submit()
    assert res["OK"], f"Submitting job failed: {res!r}"
    job_id = res["Value"]

    # wait for job to succeed, will error in case of timeout or job failure
    result = wait_for_status(
        dirac,
        job_id=job_id,
        status="Done",
        error_on={"Failed"},
        timeout=300,
        job_output_dir=tmp_path,
    )
    log.info(result)


@pytest.mark.verifies_usecase("DPPS-UC-100-2")
@pytest.mark.usefixtures("_init_dirac")
def test_cwl_workflow_job(tmp_path):
    from CTADIRAC.Interfaces.API.CWLJob import CWLJob
    from DIRAC.Interfaces.API.Dirac import Dirac

    log = logging.getLogger(__name__)

    dirac = Dirac()
    cwl_workflow = Path("src/wms/tests/cwl/basic_workflow/gaussian-fit-workflow.cwl")
    cwl_inputs = Path(
        "src/wms/tests/cwl/basic_workflow/inputs-gaussian-fit-complete.yaml"
    )
    cvmfs_path = Path("/cvmfs/ctao.dpps.test/")
    job = CWLJob(
        cwl_workflow=cwl_workflow, cwl_inputs=cwl_inputs, cvmfs_base_path=cvmfs_path
    )
    job.setName = "gaussian_fit_workflow"
    res = job.submit()
    assert res["OK"], f"Submitting job failed: {res!r}"
    job_id = res["Value"]

    # wait for job to succeed, will error in case of timeout or job failure
    result = wait_for_status(
        dirac,
        job_id=job_id,
        status="Done",
        error_on={"Failed"},
        timeout=300,
        job_output_dir=tmp_path,
    )
    log.info(result)

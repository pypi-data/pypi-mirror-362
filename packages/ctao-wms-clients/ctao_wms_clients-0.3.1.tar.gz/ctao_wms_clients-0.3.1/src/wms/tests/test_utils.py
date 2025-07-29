import pytest

from wms.tests.utils import wait_for_status


@pytest.mark.usefixtures("_init_dirac")
def test_wait_for_status_error(tmp_path):
    from DIRAC.Interfaces.API.Dirac import Dirac
    from DIRAC.Interfaces.API.Job import Job

    dirac = Dirac()

    job = Job()
    job.setExecutable("cat", arguments="/i/do/not/exist")
    job.setName("test_error_job")
    job.setDestination("CTAO.CI.de")
    res = dirac.submitJob(job)
    assert res["OK"]
    job_id = res["Value"]

    # wait for job to succeed, will error in case of timeout or job failure
    with pytest.raises(
        ValueError, match="Job entered error state 'Failed'"
    ) as exc_info:
        wait_for_status(
            dirac,
            job_id=job_id,
            status="Done",
            error_on={"Failed"},
            timeout=300,
            job_output_dir=tmp_path,
        )

    # check downloading of output sandbox happened
    assert (tmp_path / "Script1_CodeOutput.log").is_file()
    # check content of log files was added to exception
    assert "cat: /i/do/not/exist: No such file or directory" in exc_info.value.args[0]

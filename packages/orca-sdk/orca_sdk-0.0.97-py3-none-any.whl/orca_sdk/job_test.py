import time

from .classification_model import ClassificationModel
from .datasource import Datasource
from .job import Job, Status


def test_job_creation(classification_model: ClassificationModel, datasource: Datasource):
    job = classification_model.evaluate(datasource, background=True)
    assert job.id is not None
    assert job.type == "EVALUATE_MODEL"
    assert job.status in [Status.DISPATCHED, Status.PROCESSING]
    assert job.created_at is not None
    assert job.updated_at is not None
    assert job.refreshed_at is not None
    assert len(Job.query(limit=5, type="EVALUATE_MODEL")) >= 1


def test_job_result(classification_model: ClassificationModel, datasource: Datasource):
    job = classification_model.evaluate(datasource, background=True)
    result = job.result(show_progress=False)
    assert result is not None
    assert job.status == Status.COMPLETED
    assert job.steps_completed is not None
    assert job.steps_completed == job.steps_total


def test_job_wait(classification_model: ClassificationModel, datasource: Datasource):
    job = classification_model.evaluate(datasource, background=True)
    job.wait(show_progress=False)
    assert job.status == Status.COMPLETED
    assert job.steps_completed is not None
    assert job.steps_completed == job.steps_total
    assert job.value is not None


def test_job_refresh(classification_model: ClassificationModel, datasource: Datasource):
    job = classification_model.evaluate(datasource, background=True)
    last_refreshed_at = job.refreshed_at
    # accessing the status attribute should refresh the job after the refresh interval
    Job.set_config(refresh_interval=1)
    time.sleep(1)
    job.status
    assert job.refreshed_at > last_refreshed_at
    last_refreshed_at = job.refreshed_at
    # calling refresh() should immediately refresh the job
    job.refresh()
    assert job.refreshed_at > last_refreshed_at


def test_job_query_pagination(classification_model: ClassificationModel, datasource: Datasource):
    """Test pagination with Job.query() method"""
    # Create multiple jobs to test pagination
    jobs_created = []
    for i in range(3):
        job = classification_model.evaluate(datasource, background=True)
        jobs_created.append(job.id)

    # Test basic pagination with limit
    jobs_page1 = Job.query(type="EVALUATE_MODEL", limit=2)
    assert len(jobs_page1) == 2

    # Test pagination with offset
    jobs_page2 = Job.query(type="EVALUATE_MODEL", limit=2, offset=1)
    assert len(jobs_page2) == 2

    # Verify different pages contain different jobs (allowing for some overlap due to timing)
    page1_ids = {job.id for job in jobs_page1}
    page2_ids = {job.id for job in jobs_page2}

    # At least one job should be different between pages
    assert len(page1_ids.symmetric_difference(page2_ids)) > 0

    # Test filtering by status
    jobs_by_status = Job.query(status=Status.PROCESSING, limit=10)
    for job in jobs_by_status:
        assert job.status == Status.PROCESSING

    # Test filtering by multiple statuses
    multi_status_jobs = Job.query(status=[Status.PROCESSING, Status.COMPLETED], limit=10)
    for job in multi_status_jobs:
        assert job.status in [Status.PROCESSING, Status.COMPLETED]

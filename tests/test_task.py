import pytest
from fakeredis import FakeStrictRedis
from rq import Queue


def test_enqueue_task():
    queue = Queue(is_async=False, connection=FakeStrictRedis())
    job = queue.enqueue(my_long_running_job)
    assert job.is_queued
# queue = Queue(is_async=False, connection=FakeStrictRedis())
# job = queue.enqueue(my_long_running_job)
# assert job.is_finished
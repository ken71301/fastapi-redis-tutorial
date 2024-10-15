from fastapi import APIRouter, HTTPException
from rq import Queue
from redis import Redis
from ..config import Config
from ..tasks import enqueue_task

router = APIRouter()
config = Config()
redis = Redis.from_url(config.redis_url)
task_queue = Queue('rq', connection=redis)

@router.post('/receive')
async def receive(title: str):
    try:
        job = task_queue.enqueue(enqueue_task, meta={"status": "pending"}, job_id=title)
        return {"job_id": job.id, "title": title}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/jobs')
async def get_jobs():
    try:
        jobs = task_queue.get_job_ids()
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
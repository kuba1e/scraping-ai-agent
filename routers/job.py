from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from helpers.session import get_session_id
from schemas.job import ProductScrapingJobResponse
from models.job import ProductScrapingJob
router = APIRouter(prefix='/job', tags=['job'])


@router.get('/{job_id}', response_model=ProductScrapingJobResponse)
def get_job_by_id(job_id: str, session_id:str = Depends(get_session_id),  db:Session = Depends(get_db) ):
    job = db.query(ProductScrapingJob).filter(ProductScrapingJob.job_id == str(job_id)).first()

    if type(job).__name__ == 'NoneType':
        raise  HTTPException(status_code=404, detail="Couldn't find the job by provided id")

    return job
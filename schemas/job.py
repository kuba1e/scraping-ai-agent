from typing import Optional

from pydantic import BaseModel
from datetime import  datetime

class ProductScrapingJobResponse (BaseModel):
    job_id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str]

    class Config:
        from_attributes: True


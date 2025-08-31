from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from db.database import Base

class ProductScrapingJob(Base):
    __tablename__ = 'product_scraping_jobs'

    id = Column(Integer, primary_key=True)
    job_id = Column(String, unique=True)
    session_id = Column(String)
    status = Column(String)
    scraping_products_result_id = Column(Integer, nullable=True)
    error = Column(String, nullable=True)
    created_at =Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

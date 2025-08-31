import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, BackgroundTasks, Response

from db.database import get_db, SessionLocal
from helpers.session import get_session_id
from schemas.job import ProductScrapingJobResponse
from schemas.product import ProductScrapeRequest
from  sqlalchemy.orm import Session
from core.web_scraping import scrape_products_from_page_url

from models.job import ProductScrapingJob
from models.product import ScrapedProductsResult, Product

router = APIRouter( prefix='/products', tags=['products'])

@router.post('/scrape' , response_model=ProductScrapingJobResponse )
def scrape_products(request:ProductScrapeRequest,response:Response, background_tasks:BackgroundTasks, session_id:str = Depends(get_session_id), db:Session = Depends(get_db)):
    response.set_cookie(key='session_id', value=session_id, httponly=True)

    job_id = str(uuid.uuid4())

    job = ProductScrapingJob(job_id=job_id, session_id=session_id, status='pending')

    db.add(job)
    db.commit()

    background_tasks.add_task(scrape_products_task, job_id=job_id, session_id=session_id, url= request.url)

    return job

def scrape_products_task(job_id: str, session_id:str, url: str):
    db = SessionLocal()

    try:
        job:ProductScrapingJob = db.query(ProductScrapingJob).filter(ProductScrapingJob.job_id == job_id).first()

        if not job:
            return

        try:
            job.status = 'processing'
            db.commit()

            products = scrape_products_from_page_url(url)

            scraped_result = ScrapedProductsResult(session_id=session_id)

            print(f'Products {products}')

            scraped_result.products = [Product(name= product['product_name'], brand_name= product['brand_name'], price=product['price'], price_currency=product['price_currency'], images= product['images'] ) for product in products]

            print(f'Scrapped result {scraped_result}')

            db.add(scraped_result)

            job.scraping_products_result_id= scraped_result.id

            db.commit()


        except Exception as e:
            print(e)
            job.status = 'failed'
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()

    finally:
        db.close()
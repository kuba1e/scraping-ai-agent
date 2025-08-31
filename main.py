from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import create_tables
from core.config import settings
from routers import product

app = FastAPI(
    title='Web scraping AI agent',
    description='The app is developed to scrape in advance way web',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc'
)

create_tables()

app.add_middleware(CORSMiddleware, allow_origins=settings.ALLOWED_ORIGINS, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(product.router, prefix=settings.API_PREFIX)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app',host= '0.0.0.0', port=8000, reload=True)
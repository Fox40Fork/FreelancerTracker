#FastAPI

from fastapi import FastAPI
from routers import clients, invoices, users
from database import createDatabase

app = FastAPI(
    title="Freelancer Invoice/Income Tracking System",
    description="An API for managing freelancer's invoices and incomes",
    version="1.0.0"
)
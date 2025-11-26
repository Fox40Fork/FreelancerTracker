#FastAPI

from fastapi import FastAPI
from routers import clients, invoices, users, projects, sessions
from database import createDatabase

app = FastAPI(
    title="Freelancer Invoice/Income Tracking System",
    description="An API for managing freelancers' invoices and incomes",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    createDatabase()

app.include_router(clients.router, prefix="/clients", tags=["clients"])
app.include_router(invoices.router, prefix="/invoices", tags=["invoices"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
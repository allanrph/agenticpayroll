from fastapi import FastAPI

from app.adapters.incoming.routes import payroll
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(
    title="Global Payroll Microservice",
    version="1.0.0",
    description="Modular FastAPI payroll service with Gross-to-Net calculations across countries."
)

        
# Monitoring (Prometheus metrics exposed at /metrics)
Instrumentator().instrument(app).expose(app)

# Include API routes
app.include_router(payroll.router)
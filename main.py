from fastapi import FastAPI
from pydantic import BaseModel
from src.services.inference_service import predict_ticket

app = FastAPI(title="AI-Driven Customer Support Ticketing System")


class TicketRequest(BaseModel):
    subject: str
    description: str
    priority: str
    customer_plan: str
    sla_breached: int


@app.get("/")
def root():
    return {"message": "AI Ticketing System API is running"}


@app.post("/predict-ticket")
def predict(request: TicketRequest):

    result = predict_ticket(request.dict())

    return result

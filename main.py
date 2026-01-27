from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import stripe
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.get("/pagar")
def pagar(
    success_url: str = Query(...),
    cancel_url: str = Query(...)
):
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{
            "price": os.getenv("PRICE_ID"),
            "quantity": 1,
        }],
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return {"url": session.url}

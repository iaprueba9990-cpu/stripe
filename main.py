from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import stripe
import os

app = FastAPI()

# 🔓 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego lo restringimos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.get("/")
def home():
    return {"ok": True}

@app.get("/pagar")
def pagar():
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{
            "price": os.getenv("PRICE_ID"),
            "quantity": 1,
        }],
        success_url="https://contador-64f9c.web.app/#/pagoexitoso",
        cancel_url="https://contador-64f9c.web.app/#/pagonoexitoso",
    )
    return {"url": session.url}

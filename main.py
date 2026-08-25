from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEGRAM_BOT_TOKEN = "8785423339:AAFa1z7mfHn2uAHRhJGarioyiciSwYpqrxQ"
TELEGRAM_CHAT_ID = "2055556738"

def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            phone TEXT,
            address TEXT,
            package TEXT,
            location_url TEXT,
            contact_method TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class OrderSchema(BaseModel):
    fullName: str
    phone: str
    address: str
    package: str
    locationUrl: str
    contactMethod: str

@app.post("/api/order")
def create_order(order: OrderSchema):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (full_name, phone, address, package, location_url, contact_method)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (order.fullName, order.phone, order.address, order.package, order.locationUrl, order.contactMethod))
    conn.commit()
    conn.close()

    msg = (
        f"🚨 *طلب تركيب جديد!*\n\n"
        f"👤 *الاسم:* {order.fullName}\n"
        f"📞 *الهاتف:* {order.phone}\n"
        f"📍 *العنوان:* {order.address}\n"
        f"📦 *الباقة:* {order.package}\n"
        f"💬 *طريقة التواصل:* {order.contactMethod}\n"
        f"🗺️ *الموقع:* {order.locationUrl}"
    )

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(telegram_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})

    return {"status": "success", "message": "Order created successfully"}

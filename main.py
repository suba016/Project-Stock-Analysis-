from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Subashree@mysql",
    database="stock_app"
)

cursor = db.cursor()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def read_root():
    return {"status": "OK"}


@app.get("/stock/{symbol}")
def get_stock(symbol: str):
    stock = yf.Ticker(symbol)

    price = stock.info.get("currentPrice")

    cursor.execute(
    "INSERT INTO stock_history (symbol, price) VALUES (%s, %s)",
    (symbol, price))
                    
    db.commit()

    cursor.execute("""
        DELETE FROM stock_history
        WHERE id NOT IN (
            SELECT id FROM (
                SELECT id
                FROM stock_history
                ORDER BY searched_at DESC
                LIMIT 10
            ) AS temp
        )
    """)
    db.commit()





    return {
        "symbol": symbol,
        "price": price,
        "currency": "USD"
    }





@app.get("/history")
def get_history():
    cursor.execute(
        "SELECT symbol, price, searched_at FROM stock_history ORDER BY searched_at DESC"
    )

    rows = cursor.fetchall()

    history = []

    for row in rows:
        history.append({
            "symbol": row[0],
            "price": row[1],
            "time": row[2].strftime("%Y-%m-%d %H:%M:%S")
        })

    return history



@app.get("/stock/{symbol}/history")
def get_stock_history(symbol: str):
    stock = yf.Ticker(symbol)

    history = stock.history(period="7d")

    result = []

    for date, row in history.iterrows():
        result.append({
            "date": date.strftime("%Y-%m-%d"),
            "price": float(row["Close"])
        })

    return result

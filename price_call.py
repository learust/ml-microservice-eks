from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text, select, Integer, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from price import trade
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

class Trade(Base):
    __tablename__ = "trades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)  # epoch seconds

Base.metadata.create_all(engine)

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}, 200
    except Exception as e:
        return {"status": "db_error", "detail": str(e)}, 500

@app.post("/api/trade")
def api_trade():
    data = request.get_json(silent=True) or {}

    # basic validation
    try:
        year = int(data.get("year"))
        mileage = int(data.get("mileage"))
    except (TypeError, ValueError):
        return jsonify(error="invalid inputs"), 400

    if year < 1980 or year > 2026:
        return jsonify(error="year out of range"), 400
    if mileage < 0 or mileage > 1_000_000:
        return jsonify(error="mileage out of range"), 400

    # predict
    predicted = trade(year, mileage)

    # persist
    with SessionLocal() as s:
        row = Trade(
            year=year,
            mileage=mileage,
            value=float(predicted),
            created_at=int(datetime.utcnow().timestamp()),
        )
        s.add(row)
        s.commit()
        s.refresh(row)

        return jsonify(
            id=row.id,
            year=row.year,
            mileage=row.mileage,
            value=round(row.value, 2),
            created_at=row.created_at,
        ), 200

@app.get("/api/history")
def history():
    limit = int(request.args.get("limit", 25))
    with SessionLocal() as s:
        rows = s.execute(
            select(Trade).order_by(Trade.id.desc()).limit(limit)
        ).scalars().all()

        return jsonify([
            {
                "id": r.id,
                "year": r.year,
                "mileage": r.mileage,
                "value": round(float(r.value), 2),
                "created_at": r.created_at,
            }
            for r in rows
        ]), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("BACKEND_PORT", 5000)))

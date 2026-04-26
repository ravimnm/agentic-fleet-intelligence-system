from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from math import radians, sin, cos, sqrt, atan2

from database.mongo_client import MongoConnection
from dependencies import get_db, get_current_user
from utils.llm_client import generate_response
from utils.rag_pipeline import RAGPipeline

router = APIRouter(prefix="/bot", tags=["bot"])


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


@router.post("/chat")
async def chat(payload: Dict[str, Any], db: MongoConnection = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """LLM-driven reasoning system with structured context.

    payload expected: { vehicleId: int, message: str }
    """
    if "vehicleId" not in payload:
        raise HTTPException(status_code=400, detail="vehicleId is required")

    vid = int(payload["vehicleId"])
    message = payload.get("message", "")

    # RBAC
    if current_user.get("role") == "user":
        if current_user.get("vehicleId") is None or int(vid) != int(current_user.get("vehicleId")):
            raise HTTPException(status_code=403, detail="Forbidden: access to this vehicle is denied")

    # Fetch vehicle data
    telemetry = db.find_one("telemetry", {"vehicleId": vid}, sort=[("timestamp", -1)])
    prediction = db.find_one("predictions", {"vehicleId": vid}, sort=[("timestamp", -1)])
    risk = db.find_one("risk_logs", {"vehicleId": vid}, sort=[("timestamp", -1)])

    # Get RAG context
    rag = RAGPipeline(db)
    rag_context = rag.get_context(message)

    # Build structured prompt
    telemetry_summary = f"Temperature: {telemetry.get('temperature', 'N/A')}, RPM: {telemetry.get('rpm', 'N/A')}, Location: {telemetry.get('latitude', 'N/A')},{telemetry.get('longitude', 'N/A')}" if telemetry else "No telemetry available"
    prediction_summary = f"Predicted: {prediction.get('event', 'N/A')} with {prediction.get('probability', 0)*100:.1f}% probability" if prediction else "No prediction available"
    risk_summary = f"Risk: {risk.get('category', 'N/A')} score {risk.get('risk_score', 0):.2f}" if risk else "No risk data available"

    structured_context = f"""
    Vehicle Data:
    - Telemetry: {telemetry_summary}
    - Prediction: {prediction_summary}
    - Risk: {risk_summary}
    - Retrieved Context: {rag_context}
    """

    # Generate reasoned response
    from utils.llm_client import generate_reasoned_response
    response = generate_reasoned_response(message, structured_context)
    return {"answer": response}


@router.get("/assist/breakdown/{vehicleId}")
async def breakdown_assist(vehicleId: str, db: MongoConnection = Depends(get_db), current_user: dict = Depends(get_current_user)):
    vid = int(vehicleId)

    # RBAC
    if current_user.get("role") == "user":
        if current_user.get("vehicleId") is None or int(vid) != int(current_user.get("vehicleId")):
            raise HTTPException(status_code=403, detail="Forbidden: access to this vehicle is denied")

    # get latest risk and prediction
    risk = db.find_one("risk_logs", {"vehicleId": vid}, sort=[("timestamp", -1)])
    prediction = db.find_one("predictions", {"vehicleId": vid}, sort=[("timestamp", -1)])

    risk_score = float(risk.get("risk_score", 0)) if risk else 0.0
    prob = float(prediction.get("probability", 0)) if prediction else 0.0

    # trigger condition
    if not (risk_score > 0.8 or prob > 0.85):
        return {"breakdown": False, "message": "No breakdown condition detected."}

    # last location
    telemetry = db.find_one("telemetry", {"vehicleId": vid}, sort=[("timestamp", -1)])
    if not telemetry:
        raise HTTPException(status_code=404, detail="No telemetry location available")

    lat = telemetry.get("lat") or telemetry.get("latitude")
    lng = telemetry.get("lng") or telemetry.get("longitude")
    if lat is None or lng is None:
        raise HTTPException(status_code=400, detail="Telemetry lacks coordinates")

    centers_cursor = db.get_collection("service_centers").find({"open_now": True})
    centers = []
    for c in centers_cursor:
        c_lat = c.get("latitude")
        c_lng = c.get("longitude")
        if c_lat is None or c_lng is None:
            continue
        dist = haversine(float(lat), float(lng), float(c_lat), float(c_lng))
        centers.append({"center": c, "distance_km": dist})

    if not centers:
        return {"breakdown": True, "service_centers": []}

    # Build serializable list with distance and rating, sort by rating desc then distance asc
    def serial(cobj):
        c = cobj["center"].copy()
        c["_id"] = str(c.get("_id")) if c.get("_id") is not None else None
        c["distance_km"] = round(cobj["distance_km"], 3)
        c["rating"] = float(c.get("rating", 0)) if c.get("rating") is not None else 0.0
        return c

    centers_serial = [serial(c) for c in centers]
    centers_serial.sort(key=lambda c: (-c.get("rating", 0), c.get("distance_km", 9999)))

    # keep backwards compatibility by exposing best_rated and nearest_open
    best_rated = centers_serial[0]
    centers_by_distance = sorted(centers_serial, key=lambda c: (c.get("distance_km", 9999), -c.get("rating", 0)))
    nearest_open = centers_by_distance[0]

    return {"breakdown": True, "service_centers": centers_serial, "best_rated": best_rated, "nearest_open": nearest_open}

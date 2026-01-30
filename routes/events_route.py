from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from db.mongodb import events_collection

events_bp = Blueprint("events", __name__)

@events_bp.route("/events", methods=["GET"])
def get_events():
    try:
        threshold = datetime.utcnow() - timedelta(seconds=30)

        events = list(
            events_collection.find(
                {"timestamp": {"$gte": threshold}},
                {"_id": 0}
            ).sort("timestamp", -1)
        )

        # Convert datetime to ISO string for JSON serialization
        for event in events:
            if isinstance(event.get("timestamp"), datetime):
                event["timestamp"] = event["timestamp"].isoformat()

        return jsonify(events), 200

    except Exception as e:
        print(f"Events fetch error: {e}")
        return jsonify([]), 200

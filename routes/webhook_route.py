from flask import Blueprint, request, jsonify
from services.parser import parse_github_event
from services.deduplications import insert_if_new
from db.mongodb import events_collection

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/webhook", methods=["POST"])
def handle_webhook():
    try:
        event_type = request.headers.get("X-GitHub-Event")
        payload = request.get_json()

        event_data = parse_github_event(event_type, payload)

        if event_data:
            insert_if_new(event_data, events_collection)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"status": "error"}), 200

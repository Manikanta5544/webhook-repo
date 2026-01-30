from flask import Flask
from config import FLASK_PORT, FLASK_ENV
from db.mongodb import client
from routes.webhook_route import webhook_bp
from routes.events_route import events_bp

app = Flask(__name__, static_folder="ui", static_url_path="")

# Register blueprints
app.register_blueprint(webhook_bp)
app.register_blueprint(events_bp)

@app.route("/")
def index():
    return app.send_static_file("index.html")

# Health check
@app.route("/health")
def health():
    try:
        client.admin.command("ping")
        return {"status": "healthy"}, 200
    except:
        return {"status": "unhealthy"}, 200

if __name__ == "__main__":
    app.run(
        port=FLASK_PORT,
        debug=(FLASK_ENV == "development"),
        host="0.0.0.0"
    )

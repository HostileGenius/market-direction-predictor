from flask import Flask
from flask_cors import CORS
from backend.routes.predict_route import predict_bp
import os

app = Flask(__name__)
CORS(app)

app.register_blueprint(predict_bp)

@app.route("/health")
def health():
    return {"status": "Backend running"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

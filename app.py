from flask import Flask
from flask_cors import CORS
from config.db import init_db
from routes.user_routes import user_bp

app = Flask(__name__)

# ? Enable CORS for all routes
CORS(app)  # Allow all origins


# ? DB Connection
init_db()

# ? Routes
app.register_blueprint(user_bp, url_prefix="/api/users")

@app.route("/")
def home():
    return {"msg": "Army Recruitment API Running ?"}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


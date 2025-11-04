
from flask import Flask,send_from_directory
from flask_cors import CORS
from config.db import init_db
from routes.user_routes import user_bp
from routes.finger_routes import finger_bp
app = Flask(__name__)

# ? Allow CORS from Vite Dev, Electron, LAN clients
# CORS(app, resources={r"/*": {"origins": [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
#     "http://localhost",
#     "http://127.0.0.1",
#     "http://192.168.1.*"   # LAN network
# ]}})

# @app.after_request
# def after_request(response):
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
#     response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
#     return response
CORS(app)
# ? DB Init
init_db()

# ? Routes
app.register_blueprint(user_bp, url_prefix="/api/users")

app.register_blueprint(finger_bp, url_prefix="/api/finger")

@app.route("/")
def home():
    return {"msg": "Army Recruitment API Running ?"}
# Serve photos
@app.route('/photos/<filename>')
def get_photo(filename):
    return send_from_directory('/home/siva/photos', filename)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

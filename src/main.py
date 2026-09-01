from flask import Flask
from src.app.routes.auth_routes import auth_bp
from src.app.routes.user_routes import user_bp
from src.app.routes.task_routes import task_bp
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(task_bp)



if __name__ == "__main__":
    app.run(debug=True)

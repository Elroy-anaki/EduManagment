from DB.DB_CONFIG import *
from .login_routes import *
from .manager_routes import * 
from .teacher_routes import *

def register_blueprints(app):
    app.register_blueprint(login_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(manager_bp)
    
    
    
import os
import logging
from datetime import datetime
import pytz
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Configure Indian timezone
INDIAN_TZ = pytz.timezone('Asia/Kolkata')

def get_indian_time():
    """Get current time in Indian timezone"""
    return datetime.now(INDIAN_TZ)

def format_indian_time(dt=None, format_str='%Y-%m-%d %H:%M:%S'):
    """Format datetime in Indian timezone"""
    if dt is None:
        dt = get_indian_time()
    elif dt.tzinfo is None:
        # Convert naive datetime to Indian timezone
        dt = INDIAN_TZ.localize(dt)
    elif dt.tzinfo != INDIAN_TZ:
        # Convert to Indian timezone
        dt = dt.astimezone(INDIAN_TZ)
    return dt.strftime(format_str)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# Create the app
app = Flask(__name__)
# Hardcoded configuration - no environment variables needed
app.secret_key = os.environ.get("SESSION_SECRET") or "battery_erp_secret_key_hardcoded_2025_production"
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure the database - use PostgreSQL for production, fallback to hardcoded values
database_url = os.environ.get("DATABASE_URL") or "postgresql://erp_user:erp_secure_pass_2025@localhost:5432/battery_repair_db"
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # type: ignore
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

def initialize_database():
    """Initialize database with default users and settings"""
    from models import User, SystemSettings
    from werkzeug.security import generate_password_hash
    
    # Create default users if they don't exist
    if not User.query.filter_by(username='admin').first():
        admin_user = User()
        admin_user.username = 'admin'
        admin_user.password_hash = generate_password_hash('admin123')
        admin_user.role = 'admin'
        admin_user.full_name = 'Administrator'
        db.session.add(admin_user)
    
    if not User.query.filter_by(username='staff').first():
        staff_user = User()
        staff_user.username = 'staff'
        staff_user.password_hash = generate_password_hash('staff123')
        staff_user.role = 'shop_staff'
        staff_user.full_name = 'Shop Staff'
        db.session.add(staff_user)
    
    if not User.query.filter_by(username='technician').first():
        tech_user = User()
        tech_user.username = 'technician'
        tech_user.password_hash = generate_password_hash('tech123')
        tech_user.role = 'technician'
        tech_user.full_name = 'Technician'
        db.session.add(tech_user)
    
    # Initialize system settings
    default_settings = [
        ('shop_name', 'Battery Repair Service'),
        ('battery_id_prefix', 'BAT'),
        ('battery_id_start', '1'),
        ('battery_id_padding', '4')
    ]
    
    for key, value in default_settings:
        if not SystemSettings.query.filter_by(setting_key=key).first():
            setting = SystemSettings()
            setting.setting_key = key
            setting.setting_value = value
            db.session.add(setting)
    
    try:
        db.session.commit()
    except Exception as e:
        logging.error(f"Error creating default users and settings: {e}")
        db.session.rollback()

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    initialize_database()

# Register blueprints
from auth import auth_bp
from routes import main_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

# Add template globals for time functions
@app.template_global()
def current_indian_time():
    """Template function to get current Indian time"""
    return get_indian_time()

@app.template_global()
def format_time(dt, format_str='%d/%m/%Y %H:%M'):
    """Template function to format time in Indian timezone"""
    return format_indian_time(dt, format_str)

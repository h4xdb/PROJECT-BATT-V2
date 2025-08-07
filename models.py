from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import func
import pytz

# Indian timezone
INDIAN_TZ = pytz.timezone('Asia/Kolkata')

def get_indian_now():
    """Get current time in Indian timezone"""
    return datetime.now(INDIAN_TZ).replace(tzinfo=None)  # Store as naive datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'shop_staff', or 'technician'
    full_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=get_indian_now)
    active = db.Column(db.Boolean, default=True)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    mobile_secondary = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, default=get_indian_now)
    
    # Relationship with batteries
    batteries = db.relationship('Battery', backref='customer', lazy=True)

class Battery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    battery_id = db.Column(db.String(20), unique=True, nullable=False)  # BAT0001, BAT0002, etc.
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    battery_type = db.Column(db.String(100), nullable=False)
    voltage = db.Column(db.String(10), nullable=False)  # e.g., "12V"
    capacity = db.Column(db.String(10), nullable=False)  # e.g., "100Ah"
    status = db.Column(db.String(20), default='Received', nullable=False)  # Received, Pending, Ready, Delivered, Returned, Not Repairable
    inward_date = db.Column(db.DateTime, default=get_indian_now)
    service_price = db.Column(db.Float, default=0.0)
    pickup_charge = db.Column(db.Float, default=0.0)  # Extra charge for pickup service
    is_pickup = db.Column(db.Boolean, default=False)  # Whether battery was picked up by employees
    
    # Relationship with status history and staff notes
    status_history = db.relationship('BatteryStatusHistory', backref='battery', lazy=True, cascade='all, delete-orphan')
    staff_notes = db.relationship('BatteryStaffNote', backref='battery', lazy=True, cascade='all, delete-orphan')
    
    @staticmethod
    def generate_next_battery_id():
        """Generate the next sequential battery ID using system settings"""
        from app import db
        
        prefix = SystemSettings.get_setting('battery_id_prefix', 'BAT')
        start_num = int(SystemSettings.get_setting('battery_id_start', '1'))
        padding = int(SystemSettings.get_setting('battery_id_padding', '4'))
        
        last_battery = Battery.query.order_by(Battery.id.desc()).first()
        if last_battery:
            # Extract number from last battery ID (e.g., BAT0001 -> 1)
            try:
                last_num = int(last_battery.battery_id[len(prefix):])
                next_num = last_num + 1
            except (ValueError, IndexError):
                next_num = start_num
        else:
            next_num = start_num
        
        return f"{prefix}{next_num:0{padding}d}"

class BatteryStatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    battery_id = db.Column(db.Integer, db.ForeignKey('battery.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    comments = db.Column(db.Text)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_at = db.Column(db.DateTime, default=get_indian_now)
    
    # Relationship
    user = db.relationship('User', backref='status_updates')

class BatteryStaffNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    battery_id = db.Column(db.Integer, db.ForeignKey('battery.id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    note_type = db.Column(db.String(50), default='followup')  # followup, reminder, issue, resolved
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=get_indian_now)
    is_resolved = db.Column(db.Boolean, default=False)
    
    # Relationship
    user = db.relationship('User', backref='staff_notes')

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_code = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # acid, plates, separators, terminals, etc.
    unit = db.Column(db.String(20), nullable=False)  # liters, pieces, kg, etc.
    current_stock = db.Column(db.Float, default=0.0)
    minimum_stock = db.Column(db.Float, default=0.0)
    unit_cost = db.Column(db.Float, default=0.0)
    supplier = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=get_indian_now)
    last_updated = db.Column(db.DateTime, default=get_indian_now)
    active = db.Column(db.Boolean, default=True)
    
    # Relationships
    stock_transactions = db.relationship('StockTransaction', backref='inventory_item', lazy=True)
    material_usage = db.relationship('BatteryMaterialUsage', backref='inventory_item', lazy=True)

class StockTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inventory_item_id = db.Column(db.Integer, db.ForeignKey('inventory_item.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # purchase, usage, adjustment, return
    quantity = db.Column(db.Float, nullable=False)
    unit_cost = db.Column(db.Float, default=0.0)
    total_cost = db.Column(db.Float, default=0.0)
    reference_id = db.Column(db.String(50))  # purchase order, battery ID, etc.
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=get_indian_now)
    
    # Relationships
    user = db.relationship('User', backref='stock_transactions')

class BatteryMaterialUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    battery_id = db.Column(db.Integer, db.ForeignKey('battery.id'), nullable=False)
    inventory_item_id = db.Column(db.Integer, db.ForeignKey('inventory_item.id'), nullable=False)
    quantity_used = db.Column(db.Float, nullable=False)
    unit_cost = db.Column(db.Float, default=0.0)
    total_cost = db.Column(db.Float, default=0.0)
    used_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    used_at = db.Column(db.DateTime, default=get_indian_now)
    notes = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', backref='material_usage')
    battery = db.relationship('Battery', backref='materials_used')

class SystemSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(50), unique=True, nullable=False)
    setting_value = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=get_indian_now)
    
    @staticmethod
    def get_setting(key, default_value=''):
        setting = SystemSettings.query.filter_by(setting_key=key).first()
        return setting.setting_value if setting else default_value
    
    @staticmethod
    def set_setting(key, value):
        setting = SystemSettings.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = value
            setting.updated_at = get_indian_now()
        else:
            setting = SystemSettings()
            setting.setting_key = key
            setting.setting_value = value
            from app import db
            db.session.add(setting)
        return setting

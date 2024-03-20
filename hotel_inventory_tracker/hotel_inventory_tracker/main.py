from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the Flask application
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and SocketIO
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Define models
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def add_item(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Error:", e)

    def remove_item(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Error:", e)

    def update_item(self, name=None, quantity=None, price=None):
        try:
            if name is not None:
                self.name = name
            if quantity is not None:
                self.quantity = quantity
            if price is not None:
                self.price = price
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Error:", e)

class InventoryManager:
    def add_item(self, item):
        item.add_item()

    def remove_item(self, id):
        item = Item.query.get(id)
        if item:
            item.remove_item()

    def update_item(self, id, data):
        item = Item.query.get(id)
        if item:
            item.update_item(**data)

    def get_low_stock_items(self):
        return Item.query.filter(Item.quantity < 10).all()

class ReportGenerator:
    @staticmethod
    def generate_report():
        items = pd.read_sql(Item.query.statement, db.session.bind)
        # Example report generation logic
        low_stock = items[items['quantity'] < 10]
        plt.figure(figsize=(10, 6))
        plt.bar(low_stock['name'], low_stock['quantity'])
        plt.title('Low Stock Items')
        plt.xlabel('Item Name')
        plt.ylabel('Quantity')
        plt.xticks(rotation=45)
        plt.tight_layout()
        report_path = os.path.join('static', 'reports', 'low_stock_report.png')
        plt.savefig(report_path)
        print("Report generated at:", report_path)

# Socket.IO event handlers
@socketio.on('add_item')
def handle_add_item(json):
    item = Item(name=json['name'], quantity=json['quantity'], price=json['price'])
    inventory_manager = InventoryManager()
    inventory_manager.add_item(item)
    emit('item_added', {'name': json['name'], 'quantity': json['quantity'], 'price': json['price']}, broadcast=True)

# Routes
@app.route('/')
def index():
    return "Hello, this is the inventory tracking app!"

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, debug=True)

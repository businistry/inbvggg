## app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import os

# Import models and forms
from models import db, Item, InventoryManager
from forms import ItemForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'you-will-never-guess')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
socketio = SocketIO(app)
with app.app_context():
    db.create_all()

inventory_manager = InventoryManager()

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    items = inventory_manager.get_all_items()
    return render_template('dashboard.html', items=items)

@app.route('/item/add', methods=['GET', 'POST'])
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        try:
            new_item = Item(name=form.name.data, quantity=form.quantity.data, price=form.price.data)
            inventory_manager.add_item(new_item)
            socketio.emit('update_inventory', {'message': 'Inventory updated'}, namespace='/inventory')
        except Exception as e:
            db.session.rollback()
            print(f"Error adding item: {e}")
        return redirect(url_for('dashboard'))
    return render_template('item_management.html', form=form, action='Add')

@app.route('/item/update/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    item = inventory_manager.get_item_by_id(id)
    if item is None:
        return redirect(url_for('dashboard'))
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        try:
            item.name = form.name.data
            item.quantity = form.quantity.data
            item.price = form.price.data
            db.session.commit()
            socketio.emit('update_inventory', {'message': 'Inventory updated'}, namespace='/inventory')
        except Exception as e:
            db.session.rollback()
            print(f"Error updating item: {e}")
        return redirect(url_for('dashboard'))
    return render_template('item_management.html', form=form, action='Update', item_id=id)

@app.route('/item/remove/<int:id>', methods=['POST'])
def remove_item(id):
    try:
        inventory_manager.remove_item(id)
        socketio.emit('update_inventory', {'message': 'Inventory updated'}, namespace='/inventory')
    except Exception as e:
        db.session.rollback()
        print(f"Error removing item: {e}")
    return redirect(url_for('dashboard'))

@app.route('/report')
def report():
    try:
        low_stock_items = inventory_manager.get_low_stock_items()
        report_path = inventory_manager.generate_report(low_stock_items)
    except Exception as e:
        db.session.rollback()
        print(f"Error generating report: {e}")
        report_path = None
    return render_template('report.html', report_path=report_path)

if __name__ == '__main__':
    socketio.run(app, debug=True)

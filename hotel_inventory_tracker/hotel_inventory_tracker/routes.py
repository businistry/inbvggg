## routes.py
from flask import Blueprint, request, render_template, redirect, url_for, current_app, flash
import logging

from .forms import ItemForm

# Create a Blueprint for the inventory routes
bp = Blueprint('inventory', __name__, template_folder='templates')

@bp.route('/')
def dashboard():
    """Route to display the dashboard with an overview of the inventory."""
    inventory_manager = current_app.inventory_manager
    low_stock_items = inventory_manager.get_low_stock_items()
    return render_template('dashboard.html', low_stock_items=low_stock_items)

@bp.route('/manage', methods=['GET', 'POST'])
def manage_item():
    """Route to add, remove, or update items in the inventory."""
    form = ItemForm()
    if form.validate_on_submit():
        inventory_manager = current_app.inventory_manager
        try:
            if form.action.data == 'Add':
                add_item(form, inventory_manager)
            elif form.action.data == 'Remove':
                remove_item(form, inventory_manager)
            elif form.action.data == 'Update':
                update_item(form, inventory_manager)
            flash('Operation successful!', 'success')
            return redirect(url_for('inventory.dashboard'))
        except ValueError as e:
            flash(str(e), 'error')
            logging.error(f"Error managing item: {e}")
    return render_template('item_management.html', form=form)

@bp.route('/report')
def report():
    """Route to display the inventory report."""
    inventory_manager = current_app.inventory_manager
    items = inventory_manager.items
    report_path = inventory_manager.generate_report(items)
    return render_template('report.html', report_path=report_path)

def add_item(form, inventory_manager):
    item_data = {
        'name': form.name.data,
        'quantity': form.quantity.data,
        'price': form.price.data
    }
    inventory_manager.add_item(item_data)

def remove_item(form, inventory_manager):
    item_id = int(form.item_id.data)
    if not inventory_manager.item_exists(item_id):
        raise ValueError("Item ID is invalid")
    inventory_manager.remove_item(item_id)

def update_item(form, inventory_manager):
    item_id = int(form.item_id.data)
    item_data = {
        'name': form.name.data,
        'quantity': form.quantity.data,
        'price': form.price.data
    }
    if not inventory_manager.item_exists(item_id):
        raise ValueError("Item ID is invalid")
    inventory_manager.update_item(item_id, item_data)

## models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, Column
import pandas as pd
import matplotlib.pyplot as plt

db = SQLAlchemy()

class Item(db.Model):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0.0)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def update(cls, id, data):
        cls.query.filter_by(id=id).update(data)
        db.session.flush()  # Apply the changes to the database.
        updated_item = cls.query.get(id)  # Fetch the updated item.
        db.session.commit()
        return updated_item

class InventoryManager:
    @staticmethod
    def add(item):
        item.add()

    @staticmethod
    def remove(id):
        item = Item.query.get(id)
        if item:
            item.remove()

    @staticmethod
    def update(id, data):
        return Item.update(id, data)

    @staticmethod
    def get_low_stock(threshold=10):
        return Item.query.filter(Item.quantity <= threshold).all()

class ReportGenerator:
    @staticmethod
    def generate(items):
        # Convert items to a DataFrame
        df = pd.DataFrame([{"id": item.id, "name": item.name, "quantity": item.quantity, "price": item.price} for item in items])
        # Generate a more detailed plot
        plt.figure(figsize=(10, 6))
        plt.scatter(df['quantity'], df['price'], alpha=0.5)
        plt.title('Inventory Report')
        plt.xlabel('Quantity')
        plt.ylabel('Price')
        plt.savefig('report.png')
        plt.close()
        # Additional visualization (example: histogram of item quantities)
        plt.figure(figsize=(10, 6))
        df['quantity'].plot(kind='hist', bins=20, alpha=0.7)
        plt.title('Item Quantity Distribution')
        plt.xlabel('Quantity')
        plt.ylabel('Frequency')
        plt.savefig('quantity_distribution.png')
        plt.close()
        return df.to_dict('records')

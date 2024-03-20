## utils.py
import pandas as pd
import matplotlib.pyplot as plt
from models import Item
from typing import List
import tempfile
import os
from PyPDF2 import PdfFileMerger
from reportlab.pdfgen import canvas

def generate_report(items: List[Item], report_path: str = "inventory_report.pdf") -> None:
    """
    Generates a report from a list of Item objects and saves it as a PDF.

    Args:
    - items (List[Item]): A list of Item objects to be included in the report.
    - report_path (str): The file path where the report will be saved. Defaults to "inventory_report.pdf".

    Returns:
    - None
    """
    if not items:
        raise ValueError("The items list cannot be empty.")

    data = {
        "ID": [item.id for item in items],
        "Name": [item.name for item in items],
        "Quantity": [item.quantity for item in items],
        "Price": [item.price for item in items]
    }
    df = pd.DataFrame(data)

    plt.figure(figsize=(10, 6))
    plt.bar(df["Name"], df["Quantity"], color='skyblue')
    plt.xlabel('Item Name')
    plt.ylabel('Quantity')
    plt.title('Inventory Stock Levels')
    plt.tight_layout()

    # Save the plot to a temporary file
    temp_plot_path = tempfile.mktemp(suffix=".pdf")
    plt.savefig(temp_plot_path)
    plt.close()

    # Create text content in a temporary PDF
    temp_text_path = tempfile.mktemp(suffix=".pdf")
    c = canvas.Canvas(temp_text_path)
    c.drawString(100, 750, "Inventory Report\n")
    text = c.beginText(40, 700)
    text.setFont("Helvetica", 10)
    for line in df.to_string(index=False).split('\n'):
        text.textLine(line)
    c.drawText(text)
    c.save()

    # Merge the plot and text PDFs
    merger = PdfFileMerger()
    merger.append(temp_plot_path)
    merger.append(temp_text_path)
    merger.write(report_path)
    merger.close()

    # Clean up temporary files
    os.remove(temp_plot_path)
    os.remove(temp_text_path)

    print(f"Report successfully generated and saved to {report_path}")

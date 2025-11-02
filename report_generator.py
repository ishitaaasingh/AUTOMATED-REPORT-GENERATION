"""
CODTECH Internship Task:
Automated Report Generation using Python, Pandas, Matplotlib & ReportLab
Author: Ishita Singh
Deliverable: A script that reads data from a file, analyzes it, and generates a formatted PDF report.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import cm
from datetime import datetime
import os

# ---------- Step 1: Setup ----------
output_folder = "report_output"
os.makedirs(output_folder, exist_ok=True)
csv_file = os.path.join(output_folder, "sales_data.csv")

# ---------- Step 2: Create Sample Dataset ----------
np.random.seed(10)
dates = pd.date_range(start="2025-01-01", periods=100)
categories = ["Electronics", "Clothing", "Books", "Food"]
data = {
    "Date": np.random.choice(dates, 120),
    "Category": np.random.choice(categories, 120),
    "Amount": np.round(np.random.uniform(50, 1000, 120), 2)
}
df = pd.DataFrame(data)
df.to_csv(csv_file, index=False)

# ---------- Step 3: Analyze the Data ----------
summary = {
    "Total Transactions": len(df),
    "Total Amount": df["Amount"].sum(),
    "Average Amount": df["Amount"].mean(),
    "Highest Sale": df["Amount"].max(),
    "Lowest Sale": df["Amount"].min()
}

category_totals = df.groupby("Category")["Amount"].agg(["count", "sum", "mean"]).reset_index()

# ---------- Step 4: Create Charts ----------
plt.figure(figsize=(6, 4))
plt.bar(category_totals["Category"], category_totals["sum"], color="skyblue")
plt.title("Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales (₹)")
chart_path = os.path.join(output_folder, "chart.png")
plt.tight_layout()
plt.savefig(chart_path)
plt.close()

# ---------- Step 5: Generate PDF Report ----------
pdf_path = os.path.join(output_folder, "report.pdf")
doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
styles = getSampleStyleSheet()
story = []

# Title
story.append(Paragraph("CODTECH Internship Task", styles["Title"]))
story.append(Spacer(1, 12))
story.append(Paragraph("Automated Data Report", styles["Heading1"]))
story.append(Spacer(1, 12))
story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
story.append(Spacer(1, 20))

# Summary Table
story.append(Paragraph("<b>Summary Statistics</b>", styles["Heading2"]))
data_summary = [[k, f"{v:,.2f}" if isinstance(v, float) else v] for k, v in summary.items()]
table = Table(data_summary, hAlign="LEFT", colWidths=[8*cm, 6*cm])
table.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
    ("ALIGN", (1, 1), (-1, -1), "RIGHT")
]))
story.append(table)
story.append(Spacer(1, 12))

# Category Table
story.append(Paragraph("<b>Category Totals</b>", styles["Heading2"]))
cat_table_data = [category_totals.columns.tolist()] + category_totals.round(2).values.tolist()
cat_table = Table(cat_table_data, hAlign="LEFT")
cat_table.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
]))
story.append(cat_table)
story.append(Spacer(1, 12))

# Add Chart
story.append(Paragraph("<b>Visual Summary</b>", styles["Heading2"]))
story.append(Spacer(1, 8))
story.append(Image(chart_path, width=14*cm, height=8*cm))
story.append(Spacer(1, 20))

# Footer
story.append(Paragraph("Generated automatically using Python 🐍", styles["Normal"]))
story.append(Spacer(1, 12))
story.append(Paragraph("Prepared by: <b>Ishita Singh</b>", styles["Normal"]))
story.append(Spacer(1, 12))
story.append(Paragraph("For: CODTECH Internship Project", styles["Normal"]))

doc.build(story)

print(f"\n✅ Report generated successfully!\nCheck the folder: {output_folder}")

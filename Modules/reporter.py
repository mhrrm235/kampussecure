import csv
from fpdf import FPDF
import os
from datetime import datetime

def export_to_csv(data, filename="reports/history.csv"):
    os.makedirs("reports", exist_ok=True)
    with open(filename, mode="w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Target", "Scan Type", "Result", "Timestamp"])
        writer.writerows(data)

def export_to_pdf(data, filename="reports/scan_result.pdf"):
    os.makedirs("reports", exist_ok=True)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Hasil Scan KampusSecure", ln=True, align='C')

    for item in data:
        target, scan_type, result, timestamp = item
        pdf.multi_cell(0, 10, f"Target: {target}\nScan Type: {scan_type}\nResult: {result}\nTimestamp: {timestamp}\n")
        pdf.ln()

    pdf.output(filename)

from fpdf import FPDF
import csv
import datetime
import os

def generate_pdf():
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = f"reports/scan_result_{timestamp}.pdf"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Laporan Hasil Scan", ln=True, align='C')

        with open('reports/history.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                pdf.multi_cell(0, 10, txt=", ".join(row))

        pdf.output(pdf_path)
        return pdf_path
    except Exception as e:
        return f"Error generating PDF: {e}"

def generate_csv():
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f"reports/scan_result_{timestamp}.csv"

        with open('reports/history.csv', 'r') as infile, open(csv_path, 'w', newline='') as outfile:
            data = infile.read()
            outfile.write(data)

        return csv_path
    except Exception as e:
        return f"Error generating CSV: {e}"

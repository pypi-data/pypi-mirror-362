import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF

def generate_report(data: pd.DataFrame, filename="topsisx_report.pdf"):
    """
    Generate a PDF report with rankings and charts.
    """
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add title
    pdf.cell(200, 10, txt="TOPSISX Decision Report", ln=True, align="C")
    pdf.ln(10)

    # Add table
    pdf.cell(200, 10, txt="Rankings Table:", ln=True)
    pdf.ln(5)
    for i, row in data.iterrows():
        row_str = " | ".join(str(x) for x in row)
        pdf.cell(200, 8, txt=row_str, ln=True)

    # Add chart
    plt.barh(data.iloc[:, 0], data["Topsis Score"])
    plt.xlabel("Topsis Score")
    plt.title("Ranking Scores")
    plt.tight_layout()
    plt.savefig("chart.png")
    plt.close()

    pdf.add_page()
    pdf.cell(200, 10, txt="Ranking Chart:", ln=True)
    pdf.image("chart.png", x=10, y=30, w=180)

    # Save PDF
    pdf.output(filename)
    print(f"✅ Report saved as {filename}")

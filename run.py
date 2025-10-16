# run.py

from coordinator import orchestrate

if __name__ == "__main__":
    path = 'sample_input.pdf'
    orchestrate(path, output_pdf="final_financial_report.pdf")

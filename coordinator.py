# import json
# import pandas as pd
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from Feed_Data_Functions import parse_csv, parse_excel, parse_pdf, parse_docx, normalize_financial_table
# from agents import (
#     create_data_ingest_agent,
#     create_risk_agent,
#     create_strategy_agent,
#     create_team,
# )

# def load_file(path):
#     print("11111111")
#     if path.endswith(".csv"):
#         return parse_csv(path)
#     if path.endswith(".xlsx") or path.endswith(".xls"):
#         return parse_excel(path)
#     if path.endswith(".pdf"):
#         print("eeeeeeeeeee")
#         return parse_pdf(path)
#     if path.endswith(".docx"):
#         return parse_docx(path)
#     raise ValueError("Unsupported file type")

# def df_to_json_summary(df: pd.DataFrame):
#     head = df.head(5).to_dict(orient="records")
#     cols = list(df.columns)
#     dtypes = {c: str(df[c].dtype) for c in df.columns}
#     return {"columns": cols, "dtypes": dtypes, "sample_rows": head, "rows": len(df)}

# def generate_pdf_report(filename: str, title: str, sections: dict):
#     c = canvas.Canvas(filename, pagesize=A4)
#     width, height = A4
#     y = height - 50
#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(40, y, title)
#     y -= 30
#     c.setFont("Helvetica", 10)
#     for section_title, content in sections.items():
#         if y < 120:
#             c.showPage()
#             y = height - 60
#             c.setFont("Helvetica", 10)
#         c.setFont("Helvetica-Bold", 12)
#         c.drawString(40, y, section_title)
#         y -= 18
#         c.setFont("Helvetica", 10)
#         lines = str(content).split("\n")
#         for line in lines:
#             for chunk in [line[i:i+120] for i in range(0, len(line), 120)]:
#                 c.drawString(45, y, chunk)
#                 y -= 12
#                 if y < 60:
#                     c.showPage()
#                     y = height - 60
#         y -= 8
#     c.save()

# def orchestrate(file_path: str, output_pdf="financial_report.pdf"):
#     ingest_agent = create_data_ingest_agent()
#     risk_agent = create_risk_agent()
#     strat_agent = create_strategy_agent()
#     team = create_team([ingest_agent, risk_agent, strat_agent])

#     print("ffffffffff",team)

#     raw = load_file(file_path)
#     if isinstance(raw, pd.DataFrame):
#         df = normalize_financial_table(raw)
#         summary = df_to_json_summary(df)
#     else:
#         summary = {"text": raw[:5000]}

#     ingest_prompt = f"Input data summary:\n{json.dumps(summary)}\n\nExtract structured financial information and summarize in JSON."
#     ingest_resp = ingest_agent.run(ingest_prompt)
#     ingest_output = getattr(ingest_resp, "content", str(ingest_resp))

#     risk_prompt = f"Structured data:\n{ingest_output}\n\nCompute risk metrics and short interpretation (JSON)."
#     risk_resp = risk_agent.run(risk_prompt)
#     risk_output = getattr(risk_resp, "content", str(risk_resp))

#     strat_prompt = f"Data:\n{ingest_output}\nRisk metrics:\n{risk_output}\n\nProvide strategy recommendations and executive summary."
#     strat_resp = strat_agent.run(strat_prompt)
#     strat_output = getattr(strat_resp, "content", str(strat_resp))

#     sections = {
#         "Input File": file_path,
#         "Data Ingestion": ingest_output,
#         "Risk Analysis": risk_output,
#         "Strategy Recommendations": strat_output,
#     }

#     generate_pdf_report(output_pdf, "Consolidated Financial Report", sections)
#     print("✅ Report generated:", output_pdf)



from PyPDF2 import PdfReader
from docx import Document
import mimetypes
import json
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from agents import create_data_ingest_agent, create_risk_agent, create_strategy_agent, create_team
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from datetime import datetime
import json

# Utility Functions
def load_file(file_path):
    """Load data from multiple formats: CSV, Excel, JSON, PDF, DOCX, TXT."""
    try:
        mime, _ = mimetypes.guess_type(file_path)

        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)

        elif file_path.endswith((".xls", ".xlsx")):
            return pd.read_excel(file_path)

        elif file_path.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)

        elif file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
            return text.strip()

        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
            return text.strip()

        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        else:
            return f"⚠️ Unsupported file format: {file_path}"

    except Exception as e:
        return f"❌ Error loading file: {e}"


def normalize_financial_table(df: pd.DataFrame):
    """Perform basic cleaning."""
    df = df.dropna(how="all")
    df.columns = [c.strip().replace("\n", "_") for c in df.columns]
    return df


def df_to_json_summary(df: pd.DataFrame, n_rows=5):
    """Convert a DataFrame to a JSON summary."""
    return {
        "columns": list(df.columns),
        "dtypes": {c: str(df[c].dtype) for c in df.columns},
        "sample": df.head(n_rows).to_dict(orient="records"),
        "shape": df.shape,
    }


# ------------------------ PDF Generation ------------------------

def generate_pdf_report(output_path, title, sections):
    """Generate a professional and readable PDF financial report."""
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        alignment=1,
        spaceAfter=30,
        fontSize=20,
        textColor="#003366"
    )
    header_style = ParagraphStyle(
        "HeaderStyle",
        parent=styles["Heading2"],
        textColor="#1a5276",
        spaceAfter=12
    )
    normal_text = styles["Normal"]

    # Create document
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    content = []

    # Cover Page
    content.append(Paragraph(title, title_style))
    content.append(Paragraph(f"Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", normal_text))
    content.append(Paragraph("Prepared by: Agno Multi-Agent Financial Analysis System", normal_text))
    content.append(Spacer(1, 40))
    content.append(PageBreak())

    # Section by section
# Section by section
    for section_title, data in sections.items():
        content.append(Paragraph(section_title, header_style))
        content.append(Spacer(1, 6))

        # Format JSON/text data nicely
        if isinstance(data, (dict, list)):
            formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
            formatted_data = formatted_data.replace("\n", "<br />")  # Wrap lines
            content.append(Paragraph(formatted_data, normal_text))
        else:
            formatted_data = str(data).replace("\n", "<br />")
            content.append(Paragraph(formatted_data, normal_text))

        content.append(Spacer(1, 20))
        content.append(PageBreak())


    # Build PDF
    doc.build(content)
    print(f"✅ Professional Financial Report generated: {output_path}")
# ------------------------ Main Orchestration ------------------------

# def orchestrate(file_path: str, output_pdf="financial_report.pdf"):
#     ingest_agent = create_data_ingest_agent()
#     risk_agent = create_risk_agent()
#     strat_agent = create_strategy_agent()
#     team = create_team([ingest_agent, risk_agent, strat_agent])

#     print("✅ Team created:", team)

#     raw = load_file(file_path)
#     if isinstance(raw, pd.DataFrame):
#         df = normalize_financial_table(raw)
#         summary = df_to_json_summary(df)
#     else:
#         summary = {"text": str(raw)[:5000]}

#     # ----------- Ingestion Agent -----------
#     ingest_prompt = f"Input data summary:\n{json.dumps(summary)}\n\nExtract structured financial information and summarize in JSON."
#     ingest_resp = ingest_agent.run(ingest_prompt)
#     ingest_output = getattr(ingest_resp, "content", str(ingest_resp))

#     # ----------- Risk Agent -----------
#     risk_prompt = f"Structured data:\n{ingest_output}\n\nCompute risk metrics and short interpretation (JSON)."
#     risk_resp = risk_agent.run(risk_prompt)
#     risk_output = getattr(risk_resp, "content", str(risk_resp))

#     # ----------- Strategy Agent -----------
#     strat_prompt = f"Data:\n{ingest_output}\nRisk metrics:\n{risk_output}\n\nProvide strategy recommendations and executive summary."
#     strat_resp = strat_agent.run(strat_prompt)
#     strat_output = getattr(strat_resp, "content", str(strat_resp))

#     # ----------- Consolidate & Generate PDF -----------
#     sections = {
#         "Input File": file_path,
#         "Data Ingestion Output": ingest_output,
#         "Risk Analysis Output": risk_output,
#         "Strategy Recommendations": strat_output,
#     }

#     generate_pdf_report(output_pdf, "Consolidated Financial Report", sections)
#     print("📘 Financial Report generated:", output_pdf)
def orchestrate(file_path: str, output_pdf="financial_report.pdf"):
    ingest_agent = create_data_ingest_agent()
    risk_agent = create_risk_agent()
    strat_agent = create_strategy_agent()
    team = create_team([ingest_agent, risk_agent, strat_agent])

    print("✅ Team created:", team)

    raw = load_file(file_path)
    if isinstance(raw, pd.DataFrame):
        df = normalize_financial_table(raw)
        # Convert to readable bullet-point text instead of JSON
        summary = "\n".join([f"- {col.replace('_', ' ').title()}: {df[col].iloc[0]}" for col in df.columns])
    else:
        summary = str(raw)[:5000]

    # ----------- Ingestion Agent -----------
    ingest_prompt = f"Summarize the uploaded financial data for a professional client report:\n{summary}"
    ingest_resp = ingest_agent.run(ingest_prompt)
    ingest_output = getattr(ingest_resp, "content", str(ingest_resp))

    # ----------- Risk Agent -----------
    risk_prompt = f"Analyze financial risks based on the following data:\n{ingest_output}\nProvide readable insights for management."
    risk_resp = risk_agent.run(risk_prompt)
    risk_output = getattr(risk_resp, "content", str(risk_resp))

    # ----------- Strategy Agent -----------
    strat_prompt = f"Provide strategic recommendations based on data and risk analysis:\nData:\n{ingest_output}\nRisk Insights:\n{risk_output}\nOutput in readable client-ready text."
    strat_resp = strat_agent.run(strat_prompt)
    strat_output = getattr(strat_resp, "content", str(strat_resp))

    # ----------- Consolidate & Generate PDF -----------
    sections = {
        "Executive Summary": ingest_output,
        "Key Financial Indicators": summary,
        "Risk Analysis": risk_output,
        "Strategic Recommendations": strat_output,
        "Conclusion": "Overall, the company's financial health is stable. Following the recommendations above will help manage risk and optimize strategic growth."
    }

    generate_pdf_report(output_pdf, "Consolidated Financial Report", sections)
    print("📘 Financial Report generated:", output_pdf)

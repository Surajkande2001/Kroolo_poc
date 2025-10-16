import pandas as pd
import pdfplumber
from docx import Document

def parse_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def parse_excel(path: str) -> pd.DataFrame:
    return pd.read_excel(path)

def parse_pdf(path: str) -> str:
    texts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            texts.append(page.extract_text() or "")
    print(f"text  {texts}")
    return "\n".join(texts)

def parse_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def normalize_financial_table(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=str.lower)
    for c in df.columns:
        try:
            df[c] = pd.to_numeric(df[c].str.replace(',', ''), errors='ignore')
        except Exception:
            pass
    return df

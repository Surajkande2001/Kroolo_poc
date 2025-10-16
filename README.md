# Agno Multi-Agent Financial Reporting System

This project uses the [Agno Multi-Agent Framework](https://github.com/agnoframework) to analyze financial data from multiple file formats and generate a professional PDF report using autonomous agents.

## 💡 Features

- Multi-agent architecture with specialized agents:
  - **DataIngestAgent** – Parses & summarizes financial data
  - **RiskAgent** – Performs market & portfolio risk analysis
  - **StrategyAgent** – Recommends strategic investment decisions
- Supports input formats: CSV, Excel, PDF, DOCX, JSON, TXT
- Generates clean, client-ready PDF financial reports
- Uses LLMs via Azure OpenAI for insights and reasoning

## 🏗️ Project Structure

📁 agno-financial-reporting/
├── agents.py # Defines agents & roles
├── coordinator.py # Main orchestration logic
├── report_utils.py # PDF generation utility
├── run.py # Entry point to run the pipeline
├── config.py # API keys and configurations
├── requirements.txt # Dependencies


## 🚀 Setup

### Prerequisites

- Python 3.9+
- Azure OpenAI API key (for GPT-based reasoning)
- `agno` Python SDK (pip install agno)

### Installation

```bash
git clone https://github.com/yourusername/agno-financial-reporting.git
cd agno-financial-reporting
pip install -r requirements.txt

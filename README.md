# OOC-Hack
# 📝 RFP Eligibility Analyzer

> A privacy-first, local tool to analyze RFP documents and determine your company's eligibility to bid.


---

## 🚀 Overview

The **RFP Eligibility Analyzer** helps organizations quickly determine if they qualify to respond to a Request for Proposal (RFP). Built with **Streamlit** and powered by a lightweight **local language model** (like OPT-125M), this tool ensures all your sensitive data stays secure—on your device.

---

## 🔍 Features

- ✅ **Upload & Analyze** RFPs and company profiles (PDF, DOCX, TXT)
- 🧠 **Auto-summarize** RFP content
- 📌 **Extract key eligibility criteria** (Critical, Important, Nice-to-have)
- 🏢 **Evaluate your company** against RFP requirements
- 📄 **Generate HTML reports** for download
- 🔐 **Privacy-first**: 100% local, no cloud APIs

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/)
- [Transformers](https://huggingface.co/docs/transformers/index)
- [OPT-125M](https://huggingface.co/facebook/opt-125m) or other local language models
- `PyMuPDF`, `python-docx`, `BeautifulSoup` for document parsing
- HTML report generation

---

📸 How It Works
Upload your RFP and company profile documents

Click Analyze Documents

Review:

RFP Summary

Eligibility Criteria

Company Evaluation

Final Verdict

Download a detailed HTML report

✅ Supported File Types
.pdf

.docx

.txt

🔐 Privacy & Security
This app runs entirely offline. All processing (RFP analysis, summarization, evaluation) happens on your machine using open-source models. Your documents never leave your computer.

🧪 Example Use Cases
Bid/No-Bid decisions

Pre-sales qualification

Government RFP compliance

Proposal planning and strategy

📌 Future Improvements
RAG (Retrieval-Augmented Generation) integration

Risk analysis and mitigation detection

Interactive checklist generator

Support for larger models via quantization (e.g., LLaMA)


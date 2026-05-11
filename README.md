# 📧 Cold Mail Generator

An AI-powered tool that generates personalized cold emails by scraping job description URLs and matching your portfolio to the role's requirements.

---

## Live Demo: https://cold-mail-generator-kyawktdabxojkrrqjgzf6s.streamlit.app/

 ## How It Works

1. **Scrape** – The app fetches the job description page from the provided URL.
2. **Extract** – A LLaMA 3.1 model (via Groq) parses the page and extracts structured job info: role, required skills, experience, and description.
3. **Match** – Your portfolio (stored in ChromaDB as vector embeddings) is queried to find the most relevant project links based on the job's tech stack.
4. **Generate** – The LLM writes a professional cold email from the perspective of a Business Development Executive, referencing matched portfolio links.

Job URL ──► Web Scraper ──► LLM Extraction ──► ChromaDB Query ──► Cold Email


## Tech Stack

| Layer | Tool |
|---|---|
| LLM | LLaMA 3.1 8B via [Groq](https://groq.com) |
| Orchestration | [LangChain](https://www.langchain.com/) |
| Vector Store | [ChromaDB](https://www.trychroma.com/) |
| Frontend | [Streamlit](https://streamlit.io/) |
| Data | Pandas + CSV portfolio file |

---

## 📁 Project Structure
 
Cold-mail-Generator/
│
├── app.py                  # Main Streamlit app — scrapes URL, extracts job info, generates email
├── my_portfolio.csv        # Your portfolio data (Techstack + Links columns)
├── requirements.txt        # Python dependencies
│
├── vector_db/              # Persisted ChromaDB vector store (auto-created on first run)
│   └── ...
│
└── .streamlit/
    └── secrets.toml        # API key config (not committed — add to .gitignore)
 

## Setup & Installation

### 1. Clone the repository

bash
git clone https://github.com/your-username/cold-mail-generator.git
cd cold-mail-generator

### 2. Install dependencies

bash
pip install -r requirements.txt


### 3. Add your portfolio data

Edit `my_portfolio.csv` with your own projects:

csv
Techstack,Links
"React, Node.js, MongoDB",https://github.com/you/project-1
"Python, FastAPI, PostgreSQL",https://github.com/you/project-2


### 4. Set up your API key

Create a `.streamlit/secrets.toml` file:

toml
LLAMA_API_KEY = "your_groq_api_key_here"

Get your free API key at [console.groq.com](https://console.groq.com).

### 5. Run the app

bash
streamlit run app.py


## 📋 Requirements

streamlit
langchain
langchain-groq
langchain-community
chromadb
pandas
```

> Add these to a `requirements.txt` file.

## Environment Variables

| Variable | Description |
|---|---|
| `LLAMA_API_KEY` | Your Groq API key for LLaMA inference |


## Notes

- The ChromaDB vector store is populated once on first run and persisted locally in the `vector_db/` folder.
- The app scrapes publicly accessible job pages. Some sites may block automated requests.
- The generated email is written from the persona of **Mohan**, a BDE at **AtliQ** — customize the email prompt in `app.py` to match your own identity.

---
 

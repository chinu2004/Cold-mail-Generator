import os
import uuid
import chromadb
import pandas as pd
import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import JsonOutputParser

# -----------------------------
# Load portfolio data
# -----------------------------
df = pd.read_csv("my_portfolio.csv")

client = chromadb.PersistentClient(path="vector_db")
collection = client.get_or_create_collection(name="my_portfolio")

# Add data only once
if collection.count() == 0:
    for _, row in df.iterrows():
        collection.add(
            documents=[row["Techstack"]],
            metadatas=[{"links": row["Links"]}],
            ids=[str(uuid.uuid4())]
        )
api_key = st.secrets["LLAMA_API_KEY"]
# -----------------------------
# LLM setup
# -----------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=api_key,
    temperature=0.3
)

# -----------------------------
# Core function
# -----------------------------
def cold_mail(user_input: str) -> str:
    loader = WebBaseLoader(
        user_input,
        header_template={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
    )

    docs = loader.load()
    page_text = docs[0].page_content

    # -------- Extract job info --------
    prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT:
        {page_data}

        ### TASK:
        Extract the job information and return ONLY valid JSON with these keys:
        - role
        - experience
        - skill
        - description

        ### JSON ONLY (no explanation):
        """
    )

    chain_extract = prompt_extract | llm | JsonOutputParser()

    job = chain_extract.invoke({"page_data": page_text})

    # -------- Query portfolio --------
    skills_text = ", ".join(job.get("skill", [])) if isinstance(job.get("skill"), list) else str(job.get("skill"))

    results = collection.query(
        query_texts=[skills_text],
        n_results=2
    )

    links = []
    for meta in results.get("metadatas", []):
        for m in meta:
            links.append(m["links"])

    # -------- Generate email --------
    prompt_email = PromptTemplate.from_template(
        """
        ### JOB DETAILS:
        {job_description}

        ### INSTRUCTION:
        You are Mohan, a Business Development Executive at AtliQ (AI & Software Consulting).
        Write a professional cold email explaining how AtliQ can help fulfill this role.

        Include relevant portfolio links from here:
        {link_list}

        Maintain a professional and polite tone
        No preamble. Direct email only.
        the email should be concise and to the point.

        ### EMAIL:
        """
    )

    chain_email = prompt_email | llm
    response = chain_email.invoke(
        {
            "job_description": str(job),
            "link_list": "\n".join(links)
        }
    )

    # ✅ RETURN STRING ONLY
    return response.content


# -----------------------------
# Streamlit UI
# -----------------------------
if __name__ == "__main__":
    st.set_page_config(
        page_title="Cold Mail Generator",
        page_icon="📧",
        layout="centered"
    )

    st.title("📧 Cold Mail Generator")
    st.caption("Generate personalized cold emails from job description URLs")

    url_input = st.text_input(
        "Enter a job description URL",
        placeholder="https://careers.nike.com/senior-maintenance-technician-air-mi/job/R-72244"
    )

    if st.button("Generate"):
        if not url_input:
            st.warning("⚠️ Please enter a URL")
        elif not url_input.startswith(("http://", "https://")):
            st.error("❌ URL must start with http:// or https://")
        else:
            with st.spinner("Writing cold mail..."):
                try:
                    email_text = cold_mail(url_input)

                    st.success("✅ Cold mail generated successfully!")
                    st.subheader("✉️ Generated Cold Mail")
                    st.markdown(email_text)

                except Exception as e:
                    st.error("❌ Something went wrong")
                    st.exception(e)

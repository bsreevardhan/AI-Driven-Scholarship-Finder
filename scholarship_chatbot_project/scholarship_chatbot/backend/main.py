from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Load and preprocess data ---
df = pd.read_csv("structured_scholarships wo Desired.csv")
docs = df.apply(lambda row: f"{row['Name']}: {row['Description']} Eligibility: {row['Income Eligibility']}, {row['Qualification']}, {row['Special Criteria']}", axis=1).tolist()

# --- Create or load FAISS index ---
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(docs, show_progress_bar=True)
index = faiss.IndexFlatL2(embeddings[0].shape[0])
index.add(np.array(embeddings))

# --- FastAPI app ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    question_embedding = model.encode([query.question])[0].astype("float32")
    D, I = index.search(np.array([question_embedding]), k=1)
    top_idx = I[0][0]
    match = df.iloc[top_idx]
    answer = f"{match['Name']}\n{match['Description']}\nEligibility: {match['Income Eligibility']}, {match['Qualification']}, {match['Special Criteria']}\nApply: {match['Registration Link']}"
    return {"answer": answer}

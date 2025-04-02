import json
import streamlit as st
import os
os.environ["STREAMLIT_SERVER_WATCHER_IGNORE"] = "torch"
os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load a generative model & tokenizer (e.g., FLAN-T5)
model_path = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# Set device
device = torch.device("cpu")
model.to(device)

# Load class data from JSON file
with open("class_data.json", "r") as f:
    data = json.load(f)
qa_data = data.get("qa_data", [])

def get_best_context(question, qa_data):
    best_context = None
    best_score = 0
    question_words = set(question.lower().split())
    for entry in qa_data:
        entry_context = entry.get("context", "").lower()
        context_words = set(entry_context.split())
        common = question_words.intersection(context_words)
        score = len(common) / (len(context_words) + 1e-5)
        if score > best_score:
            best_score = score
            best_context = entry.get("context", "")
    # Only return context if there is at least one meaningful overlap
    if best_score > 0:
        return best_context
    return None
# Streamlit UI
st.title("Insight AI 🎓")
st.subheader("What would you like insight on today?")

# User input for question
question = st.text_input("Enter your question:")

if st.button("Press for Answer"):
    if question:
        best_context = get_best_context(question, qa_data)
        if best_context:
            prompt = (
                f"You are an AI teaching assistant. Carefully read the context below and use it to answer the question "
                f"in at least three complete, detailed sentences.\n\n"
                f"Context:\n{best_context}\n\n"
                f"Question: {question}\n\n"
                f"Detailed Answer:"
            )
        else:
            prompt = (
                f"You are an AI teaching assistant. Answer the question in at least three complete, detailed sentences.\n\n"
                f"Question: {question}\n\n"
                f"Detailed Answer:"
            )
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        
        # Generate the answer with a set maximum token limit (adjust as needed)
        outputs = model.generate(
            inputs.input_ids, 
            max_new_tokens=150,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True,
            temperature=0.7
        )
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        st.success(f"AI Answer: {answer}")
    else:
        st.warning("Please enter a question.")
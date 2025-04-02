import streamlit as st
import json

# Load data from JSON
with open("class_data.json", "r") as f:
    data = json.load(f)

# Title
st.title("👩‍🏫 Teacher Dashboard")

# Section to add a new question and context
st.header("Add New Lesson Context")

new_context = st.text_area("Enter Lesson Context:")

if st.button("Add Lesson"):
    if new_context.strip():
        new_entry = {
            "context": new_context.strip(),
            "question": "",
            "answers": {
                "text": [],
                "answer_start": []
            }
        }
        data["qa_data"].append(new_entry)
        with open("class_data.json", "w") as f:
            json.dump(data, f, indent=2)
        st.success("New lesson context added successfully!")
    else:
        st.warning("Please enter lesson context.")

# Section to view existing lessons
st.header("View Existing Lesson Data")
for idx, entry in enumerate(data["qa_data"]):
    with st.expander(f"Lesson {idx+1}"):
        edited_context = st.text_area("Edit Lesson Context", value=entry["context"], key=f"c_{idx}")

        if st.button(f"Save Changes for Lesson {idx+1}"):
            entry["context"] = edited_context.strip()
            with open("class_data.json", "w") as f:
                json.dump(data, f, indent=2)
            st.success(f"Updated Lesson {idx+1}!")
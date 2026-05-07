import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Page title
st.title("🤖 FAQ Chatbot")

# FAQ Questions and Answers
faq_data = {
    "What is Aloe Vera used for?": "Aloe Vera is used for skin care and healing.",
    
    "How often should I water Tulsi plant?":
    "Tulsi plant should be watered daily.",

    "Does Neem plant need sunlight?":
    "Yes, Neem plant grows best in sunlight.",

    "What are the benefits of Mint plant?":
    "Mint helps in digestion and provides freshness.",

    "Can I grow plants indoors?":
    "Yes, many medicinal plants can be grown indoors."
}

# Convert questions into list
questions = list(faq_data.keys())

# User input
user_question = st.text_input("Ask a question")

# Ask button
if st.button("Get Answer"):

    # Add user question to question list
    all_questions = questions + [user_question]

    # Convert text to vectors
    vectorizer = CountVectorizer().fit_transform(all_questions)

    # Calculate similarity
    similarity = cosine_similarity(vectorizer[-1], vectorizer[:-1])

    # Find best matching question
    index = np.argmax(similarity)

    # Get answer
    answer = faq_data[questions[index]]

    # Display answer
    st.success(answer)
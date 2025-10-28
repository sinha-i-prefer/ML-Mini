import streamlit as st
import joblib

# --- Load Model & Vectorizer ---
@st.cache_resource
def load_model():
    model = joblib.load("spam_classifier_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_model()

# --- App UI ---
st.title("📧 SMS Spam Classifier")
st.write("Enter a message below to check if it's spam or not:")

user_input = st.text_area("Message:", height=150)

if st.button("Predict"):
    if user_input.strip() == "":
        st.warning("Please enter a message!")
    else:
        # Transform and predict
        text_vector = vectorizer.transform([user_input])
        prediction = model.predict(text_vector)[0]
        proba = model.predict_proba(text_vector)[0][prediction]

        label = "🚫 Spam" if prediction == 1 else "✅ Not Spam"
        st.subheader(label)
        st.progress(int(proba * 100))
        st.caption(f"Confidence: {proba*100:.2f}%")

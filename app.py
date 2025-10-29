import streamlit as st
import joblib
import numpy as np
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Modern UI ---
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    /* Glass Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin: 20px auto;
        max-width: 900px;
    }
    
    /* Title Animation */
    .animated-title {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 30px;
        font-weight: 300;
    }
    
    /* Text Area Styling */
    .stTextArea textarea {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 15px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 50px;
        font-size: 1.2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
        margin-top: 20px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Result Cards */
    .result-card {
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin: 30px 0;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .spam-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
    }
    
    .safe-card {
        background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%);
        color: white;
        box-shadow: 0 10px 30px rgba(81, 207, 102, 0.3);
    }
    
    .result-emoji {
        font-size: 5rem;
        margin-bottom: 15px;
        animation: bounce 0.6s ease;
    }
    
    @keyframes bounce {
        0%, 100% {transform: translateY(0);}
        50% {transform: translateY(-20px);}
    }
    
    .result-text {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 15px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .confidence-text {
        font-size: 1.3rem;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Stats Cards */
    .stat-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 5px;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Example Cards */
    .example-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .example-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% {transform: translateY(0px);}
        50% {transform: translateY(-10px);}
    }
    
    .float {
        animation: float 3s ease-in-out infinite;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Model & Vectorizer ---
@st.cache_resource
def load_model():
    try:
        model = joblib.load("spam_classifier_model.pkl")
        vectorizer = joblib.load("tfidf_vectorizer.pkl")
        return model, vectorizer, True
    except:
        return None, None, False

model, vectorizer, model_loaded = load_model()

# --- Hero Section ---
st.markdown('<h1 class="animated-title float">🛡️ SMS Spam Detector</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Protect yourself from spam messages with AI-powered detection</p>', unsafe_allow_html=True)

if not model_loaded:
    st.error("⚠️ Model files not found! Please train the model first.")
    st.stop()

# --- Main Card ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

# Text Input Section
st.markdown("### 📝 Enter Your Message")
user_input = st.text_area(
    "",
    height=150,
    placeholder="Type or paste your SMS message here...",
    label_visibility="collapsed"
)

# Show message stats if input exists
if user_input:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{len(user_input)}</div><div class="stat-label">Characters</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{len(user_input.split())}</div><div class="stat-label">Words</div></div>', unsafe_allow_html=True)
    with col3:
        uppercase_pct = (sum(c.isupper() for c in user_input) / len(user_input) * 100) if user_input else 0
        st.markdown(f'<div class="stat-card"><div class="stat-value">{uppercase_pct:.0f}%</div><div class="stat-label">Uppercase</div></div>', unsafe_allow_html=True)
    with col4:
        digits = sum(c.isdigit() for c in user_input)
        st.markdown(f'<div class="stat-card"><div class="stat-value">{digits}</div><div class="stat-label">Numbers</div></div>', unsafe_allow_html=True)

# Predict Button
if st.button("🔍 Analyze Message"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a message to analyze!")
    else:
        # Loading animation
        with st.spinner("🔄 Analyzing your message..."):
            time.sleep(0.8)  # Dramatic effect
            
            # Transform and predict
            text_vector = vectorizer.transform([user_input])
            prediction = model.predict(text_vector)[0]
            
            # Get probability based on model type
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(text_vector)[0]
                confidence = proba[prediction] * 100
            elif hasattr(model, 'decision_function'):
                decision = model.decision_function(text_vector)[0]
                confidence = (1 / (1 + np.exp(-abs(decision)))) * 100
            else:
                confidence = 100.0
            
            # Display Results
            if prediction == 1:
                st.markdown(f'''
                <div class="result-card spam-card">
                    <div class="result-emoji">🚫</div>
                    <div class="result-text">SPAM DETECTED!</div>
                    <div class="confidence-text">Confidence: {confidence:.1f}%</div>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown('''
                <div class="info-box">
                    <strong>⚠️ Warning Signs:</strong><br>
                    This message shows characteristics of spam. Be cautious of:
                    <ul>
                        <li>Suspicious links or phone numbers</li>
                        <li>Requests for personal information</li>
                        <li>Too-good-to-be-true offers</li>
                        <li>Urgent action requests</li>
                    </ul>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="result-card safe-card">
                    <div class="result-emoji">✅</div>
                    <div class="result-text">SAFE MESSAGE</div>
                    <div class="confidence-text">Confidence: {confidence:.1f}%</div>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown('''
                <div class="info-box">
                    <strong>✨ All Clear!</strong><br>
                    This message appears to be legitimate. However, always stay vigilant and verify unexpected requests.
                </div>
                ''', unsafe_allow_html=True)
            
            # Progress bar
            st.progress(int(confidence) / 100)

st.markdown('</div>', unsafe_allow_html=True)

# --- Example Messages Section ---
st.markdown("---")
st.markdown("### 💡 Try These Examples")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🚫 Spam Examples")
    spam_examples = [
        "🎁 WINNER! You've won $5000! Click here NOW to claim your prize!!!",
        "🔥 URGENT: Your bank account will be closed. Verify now: bit.ly/fake123",
        "💰 Congratulations! You've been selected for a FREE iPhone. Text WIN to 55555"
    ]
    
    for idx, example in enumerate(spam_examples):
        if st.button(example, key=f"spam_{idx}", use_container_width=True):
            st.session_state.example_text = example.split(":", 1)[-1] if ":" in example else example[2:]

with col2:
    st.markdown("#### ✅ Legitimate Examples")
    ham_examples = [
        "☕ Hey! Are we still on for coffee at 3pm tomorrow?",
        "📧 Meeting reminder: Team sync at 2pm. See you there!",
        "🏠 Can you grab some milk on your way home? Thanks!"
    ]
    
    for idx, example in enumerate(ham_examples):
        if st.button(example, key=f"ham_{idx}", use_container_width=True):
            st.session_state.example_text = example.split(":", 1)[-1] if ":" in example else example[2:]

# Auto-fill example if clicked
if 'example_text' in st.session_state:
    st.info(f"📋 Example loaded! Click 'Analyze Message' to test it.")
    st.session_state.pop('example_text')

# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <p style='color: white; font-size: 1.1rem; font-weight: 300;'>
            🤖 Powered by Machine Learning | Built with ❤️ using Streamlit
        </p>
        <p style='color: rgba(255,255,255,0.7); font-size: 0.9rem;'>
            Model: {} | Always stay vigilant against phishing attempts
        </p>
    </div>
""".format(type(model).__name__), unsafe_allow_html=True)
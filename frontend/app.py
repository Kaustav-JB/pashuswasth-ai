import streamlit as st
import requests
from datetime import datetime
import time

st.set_page_config(
    page_title="PashuSwasth AI - Neural Acoustic Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Futuristic CSS - Split into smaller chunks to avoid JS conflicts
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #0f1419 100%);
        color: #ffffff;
    }
    
    /* Animations */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.3); }
        50% { box-shadow: 0 0 30px rgba(0, 255, 255, 0.5); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
</style>
""", unsafe_allow_html=True)

# Header styles
st.markdown("""
<style>
    .hero-header {
        text-align: center;
        padding: 2rem 0;
        animation: slideIn 0.8s ease-out;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00ffff 0%, #00ff9d 50%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #8b9dc3;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .hero-tagline {
        font-size: 1rem;
        color: #00ffff;
        margin-top: 0.5rem;
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)
# Card styles
st.markdown("""
<style>
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: slideIn 0.6s ease-out;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 255, 255, 0.3);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(0, 255, 255, 0.2);
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        animation: glow 3s ease-in-out infinite;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(0, 255, 255, 0.5);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00ffff, #00ff9d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #8b9dc3;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Status and result styles
st.markdown("""
<style>
    .status-badge {
        display: inline-block;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 1rem 0;
        animation: slideIn 0.5s ease-out;
    }
    
    .status-healthy {
        background: rgba(0, 255, 157, 0.2);
        border: 2px solid rgba(0, 255, 157, 0.5);
        color: #00ff9d;
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.3);
    }
    
    .status-unhealthy {
        background: rgba(255, 71, 87, 0.2);
        border: 2px solid rgba(255, 71, 87, 0.5);
        color: #ff4757;
        box-shadow: 0 0 20px rgba(255, 71, 87, 0.3);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #00ffff;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .glow-text {
        color: #00ffff;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)
# Button and UI element styles
st.markdown("""
<style>
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(138, 43, 226, 0.2));
        color: #00ffff;
        border: 2px solid rgba(0, 255, 255, 0.5);
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(138, 43, 226, 0.3));
        border-color: #00ffff;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 255, 255, 0.4);
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00ffff, #a78bfa, #00ff9d);
        border-radius: 10px;
    }
    
    .stAlert {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-left: 4px solid #00ffff;
        border-radius: 8px;
        color: #e0e7ff;
    }
    
    .warning-badge {
        background: rgba(255, 193, 7, 0.1);
        border: 1px solid rgba(255, 193, 7, 0.3);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #ffc107;
        backdrop-filter: blur(10px);
    }
    
    .feature-item {
        background: rgba(255, 255, 255, 0.04);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #00ffff;
        transition: all 0.3s ease;
    }
    
    .feature-item:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateX(5px);
    }
    
    .center { text-align: center; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🧬 PASHUSWASTH AI</div>
    <div class="hero-subtitle">Neural Acoustic Intelligence Platform</div>
    <div class="hero-tagline">Advanced Bio-Acoustic Disease Detection System</div>
</div>
""", unsafe_allow_html=True)

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Model Accuracy</div>
        <div class="metric-value">~94%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Response Time</div>
        <div class="metric-value">&lt;2s</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Audio Format</div>
        <div class="metric-value">WAV</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">AI Engine</div>
        <div class="metric-value">CNN</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
# Main content
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">🎤 ACOUSTIC ANALYSIS HUB</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="warning-badge">⚠️ Currently optimized for chicken vocalization analysis</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload Audio Sample (.wav)",
        type=["wav"],
        help="Upload clear chicken vocalization recording for AI analysis"
    )
    
    if uploaded_file is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔊 AUDIO PREVIEW</div>', unsafe_allow_html=True)
        st.audio(uploaded_file)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            analyze_btn = st.button("🧠 INITIATE ANALYSIS", use_container_width=True, type="primary")
        with col_btn2:
            if st.button("🔄 RESET", use_container_width=True):
                st.rerun()
        
        if analyze_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.spinner("🔬 Neural network processing acoustic patterns..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                try:
                    response = requests.post(
                        "http://localhost:5000/predict",
                        files={"file": uploaded_file},
                        timeout=30  # Add timeout
                    )
                    
                    # Check if request was successful
                    response.raise_for_status()
                    
                    result = response.json()
                    prediction = result["prediction"]
                    score = result["risk_score"]
                    
                    st.markdown('<div class="glass-card" style="margin-top: 2rem;">', unsafe_allow_html=True)
                    st.markdown('<div class="center">', unsafe_allow_html=True)
                    
                    st.markdown('<div class="section-title">📋 ANALYSIS RESULTS</div>', unsafe_allow_html=True)
                    
                    if prediction == "Healthy":
                        st.markdown(
                            f'<div class="status-badge status-healthy">✅ HEALTHY LIVESTOCK | RISK: {score:.1%}</div>',
                            unsafe_allow_html=True
                        )
                        recommendation = "No immediate action required. Continue regular monitoring protocols."
                        icon = "✅"
                    else:
                        st.markdown(
                            f'<div class="status-badge status-unhealthy">⚠️ POTENTIAL HEALTH ISSUE | RISK: {score:.1%}</div>',
                            unsafe_allow_html=True
                        )
                        recommendation = "Veterinary consultation recommended. Implement enhanced monitoring protocols."
                        icon = "⚠️"
                    
                    st.progress(min(score, 1.0))
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("<hr style='border: 1px solid rgba(0, 255, 255, 0.2); margin: 2rem 0;'>", unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="glow-text" style="font-size: 1.1rem; font-weight: 600;">{icon} RECOMMENDATION</div>', unsafe_allow_html=True)
                    st.info(recommendation)
                    
                    if "ai_report" in result:
                        st.markdown('<div class="glow-text" style="font-size: 1.1rem; font-weight: 600;">🧠 AI HEALTH GUIDANCE</div>', unsafe_allow_html=True)
                        st.info(result["ai_report"])
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except requests.exceptions.ConnectionError:
                    st.error("❌ **Connection Failed**: Cannot connect to the AI backend service. Please ensure the backend server is running.")
                    st.info("💡 **Troubleshooting**: Check if the backend service is started and accessible.")
                    
                except requests.exceptions.Timeout:
                    st.error("⏱️ **Request Timeout**: The analysis is taking longer than expected. Please try again.")
                    st.info("💡 **Tip**: Large audio files may take more time to process.")
                    
                except requests.exceptions.HTTPError as e:
                    if response.status_code == 400:
                        st.error("📁 **Invalid File**: The uploaded file format is not supported or corrupted.")
                        st.info("💡 **Solution**: Please upload a valid WAV audio file.")
                    elif response.status_code == 500:
                        st.error("🔧 **Server Error**: Internal error in the AI backend service.")
                        st.info("💡 **Action**: Please try again or contact support if the issue persists.")
                    else:
                        st.error(f"🌐 **HTTP Error {response.status_code}**: {str(e)}")
                        
                except ValueError as e:
                    st.error("📊 **Data Processing Error**: Invalid response format from the backend service.")
                    st.info("💡 **Details**: The server response could not be parsed as JSON.")
                    
                except KeyError as e:
                    st.error(f"🔑 **Missing Data**: Expected field '{str(e)}' not found in the analysis results.")
                    st.info("💡 **Cause**: The backend service may have returned incomplete data.")
                    
                except Exception as e:
                    st.error("⚠️ **Unexpected Error**: An unknown error occurred during analysis.")
                    st.error(f"**Error Details**: {str(e)}")
                    st.info("💡 **Action**: Please try again or contact support with the error details above.")
    
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("👆 Upload a WAV audio file to initiate bio-acoustic analysis")
    
    st.markdown('</div>', unsafe_allow_html=True)
with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📖 SYSTEM PROTOCOL</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-item">
        <strong>1️⃣ AUDIO CAPTURE</strong><br>
        Record livestock vocalizations
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-item">
        <strong>2️⃣ NEURAL PROCESSING</strong><br>
        Deep learning acoustic analysis
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-item">
        <strong>3️⃣ HEALTH ASSESSMENT</strong><br>
        Real-time disease detection
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-item">
        <strong>4️⃣ ACTION PROTOCOL</strong><br>
        Follow AI recommendations
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 CAPABILITIES</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="line-height: 2;">
    • Real-time analysis ✨<br>
    • High accuracy detection 🎯<br>
    • Detailed health metrics 📊<br>
    • Secure processing 🔒<br>
    • Easy to use interface 📱
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div class="center" style="opacity: 0.6; font-size: 0.9rem; color: #8b9dc3;">
    <p>⚡ Powered by Neural Networks | Built with 💝 By Drift-Ops</p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem;">Version 2.0.0 | Last Updated: {}</p>
</div>
""".format(datetime.now().strftime('%B %d, %Y')), unsafe_allow_html=True)
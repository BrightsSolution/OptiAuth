import streamlit as st
import time
from datetime import datetime

# Page configuration with custom title and icon
st.set_page_config(
    page_title="OptiAuth - AI-Powered Attendance System", 
    layout="wide", 
    page_icon="🎯",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
with open("./static/styles.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Hero Section with animated title
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">🎯 OptiAuth</h1>
        <p class="hero-subtitle">AI-Powered Attendance Management System</p>
        <div class="hero-description">
            Revolutionizing education with cutting-edge facial recognition technology
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🚀 Features", "📖 Documentation", "📸 Gallery"])

with tab1:
    st.markdown("""
    <div class="welcome-section">
        <h2>🌟 Welcome to OptiAuth</h2>
        <p class="intro-text">
            OptiAuth is a next-generation AI-driven attendance management system that transforms how educational institutions 
            handle student registration and attendance tracking. Built with state-of-the-art facial recognition technology, 
            it delivers unparalleled accuracy, security, and efficiency.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key highlights in cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>AI-Powered Recognition</h3>
            <p>Advanced facial recognition using eye region embeddings for maximum accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3>Real-Time Processing</h3>
            <p>Instant attendance marking with FAISS indexing for lightning-fast searches</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3>Secure & Private</h3>
            <p>Enterprise-grade security with encrypted biometric data storage</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="features-section">
        <h2>✨ Core Capabilities</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature grid
    features = [
        {
            "icon": "👥",
            "title": "Student Registration",
            "description": "Seamlessly enroll students with facial biometrics, roll numbers, and course details. Duplicate prevention ensures data integrity."
        },
        {
            "icon": "📊",
            "title": "Attendance Marking",
            "description": "Upload single or group photos for automated recognition. AI processes images in real-time with 99%+ accuracy."
        },
        {
            "icon": "📈",
            "title": "Analytics Dashboard",
            "description": "Comprehensive insights with attendance rates, trends, and detailed reports for data-driven decisions."
        },
        {
            "icon": "🎓",
            "title": "Multi-Course Support",
            "description": "Manage multiple courses simultaneously with isolated FAISS indices and organized data structures."
        },
        {
            "icon": "🔍",
            "title": "Advanced Search",
            "description": "FAISS-powered similarity search with configurable thresholds for optimal recognition performance."
        },
        {
            "icon": "📱",
            "title": "Modern Interface",
            "description": "Intuitive Streamlit-based UI with dark theme, animations, and responsive design for all devices."
        }
    ]
    
    for i in range(0, len(features), 2):
        col1, col2 = st.columns(2)
        with col1:
            feature = features[i]
            st.markdown(f"""
            <div class="capability-card">
                <div class="capability-icon">{feature['icon']}</div>
                <h4>{feature['title']}</h4>
                <p>{feature['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if i + 1 < len(features):
            with col2:
                feature = features[i + 1]
                st.markdown(f"""
                <div class="capability-card">
                    <div class="capability-icon">{feature['icon']}</div>
                    <h4>{feature['title']}</h4>
                    <p>{feature['description']}</p>
                </div>
                """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="documentation-section">
        <h2>📚 Quick Start Guide</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Installation steps
    st.markdown("### 🛠️ Installation & Setup")
    
    with st.expander("Step 1: Clone Repository", expanded=True):
        st.code("""
git clone https://github.com/BrightsSolution/OptiAuth
cd OptiAuth
        """, language="bash")
    
    with st.expander("Step 2: Environment Setup", expanded=True):
        st.code("""
# Create virtual environment
python3.12 -m venv venv

# Activate environment
# Windows:
venv\\Scripts\\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
        """, language="bash")
    
    with st.expander("Step 3: System Dependencies (Linux/Ubuntu)", expanded=True):
        st.code("""
sudo apt update
sudo apt install -y libpng-dev libjpeg-dev libz-dev
pip install opencv-python-headless
        """, language="bash")
    
    with st.expander("Step 4: Run Application", expanded=True):
        st.code("""
streamlit run app.py
# Access at: http://localhost:8501
        """, language="bash")
    
    # Technology stack
    st.markdown("### 🛠️ Technology Stack")
    
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown("""
        **Core Technologies:**
        - 🐍 Python 3.12+
        - 🤖 DeepFace (ArcFace)
        - 👁️ MediaPipe
        - 🔍 FAISS (Vector Search)
        - 🗄️ SQLite Database
        """)
    
    with tech_col2:
        st.markdown("""
        **Web Framework:**
        - 🌐 Streamlit
        - 🎨 Custom CSS/HTML
        - 📱 Responsive Design
        - ⚡ Real-time Updates
        """)

with tab4:
    st.markdown("""
    <div class="gallery-section">
        <h2>📸 System Screenshots</h2>
        <p>Experience OptiAuth through these visual demonstrations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Image gallery with descriptions
    gallery_items = [
        {
            "image": "./assets/attendence_dashboard.png",
            "title": "Attendance Dashboard",
            "description": "Comprehensive analytics and attendance tracking interface"
        },
        {
            "image": "./assets/mark_attendence.png", 
            "title": "Attendance Marking",
            "description": "AI-powered facial recognition for attendance logging"
        },
        {
            "image": "./assets/register.png",
            "title": "Student Registration",
            "description": "Secure student enrollment with biometric capture"
        }
    ]
    
    for item in gallery_items:
        st.markdown(f"### {item['title']}")
        st.markdown(f"*{item['description']}*")
        st.image(item['image'], use_container_width=True)
        st.markdown("---")

# Footer with enhanced information
st.markdown("""
<div class="footer-enhanced">
    <div class="footer-content">
        <div class="footer-section">
            <h4>🎯 OptiAuth</h4>
            <p>AI-Powered Attendance Management</p>
        </div>
        <div class="footer-section">
            <h4>🔗 Links</h4>
            <p><a href="https://github.com/BrightsSolution/OptiAuth" target="_blank">GitHub Repository</a></p>
            <p><a href="https://github.com/BrightsSolution" target="_blank">BrightSolution</a></p>
        </div>
        <div class="footer-section">
            <h4>📧 Contact</h4>
            <p>info@brightsolution.com</p>
            <p>© 2024 BrightSolution. All rights reserved.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
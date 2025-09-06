import streamlit as st

# Page configuration with custom title and icon
st.set_page_config(page_title="OptiAuth - AI Attendance System", layout="wide", page_icon="📸")

# Inject custom CSS
with open("./static/styles.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main title with styled HTML
st.markdown("<div class='title'>📸 OptiAuth - AI Attendance System</div>", unsafe_allow_html=True)

# Introduction section
st.markdown("""
### 🌟 Introduction to OptiAuth

OptiAuth is an advanced AI-driven attendance management system developed by BrightSolution. This platform leverages cutting-edge facial recognition technology, focusing on eye region embeddings, to provide a secure, accurate, and efficient solution for student registration and attendance tracking. Designed for educational institutions, it supports multiple courses and offers real-time processing with a professional user interface.

### 🎯 What It Does

- **Student Registration**: Enroll students by capturing facial biometrics, roll numbers, names, and course details.
- **Attendance Marking**: Automatically detect and log attendance using single or group photos with AI-powered recognition.
- **Attendance Dashboard**: Visualize attendance records and summaries for insightful analysis.
- **Scalable Design**: Supports course-specific management with FAISS indexing for fast similarity searches.

### 🚧 Deployment Issue

Unfortunately, due to a dependency conflict with OpenCV (`libGL.so.1` not available in the Streamlit Cloud environment), we are unable to deploy this application directly on Streamlit at this time. The system requires a headless environment setup, which is challenging to configure on the free tier of Streamlit Cloud.

### 🛠️ How to Run Locally

You can explore and use OptiAuth by cloning the project from our GitHub repository:

1. **Clone the Repository**:
   ```
   git clone https://github.com/BrightsSolution/OptiAuth
   cd optiauth
   ```

2. **Set Up Environment**:
   - Create a virtual environment: `python3.12 -m venv venv`
   - Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
   - Install dependencies: `pip install -r requirements.txt`

3. **Install System Dependencies** (Ubuntu/Debian):
   ```
   sudo apt update
   sudo apt install -y libpng-dev libjpeg-dev libz-dev
   pip install opencv-python-headless
   ```

4. **Run the Application**:
   ```
   streamlit run main.py
   ```
   Access it at `http://localhost:8501`.

### 📸 Screenshots

Below are some visuals of the OptiAuth system in action:
""", unsafe_allow_html=True)

st.image('./assets/attendence_dashboard.png', use_container_width=True)
st.image('./assets/mark_attendence.png', use_container_width=True)
st.image('./assets/attendence_dashboard.png', use_container_width=True)

# Footer
st.markdown("""
<div class='footer'>
    Developed by <a href='https://github.com/BrightsSolution' target='_blank'>BrightSolution</a> | 
    <a href='https://github.com/BrightsSolution/OptiAuth' target='_blank'>View on GitHub</a>
</div>
""", unsafe_allow_html=True)
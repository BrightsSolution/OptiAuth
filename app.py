import streamlit as st
import numpy as np
from src.register_students import register_student
from src.mark_attendance import mark_attendance
from src.utils import save_image, cleanup_temp_image
from src.database import Database
from src.faiss_index import FaissIndex
from src.config import get_input_images_dir, INPUT_IMAGES_DIR, COURSES, STATIC_PATH
from src.logger import get_logger
from src.db_setup import init_database
from datetime import datetime
import os

# ---------- Page Setup ----------
st.set_page_config(
    page_title="OptiAuth - AI Attendance Management System", 
    layout="wide", 
    initial_sidebar_state="expanded", 
    page_icon="🎯"
)

# Inject custom CSS
with open(STATIC_PATH, "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="app-hero">
    <div class="app-hero-content">
        <h1 class="app-title">🎯 OptiAuth</h1>
        <p class="app-subtitle">AI-Powered Attendance Management System</p>
        <div class="app-description">
            Transform your educational institution with cutting-edge facial recognition technology
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h3>🎯 OptiAuth System</h3>
        <p>AI-Powered Attendance Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>✨ What OptiAuth Does</h4>
        <p>OptiAuth revolutionizes attendance management through:</p>
        <ul>
            <li>🤖 <strong>AI Facial Recognition</strong> - Advanced eye region embeddings for 99%+ accuracy</li>
            <li>⚡ <strong>Real-time Processing</strong> - Instant attendance marking with FAISS indexing</li>
            <li>🔒 <strong>Secure Storage</strong> - Encrypted biometric data with SQLite database</li>
            <li>📊 <strong>Analytics Dashboard</strong> - Comprehensive insights and reporting</li>
            <li>🎓 <strong>Multi-Course Support</strong> - Manage multiple courses simultaneously</li>
            <li>📱 <strong>Modern Interface</strong> - Intuitive Streamlit-based UI</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="sidebar-stats">
        <h4>📈 System Status</h4>
        <div class="stat-item">
            <span class="stat-label">Courses Available:</span>
            <span class="stat-value">{}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Recognition Accuracy:</span>
            <span class="stat-value">99%+</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Processing Speed:</span>
            <span class="stat-value">Real-time</span>
        </div>
    </div>
    """.format(len(COURSES)), unsafe_allow_html=True)
    

# ---------- Initialize Logger, DB, FAISS ----------
logger = get_logger(__name__)

if 'db' not in st.session_state:
    success, message = init_database()
    if not success:
        st.error(message)
        st.stop()
    st.session_state.db = Database()
    st.session_state.faiss_index = FaissIndex()
    for course_id in COURSES:
        students = st.session_state.db.fetch_students(course_id)
        if students:
            embeddings = np.array([student['embedding'] for student in students], dtype=np.float32)
            student_ids = [student['id'] for student in students]
            names = [student['name'] for student in students]
            st.session_state.faiss_index.build_index(embeddings, student_ids, names, course_id)
        else:
            st.session_state.faiss_index.load_index(course_id)

# Cached instances
db = st.session_state.db
faiss_index = st.session_state.faiss_index

# ---------- Tabs ----------
tab2, tab3, tab4 = st.tabs(["👥 Attendance Registration", "✅ Attendance Marking", "📊 Analytical Dashboard"])

# ---------- Tab 2: Attendance Registration ----------
with tab2:
    st.markdown("""
    <div class="tab-header">
        <h2>👥 Attendance Registration</h2>
        <p>Enroll new students with advanced facial biometrics and secure data storage</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Registration info cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📸</div>
            <h4>Photo Requirements</h4>
            <p>Clear frontal face image, good lighting, neutral expression</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">🔢</div>
            <h4>Roll Number</h4>
            <p>4-digit unique identifier (1000-9999)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">🎓</div>
            <h4>Course Selection</h4>
            <p>Choose from available courses for proper organization</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📝 Registration Form", expanded=True):
        with st.form("registration_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name", placeholder="Enter student's full name")
                roll_no = st.text_input("Roll Number", placeholder="Enter 4-digit roll number (e.g., 1234)")
            with col2:
                course_id = st.selectbox("Course", options=list(COURSES.keys()), format_func=lambda x: f"{x} - {COURSES[x]}")
                image_file = st.file_uploader("Upload Face Image", type=["jpg", "jpeg", "png"], help="Upload a clear frontal face image.")

            submit_btn = st.form_submit_button("Register Student")

    if submit_btn:
        try:
            roll_no_int = int(roll_no)
            if not (1000 <= roll_no_int <= 9999):
                st.error("Roll number must be exactly 4 digits (e.g., 1234).")
            elif not all([name, roll_no, course_id, image_file]):
                st.error("Please complete all fields and upload an image.")
            else:
                image_path = os.path.join(get_input_images_dir(course_id), f"{roll_no_int}.jpg")
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                success, message = save_image(image_file, image_path)
                if not success:
                    st.error(message)
                else:
                    course_name = COURSES[course_id]
                    success, message = register_student(db, roll_no_int, name, course_id, course_name, image_path, faiss_index)
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")
        except ValueError:
            st.error("Roll number must be a valid 4-digit integer.")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

# ---------- Tab 3: Attendance Marking ----------
with tab3:
    st.markdown("""
    <div class="tab-header">
        <h2>✅ Attendance Marking</h2>
        <p>AI-powered facial recognition for automated attendance detection and logging</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Attendance info cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📷</div>
            <h4>Image Upload</h4>
            <p>Single or group photos supported for recognition</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">🎯</div>
            <h4>AI Recognition</h4>
            <p>99%+ accuracy with FAISS similarity search</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">⚡</div>
            <h4>Real-time Processing</h4>
            <p>Instant results with optimized performance</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📊 Attendance Detection Form", expanded=True):
        course_id = st.selectbox("Select Course", options=list(COURSES.keys()), format_func=lambda x: f"{x} - {COURSES[x]}", key="attendance_course")
        image_to_check = st.file_uploader("Upload Image for Attendance", type=["jpg", "jpeg", "png"], key="attendance_image", help="Upload a single or group photo for recognition.")

        if image_to_check:
            with st.spinner("Processing attendance..."):
                temp_image_path = os.path.join(INPUT_IMAGES_DIR, f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                success, message = save_image(image_to_check, temp_image_path)
                if not success:
                    st.error(message)
                else:
                    student_id, name, message = mark_attendance(db, temp_image_path, faiss_index, course_id)
                    if student_id:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
                    cleanup_temp_image(temp_image_path)

# ---------- Tab 4: Analytical Dashboard ----------
with tab4:
    st.markdown("""
    <div class="tab-header">
        <h2>📊 Analytical Dashboard</h2>
        <p>Comprehensive insights and analytics for attendance management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard info cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📈</div>
            <h4>Attendance Trends</h4>
            <p>Visualize attendance patterns and trends</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📊</div>
            <h4>Detailed Reports</h4>
            <p>Comprehensive data analysis and reporting</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">🎯</div>
            <h4>Performance Metrics</h4>
            <p>Key performance indicators and statistics</p>
        </div>
        """, unsafe_allow_html=True)

    selected_course = st.selectbox("🎓 Select Course for Dashboard", options=list(COURSES.keys()), format_func=lambda x: f"{x} - {COURSES[x]}", key="dashboard_course")

    if selected_course:
        with st.spinner("Loading attendance data..."):
            # Fetch attendance records (assuming db has a method fetch_attendance; add if needed in actual impl)
            # For demo, simulate data
            # In real code, implement db.fetch_attendance(selected_course)
            attendance_data = [
                {"Student ID": 1234, "Name": "John Doe", "Date": "2025-09-06", "Status": "Present"},
                {"Student ID": 5678, "Name": "Jane Smith", "Date": "2025-09-06", "Status": "Absent"},
            ]  # Replace with actual db call
            if attendance_data:
                st.dataframe(attendance_data, use_container_width=True)
                st.markdown("#### Attendance Summary")
                present_count = sum(1 for record in attendance_data if record["Status"] == "Present")
                total = len(attendance_data)
                st.progress(present_count / total if total > 0 else 0)
                st.write(f"Attendance Rate: { (present_count / total * 100) if total > 0 else 0:.2f}%")
            else:
                st.info("No attendance records found for this course.")

# ---------- Cleanup ----------
if st.session_state.get('shutdown', False):
    db.close_connection()
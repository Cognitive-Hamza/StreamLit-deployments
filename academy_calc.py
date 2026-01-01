import streamlit as st

# Page config
st.set_page_config(
    page_title="Academic Result Calculator",
    page_icon="🎓",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
    }
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
    }
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    section[data-testid="stSidebar"] {
        background: #1a1a2e !important;
    }
    .main-header {
        text-align: center;
        color: white;
        padding: 2rem 0;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .subtitle {
        text-align: center;
        color: #64b5f6;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .card {
        background: transparent;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: none;
        border: none;
        margin: 1rem 0;
    }
    .step-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .step-number {
        background: #2196F3;
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .step-title {
        font-size: 2rem;
        font-weight: bold;
        color: white;
    }
    .grade-card {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        border: 4px solid #64b5f6;
    }
    .grade-display {
        font-size: 6rem;
        font-weight: bold;
        color: white;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    }
    .stat-card {
        background: rgba(33, 150, 243, 0.15);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #2196F3;
    }
    .stat-card p {
        color: white !important;
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: white !important;
    }
    .subject-item {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 2px solid #2196F3;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
    }
    .subject-item * {
        color: white !important;
    }
    .subject-item:hover {
        background: rgba(33, 150, 243, 0.2);
        border-color: #64b5f6;
    }
    .progress-bar {
        background: #e0e0e0;
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
    }
    .progress-fill {
        background: linear-gradient(90deg, #2196F3 0%, #1976D2 100%);
        height: 100%;
        transition: width 0.3s ease;
    }
    .stButton>button {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 12px;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(33,150,243,0.4);
    }
    .welcome-box {
        background: rgba(33, 150, 243, 0.2);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #2196F3;
        margin: 1rem 0;
        color: white;
    }
    .stTextInput > div > div > input {
        background: white !important;
        color: #1a1a2e !important;
        border: 2px solid #2196F3 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #999 !important;
        opacity: 1 !important;
    }
    .stNumberInput > div > div > input {
        background: white !important;
        color: #1a1a2e !important;
        border: 2px solid #2196F3 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
    }
    .stNumberInput > div > div > input::placeholder {
        color: #999 !important;
        opacity: 1 !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: white !important;
    }
    .stMarkdown {
        color: white !important;
    }
    .stMarkdown p {
        color: white !important;
    }
    .stMarkdown span {
        color: white !important;
    }
    .stMarkdown strong {
        color: white !important;
    }
    .footer {
        text-align: center;
        color: #64b5f6;
        margin-top: 2rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'name' not in st.session_state:
    st.session_state.name = ''
if 'num_subjects' not in st.session_state:
    st.session_state.num_subjects = 0
if 'subjects' not in st.session_state:
    st.session_state.subjects = []
if 'result' not in st.session_state:
    st.session_state.result = None

# Header
st.markdown('<div class="main-header">🎓 Academic Result Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Professional grade calculation system</div>', unsafe_allow_html=True)

# Main card container
st.markdown('<div class="card">', unsafe_allow_html=True)

# Step 1: Name Input
if st.session_state.step == 1:
    st.markdown('<h2 style="color: white; margin-bottom: 1.5rem;">Student Name</h2>', unsafe_allow_html=True)
    
    st.markdown('<label style="font-size: 1.2rem; font-weight: 600; color: white; display: block; margin-bottom: 0.5rem;">Enter your full name</label>', unsafe_allow_html=True)
    name = st.text_input("Enter your full name", key="name_input", placeholder="e.g., Ahmed Ali Khan", label_visibility="collapsed")
    
    if st.button("Next Step →", key="name_btn"):
        if name and name.replace(" ", "").isalpha():
            st.session_state.name = name
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("❌ Name can only contain letters")

# Step 2: Number of Subjects
elif st.session_state.step == 2:
    st.markdown('<h2 style="color: white; margin-bottom: 1.5rem;">Number of Subjects</h2>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="welcome-box"><strong>Welcome, {st.session_state.name}! 🎓</strong></div>', unsafe_allow_html=True)
    
    st.markdown('<label style="font-size: 1.2rem; font-weight: 600; color: white; display: block; margin-bottom: 0.5rem;">How many subjects? (Max 10)</label>', unsafe_allow_html=True)
    num_subjects = st.number_input("How many subjects? (Max 10)", min_value=1, max_value=10, step=1, key="num_input", label_visibility="collapsed")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_1"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next Step →", key="num_btn"):
            if num_subjects >= 1:
                st.session_state.num_subjects = num_subjects
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("❌ Please enter number of subjects")

# Step 3: Subject Entry
elif st.session_state.step == 3:
    st.markdown('<h2 style="color: white; margin-bottom: 1.5rem;">Enter Subject Details</h2>', unsafe_allow_html=True)
    
    # Progress
    progress = len(st.session_state.subjects) / st.session_state.num_subjects
    st.markdown(f'<div class="welcome-box"><strong>Progress: {len(st.session_state.subjects)} / {st.session_state.num_subjects}</strong></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {progress*100}%"></div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display added subjects
    if st.session_state.subjects:
        st.markdown("### ✅ Added Subjects")
        for idx, sub in enumerate(st.session_state.subjects):
            st.markdown(f'<div class="subject-item"><span><strong>{idx+1}. {sub["name"]}</strong></span><span><strong>{sub["marks"]}/150</strong></span></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Current subject input
    if len(st.session_state.subjects) < st.session_state.num_subjects:
        st.markdown(f"### Subject {len(st.session_state.subjects) + 1}")
        
        st.markdown('<label style="font-size: 1.1rem; font-weight: 600; color: white; display: block; margin-bottom: 0.5rem;">Subject Name</label>', unsafe_allow_html=True)
        subject_name = st.text_input("Subject Name", key=f"sub_name_{len(st.session_state.subjects)}", placeholder="e.g., Mathematics", label_visibility="collapsed")
        
        st.markdown('<label style="font-size: 1.1rem; font-weight: 600; color: white; display: block; margin-bottom: 0.5rem;">Marks (0-150)</label>', unsafe_allow_html=True)
        subject_marks = st.number_input("Marks (0-150)", min_value=0, max_value=150, step=1, key=f"sub_marks_{len(st.session_state.subjects)}", label_visibility="collapsed")
        
        btn_text = "🎯 Calculate Result" if len(st.session_state.subjects) + 1 == st.session_state.num_subjects else "✓ Add Subject"
        
        if st.button(btn_text, key="add_btn"):
            if subject_name and subject_name.replace(" ", "").isalpha():
                st.session_state.subjects.append({"name": subject_name, "marks": subject_marks})
                
                if len(st.session_state.subjects) == st.session_state.num_subjects:
                    # Calculate result
                    total = sum(sub["marks"] for sub in st.session_state.subjects)
                    max_total = st.session_state.num_subjects * 150
                    percentage = round((total / max_total) * 100)
                    
                    if percentage >= 95:
                        grade = "A*"
                    elif percentage >= 81:
                        grade = "A"
                    elif percentage >= 71:
                        grade = "B"
                    elif percentage >= 61:
                        grade = "C"
                    elif percentage >= 51:
                        grade = "D"
                    else:
                        grade = "F"
                    
                    st.session_state.result = {
                        "total": total,
                        "max_total": max_total,
                        "percentage": percentage,
                        "grade": grade
                    }
                    st.session_state.step = 4
                
                st.rerun()
            else:
                st.error("❌ Subject name can only contain letters")

# Step 4: Results
elif st.session_state.step == 4:
    st.markdown('<div style="text-align: center; margin-bottom: 2rem;"><h2 style="color: white;">🏆 Result Card</h2><p style="color: #64b5f6;">Your academic performance summary</p></div>', unsafe_allow_html=True)
    
    # Student name
    st.markdown(f'<div class="welcome-box" style="text-align: center;"><h3 style="color: white;">{st.session_state.name}</h3></div>', unsafe_allow_html=True)
    
    # Grade display
    st.markdown(f'<div class="grade-card"><p style="color: white; font-size: 1.5rem; margin-bottom: 1rem;">Your Grade</p><div class="grade-display">{st.session_state.result["grade"]}</div></div>', unsafe_allow_html=True)
    
    # Stats
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'''
        <div class="stat-card">
            <p style="color: white; font-weight: bold; margin-bottom: 0.5rem;">📈 Percentage</p>
            <div class="stat-value">{st.session_state.result["percentage"]}%</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="stat-card">
            <p style="color: white; font-weight: bold; margin-bottom: 0.5rem;">⭐ Total Marks</p>
            <div class="stat-value">{st.session_state.result["total"]}/{st.session_state.result["max_total"]}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Subject breakdown
    st.markdown("### 📊 Subject Breakdown")
    for idx, sub in enumerate(st.session_state.subjects):
        sub_percentage = round((sub["marks"] / 150) * 100)
        st.markdown(f'''
        <div class="subject-item">
            <span style="color: white;"><strong>{idx+1}. {sub["name"]}</strong></span>
            <span style="color: white;"><strong>{sub["marks"]}/150</strong> <span style="color: #64b5f6;">({sub_percentage}%)</span></span>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔄 Calculate Another Result", key="reset_btn"):
        st.session_state.step = 1
        st.session_state.name = ''
        st.session_state.num_subjects = 0
        st.session_state.subjects = []
        st.session_state.result = None
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Professional Academic Calculator</div>', unsafe_allow_html=True)
import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="Quiz Master 🎯",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: 600;
    }
    .quiz-container {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .stat-box {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    h1 {
        color: #667eea;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = []
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'player_name' not in st.session_state:
    st.session_state.player_name = ""

# Quiz questions
QUESTIONS = [
    {"question": "What is 2 - 2?", "answer": "0", "type": "number"},
    {"question": "What is 5 + 13?", "answer": "18", "type": "number"},
    {"question": "What is 10 × 6?", "answer": "60", "type": "number"},
    {"question": "What is 3 ÷ 3?", "answer": "1", "type": "number"},
    {"question": "What is the capital city of Pakistan?", "answer": "islamabad", "type": "text"}
]

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🎯 Quiz Master")
    st.markdown("### Test Your Knowledge!")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/brain.png", width=100)
    st.markdown("## 📊 Dashboard")
    
    # Stats
    total_attempts = len(st.session_state.results)
    if total_attempts > 0:
        avg_score = sum([r['score'] for r in st.session_state.results]) / total_attempts
        best_score = max([r['score'] for r in st.session_state.results])
    else:
        avg_score = 0
        best_score = 0
    
    st.metric("Total Attempts", total_attempts)
    st.metric("Average Score", f"{avg_score:.1f}/5")
    st.metric("Best Score", f"{best_score}/5")
    
    st.markdown("---")
    st.markdown("### 🎮 Navigation")
    menu_option = st.radio(
        "Choose an option:",
        ["🏠 Home", "📝 Start Quiz", "📈 View Results", "🔍 Search Results", "💾 Download Results"],
        label_visibility="collapsed"
    )

# Main content area
if menu_option == "🏠 Home":
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## Welcome to Quiz Master! 👋")
        st.markdown("""
        Test your knowledge with our exciting quiz! Here's what you can do:
        
        - ✅ Take interactive quizzes
        - 📊 Track your performance
        - 🔍 Search your past attempts
        - 💾 Download your results
        
        **Ready to get started?** Choose an option from the sidebar!
        """)
    
    with col2:
        st.image("https://img.icons8.com/color/200/000000/quiz.png")
    
    if st.session_state.results:
        st.markdown("### 🏆 Recent Attempts")
        recent_df = pd.DataFrame(st.session_state.results[-5:])
        recent_df = recent_df[['name', 'score', 'timestamp']]
        st.dataframe(recent_df, use_container_width=True, hide_index=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif menu_option == "📝 Start Quiz":
    if not st.session_state.quiz_active:
        st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
        st.markdown("## 📝 Start New Quiz")
        
        with st.form("start_quiz_form"):
            player_name = st.text_input("Enter your name:", placeholder="Your name here...")
            submit = st.form_submit_button("🚀 Start Quiz", use_container_width=True)
            
            if submit:
                if player_name.strip():
                    st.session_state.player_name = player_name.strip()
                    st.session_state.quiz_active = True
                    st.session_state.current_question = 0
                    st.session_state.score = 0
                    st.session_state.answers = []
                    st.rerun()
                else:
                    st.error("⚠️ Please enter your name!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Quiz in progress
        if st.session_state.current_question < len(QUESTIONS):
            q_num = st.session_state.current_question
            question = QUESTIONS[q_num]
            
            # Progress bar
            progress = (q_num) / len(QUESTIONS)
            st.progress(progress)
            st.markdown(f"**Question {q_num + 1} of {len(QUESTIONS)}**")
            
            st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
            st.markdown(f"### {question['question']}")
            
            with st.form(f"question_form_{q_num}"):
                if question['type'] == 'number':
                    user_answer = st.text_input("Your answer:", placeholder="Enter number...")
                else:
                    user_answer = st.text_input("Your answer:", placeholder="Enter your answer...")
                
                submitted = st.form_submit_button("✅ Submit Answer", use_container_width=True)
                
                if submitted:
                    if user_answer.strip():
                        correct_answer = question['answer']
                        is_correct = user_answer.strip().lower() == correct_answer.lower()
                        
                        if is_correct:
                            st.session_state.score += 1
                            st.success("✅ Correct!")
                        else:
                            st.error(f"❌ Wrong! Correct answer: {correct_answer.title()}")
                        
                        st.session_state.answers.append({
                            'question': question['question'],
                            'user_answer': user_answer.strip(),
                            'correct_answer': correct_answer,
                            'is_correct': is_correct
                        })
                        
                        st.session_state.current_question += 1
                        st.rerun()
                    else:
                        st.warning("⚠️ Please enter an answer!")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            # Quiz completed
            score = st.session_state.score
            total = len(QUESTIONS)
            percentage = (score / total) * 100
            
            # Save result
            result = {
                'name': st.session_state.player_name,
                'score': score,
                'total': total,
                'percentage': percentage,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'answers': st.session_state.answers
            }
            
            if result not in st.session_state.results:
                st.session_state.results.append(result)
            
            # Display results
            st.markdown('<div class="score-card">', unsafe_allow_html=True)
            st.markdown(f"# 🎉 Quiz Completed!")
            st.markdown(f"## {st.session_state.player_name}")
            st.markdown(f"### Score: {score}/{total} ({percentage:.0f}%)")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Feedback
            st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
            if score == 5:
                st.success("🌟 Excellent! Perfect score!")
                st.balloons()
            elif score == 4:
                st.success("👏 Great Job! Almost perfect.")
            elif score == 3:
                st.info("👍 Good Effort! Keep practicing.")
            elif score == 2:
                st.warning("💪 You have potential! Practice more.")
            else:
                st.warning("📚 Don't worry. Try again!")
            
            # Show detailed answers
            st.markdown("### 📋 Detailed Review")
            for i, ans in enumerate(st.session_state.answers, 1):
                with st.expander(f"Question {i}: {ans['question']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Your Answer:** {ans['user_answer']}")
                    with col2:
                        st.write(f"**Correct Answer:** {ans['correct_answer']}")
                    
                    if ans['is_correct']:
                        st.success("✅ Correct")
                    else:
                        st.error("❌ Incorrect")
            
            if st.button("🔄 Take Quiz Again", use_container_width=True):
                st.session_state.quiz_active = False
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.answers = []
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

elif menu_option == "📈 View Results":
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.markdown("## 📈 All Results")
    
    if st.session_state.results:
        # Convert to DataFrame
        df = pd.DataFrame(st.session_state.results)
        df = df[['name', 'score', 'total', 'percentage', 'timestamp']]
        df['percentage'] = df['percentage'].round(1)
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "name": "Name",
                "score": st.column_config.NumberColumn("Score", format="%d"),
                "total": st.column_config.NumberColumn("Total", format="%d"),
                "percentage": st.column_config.ProgressColumn("Performance", format="%.1f%%", min_value=0, max_value=100),
                "timestamp": "Date & Time"
            }
        )
        
        # Visualization
        st.markdown("### 📊 Performance Chart")
        chart_data = pd.DataFrame({
            'Attempt': range(1, len(st.session_state.results) + 1),
            'Score': [r['score'] for r in st.session_state.results]
        })
        st.line_chart(chart_data.set_index('Attempt'))
    else:
        st.info("📭 No results yet. Take a quiz to see your results!")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif menu_option == "🔍 Search Results":
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.markdown("## 🔍 Search Results by Name")
    
    if st.session_state.results:
        search_name = st.text_input("Enter name to search:", placeholder="Search by name...")
        
        if search_name:
            filtered = [r for r in st.session_state.results if search_name.lower() in r['name'].lower()]
            
            if filtered:
                st.success(f"Found {len(filtered)} result(s) for '{search_name}'")
                df = pd.DataFrame(filtered)
                df = df[['name', 'score', 'total', 'percentage', 'timestamp']]
                df['percentage'] = df['percentage'].round(1)
                
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "name": "Name",
                        "score": "Score",
                        "total": "Total",
                        "percentage": st.column_config.ProgressColumn("Performance", format="%.1f%%"),
                        "timestamp": "Date & Time"
                    }
                )
            else:
                st.warning(f"No results found for '{search_name}'")
    else:
        st.info("📭 No results available to search.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif menu_option == "💾 Download Results":
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.markdown("## 💾 Download Results")
    
    if st.session_state.results:
        # Prepare download data
        df = pd.DataFrame(st.session_state.results)
        df = df[['name', 'score', 'total', 'percentage', 'timestamp']]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV Download
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"quiz_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # JSON Download
            json_data = json.dumps(st.session_state.results, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"quiz_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.success("✅ Your results are ready to download!")
    else:
        st.info("📭 No results available to download.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Quiz Master v1.0</p>
</div>
""", unsafe_allow_html=True)
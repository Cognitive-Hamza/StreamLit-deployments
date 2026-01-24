import streamlit as st
import whisper
import tempfile
import os
from pathlib import Path
import time
import zipfile
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Whisper Transcription",
    page_icon="🎤",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    h1, h2, h3, p, label, .stMarkdown {
        color: #000000 !important;
    }
    .transcription-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #667eea;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🎤 Whisper Audio Transcription")
st.markdown("Upload audio files or entire folders and get instant transcription using Whisper Tiny model")
st.markdown("---")

# Initialize session state
if 'transcriptions' not in st.session_state:
    st.session_state.transcriptions = {}
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
    st.session_state.model = None
if 'processing_times' not in st.session_state:
    st.session_state.processing_times = {}

# Load model function
@st.cache_resource
def load_whisper_model():
    """Load Whisper Tiny model"""
    return whisper.load_model("tiny")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Language selection
    language = st.selectbox(
        "Select Language",
        options=["auto", "en", "ur", "hi", "ar", "es", "fr", "de", "zh", "ja", "ko"],
        format_func=lambda x: {
            "auto": "Auto Detect",
            "en": "English",
            "ur": "Urdu",
            "hi": "Hindi",
            "ar": "Arabic",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean"
        }.get(x, x)
    )
    
    # Task selection
    task = st.radio(
        "Task",
        options=["transcribe", "translate"],
        help="Transcribe: Convert audio to text in original language\nTranslate: Convert audio to English text"
    )
    
    st.markdown("---")
    st.info("💡 **Tip:** For best results, use clear audio with minimal background noise")

# Main content area
st.subheader("📁 Upload Audio Files")

# Upload mode selection
upload_mode = st.radio(
    "Upload Mode:",
    options=["Single/Multiple Files", "Folder (Multiple Files)"],
    horizontal=True
)

audio_files = []

if upload_mode == "Single/Multiple Files":
    # Multiple file uploader
    uploaded_files = st.file_uploader(
        "Choose audio files",
        type=["mp3", "wav", "m4a", "ogg", "flac", "mp4", "avi", "mov"],
        accept_multiple_files=True,
        help="You can select multiple files at once"
    )
    if uploaded_files:
        audio_files = uploaded_files
else:
    # Folder upload (via multiple file selection)
    st.info("📂 Select all audio files from your folder (you can select multiple files at once)")
    uploaded_files = st.file_uploader(
        "Choose all audio files from folder",
        type=["mp3", "wav", "m4a", "ogg", "flac", "mp4", "avi", "mov"],
        accept_multiple_files=True,
        help="Select all files from your folder"
    )
    if uploaded_files:
        audio_files = uploaded_files

# Display uploaded files
if audio_files:
    st.success(f"✅ {len(audio_files)} file(s) uploaded")
    
    with st.expander("📋 View uploaded files"):
        for i, file in enumerate(audio_files, 1):
            st.write(f"{i}. {file.name} ({file.size / 1024 / 1024:.2f} MB)")
    
    # Transcribe button
    col1, col2 = st.columns([3, 1])
    with col1:
        transcribe_btn = st.button("🎯 Transcribe All Files", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.transcriptions = {}
            st.session_state.processing_times = {}
            st.rerun()
    
    if transcribe_btn:
        try:
            # Load model
            with st.spinner("🔄 Loading Whisper model..."):
                if not st.session_state.model_loaded:
                    st.session_state.model = load_whisper_model()
                    st.session_state.model_loaded = True
            
            # Progress tracking
            progress_text = st.empty()
            progress_bar = st.progress(0)
            
            # Process each file
            for idx, audio_file in enumerate(audio_files):
                start_time = time.time()
                
                progress_text.text(f"🎤 Processing {idx + 1}/{len(audio_files)}: {audio_file.name}")
                
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(audio_file.name).suffix) as tmp_file:
                    tmp_file.write(audio_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Transcription options
                options = {
                    "task": task,
                    "fp16": False
                }
                
                if language != "auto":
                    options["language"] = language
                
                # Transcribe
                result = st.session_state.model.transcribe(tmp_file_path, **options)
                
                # Store results
                elapsed_time = time.time() - start_time
                st.session_state.transcriptions[audio_file.name] = result["text"]
                st.session_state.processing_times[audio_file.name] = elapsed_time
                
                # Cleanup
                os.unlink(tmp_file_path)
                
                # Update progress
                progress_bar.progress((idx + 1) / len(audio_files))
            
            progress_text.empty()
            progress_bar.empty()
            
            total_time = sum(st.session_state.processing_times.values())
            st.success(f"✅ All {len(audio_files)} files transcribed in {total_time:.2f} seconds!")
            
        except Exception as e:
            st.error(f"❌ Error during transcription: {str(e)}")
            st.info("Make sure you have installed: `pip install openai-whisper`")

# Display transcriptions
if st.session_state.transcriptions:
    st.markdown("---")
    st.header("📝 Transcription Results")
    
    # Download all as ZIP
    if len(st.session_state.transcriptions) > 1:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for filename, transcription in st.session_state.transcriptions.items():
                txt_filename = Path(filename).stem + "_transcription.txt"
                zip_file.writestr(txt_filename, transcription)
        
        zip_buffer.seek(0)
        st.download_button(
            label="📦 Download All Transcriptions (ZIP)",
            data=zip_buffer,
            file_name="all_transcriptions.zip",
            mime="application/zip",
            use_container_width=True
        )
        st.markdown("---")
    
    # Display each transcription
    for filename, transcription in st.session_state.transcriptions.items():
        with st.container():
            st.markdown(f"### 🎵 {filename}")
            
            # Show processing time
            if filename in st.session_state.processing_times:
                st.caption(f"⏱️ Processed in {st.session_state.processing_times[filename]:.2f} seconds")
            
            # Transcription text area
            trans_text = st.text_area(
                "Transcription:",
                value=transcription,
                height=150,
                key=f"trans_{filename}",
                label_visibility="collapsed"
            )
            
            # Action buttons for each file
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Copy button - shows text in code block for easy copying
                if st.button(f"📋 Show for Copy", key=f"copy_{filename}", use_container_width=True):
                    st.code(trans_text, language=None)
            
            with col2:
                # Download individual file
                txt_filename = Path(filename).stem + "_transcription.txt"
                st.download_button(
                    label="💾 Download TXT",
                    data=trans_text,
                    file_name=txt_filename,
                    mime="text/plain",
                    key=f"download_{filename}",
                    use_container_width=True
                )
            
            with col3:
                # Delete this transcription
                if st.button(f"🗑️ Remove", key=f"delete_{filename}", use_container_width=True):
                    del st.session_state.transcriptions[filename]
                    if filename in st.session_state.processing_times:
                        del st.session_state.processing_times[filename]
                    st.rerun()
            
            st.markdown("---")

# Footer
st.markdown("""
    <div style='text-align: center; color: #000000; padding: 20px;'>
        <p><strong>Installation Instructions:</strong></p>
        <code>pip install streamlit openai-whisper</code><br>
        <code>streamlit run app.py</code>
    </div>
    """, unsafe_allow_html=True)
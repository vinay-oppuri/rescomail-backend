import streamlit as st
import requests
import json

# Set Page Config
st.set_page_config(
    page_title="Resume Parser & ATS Analyzer",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 Resume Parser & ATS Analyzer")
st.markdown("---")

# Sidebar
st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Upload your resume (PDF or TXT).
2. Click **Analyze Resume**.
3. View structured data and ATS Score.
""")

st.sidebar.markdown("---")
# Backend URL Configuration
backend_url = st.sidebar.text_input(
    "Backend API URL", 
    value="https://rescomail-backend.vercel.app",
    help="Enter your deployed FastAPI backend URL if not running locally."
)

# Main Content
st.subheader("Upload Resume")
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])

if uploaded_file is not None:
    st.info(f"File uploaded: **{uploaded_file.name}**")
    
    if st.button("🚀 Analyze Resume"):
        with st.spinner("Analyzing resume... This may take a few seconds."):
            try:
                # Prepare file for upload
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                
                # Make API Request to FastAPI Backend
                response = requests.post(f"{backend_url}/upload-resume", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Analysis complete!")
                    st.markdown("---")
                    
                    # Create Tabs
                    tab1, tab2 = st.tabs(["📊 ATS Analysis", "🔍 Parsed Data"])
                    
                    # ATS Analysis Tab
                    with tab1:
                        ats_data = data.get("ats_analysis", {})
                        if "error" in ats_data:
                            st.error(ats_data["error"])
                            if "raw_output" in ats_data:
                                with st.expander("🔍 View Raw LLM Output"):
                                    st.code(ats_data["raw_output"])
                        else:
                            score = ats_data.get("ats_score", 0)
                            
                            # Metric
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                st.metric(label="ATS Score", value=f"{score}/100")
                            with col2:
                                # Progress bar
                                st.progress(score / 100)
                                
                            st.markdown("### 🔑 Missing Keywords")
                            keywords = ats_data.get("missing_keywords", [])
                            if keywords:
                                for kw in keywords:
                                    st.markdown(f"- `{kw}`")
                            else:
                                st.write("No missing keywords identified.")
                                
                            st.markdown("### 💡 Suggestions for Improvement")
                            suggestions = ats_data.get("suggestions", [])
                            if suggestions:
                                for sug in suggestions:
                                    st.markdown(f"- {sug}")
                            else:
                                st.write("No suggestions provided.")
                                
                    # Parsed Data Tab
                    with tab2:
                        parsed_data = data.get("parsed_resume", {})
                        if "error" in parsed_data:
                            st.error(parsed_data["error"])
                            if "raw_output" in parsed_data:
                                with st.expander("🔍 View Raw LLM Output"):
                                    st.code(parsed_data["raw_output"])
                        else:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.subheader("Personal Info")
                                st.write(f"**Name:** {parsed_data.get('name', 'N/A')}")
                                st.write(f"**Email:** {parsed_data.get('email', 'N/A')}")
                                st.write(f"**Phone:** {parsed_data.get('phone', 'N/A')}")
                                
                            with col2:
                                st.subheader("Skills")
                                skills = parsed_data.get("skills", [])
                                if skills:
                                    st.write(", ".join(skills))
                                else:
                                    st.write("None")
                                    
                            st.markdown("---")
                            
                            col3, col4 = st.columns(2)
                            with col3:
                                st.subheader("Education")
                                edu = parsed_data.get("education", [])
                                if isinstance(edu, list):
                                    for item in edu:
                                        if isinstance(item, dict):
                                            st.markdown(f"**{item.get('degree', 'Degree')}** at {item.get('school', 'School')} ({item.get('year', '')})")
                                        else:
                                            st.markdown(f"- {item}")
                                else:
                                    st.write(edu)
                                    
                            with col4:
                                st.subheader("Experience")
                                exp = parsed_data.get("experience", [])
                                if isinstance(exp, list):
                                        for item in exp:
                                            if isinstance(item, dict):
                                                st.markdown(f"**{item.get('role', 'Role')}** at {item.get('company', 'Company')} ({item.get('duration', '')})")
                                            else:
                                                st.markdown(f"- {item}")
                                else:
                                    st.write(exp)
                                    
                else:
                    st.error(f"Error from Backend: {response.status_code} - {response.text}")
                    
            except Exception as e:
                st.error(f"Failed to connect to backend: {str(e)}")
else:
    st.info("Please upload a file to begin.")

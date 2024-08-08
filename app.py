import streamlit as st
from model.agents import CyberCopilot
from data.datafetching import fetch_data
from data.dataloading import load_data

# Initialize the model (assuming you've already set up your CyberCopilot class)
copilot = CyberCopilot()

# Streamlit UI Configuration
st.set_page_config(page_title="Cybersecurity Search Engine + AI Copilot", layout="wide")

# Sidebar for Configuration
st.sidebar.title("🔧 Settings")
query_chunking = st.sidebar.checkbox("Enable Query Chunking", value=True)
show_sources = st.sidebar.checkbox("Show Data Sources", value=True)
show_summary = st.sidebar.checkbox("Generate Summary", value=True)

# Main UI
st.title("🛡️ Cybersecurity Search Engine + AI Copilot")
st.write("Search across multiple sources and get accurate, context-aware cybersecurity insights.")

# Search Input
user_query = st.text_area("Enter your query", placeholder="e.g., Recent ransomware attacks in healthcare.")

# Search and Display Results
if st.button("Search"):
    if user_query:
        # Fetch and curate data
        prompt = f"{user_query}" if not query_chunking else f"[CHUNKED] {user_query}"
        fetched_data = fetch_data(prompt)
        curated_results = load_data(fetched_data, show_sources=show_sources)
        
        # Get and display response from the copilot
        response = copilot.get_response(curated_results)
        st.subheader("Results")
        st.write(response)
        
        # Show Data Sources if enabled
        if show_sources:
            st.write("Data Sources:")
            st.write(fetched_data.get('sources', "No sources available."))
        
        # Show Summary if enabled
        if show_summary:
            summary = copilot.generate_summary(response)
            st.subheader("Summary")
            st.write(summary)
    else:
        st.warning("Please enter a query to search.")

# Footer with Custom Message
st.markdown(
    """
    <style>
    footer {visibility: hidden;}
    footer:after {
        content:'Cyber Search Engine + Copilot | Designed for Cybersecurity Professionals';
        visibility: visible;
        display: block;
        position: relative;
        padding: 5px;
        top: 2px;
    }
    </style>
    """, unsafe_allow_html=True
)

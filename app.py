import streamlit as st
from model.agents import process_query
from data.dataloading import load_data

# Streamlit UI Configuration
st.set_page_config(page_title="Cybersecurity Search Engine + AI Copilot", layout="wide")

# Sidebar for Configuration
st.sidebar.title("🔧 Settings")
query_chunking = st.sidebar.checkbox("Enable Query Chunking", value=True)
show_summary = st.sidebar.checkbox("Generate Summary", value=True)

# Main UI
st.title("🛡️ Cybersecurity Search Engine + AI Copilot")
st.write("Search across multiple sources and get accurate, context-aware cybersecurity insights.")

# Search Input
user_query = st.text_area("Enter your query", placeholder="e.g., Recent ransomware attacks in healthcare.")

# Search and Display Results
if st.button("Search"):
    if user_query:
        # Show spinner and stage feedback
        with st.spinner("Processing query..."):
            st.write("Stage: Preparing Query")
            prompt = f"{user_query}" if not query_chunking else f"[CHUNKED] {user_query}"

            st.write("Stage: Fetching and Loading Data")
            fetched_data_chunks = load_data(chunk_size=1000)  # Adjust chunk_size as needed

            st.write("Stage: Processing Query")
            response = ""
            for chunk in fetched_data_chunks:
                response += process_query(chunk)

        # Display results
        st.subheader("Results")
        st.write(response)

        # Show Summary if enabled
        if show_summary:
            st.write("Stage: Generating Summary")
            with st.spinner("Generating summary..."):
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

import streamlit as st
import streamlit.components.v1 as components

st.markdown("## 📊 Embedded Power BI Dashboard")

components.html(
    """
    <iframe title="Digital Capability Dashboard"
            width="1140"
            height="541.25"
            src="https://app.powerbi.com/reportEmbed?reportId=46472439-f848-4534-95c2-f3165c436442&autoAuth=true&ctid=4f5b8d9f-2c66-4220-96c7-4999daa340b9"
            frameborder="0"
            allowFullScreen="true">
    </iframe>
    """,
    height=600,  # adjust height for Streamlit container
    scrolling=True
)

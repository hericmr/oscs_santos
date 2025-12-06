import streamlit as st

def apply_academic_style():
    """
    Applies custom CSS for academic formatting:
    - Serif fonts (Merriweather).
    - Justified text.
    - Clean layout.
    """
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap');
            
            html, body, [class*="css"], .stMarkdown, .stText, .stDataFrame {
                font-family: 'Merriweather', serif !important;
                color: #2c3e50;
            }
            
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Merriweather', serif !important;
                font-weight: 700;
                color: #1a1a1a;
            }
            
            /* Justify standard markdown text paragraphs */
            .stMarkdown p {
                text-align: justify;
                line-height: 1.7;
                font-size: 1.05rem;
            }
            
            /* Metric labels */
            div[data-testid="stMetricLabel"] {
                font-family: 'Merriweather', serif !important;
                font-weight: bold;
            }
            
            /* Sidebar styling */
            section[data-testid="stSidebar"] {
                background-color: #f8f9fa;
            }
            
            /* Info Box styling to look more academic */
            .stAlert {
                background-color: #f0f2f6;
                border-left: 5px solid #4e8cff;
            }
            
        </style>
    """, unsafe_allow_html=True)

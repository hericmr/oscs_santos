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
            /* Force GLOBAL Pure White Background & Black Text */
            .stApp {
                background-color: #FFFFFF !important;
                color: #000000 !important;
            }
            
            /* Metric labels - KEEP Times New Roman for "Academic" feel or switch? 
               Usually metrics are numbers/titles. Let's keep them Serif for contrast or Arial? 
               User asked for "normal text" to be Arial. Metrics are arguably "normal" in a dashboard, but Headers are not.
               I will make everything Arial EXCEPT h1-h6 to be safe, or maybe just h1-h6.
               Actually, for ABNT, it's usually ALL Arial or ALL Times.
               I will assume they want valid ABNT Arial style.
               But they might like the "Paper" look of Times Headers.
               I will split them: Body = Arial, Headers = Times.
            */
            
            /* Metric labels */
            div[data-testid="stMetricLabel"] {
                font-family: 'Arial', sans-serif !important;
                color: #000000 !important; 
                font-weight: bold;
            }

            /* GLOBAL BODY TEXT - ARIAL */
            html, body, [class*="css"], .stMarkdown, .stText, .stDataFrame, p, div, span, label {
                font-family: 'Arial', sans-serif !important;
                color: #000000 !important;
            }
            
            /* HEADERS - Keep Times New Roman for Academic/Paper contrast */
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Times New Roman', serif !important;
                color: #000000 !important;
                font-weight: 700;
            }
            
            /* Sidebar specific */
            section[data-testid="stSidebar"] {
                background-color: #FFFFFF !important; /* Force White */
                border-right: 1px solid #e0e0e0; /* Subtle separator */
                color: #000000 !important;
            }
            
            section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] div, section[data-testid="stSidebar"] label {
                 font-family: 'Arial', sans-serif !important;
                 color: #000000 !important;
            }

            /* INPUTS & WIDGETS - Deep Cleaning */
            /* Text Input, Number Input, Date Input, Selectbox labels */
            .stTextInput label, .stNumberInput label, .stDateInput label, .stSelectbox label, .stMultiSelect label {
                color: #000000 !important;
                font-weight: bold;
            }
            
            /* Input boxes background and text */
            input[type="text"], input[type="number"], .stSelectbox div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div {
                background-color: #FFFFFF !important;
                color: #000000 !important;
                border-color: #cccccc !important;
            }
             
            /* Dropdown options */
            ul[data-baseweb="menu"] li {
                background-color: #FFFFFF !important;
                color: #000000 !important;
            }

            /* Justify standard markdown text paragraphs */
            .stMarkdown p {
                text-align: justify;
                line-height: 1.7;
                font-size: 1.1rem;
            }
            
            /* Buttons */
            button[kind="secondary"] {
                background-color: #FFFFFF !important;
                color: #000000 !important;
                border: 1px solid #000000 !important;
            }
            button[kind="secondary"]:hover {
                background-color: #f0f0f0 !important;
            }
            
            /* Titles */
            h1, h2, h3, h4, h5, h6 {
                font-weight: 700;
            }
            
            /* Hide Streamlit Header, Menu, and Footer */
            /* Header restored for navigation access */
            /* header[data-testid="stHeader"] {
                visibility: visible;
            } */
            
            /* Remove the colored top decoration */
            div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0px;
            }

            /* Hide footer if needed */
            footer {
                visibility: hidden;
            }
            
        </style>
    """, unsafe_allow_html=True)

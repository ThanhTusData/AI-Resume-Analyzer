import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu
from functions.resume_analyzer import resume_analyzer
from functions.linkedin_scraper import linkedin_scraper
import warnings
warnings.filterwarnings('ignore')

def streamlit_config():
    st.set_page_config(
        page_title='Resume Analyzer AI',
        page_icon='🤖',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    st.markdown("""
    <style>
        /* Dark theme base */
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            color: #ffffff;
        }
                
        /* Transparent header */
        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }

        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(135deg, #111111 0%, #1f1f1f 100%);
            border-right: 1px solid #333333;
        }

        /* Main content area */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2ren;
            background: transparent;
        }

        /* Custom card styling */
        .custom-card {
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
            padding: 1,5rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
            margin: 1rem 0;
            border-left: 4px solid #00d9ff;
            transition: all 0.3s ease;
            color: #ffffff;
            border: 1px solid #333333;
        }

        .custom-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 35px rgba(0, 217, 255, 0.2);
            border-left-color: #ff6b6b;
        }

        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #333333 0%, #1a1a1a 100%);
            color: #00d9ff;
            border: 2px solid #00d9ff;
            border-radius: 25px;
            padding: 0.6rem 2.5rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 217, 255, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 217, 255, 0.5);
            background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%);
            color: #000000;
            border-color: #00d9ff;
        }

        /* File uploader styling */
        .stFileUploader > div > div {
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
            border: 2px dashed #00d9ff;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            color: #ffffff;
        }

        .stFileUploader > div > div:hover {
            border-color: #ff6b6b;
            background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%);
        }

        /* Form styling */
        .stForm {
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            margin: 1rem 0;
            border: 1px solid #333333;
        }

        /* Success/Error messages */
        .stSuccess {
            background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%);
            border-radius: 12px;
            color: #000000;
            padding: 1rem;
        }

        .stError {
            background: linear-gradient(135deg, #ff6b6b 0%, #ff4757 100%);
            border-radius: 12px;
            color: #ffffff;
            padding: 1rem;
        }

        /* Progress bar */
        .stProgress > dix > dix {
            background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%);
            border-radius: 10px;
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }

        .stTabs [data-baseweb='tab'] {
            background: #2a2a2a;
            border-radius: 12px;
            padding: 1rem 2rem;
            color: #cccccc;
            border: 1px solid #333333;
            font-weight: 500;
        }

        .stTabs [aria-selectedf='true] {
            background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%);
            color: #000000;
        }

        /* Expander styling */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #333333 0%, #1a1a1a 100%);
            color: #00d9ff;
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid #00d9ff;
        }

        /* Custom title styling */
        .main-title {
            background: linear-gradient(135deg, #009dff 0%, #ff6b6b 50%, #ffd700 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-colorr: transparent;
            background-clip: text;
            text-align: center;
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.5));
        }

        .subtitle {
            text-align: center;
            color: #cccccc;
            font-size: 1.3rem;
            margin-bottom: 3rem;
            font-weight: 400;
        }

        /* Animation for loading */
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.6; }
            100% { opacity: 1; }
        }

        .loading {
            animation: pulse 2s infinite;
        }

        /* Custom metrics */
        .metric-card {
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
            padding: 1.8rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            text-alignp: center;
            margin: 1rem 0;
            transition: all 0.3s ease;
            border: 1px solid #333333;
        }

        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 217, 255, 0.3);
            border-color: #00d9ff;
        }

        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }

        .metric-label {
            color: #cccccc;
            font-size: 1rem;
            font-weight: 500;
        }
                
        /* Sidebar improvements */
        .stSidebar > div {
            background: linear-gradient(180deg, #111111 0%, #1a1a1a 100%);
        }

        /* Input styling */
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 2px solid #333333;
            padding: 0.75rem 1rem;
            font-size: 1rem;
            background: #2a2a2a;
            color: #ffffff;
        }

        .stTextInput > div > div > input:focus {
            border-color: #00d9ff;
            box-shadow: 0 0 0 3px rgba(0, 217, 255, 0.2);
        }

        /* Select box styling */
        .stSelectbox > div > div {
            border-radius: 10px;
            border: 2px solid #333333;
            background: #2a2a2a;
        }

        /* Custom info box */
        .info-box {
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
            border: 1px solid #00d9ff;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: #ffffff;
        }

        .warning-box {
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
            border: 1px solid #ffd700;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: #ffffff;
        }

        /* Text color overides */
        .stMarkdown, .stText, p, h1, h2, h3, h4. h5, h6 {
            color: #ffffff !important;
        }

        /* Streamlit specific dark theme adjustments */
        .stApp > div {
            background: linear-gradient(135deg, #0a0a0a 0%. #1a1a1a 100%);
        }
    </style>      
    """, unsafe_allow_html=True)
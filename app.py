# app.py
import streamlit as st
from streamlit_option_menu import option_menu
from pathlib import Path

st.set_page_config(page_title="Human Capital", layout="wide")

# Path absolut ke file gambar
logo_path = Path(__file__).parent / "statistics.png"

# Header dengan logo
col1, col2 = st.columns([1, 10])
with col1:
    st.image(str(logo_path), width=70)
with col2:
    st.title("Human Capital Evaluation")

# NAVIGATION MENU
selected = option_menu(
    menu_title=None,
    options=["💡 Introduction", "🔎 Feature", "🛠️ HC Tools"],
    icons=[" ", " ", " "],  # string kosong untuk hilangkan icon
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f0f2f6"},
        "icon": {"color": "black", "font-size": "18px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "#EA6464", "color": "white"},
    }
)

# Panggil halaman yang sesuai
if selected == "💡 Introduction":
    import introduction
    introduction.show()

elif selected == "🔎 Feature":
    import insight
    insight.show()

elif selected == "🛠️ HC Tools":
    import tools
    tools.show()

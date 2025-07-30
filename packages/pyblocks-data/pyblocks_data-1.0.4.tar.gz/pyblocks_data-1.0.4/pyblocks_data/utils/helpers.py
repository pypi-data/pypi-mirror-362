# utils/helpers.py

import streamlit as st

def lego_card(title, emoji, color, body):
    st.markdown(
        f"""
        <div style='
            background-color:{color};
            padding:20px;
            border-radius:15px;
            margin-bottom:15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        '>
            <h3 style='margin-bottom:10px;'>{emoji} {title}</h3>
            <div>{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )



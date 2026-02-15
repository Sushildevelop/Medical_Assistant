import streamlit as st
from components.upload import render_uploader
from components.chatUI import render_chat
from components.history_download import render_history_download



st.set_page_config(page_title="AI Medical Assistant", page_icon=":robot_face:", layout="wide")

st.title("AI Medical Assistant")

render_uploader()
render_chat()
render_history_download()

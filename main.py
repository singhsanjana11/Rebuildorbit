import streamlit as st
import base64

st.set_page_config(page_title = "Orbit", layout="wide")

def add_sidebar_logo(logo_path: str, height_px: int = 90):
    with open(logo_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")

    st.markdown(
        f"""
        <style>
        /* Target the sidebar nav container */
        [data-testid="stSidebarNav"] {{
            background-image: url("data:image/png;base64,{b64}");
            background-repeat: no-repeat;
            background-position: 6px 1px;      /* position inside sidebar */
            background-size: auto {height_px}px; /* control logo size */
            padding-top: {height_px + 40}px;     /* push page links below logo */
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

add_sidebar_logo("assets/logonew.png")


home_page= st.Page(
    page="pages/home.py",
    title="Home",
    default=True
)

predict_single= st.Page(
    page="pages/predict.py",
    title="Single Prediction",
)

predict_batch= st.Page(
    page="pages/predict2.py",
    title="Batch Prediction",
)

analytics_page= st.Page(
    page="pages/analytics.py",
    title="Dashboards"
)

blog_page= st.Page(
    page="pages/blog.py",
    title="Blog"
)



pg= st.navigation(pages=[home_page, predict_single,predict_batch, analytics_page, blog_page])

st.sidebar.text("Made by Sanjana Singh")


pg.run()



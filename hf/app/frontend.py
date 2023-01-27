import streamlit as st
import streamlit_nested_layout
from PIL import Image

st.set_page_config(page_title="Text-to-Emoji",layout="wide")

def main() :
    left, right = st.columns([4, 1])

    if "submit" not in st.session_state:
        st.session_state["submit"] = False

    with left :
        st.subheader("Text-to-Emoji")

        with st.container():
            if st.session_state.submit :
                image = Image.open('../outputs/Cute rabbi3.png')
                st.image(image)
            else :
                st.write("test")

        with st.form(key="my_form", clear_on_submit=True):
            col1, col2 = st.columns([8, 1])

            with col1:
                st.text_input(
                    "",
                    placeholder="a cute buddy rabbit",
                    key="input",
                    label_visibility="collapsed",
                )
            with col2:
                submit = st.form_submit_button(label="submit")
    
    with right :
        option = st.selectbox(
                "Select Model",
                ("stable_diffusion_v1-5", "stable_diffusion_v2-1"),
                label_visibility = "visible",
            )
        st.write(option)

        num_inference = st.slider('',0,6,4)
        st.write(f'num_inference : {num_inference}')

        cfg_value = st.slider('',0, 100, 7)
        st.write(f'cfg_scale : {cfg_value}')

        inference_step = st.slider('', 0, 100, 30)
        st.write(f'inference_step : {inference_step}')
    
    
    if submit :
        st.session_state.submit = True
        st.experimental_rerun()
        

def right_container(right) :

    option = right.selectbox(
        "Select Model",
        ("stable_diffusion_v1-5", "stable_diffusion_v2-1"),
        label_visibility = "visible",
    )

    print(option)

    num_inference = right.slider

    cfg_value = right.slider('',0, 100, 7)
    right.write(f'cfg_scale : {cfg_value}')

    inference_step = right.slider('', 0, 100, 30)
    right.write(f'inference_step : {inference_step}')
    
if __name__ == "__main__" :
    main()
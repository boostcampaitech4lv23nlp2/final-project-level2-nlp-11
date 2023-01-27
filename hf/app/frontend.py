import streamlit as st
import streamlit_nested_layout
from PIL import Image

st.set_page_config(page_title="Text-to-Emoji",layout="wide")

def main() :
    left, right = st.columns([4, 1])

    if "submit" not in st.session_state:
        st.session_state["submit"] = False
    if "output_size" not in st.session_state :
        st.session_state["output_size"] = "128"
    if "num_inference" not in st.session_state :
        st.session_state["num_inference"] = "4"

    with left :
        st.subheader("Text-to-Emoji")

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

        if st.session_state.submit :
            print(st.session_state.output_size)

            #512 512 columns 4
            #256 256 columns 4
            #128 128 columns 8
            #64 64 columns 16
            image_reize_dict = {
                "64" : 16,
                "128" : 8,
                "256" : 4,
                "512" : 4,
            }

            image1 = Image.open('../outputs/Cute rabbi3.png')

            img_size = int(st.session_state.output_size)
            size_column = image_reize_dict[st.session_state.output_size]
            num_inference = st.session_state.num_inference

            image1 = image1.resize((img_size,img_size))
            
            image_list = [image1] * 20
            image_list = image_list[:num_inference]

            cols = st.columns(size_column)
            
            for idx , image in enumerate(image_list) :
                cols[idx%size_column].image(image, use_column_width="auto")
            
    with right :

        output_option = st.selectbox(
            "output_size",
            ("128","256","512")
        )
        st.session_state['output_size'] = output_option
        st.write(output_option)
        st.markdown("##")

        model_option = st.selectbox(
                "Select Model",
                ("stable_diffusion_v1-5", "stable_diffusion_v2-1"),
                label_visibility = "visible",
            )

        st.write(model_option)
        st.markdown("##")

        num_inference = st.slider("",0,12,4,label_visibility="hidden")
        st.session_state['num_inference'] = num_inference
        st.write(f'num_inference : {num_inference}')
        st.markdown("##")

        cfg_value = st.slider("",0, 100, 7, label_visibility="hidden")
        st.write(f'cfg_scale : {cfg_value}')
        st.markdown("##")

        inference_step = st.slider("",0, 100, 30, label_visibility="hidden")
        st.write(f'inference_step : {inference_step}')
    
    
    if submit :
        st.session_state.submit = True
        st.experimental_rerun()
    
    
if __name__ == "__main__" :
    main()
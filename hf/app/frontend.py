import streamlit as st
import io
import base64
import requests
import streamlit_nested_layout
from streamlit_image_select import image_select

from PIL import Image
from rembg import remove

st.set_page_config(page_title="Text-to-Emoji",layout="wide")

def main():
    left, right = st.columns([4, 1])

    if "submit" not in st.session_state:
        st.session_state["submit"] = False
    if "prompt" not in st.session_state:
        st.session_state["prompt"] = ""
    if "image_list" not in st.session_state:
        st.session_state["image_list"] = []
    if "output_size" not in st.session_state:
        st.session_state["output_size"] = 256
    if "num_inference" not in st.session_state:
        st.session_state["num_inference"] = None
    if "guidance_scale" not in st.session_state : 
        st.session_state['guidance_scale'] = None
    if "inference_step" not in st.session_state : 
        st.session_state['inference_step'] = None
    if "save_prameter" not in st.session_state : 
        st.session_state['save_prameter'] = {}
    if "model_select" not in st.session_state :
        st.session_state['model_select'] = ""
    if "remove_bg" not in st.session_state :
        st.session_state['remove_bg'] = False
    if "image_style" not in st.session_state :
        st.session_state['image_style'] = ""
    
    with left :
        st.markdown("## Text-to-Emoji")

        with st.form(key="my_form", clear_on_submit=True):
            col1, col2 = st.columns([8, 1])

            with col1:
                st.text_input(
                    " ",
                    value = st.session_state.prompt,
                    key="prompt",
                    label_visibility="collapsed",
                )
            with col2:
                submit = st.form_submit_button(label="submit")
                if submit:
                    st.session_state.submit = True
        
        if st.session_state.submit :

            data = {
                "prompt": st.session_state.prompt ,
                "guidance_scale":  st.session_state.guidance_scale,
                "num_images_per_prompt":  st.session_state.num_inference,
                "num_inference_steps":  st.session_state.inference_step,
                "size":  st.session_state.output_size
                }
            
            print(data)
            
            st.session_state.save_parameter = data
            # 리퀘스트를 보낼 URL
            response = requests.post("http://localhost:30001/eng_submit", json=data)

            response = requests.post( "http://118.67.133.216:30001/eng_submit",json= data)

            image_byte_list = response.json()["images"]
            remove_image_byte_list = response.json()["removes"]

            decode_image_list = [Image.open(io.BytesIO(base64.b64decode(image))) for image in image_byte_list ]
            remove_decode_image_list = [Image.open(io.BytesIO(base64.b64decode(image))) for image in remove_image_byte_list ]
           
            st.session_state['image_list'] = decode_image_list
            st.session_state['remove_bg_image_list'] = remove_decode_image_list
            
            st.session_state.submit = False
            st.session_state['remove_bg'] = False
                
        if st.session_state['image_list'] :
            
            st.markdown("#### Show Generation Image")
            img_index = image_select(
                label="",
                images= st.session_state['image_list'],
                use_container_width = 10,
                return_value = "index" 
            )
            
            st.write('###')
            st.markdown("#### Select Image!")

            with st.container() :
                image_col1 , image_col2 = st.columns([4,1])

                print(image_col1.id)
                
                with image_col1 :
                    st.markdown(
                        """
                        <style>
                            [data-testid=stImage]{
                                text-align: center;
                                display: block;
                                margin-left: auto;
                                margin-right: auto;
                                width: 100%;
                            }
                        </style>
                        """, unsafe_allow_html=True)
                    if st.session_state["remove_bg"] :
                        st.image(st.session_state['remove_bg_image_list'][img_index], use_column_width="auto")
                        img = st.session_state['remove_bg_image_list'][img_index]
                    else :
                        st.image(st.session_state['image_list'][img_index], use_column_width="auto")
                        img = st.session_state['image_list'][img_index]
    
                with image_col2 :
                    buf = io.BytesIO()
                    img.save(buf, format = "PNG")
                    buf_img = buf.getvalue()

                    btn = st.download_button(
                        label="Download image",
                        data= buf_img,
                        file_name = 'generation_image.png',
                        mime="image/png",
                        )
                    
                    st.markdown("##")
                    st.markdown("###### Remove Background")
                    remove_bg = st.radio(" ", (False, True), label_visibility="collapsed")
                    if remove_bg != st.session_state['remove_bg'] :
                        st.session_state['remove_bg'] = remove_bg
                        st.experimental_rerun()



    with right :

        st.markdown("##### model select")
        model_select = st.selectbox(
            "model select",
            ("English",
            "한국어",),
            label_visibility="collapsed"
        )

        st.markdown("##")
        st.markdown("##### image style")
        image_style = st.selectbox(
            "image_style",
            ("open-emoji","nato"),
            label_visibility="collapsed"
        )
        
        st.markdown("##")
        st.markdown("##### image size")
        output_option = st.selectbox(
            "image size",
            ("512","256","128"),
            label_visibility= "collapsed"
        )

        st.markdown("##")
        st.markdown("##### output count")
        num_inference = st.slider(" ",1,4,3,label_visibility="collapsed")

        st.markdown("##")
        st.markdown("##### cfg scale")
        guidance_scale = st.slider(" ",0, 50, 10,label_visibility="collapsed")


        st.session_state['model_select'] = model_select
        st.session_state['image_style'] = image_style
        st.session_state['output_size'] = int(output_option)
        st.session_state['num_inference'] = int(num_inference)
        st.session_state['guidance_scale'] = int(guidance_scale)
        st.session_state['inference_step'] = 30
    
if __name__ == "__main__" :
    main()

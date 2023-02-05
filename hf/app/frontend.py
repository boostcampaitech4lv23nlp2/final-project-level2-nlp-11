import streamlit as st
import io
import base64
import requests
import streamlit_nested_layout
from PIL import Image

st.set_page_config(page_title="Text-to-Emoji", layout="wide")


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
    if "guidance_scale" not in st.session_state:
        st.session_state["guidance_scale"] = None
    if "inference_step" not in st.session_state:
        st.session_state["inference_step"] = None
    if "save_prameter" not in st.session_state:
        st.session_state["save_prameter"] = {}

    # 512 512 columns 4
    # 256 256 columns 4
    # 128 128 columns 8
    # 64 64 columns 16
    image_reize_dict = {
        "64": 16,
        "128": 8,
        "256": 4,
        "512": 4,
    }

    size_column = image_reize_dict["".join(str(st.session_state.output_size))]

    with left:
        st.subheader("Text-to-Emoji")

        with st.form(key="my_form", clear_on_submit=True):
            col1, col2 = st.columns([8, 1])

            with col1:
                st.text_input(
                    "a cute buddy rabbit",
                    placeholder="a cute buddy rabbit",
                    key="prompt",
                    label_visibility="collapsed",
                )
            with col2:
                submit = st.form_submit_button(label="submit")
                if submit:
                    st.session_state.submit = True

        if st.session_state.submit:
            data = {
                "prompt": st.session_state.prompt,
                "guidance_scale": st.session_state.guidance_scale,
                "num_images_per_prompt": st.session_state.num_inference,
                "num_inference_step": st.session_state.inference_step,
                "size": st.session_state.output_size,
            }

            print(data)
            st.session_state.save_parameter = data
            # 리퀘스트를 보낼 URL
            response = requests.post("http://localhost:30001/eng_submit", json=data)

            image_byte_list = response.json()
            decode_image_list = [
                Image.open(io.BytesIO(base64.b64decode(image)))
                for image in image_byte_list.values()
            ]
            # image1 = Image.open('../outputs/Cute rabbi3.png')
            size_column = image_reize_dict["".join(str(st.session_state.output_size))]
            st.session_state["image_list"] = decode_image_list

            cols = st.columns(size_column)

            for idx, image in enumerate(st.session_state["image_list"]):
                cols[idx % size_column].image(image, use_column_width="auto")

            st.session_state.submit = False

        else:
            if st.session_state["image_list"]:
                output_size = st.session_state.save_parameter["size"]
                size_column = image_reize_dict["".join(str(output_size))]
                cols = st.columns(size_column)

                for idx, image in enumerate(st.session_state["image_list"]):
                    cols[idx % size_column].image(image, use_column_width="auto")

    with right:

        output_option = st.selectbox("output_size", ("128", "256", "512"))
        st.write(output_option)
        st.markdown("##")

        model_option = st.selectbox(
            "Select Model",
            ("stable_diffusion_v1-5", "stable_diffusion_v2-1"),
            label_visibility="visible",
        )

        st.write(model_option)
        st.markdown("##")

        num_inference = st.slider("", 0, 8, 4, label_visibility="hidden")
        st.write(f"num_inference : {num_inference}")
        st.markdown("##")

        guidance_scale = st.slider("", 0, 100, 20, label_visibility="hidden")
        st.write(f"cfg_scale : {guidance_scale}")
        st.markdown("##")

        inference_step = st.slider("", 0, 100, 30, label_visibility="hidden")
        st.write(f"inference_step : {inference_step}")

        st.session_state["output_size"] = int(output_option)
        st.session_state["num_inference"] = int(num_inference)
        st.session_state["guidance_scale"] = int(guidance_scale)
        st.session_state["inference_step"] = int(inference_step)


if __name__ == "__main__":
    main()

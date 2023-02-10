# BentoML

## BentoML을 통해 ML Serving을 진행합니다.

폴더는 다음과 같은 구조를 가지고 있습니다.
'''
📦bentoml
┣ 📂eng_serve
┃ ┣ 📂models
┃ ┃ ┣ 📂notoemoji
┃ ┃ ┃ ┣ 📜custom_checkpoint_0.pkl
┃ ┃ ┃ ┣ 📜optimizer.bin
┃ ┃ ┃ ┣ 📜pytorch_lora_weights.bin
┃ ┃ ┃ ┣ 📜pytorch_model.bin
┃ ┃ ┃ ┣ 📜random_states_0.pkl
┃ ┃ ┃ ┣ 📜scaler.pt
┃ ┃ ┃ ┗ 📜scheduler.bin
┃ ┃ ┗ 📂openmoji
┃ ┃ ┃ ┣ 📜custom_checkpoint_0.pkl
┃ ┃ ┃ ┣ 📜optimizer.bin
┃ ┃ ┃ ┣ 📜pytorch_lora_weights.bin
┃ ┃ ┃ ┣ 📜pytorch_model.bin
┃ ┃ ┃ ┣ 📜random_states_0.pkl
┃ ┃ ┃ ┣ 📜scaler.pt
┃ ┃ ┃ ┗ 📜scheduler.bin
┃ ┣ 📜bentofile_eng_model.yaml
┃ ┣ 📜configuration.yaml
┃ ┣ 📜requirements.txt
┃ ┗ 📜service.py
┣ 📂kor_serve
┃ ┣ 📂models
┃ ┃ ┗ 📂openmoji
┃ ┃ ┃ ┣ 📜custom_checkpoint_0.pkl
┃ ┃ ┃ ┣ 📜optimizer.bin
┃ ┃ ┃ ┣ 📜pytorch_lora_weights.bin
┃ ┃ ┃ ┣ 📜pytorch_model.bin
┃ ┃ ┃ ┣ 📜random_states_0.pkl
┃ ┃ ┃ ┣ 📜scaler.pt
┃ ┃ ┃ ┗ 📜scheduler.bin
┃ ┣ 📜bentofile_kor_model.yaml
┃ ┣ 📜configuration.yaml
┃ ┣ 📜requirements.txt
┃ ┗ 📜service.py
┣ 📂models
┃ ┗ 📂eng_model
┃ ┃ ┣ 📜custom_checkpoint_0.pkl
┃ ┃ ┣ 📜optimizer.bin
┃ ┃ ┣ 📜pytorch_lora_weights.bin
┃ ┃ ┣ 📜pytorch_model.bin
┃ ┃ ┣ 📜random_states_0.pkl
┃ ┃ ┣ 📜scaler.pt
┃ ┃ ┗ 📜scheduler.bin
┣ 📜bentofile_multilingual_model.yaml
┣ 📜configuration.yaml
┣ 📜readme.md
┣ 📜requirements.txt
┗ 📜service.py

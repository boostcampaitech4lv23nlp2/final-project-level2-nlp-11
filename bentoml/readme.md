# **BentoML Diffusion Model serving**

bentoml 폴더는 bentoml을 사용하여 어떻게 diffusion 모델을 서빙할 수 있는지를 제공합니다.

영어 텍스트를 입력받는 모델을 서빙하는 eng_serve폴더,
한국어 텍스트를 입력받아 이모지를 생성하는 kor_serve폴더 두 가지로 구성되어있습니다.

## **Bentoml**

![bentoml](image/bentoml-readme-header.jpeg)
**Bentoml:Unified Model Serving Framework**

BentoML은 다양한 환경에 쉽게 공유하고 배포할 수 있는 형식으로 기계 학습 모델을 패키징하기 위한 오픈 소스 프레임워크입니다.

### **BentoML을 통해 구축해야하는 이유는 무엇인가요?**

모델 배포는 머신 러닝 수명 주기의 마지막이자 가장 중요한 단계 중 하나입니다. 머신 러닝 모델을 프로덕션 환경에 적용하고 최종 애플리케이션에 대한 예측을 수행해야만 ML의 잠재력을 최대한 실현할 수 있습니다.

**데이터 과학과 엔지니어링의 교차점에 위치한 모델 배포는 팀 간에 새로운 운영 문제를 발생시킵니다.**

일반적으로 모델 구축 및 학습을 담당하는 데이터 과학자는 모델을 프로덕션에 적용할 수 있는 전문 지식이 없는 경우가 많습니다. 동시에, 지속적인 반복과 개선이 필요한 모델 작업에 익숙하지 않은 엔지니어는 자신의 노하우와 일반적인 관행(예: CI/CD)을 활용하여 모델을 배포하는 데 어려움을 겪습니다. 두 팀이 중간에서 만나 모델을 완성하려고 노력하다 보면 시간이 많이 걸리고 오류가 발생하기 쉬운 워크플로가 발생하여 진행 속도가 느려질 수 있습니다.

BentoML은 빠르고 반복 가능하며 확장 가능한 방식으로 ML 모델을 출시하고자 합니다. BentoML은 프로덕션 배포로의 핸드오프를 간소화하도록 설계되어 개발자와 데이터 과학자 모두 쉽게 모델을 테스트, 배포하고 다른 시스템과 통합할 수 있습니다.

데이터 과학자는 BentoML을 사용하여 모델을 만들고 개선하는 데 주로 집중할 수 있으며, 배포 엔지니어는 배포 로직이 변경되지 않고 프로덕션 서비스가 안정적이라는 사실에 안심할 수 있습니다.
-Bentoml 공식 문서 인용-

### **장점**

**Bento 패키지화를 통해 쉽게 버전 생성 및 공유, 배포가 가능하다.**

-   도커 이미지 및 패키지 설치 스크립트를 자동으로 생성해 주기 때문에,
    서버 확장 시 동일 환경 구축 자동화를 쉽게 할 수 있습니다.

**모델 배포를 위한 공통 도구와 API를 제공합니다.**

-   함수의 Docstring을 기반으로 API에 대한 설명을 생성합니다.
-   로거, 디버그 도구 등 개발 및 배포에 도움을 주는 도구를 제공합니다.

**다양한 프레임워크 지원**

-   Bentoml은 sklearn, Transformers, Keras, Pytorch lightning등 다양한 프레임워크를 지원합니다.(해당 프로젝트에서는 신생 프레임워크인 Diffusers사용하여 커스텀 하여사용)

## **사용 방법**

## **폴더 구조**

폴더 구조는 다음과 같습니다.

```
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
 ┃ ┣ 📜bentofile_kor_model.yaml
 ┃ ┣ 📜configuration.yaml
 ┃ ┣ 📜requirements.txt
 ┃ ┗ 📜service.py
 ┣ 📜readme.md
 ┗ 📜requirements.txt
```

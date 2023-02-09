import requests

data = {
  "prompt": "a cute bunny rabbit",
  "guidance_scale": 30,
  "num_inference": 2,
  "inference_step": 30,
  "resize": 256
}
response = requests.post("http://localhost:6026/submit",json= data)
export MODEL_NAME="runwayml/stable-diffusion-v1-5"
export INSTANCE_DIR="datasets/dreambooth/noto_sans"
export OUTPUT_DIR="models/noto-emoji-dreambooth"

accelerate launch dreambooth.py \
  --pretrained_model_name_or_path=$MODEL_NAME  \
  --instance_data_dir=$INSTANCE_DIR \
  --output_dir=$OUTPUT_DIR \
  --train_text_encoder \
  --instance_prompt="noto-emoji style" \
  --resolution=512 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=1 --gradient_checkpointing \
  --max_train_steps=5000 \
  --learning_rate=2e-6 --lr_scheduler="constant" --lr_warmup_steps=0 \
  --seed=42 \
  --checkpointing_steps=5200 \
  --hub_model_id="kuotient/noto-emoji-dreambooth" \
  --push_to_hub
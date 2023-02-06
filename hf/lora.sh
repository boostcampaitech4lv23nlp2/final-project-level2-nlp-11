accelerate launch --mixed_precision="fp16" lora.py 
export MODEL_NAME="runwayml/stable-diffusion-v1-5"
export DATASET_NAME="soypablo/Emoji_Dataset-Openmoji"

accelerate launch --mixed_precision="fp16" lora.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --dataset_name=$DATASET_NAME --caption_column="text" \
  --output_dir="models/emoji-model-lora" \
  --resolution=512 --random_flip \
  --train_batch_size=4 \
  --gradient_accumulation_steps=4 \
  --gradient_checkpointing \
  --max_train_steps=30000 \
  --checkpointing_steps=500 \
  --learning_rate=1e-04 --lr_scheduler="constant" --lr_warmup_steps=0 \
  --seed=42 \
  --validation_prompt="Cute rabbit wearing a blue hat and eating a carrot" --report_to="wandb" \
  # --hub_model_id="kuotient/emoji-model-finetuned-lora"
  # --push_to_hub
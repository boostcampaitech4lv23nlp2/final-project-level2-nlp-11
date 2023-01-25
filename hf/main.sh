export MODEL_NAME="runwayml/stable-diffusion-v1-5"
export dataset_name="soypablo/Emoji_Dataset-Openmoji"

accelerate launch --mixed_precision="fp16"  main.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --dataset_name=$dataset_name \
  --use_ema \
  --resolution=512 --center_crop --random_flip \
  --train_batch_size=4 \
  --gradient_accumulation_steps=4 \
  --gradient_checkpointing \
  --max_train_steps=30400 \
  --learning_rate=1e-05 \
  --max_grad_norm=1 \
  --lr_scheduler="constant" --lr_warmup_steps=0 \
  --output_dir="emoji-model"  \
  --use_8bit_adam \
  --checkpointing_steps=30000
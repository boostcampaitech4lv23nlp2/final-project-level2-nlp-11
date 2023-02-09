export MODEL_NAME="Norod78/sd15-fluentui-emoji"
export INSTANCE_DIR="datasets/dreambooth"
export OUTPUT_DIR="models/emoji-dreambooth-lora-2"

accelerate launch dreambooth-lora.py \
  --pretrained_model_name_or_path=$MODEL_NAME  \
  --instance_data_dir=$INSTANCE_DIR \
  --output_dir=$OUTPUT_DIR \
  --instance_prompt="a photo of sks dog" \
  --resolution=512 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=1 \
  --max_train_steps=1200 \
  --checkpointing_steps=100 \
  --learning_rate=2e-6 --lr_scheduler="constant" --lr_warmup_steps=0 \
  --seed=42 \
  --report_to="wandb" \
  --validation_prompt="A photo of sks dog in a bucket" \
  --validation_epochs=50 \
  --hub_model_id="kuotient/emoji-dreambooth-lora"
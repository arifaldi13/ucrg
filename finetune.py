import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

from huggingface_hub import notebook_login
notebook_login()

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

dataset = load_dataset("json", data_files="train_dataset.jsonl", split="train")

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    trust_remote_code=True
)
model.config.use_cache = False
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

training_config = SFTConfig(
    output_dir="./results",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    max_steps=300,
    logging_steps=10,
    dataset_text_field="text",
    max_seq_length=512,
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=lora_config,
    processing_class=tokenizer,
    args=training_config,
)

print("Starting the training process...")
trainer.train()
print("Training finished!")

output_model_dir = "ucrg-tinyllama-finetuned"
trainer.save_model(output_model_dir)
print(f"Model saved to {output_model_dir}")
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from datasets import load_dataset
from config import settings

def train():
    model_id = settings.VLLM_MODEL
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
    model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")
    model = prepare_model_for_kbit_training(model)
    peft_config = LoraConfig(lora_alpha=16, lora_dropout=0.1, r=64, bias="none", task_type="CAUSAL_LM")
    model = get_peft_model(model, peft_config)

    dataset = load_dataset("json", data_files=settings.TRAINING_DATA_PATH, split="train")
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        dataset_text_field="messages",
        max_seq_length=2048,
        tokenizer=tokenizer,
        args=TrainingArguments(
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            num_train_epochs=3,
            output_dir=settings.LORA_OUTPUT_DIR,
            logging_steps=10,
            save_strategy="epoch",
        ),
    )
    trainer.train()
    model.save_pretrained(settings.LORA_OUTPUT_DIR)
    tokenizer.save_pretrained(settings.LORA_OUTPUT_DIR)
    print("QLoRA training complete!")

if __name__ == "__main__":
    train()
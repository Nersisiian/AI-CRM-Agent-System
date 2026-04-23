from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from config import settings
import torch

def merge():
    base_model = AutoModelForCausalLM.from_pretrained(settings.VLLM_MODEL, torch_dtype=torch.float16)
    tokenizer = AutoTokenizer.from_pretrained(settings.VLLM_MODEL)
    model = PeftModel.from_pretrained(base_model, settings.LORA_OUTPUT_DIR)
    merged = model.merge_and_unload()
    merged.save_pretrained("./models/merged-sales-agent")
    tokenizer.save_pretrained("./models/merged-sales-agent")
    print("Модель сохранена в ./models/merged-sales-agent")

if __name__ == "__main__":
    merge()
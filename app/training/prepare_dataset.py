import json

def convert_conversations_to_sharegpt(input_path, output_path):
    """Пример преобразования диалогов в формат ShareGPT для тонкой настройки."""
    with open(input_path, 'r', encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            data = json.loads(line)
            # Ожидаем {"messages": [{"role": "user", "content": ...}, {"role": "assistant", ...}]}
            f_out.write(json.dumps(data) + '\n')
    print(f"Dataset подготовлен: {output_path}")

if __name__ == "__main__":
    convert_conversations_to_sharegpt("raw_sales.jsonl", "data/training/sales_conversations.jsonl")
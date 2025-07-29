# gentune-flan
Genetic Algorithm used to optimise the finetunning of FLAN-T5

# library dependecies
The following libraries must be installed for the library gentune-flan to work

pip install evaluate, transformers, rouge-score, pandas, numpy, torch

# the gentune-flan library
pip install gentune-flan

# Example (Summery creation from FLAN-T5 Base Model)

import gentune-flan

dataset = dataset = load_dataset("cnn_dailymail", "3.0.0", cache_dir="./hf_cache")

test_data = dataset["test"].select(range(100))

prompts = []
references = []

for ex in (list(test_data))[0:10]:
    article = ex.get("article", "")
    summary = ex.get("highlights", "")
    if isinstance(article, str) and isinstance(summary, str) and article.strip() != "" and summary.strip() != "":
        prompt = f"Summarize the following article:\n\n{article.strip()}\n\nSummary:"
        prompts.append(prompt)
        references.append(summary.strip())

params = {
            "max_length": [200, 300,400,500,600,700],
            "temperature": [0.1,0.3,0.5,0.7,0.9,1],
            "top_k": [10,20,30,50,70,90,100],
            "top_p": [0.2,0.3,0.5,0.7,0.9],
            "do_sample": True,       # Enables sampling-based decoding
            "num_beams": 1           # Beam search disabled (greedy/sample)
        }

args = gentune-flan.optimize_flan_t5_base(prompts=prompts, references=references,   params=params,      error_metric='ROUGE-L', number_of_generation = 2, mutation_rate=0.05, population_size=4, random_seed=2025)
print(args)

model_name = "google/flan-t5-base"  # or your fine-tuned path
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

inputs = tokenizer(
                  prompts,
                  return_tensors="pt",
                  padding=True,
                  truncation=True,
                  max_length=512
              )

with torch.no_grad():
            outputs = model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                **args
            )

decoded_preds = tokenizer.batch_decode(outputs, skip_special_tokens=True)

rouge = evaluate.load("rouge")
result = rouge.compute(predictions=decoded_preds, references=references, use_stemmer=True)

rouge_value = round(result['rougeL'] * 100, 2)
print(rouge_value)


# Default Hyperparameter value range

max_length : [50,100,150,200,250,300]
temperature : [0.2,0.4,0.6,0.8]
top_k : [10,20,30,40,50]
top_p : [0.3,0.5,0.7,0.9]

error_metric = 'ROUGE-L' (user can check for 'ROUGE-1', 'ROUGE-2' also)
number_of_generation = 3 (user can increase the value for better evolution)
mutation_rate = 0.05
population_size = 10 (user can increase the value for larger set for better results)

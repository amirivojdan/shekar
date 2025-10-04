import os
from transformers import (
    AlbertTokenizer,
    AutoModelForMaskedLM,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

from datasets import load_dataset
from shekar import Normalizer

normalizer = Normalizer()
num_cpus = os.cpu_count() - 10
datasets = load_dataset("SLPL/naab")

tokenizer = AlbertTokenizer.from_pretrained(
    "shekar-ai/albert-base-v2-persian-zwnj-naab-mlm", use_fast=True
)

def tokenize_function(examples):
    # Normalize the text using shekar normalizer
    examples["text"] = [normalizer(text) for text in examples["text"]]
    # Apply the cleaning pipeline
    return tokenizer(examples["text"])


tokenized_datasets = datasets.map(
    tokenize_function, batched=True, num_proc=num_cpus, remove_columns=["text"]
)

block_size = tokenizer.model_max_length

def group_texts(examples):
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated_examples[list(examples.keys())[0]])

    total_length = (total_length // block_size) * block_size

    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated_examples.items()
    }
    result["labels"] = result["input_ids"].copy()
    return result


lm_datasets = tokenized_datasets.map(
    group_texts,
    batched=True,
    batch_size=1000,
    num_proc=num_cpus,
)

model = AutoModelForMaskedLM.from_pretrained(
    "shekar-ai/albert-base-v2-persian-zwnj-naab-mlm"
)
model.resize_token_embeddings(len(tokenizer))
model_checkpoint = "shekar-ai/albert-base-v2-persian-zwnj-naab-mlm"

training_args = TrainingArguments(
    model_checkpoint,
    overwrite_output_dir="True",
    eval_strategy="steps",
    save_steps=50000,
    eval_steps=50000,
    warmup_steps=10000,
    learning_rate=2e-5,
    weight_decay=0.01,
    save_strategy="steps",
    save_total_limit=1,
    push_to_hub=True,
    hub_model_id=model_checkpoint,
    num_train_epochs=3,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    load_best_model_at_end=True,
    report_to="tensorboard",
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm_probability=0.15
)

lm_datasets = lm_datasets["train"].train_test_split(test_size=0.02, seed=42)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=lm_datasets["train"],
    eval_dataset=lm_datasets["test"],
    data_collator=data_collator,
)

trainer.train()

trainer.push_to_hub(commit_message="Training complete", blocking=True)

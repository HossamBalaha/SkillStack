---
name: transformer-finetuner
description: Fine-tune Hugging Face transformers for text classification, token classification, or sequence-to-sequence tasks. Triggers on "Hugging Face", "transformers Trainer", "TrainingArguments", "warmup_ratio", "weight_decay", "fp16 bf16", "LoRA PEFT", "tokenize dataset", "compute_metrics".
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: ml-engineering
tags: [huggingface, transformers, finetuning, peft]
related: [ml-engineering/pytorch-lightning-scaffold, ml-engineering/model-explainer, ml-engineering/mixed-precision-trainer]
prerequisites: [ml-engineering/modular-ml-architect]
outputs: [python, json]
difficulty: advanced
estimated_tokens: 2400
cost_warning: "Optional: HuggingFace API inference may incur costs if using paid endpoints."
permissions:
  read_files: true
  write_files: true
  network: true
  execute_code: true
language: en
---

# Transformer Finetuner

## When To Use
- Fine-tuning a pretrained LM (BERT, RoBERTa, T5, LLaMA) on a downstream task.
- Running parameter-efficient fine-tuning with LoRA / PEFT.
- Configuring `TrainingArguments` (batch size, learning rate, warmup, weight decay, fp16/bf16).
- Monitoring train/validation gap for overfitting diagnostics.

## Workflow
1. Load the pretrained tokenizer and model from `transformers.AutoModelForSequenceClassification`.
2. Tokenize the dataset with `tokenizer(text, truncation=True, padding="max_length")`.
3. Convert to a `datasets.Dataset` and split into train/validation/test.
4. Build `TrainingArguments` with per_device_train_batch_size, learning_rate, num_train_epochs, warmup_ratio, weight_decay, eval_strategy, save_strategy, fp16/bf16.
5. Define `compute_metrics(eval_pred)` returning accuracy, F1, AUC.
6. Instantiate `Trainer(model, args, train_dataset, eval_dataset, compute_metrics)`.
7. Optionally attach a `peft.LoraConfig` for parameter-efficient fine-tuning.
8. Enable early stopping and gradient clipping.
9. Call `trainer.train()` then `trainer.evaluate()`.
10. Save the fine-tuned model and tokenizer to disk.

## Inputs
- A Hugging Face model identifier (e.g. `bert-base-uncased`).
- A labeled text dataset (CSV, JSON, or `datasets.Dataset`).
- `Configs/Config.yaml` with training hyperparameters.

## Outputs
- Fine-tuned model + tokenizer saved to `Results/{DatasetName}_{Timestamp}/Train/`.
- Trainer log history saved as CSV.
- Evaluation metrics JSON.

## Key Rules
- Use `peft` library for LoRA / PEFT when full fine-tuning is too expensive.
- Monitor train vs validation loss gap to detect overfitting.
- Use `bf16=True` on Ampere+ GPUs; fall back to `fp16=True` otherwise.
- `eval_strategy` and `save_strategy` should match (e.g. both `"epoch"`).
- Reference only real HuggingFace docs at https://huggingface.co/docs/transformers.

## Examples
```python
# Fine-tune BERT with optional LoRA.
from transformers import (
  AutoTokenizer,
  AutoModelForSequenceClassification,
  TrainingArguments,
  Trainer
)
from datasets import Dataset
import numpy as np
from sklearn.metrics import accuracy_score, f1_score


def TokenizeDataset(Texts, Labels, ModelName, MaxLength):
  """Tokenize texts and wrap into a Hugging Face Dataset."""
  # Load the tokenizer matching the model.
  tokenizer = AutoTokenizer.from_pretrained(ModelName)
  # Tokenize with truncation and padding.
  encodings = tokenizer(
    Texts,
    truncation=True,
    padding="max_length",
    max_length=MaxLength
  )
  # Build a datasets.Dataset from the encodings.
  dataset = Dataset.from_dict({
    "input_ids": encodings["input_ids"],
    "attention_mask": encodings["attention_mask"],
    "labels": Labels
  })
  return dataset, tokenizer


def ComputeMetrics(EvalPred):
  """Return accuracy and macro F1."""
  # Unpack logits and labels.
  logits, labels = EvalPred
  # Argmax for predicted class.
  preds = np.argmax(logits, axis=-1)
  return {
    "Accuracy": accuracy_score(labels, preds),
    "F1Macro": f1_score(labels, preds, average="macro")
  }


def BuildTrainer(Model, Tokenizer, TrainDataset, EvalDataset, Config, OutputDir):
  """Build the HF Trainer with the configured arguments."""
  # Configure training arguments.
  args = TrainingArguments(
    output_dir=OutputDir,
    per_device_train_batch_size=Config["BatchSize"],
    per_device_eval_batch_size=Config["BatchSize"],
    learning_rate=Config["LearningRate"],
    num_train_epochs=Config["Epochs"],
    warmup_ratio=0.1,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    fp16=True,
    load_best_model_at_end=True,
    metric_for_best_model="F1Macro"
  )
  return Trainer(
    model=Model,
    args=args,
    train_dataset=TrainDataset,
    eval_dataset=EvalDataset,
    processing_class=Tokenizer,
    compute_metrics=ComputeMetrics
  )
```

## References
- Hugging Face Transformers docs: https://huggingface.co/docs/transformers
- PEFT library: https://huggingface.co/docs/peft
- TrainingArguments reference: https://huggingface.co/docs/transformers/main_classes/trainer#transformers.TrainingArguments

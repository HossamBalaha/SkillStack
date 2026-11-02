---
name: coding-conventions-enforcer
description: Enforce five strict Python coding rules across an entire repository — camelCase variables, CamelCase functions/classes/files/dict-keys, parenthesized if-conditions, period-terminated comments above every statement, and double-quoted strings. Use when auditing Python code, preparing ML/DL repos for review, or onboarding contributors to a strict-style codebase.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [python, style, lint, camelcase, conventions]
related: [ml-engineering/modular-ml-architect, style-integrity/latex-style-guard, ml-engineering/reproducible-experiment-runner]
prerequisites: []
outputs: [python]
difficulty: intermediate
estimated_tokens: 2500
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Coding Conventions Enforcer

## When To Use

- User asks to "lint", "format", "audit", or "standardize" a Python codebase.
- A machine-learning or deep-learning repo needs a strict style pass before submission.
- Contributor code mixes camelCase and snake_case inconsistently.
- Comments are missing, lowercase, or do not end with a period.
- Strings mix single and double quotes arbitrarily.

## Workflow

1. Enumerate every `.py` file in the repo (excluding `__pycache__`, `.venv`, `node_modules`).
2. For each file, scan declarations and statements against the five rules below.
3. Apply Rule 1 (camelCase variables): rename local and module-level variables from `snake_case` to `camelCase`.
4. Apply Rule 2 (CamelCase functions, classes, file names, dict keys): rename `def process_data(...)` to
   `def ProcessData(...)`; rename `data_utils.py` to `DataUtils.py`; rename dict key `"validation_status"` to
   `"ValidationStatus"`. Functions must NOT be camelCase — they must be CamelCase.
5. Apply Rule 3 (parenthesized if-conditions): rewrite `if x > 0:` as `if (x > 0):`. Same for `elif` and `while`.
6. Apply Rule 4 (comment above every statement, ending with a period): insert a descriptive comment directly above each
   statement. Every comment MUST end with `.`.
7. Apply Rule 5 (double-quoted strings): convert `'hello'` to `"hello"` everywhere except inside docstrings.
8. Enforce infrastructure: a centralized `Configs/Config.yaml` exists at repo root. Every `nn.Module` uses
   `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")` with `.to(device)`.
9. Enforce 2-space indentation across every file.
10. Attach the canonical docstring template to every public function and class.
11. Re-run the scanner to confirm zero violations remain.
12. Produce a per-file change report: rule, count, sample before/after.

## Inputs

- Repository root path.
- Optional list of framework-mandated lowercase method names to preserve.
- Existing `Configs/Config.yaml` if present (else create one).

## Outputs

- Modified `.py` files conforming to all five rules.
- `Configs/Config.yaml` centralized config (created if missing).
- A per-file change report.
- A violations summary listing any unfixable items (e.g., external API names).

## Key Rules

### Rule 1 — Variables use camelCase

Local, module-level, and non-framework parameters use camelCase: `dataSourceUrl`, `modelParameters`, `batchSize`,
`learningRate`.

### Rule 2 — Functions, classes, file names, AND dict keys use CamelCase

Functions: `ProcessData`, `TrainModel`. Classes: `DataProcessor`, `VisualizationUtils`. Files: `DataUtils.py`,
`ModelTrainer.py`. Dict keys: `"ValidationStatus"`, `"LearningRate"`. Functions must NOT be camelCase.

### Rule 3 — if statements wrap conditions in parentheses

Every `if`, `elif`, `while` condition is wrapped in parentheses: `if (condition):`.

### Rule 4 — Descriptive comment above EVERY statement, ending with a period

Every statement has a comment on the line directly above it. Every comment ends with `.`. No exceptions.

### Rule 5 — Double-quoted strings, except in docstrings

All string literals use `"..."`. Docstrings retain `"""..."""` triple-double-quote form.

### Exemption — Framework-mandated lowercase method names

Names kept lowercase because the framework dispatches by exact name:

- PyTorch: `forward`, `backward`, `reset_parameters`, `extra_repr`, `load_state_dict`, `state_dict`.
- PyTorch Lightning: `training_step`, `validation_step`, `test_step`, `configure_optimizers`, `on_train_start`,
  `on_validation_end`.
- unittest: `setUp`, `tearDown`, `setUpClass`, `tearDownClass`, `runTest`.

Their internals still follow Rules 1–5.

### Indentation — exactly 2 spaces

No tabs. No 4-space indentation.

### Infrastructure — Centralized config and device handling

- `Configs/Config.yaml` at repository root holds all hyperparameters, paths, and flags.
- Every script declaring an `nn.Module` sets `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")` and
  calls `model.to(device)` plus `.to(device)` on input tensors.

## Canonical Docstring Template

```python
def TrainModel(ModelClass, TrainingData, LearningRate, Epochs):
    """
    Trains a model on the provided training data.

    Args:
        ModelClass (type): The model class to instantiate.
        TrainingData (DataLoader): Loader yielding training batches.
        LearningRate (float): Initial learning rate for the optimizer.
        Epochs (int): Number of training epochs.

    Returns:
        tuple[nn.Module, dict]: The trained model and a "Metrics" dictionary
            with "TrainingLoss" and "ValidationAccuracy" entries.

    Raises:
        ValueError: If Epochs is non-positive.
    """
    # Validate the epoch count.
    if (Epochs <= 0):
        raise ValueError("Epochs must be a positive integer.")
    # Instantiate the model and move it to the configured device.
    Model = ModelClass().to(device)
    # Build the optimizer.
    Optimizer = torch.optim.Adam(Model.parameters(), lr=LearningRate)
    # Train for the requested number of epochs.
    for EpochIndex in range(Epochs):
        # Iterate over training batches.
        for BatchIndex, (Inputs, Targets) in enumerate(TrainingData):
            # Move the batch to the device.
            Inputs = Inputs.to(device)
            # Move the targets to the device.
            Targets = Targets.to(device)
            # Zero the parameter gradients.
            Optimizer.zero_grad()
            # Run the forward pass.
            Outputs = Model(Inputs)
            # Compute the loss.
            Loss = torch.nn.functional.cross_entropy(Outputs, Targets)
            # Backpropagate the gradients.
            Loss.backward()
            # Update the parameters.
            Optimizer.step()
    # Return the trained model and a metrics dictionary.
    return Model, {"TrainingLoss": [], "ValidationAccuracy": []}
```

## Examples

### Rule 1 — camelCase variables

Before:

```python
data_source_url = "https://example.com/data"
batch_size = 32
```

After:

```python
# Define the URL of the data source.
dataSourceUrl = "https://example.com/data"
# Set the mini-batch size for stochastic gradient descent.
batchSize = 32
```

### Rule 2 — CamelCase functions, classes, files, dict keys

Before (`data_utils.py`):

```python
def process_data(record):
    return {"validation_status": "passed"}

class data_processor:
    pass
```

After (`DataUtils.py`):

```python
class DataProcessor:
    """Processes incoming records and emits a result dictionary."""
    pass


def ProcessData(Record):
    # Return a dictionary with a validation status key.
    return {"ValidationStatus": "passed"}
```

### Rule 3 — Parenthesized if-conditions

Before:

```python
if x > 0 and y < 10:
    print("ok")
elif x == 0:
    print("zero")
```

After:

```python
# Check whether x is positive and y is within range.
if (x > 0 and y < 10):
    # Print the success message.
    print("ok")
# Check whether x is exactly zero.
elif (x == 0):
    # Print the zero message.
    print("zero")
```

### Rule 4 — Comment above every statement, ending with a period

Before:

```python
total = 0
for i in range(10):
    total += i
```

After:

```python
# Initialize the running total to zero.
total = 0
# Accumulate integers from zero through nine.
for i in range(10):
    # Add the current index to the running total.
    total += i
```

### Rule 5 — Double-quoted strings

Before:

```python
greeting = 'hello'
path = '/home/user/data'
```

After:

```python
# Define the greeting string.
greeting = "hello"
# Define the filesystem path.
path = "/home/user/data"
```

### Framework-mandated exemption

Before:

```python
class MyModel(nn.Module):
    def forward(self, x):
        return self.layer(x)
```

After:

```python
class MyModel(nn.Module):
    """A minimal neural network module for demonstration purposes."""
    def forward(self, InputTensor):
        # Pass the input through the linear layer.
        return self.layer(InputTensor)
```

`forward` stays lowercase (PyTorch dispatch). The body follows Rules 1–5.

### Infrastructure — device handling

Before:

```python
model = MyModel()
outputs = model(inputs)
```

After:

```python
# Select the compute device.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Instantiate the model and move it to the device.
model = MyModel().to(device)
# Move the input tensor to the device.
inputs = inputs.to(device)
# Run the forward pass.
outputs = model(inputs)
```

## References

- PEP 8 (context only; this skill overrides PEP 8 where stated).
- PyTorch `nn.Module` documentation: https://pytorch.org/docs/stable/generated/torch.nn.Module.html
- PyTorch Lightning lifecycle hooks: https://lightning.ai/docs/pytorch/stable/common/lightning_module.html
- Python `unittest` framework: https://docs.python.org/3/library/unittest.html

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
language: zh
---

# 编码规范执行器

## 何时使用

- 用户要求对一个 Python 代码库进行"lint"、"format"、"audit"或"standardize"。
- 机器学习或深度学习仓库在提交前需要一次严格风格检查。
- 贡献者代码不一致地混用 camelCase 与 snake_case。
- 注释缺失、全小写或未以句点结尾。
- 字符串任意混用单引号与双引号。

## 工作流程

1. 枚举仓库中的每个 `.py` 文件（排除 `__pycache__`、`.venv`、`node_modules`）。
2. 对每个文件，将声明和语句对照下方五条规则进行扫描。
3. 应用规则 1（camelCase 变量）：将局部和模块级变量从 `snake_case` 重命名为 `camelCase`。
4. 应用规则 2（CamelCase 函数、类、文件名、字典键）：把 `def process_data(...)` 重命名为 `def ProcessData(...)`；把
   `data_utils.py` 重命名为 `DataUtils.py`；把字典键 `"validation_status"` 重命名为 `"ValidationStatus"`。函数**不得**为
   camelCase——必须为 CamelCase。
5. 应用规则 3（带括号的 if 条件）：把 `if x > 0:` 改写为 `if (x > 0):`。`elif` 与 `while` 同理。
6. 应用规则 4（每条语句上方带描述性注释，以句点结尾）：在每条语句正上方插入描述性注释。每条注释**必须**以 `.` 结尾。
7. 应用规则 5（双引号字符串）：除 docstring 内部外，将所有 `'hello'` 转换为 `"hello"`。
8. 执行基础设施：仓库根目录存在集中化的 `Configs/Config.yaml`。每个 `nn.Module` 使用
   `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")` 并调用 `.to(device)`。
9. 在每个文件中执行 2 空格缩进。
10. 为每个公开函数和类附加标准 docstring 模板。
11. 重新运行扫描器以确认零违规残留。
12. 生成每文件变更报告：规则、计数、前后示例。

## 输入

- 仓库根路径。
- 可选：需要保留的框架强制小写方法名列表。
- 若存在则使用现有 `Configs/Config.yaml`（否则创建一个）。

## 输出

- 符合全部五条规则的已修改 `.py` 文件。
- 集中化的 `Configs/Config.yaml`（缺失时创建）。
- 每文件变更报告。
- 列出任何不可修复项（例如外部 API 名称）的违规摘要。

## 核心规则

### 规则 1 — 变量使用 camelCase

局部、模块级以及非框架参数使用 camelCase：`dataSourceUrl`、`modelParameters`、`batchSize`、`learningRate`。

### 规则 2 — 函数、类、文件名、字典键使用 CamelCase

函数：`ProcessData`、`TrainModel`。类：`DataProcessor`、`VisualizationUtils`。文件：`DataUtils.py`、`ModelTrainer.py`。字典键：
`"ValidationStatus"`、`"LearningRate"`。函数**不得**为 camelCase。

### 规则 3 — if 语句将条件括在括号内

每个 `if`、`elif`、`while` 条件都用括号包裹：`if (condition):`。

### 规则 4 — 每条语句上方带描述性注释，以句点结尾

每条语句正上方都有注释。每条注释以 `.` 结尾。无例外。

### 规则 5 — 双引号字符串，docstring 内部除外

所有字符串字面量使用 `"..."`。docstring 保留 `"""..."""` 三双引号形式。

### 豁免 — 框架强制的小写方法名

保持小写的名称，因为框架按精确名称分派：

- PyTorch：`forward`、`backward`、`reset_parameters`、`extra_repr`、`load_state_dict`、`state_dict`。
- PyTorch Lightning：`training_step`、`validation_step`、`test_step`、`configure_optimizers`、`on_train_start`、
  `on_validation_end`。
- unittest：`setUp`、`tearDown`、`setUpClass`、`tearDownClass`、`runTest`。

其内部仍遵循规则 1–5。

### 缩进 — 恰好 2 空格

无制表符。无 4 空格缩进。

### 基础设施 — 集中化配置与设备处理

- 仓库根目录的 `Configs/Config.yaml` 保存所有超参数、路径与开关。
- 每个声明 `nn.Module` 的脚本都设置 `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")` 并调用
  `model.to(device)` 以及对输入张量调用 `.to(device)`。

## 标准 docstring 模板

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

## 示例

### 规则 1 — camelCase 变量

之前：

```python
data_source_url = "https://example.com/data"
batch_size = 32
```

之后：

```python
# Define the URL of the data source.
dataSourceUrl = "https://example.com/data"
# Set the mini-batch size for stochastic gradient descent.
batchSize = 32
```

### 规则 2 — CamelCase 函数、类、文件、字典键

之前（`data_utils.py`）：

```python
def process_data(record):
    return {"validation_status": "passed"}

class data_processor:
    pass
```

之后（`DataUtils.py`）：

```python
class DataProcessor:
    """Processes incoming records and emits a result dictionary."""
    pass


def ProcessData(Record):
    # Return a dictionary with a validation status key.
    return {"ValidationStatus": "passed"}
```

### 规则 3 — 带括号的 if 条件

之前：

```python
if x > 0 and y < 10:
    print("ok")
elif x == 0:
    print("zero")
```

之后：

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

### 规则 4 — 每条语句上方带注释，以句点结尾

之前：

```python
total = 0
for i in range(10):
    total += i
```

之后：

```python
# Initialize the running total to zero.
total = 0
# Accumulate integers from zero through nine.
for i in range(10):
    # Add the current index to the running total.
    total += i
```

### 规则 5 — 双引号字符串

之前：

```python
greeting = 'hello'
path = '/home/user/data'
```

之后：

```python
# Define the greeting string.
greeting = "hello"
# Define the filesystem path.
path = "/home/user/data"
```

### 框架强制豁免

之前：

```python
class MyModel(nn.Module):
    def forward(self, x):
        return self.layer(x)
```

之后：

```python
class MyModel(nn.Module):
    """A minimal neural network module for demonstration purposes."""
    def forward(self, InputTensor):
        # Pass the input through the linear layer.
        return self.layer(InputTensor)
```

`forward` 保持小写（PyTorch 分派）。函数体遵循规则 1–5。

### 基础设施 — 设备处理

之前：

```python
model = MyModel()
outputs = model(inputs)
```

之后：

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

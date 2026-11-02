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
language: ar
---

# منفِّذ قواعد البرمجة

## متى تستخدم
- يطلب المستخدم "تنظيف" (lint) أو "تنسيق" (format) أو "تدقيق" (audit) أو "توحيد" قاعدة كود Python.
- مستودع تعلّم آليّ أو تعلّم عميق يحتاج إلى مرور نمط صارم قبل التقديم.
- كود المساهمين يمزج camelCase وsnake_case بشكل غير متّسق.
- التعليقات مفقودة أو بأحرف صغيرة أو لا تنتهي بنقطة.
- النصوص المُحاطة بعلامات اقتباس تمزج المفردة والمزدوجة بشكل عشوائيّ.

## سير العمل
1. عدّ كلّ ملفّ `.py` في المستودع (مع استبعاد `__pycache__` و`.venv` و`node_modules`).
2. لكلّ ملفّ، امسح التصريحات والعبارات مقابل القواعد الخمس أدناه.
3. طبِّق القاعدة 1 (متغيّرات camelCase): أعد تسمية المتغيّرات المحلّيّة وعلى مستوى الوحدة من `snake_case` إلى `camelCase`.
4. طبِّق القاعدة 2 (دوالّ وأصناف وأسماء ملفّات ومفاتيح قواميس CamelCase): أعد تسمية `def process_data(...)` إلى `def ProcessData(...)`؛ أعد تسمية `data_utils.py` إلى `DataUtils.py`؛ أعد تسمية مفتاح القاموس `"validation_status"` إلى `"ValidationStatus"`. الدوالّ يجب ألّا تكون camelCase — بل CamelCase.
5. طبِّق القاعدة 3 (شروط if بين قوسين): أعد كتابة `if x > 0:` كـ `if (x > 0):`. ينطبق نفس الأمر على `elif` و`while`.
6. طبِّق القاعدة 4 (تعليق فوق كلّ عبارة، ينتهي بنقطة): أدخل تعليقاً وصفياً مباشرةً فوق كلّ عبارة. يجب أن ينتهي كلّ تعليق بـ `.`.
7. طبِّق القاعدة 5 (نصوص بين علامتي اقتباس مزدوجتين): حوّل `'hello'` إلى `"hello"` في كلّ مكان ما عدا داخل docstrings.
8. افرض البنية التحتيّة: يوجد `Configs/Config.yaml` مركزيّ في جذر المستودع. كلّ `nn.Module` يستخدم `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")` مع `.to(device)`.
9. افرض مسافة بادئة بمقدار 2 فراغ في كلّ ملفّ.
10. أرفق قالب docstring القانونيّ بكلّ دالة وصنف عامّ.
11. أعد تشغيل الماسح للتأكّد من عدم بقاء أيّ مخالفة.
12. أنتج تقرير تغييرات لكلّ ملفّ: القاعدة، العدد، نموذج قبل/بعد.

## المُدخلات
- المسار الجذريّ للمستودع.
- قائمة اختياريّة بأسماء الطرق التي يفرضها إطار العمل بأحرف صغيرة للحفاظ عليها.
- `Configs/Config.yaml` الموجود إن وُجد (وإلاّ فأنشئ واحداً).

## المُخرجات
- ملفّات `.py` معدّلة تتوافق مع القواعد الخمس جميعاً.
- `Configs/Config.yaml` المركزيّ (يُنشأ إذا كان مفقوداً).
- تقرير تغييرات لكلّ ملفّ.
- ملخّص المخالفات يسرد أيّ عناصر غير قابلة للإصلاح (مثل أسماء API الخارجيّة).

## القواعد الأساسية

### القاعدة 1 — المتغيّرات تستخدم camelCase
المتغيّرات المحلّيّة وعلى مستوى الوحدة والمعاملات غير الخاصّة بالإطار تستخدم camelCase: `dataSourceUrl`، `modelParameters`، `batchSize`، `learningRate`.

### القاعدة 2 — الدوالّ والأصناف وأسماء الملفّات ومفاتيح القواميس تستخدم CamelCase
الدوالّ: `ProcessData`، `TrainModel`. الأصناف: `DataProcessor`، `VisualizationUtils`. الملفّات: `DataUtils.py`، `ModelTrainer.py`. مفاتيح القواميس: `"ValidationStatus"`، `"LearningRate"`. الدوالّ يجب ألّا تكون camelCase.

### القاعدة 3 — عبارات if تُحيط الشروط بأقواس
كلّ شرط `if` و`elif` و`while` مُحاط بأقواس: `if (condition):`.

### القاعدة 4 — تعليق وصفيّ فوق كلّ عبارة، ينتهي بنقطة
كلّ عبارة لها تعليق على السطر مباشرةً فوقها. كلّ تعليق ينتهي بـ `.`. بلا استثناء.

### القاعدة 5 — نصوص بين علامتي اقتباس مزدوجتين، ما عدا في docstrings
كلّ النصوص الحرفيّة تستخدم `"..."`. تحتفظ docstrings بالشكل الثلاثيّ المزدوج `"""..."""`.

### الإعفاء — أسماء الطرق التي يفرضها إطار العمل بأحرف صغيرة
أسماء تُحفظ بأحرف صغيرة لأنّ إطار العمل يُوزِّع حسب الاسم الدقيق:
- PyTorch: `forward`، `backward`، `reset_parameters`، `extra_repr`، `load_state_dict`، `state_dict`.
- PyTorch Lightning: `training_step`، `validation_step`، `test_step`، `configure_optimizers`، `on_train_start`، `on_validation_end`.
- unittest: `setUp`، `tearDown`، `setUpClass`، `tearDownClass`، `runTest`.

دواخلها لا تزال تتّبع القواعد 1–5.

### المسافة البادئة — 2 فراغ تماماً
لا tabs. لا مسافة بادئة 4 فراغات.

### البنية التحتيّة — إعداد مركزيّ للتكوين والجهاز
- `Configs/Config.yaml` في جذر المستودع يحوي كلّ المعاملات الفائقة والمسارات والأعلام.
- كلّ سكربت يُصرِّح عن `nn.Module` يضبط `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")` ويستدعي `model.to(device)` بالإضافة إلى `.to(device)` على مدخلات الموترّ.

## قالب docstring القانونيّ

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

## أمثلة

### القاعدة 1 — متغيّرات camelCase
قبل:
```python
data_source_url = "https://example.com/data"
batch_size = 32
```
بعد:
```python
# Define the URL of the data source.
dataSourceUrl = "https://example.com/data"
# Set the mini-batch size for stochastic gradient descent.
batchSize = 32
```

### القاعدة 2 — دوالّ وأصناف وملفّات ومفاتيح قواميس CamelCase
قبل (`data_utils.py`):
```python
def process_data(record):
    return {"validation_status": "passed"}

class data_processor:
    pass
```
بعد (`DataUtils.py`):
```python
class DataProcessor:
    """Processes incoming records and emits a result dictionary."""
    pass


def ProcessData(Record):
    # Return a dictionary with a validation status key.
    return {"ValidationStatus": "passed"}
```

### القاعدة 3 — شروط if بين قوسين
قبل:
```python
if x > 0 and y < 10:
    print("ok")
elif x == 0:
    print("zero")
```
بعد:
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

### القاعدة 4 — تعليق فوق كلّ عبارة، ينتهي بنقطة
قبل:
```python
total = 0
for i in range(10):
    total += i
```
بعد:
```python
# Initialize the running total to zero.
total = 0
# Accumulate integers from zero through nine.
for i in range(10):
    # Add the current index to the running total.
    total += i
```

### القاعدة 5 — نصوص بين علامتي اقتباس مزدوجتين
قبل:
```python
greeting = 'hello'
path = '/home/user/data'
```
بعد:
```python
# Define the greeting string.
greeting = "hello"
# Define the filesystem path.
path = "/home/user/data"
```

### إعفاء إطار العمل
قبل:
```python
class MyModel(nn.Module):
    def forward(self, x):
        return self.layer(x)
```
بعد:
```python
class MyModel(nn.Module):
    """A minimal neural network module for demonstration purposes."""
    def forward(self, InputTensor):
        # Pass the input through the linear layer.
        return self.layer(InputTensor)
```
يبقى `forward` بأحرف صغيرة (توزيع PyTorch). يتبع الجسم القواعد 1–5.

### البنية التحتيّة — إعداد الجهاز
قبل:
```python
model = MyModel()
outputs = model(inputs)
```
بعد:
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

## المراجع
- PEP 8 (للسياق فقط؛ هذه المهارة تتجاوز PEP 8 حيثما تنصّ).
- توثيق PyTorch `nn.Module`: https://pytorch.org/docs/stable/generated/torch.nn.Module.html
- خطافات دورة حياة PyTorch Lightning: https://lightning.ai/docs/pytorch/stable/common/lightning_module.html
- إطار عمل `unittest` في Python: https://docs.python.org/3/library/unittest.html

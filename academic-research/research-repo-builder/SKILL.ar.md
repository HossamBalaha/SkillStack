---
name: research-repo-builder
description: Scaffold a complete modular research repository from an approved plan, including src/data, src/models, src/utils, Configs/Config.yaml, manual/ chapters, Datasets.md, unversioned Requirements.txt, CreateProjectZip.py, and Main.py entry point. Use when the user asks to scaffold, bootstrap, or generate a research codebase skeleton.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [scaffolding, repository, project-structure]
related: [style-integrity/coding-conventions-enforcer, ml-engineering/modular-ml-architect, academic-research/reproducibility-checklist-author]
prerequisites: []
outputs: [python, markdown, bash]
difficulty: intermediate
estimated_tokens: 1800
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: ar
---

# باني مستودع البحث

## متى تستخدم

- يقول المستخدم "أنشئ مستودع بحث" أو "أنشئ هيكل مشروع" أو "أعدّ قاعدة الكود خاصّتي".
- لدى المستخدم خطة معتمدة ويريد تجسيد شجرة الدليل.
- يريد المستخدم بنية قابلة للتكرار: تكوينات، أدلّة، سكربتات، بيانات مجموعات البيانات.
- كلمات مفتاحيّة مُحفِّزة: أنشئ، هيِّئ، شجرة المستودع، بنية المشروع، CreateProjectZip، Main.py.

## سير العمل

1. اقرأ الخطة المعتمدة (الملخّص التنفيذيّ، قائمة الكود، شجرة المستودع) من خطوة التأمّل أو إدخال المستخدم.
2. أنشئ دليل المشروع الجذريّ المُسمّى على اسم سبيكة المشروع.
3. ابنِ شجرة الدليل أدناه. ضع `.gitkeep` في كلّ دليل سيكون فارغاً لولا ذلك.
4. اكتب `Configs/Config.yaml` بأقسام لـ `data` و`model` و`training` و`evaluation` و`paths` و`random_seed`.
5. أنشئ `Main.py` كمنسّق: حلّل التكوين، ابنِ محمّل البيانات، استنسخ النموذج، حلقة التدريب، حلقة التقييم، احفظ المنتجات.
6. أنشئ `src/data/loader.py` و`src/data/preprocess.py` و`src/models/baseline.py` و`src/models/proposed.py` و
   `src/utils/metrics.py` و`src/utils/logger.py`.
7. اكتب `Datasets.md` موثِّقاً المصدر والترخيص والتقسيمات والمعالجة المسبقة ومتطلّبات الاستشهاد.
8. اكتب `Requirements.txt` (غير مُصدَّر افتراضيّاً؛ ثبّت الإصدارات فقط عند طلب المستخدم).
9. أضِف `CreateProjectZip.py` يضغط المستودع مع استبعاد `data/raw` و`outputs` و`.git`.
10. أضِف `.gitignore` يغطّي `__pycache__/` و`*.pyc` و`data/raw/` و`outputs/` و`.venv/` و`.env`.
11. أضِف `README.md` بالبدء السريع والتثبيت والتدريب وأوامر التقييم وكتلة الاستشهاد.
12. اطبع الشجرة الناتجة وتأكّد أنّ كلّ دليل يحوي إمّا محتوى أو `.gitkeep`.

## المُدخلات

- سبيكة المشروع (kebab-case).
- خطة معتمدة بقائمة الوحدات ومخطّط التكوين.
- اختياريّ: اختيار إطار العمل (PyTorch، JAX، TensorFlow).
- اختياريّ: قائمة مجموعات بيانات لتسجيلها في `Datasets.md`.

## المُخرجات

- شجرة دليل مُجسَّدة تحت سبيكة المشروع.
- `Configs/Config.yaml`، `Main.py`، `Requirements.txt`، `Datasets.md`، `README.md`، `CreateProjectZip.py`، `.gitignore`.
- `.gitkeep` في كلّ دليل فارغ.
- مخطّط شجرة مطبوع للتحقّق.

## القواعد الأساسية

- كلّ دليل يجب أن يحوي إمّا محتوى حقيقيّاً أو `.gitkeep`؛ لا تترك دليلاً فارغاً أبداً.
- `Requirements.txt` غير مُصدَّر إلا إذا طلب المستخدم صراحةً التثبيت.
- قيم التكوين يجب الإشارة إليها، لا ترميزها داخل `Main.py` والوحدات.
- يجب أن يتضمّن `Datasets.md` الترخيص ومتطلّبات الاستشهاد لكلّ مجموعة بيانات.
- يجب أن يستثني `CreateProjectZip.py` البيانات الخام والمخرجات و`.git` لإبقاء الأرشيف صغيراً وقابلاً للمشاركة.
- لا تُلتزم الأسرار؛ يجب أن يكون `.env` في `.gitignore`.

## أمثلة

```text
Project tree generated:
my-project/
├── Configs/
│   ├── Config.yaml
│   └── .gitkeep
├── Datasets.md
├── Main.py
├── Requirements.txt
├── CreateProjectZip.py
├── .gitignore
├── README.md
├── manual/
│   ├── chapters/
│   ├── images/
│   ├── scripts/
│   └── .gitkeep
├── src/
│   ├── data/
│   │   ├── loader.py
│   │   ├── preprocess.py
│   │   └── __init__.py
│   ├── models/
│   │   ├── baseline.py
│   │   ├── proposed.py
│   │   └── __init__.py
│   └── utils/
│       ├── metrics.py
│       ├── logger.py
│       └── __init__.py
```

```yaml
# Configs/Config.yaml (excerpt)
random_seed: 42
data:
  dataset_name: mri-multisite
  split: [0.7, 0.15, 0.15]
model:
  name: fedtopo
  hidden_dim: 256
training:
  epochs: 100
  batch_size: 16
  lr: 0.0001
```

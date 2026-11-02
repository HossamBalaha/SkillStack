---
name: maestro
description: Top-level orchestrator for the SkillStack 168-skill composable toolkit. When a task arrives, classify it into one of 9 themes (academic-research, style-integrity, ml-engineering, data-engineering, visualization, writing-citation, ai-text, ai-output-judgement, project-tooling) and point the agent at the correct skill folder and skill name. Themes are non-numbered so any can be dropped, swapped, or renamed without renumbering — removing a theme never breaks routing for the others. Use this FIRST whenever the agent needs to find a skill, before loading any individual skill.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  role: orchestrator
  skill_count: 168
  theme_count: 9
  repo_name: SkillStack
tags: [orchestrator, routing, classification, themes, skillstack]
related: []
prerequisites: []
outputs: [markdown]
difficulty: beginner
estimated_tokens: 1500
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: false
language: ar
---

# Maestro — منسّق المهارات

## الغرض

هذه المهارة هي البوابة الأمامية لمكتبة قابلة للتكوين مؤلفة من 168 مهارة منظّمة في 9 مجلدات موضوعات مستقلّة. الموضوعات وحدات مستقلّة — يمكنك حذف أو استبدال أو إعادة تسمية أيٍّ منها ولا يزال باقي المجموع يعمل. عندما تتلقّى مهمّة، لا تخمّن أيّ مهارة تُحمَّل، بل:

1. اقرأ وصف المهمّة.
2. طابقه مع **واحد** من الموضوعات التسعة أدناه.
3. داخل مجلد ذلك الموضوع، ابحث عن المهارة التي يناسب اسمها ووصفها المهمّة.
4. حمِّل `SKILL.md` الخاصّة بها واتّبعها.

## تخطيط المستودع

```
skillstack/
├── maestro/SKILL.md                          ← أنت هنا
├── README.md                                 ← الفهرس الرئيسي (كلّ المهارات الـ 168)
├── academic-research/    (20 مهارة)          ← تخطيط البحث والكتابة
├── style-integrity/      (18 مهارة)          ← LaTeX والنص وقواعد البرمجة
├── ml-engineering/        (22 مهارة)         ← PyTorch والتدريب والتحقّق
├── data-engineering/      (18 مهارة)         ← ETL والمخطّطات والنسب
├── visualization/         (18 مهارة)         ← الأشكال وTikZ والملصقات
├── writing-citation/      (18 مهارة)         ← BibTeX والاستشهادات والتحرير
├── ai-text/               (15 مهارة)         ← كشف النصّ الآليّ وتأنيسه
├── ai-output-judgement/   (18 مهارة)         ← تقييم مخرجات الذكاء الاصطناعيّ والتحقّق منها
└── project-tooling/       (20 مهارة)         ← التغليف وDocker والتكامل المستمرّ
```

كلّ مجلد موضوع فرعيّ يحتوي على مجلّد واحد لكلّ مهارة، وكلّ مجلد مهارة يحوي `SKILL.md` (وبعضها يحوي مجلد `references/` فرعيّاً بقواعد أعمق).

## جدول توجيه الموضوعات

| مجلد الموضوع | يُستخدم عندما تتضمّن المهمّة... | # المهارات |
|---|---|---|
| `academic-research/` | تخطيط دراسة، صياغة مسوّدة مخطوطة، كتابة أطروحة، تصميم منح، مراجعة ورقة، تجهيز محاضرة | 20 |
| `style-integrity/` | فرض قواعد LaTeX/النص/البرمجة، فحوصات عدم الاختلاق، اتّساق الرموز، تنفيذ أيّ مهمّة متعدّدة الخطوات بانضباط | 18 |
| `ml-engineering/` | بناء أو تدريب أو ضبط أو تفسير أو التحقّق من نماذج التعلّم الآليّ في PyTorch/Lightning/HuggingFace | 22 |
| `data-engineering/` | ETL وجودة البيانات وفرض المخطّطات ومخازن الخصائص وبطاقات مجموعات البيانات والمحوّلات | 18 |
| `visualization/` | أشكال النشر ومخطّطات TikZ والملصقات والجداول ولوحات القيادة والرسوم البيانيّة | 18 |
| `writing-citation/` | BibTeX والاستشهادات والملخّصات وIMRaD والمنهجيّة وتحرير الإنجليزيّة وإعادة الصياغة | 18 |
| `ai-text/` | كشف النصّ المُولَّد بالذكاء الاصطناعيّ، تأنيس النصّ الآليّ، التحيّز/الانفجاريّة، كشف العلامات المائيّة | 15 |
| `ai-output-judgement/` | تقييم مخرجات الذكاء الاصطناعيّ للواقعيّة والهلعلة والتحيّز والسلامة والتأريض والإخلاص والمحاذاة وصحّة الكود، بناء هياكل التقييم | 18 |
| `project-tooling/` | التغليف وDocker والتكامل المستمرّ وpytest والتوثيق وREADMEs وpyproject.toml وMakefiles | 20 |

## كيفيّة التوجيه

### الخطوة 1 — تصنيف المهمّة

اقرأ طلب المستخدم واختر موضوعاً أساسيّاً واحداً فقط. إذا امتدّت المهمّة عبر موضوعين (مثلاً «اكتب ورقة وأنتِج أشكالها»)، وجِّه إلى الموضوع **الأساسي** أوّلاً ثمّ تسلسل إلى الثاني.

### الخطوة 2 — اختيار المهارة

داخل مجلد الموضوع، امسح أسماء المهارات. كلّ `SKILL.md` يبدأ بحقل `description` في YAML يوضّح متى يُستخدم. طابق المهمّة مع أقرب وصف.

### الخطوة 3 — التحميل والاتّباع

افتح `SKILL.md` المختار، اقرأه كاملاً، واتّبع سير عمله. إذا أحال إلى ملفّ فرعيّ في `references/`، فاقرأه أيضاً قبل التصرّف.

### الخطوة 4 — التسلسل عند الحاجة

إذا تسلسلت المهمّة طبيعيّاً (مثلاً `research-ideation-planner` ← `research-repo-builder` ← `modular-ml-architect`)، فأكمل مخرجات المهارة الأولى قبل تحميل التالية.

## أمثلة شائعة على التوجيه

| يقول المستخدم | الموضوع | المهارة |
|---|---|---|
| "اقترح 3 أفكار بحثيّة لمجلّة تصوير طبيّ" | academic-research | research-ideation-planner |
| "أنشئ مستودع بحثيّاً بـ src/ وconfigs ودليل" | academic-research | research-repo-builder |
| "صُغ قسم المنهجيّة بـ LaTeX" | academic-research | journal-manuscript-writer |
| "افرض مسافة بادئة بمقدار 2 فراغ وCamelCase وتعليقات منتهيّة بنقطة في Python" | style-integrity | coding-conventions-enforcer |
| "افحص LaTeX بحثاً عن فواصل `% ====== %` مفقودة" | style-integrity | latex-style-guard |
| "تحقّق من أنّ كلّ DOI في المراجع حقيقيّ" | style-integrity | zero-fabrication-guard |
| "شغّل حلقة تدريب متعدّدة البذور مع `.to(device)` على كلّ nn.Module" | ml-engineering | reproducible-experiment-runner |
| "بحث بايزيّ للضبط الفائق بـ Optuna TPE" | ml-engineering | hyperparameter-tuner |
| "أنشئ ملخّص SHAP + رسوم الاعتماديّة" | ml-engineering | model-explainer |
| "ابنِ ETL بتحويلات غير مُتماثلة ومسار تدقيق" | data-engineering | etl-pipeline-builder |
| "تحقّق من CSV مقابل مخطّط pandera" | data-engineering | data-quality-validator |
| "اصنع شكل matplotlib بدقّة 300 DPI جاهز للنشر" | visualization | publication-figure-maker |
| "ارسم مخطّط TikZ لخطّ أنابيب بخطوط تجميع صلبة" | visualization | tikz-framework-diagrammer |
| "حوّل .bib إلى نمط استشهاد IEEE" | writing-citation | citation-style-converter |
| "تأكّد أنّ كلّ bibitem مُستشهَد به مرة على الأقلّ" | writing-citation | bibtex-citation-manager |
| "اكشف إن كان هذا المقال مُولَّداً بالذكاء الاصطناعيّ" | ai-text | ai-text-detector |
| "أنسِن هذا النصّ الآليّ مع الحفاظ على كلّ الحقائق" | ai-text | ai-text-humanizer |
| "تحقّق إن كانت استجابة LLM تتضمّن حقائق مُهلْولة" | ai-output-judgement | hallucination-detector |
| "تحقّق من الادّعاءات الواقعيّة في فقرة مُولَّدة بالذكاء الاصطناعيّ" | ai-output-judgement | factuality-checker |
| "تحقّق إن كان مخرج RAG مُؤرَّضاً في المستندات المسترجعة" | ai-output-judgement | groundedness-verifier |
| "دقّق مخرجات LLM بحثاً عن تحيّز الجنس/العرق" | ai-output-judgement | bias-auditor |
| "ابنِ هيكل تقييم LLM مع MMLU + GSM8K" | ai-output-judgement | evaluation-harness-builder |
| "استخدم LLM-as-judge لتقييم استجابات روبوت المحادثة" | ai-output-judgement | llm-as-judge-evaluator |
| "اكشف حقن الأوامر في صفحة ويب مسترجعة" | ai-output-judgement | prompt-injection-detector |
| "تحقّق من أنّ كود Python المُولَّد بالذكاء الاصطناعيّ يعمل ويمرّر الاختبارات" | ai-output-judgement | code-output-validator |
| "احزم مستودعي في ملفّ zip مع استبعاد results/ و .git/" | project-tooling | project-zip-packager |
| "اكتب Dockerfile لبحث قابل للتكرار" | project-tooling | docker-research-container |
| "ولِّد README.md لحزمتي Python" | project-tooling | readme-generator |

## مهارة قواعد البرمجة (ملاحظة خاصّة)

يفرض مستودع المستخدم نمط Python صارماً وغير قياسيّ. كلّما كتبت أو حرّرت كود Python في هذا المستودع، حمّل `style-integrity/coding-conventions-enforcer/SKILL.md` أوّلاً. القواعد الخمس:

1. **المتغيّرات** تستخدم `camelCase` (مثل `dataSourceUrl`).
2. **الدوالّ والأصناف وأسماء الملفّات ومفاتيح القواميس** تستخدم `CamelCase` (مثل `ProcessData`، `DataProcessor`، `VisualizationUtils.py`، `"ValidationStatus"`).
3. **عبارات `if`** تُحيط الشروط دائماً بأقواس: `if (condition):`.
4. **التعليقات** تأتي فوق كلّ عبارة وتنتهي بنقطة: `# Initialize the data source URL.`.
5. **النصوص** تستخدم علامتي اقتباس مزدوجتين `""` في كلّ مكان ما عدا داخل docstrings.

أسماء الطرق التي يفرضها إطار العمل بأحرف صغيرة (`forward`، `backward`، `training_step`، `validation_step`، `configure_optimizers`، `setUp`، `tearDown`) معفاة.

## حلّ التعارض

إذا بدت مهارتان منطبقتين:
- فضِّل المهارة **الأكثر تخصّصاً**.
- فضِّل المهارة في الموضوع الذي يطابق **المخرج الأساسيّ** للمهمّة (الملفّ أو المنتج النهائيّ الذي يريده المستخدم).
- عند عدم اليقين، اطلب من المستخدم تأكيد أيّ منتج يريد إنتاجه.

## متى لا تستخدم Maestro

- أسئلة وأجوبة بسيطة أو قراءات لملفّ واحد (أجب مباشرة).
- مهامّ مغطّاة بمهارة خارج هذا المستودع (مثل المهارات المدمجة `docx`، `pdf`، `xlsx`، `charts`).
- بحث على الويب فقط دون الحاجة لاستدعاء مهارة.

## تحديث هذا الملفّ

إذا أضفت مهارة جديدة إلى أيّ موضوع، حدِّث عدّاد ذلك الموضوع في جدول التوجيه أعلاه وفي `README.md`. أبقِ الملفّين متزامنين.

الموضوعات غير مرقّمة عمداً — يمكنك حذف أو إعادة تسمية أيّ مجلد موضوع دون إعادة ترقيم الباقي. الـ maestro يوجِّه حسب اسم المجلد، لا حسب الترتيب.

---
name: ai-text-humanizer
description: Rewrite AI-sounding text to restore natural voice and burstiness while preserving every fact, citation, date, name, and number verbatim. Use when a passage reads as machine-generated and needs to read as a human wrote it, or when an `ai-text-detector` verdict triggers a rewrite.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: ai-text
  language: ar
---

# مُأنسِن نصّ الذكاء الاصطناعيّ

## متى تستخدم
- أعاد تشغيل `ai-text-detector` نتيجة `Likely AI` أو `Near-Certain AI`.
- يقول المستخدم "هذا يبدو كـ ChatGPT، هل يمكنك إصلاحه؟" أو "اجعل هذا يبدو بشريّاً".
- يجب أن تمرّ مسوّدة عبر محرّر أو مراجع يرفض النصّ الآليّ الواضح.
- أنت تحوّل مخرجات روبوت محادثة إلى نثر قابل للنشر.
- تريد التأنيس دون اختلاق أو فقدان أيّ محتوى واقعيّ.

## سير العمل
1. مرِّر المُدخلات عبر `ai-text-detector` للحصول على جدول الأدلّة.
2. جمّع العلامات المُكتشَفة حسب الفئة: تنسيقيّة، إيقاع-بالقاعدة، تضخّم، تنسيق-بالقاعدة، بقايا.
3. لكلّ مجموعة، طبِّق المهارة المتخصّصة المطابقة:
   - علامات التنسيقيّة ← `staging-tell-remover`
   - علامات التضخّم ← `inflation-stripper`
   - علامات الإيقاع ← `rhythm-by-rule-fixer`
   - علامات التنسيق ← `formatting-by-rule-cleaner`
   - البقايا المحادثيّة ← `chatbot-residue-cleaner`
4. احفظ حرفيّاً: كلّ اسم وتاريخ ورقم وإحصاء واستشهاد وDOI وURL ومقطع مقتبس.
5. استعد الانفجاريّة: نوّع طول الجمل، كسر الإيقاع الموحّد، اسمح بجملة قصيرة ثمّ طويلة.
6. نوّع بدايات الجمل فلا جملتان متتاليتان تبدآن بنفس الكلمة أو البنية.
7. إذا كان ملف تعريف صوت هدف موجوداً، استدعِ `voice-profile-matcher` ودع صوت المؤلّف يتجاوز القواعد العامّة.
8. لأيّ ادّعاء واقعيّ لا يمكن التحقّق منه من المواد المصدر، استدعِ `grace-degradation-protocol`: احذف بصمت أو أدخل `[Verify Source]`. لا تختلق أبداً.
9. أعد تشغيل `ai-text-detector` على المخرجات المُعاد كتابتها. استهدف `Likely Human` أو `Mixed`.
10. إذا لم يزل مُعلَّماً، كرّر مرة واحدة. لا تتنافس حلقة لا نهائيّة — عوائد متناقصة وخطر الإفراط في التوافق.
11. أنتج ملخّص اختلاف يسرد كلّ علامة أُزيلت وزوج قبل/بعد وأيّ حذف مُسجَّل.

## المُدخلات
- النصّ الآليّ المُراد إعادة كتابته (فقرة، قسم، أو مستند كامل).
- اختياريّ: مواد مصدر أصليّة حتّى يمكن التحقّق من الحقائق وعدم اختلاقها.
- اختياريّ: ملف تعريف صوت الهدف (عيّنة كتابة من المؤلّف المطلوب).
- اختياريّ: أدلّة الكشف من `ai-text-detector` (يوفر إعادة تشغيل).

## المُخرجات
- النصّ المُعاد كتابته بنثر عاديّ.
- اختلاف قبل/بعد يبرز كلّ تغيير.
- سجلّ حذف (إذا تمّ تشغيل `grace-degradation-protocol`)، مُلحَق منفصلاً عن المخرج الرئيسيّ.
- درجة كشف ما بعد إعادة الكتابة تُظهر الحُكم الجديد.

## القواعد الأساسية
- احفظ الحقائق حرفيّاً. الأرقام والتواريخ والأسماء والاستشهادات وDOI والسلاسل المقتبسة يجب أن تنجو من إعادة الكتابة بايت-ببايت.
- لا تختلق استشهاداً أو اسماً أو تاريخاً أو إحصاءً أو اقتباساً. إن لم تستطع التحقّق، احذف أو وضع علامة `[Verify Source]`.
- الصوت يتجاوز القواعد. إذا كان المؤلّف الهدف يستخدم عادة شرطة م-em فعلاً، أبقِها.
- لا تُصدِر تعليقات وصفيّة (`[DECLARATION: ...]`، `[REWRITTEN]`، إلخ.) داخل متن النثر.
- لا تكرّر إعادة الكتابة أكثر من مرّتين. تحسين 70% أفضل من الهندرة الزائدة.
- استعد الانفجاريّة الطبيعيّة: تجنّب جمل 15-20 كلمة موحّدة.
- أبقِ المعنى ثابتاً. لو لم يستطع القارئ تمييز أيّ نسخة قرأها، فقد فعلتها صحّ.

## أمثلة

**قبل:**
```
It's worth noting that this approach delves into the pivotal role of caching
in the broader landscape of modern web architecture, ultimately leaving an
indelible mark on performance optimization.
```

**بعد:**
```
Caching still matters here. Every repeated query hits the database twice, and on
a busy day that doubles the load on a service we already pay for by the minute.
```

**قبل (بقايا روبوت محادثة + تضخّم):**
```
Great question! The 2023 paper by Chen et al. (DOI: 10.1109/FAKE.2023.99999)
stands as a testament to how seamless integration can reshape the field.
Let me know if you'd like me to expand!
```

**بعد:**
```
Chen et al. (2023, DOI: 10.1109/FAKE.2023.99999) report that integration reduced
latency by 38% in their test cluster.

[Omission Log]
- Original line "stands as a testament to..." was removed: significance claim
  not supported by the cited paper's abstract.
```

## المراجع
- المهارات المرافقة: `ai-text-detector`، `ai-tell-catalogue`، `grace-degradation-protocol`، `voice-profile-matcher`.
- Weber-Wulff, S., et al. (2023). "Testing of detection signals for AI-generated text." *Patterns* 4(7) — أساس خطوة إعادة التحقّق التكراريّة.

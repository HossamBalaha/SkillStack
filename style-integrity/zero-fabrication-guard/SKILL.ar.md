---
name: zero-fabrication-guard
description: Verify every citation, DOI, URL, dataset name, author name, paper title, and numerical claim in a manuscript against authoritative external sources before submission. Use when checking factual integrity, hunting fabricated references, or auditing numerical claims for accuracy.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: style-integrity
  language: ar
---

# حارس عدم الاختلاق

## متى تستخدم
- يطلب المستخدم "التحقّق الواقعيّ" أو "تدقيق المراجع" أو "تدقيق الادّعاءات" في مخطوطة.
- تحتوي مسوّدة على استشهادات أو DOI أو URL أو أسماء مجموعات بيانات أو إحصاءات رقميّة دقّتها غير مؤكّدة.
- غير متأكّد ممّا إذا كان النصّ المُولَّد بالذكاء الاصطناعيّ قد أدخل مصادر مُختلَقة.
- مراجعة سلامة قبل التقديم مطلوبة.

## سير العمل
1. استخرج كلّ قطعة واقعيّة من المخطوطة: أسماء المؤلّفين، عناوين الأوراق، أسماء المجلاّت، السنوات، DOI، URL، أسماء مجموعات البيانات، وكلّ ادّعاء رقميّ.
2. لكلّ DOI، استعلم `https://api.crossref.org/works/{DOI}` وتأكّد أنّ العنوان والمؤلّفين والمجلّة المُعادة تطابق استشهاد المخطوطة.
3. لكلّ استشهاد، ابحث في Google Scholar (أو Semantic Scholar API على `https://api.semanticscholar.org/graph/v1/paper/search`) باستخدام العنوان وأوّل مؤلّف. تأكّد من وجود سجلّ مطابق.
4. لكلّ URL، نفِّذ طلب HTTP HEAD وتأكّد من استجابة 2xx/3xx. سجّل عمليّات إعادة التوجيه.
5. لكلّ اسم مجموعة بيانات، تحقّق عبر السجلّ القانونيّ (مثل `https://registry.identifiers.org/` أو الصفحة الرسميّة لمجموعة البيانات).
6. لكلّ ادّعاء رقميّ («دقّة 94.2%»)، حدِّد المصدر الأصليّ وتأكّد أنّ الرقم والمقياس والإعداد التجريبيّ تتطابق.
7. طبّق بروتوكول الحذف الصامت لأيّ ادّعاء لا يمكن التحقّق منه: احذف الادّعاء بصمت من المتن (لا تُصدِر نصّ `[DECLARATION: ...]`)، وألحق "ملاحظة تخطيط" في نهاية المُسلَّمة تسرد ما حُذف وما البيانات اللازمة للتحقّق.
8. استخدم مصادر حقيقيّة قابل للتحقّق فقط. لا تخترع DOI أو URL أو مؤلّفاً لـ"سدّ" فجوة.
9. أنتج تقرير تحقّق: العناصر المُتحقَّق منها، العناصر غير المتطابقة، والعناصر المحذوفة بصمت.

## المُدخلات
- نصّ المخطوطة مع الاستشهادات المضمّنة والقائمة المرجعيّة.
- ملفّ `.bib` اختياريّ للتقاطع.
- الوصول إلى متصفّح أو `curl`/`httpx` للفحوصات الحيّة.

## المُخرجات
- جدول تحقّق: الادّعاء، نوع المصدر، URL المصدر، حالة التطابق.
- مخطوطة معدّلة مع حذف الادّعاءات غير القابلة للتحقّق بصمت.
- ملاحظة تخطيط مُلحَقة في النهاية تسرد العناصر المحذوفة والتحقّقات المطلوبة.

## القواعد الأساسية
- كلّ DOI وURL واستشهاد واسم مجموعة بيانات ومؤلّف وادّعاء رقميّ يجب التحقّق منه مقابل مصدر خارجيّ حقيقيّ.
- الادّعاءات غير القابلة للتحقّق تُحذف بصمت من المتن — لا علامات `[DECLARATION: ...]`.
- "ملاحظة تخطيط" في النهاية تسرد ما حُذف وما يجب على المستخدم توفيره.
- استخدم مصادر حقيقيّة قابلة للتحقّق فقط. لا تختلق مرجعاً لسدّ فجوة.
- سجّل API أو URL المُستعلم عنه لكلّ تحقّق ليكون التدقيق قابلاً للتكرار.
- تُفحص أسماء المؤلّفين بترتيب العرض مقابل السجلّ الرسميّ للناشر.
- يجب أن تتطابق الادّعاءات الرقميّة في المقياس والقيمة والوحدة والإعداد التجريبيّ.

## أمثلة

قبل (المتن):
```
Recent work shows an accuracy of 97.4% on ImageNet [Smith et al. 2024,
doi:10.1000/fake123].
```

بعد (المتن):
```
Recent work reports strong accuracy on ImageNet [verified reference].
```

ملاحظة التخطيط (مُلحَقة):
```
Planning Note:
- Omitted claim: "accuracy of 97.4%" — DOI 10.1000/fake123 returned 404
  from Crossref. Provide a corrected DOI or the original paper's Table 3
  values for verification.
```

جدول التحقّق (مقتطف):
```
| Claim                  | Source Type | Source URL                                      | Match |
|------------------------|-------------|--------------------------------------------------|-------|
| accuracy 97.4%         | DOI         | https://api.crossref.org/works/10.1000/fake123   | 404   |
| ImageNet dataset       | Registry    | https://registry.identifiers.org/registry/miriam | Yes   |
| Smith et al. 2024      | Search      | https://api.semanticscholar.org/...              | No    |
```

## المراجع
- Crossref REST API: https://api.crossref.org/works
- Semantic Scholar API: https://api.semanticscholar.org/graph/v1/paper/search
- سجلّ Identifiers.org: https://registry.identifiers.org/
- Google Scholar: https://scholar.google.com

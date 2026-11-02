---
name: latex-style-guard
description: Enforce strict LaTeX typography and structural formatting rules on manuscripts before submission. Use when editing .tex files, reviewing equations, figures, tables, algorithms, or normalizing quote styles and float placements for camera-ready papers.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [latex, typography, manuscript, formatting, camera-ready]
related: [style-integrity/cross-reference-validator, style-integrity/notation-consistency-checker, academic-research/journal-manuscript-writer]
prerequisites: []
outputs: [latex, markdown]
difficulty: advanced
estimated_tokens: 880
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: ar
---

# حارس نمط LaTeX

## متى تستخدم
- يُسلِّم المستخدم ملفّاً `.tex` ويطلب "تنظيف التنسيق" أو "فحص النمط" أو "تجهيز النسخة النهائيّة للنشر".
- تحتوي مخطوطة على سطور فارغة غير متّسقة حول العناصر الطافية والمعادلات أو أوامر الأقسام.
- تظهر علامات اقتباس مزدوجة على شكل `"text"` أو `"text"` بدلاً من نمط LaTeX ``text''.
- يستخدم المتن `\subsubsection{}` بدلاً من العناوين المضمّنة العريضة.
- تفتقر المعادلات أو العناصر الطافية لأسطر التعليقات الفاصلة.

## سير العمل
1. اقرأ ملفّ المصدر `.tex` كاملاً من البداية للنهاية قبل التحرير.
2. تحقّق من وجود سطر فارغ واحد تماماً بعد كلّ أمر `\section{}` و`\subsection{}`.
3. أكِّد وجود سطر فارغ واحد تماماً قبل وبعد كلّ بيئة طافية: `table` و`figure` و`algorithm` وأيّ كتلة `equation`/`align`.
4. أدخل أسطر فاصلة `% ====================== %` على سطر خاصّ بها مباشرةً قبل وبعد كلّ كتلة معادلة أو جدول أو شكل أو خوارزميّة. لا تُضِف فواصل حول أوامر `\section{}`.
5. استبدل كلّ علامات الاقتباس المزدوجة بـ `` `` `` فتح و`''` إغلاق، والمفردة بـ `` ` `` فتح و`'` إغلاق.
6. دقّق استخدام `\textbf{}`: أبقِه فقط للتسلسل الهرميّ الهيكليّ (تأكيد شبيه بالأقسام). احذف التعريض الزخرفيّ من المتن المضمّن.
7. احذف كلّ ظهور لـ `\textit{}`. إذا كان التوكيد ضروريّاً، أعد هيكلة الجملة بدلاً من ذلك.
8. استبدل كلّ `\subsubsection{Title}` بـ `\textbf{Title.}` مُعرض مضمّناً في بداية الفقرة التالية.
9. انقل علامات الترقيم خارج أقواس إغلاق `\ref{}` و`\cite{}`: اكتب `Figure~\ref{fig:x}.` لا `Figure~\ref{fig:x.}`.
10. أعِد تعريف موضع العناصر الطافية الافتراضيّ في المقدّمة:
    ```latex
    \makeatletter
    \renewcommand{\fps@figure}{!htb}
    \renewcommand{\fps@table}{!htb}
    \makeatother
    ```
11. أعد قراءة الملفّ المُرقَّع للتأكّد من اتّساق كلّ القواعد.
12. أبلغ عن عدد كلّ تحويل مطبَّق.

## المُدخلات
- المسار إلى ملفّ أو أكثر `.tex` (مشروع بملفّ واحد أو متعدّد الملفّات عبر `\input{}`/`\include{}`).
- دليل أسلوب المكان المستهدف إن وُجد (يتجاوز الافتراضيّات عند التعارض).
- أيّ وحدات ماكرو موجودة في المقدّمة يرغب المستخدم في الحفاظ عليها.

## المُخرجات
- ملفّ(ات) `.tex` معدّلة مع تطبيق كلّ القواعد.
- جدول ملخّص قصير: اسم القاعدة، عدد الحالات الموجودة، عدد الحالات المُصلَحة.

## القواعد الأساسية
- سطر فارغ واحد تماماً بعد كلّ `\section{}` و`\subsection{}`.
- سطر فارغ واحد تماماً قبل وبعد كلّ بيئة معادلة/عنصر طافٍ.
- فواصل `% ====================== %` تحيط بالمعادلات والجداول والأشكال والخوارزميّات فقط، لا أوامر الأقسام أبداً.
- `` ``text'' `` للاقتباس المزدوج، `` `text' `` للاقتباس المفرد. الاقتباسات المستقيمة محظورة.
- `\textbf{}` محجوز للتسلسل الهرميّ الهيكليّ؛ `\textit{}` محظور كليّاً.
- `\subsubsection{}` محظور. استخدم `\textbf{Inline Heading.}` مضمّناً.
- تقع علامات الترقيم خارج القوس المغلق لـ `\ref{}` و`\cite{}` و`\eqref{}`.
- موضع العناصر الطافية يفترض `[!htb]` عبر إعادة تعريف `\fps@...`، لا تجاوزات لكلّ عنصر.

## أمثلة

قبل:
```latex
\subsection{Method}
We define the loss as:
\begin{equation}
L = (y - \hat{y})^2
\end{equation}
The "standard" approach is shown in Figure~\ref{fig:x.}.
```

بعد:
```latex
\subsection{Method}

We define the loss as:

% ====================== %
\begin{equation}
L = (y - \hat{y})^2
\end{equation}
% ====================== %

The ``standard'' approach is shown in Figure~\ref{fig:x}.
```

## المراجع
- Leslie Lamport، *LaTeX: A Document Preparation System* (الطبعة الثانية).
- TeX FAQ حول موضع العناصر الطافية: https://texfaq.org/FAQ-floats
- دليل مستخدم `amsmath` (AMS) لبيئات المعادلات.

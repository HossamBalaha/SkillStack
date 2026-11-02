---
name: academic-book-author
description: Draft academic book chapters in LaTeX with learning objectives, narrative hooks, progressive disclosure, mandatory code-walkthrough sequences, A-Z numerical examples, chapter summaries, Q&A, exercises, nomenclature glossary, and summary slides via tcolorbox. Use when the user asks to write, outline, or revise a textbook chapter or instructional academic book section.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [latex, textbook, book-chapter, exercises, nomenclature]
related: [academic-research/journal-manuscript-writer, academic-research/thesis-chapter-planner, style-integrity/latex-style-guard]
prerequisites: []
outputs: [latex]
difficulty: advanced
estimated_tokens: 910
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Academic Book Author

## When To Use

- The user asks to write or outline a textbook chapter.
- The user provides learning objectives and wants measurable outcomes.
- The user wants a code walkthrough sequence (pre-code prose, code, output, reflection, figure).
- The user needs a worked numerical example from start to finish.
- Trigger keywords: textbook, chapter, learning objectives, worked example, exercises, nomenclature, tcolorbox.

## Workflow

1. State 3-4 measurable learning objectives at the chapter top using a `tcolorbox`.
2. Open with a narrative hook (concrete scenario, historical anecdote, or motivating problem).
3. Introduce concepts with progressive disclosure: intuition first, formalism second, edge cases last.
4. For every concept defined in an earlier chapter, reference it ("As detailed in Section 2.3...") instead of
   re-explaining.
5. Insert mandatory code-walkthrough blocks in this exact order: pre-code paragraph → `listings`/`minted` snippet →
   output description → reflection paragraph → figure cross-reference.
6. For every concept requiring calculation, produce an A-Z step-by-step numerical example. Label each step.
7. Use 2-space indentation inside code blocks; never use tabs.
8. Close the chapter with: Summary, Key Takeaways (bulleted), Q&A (5-10 items), Exercises (graded difficulty),
   Nomenclature glossary (symbol → meaning).
9. Generate summary slides as a `tcolorbox` per major section.
10. Cross-check that every figure, table, equation, listing has a `\label{}` and is referenced at least once.

## Inputs

- Book title, chapter number, and chapter scope.
- Learning objectives from the book's master list.
- Prior chapters' glossaries and notation (for cross-referencing).
- Code samples and datasets used in examples.
- Target audience (undergraduate, graduate, practitioner).

## Outputs

- `chapterXX.tex` — full chapter source.
- `nomenclature.tex` — chapter-local glossary feeding the book-wide nomenclature.
- `exercises.tex` — exercises with hidden solutions block.
- `slides/chapterXX_slides.tex` — `tcolorbox`-based summary slides.
- `code/listing_XX_YY.py` (or `.m`, `.r`) — referenced code files.

## Key Rules

- Every chapter opens with 3-4 measurable learning objectives inside a `tcolorbox`.
- Code-walkthrough order is fixed: pre-code → code → output → reflection → figure cross-reference.
- Never re-explain a concept defined in an earlier chapter; cross-reference instead.
- Every concept requiring calculation gets an A-Z numerical example with labeled steps.
- Use 2-space indentation in all code blocks; no tabs.
- `listings` or `minted` for code; both are acceptable, but pick one per book.
- Chapter end must contain Summary, Key Takeaways, Q&A, Exercises, Nomenclature.

## Examples

```latex
\begin{tcolorbox}[title=Learning Objectives]
After completing this chapter, you will be able to:
\begin{enumerate}
  \item Derive the gradient of cross-entropy loss with respect to softmax logits.
  \item Implement mini-batch gradient descent in 20 lines of Python.
  \item Diagnose vanishing-gradient symptoms via loss curves.
\end{enumerate}
\end{tcolorbox}
```

```latex
% Code-walkthrough sequence
The following snippet trains a logistic regressor for one epoch. We use
2-space indentation and inline comments sparingly.

\begin{lstlisting}[language=Python]
for epoch in range(1):
  for xb, yb in loader:
    logits = model(xb)
    loss = ce(logits, yb)
    loss.backward()
    opt.step()
    opt.zero_grad()
\end{lstlisting}

The output trace shows a monotonic decrease in training loss from 0.69 to
0.41 over one epoch, consistent with theoretical convex convergence.
Reflecting on this, the smooth decay confirms that the learning rate
($\eta = 10^{-2}$) is well-tuned; larger rates would oscillate.
See Fig.~\ref{fig:loss_curve} for the visualization.
```

## References

- `listings` package: https://ctan.org/pkg/listings
- `minted` package: https://ctan.org/pkg/minted
- `tcolorbox` package: https://ctan.org/pkg/tcolorbox
- Bloom's taxonomy for measurable learning objectives: https://cft.vanderbilt.edu/guides-sub-pages/blooms-taxonomy/

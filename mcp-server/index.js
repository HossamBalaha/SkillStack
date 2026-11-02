#!/usr/bin/env node
// SkillStack MCP Server
// Exposes the SkillStack 168-skill library over the Model Context Protocol (stdio transport).
//
// Tools:
//   - list_skills()                     -> [{theme, name, description, tags, path}, ...]
//   - search_skills(query)              -> matching skills by name / description / tags
//   - get_skill(theme, skill_name?)     -> full SKILL.md content for <theme>/<skill_name>/SKILL.md
//   - route_task(task_description)      -> 1-3 skill suggestions via the maestro keyword router
//
// Author: Hossam Magdy Balaha
// License: MIT

import {Server} from "@modelcontextprotocol/sdk/server/index.js";
import {StdioServerTransport} from "@modelcontextprotocol/sdk/server/stdio.js";
import {CallToolRequestSchema, ListToolsRequestSchema,} from "@modelcontextprotocol/sdk/types.js";
import {glob} from "glob";
import yaml from "js-yaml";
import fs from "node:fs/promises";
import path from "node:path";
import {fileURLToPath} from "node:url";

// ---------------------------------------------------------------------------
// Path setup — skills/ is the parent directory of this script.
// ---------------------------------------------------------------------------
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SKILLS_ROOT = path.resolve(__dirname, "..");

// ---------------------------------------------------------------------------
// Maestro routing table — keyword → theme. Derived from maestro/SKILL.md.
// Used by route_task() to classify the user's task description into a theme
// before picking specific skills.
// ---------------------------------------------------------------------------
const THEME_KEYWORDS = {
  "academic-research": [
    // Output types — the primary signal for this theme.
    "manuscript", "journal", "paper", "thesis", "dissertation", "grant",
    "proposal", "rebuttal", "conference-talk", "talk", "academic-book",
    "book-chapter", "abstract", "methods", "methodology",
    // Phrases that strongly suggest academic-research output.
    "methods section", "methods-section", "draft manuscript", "draft-manuscript",
    "draft section", "draft-section", "draft paper", "draft-paper",
    "manuscript draft", "latex manuscript", "latex paper", "latex section",
    "journal article", "publication-ready",
    // Planning artefacts.
    "research-idea", "ideation", "hypothesis", "experimental-design",
    "rct", "factorial", "research-question", "pico", "finer",
    "scope", "aims", "related-work", "literature-review",
    "systematic-review", "prisma", "citation-network",
    // Process / collaboration.
    "peer-review", "pre-registration", "preregistration", "osf",
    "registered-report", "reproducibility-checklist", "research-portfolio",
    "open-science", "supplementary-materials",
    // Repo scaffolding.
    "scaffold", "research-repo", "research repo", "research repository",
    "scaffold repo", "scaffold research", "repo builder",
  ],
  "style-integrity": [
    // Phrase-style signals — style-integrity is about ENFORCING rules, not
    // drafting content. These phrases distinguish it from academic-research.
    "latex-style", "latex typography", "latex rules", "latex style",
    "enforce latex", "prose polish", "prose",
    "banned-vocabulary", "delve", "tapestry", "leverage", "paramount",
    "zero-fabrication", "verify citation", "verify doi",
    "notation", "nomenclature",
    "coding-convention", "camelcase", "period-ended comment",
    "claim-source", "silent-omission", "planning-note",
    "cross-reference", "label", "ref", "abbreviation",
    "numerical-value", "ineq", "math-symbol",
    "passive-voice", "em-dash", "meta-commentary", "voice-matching",
    "execution-protocol",
  ],
  "ml-engineering": [
    "pytorch", "lightning", "huggingface", "transformer-finetune", "peft",
    "training", "train", "training-loop", "reproducible-experiment",
    "data-leakage", "train-val-test", "statistical-validation", "bootstrap",
    "wilcoxon", "mcnemar", "hyperparameter", "optuna", "tpe", "median-pruner",
    "shap", "lime", "integrated-gradient", "model-explainer", "lightningmodule",
    "datamodule", "callback", "logger", "dataset-adapter", "seed", "device",
    "experiment-folder", "early-stopping", "learning-rate", "lr-range-test",
    "mixed-precision", "amp", "autocast", "gradscaler", "ddp", "torchrun",
    "checkpoint", "inference-pipeline", "fastapi", "baseline", "xgboost",
    "ablation", "cross-validation", "k-fold", "stratified", "grouped",
    "metrics", "accuracy", "f1", "auc", "mcc", "cohen-kappa", "calibration",
  ],
  "data-engineering": [
    "etl", "extract-transform-load", "idempotent", "feature-store",
    "point-in-time", "data-quality", "pandera", "great-expectations",
    "csv", "json", "parquet", "arrow", "dataset-card", "data-schema",
    "pydantic", "dataframeschema", "incremental-loader", "data-anonymizer",
    "pii", "k-anonymity", "time-series-resampler", "impute", "knn-imputer",
    "mice", "outlier", "iqr", "z-score", "isolation-forest", "dbscan",
    "data-drift", "psi", "ks-test", "wasserstein", "feature-engineering",
    "polynomial", "binning", "target-encoding", "categorical-encoder",
    "one-hot", "ordinal", "embedding", "text-preprocess", "tokenize",
    "lemmatize", "stopword", "image-dataset", "augmentation", "tabular",
    "reservoir-sampling", "data-lineage", "provenance",
  ],
  "visualization": [
    "publication-figure", "matplotlib", "matplotlib figure", "seaborn", "vector",
    "300dpi", "300 dpi", "journal-ready figure", "journal-ready",
    "academic-plotting", "tikz", "tikz-diagram", "tikz pipeline",
    "scientific-poster", "a0-poster", "imrad-layout", "booktabs",
    "multi-row", "results-table", "infographic", "confusion-matrix",
    "roc", "pr-curve", "auc", "training-curve", "attention-map",
    "transformer-attention", "embedding", "pca", "tsne", "umap",
    "embedding-projector", "dashboard", "streamlit", "dash", "gradio",
    "interactive-plot", "plotly", "bokeh", "holoviews", "color-palette",
    "viridis", "cividis", "colorbrewer", "colorblind", "figure-caption",
    "multi-panel", "subplot", "shared-axes", "surface-plot", "3d-plot",
    "colorbar", "network-graph", "layout-algorithm",
  ],
  "writing-citation": [
    "bibtex", "bibitem", "citekey", "structured-abstract", "imrad",
    "imrad-thesis", "methodology", "research-methodology", "sample-size",
    "ethics", "english-academic-editor", "non-native-english", "article",
    "tense", "hedging", "plagiarism", "paraphrase", "zotero",
    "better-bibtex", "citation-style", "ieee", "apa", "chicago",
    "vancouver", "mla", "doi-verifier", "crossref", "reference-list",
    "annotated-bibliography", "literature-matrix", "outline-to-prose",
    "paragraph-transition", "tense-consistency", "cohesive-device",
    "reading-level", "flesch-kincaid",
  ],
  "ai-text": [
    "ai-text-detect", "ai-detector", "ai-tell", "ai-humanize",
    "humanize", "umanization", "perplexity", "burstiness", "ai-watermark",
    "watermark-detect", "citation-hallucination", "staging-tell",
    "voice-profile", "inflation", "rhythm", "formatting-by-rule",
    "chatbot-residue", "severity-classifier", "ai-tell-catalogue",
    "multi-engine-verification",
    // Detection phrasing — when the user wants to know if text was AI-written.
    "detect ai", "detect ai-generated", "ai-generated essay",
    "ai-generated text", "ai-generated article", "essay ai",
    "is this ai", "written by ai", "written by llm", "essay",
  ],
  "ai-output-judgement": [
    "hallucination", "hallucinated", "factuality", "factual-claim",
    "faithfulness", "faithfulness-scorer", "bias", "bias-audit",
    "safety-classifier", "alignment", "alignment-evaluator",
    "prompt-injection", "llm-as-judge", "judge-evaluator",
    "groundedness", "groundedness-verifier", "pii-leak", "consistency",
    "coherence", "fluency", "numeric-accuracy", "code-output-validator",
    "eval-harness", "mmlu", "gsm8k", "response-quality", "relevance",
    "reference-accuracy",
    // Verification phrasing — when the user wants to verify LLM output.
    "verify claim", "verify claims", "verify fact", "verify facts",
    "factual claim", "factual claims", "fact check", "fact-check",
    "verify factual",
    // RAG / grounding phrasing.
    "rag output", "rag grounded", "rag grounding", "grounded in retrieved",
    "retrieved docs", "retrieval grounded",
    // Prompt-injection phrasing.
    "detect prompt injection", "detect injection", "injection attack",
    // Generic LLM-output judgement phrasing.
    "llm output", "llm response", "ai output", "ai-output",
    "ai-generated paragraph", "ai-generated response", "ai-generated claim",
    "judge llm", "score llm", "evaluate llm",
  ],
  "project-tooling": [
    "gitignore", "makefile", "code-of-conduct", "readme", "readme-generator",
    "requirements", "requirements-pinner", "pre-commit", "release-notes",
    "changelog", "environment-yaml", "pytest", "license-selector",
    "sphinx-docs", "issue-template", "pr-template", "jupyter-to-script",
    "github-actions", "ci", "contribution-guide", "project-zip",
    "dockerfile", "docker-research-container", "pyproject.toml",
    "pyproject",
    // Repo packaging / zipping.
    "bundle repo", "bundle my repo", "zip repo", "project zip",
    "package repo", "zip", "tarball", "archive repo",
  ],
};

// The 9 theme folders — order matters for stable output.
const THEMES = [
  "academic-research",
  "style-integrity",
  "ml-engineering",
  "data-engineering",
  "visualization",
  "writing-citation",
  "ai-text",
  "ai-output-judgement",
  "project-tooling",
];

// ---------------------------------------------------------------------------
// Frontmatter parsing — tolerant of malformed YAML.
// ---------------------------------------------------------------------------
const STOPWORDS = new Set([
  "the", "a", "an", "and", "or", "but", "if", "then", "when", "use", "to",
  "for", "with", "by", "of", "in", "on", "this", "that", "is", "are", "be",
  "as", "at", "it", "you", "your", "we", "our", "they", "their", "from",
  "into", "out", "up", "down", "over", "under", "not", "no", "so", "than",
  "too", "very", "can", "will", "just", "should", "now", "any", "all",
  "has", "had", "have", "was", "were", "been", "being", "do", "does", "did",
  "such", "about", "above", "after", "before", "between", "during",
  "through", "while", "where", "which", "who", "whom", "what", "how",
  "why", "whether", "also", "more", "most", "some", "each", "other",
]);

function tokenize(text) {
  if (!text) return [];
  return text
    .toLowerCase()
    .split(/[^a-z0-9+-]+/)
    .filter((t) => t.length > 0);
}

function extractKeywordsFromDescription(description, maxTags = 5) {
  const tokens = tokenize(description);
  const counts = new Map();
  for (const token of tokens) {
    if (token.length <= 3) continue;
    if (STOPWORDS.has(token)) continue;
    counts.set(token, (counts.get(token) || 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, maxTags)
    .map(([word]) => word);
}

function parseTagsField(raw) {
  if (Array.isArray(raw)) {
    return raw.map((t) => String(t).trim()).filter((t) => t.length > 0);
  }
  if (typeof raw !== "string") return [];
  let s = raw.trim();
  // Tolerate malformed entries like "umanization, rewriting, voice, ai-text]"
  // (missing opening "[") by stripping a stray trailing "]".
  if (s.startsWith("[")) s = s.slice(1);
  if (s.endsWith("]")) s = s.slice(0, -1);
  return s
    .split(",")
    .map((t) => t.trim())
    .filter((t) => t.length > 0);
}

function extractFrontmatter(content) {
  // Frontmatter is delimited by leading "---" on its own line.
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!match) return {frontmatter: null, body: content};
  return {frontmatter: match[1], body: content.slice(match[0].length)};
}

function parseSkillFile(filePath, content) {
  const {frontmatter, body} = extractFrontmatter(content);
  let parsed = null;
  if (frontmatter) {
    try {
      parsed = yaml.load(frontmatter);
    } catch {
      // Malformed YAML (e.g., ai-text/ai-text-humanizer/SKILL.md is missing
      // the opening "[" on its tags: field). Fall back to regex extraction.
      parsed = null;
    }
  }

  let name = null;
  let description = null;
  let theme = null;
  let tags = [];

  if (parsed && typeof parsed === "object") {
    name = parsed.name || null;
    description = parsed.description || null;
    theme =
      (parsed.metadata && parsed.metadata.theme) ||
      parsed.theme ||
      null;
    tags = parseTagsField(parsed.tags);
  }

  // Regex fallback for malformed YAML.
  if (frontmatter) {
    if (!name) {
      const m = frontmatter.match(/^name:\s*(.+?)\s*$/m);
      if (m) name = m[1].replace(/^["']|["']$/g, "");
    }
    if (!description) {
      const m = frontmatter.match(/^description:\s*(.+?)\s*$/m);
      if (m) description = m[1].replace(/^["']|["']$/g, "");
    }
    if (!theme) {
      const m = frontmatter.match(/^\s*theme:\s*(.+?)\s*$/m);
      if (m) theme = m[1].replace(/^["']|["']$/g, "");
    }
    if (tags.length === 0) {
      const m = frontmatter.match(/^tags:\s*(.+?)\s*$/m);
      if (m) tags = parseTagsField(m[1]);
    }
  }

  // Infer theme from the parent directory path if still missing.
  const relPath = path.relative(SKILLS_ROOT, filePath);
  const relParts = relPath.split(path.sep);
  if (!theme && relParts.length >= 2) {
    theme = relParts[0];
  }

  // If no explicit tags, derive a few keywords from the description.
  if (tags.length === 0 && description) {
    tags = extractKeywordsFromDescription(description, 5);
  }

  // Infer name from the skill folder if not present in frontmatter.
  if (!name && relParts.length >= 3) {
    name = relParts[relParts.length - 2];
  } else if (!name && relParts.length === 2) {
    name = relParts[0];
  }

  return {
    name: name || path.basename(filePath, ".md"),
    theme: theme || "uncategorized",
    description: description || "",
    tags,
    path: relPath,
    absolutePath: filePath,
    body,
  };
}

// ---------------------------------------------------------------------------
// Skill index — loaded once at startup, exposed via tools.
// ---------------------------------------------------------------------------
let skillIndex = null;

async function loadSkillIndex() {
  if (skillIndex) return skillIndex;
  const pattern = "**/SKILL.md";
  const files = await glob(pattern, {
    cwd: SKILLS_ROOT,
    absolute: true,
    ignore: ["**/node_modules/**", "**/.git/**"],
  });

  const skills = [];
  for (const file of files) {
    // Skip the maestro orchestrator file itself from the listing — it is not
    // a per-theme skill, it is the router. (route_task reads it separately.)
    const relPath = path.relative(SKILLS_ROOT, file);
    if (relPath === path.join("maestro", "SKILL.md")) continue;
    let content;
    try {
      content = await fs.readFile(file, "utf8");
    } catch (err) {
      process.stderr.write(`[skillstack-mcp] skip ${relPath}: ${err.message}\n`);
      continue;
    }
    skills.push(parseSkillFile(file, content));
  }

  // Stable ordering: by theme (in THEMES order), then alphabetical by name.
  skills.sort((a, b) => {
    const ai = THEMES.indexOf(a.theme);
    const bi = THEMES.indexOf(b.theme);
    const aOrder = ai === -1 ? THEMES.length : ai;
    const bOrder = bi === -1 ? THEMES.length : bi;
    if (aOrder !== bOrder) return aOrder - bOrder;
    return a.name.localeCompare(b.name);
  });

  skillIndex = skills;
  return skills;
}

// ---------------------------------------------------------------------------
// Tool implementations
// ---------------------------------------------------------------------------
async function listSkills() {
  const skills = await loadSkillIndex();
  return skills.map((s) => ({
    theme: s.theme,
    name: s.name,
    description: s.description,
    tags: s.tags,
    path: s.path,
  }));
}

async function searchSkills(query) {
  const skills = await loadSkillIndex();
  if (!query || typeof query !== "string" || query.trim().length === 0) {
    return {
      query: query || "",
      matches: [],
      note: "Empty query. Pass a non-empty string to search by name / description / tags.",
    };
  }
  const q = query.toLowerCase().trim();
  const qTokens = new Set(tokenize(q));

  const scored = skills.map((s) => {
    const hayName = (s.name || "").toLowerCase();
    const hayDesc = (s.description || "").toLowerCase();
    const hayTags = (s.tags || []).map((t) => t.toLowerCase());

    let score = 0;
    let reason = [];

    // Exact substring match on name (highest signal).
    if (hayName.includes(q)) {
      score += 100;
      reason.push(`name contains "${q}"`);
    }
    // Substring match on description.
    if (hayDesc.includes(q)) {
      score += 30;
      reason.push(`description contains "${q}"`);
    }
    // Substring match on tags.
    for (const tag of hayTags) {
      if (tag.includes(q)) {
        score += 40;
        reason.push(`tag "${tag}" matches`);
      }
    }
    // Token overlap (handles multi-word queries).
    const nameTokens = new Set(tokenize(hayName));
    const descTokens = new Set(tokenize(hayDesc));
    const tagTokens = new Set(hayTags.flatMap((t) => tokenize(t)));
    for (const token of qTokens) {
      if (nameTokens.has(token)) {
        score += 8;
        reason.push(`name token "${token}"`);
      }
      if (descTokens.has(token)) {
        score += 3;
      }
      if (tagTokens.has(token)) {
        score += 10;
        reason.push(`tag token "${token}"`);
      }
    }
    return {s, score, reason: [...new Set(reason)]};
  });

  const matches = scored
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score)
    .map((x) => ({
      theme: x.s.theme,
      name: x.s.name,
      description: x.s.description,
      tags: x.s.tags,
      path: x.s.path,
      score: x.score,
      matched_on: x.reason,
    }));

  return {query, match_count: matches.length, matches};
}

async function getSkill(theme, skillName) {
  if (!theme || typeof theme !== "string" || theme.trim().length === 0) {
    return {
      error: "Missing 'theme' argument.",
      usage: "get_skill(theme, skill_name?) — theme is required. skill_name is optional for theme-level skills (e.g., LLM/SKILL.md).",
    };
  }

  const themeDir = path.join(SKILLS_ROOT, theme);
  let targetFile;
  if (skillName && skillName.trim().length > 0) {
    targetFile = path.join(themeDir, skillName, "SKILL.md");
  } else {
    targetFile = path.join(themeDir, "SKILL.md");
  }

  let content;
  try {
    content = await fs.readFile(targetFile, "utf8");
  } catch (err) {
    return {
      error: `Could not read SKILL.md at ${path.relative(SKILLS_ROOT, targetFile)}.`,
      reason: err.code === "ENOENT" ? "File does not exist." : err.message,
      hint: "Use list_skills to see all available (theme, skill_name) pairs.",
    };
  }

  return {
    theme,
    skill_name: skillName || null,
    path: path.relative(SKILLS_ROOT, targetFile),
    content,
  };
}

async function routeTask(taskDescription) {
  if (
    !taskDescription ||
    typeof taskDescription !== "string" ||
    taskDescription.trim().length === 0
  ) {
    return {
      error: "Missing 'task_description' argument.",
      usage: "route_task(task_description) — pass the user's natural-language task.",
    };
  }

  const text = taskDescription.toLowerCase();
  const taskTokens = new Set(tokenize(text));

  // Score each theme by counting keyword hits. Two passes per theme:
  //   Pass 1 — contiguous phrase match (text.includes(keyword)).
  //            Multi-word phrases (containing space or hyphen) score 5
  //            because they are high-signal. Single-word keywords score 2.
  //   Pass 2 — token subset match (every keyword token is present in the
  //            task). Each UNIQUE task token matched contributes +1, so a
  //            theme that just has many keywords containing the same
  //            ambiguous token (e.g., "latex") cannot inflate its score
  //            by repeating that token across many keyword entries.
  const themeScores = THEMES.map((theme) => {
    const keywords = THEME_KEYWORDS[theme] || [];
    let score = 0;
    const phraseHits = [];
    const matchedTokens = new Set();

    // Pass 1: contiguous phrase match.
    for (const kw of keywords) {
      const kwLower = kw.toLowerCase();
      if (text.includes(kwLower)) {
        const isPhrase = kw.includes("-") || kw.includes(" ");
        score += isPhrase ? 5 : 2;
        phraseHits.push(kw);
      }
    }
    const phraseHitSet = new Set(phraseHits);

    // Pass 2: token subset match (skip keywords already matched as phrases).
    for (const kw of keywords) {
      if (phraseHitSet.has(kw)) continue;
      const kwTokens = tokenize(kw);
      if (kwTokens.length === 0) continue;
      // Subset match — all keyword tokens must be present in the task.
      if (kwTokens.every((t) => taskTokens.has(t))) {
        for (const t of kwTokens) matchedTokens.add(t);
      }
    }
    score += matchedTokens.size;

    const hits = [...phraseHits];
    for (const t of matchedTokens) hits.push("token:" + t);
    return {theme, score, hits};
  });

  const ranked = themeScores
    .filter((t) => t.score > 0)
    .sort((a, b) => b.score - a.score);
  const topTheme = ranked.length > 0 ? ranked[0].theme : null;

  if (!topTheme) {
    // No theme matched — surface 3 most-generic fallback skills.
    const skills = await loadSkillIndex();
    const fallback = ["readme-generator", "execution-protocol", "research-repo-builder"]
      .map((name) => skills.find((s) => s.name === name))
      .filter(Boolean);
    return {
      task: taskDescription,
      top_theme: null,
      reason:
        "No theme keyword matched. The task may be outside the SkillStack scope, or you may want to load the maestro orchestrator (maestro/SKILL.md) for full routing.",
      suggestions: fallback.map((s) => ({
        theme: s.theme,
        skill: s.name,
        reason: "Generic fallback skill — usually safe to try.",
      })),
    };
  }

  // Within the top theme, score each skill by token overlap with the task.
  const skills = await loadSkillIndex();
  const themeSkills = skills.filter((s) => s.theme === topTheme);

  const skillScores = themeSkills.map((s) => {
    let score = 0;
    const hits = [];
    const nameTokens = new Set(tokenize(s.name));
    const descTokens = new Set(tokenize(s.description));
    const tagTokens = new Set((s.tags || []).flatMap((t) => tokenize(t)));

    for (const token of taskTokens) {
      if (token.length <= 2) continue;
      if (nameTokens.has(token)) {
        score += 5;
        hits.push(`name:${token}`);
      }
      if (descTokens.has(token)) {
        score += 2;
      }
      if (tagTokens.has(token)) {
        score += 3;
        hits.push(`tag:${token}`);
      }
    }
    // Bonus: direct substring match between task and skill name.
    if (text.includes(s.name.toLowerCase().replace(/-/g, " "))) {
      score += 6;
      hits.push("name-phrase-match");
    } else if (text.includes(s.name.toLowerCase())) {
      score += 4;
      hits.push("name-substring-match");
    }
    return {skill: s, score, hits: [...new Set(hits)]};
  });

  const topSkills = skillScores
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);

  // Fallback if nothing matched by token overlap — just take the first 3
  // skills in the theme, with a note that routing is heuristic.
  let suggestions;
  let note;
  if (topSkills.length === 0) {
    suggestions = themeSkills.slice(0, 3).map((s) => ({
      theme: s.theme,
      skill: s.name,
      description: s.description,
      reason: "Theme matched, but no specific skill name overlapped. Inspect this theme manually.",
    }));
    note =
      `Theme "${topTheme}" matched via keywords [${ranked[0].hits.join(", ")}], ` +
      `but no individual skill name overlapped with the task. Review the listed skills.`;
  } else {
    suggestions = topSkills.map((x) => ({
      theme: x.skill.theme,
      skill: x.skill.name,
      description: x.skill.description,
      reason: x.hits.length > 0 ? `Matched on: ${x.hits.join(", ")}.` : "Highest token overlap.",
    }));
    note =
      `Theme "${topTheme}" matched via keywords [${ranked[0].hits.join(", ")}]. ` +
      `Top ${topSkills.length} skill(s) ranked by token overlap with the task description.`;
  }

  return {
    task: taskDescription,
    top_theme: topTheme,
    theme_hits: ranked[0].hits,
    note,
    suggestions,
  };
}

// ---------------------------------------------------------------------------
// MCP server setup
// ---------------------------------------------------------------------------
const server = new Server(
  {
    name: "skillstack-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  },
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "list_skills",
      description:
        "List every SkillStack skill (168 total across 9 themes). Returns a JSON array with {theme, name, description, tags, path} for each. Use this first to discover what is available before calling get_skill.",
      inputSchema: {
        type: "object",
        properties: {},
        additionalProperties: false,
      },
    },
    {
      name: "search_skills",
      description:
        "Search the SkillStack library by a free-text query. Matches skill names, descriptions, and tags. Returns ranked matches with a score and the fields that triggered the match. Useful when you know roughly what you want (e.g., 'Optuna', 'BibTeX', 'confusion matrix') but not the exact skill name.",
      inputSchema: {
        type: "object",
        properties: {
          query: {
            type: "string",
            description:
              "Free-text search query. Matched against skill name, description, and tags (case-insensitive).",
          },
        },
        required: ["query"],
        additionalProperties: false,
      },
    },
    {
      name: "get_skill",
      description:
        "Return the full SKILL.md content for a specific (theme, skill_name). Pass skill_name=null or omit it to fetch the theme-level SKILL.md (e.g., LLM/SKILL.md, pdf/SKILL.md). The returned 'content' field is the raw markdown body — load it as the active skill and follow its workflow.",
      inputSchema: {
        type: "object",
        properties: {
          theme: {
            type: "string",
            description:
              "Theme folder name (e.g., 'academic-research', 'ml-engineering', 'ai-output-judgement').",
          },
          skill_name: {
            type: "string",
            description:
              "Skill folder name (e.g., 'journal-manuscript-writer'). Omit for theme-level skills like LLM/SKILL.md.",
          },
        },
        required: ["theme"],
        additionalProperties: false,
      },
    },
    {
      name: "route_task",
      description:
        "Given a natural-language task description, suggest 1-3 SkillStack skills to load. Uses the maestro keyword router: classifies the task into one of the 9 themes by keyword overlap, then picks the top skills inside that theme by token overlap with the task. Always returns a 'top_theme' and a 'suggestions' array. This mirrors the maestro/SKILL.md routing table.",
      inputSchema: {
        type: "object",
        properties: {
          task_description: {
            type: "string",
            description:
              "The user's task, e.g., 'Draft a methods section in LaTeX'.",
          },
        },
        required: ["task_description"],
        additionalProperties: false,
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const {name, arguments: args} = request.params;
  let result;
  try {
    switch (name) {
      case "list_skills":
        result = await listSkills();
        break;
      case "search_skills":
        result = await searchSkills(args && args.query);
        break;
      case "get_skill":
        result = await getSkill(args && args.theme, args && args.skill_name);
        break;
      case "route_task":
        result = await routeTask(args && args.task_description);
        break;
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (err) {
    return {
      content: [
        {
          type: "text",
          text: `Error executing tool "${name}": ${err.message}\n${err.stack || ""}`,
        },
      ],
      isError: true,
    };
  }
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(result, null, 2),
      },
    ],
  };
});

// ---------------------------------------------------------------------------
// Boot — stdio transport
// ---------------------------------------------------------------------------
const transport = new StdioServerTransport();
await server.connect(transport);
process.stderr.write(
  `[skillstack-mcp] server running on stdio (skills root: ${SKILLS_ROOT})\n`,
);

---
name: compatible-response
description: Apply to every Codex user-facing response and output from any skill, across all projects. Adapt presentation to the content and maximize information density without losing essential details.
---

# Compatible Response

Apply the following two rules to every user-facing response, including explanations, reports, documentation, progress messages, and output from other skills. This skill controls presentation only; it does not change the requested task, factual standards, tools, or code behavior.

## 1. Adaptive presentation

Select the most useful format for the current content; do not force a single layout onto every answer.

- Use numbered steps for ordered procedures, investigations, learning sequences, and actionable plans.
- Use tables when comparing alternatives or mapping several items across consistent attributes; do not turn simple prose into a table.
- Use file trees for directory structures and code blocks for commands or code.
- Use flowcharts / Mermaid only when branches, dependencies, architecture, or execution flow become meaningfully clearer than in text. Ensure the diagram is valid and relevant; otherwise use a concise call chain.
- Use short prose for simple answers; use headings and sections only when they improve scanning and navigation.
- Mix formats as needed. Keep visual hierarchy clean and avoid decorative formatting.
- In Persian answers, use natural, readable RTL prose where the output renderer supports it. Keep code, commands, identifiers, and paths LTR, preferably as inline code or code blocks. Do not force HTML wrappers or direction attributes that can break Markdown or the target platform.

## 2. Maximum information density

Keep all information needed to understand, verify, or perform the task, using the fewest useful words.

- Answer the request directly. Remove filler, generic introductions, praise, repeated points, obvious background, and unnecessary conclusions.
- Make each sentence carry a distinct fact, action, reason, constraint, or consequence.
- Compress wording, not meaning. Preserve essential technical details, prerequisites, commands, evidence, uncertainty, risks, and exceptions.
- Do not invent a fixed line, word, heading, or bullet limit. A complex topic may need a long but non-repetitive answer; a simple question may need one sentence.
- Avoid explaining self-evident syntax unless it is necessary for understanding or the user requests instruction.
- Avoid narrating the formatting decisions or mentioning this skill unless explicitly asked.

Before sending, check: (a) Is this the clearest structure for this content? (b) Can any words be removed without losing important information?

Respect explicit user-requested formats and higher-priority constraints. When another skill specifies required content, preserve that content while applying these two presentation rules.

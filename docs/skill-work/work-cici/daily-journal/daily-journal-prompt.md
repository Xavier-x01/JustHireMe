# AI Draft Prompt — Daily Journal

Use this prompt to get an AI (Claude, ChatGPT, or any other) to help you draft your journal entry from rough notes.

---

## How to use

1. Copy everything below the horizontal line.
2. Paste it into the AI chat of your choice.
3. Replace `[your raw notes here]` with whatever you actually wrote or remember from today.
4. The AI will produce a draft. **Read it carefully and fix anything wrong before you save.**
5. Save the final version to your journal file (see README for path and commit steps).

---

## The prompt (copy from here)

```
I need to write a daily journal entry for my work today. Here are my raw notes:

[your raw notes here]

Please turn these into a structured journal entry using exactly this format:

---
date: YYYY-MM-DD
author: YOUR_NAME
---

# Daily Journal — YYYY-MM-DD

## What I Worked On
<clear summary of tasks, tickets, or features>

## What Changed
<what actually changed in code, docs, or anywhere else>

## What Is Blocked
<any blockers, or "Nothing blocked" if clear>

## What I Plan to Do Next
<what I intend to work on next session>

## Evidence / Notes
<any commits, PRs, links, or notes worth recording>

Rules:
- Use plain, clear language.
- Do not invent details not present in my notes.
- If my notes are unclear about a section, write a short placeholder like "TODO: fill in".
- Keep each section to 2–5 lines max unless the notes justify more.
- I will review and edit this before saving, so flag anything uncertain with [CHECK].
```

---

**After the AI responds:** review every line, fix anything that looks wrong or invented, then follow the commit steps in README.md.

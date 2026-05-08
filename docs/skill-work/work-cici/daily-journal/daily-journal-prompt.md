# Journal Drafter Prompt

Paste this into any AI chatbot (Claude, Gemini, ChatGPT) to turn your messy notes into a ready-to-review journal entry. No install, no account, no setup beyond the chat window.

---

## How to use

1. Copy the prompt block below.
2. Paste it into your AI chatbot.
3. Replace the two placeholder sections with your actual notes and terminal history.
4. Read the draft. Fix anything wrong or invented. Then save it to your file.
5. **Never commit the draft without reading it first.**

---

## The prompt (copy everything inside the code block)

```
I need to write a daily work journal entry. Here is my input:

--- MESSY NOTES ---
[paste any notes you took during the day — rough is fine, even bullet fragments]

--- TERMINAL HISTORY ---
[paste your recent terminal history, e.g.: history | tail -40
 or just the commands you remember running today]
---

Using only what I gave you above (do not invent anything), fill in this exact template:

---
date: TODAY
author: YOUR_NAME
---

# Daily Journal — TODAY

## What I Worked On
<2–4 lines summarising the tasks, tickets, or features>

## What Changed
<what actually changed in code, docs, config, or anywhere else>

## What Is Blocked
<any blockers, or "Nothing blocked">

## What I Plan to Do Next
<what I intend to work on next session>

## Evidence / Quick Links

| Type | Link or Reference |
|------|------------------|
| PR / branch | <extract any PR or branch URLs from the notes/history, or leave blank> |
| Commit | <extract any commit hashes from the notes/history, or leave blank> |
| Issue / ticket | <extract any issue numbers or ticket IDs, or leave blank> |
| Recording | <any Loom or screenshot links, or leave blank> |
| Notes | <anything else worth saving> |

Rules:
- Write plain, clear sentences.
- If a section has no information, write a one-line placeholder starting with TODO:.
- Mark anything you are unsure about with [CHECK].
- Keep each prose section to 2–5 lines maximum.
- Fill the Evidence table only from URLs, hashes, or IDs present in my input.
```

---

**After you get the draft:** read every line, delete anything invented, fill in any `TODO:` placeholders, then save it to `users/<your-name>/YYYY-MM-DD.md` and follow the commit steps in README.md.

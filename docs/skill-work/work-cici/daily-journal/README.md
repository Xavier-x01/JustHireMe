# Daily Journal — cici-ai Team

One short entry per person per day. GitHub-tracked, beginner-friendly, no special tools required.

---

## Quick Start

```
1. Copy the template to  users/<your-name>/YYYY-MM-DD.md
2. Fill it in (use the AI prompt or the helper script to get a draft)
3. git add → git commit → git push
```

That's it. Details below if you need them.

---

## Where your journal file goes

```
docs/skill-work/work-cici/daily-journal/users/<your-name>/YYYY-MM-DD.md
```

Examples:
```
users/alice/2026-05-08.md
users/bob/2026-05-08.md
```

Use **the same name every day** — it becomes your personal archive. Everyone has their own folder so you never conflict with a teammate's commit.

---

## How to fill it in

The template has **6 sections**. Keep each one short (2–5 lines):

| Section | What to write |
|---------|--------------|
| **What I Worked On** | Tasks or features you touched today |
| **What Changed** | What actually changed — code, docs, config |
| **What Is Blocked** | Blockers. Write "Nothing blocked" if clear. |
| **What I Plan to Do Next** | What you will work on next session |
| **Evidence / Quick Links** | PR, commit, issue, Loom, or any useful link |

Delete any Evidence table rows you don't have links for.

---

## Option A — AI chatbot (no install, works everywhere)

Best for beginners or anyone working without a terminal.

1. Open `daily-journal-prompt.md` in this folder.
2. Copy the prompt block inside it.
3. Paste it into Claude, Gemini, ChatGPT, or any AI chat.
4. Replace `[paste your notes]` with what you remember from today.
5. Also paste your terminal history if you have it (`history | tail -40` on Mac/Linux).
6. The AI returns a draft. **Read every line. Fix anything wrong.**
7. Save the corrected text to `users/<your-name>/YYYY-MM-DD.md`.

---

## Option B — Helper script (Mac / Linux)

Automates the boring parts. Still requires you to review before committing.

```bash
# Run from the repo root
bash docs/skill-work/work-cici/daily-journal/daily-journal-helper.sh
```

What it does:
1. Asks for your name (type it once; same name every day).
2. Creates `users/<your-name>/YYYY-MM-DD.md` from the template.
3. Opens it in your editor (`$EDITOR`, or `nano`, or `vi`).
4. After you save and close, shows you the file location.
5. Asks whether to commit — **it never commits without asking**.
6. Prints the push command — **it never pushes automatically**.

Skip the name prompt by setting your name once:
```bash
export JOURNAL_AUTHOR=alice   # add to ~/.bashrc or ~/.zshrc to make it permanent
```

---

## How to commit and push

Whether you used the AI prompt or the helper, committing is the same two commands:

```bash
git add docs/skill-work/work-cici/daily-journal/users/<your-name>/YYYY-MM-DD.md
git commit -m "journal: YYYY-MM-DD <your-name>"
git push -u origin $(git branch --show-current)
```

Once pushed, your entry is visible to the whole team on GitHub.

---

## How to browse everyone's journals on GitHub

**Fastest way — File Finder:**

1. Go to the repo on GitHub.
2. Press **`t`** on your keyboard.
3. Type `daily-journal/users/` to filter to all journal entries.
4. Type a name or date to narrow further.

**Browse by person:**
Navigate to `docs/skill-work/work-cici/daily-journal/users/` — each subfolder is one person's complete archive, oldest to newest.

**Browse by date across everyone:**
Use GitHub's search: `path:daily-journal/users filename:2026-05-08`

---

## Files in this folder

| File | What it is |
|------|-----------|
| `README.md` | This guide |
| `daily-journal-template.md` | Blank template — copy it, don't edit it directly |
| `daily-journal-prompt.md` | AI chatbot prompt for drafting from notes + terminal history |
| `daily-journal-helper.sh` | Optional shell script (bash, zero dependencies) |
| `users/` | All submitted journals, one subfolder per person |

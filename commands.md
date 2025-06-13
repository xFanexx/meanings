# 🤖 Meanings Bot - Commands Reference

## 📋 Overview
This document provides a comprehensive guide to all commands available for the Meanings Bot. Commands are divided into **Public Commands** (accessible to everyone) and **Admin Commands** (restricted to whitelisted users). All commands use the prefix **`?`**.

---

## 👥 Public Commands (Everyone)

| Command          | Description                          | Usage Example         | Details/Response Example                              |
|------------------|--------------------------------------|-----------------------|-------------------------------------------------------|
| `?meaning [word]` | Shows the meaning of a word/phrase   | `?meaning sybau`      | <ul><li>📖 Meaning: SYBAU</li><li>Shut Your Bitch Ass Up - A rude way to be quiet</li><li>💡 Example: Person A annoys → Person B: 'sybau!'</li><li>🏷️ Category: Slang/Offensive</li></ul> |
| `?list`          | Displays all available words         | `?list`               | <ul><li>Shows words in chunks of 20 per embed</li><li>Paginated for large databases</li><li>Total word count included</li></ul> |
| `?stats`         | Shows bot statistics and information | `?stats`              | <ul><li>📖 Total Words: Number of words in database</li><li>🌐 Servers: Number of servers bot is in</li><li>👥 Users: Total users bot can see</li></ul> |
| `?ping`          | Displays the bot's latency           | `?ping`               | <ul><li>🏓 Pong!</li><li>Latency: **X.XX ms** (e.g., 45.67 ms)</li></ul> |

---

## 🔐 Admin Commands (Whitelisted Users Only)

| Command          | Description                          | Usage Example         | Process/Details                                      |
|------------------|--------------------------------------|-----------------------|------------------------------------------------------|
| `?addmeaning`    | Opens a modal to add a new word      | `?addmeaning`         | <ul><li>Sends a button to open a modal form</li><li>Fields: Word/Phrase (req), Meaning/Definition (req), Example (opt), Category (opt)</li><li>Submit to add word to database</li></ul> |
| `?deletemeaning [word]` | Initiates deletion of a word    | `?deletemeaning sybau` | <ul><li>Shows confirmation embed with current meaning</li><li>Requires `?yes` to confirm or `?no` to cancel</li></ul> |
| `?yes`           | Confirms a pending word deletion     | `?yes`                | <ul><li>Must follow `?deletemeaning` in same channel</li><li>Permanently removes the word</li></ul> |
| `?no`            | Cancels a pending word deletion      | `?no`                 | <ul><li>Must follow `?deletemeaning`</li><li>Keeps word in database</li><li>Clears pending deletion</li></ul> |

---

## 📊 Command Summary

| Command            | Access Level    | Purpose                     |
|---------------------|-----------------|-----------------------------|
| `?meaning [word]`  | Everyone        | Retrieve word definition    |
| `?list`            | Everyone        | View all available words    |
| `?stats`           | Everyone        | Display bot statistics      |
| `?ping`            | Everyone        | Check bot latency           |
| `?addmeaning`      | Whitelisted     | Add new word via modal      |
| `?deletemeaning [word]` | Whitelisted | Initiate word deletion     |
| `?yes`             | Whitelisted     | Confirm word deletion       |
| `?no`              | Whitelisted     | Cancel word deletion        |

---

## 🛡️ Access Control

- **Whitelisted Users:** Only users with their Discord ID in the `WHITELISTED_USERS` list can use admin commands (`?addmeaning`, `?deletemeaning`, `?yes`, `?no`).
- **Error Handling:** All commands include clear error messages and user guidance.
- **Safety Features:**
  - Deletion requires confirmation with `?yes`.
  - Confirmation must occur in the same channel as the deletion request.
  - Displays current meaning before deletion.
  - Provides success/failure feedback.

---

## 💡 Usage Tips

1. **For Users:** Start with `?list` to explore available words, then use `?meaning [word]` for details or `?ping` to check bot responsiveness.
2. **For Admins:** Use the modal popup (`?addmeaning`) for an intuitive experience when adding words.
3. **For Safety:** Always double-check before confirming deletions with `?yes`.

---

## 🎯 Bot Prefix
All commands use the prefix: **`?`**

**Example:** `?meaning` (correct) vs. `meaning` or `/meaning` (incorrect).

---

## 📝 Notes
- Ensure your Discord ID is added to `WHITELISTED_USERS` in `bot.py` to access admin commands.
- Keep your `.env` file secure with your Discord token.
- Report issues or suggest new words to the bot owner for updates.

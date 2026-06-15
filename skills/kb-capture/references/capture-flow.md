# Capture-from-chat flow

Goal: the user is mid-conversation, has some content, and wants it in a vault with minimal friction. Be fast when intent is clear; ask only what you can't infer.

## Detecting the content
- **Uploaded/attached file**: the harness gives you a path (often a temp path). Treat that path as the source; copy it into the chosen `.raw/`.
- **Pasted text**: capture the block the user means. Ask for a title if none is obvious; save as `<Title>.md` (Title Case, capitalised).
- **A path or URL in their message**: use it directly (URL → web source).
- **"Save what we just figured out"**: extract the relevant portion of the conversation (a decision, a spec) into a `.md` — don't dump the whole transcript.

## The questions (use the AskUserQuestion tool; batch them)
Resolve as much as possible from the message first, then ask only the rest. Offer existing options + a create-new option, with a recommended default first.

1. **Vault** — from `kb_init.py list-vaults`. Skip if only one (just confirm) or if the user named it.
2. **Client** — existing `Clients/*` or "+ New client".
3. **Project KB** — existing KBs under that client or "+ New KB".
4. **Folder / type** — where the resulting note lives:
   - `Sources/` (default — general document)
   - `Meetings/` (it's a meeting/transcript → routes to kb-timeline)
   - `Decisions/` (it's a decision → routes to kb-decisions)
   - "+ New folder" → ask for a name; kb-organize creates it.

If the user said e.g. "add this to Acme / Billing as a meeting note", infer all four and skip straight to filing.

## Create-new branches
- New client/KB/folder → call **kb-organize** (which runs `kb_init.py client|kb` or makes the folder), then continue.
- No vault at all → call **kb-setup** first, then resume capture.

## Filing
1. Copy the raw content into `<KB>/.raw/` (the immutable source). For a chosen non-default folder, remember it so the generated note is placed there.
2. Hand to **kb-ingest** for that one source (it processes and delegates to kb-people / kb-decisions / kb-timeline / kb-architecture as warranted, and runs the post-write protocol).

## Confirm
Report: "Added `<file>` to **<Client> / <KB>** under `<folder>` — created `<notes>`." Mention any new client/KB/folder you created. Offer a follow-up (e.g. "want a brief, or to ingest related material?").

## Multiple attachments
If several files are attached, ask the destination **once**, then batch them through kb-ingest (which fans out kb-source-agent).

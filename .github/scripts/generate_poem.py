import os
import re
import json
import requests
from transformers import pipeline, set_seed
from github import Github

# ─── Setup GitHub client ──────────────────────────────────────────────────────
token = os.getenv("MY_GITHUB_TOKEN")
repo = Github(token).get_repo(os.getenv("GITHUB_REPOSITORY"))
with open(os.getenv("GITHUB_EVENT_PATH")) as f:
    event = json.load(f)
pr_number = event["number"]
pr = repo.get_pull(pr_number)

# ─── Build your prompt ────────────────────────────────────────────────────────
# 1) Check PR body for a custom prompt line:
body = pr.body or ""
m = re.search(r"^Poem prompt:\s*(.+)$", body, flags=re.MULTILINE)
if m:
    prompt_text = m.group(1).strip()
else:
    # 2) Fallback to default:
    title = pr.title
    prompt_text = f"Write a short poem about this GitHub pull request titled “{title}”."

# ─── Generate poem with HF transformers ───────────────────────────────────────
generator = pipeline("text-generation", model="gpt2")
set_seed(42)
out = generator(prompt_text, max_length=100, num_return_sequences=1)[0]["generated_text"]

# ─── Post back to the PR ──────────────────────────────────────────────────────
comment = f"📝 **Your PR Poetry:**\n\n> {prompt_text}\n\n```\n{out.strip()}\n```"
pr.create_issue_comment(comment)

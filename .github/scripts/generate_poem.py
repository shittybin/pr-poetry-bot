import os
import json
import requests
import openai
from github import Github

# GitHub setup
g = Github(os.getenv("GITHUB_TOKEN"))
repo_name = os.getenv("GITHUB_REPOSITORY")
event_path = os.getenv("GITHUB_EVENT_PATH")

# Load PR event data
with open(event_path) as f:
    event = json.load(f)
pr_number = event["number"]
repo = g.get_repo(repo_name)
pr = repo.get_pull(pr_number)

# Collect PR info
title = pr.title
diff = requests.get(pr.diff_url).text
short_diff = diff[:500]  # keep it short

# Prepare LLM call
openai.api_key = os.getenv("OPENAI_API_KEY")
prompt = f"""Write a short haiku about this pull request titled:
“{title}”

Code diff:
{short_diff}
"""

# Use ChatCompletion with gpt-3.5-turbo
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=100
)
poem = response.choices[0].message.content.strip()

# Post it back on the PR
pr.create_issue_comment(f"📝 **Your PR Poetry:**\n\n{poem}")

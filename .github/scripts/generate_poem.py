import os
import json
import requests
import openai
from github import Github
from openai import OpenAI
import os

# GitHub setup
token = os.getenv("GITHUB_TOKEN")
g = Github(token)
repo_name = os.getenv("GITHUB_REPOSITORY")
event_path = os.getenv("GITHUB_EVENT_PATH")

# Load PR event data
with open(event_path) as f:
    event = json.load(f)
pr_number = event["number"]
repo = g.get_repo(repo_name)
pr = repo.get_pull(pr_number)

# Collect PR title and diff
title = pr.title
diff_url = pr.diff_url
diff = requests.get(diff_url).text
short_diff = diff[:500]  # Limit size

# Prompt the LLM (OpenAI API Key should be set in the environment)
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = f"""Write a short haiku about the following GitHub pull request:

Title: {title}

Code Diff: {short_diff}
"""

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=100
)
poem = response.choices[0].message.content.strip()

poem = response.choices[0].text.strip()  # Remove extra whitespace

# Comment the poem on the PR
pr.create_issue_comment(f"📝 **Your PR Poetry:**\n\n{poem}")

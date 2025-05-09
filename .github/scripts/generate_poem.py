import os
import json
import requests
import openai
from github import Github

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

# Use the new API method
response = openai.Completion.create(
    model="text-davinci-003",  # or another appropriate model
    prompt=prompt,
    max_tokens=100  # Adjust the token count as needed
)

poem = response.choices[0].text.strip()  # Remove extra whitespace

# Comment the poem on the PR
pr.create_issue_comment(f"📝 **Your PR Poetry:**\n\n{poem}")

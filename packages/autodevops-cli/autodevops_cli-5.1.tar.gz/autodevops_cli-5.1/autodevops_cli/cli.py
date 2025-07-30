import os
import time
import io
import zipfile
import subprocess
import sys
import json
import requests
import click
from tabulate import tabulate
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from collections import defaultdict
from datetime import datetime, timezone
from loguru import logger
from rich.console import Console
from pymongo import MongoClient
import shutil

# --------------------- INIT ---------------------
BASE_DIR = Path(__file__).resolve().parent
REQUIREMENTS_DIR = BASE_DIR

load_dotenv(dotenv_path=BASE_DIR.parent / ".env")

console = Console()
client = OpenAI(api_key="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")

LOG_DIR = BASE_DIR / "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logger.add(
    LOG_DIR / f"autodevops_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", rotation="1 MB"
)

OWNER = "kannanb2745"
REPO = "testing-CI-CD"
BRANCH = "main"
WORKFLOW_FILENAME = "main.yml"
TOKEN = os.getenv('TOKEN')
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

summary_lines = []


def log_summary(line=""):
    summary_lines.append(line)


@click.command()
@click.argument('command_input')
def autodevops(command_input):
    if command_input.lower().startswith("setup "):
        folder_path = Path(command_input[6:].strip()).expanduser().resolve()
        if not folder_path.exists() or not folder_path.is_dir():
            console.print(f"[red]❌ Invalid path: {folder_path}[/red]")
            raise click.Abort()
        run_analysis(folder_path, max_files=500)
    else:
        run_pipeline()


def run_analysis(folder_path, max_files=500):
    console.rule(f"[bold yellow]📂 AutoDevOps Analysis Started: {folder_path}")
    summary = scan_directory_structure(folder_path, max_files)
    structure_analysis = gpt_call(
        "Structure Analysis", "Analyze the folder structure and suggest improvements.", summary)
    save_output("structure_analysis.md", structure_analysis, folder_path)
    tech_stack = gpt_call(
        "Tech Stack", "Detect the tech stack from this project structure.", summary)
    save_output("tech_stack.md", tech_stack, folder_path)
    readme = gpt_call(
        "README.md", "Generate a README.md file for this project.", summary)
    save_output("README.md", readme, folder_path, copy_files=True)
    console.rule(
        "[bold green]🎉 Project analyzed and README generated successfully!")


def scan_directory_structure(folder_path, max_files=500):
    ext_count, folder_count = defaultdict(int), defaultdict(int)
    important_files = []
    for i, path in enumerate(Path(folder_path).rglob("*")):
        if path.is_file():
            if i >= max_files:
                break
            rel_path = path.relative_to(folder_path)
            ext_count[path.suffix or "no_ext"] += 1
            folder_count[str(rel_path.parent)] += 1
            important_files.append(str(rel_path))
    summary = [
        f"Total files scanned: {min(i + 1, max_files)}", "\nFile types count:"
    ] + [f"  {ext}: {count}" for ext, count in sorted(ext_count.items(), key=lambda x: -x[1])]
    summary += ["\nTop folders by file count:"] + [
        f"  {folder}/: {count} files" for folder, count in sorted(folder_count.items(), key=lambda x: -x[1])[:10]]
    summary += ["\nSample files:"] + \
        [f"  {file}" for file in important_files[:25]]
    return summary


def gpt_call(title, instruction, summary_lines):
    prompt = f"""{instruction}
Summarized Project Structure:
{chr(10).join(summary_lines)}
Avoid using triple backticks in code."""
    console.print(f"[yellow]🔹 Generating {title}...[/yellow]")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    content = response.choices[0].message.content.strip()
    console.print(f"[green]✅ Done: {title}[/green]\n")
    return content


def save_output(filename, content, folder_path, copy_files=False):
    path = Path(folder_path) / filename
    path.write_text(content)
    console.log(f"📄 Saved: {filename}")
    if copy_files:
        copy_required_files(folder_path)


def copy_required_files(folder_path):
    current_dir = Path(__file__).resolve().parent
    docker_target = Path("/home/kannan/testing-CI-CD/Docker")
    test_file_target = Path("/home/kannan/testing-CI-CD/test_main.py")
    github_workflow_target = Path(
        "/home/kannan/testing-CI-CD/.github/workflow/main.yml")

    docker_target.mkdir(parents=True, exist_ok=True)
    github_workflow_target.parent.mkdir(parents=True, exist_ok=True)

    def safe_copy(src_file, dest_file, label):
        try:
            shutil.copy(src_file, dest_file)
        except FileNotFoundError:
            pass

    safe_copy(current_dir / "test_main.py", test_file_target, "test_main.py")


def run_pipeline():
    load_dotenv()
    OWNER = "Dinesh-4"
    REPO = "Devops"
    BRANCH = "main"
    WORKFLOW_FILENAME = "main.yml"
    TOKEN = os.getenv('TOKEN')
    MONGO_URI = os.getenv("MONGO_URI")
    HEADERS = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    def trigger_workflow():
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILENAME}/dispatches"
        payload = {"ref": BRANCH}
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code == 204:
            print("✅ Workflow triggered.")
        else:
            print("❌ Trigger failed:", response.text)
            exit(1)

    def get_latest_run_id():
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs"
        while True:
            response = requests.get(url, headers=HEADERS)
            runs = response.json().get("workflow_runs", [])
            if runs:
                return runs[0]["id"]
            time.sleep(3)

    def wait_for_run(run_id):
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}"
        while True:
            response = requests.get(url, headers=HEADERS).json()
            status = response["status"]
            print(f"🔄 Status: {status}")
            if status == "completed":
                return response["conclusion"]
            time.sleep(5)

    def download_and_extract_logs(run_id):
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}/logs"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                z.extractall("logs")
            print("📦 Logs downloaded to 'logs/'")
        else:
            print("❌ Failed to download logs:", response.text)
            exit(1)

    def print_logs():
        for root, dirs, files in os.walk("logs"):
            for file in sorted(files):
                path = os.path.join(root, file)
                print(f"\n📄 === {file.replace('.txt', '')} ===")
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    print(f.read())

    def save_to_mongodb(summary_text, commit_sha, branch, status, author):
        client = MongoClient(MONGO_URI)
        db = client["ci_cd_logs"]
        collection = db["summaries"]
        doc = {
            "summary": summary_text,
            "commit_sha": commit_sha,
            "branch": branch,
            "author": author,
            "status": status,
            "timestamp": datetime.now(timezone.utc)
        }
        result = collection.insert_one(doc)
        print(f"📝 Summary stored in MongoDB with ID: {result.inserted_id}")

    def summarize_run(run_id):
        print("\n📋 Generating summary...")
        run_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}"
        run_info = requests.get(run_url, headers=HEADERS).json()
        commit_sha = run_info["head_sha"]
        actor = run_info["actor"]["login"]
        status = run_info["conclusion"]
        trigger = run_info["event"]
        branch = run_info["head_branch"]
        workflow_name = run_info["name"]
        duration = run_info.get("run_duration_ms", 0) / 1000
        commit_url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits/{commit_sha}"
        commit_data = requests.get(commit_url, headers=HEADERS).json()
        message = commit_data["commit"]["message"]
        steps = []
        for root, dirs, files in os.walk("logs"):
            for file in sorted(files):
                if file.endswith(".txt"):
                    steps.append(file.replace(".txt", ""))
        actions = []
        for step in steps:
            lower = step.lower()
            if "pytest" in lower:
                actions.append("✅ Ran unit tests using Pytest")
            if "docker" in lower and "login" in lower:
                actions.append("🔐 Logged in to Docker Hub")
            if "docker image" in lower or "build docker" in lower:
                actions.append("📦 Built Docker image")
            if "push" in lower:
                actions.append("🚀 Pushed Docker image to Docker Hub")
        summary = f"""✅ CI/CD Pipeline Summary
----------------------------

📦 Commit Info:
- Message       : {message}
- Author        : {actor}
- Commit SHA    : {commit_sha}
- Branch        : {branch}

🧪 Workflow Run: {workflow_name}
- Status        : {'✅ Success' if status == 'success' else '❌ Failed'}
- Triggered by  : {trigger}
- Duration      : {duration:.2f} seconds

📋 Job Steps:
""" + "\n".join([f"{i+1}. {step} ✅" for i, step in enumerate(steps)]) + "\n\n"
        summary += "🛠️ Actions Performed:\n"
        for action in actions:
            summary += f"- {action}\n"
        summary += "\n📄 Logs saved in: ./logs/\n📝 Summary saved in: ./ci_summary.txt\n"
        with open("ci_summary.txt", "w") as f:
            f.write(summary)
        save_to_mongodb(summary, commit_sha, branch, status, actor)
        print(summary)

    trigger_workflow()
    time.sleep(10)
    run_id = get_latest_run_id()
    wait_for_run(run_id)
    download_and_extract_logs(run_id)
    print_logs()
    summarize_run(run_id)


if __name__ == "__main__":
    autodevops()

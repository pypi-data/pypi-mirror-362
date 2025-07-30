import os
import time
import io
import zipfile
import requests
import click
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from collections import defaultdict
from datetime import datetime
from loguru import logger
from rich.console import Console

# --------------------- INIT ---------------------
load_dotenv()
console = Console()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logger.add(
    f"{LOG_DIR}/autodevops_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", rotation="1 MB")

OWNER = "kannanb2745"
REPO = "testing-CI-CD"
BRANCH = "main"
WORKFLOW_FILENAME = "main.yml"
TOKEN = os.getenv('TOKEN')
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}


@click.command()
@click.argument('command_input')
def autodevops(command_input):
    """AutoDevOps CLI: `setup ./path` or commit message for CI/CD"""

    # Handle: setup path/to/folder
    if command_input.lower().startswith("setup "):
        path = command_input[6:].strip()
        folder_path = Path(path).expanduser().resolve()
        if not folder_path.exists() or not folder_path.is_dir():
            console.print(f"[red]❌ Invalid path: {folder_path}[/red]")
            raise click.Abort()
        run_analysis(folder_path, max_files=500)

    # Else treat as commit message
    else:
        run_pipeline(command_input)

# --------------------- AI ANALYSIS ---------------------


def run_analysis(folder_path, max_files=500):
    console.rule(f"[bold yellow]📂 AutoDevOps Analysis Started: {folder_path}")
    summary = scan_directory_structure(folder_path, max_files)
    console.print(
        f"[cyan]📁 Total Files Scanned:[/cyan] {min(len(summary), max_files)}")
    console.print("\n".join(summary[:20]) + "\n...")

    structure_analysis = gpt_call(
        "Structure Analysis", "Analyze the folder structure and suggest improvements.", summary)
    save_output("structure_analysis.md", structure_analysis, folder_path)
    console.rule("[bold blue]📦 STRUCTURE ANALYSIS")
    console.print(structure_analysis)

    tech_stack = gpt_call(
        "Tech Stack", "Detect the tech stack (backend, frontend, tools, DB, testing) from this project structure.", summary)
    save_output("tech_stack.md", tech_stack, folder_path)
    console.rule("[bold green]🛠️ TECH STACK")
    console.print(tech_stack)

    readme = gpt_call(
        "README.md", "Generate a clean, production-ready README.md file for this project.", summary)
    save_output("README.md", readme, folder_path)
    console.rule("[bold cyan]📘 README.md")
    console.print(readme)

    console.rule(
        "[bold green]🎉 Project analyzed and README generated successfully!")


def scan_directory_structure(folder_path, max_files=500):
    ext_count = defaultdict(int)
    folder_count = defaultdict(int)
    important_files = []

    for i, path in enumerate(Path(folder_path).rglob("*")):
        if path.is_file():
            if i >= max_files:
                break
            rel_path = path.relative_to(folder_path)
            ext = path.suffix or "no_ext"
            ext_count[ext] += 1
            folder_count[str(rel_path.parent)] += 1
            important_files.append(str(rel_path))

    summary = [
        f"Total files scanned: {min(i + 1, max_files)}",
        "\nFile types count:"
    ]
    for ext, count in sorted(ext_count.items(), key=lambda x: -x[1]):
        summary.append(f"  {ext}: {count}")

    summary.append("\nTop folders by file count:")
    for folder, count in sorted(folder_count.items(), key=lambda x: -x[1])[:10]:
        summary.append(f"  {folder}/: {count} files")

    summary.append("\nSample files:")
    for file in important_files[:25]:
        summary.append(f"  {file}")

    return summary


def gpt_call(title, instruction, summary_lines):
    prompt = f"""{instruction}

Summarized Project Structure:
{chr(10).join(summary_lines)}

Avoid using triple backticks in code.
"""
    console.print(f"[yellow]🔹 Generating {title}...[/yellow]")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    content = response.choices[0].message.content.strip()
    console.print(f"[green]✅ Done: {title}[/green]\n")
    return content


def save_output(filename, content, folder_path):
    output_path = Path(folder_path) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)
    console.log(f"📄 Saved: {filename}")

# --------------------- PIPELINE ---------------------


def run_pipeline(message):
    console.rule("[bold green]🔧 AutoDevOps Pipeline Started")
    try:
        from sh import git
        with console.status("[green]Performing Git operations...", spinner="dots"):
            console.log("[yellow]Pulling latest code...")
            git.pull()

            console.log("[cyan]Adding changes...")
            git.add(".")

            console.log(f"[magenta]Committing: {message}")
            git.commit("-m", message)

            console.log("[green]Pushing to GitHub...")
            git.push()

        console.rule("[bold blue]🚀 GitHub Actions CI/CD Triggered")
        trigger_workflow()
        time.sleep(10)
        run_id = get_latest_run_id()
        result = wait_for_run(run_id)
        console.log(f"[bold green]✅ Pipeline Result: {result.upper()}")
        download_and_extract_logs(run_id)
        print_logs()
        summarize_run(run_id)
        logger.success("✅ AutoDevOps completed successfully!")

    except Exception as e:
        logger.exception("❌ AutoDevOps failed")
        console.print(f"[red]❌ Error: {e}")
        exit(1)


def trigger_workflow():
    console.log("[green]Triggering GitHub Actions Workflow...")
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILENAME}/dispatches"
    payload = {"ref": BRANCH}
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 204:
        console.log("✅ Workflow triggered.")
    else:
        logger.error(f"Trigger failed: {response.text}")
        console.print(f"[red]❌ Trigger failed:\n{response.text}")
        exit(1)


def get_latest_run_id():
    console.log("[cyan]Fetching latest run ID...")
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs"
    while True:
        response = requests.get(url, headers=HEADERS)
        runs = response.json().get("workflow_runs", [])
        if runs:
            return runs[0]["id"]
        time.sleep(3)


def wait_for_run(run_id):
    console.log("[yellow]Waiting for CI/CD pipeline to finish...")
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}"
    while True:
        response = requests.get(url, headers=HEADERS).json()
        status = response["status"]
        console.log(f"🔄 Status: {status}")
        if status == "completed":
            return response["conclusion"]
        time.sleep(5)


def download_and_extract_logs(run_id):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}/logs"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall("logs")
        console.log("📦 Logs downloaded to 'logs/'")
    else:
        logger.error("Failed to download logs")
        console.print(f"[red]❌ {response.text}")
        exit(1)


def print_logs():
    for root, dirs, files in os.walk("logs"):
        for file in sorted(files):
            path = os.path.join(root, file)
            console.print(f"\n📄 [bold]{file.replace('.txt', '')}[/bold]")
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                console.print(f.read())


def summarize_run(run_id):
    console.print("\n📋 [bold cyan]Generating Summary...")
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

    console.print(summary)


if __name__ == "__main__":
    autodevops()

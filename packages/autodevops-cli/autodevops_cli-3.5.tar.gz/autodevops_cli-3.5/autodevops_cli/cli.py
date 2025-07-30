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
from datetime import datetime
from loguru import logger
from rich.console import Console
import shutil

# --------------------- INIT ---------------------
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

console = Console()
client = OpenAI(api_key="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")

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
        run_pipeline(command_input)


# --------------------- STRUCTURE + AI ANALYSIS ---------------------
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
    save_output("README.md", readme, folder_path)
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
    summary += ["\nTop folders by file count:"] + \
        [f"  {folder}/: {count} files" for folder,
            count in sorted(folder_count.items(), key=lambda x: -x[1])[:10]]
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


def save_output(filename, content, folder_path):
    path = Path(folder_path) / filename
    path.write_text(content)
    console.log(f"📄 Saved: {filename}")

    requirements_dir = Path(__file__).resolve().parent / "Requirements"
    target_path = Path.cwd()

    def safe_copy(src, dest, label):
        try:
            if not dest.exists():
                shutil.copy(src, dest)
                console.log(f"✅ Copied {label}")
        except FileNotFoundError:
            console.log(
                f"[yellow]⚠️ {label} not found in {requirements_dir}, skipping...[/yellow]")

    safe_copy(requirements_dir / "Dockerfile",
              target_path / "Dockerfile", "Dockerfile")
    safe_copy(requirements_dir / "test_main.py",
              target_path / "test_main.py", "test_main.py")

    workflow_file = target_path / ".github/workflows/main.yml"
    if not workflow_file.exists():
        workflow_file.parent.mkdir(parents=True, exist_ok=True)
        safe_copy(requirements_dir / "main.yml", workflow_file,
                  "GitHub Actions workflow file")


# --------------------- CI/CD + GITHUB ACTIONS ---------------------
def run_pipeline(commit_message):
    console.rule("[bold blue]🚀 CI/CD Pipeline Triggering")
    try:
        from sh import git
        console.log("[yellow]Pulling latest code...")
        git.pull()
        console.log("[cyan]Adding changes...")
        git.add(".")
        console.log(f"[magenta]Committing: {commit_message}")
        git.commit("-m", commit_message)
        console.log("[green]Pushing to GitHub...")
        git.push()
    except Exception as e:
        console.print(f"[red]❌ Git error: {e}")
        exit(1)

    trigger_workflow()
    time.sleep(10)
    run_id = get_latest_run_id()
    wait_for_run(run_id)
    download_and_extract_logs(run_id)
    print_logs()
    summarize_run(run_id)
    evaluate_docker_image("your-image-name:latest")


def trigger_workflow():
    console.log("[green]Triggering GitHub Actions...")
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILENAME}/dispatches"
    res = requests.post(url, headers=HEADERS, json={"ref": BRANCH})
    if res.status_code == 204:
        console.log("✅ Workflow triggered.")
    else:
        console.print(f"[red]❌ Trigger failed: {res.text}")
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
        status = requests.get(url, headers=HEADERS).json()["status"]
        console.log(f"🔄 Status: {status}")
        if status == "completed":
            return
        time.sleep(5)


def download_and_extract_logs(run_id):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}/logs"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            z.extractall("logs")
        console.log("📦 Logs downloaded to 'logs/'")
    else:
        console.print(f"[red]❌ Failed to download logs: {r.text}")
        exit(1)


def print_logs():
    for root, _, files in os.walk("logs"):
        for file in sorted(files):
            path = os.path.join(root, file)
            console.print(f"\n📄 === {file.replace('.txt', '')} ===")
            console.print(Path(path).read_text(
                encoding="utf-8", errors="ignore"))


def summarize_run(run_id):
    console.print("\n📋 [bold cyan]Generating Summary...")
    run_info = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}", headers=HEADERS).json()
    commit = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/commits/{run_info['head_sha']}", headers=HEADERS).json()
    steps = [file.replace('.txt', '') for root, _, files in os.walk(
        "logs") for file in files if file.endswith('.txt')]
    actions = []
    for step in steps:
        s = step.lower()
        if "pytest" in s:
            actions.append("✅ Ran unit tests using Pytest")
        if "docker" in s and "login" in s:
            actions.append("🔐 Logged in to Docker Hub")
        if "docker image" in s or "build" in s:
            actions.append("📦 Built Docker image")
        if "push" in s:
            actions.append("🚀 Pushed Docker image")
    summary = f"""✅ CI/CD Pipeline Summary
----------------------------

📦 Commit Info:
- Message       : {commit['commit']['message']}
- Author        : {run_info['actor']['login']}
- Commit SHA    : {run_info['head_sha']}
- Branch        : {run_info['head_branch']}

🧪 Workflow Run: {run_info['name']}
- Status        : {'✅ Success' if run_info['conclusion'] == 'success' else '❌ Failed'}
- Triggered by  : {run_info['event']}
- Duration      : {run_info.get("run_duration_ms", 0)/1000:.2f} sec

📋 Job Steps:""" + "\n".join([f"{i+1}. {step} ✅" for i, step in enumerate(steps)]) + "\n\n🛠️ Actions Performed:\n" + "\n".join([f"- {a}" for a in actions])
    Path("ci_summary.txt").write_text(summary)
    console.print(summary)


# --------------------- DOCKER CHECK ---------------------
def run_command(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"


def evaluate_docker_image(image):
    log_summary("# 🐳 Docker Image Evaluation")
    log_summary(f"**Image Name:** `{image}`\n")
    inspect_image(image)
    check_history(image)
    check_size(image)
    container_id = run_command(["docker", "run", "-d", image])
    time.sleep(5)
    check_health(container_id)
    run_command(["docker", "rm", "-f", container_id])
    Path("docker_summary.txt").write_text("\n".join(summary_lines))
    console.print("[bold green]📄 Docker summary saved to 'docker_summary.txt'")


def inspect_image(image):
    output = run_command(["docker", "inspect", image])
    try:
        info = json.loads(output)[0]
        log_summary(f"- Entrypoint: {info['Config'].get('Entrypoint')}")
        log_summary(f"- CMD: {info['Config'].get('Cmd')}")
        log_summary(f"- Env Vars: {len(info['Config'].get('Env', []))}")
        log_summary(f"- Exposed Ports: {info['Config'].get('ExposedPorts')}")
    except Exception as e:
        log_summary(f"❌ Failed to inspect image: {e}")


def check_history(image):
    output = run_command(["docker", "history", "--no-trunc",
                         "--format", "{{.CreatedBy}}\t{{.Size}}", image])
    table = tabulate([line.split("\t") for line in output.splitlines()], headers=[
                     "Command", "Size"], tablefmt="github")
    log_summary("\n## 📜 Docker History\n" + table)


def check_size(image):
    output = run_command(["docker", "image", "inspect",
                         image, "--format={{.Size}}"])
    size_mb = round(int(output) / (1024 ** 2),
                    2) if output.isdigit() else output
    log_summary(f"- Size: {size_mb} MB")


def check_health(container_id):
    output = run_command(
        ["docker", "inspect", "--format={{json .State.Health}}", container_id])
    try:
        health = json.loads(output)
        log_summary(f"- Health Status: {health.get('Status')}")
        for entry in health.get("Log", []):
            log_summary(f"  - [{entry['ExitCode']}] {entry['Output'].strip()}")
    except:
        log_summary("No health check defined or error parsing.")


if __name__ == "__main__":
    autodevops()

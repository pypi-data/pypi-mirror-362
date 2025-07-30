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
BASE_DIR = Path(__file__).resolve().parent
# No separate 'requirements' folder, just near by
REQUIREMENTS_DIR = BASE_DIR

load_dotenv(dotenv_path=BASE_DIR.parent / ".env")

console = Console()
client = OpenAI(api_key="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")

LOG_DIR = BASE_DIR / "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logger.add(
    LOG_DIR / f"autodevops_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", rotation="1 MB")

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


def save_output(filename, content, folder_path, copy_files=False):
    path = Path(folder_path) / filename
    path.write_text(content)
    console.log(f"📄 Saved: {filename}")

    if copy_files:
        copy_required_files(folder_path)


def copy_required_files(folder_path):
    target_path = Path(folder_path)

    def safe_copy(src_file, dest_file, label):
        try:
            if not dest_file.exists():
                shutil.copy(src_file, dest_file)
                console.log(f"✅ Copied {label} to {dest_file}")
        except FileNotFoundError:
            console.log(
                f"[yellow]⚠️ {label} not found in {REQUIREMENTS_DIR}, skipping...[/yellow]")

    safe_copy(REQUIREMENTS_DIR / "Dockerfile",
              target_path / "Dockerfile", "Dockerfile")
    safe_copy(REQUIREMENTS_DIR / "test_main.py",
              target_path / "test_main.py", "test_main.py")

    workflow_file = target_path / ".github/workflows/main.yml"
    if not workflow_file.exists():
        workflow_file.parent.mkdir(parents=True, exist_ok=True)
        safe_copy(REQUIREMENTS_DIR / "main.yml",
                  workflow_file, "GitHub Actions workflow")


if __name__ == "__main__":
    autodevops()

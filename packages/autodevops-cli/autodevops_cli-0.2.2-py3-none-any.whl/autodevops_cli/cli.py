import os
import sys
import json
import time
import click
import sh
import subprocess
from datetime import datetime
from time import sleep
from loguru import logger
from rich.console import Console
from rich.status import Status
from rich.progress import track
from tabulate import tabulate
import typer

# ========================
# 🎯 Initialization
# ========================
console = Console()
app = typer.Typer()
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger.add(
    f"{LOG_DIR}/autodevops_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", rotation="1 MB")

MAX_LINES = 10
ci_logs = []
summary_lines = []


# ========================
# 🔁 CLI Log Handler
# ========================
def bounded_log(msg, color="cyan"):
    if len(ci_logs) >= MAX_LINES:
        ci_logs.pop(0)
        console.clear()
        for line in ci_logs:
            console.print(line)
    styled_msg = f"[{color}]{msg}"
    ci_logs.append(styled_msg)
    console.print(styled_msg)
    logger.info(msg)


# ========================
# 🚀 Git + CI/CD Simulation
# ========================
@app.command()
def autodevops(message: str):
    """🚀 AutoDevOps: Git Push + CI/CD Simulation Tool"""

    console.rule("[bold blue]🔧 Starting AutoDevOps Workflow")

    try:
        with console.status("[bold green]Running Git Commands...", spinner="dots"):
            bounded_log("📥 Pulling latest changes", "yellow")
            sh.git.pull()

            bounded_log("➕ Adding all changes", "blue")
            sh.git.add(".")

            bounded_log(f"📝 Committing with message: '{message}'", "magenta")
            sh.git.commit("-m", message)

            bounded_log("🚀 Pushing to remote...", "green")
            sh.git.push()

        console.rule("[bold blue]🧪 Triggering CI/CD Pipeline")
        with console.status("[bold green]Simulating CI/CD...", spinner="bouncingBall"):
            sleep(1)
            bounded_log("🏗️ Building Docker image...", "yellow")
            sleep(1)
            bounded_log("✅ Running unit tests...", "blue")
            sleep(1)
            bounded_log("📦 Pushing to Docker Hub...", "magenta")
            sleep(1)
            bounded_log("🎉 Deployment Successful!", "green")

        console.rule("[bold green]✅ AutoDevOps Completed Successfully")
        logger.success("✅ Git Push & CI/CD Workflow Completed Successfully")

    except sh.ErrorReturnCode as e:
        console.print(f"[bold red]❌ Command failed: {e.stderr.decode()}")
        logger.error(f"❌ Git command failed: {e.stderr.decode()}")
        sys.exit(1)

    proceed = typer.confirm(
        "🧪 Do you want to evaluate the Docker image?", default=True)
    if proceed:
        image_name = typer.prompt("Enter the Docker image name")
        evaluate_image(image_name)


# ========================
# 🐳 Docker Evaluation
# ========================
def log_summary(line=""):
    summary_lines.append(line)


def run_command(cmd):
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"


def inspect_image(image_name):
    console.rule("[bold cyan]🔍 Inspecting Docker Image")
    log_summary("## 🔍 Inspecting Docker Image")
    output = run_command(["docker", "inspect", image_name])
    try:
        info = json.loads(output)[0]
        entrypoint = info['Config'].get('Entrypoint')
        cmd = info['Config'].get('Cmd')
        env = info['Config'].get('Env', [])
        ports = info['Config'].get('ExposedPorts')

        console.print(f"Entrypoint: {entrypoint}")
        console.print(f"CMD: {cmd}")
        console.print(f"Env Vars: {len(env)}")
        console.print(f"Exposed Ports: {ports}")

        log_summary(f"- Entrypoint: {entrypoint}")
        log_summary(f"- CMD: {cmd}")
        log_summary(f"- Env Vars: {len(env)} variables")
        log_summary(f"- Exposed Ports: {ports}")
    except Exception as e:
        console.print(f"[red]Failed to parse inspect output: {e}")
        log_summary("❌ Failed to parse inspect output.")


def check_history(image_name):
    console.rule("[bold cyan]📜 Docker Image History")
    log_summary("\n## 📜 Docker Image History")
    output = run_command(["docker", "history", "--no-trunc",
                         "--format", "{{.CreatedBy}}\t{{.Size}}", image_name])
    lines = output.splitlines()
    table = [line.split('\t') for line in lines]
    console.print(
        tabulate(table, headers=["Command", "Size"], tablefmt="github"))
    log_summary(tabulate(table, headers=[
                "Command", "Size"], tablefmt="github"))


def check_size(image_name):
    console.rule("[bold cyan]📦 Docker Image Size")
    log_summary("\n## 📦 Docker Image Size")
    output = run_command(["docker", "image", "inspect",
                         image_name, "--format={{.Size}}"])
    if output.isdigit():
        size_mb = round(int(output) / (1024 ** 2), 2)
        console.print(f"Size: {size_mb} MB")
        log_summary(f"- Size: {size_mb} MB")
    else:
        console.print(f"Size: {output}")
        log_summary(f"- Size: {output}")


def check_health(container_id):
    console.rule("[bold cyan]❤️ Container Health Check")
    log_summary("\n## ❤️ Container Health Status")
    output = run_command(
        ["docker", "inspect", "--format={{json .State.Health}}", container_id])
    try:
        health = json.loads(output)
        status = health.get("Status")
        streak = health.get("FailingStreak")
        logs = health.get("Log", [])

        console.print(f"Status: {status}")
        console.print(f"Failing Streak: {streak}")
        log_summary(f"- Status: {status}")
        log_summary(f"- Failing Streak: {streak}")
        for entry in logs:
            msg = f"  - [{entry['ExitCode']}] {entry['Output'].strip()}"
            console.print(msg)
            log_summary(msg)
    except:
        console.print(
            "[yellow]No health check defined or container too early to inspect health.")
        log_summary(
            "No health check defined or container too early to inspect health.")


def evaluate_image(image_name):
    log_summary("# 🐳 Docker Image Evaluation")
    log_summary(f"**Image Name:** `{image_name}`\n")

    inspect_image(image_name)
    check_history(image_name)
    check_size(image_name)

    console.print("\n🚀 Spinning up container to test healthcheck...")
    log_summary("\n## 🚀 Container Healthcheck")
    container_id = run_command(["docker", "run", "-d", image_name]).strip()
    console.print(f"Container ID: {container_id}")
    log_summary(f"- Container ID: `{container_id}`")

    console.print("⏳ Waiting 5 seconds for healthcheck to initialize...")
    time.sleep(5)
    check_health(container_id)

    console.print("\n🧹 Cleaning up container...")
    run_command(["docker", "rm", "-f", container_id])
    console.print("✅ Done")
    log_summary("\n✅ Container cleaned up.\n")

    with open("docker_summary.txt", "w") as f:
        f.write("\n".join(summary_lines))

    console.print("\n📄 [green]Docker summary saved to 'docker_summary.txt'")


# ========================
# 🏁 Entry Point
# ========================
if __name__ == "__main__":
    app()

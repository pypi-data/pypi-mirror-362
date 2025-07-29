import click
import sh
from time import sleep
from rich.console import Console
from rich.status import Status
from loguru import logger
from datetime import datetime
import os

console = Console()
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logger.add(f"{LOG_DIR}/autodevops_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", rotation="1 MB")

@click.command()
@click.argument('message')
def autodevops(message):
    """🚀 AutoDevOps CLI: Git Push + CI/CD Simulation"""
    console.rule("[bold blue]🔧 AutoDevOps Starting")

    try:
        with console.status("[green]Git Operations...", spinner="dots") as status:
            console.log("[yellow]Pulling latest...")
            sh.git.pull()

            console.log("[cyan]Adding changes...")
            sh.git.add(".")

            console.log(f"[magenta]Committing: {message}")
            sh.git.commit("-m", message)

            console.log("[green]Pushing to remote...")
            sh.git.push()

        console.rule("[bold blue]🧪 Simulating CI/CD Pipeline")
        with console.status("[green]Running pipeline...", spinner="bouncingBar"):
            sleep(1)
            console.log("[yellow]Building Docker image...")
            sleep(1)
            console.log("[cyan]Running tests...")
            sleep(1)
            console.log("[magenta]Deploying to staging...")
            sleep(1)
            console.log("[green]✅ Deployed!")

        logger.success("CI/CD process completed successfully.")
        console.rule("[bold green]✅ Done")

    except sh.ErrorReturnCode as e:
        logger.error(f"Git error: {e.stderr.decode()}")
        console.print(f"[red]❌ Git Error:\n{e.stderr.decode()}")
        exit(1)

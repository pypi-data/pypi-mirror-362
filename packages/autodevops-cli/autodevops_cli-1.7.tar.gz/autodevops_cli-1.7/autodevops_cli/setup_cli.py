import os
import click
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from collections import defaultdict
from rich.console import Console

# Load environment
load_dotenv()
console = Console()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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


def run_analysis(folder_path, max_files):
    console.rule(f"[bold yellow]📂 AutoDevOps Analysis Started: {folder_path}")
    summary = scan_directory_structure(folder_path, max_files)
    console.print(
        f"[cyan]📁 Total Files Scanned:[/cyan] {min(len(summary), max_files)}")
    console.print("\n".join(summary[:20]) + "\n...")

    # 1. Structure Analysis
    structure_analysis = gpt_call(
        "Structure Analysis",
        "Analyze the folder structure and suggest improvements.",
        summary
    )
    save_output("structure_analysis.md", structure_analysis, folder_path)
    console.rule("[bold blue]📦 STRUCTURE ANALYSIS")
    console.print(structure_analysis)

    # 2. Tech Stack
    tech_stack = gpt_call(
        "Tech Stack",
        "Detect the tech stack (backend, frontend, tools, DB, testing) from this project structure.",
        summary
    )
    save_output("tech_stack.md", tech_stack, folder_path)
    console.rule("[bold green]🛠️ TECH STACK")
    console.print(tech_stack)

    # 3. README.md
    readme = gpt_call(
        "README.md",
        "Generate a clean, production-ready README.md file for this project.",
        summary
    )
    save_output("README.md", readme, folder_path)

    console.rule(
        "[bold green]🎉 Project analyzed and README generated successfully!")


@click.command()
@click.argument('folder_path', required=True)
def main(folder_path):
    """AutoDevOps Setup: Analyze project structure and generate docs"""
    path = Path(folder_path).expanduser().resolve()
    if not path.exists() or not path.is_dir():
        console.print(
            f"[red]❌ Path not found or not a directory: {folder_path}[/red]")
        raise click.Abort()

    run_analysis(path, max_files=500)


if __name__ == "__main__":
    main()

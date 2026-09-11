"""Execute the analysis notebook and export it as a clean HTML report."""

from pathlib import Path
import subprocess
import sys


def main() -> None:
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--execute",
        "--to",
        "html",
        "src/analysis/analysis_pipeline.ipynb",
        "--output",
        "../../output/analysis.html",
        "--TemplateExporter.exclude_input=True",
        "--TemplateExporter.exclude_input_prompt=True",
        "--TemplateExporter.exclude_output_prompt=True",
    ]

    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
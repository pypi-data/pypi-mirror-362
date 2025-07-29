import shutil
import subprocess
from pathlib import Path


class MissingBinaryException(Exception): ...


def _ensure_installed(binary: str) -> None:
    if not shutil.which(binary):
        raise MissingBinaryException(
            f"This library requires `{binary}`." "Please ensure it is installed."
        )


_ensure_installed("pdflatex")
_ensure_installed("pdftoppm")


DEFAULT_TEMPLATE = r"""
\documentclass[border=10pt, 12pt, preview]{{standalone}}

\begin{{document}}

{snippet}

\end{{document}}
"""
"""The default template for [`latex_to_png`][tex2image.latex_to_png].

This is passed to `DEFAULT_TEMPLATE.format(snippet=latex_snippet)` in
[`latex_to_png`][tex2image.latex_to_png].
"""


def latex_to_png(
    latex_snippet: str, temp_dir: Path, template: str | None = DEFAULT_TEMPLATE
) -> None:
    """Render `latex_snippet` to `snippet.png` in `temp_dir`.

    Note that this function expects `temp_dir_name` to be empty when executed.
    The function may still work if it is not empty, but there are no guarantees.

    If the function successfully completes, then `temp_dir` should contain a file
    called `snippet.png`.
    The directory may also contain auxiliary files generated from the compilation
    process.

    Parameters:
        latex_snippet: The latex code to render.

        temp_dir: The directory in which the generated image will be saved.

        template: If None, then the latex_snippet will be directly passed to
            `pdflatex`.
            Otherwise, `template.format(snippet=latex_snippet)` will be passed to
            `pdflatex`.

    Example:

    ```py
    from pathlib import Path
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as temp_dir:
        latex_to_png("Pythagorean Theorem: $a^2 + b^2 = c^2$.", Path(temp_dir))
        image_file_path = Path(temp_dir) / "main.png"
        # Do something with the image here, before temp_dir gets deleted...
    ```
    """
    (temp_dir / "main.tex").write_text(
        template.format(snippet=latex_snippet)
        if template is not None
        else latex_snippet
    )

    run_pdflatex(temp_dir, "main.tex")
    run_pdftoppm(temp_dir, "main.pdf", "main.png")


def run_pdflatex(directory: Path, file_name: str) -> None:
    """Run `pdflatex` with sensible arguments to convert tex source to PDF."""
    latex_result = subprocess.run(
        ["pdflatex", "-interaction=batchmode", file_name],
        cwd=directory,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    latex_result.check_returncode()


def run_pdftoppm(directory: Path, input_file_name: str, output_file_name) -> None:
    """Run `pdftoppm` with sensible arguments to convert PDF to PNG."""
    with open(directory / output_file_name, "w") as image_file:
        pdftoppm_result = subprocess.run(
            [
                "pdftoppm",
                "-png",
                "-r",
                "300",
                "-x",
                "1",
                "-y",
                "1",
                "-W",
                "-2",
                "-H",
                "-2",
                str(directory / input_file_name),
            ],
            stdout=image_file,
            stderr=subprocess.DEVNULL,
        )
    pdftoppm_result.check_returncode()

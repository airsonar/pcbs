# SPDX-FileCopyrightText: AirSonar contributors
# SPDX-License-Identifier: BSD-2-Clause-Patent

# mkdocs hook to export KiCad files to a PDF. This can be given multiple exports which
# it then concatenates to a single PDF for the file output. Usage:
#
# ```kipdf
# output: filename.pdf
# link_text: exported design
# %%%
# source: path/to/schematic.kicad_sch
# --no-background-color
# %%%
# source: path/to/layout.kicad_pcb
# --layers
# F.Cu,F.Silkscreen,Edge.Cuts
# --scale
# 0
# %%%
# source: path/to/layout.kicad_pcb
# --layers
# B.Cu,B.Silkscreen,Edge.Cuts
# --scale
# 0
# ```
#
# The first line of each section is the file to export (the export command is determined
# based on the extension). The remaining lines are command-line arguments for the
# export. The exports are concatenated into a single PDF in the order given. This
# requires that the `kicad-cli` executable is available on the path, and that the pypdf
# library is installed.

from pathlib import Path, PosixPath
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import event_priority
import pypdf  # type:ignore[import-not-found]


@event_priority(999)
def on_config(config: MkDocsConfig):
    # Ensure the superfences extension is enabled.
    if "pymdownx.superfences" not in config.markdown_extensions:
        config.markdown_extensions.append("pymdownx.superfences")
    if "pymdownx.superfences" not in config.mdx_configs:
        config.mdx_configs["pymdownx.superfences"] = {}
    if "custom_fences" not in config.mdx_configs["pymdownx.superfences"]:
        config.mdx_configs["pymdownx.superfences"]["custom_fences"] = []

    # Add a custom fence.
    config.mdx_configs["pymdownx.superfences"]["custom_fences"].append(
        {
            "name": "kipdf",
            "class": "kipdf",
            "format": kipdf_fence,
        }
    )


@event_priority(0)
def on_post_build(config: MkDocsConfig) -> None:
    # Non-markdown files in docs/ are copied into the final site. Remove this script and
    # the compiled versions of it.
    site = Path(config.site_dir)
    (site / "kipdf.py").unlink()
    cache = site / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


@event_priority(0)
def on_page_content(html: str, page, config: MkDocsConfig, files) -> str:
    # Find the directory containing this rendered page.
    subdir = Path(page.file.abs_dest_path).parent
    subdir.mkdir(parents=True, exist_ok=True)

    def generate_and_update_tag(matchobj: re.Match) -> str:
        output = ""
        link_text = ""

        # Split the contents into sections.
        sections = matchobj.group(1).split("%%%")

        # The first section should contain details about the output.
        for line in sections[0].splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("output:"):
                output = line[8:].strip()
            elif line.startswith("link_text:"):
                link_text = line[10:].strip()
            else:
                raise RuntimeError(f"KiPDF unexpected line {line}")

        # These are mandatory.
        if not output:
            raise RuntimeError("KiPDF output filename not specified")
        if not link_text:
            raise RuntimeError("KiPDF link text not specified")

        # Each remaining section corresponds to one PDF export which we will then
        # combine into a single PDF. Export these to a temporary directory that will be
        # cleaned up when we are done.
        pieces = []
        base = Path(__file__).parent.parent
        with TemporaryDirectory() as tempd:
            for i, section in enumerate(sections[1:]):
                # Parse the section contents.
                source = None
                cliargs = []
                for line in section.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("source:"):
                        rel = PosixPath(line[7:].strip())
                        source = base.joinpath(*rel.parts)
                    else:
                        cliargs.append(line)

                # Source is mandatory.
                if not source:
                    raise RuntimeError("KiPDF source filename not specified")

                # Figure out which converter to use.
                if source.suffix == ".kicad_sch":
                    cmd = "sch"
                elif source.suffix == ".kicad_pcb":
                    cmd = "pcb"
                else:
                    raise RuntimeError("KiPDF unhandled filetype")

                # And generate this PDF.
                fn = Path(tempd) / f"section-{i}.pdf"
                subprocess.run(
                    ["kicad-cli", cmd, "export", "pdf", "--output", str(fn)]
                    + cliargs
                    + [str(source)],
                    check=True,
                )
                pieces.append(fn)

            # Concatenate all PDFs into the desired output.
            writer = pypdf.PdfWriter()
            for piece in pieces:
                writer.append(piece)
            writer.write(subdir / output)

        # And return a new tag linking to this PDF.
        return f'<a class="kipdf" href="{output}">{link_text}</a>'

    # Run this function over each <kipdf> tag added by the fence.
    html = re.sub(
        "<kipdf>(.+?)</kipdf>", generate_and_update_tag, html, flags=re.DOTALL
    )
    return html


def kipdf_fence(
    source: str, language: str, class_name: str, options: dict, md, **kwargs
) -> str:
    # Wrap the source in a custom <kipdf> tag. The on_page_content() hook will do the
    # actual work of generating and linking the PDF.
    return f"<kipdf>{source}</kipdf>"

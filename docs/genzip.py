# SPDX-FileCopyrightText: AirSonar contributors
# SPDX-License-Identifier: BSD-2-Clause-Patent

# mkdocs hook to generate a zip file. Usage:
#
# ```genzip
# output: filename.zip
# link test: a zip file
# %%%
# directory: path/to/dir
# file: filea.txt
# file: subdir/fileb.txt
# ```
#
# This will create a zip file with the named directories and files, and be formatted in
# the built page as <a href="filename.zip">a zip file</a>.

from pathlib import Path, PosixPath
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory
import zipfile

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
            "name": "genzip",
            "class": "genzip",
            "format": genzip_fence,
        }
    )


@event_priority(0)
def on_post_build(config: MkDocsConfig) -> None:
    # Non-markdown files in docs/ are copied into the final site. Remove this script and
    # the compiled versions of it.
    site = Path(config.site_dir)
    (site / "genzip.py").unlink()
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
        if len(sections) != 2:
            raise RuntimeError("genzip should have exactly two sections")

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
                raise RuntimeError(f"genzip unexpected line {line}")

        # These are mandatory.
        if not output:
            raise RuntimeError("genzip output filename not specified")
        if not link_text:
            raise RuntimeError("genzip link text not specified")

        # Each remaining section corresponds to one PDF export which we will then
        # combine into a single PDF. Export these to a temporary directory that will be
        # cleaned up when we are done.
        pieces = []
        base = Path(__file__).parent.parent
        with zipfile.ZipFile(subdir / output, "w", compression=zipfile.ZIP_DEFLATED) as f:
            for source in sections[1].splitlines():
                source = source.strip()
                if not source:
                    continue

                if source.startswith("file:"):
                    rel = PosixPath(source[5:].strip())
                    fn = base.joinpath(*rel.parts)
                    if not fn.is_file():
                        raise RuntimeError(f"genzip source {rel} is not a file")
                    f.write(fn, fn.relative_to(base))

                elif source.startswith("directory:"):
                    rel = PosixPath(source[10:].strip())
                    dn = base.joinpath(*rel.parts)
                    if not dn.is_dir():
                        raise RuntimeError(f"genzip source {rel} is not a directory")

                    for dirpath, _, filenames in dn.walk():
                        for filename in filenames:
                            fn = dirpath / filename
                            f.write(fn, fn.relative_to(base))

                else:
                    raise RuntimeError(f"unknown genzip source {source}")

        # And return a new tag linking to this PDF.
        return f'<a class="kipdf" href="{output}">{link_text}</a>'

    # Run this function over each <kipdf> tag added by the fence.
    html = re.sub(
        "<genzip>(.+?)</genzip>", generate_and_update_tag, html, flags=re.DOTALL
    )
    return html


def genzip_fence(
    source: str, language: str, class_name: str, options: dict, md, **kwargs
) -> str:
    # Wrap the source in a custom <genzip> tag. The on_page_content() hook will do the
    # actual work of generating and linking the zipfile..
    return f"<genzip>{source}</genzip>"

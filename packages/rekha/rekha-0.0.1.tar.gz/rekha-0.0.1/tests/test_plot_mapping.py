#!/usr/bin/env python3
"""
Quick test to check plot mapping between documentation and generated files.
"""

import os
import re
from pathlib import Path


def get_svg_references_from_docs(docs_dir):
    """Extract all SVG references from documentation files."""
    svg_refs = set()

    # Pattern to match image references in Markdown and RST
    patterns = [
        re.compile(r"!\[.*?\]\((.*?\.svg)\)"),  # Markdown: ![alt](path.svg)
        re.compile(r"\.\. image::\s+(.+?\.svg)"),  # RST: .. image:: path.svg
        re.compile(r"\.\. figure::\s+(.+?\.svg)"),  # RST: .. figure:: path.svg
        re.compile(
            r'<img[^>]+src=["\']([^"\']+\.svg)["\']'
        ),  # HTML: <img src="path.svg">
    ]

    # Walk through docs directory, excluding _build
    for root, dirs, files in os.walk(docs_dir):
        # Skip _build directory
        if "_build" in dirs:
            dirs.remove("_build")

        for file in files:
            if file.endswith((".md", ".rst", ".txt")):
                file_path = Path(root) / file
                try:
                    content = file_path.read_text()

                    for pattern in patterns:
                        matches = pattern.findall(content)
                        for match in matches:
                            # Extract just the filename, not the full path
                            svg_name = Path(match).name
                            svg_refs.add(svg_name)
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")

    return svg_refs


def get_generated_plots(plots_dir):
    """Get all generated SVG files."""
    svg_files = set()

    if plots_dir.exists():
        for svg_path in plots_dir.glob("*.svg"):
            svg_files.add(svg_path.name)

    return svg_files


def create_filename_mapping(doc_refs, generated_plots):
    """Create a mapping between expected and actual filenames."""
    mapping = {}

    # Try to match documentation references to generated files
    for doc_ref in doc_refs:
        # Skip non-plot SVGs
        if "License" in doc_ref or "rekha.svg" == doc_ref:
            continue

        # Try exact match first
        if doc_ref in generated_plots:
            mapping[doc_ref] = doc_ref
            continue

        # Try to find a matching generated file
        base_name = doc_ref.replace(".svg", "")
        candidates = []

        for gen_file in generated_plots:
            gen_base = gen_file.replace(".svg", "")
            # Check if the documentation name is contained in the generated name
            if base_name in gen_base or gen_base in base_name:
                candidates.append(gen_file)

        if len(candidates) == 1:
            mapping[doc_ref] = candidates[0]
        elif len(candidates) > 1:
            # Try to find the best match
            # Prefer shorter names as they're likely more specific
            best_match = min(candidates, key=len)
            mapping[doc_ref] = best_match

    return mapping


def main():
    project_root = Path(__file__).parent.parent
    docs_dir = project_root / "docs"
    plots_dir = project_root / "docs" / "_static" / "plots"

    # Get all SVG references from documentation
    doc_refs = get_svg_references_from_docs(docs_dir)
    print(f"\nFound {len(doc_refs)} SVG references in documentation:")
    for ref in sorted(doc_refs):
        print(f"  - {ref}")

    # Get all generated plots
    generated_plots = get_generated_plots(plots_dir)
    print(f"\nGenerated {len(generated_plots)} plots:")
    for plot in sorted(generated_plots):
        print(f"  - {plot}")

    # Create mapping
    mapping = create_filename_mapping(doc_refs, generated_plots)

    # Check for missing plots (referenced but not generated)
    missing_plots = set()
    for doc_ref in doc_refs:
        if "License" in doc_ref or "rekha.svg" == doc_ref:
            continue
        if doc_ref not in mapping:
            missing_plots.add(doc_ref)

    if missing_plots:
        print(f"\n❌ Missing plots (referenced but not generated):")
        for plot in sorted(missing_plots):
            print(f"  - {plot}")

    # Show mapping
    print(f"\n📊 Filename mapping (documentation -> generated):")
    for doc_name, gen_name in sorted(mapping.items()):
        if doc_name != gen_name:
            print(f"  {doc_name} -> {gen_name}")

    # Check for extra plots (generated but not referenced)
    used_generated = set(mapping.values())
    extra_plots = generated_plots - used_generated

    # Filter out known duplicates or test files
    extra_plots = {
        p for p in extra_plots if not any(skip in p for skip in ["example", "test"])
    }

    if extra_plots:
        print(f"\n⚠️  Extra plots (generated but not referenced):")
        for plot in sorted(extra_plots):
            print(f"  - {plot}")

    # Summary
    print(f"\n📊 Summary:")
    print(f"  - Documentation references: {len(doc_refs)}")
    print(f"  - Generated plots: {len(generated_plots)}")
    print(f"  - Successfully mapped: {len(mapping)}")
    print(f"  - Missing plots: {len(missing_plots)}")
    print(f"  - Extra plots: {len(extra_plots)}")

    if missing_plots:
        print(f"\n❌ Test failed: {len(missing_plots)} plots are missing!")
        return 1
    else:
        print(f"\n✅ All documented plots are generated!")
        return 0


if __name__ == "__main__":
    exit(main())

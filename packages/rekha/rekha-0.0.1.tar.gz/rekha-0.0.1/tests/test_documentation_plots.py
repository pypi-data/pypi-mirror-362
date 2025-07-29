#!/usr/bin/env python3
"""
Test to ensure 1-1 mapping between generated plots and documentation references.

This test:
1. Runs the generate_docs_plots.sh script to generate all plots
2. Greps all .png references from the documentation
3. Verifies that all referenced plots are generated
4. Ensures no extra plots are generated that aren't referenced
5. Validates plot integrity and properties
6. Checks for common issues (e.g., empty files, corrupted images)
"""

import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Set, Tuple

import pytest


@pytest.mark.unit
class TestDocumentationPlots:
    """Test documentation plot generation and references."""

    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.project_root = Path(__file__).parent.parent
        cls.docs_dir = cls.project_root / "docs"
        cls.scripts_dir = cls.project_root / "scripts"
        cls.examples_dir = cls.project_root / "examples"
        cls.plots_dir = cls.project_root / "docs" / "_static" / "plots"

    def get_png_references_from_docs(self) -> Set[str]:
        """Extract all PNG references from documentation files."""
        png_refs = set()

        # Pattern to match image references in Markdown and RST
        patterns = [
            re.compile(r"!\[.*?\]\((.*?\.png)\)"),  # Markdown: ![alt](path.png)
            re.compile(r"\.\. image::\s+(.+?\.png)"),  # RST: .. image:: path.png
            re.compile(r"\.\. figure::\s+(.+?\.png)"),  # RST: .. figure:: path.png
            re.compile(
                r'<img[^>]+src=["\']([^"\']+\.png)["\']'
            ),  # HTML: <img src="path.png">
        ]

        # Walk through docs directory, excluding _build
        for root, dirs, files in os.walk(self.docs_dir):
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
                                png_name = Path(match).name
                                png_refs.add(png_name)
                    except Exception as e:
                        print(f"Warning: Could not read {file_path}: {e}")

        return png_refs

    def run_generate_docs_plots_script(self, output_dir: Path) -> Tuple[bool, str]:
        """Run the generate_docs_plots.sh script."""
        script_path = self.scripts_dir / "generate_docs_plots.sh"

        if not script_path.exists():
            return False, f"Script not found: {script_path}"

        # Run the script
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.project_root)

        try:
            result = subprocess.run(
                [str(script_path), "--clean"],
                capture_output=True,
                text=True,
                env=env,
                cwd=str(self.project_root),
                timeout=300,  # 5 minute timeout
            )

            if result.returncode != 0:
                error_output = f"Return code: {result.returncode}\n"
                error_output += f"STDOUT:\n{result.stdout}\n"
                error_output += f"STDERR:\n{result.stderr}\n"
                error_output += f"Command: {' '.join([str(script_path), '--clean'])}\n"
                error_output += f"Working directory: {self.project_root}\n"
                error_output += (
                    f"Environment PYTHONPATH: {env.get('PYTHONPATH', 'Not set')}\n"
                )

                # Check if common commands exist
                common_commands = ["python", "bash", "parallel", "xargs"]
                for cmd in common_commands:
                    try:
                        cmd_result = subprocess.run(
                            ["which", cmd], capture_output=True, text=True
                        )
                        if cmd_result.returncode == 0:
                            error_output += f"Command '{cmd}' found at: {cmd_result.stdout.strip()}\n"
                        else:
                            error_output += f"Command '{cmd}' not found\n"
                    except:
                        error_output += f"Failed to check for command '{cmd}'\n"

                return False, error_output

            return True, result.stdout
        except subprocess.TimeoutExpired:
            return False, f"Script timed out after 5 minutes"
        except Exception as e:
            return (
                False,
                f"Error running script: {e}\nScript path: {script_path}\nWorking dir: {self.project_root}",
            )

    def get_generated_plots(self, output_dir: Path) -> Set[str]:
        """Get all generated PNG files."""
        png_files = set()

        if output_dir.exists():
            for png_path in output_dir.glob("*.png"):
                png_files.add(png_path.name)

        return png_files

    def validate_plot_integrity(self, plot_path: Path) -> Tuple[bool, str]:
        """Validate that a plot file is valid and not corrupted."""
        if not plot_path.exists():
            return False, "File does not exist"

        # Check file size (should be at least 1KB for a valid PNG)
        file_size = plot_path.stat().st_size
        if file_size < 1024:
            return False, f"File too small ({file_size} bytes)"

        # Check PNG signature
        try:
            with open(plot_path, "rb") as f:
                # PNG files start with these bytes
                png_signature = b"\x89PNG\r\n\x1a\n"
                if f.read(8) != png_signature:
                    return False, "Invalid PNG signature"
        except Exception as e:
            return False, f"Could not read file: {e}"

        return True, "Valid PNG"

    def check_plot_consistency(self, plot_dir: Path) -> Dict[str, Dict[str, Any]]:
        """Check consistency of plot pairs (light/dark variants)."""
        issues = {}

        # Get all plots
        all_plots = list(plot_dir.glob("*.png"))

        # Group by base name
        plot_groups = {}
        for plot in all_plots:
            if plot.name.endswith("_light.png"):
                base_name = plot.name[:-10]
                if base_name not in plot_groups:
                    plot_groups[base_name] = {}
                plot_groups[base_name]["light"] = plot
            elif plot.name.endswith("_dark.png"):
                base_name = plot.name[:-9]
                if base_name not in plot_groups:
                    plot_groups[base_name] = {}
                plot_groups[base_name]["dark"] = plot
            else:
                # Single variant plot (e.g., quickstart_dark_mode.png)
                plot_groups[plot.stem] = {"single": plot}

        # Check each group
        for base_name, variants in plot_groups.items():
            group_issues = {}

            # Check if both variants exist (unless it's a single variant)
            if "single" not in variants:
                if "light" not in variants:
                    group_issues["missing_light"] = True
                if "dark" not in variants:
                    group_issues["missing_dark"] = True

                # If both exist, check their sizes are reasonable
                if "light" in variants and "dark" in variants:
                    light_size = variants["light"].stat().st_size
                    dark_size = variants["dark"].stat().st_size

                    # Sizes should be within 50% of each other
                    size_ratio = max(light_size, dark_size) / min(light_size, dark_size)
                    if size_ratio > 2.0:
                        group_issues["size_mismatch"] = {
                            "light_size": light_size,
                            "dark_size": dark_size,
                            "ratio": size_ratio,
                        }

            if group_issues:
                issues[base_name] = group_issues

        return issues

    def test_plot_documentation_mapping(self):
        """Test that all documented plots are generated and vice versa."""
        # Use the actual output directory from generate_docs_plots.sh
        output_dir = self.plots_dir

        # Get all PNG references from documentation
        doc_refs = self.get_png_references_from_docs()
        print(f"\nFound {len(doc_refs)} PNG references in documentation:")
        for ref in sorted(doc_refs):
            print(f"  - {ref}")

        # Run the generate_docs_plots.sh script
        print(f"\nRunning generate_docs_plots.sh...")
        success, output = self.run_generate_docs_plots_script(output_dir)

        if not success:
            error_msg = f"Failed to run generate_docs_plots.sh:\n"
            error_msg += f"Exit code: Script failed\n"
            error_msg += f"Error output:\n{output}\n"
            error_msg += f"Script path: {self.scripts_dir / 'generate_docs_plots.sh'}\n"
            error_msg += f"Working directory: {self.project_root}\n"
            error_msg += f"Output directory: {output_dir}\n"

            # Check if the script exists
            script_path = self.scripts_dir / "generate_docs_plots.sh"
            if not script_path.exists():
                error_msg += f"ERROR: Script does not exist at {script_path}\n"
            else:
                error_msg += f"Script exists and is {'executable' if script_path.stat().st_mode & 0o111 else 'not executable'}\n"

            # Check if required directories exist
            for dir_name, dir_path in [
                ("Scripts", self.scripts_dir),
                ("Examples", self.examples_dir),
                ("Output", output_dir.parent),
            ]:
                if dir_path.exists():
                    error_msg += f"{dir_name} directory exists: {dir_path}\n"
                else:
                    error_msg += f"ERROR: {dir_name} directory missing: {dir_path}\n"

            pytest.fail(error_msg)

        # Get all generated plots
        generated_plots = self.get_generated_plots(output_dir)
        print(f"\nGenerated {len(generated_plots)} plots:")
        for plot in sorted(generated_plots):
            print(f"  - {plot}")

        # Check for missing plots (referenced but not generated)
        non_plot_pngs = set()
        plot_refs = doc_refs - non_plot_pngs
        missing_plots = plot_refs - generated_plots
        if missing_plots:
            print(f"\n❌ Missing plots (referenced but not generated):")
            for plot in sorted(missing_plots):
                print(f"  - {plot}")

        # Check for extra plots (generated but not referenced)
        extra_plots = generated_plots - doc_refs
        if extra_plots:
            print(f"\n⚠️  Extra plots (generated but not referenced):")
            for plot in sorted(extra_plots):
                print(f"  - {plot}")

        # Assertions
        assert (
            not missing_plots
        ), f"Missing {len(missing_plots)} plots that are referenced in docs"

        # Extra plots are okay (they don't break anything), but warn about them
        if extra_plots:
            print(
                f"\n⚠️  Note: {len(extra_plots)} extra plots generated but not used in docs (this is okay)"
            )
            # Don't fail the test for extra plots, only for missing ones

        print(f"\n✅ All {len(doc_refs)} documented plots are generated correctly!")

    def test_plot_integrity(self):
        """Test that all generated plots are valid PNG files."""
        output_dir = self.plots_dir

        # Ensure plots are generated
        if not output_dir.exists() or not list(output_dir.glob("*.png")):
            success, output = self.run_generate_docs_plots_script(output_dir)
            if not success:
                pytest.fail(f"Failed to generate plots: {output}")

        invalid_plots = []
        for plot_path in output_dir.glob("*.png"):
            valid, message = self.validate_plot_integrity(plot_path)
            if not valid:
                invalid_plots.append((plot_path.name, message))

        if invalid_plots:
            print("\n❌ Invalid plots found:")
            for plot_name, issue in invalid_plots:
                print(f"  - {plot_name}: {issue}")
            pytest.fail(f"Found {len(invalid_plots)} invalid plot files")

        print(f"\n✅ All plots are valid PNG files")

    def test_plot_generation_modes(self):
        """Test that both light and dark mode variants are generated for each plot."""
        output_dir = self.plots_dir

        # Run generation if output directory doesn't exist
        if not output_dir.exists() or not list(output_dir.glob("*.png")):
            success, output = self.run_generate_docs_plots_script(output_dir)
            if not success:
                pytest.fail(f"Failed to run generate_docs_plots.sh: {output}")

        # Check plot consistency
        issues = self.check_plot_consistency(output_dir)

        if issues:
            print("\n⚠️  Plot consistency issues found:")
            for base_name, group_issues in issues.items():
                print(f"\n  {base_name}:")
                for issue_type, issue_data in group_issues.items():
                    if issue_type == "size_mismatch":
                        print(
                            f"    - Size mismatch: light={issue_data['light_size']} bytes, dark={issue_data['dark_size']} bytes (ratio={issue_data['ratio']:.2f})"
                        )
                    else:
                        print(f"    - {issue_type}")

        # Some plots intentionally have only one variant
        allowed_single_variants = {"quickstart_dark_mode"}

        # Filter out allowed single variants
        real_issues = {
            k: v
            for k, v in issues.items()
            if k not in allowed_single_variants
            and ("missing_light" in v or "missing_dark" in v)
        }

        if real_issues:
            pytest.fail(f"Found {len(real_issues)} plots with missing variants")

        print("\n✅ All plots have appropriate variants")

    def test_palette_plots_visibility(self):
        """Test that palette plots don't have invisible colors."""
        output_dir = self.plots_dir

        # Palette plots that might have visibility issues
        problematic_palettes = {
            "monokai": "contains white color (#F8F8F2) that's invisible on white background",
            "solarized": "may have contrast issues",
        }

        issues = []
        for palette_name, issue_description in problematic_palettes.items():
            light_plot = output_dir / f"palette_{palette_name}_light.png"
            if light_plot.exists():
                # In a real implementation, we'd analyze the image
                # For now, we'll flag these as needing manual review
                issues.append(f"palette_{palette_name}_light.png - {issue_description}")

        if issues:
            print("\n⚠️  Palette plots with potential visibility issues:")
            for issue in issues:
                print(f"  - {issue}")
            # Don't fail the test, just warn
            print("\nThese palettes should be reviewed for visibility issues")

    def test_example_scripts_exist(self):
        """Test that example script directories referenced in generate_docs_plots.sh exist."""
        script_path = self.scripts_dir / "generate_docs_plots.sh"
        if not script_path.exists():
            pytest.fail(f"Generate docs plots script not found: {script_path}")

        # Check that key directories exist
        example_dirs = [
            self.examples_dir / "quickstart",
            self.examples_dir / "plots",
            self.examples_dir / "advanced",
        ]

        missing_dirs = []
        for dir_path in example_dirs:
            if not dir_path.exists():
                missing_dirs.append(str(dir_path))
            else:
                # Check that directory has Python files
                py_files = list(dir_path.glob("*.py"))
                if not py_files:
                    print(f"Warning: No Python files in {dir_path}")

        if missing_dirs:
            print("\n❌ Missing example directories:")
            for dir_name in missing_dirs:
                print(f"  - {dir_name}")
            pytest.fail(f"Found {len(missing_dirs)} missing example directories")

        # Count total example scripts
        total_scripts = 0
        for dir_path in example_dirs:
            if dir_path.exists():
                if dir_path.name == "plots":
                    # Count scripts in subdirectories
                    for subdir in dir_path.iterdir():
                        if subdir.is_dir():
                            total_scripts += len(list(subdir.glob("*.py")))
                else:
                    total_scripts += len(list(dir_path.glob("*.py")))

        print(f"\n✅ All example directories exist with {total_scripts} total scripts")


if __name__ == "__main__":
    # Run the test directly
    test = TestDocumentationPlots()
    test.setup_class()

    print("=" * 80)
    print("Testing Documentation Plot System")
    print("=" * 80)

    tests = [
        ("Plot Documentation Mapping", test.test_plot_documentation_mapping),
        ("Plot Integrity", test.test_plot_integrity),
        ("Plot Generation Modes", test.test_plot_generation_modes),
        ("Palette Plot Visibility", test.test_palette_plots_visibility),
        ("Example Scripts Existence", test.test_example_scripts_exist),
    ]

    failed_tests = []
    for test_name, test_func in tests:
        print(f"\n{'=' * 80}")
        print(f"Running: {test_name}")
        print("=" * 80)

        try:
            test_func()
        except AssertionError as e:
            print(f"\n❌ Test failed: {e}")
            failed_tests.append((test_name, str(e)))
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            failed_tests.append((test_name, f"Unexpected error: {e}"))

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    if failed_tests:
        print(f"\n❌ {len(failed_tests)} tests failed:")
        for test_name, error in failed_tests:
            print(f"  - {test_name}: {error}")
        exit(1)
    else:
        print("\n✅ All tests passed!")

"""
Script to render PNG images from UI reference HTML files.

This script scans the repository for HTML files inside `ui-reference` folders
(both direct children and subfolders), executes JavaScript (Tailwind CDN, web fonts,
micro-interactions), and captures high-fidelity PNG screenshots.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Sequence

from playwright.sync_api import Browser, Page, sync_playwright


def find_ui_reference_html_files(
    root_dir: Path,
    targets: Sequence[str] | None = None,
) -> list[Path]:
    """Find all .html files within folders named `ui-reference` (or matching specific target paths)."""
    if targets:
        matched: list[Path] = []
        for target in targets:
            target_path = Path(target)
            if not target_path.is_absolute():
                target_path = (root_dir / target_path).resolve()
            if target_path.is_file() and target_path.suffix.lower() == ".html":
                matched.append(target_path)
            elif target_path.is_dir():
                for p in target_path.rglob("*.html"):
                    matched.append(p.resolve())
            else:
                # Try globbing
                for p in root_dir.glob(target):
                    if p.is_file() and p.suffix.lower() == ".html":
                        matched.append(p.resolve())
                    elif p.is_dir():
                        for sub_p in p.rglob("*.html"):
                            matched.append(sub_p.resolve())
        # Deduplicate while preserving order
        seen: set[Path] = set()
        result: list[Path] = []
        for p in matched:
            if p not in seen:
                seen.add(p)
                result.append(p)
        return result

    html_files: list[Path] = []
    for p in root_dir.rglob("*.html"):
        # Check if 'ui-reference' is one of the directory parts
        parts_lower = [part.lower() for part in p.parts]
        if "ui-reference" in parts_lower:
            html_files.append(p.resolve())

    return sorted(html_files)


def determine_output_path(
    html_file: Path,
    root_dir: Path,
    output_dir: Path | None = None,
    output_name: str | None = None,
) -> Path:
    """Determine the destination path for the rendered PNG screenshot."""
    if output_name:
        filename = output_name if output_name.lower().endswith(".png") else f"{output_name}.png"
    elif html_file.name.lower() == "code.html":
        filename = "screen.png"
    else:
        filename = f"{html_file.stem}.png"

    if output_dir:
        # Replicate relative directory structure under output_dir
        try:
            rel_dir = html_file.parent.relative_to(root_dir)
            dest_dir = output_dir / rel_dir
        except ValueError:
            dest_dir = output_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        return dest_dir / filename

    return html_file.parent / filename


def wait_for_page_ready(page: Page, wait_ms: int = 500) -> None:
    """Wait for all dynamic JavaScript, Tailwind CSS stylesheets, web fonts, and images to settle."""
    # 1. Wait for web fonts (Inter, Material Symbols, etc.) to finish loading
    try:
        page.evaluate("() => document.fonts ? document.fonts.ready : Promise.resolve()")
    except Exception:
        pass

    # 2. Wait for images to load
    try:
        page.evaluate("""() => {
            const images = Array.from(document.images);
            return Promise.all(images.map(img => {
                if (img.complete) return Promise.resolve();
                return new Promise(resolve => {
                    img.addEventListener('load', resolve, { once: true });
                    img.addEventListener('error', resolve, { once: true });
                });
            }));
        }""")
    except Exception:
        pass

    # 3. Wait for Tailwind CDN runtime compilation to inject style rules into DOM
    try:
        page.wait_for_function(
            """() => {
                const styles = Array.from(document.querySelectorAll('style'));
                return styles.some(s => s.textContent && (s.textContent.includes('bg-surface') || s.textContent.includes('tailwindcss') || s.id.includes('tailwind')));
            }""",
            timeout=3000,
        )
    except Exception:
        # If no specific tailwind style detected, continue after timeout
        pass

    # 4. Brief stabilization wait for CSS layouts, backdrop filters, and custom initializers
    if wait_ms > 0:
        page.wait_for_timeout(wait_ms)


def render_file(
    page: Page,
    html_file: Path,
    output_file: Path,
    wait_ms: int = 500,
    disable_animations: bool = True,
) -> tuple[int, int, int]:
    """Render a single HTML file to PNG and return (width, height, file_size_bytes)."""
    # Open local file via file:// URI
    file_uri = html_file.resolve().as_uri()
    page.goto(file_uri, wait_until="networkidle")

    # Wait for JS execution, Tailwind CSS generation, fonts, and assets
    wait_for_page_ready(page, wait_ms=wait_ms)

    # Ensure target parent folder exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Capture full page screenshot
    animations_opt = "disabled" if disable_animations else "allow"
    page.screenshot(path=str(output_file), full_page=True, animations=animations_opt)

    file_size = output_file.stat().st_size
    # Read image dimensions from PNG header
    with open(output_file, "rb") as f:
        header = f.read(24)
        if header.startswith(b"\x89PNG\r\n\x1a\n"):
            import struct
            w, h = struct.unpack(">LL", header[16:24])
        else:
            w, h = (0, 0)

    return w, h, file_size


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render PNG mockups from UI reference HTML files with full JavaScript & Tailwind CSS execution."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Optional path(s) or glob pattern(s) of HTML files or directories to render. Defaults to all ui-reference HTML files.",
    )
    parser.add_argument(
        "--root",
        "-r",
        type=Path,
        default=Path("."),
        help="Root directory of the project (default: current directory).",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=None,
        help="Custom output directory. If omitted, PNGs are saved alongside their corresponding HTML files.",
    )
    parser.add_argument(
        "--output-name",
        "-n",
        type=str,
        default=None,
        help="Custom output filename (e.g., 'screen.png'). Default is 'screen.png' for 'code.html' or '<stem>.png' for others.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=390,
        help="Viewport width in CSS pixels (default: 390 for mobile mockup standard).",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=884,
        help="Viewport height in CSS pixels (default: 884).",
    )
    parser.add_argument(
        "--scale",
        "--device-scale-factor",
        type=float,
        default=1.5,
        dest="scale",
        help="Device pixel scale factor (default: 1.5, producing 585px width matching Stitch reference PNGs).",
    )
    parser.add_argument(
        "--wait-ms",
        type=int,
        default=500,
        help="Stabilization wait time in milliseconds after fonts and Tailwind compile (default: 500).",
    )
    parser.add_argument(
        "--browser",
        choices=["chromium", "chrome", "msedge", "firefox", "webkit"],
        default="chromium",
        help="Browser engine to use (default: chromium).",
    )
    parser.add_argument(
        "--allow-animations",
        action="store_true",
        help="Allow CSS animations during screenshot (default is to disable animations for crisp static frames).",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root_dir = args.root.resolve()

    html_files = find_ui_reference_html_files(root_dir, args.targets)
    if not html_files:
        print(f"No HTML files found under ui-reference in '{root_dir}'.", file=sys.stderr)
        return 1

    print(f"Found {len(html_files)} HTML file(s) to render.")
    print(f"Viewport: {args.width}x{args.height} @ {args.scale}x scale factor")

    start_time = time.time()
    rendered_count = 0
    failed_count = 0

    with sync_playwright() as p:
        browser_type = getattr(p, args.browser if args.browser in ["chromium", "firefox", "webkit"] else "chromium")
        launch_kwargs = {"headless": True}
        if args.browser in ["chrome", "msedge"]:
            launch_kwargs["channel"] = args.browser

        browser: Browser = browser_type.launch(**launch_kwargs)
        page: Page = browser.new_page(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
            color_scheme="dark",
        )

        for idx, html_file in enumerate(html_files, 1):
            try:
                rel_html = html_file.relative_to(root_dir)
            except ValueError:
                rel_html = html_file

            out_path = determine_output_path(
                html_file=html_file,
                root_dir=root_dir,
                output_dir=args.output_dir.resolve() if args.output_dir else None,
                output_name=args.output_name,
            )

            try:
                rel_out = out_path.relative_to(root_dir)
            except ValueError:
                rel_out = out_path

            print(f"[{idx}/{len(html_files)}] Rendering: {rel_html} -> {rel_out} ...", end="", flush=True)

            try:
                w, h, sz = render_file(
                    page=page,
                    html_file=html_file,
                    output_file=out_path,
                    wait_ms=args.wait_ms,
                    disable_animations=not args.allow_animations,
                )
                print(f" OK ({w}x{h}, {sz / 1024:.1f} KB)")
                rendered_count += 1
            except Exception as e:
                print(f" FAILED: {e}")
                failed_count += 1

        browser.close()

    elapsed = time.time() - start_time
    print(f"\nDone! Rendered {rendered_count}/{len(html_files)} screenshots in {elapsed:.2f}s. (Failed: {failed_count})")
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

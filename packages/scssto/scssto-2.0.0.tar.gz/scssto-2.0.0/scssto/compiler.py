#!/usr/bin/env python3

import os
import argparse
import subprocess
import sys

VERSION = "1.0.0"

def compile_scss_to_css(scss_dir, css_dir, force=False):
    if not os.path.isdir(scss_dir):
        print(f"Error: SCSS directory '{scss_dir}' not found.")
        sys.exit(1)

    if not os.path.exists(css_dir):
        if force:
            os.makedirs(css_dir)
            print(f"Created output directory: {css_dir}")
        else:
            print(f"Error: CSS directory '{css_dir}' does not exist. Use --force to create it.")
            sys.exit(1)

    scss_files = [f for f in os.listdir(scss_dir) if f.endswith(".scss")]

    if not scss_files:
        print("No .scss files found in input directory.")
        sys.exit(0)

    for filename in scss_files:
        input_path = os.path.join(scss_dir, filename)
        output_filename = filename.replace(".scss", ".css")
        output_path = os.path.join(css_dir, output_filename)

        try:
            subprocess.run(["sass", input_path, output_path], check=True)
            print(f"Compiled: {filename} -> {output_filename}")
        except subprocess.CalledProcessError:
            print(f"Failed to compile: {filename}")

def main():
    parser = argparse.ArgumentParser(
        description="Compile all .scss files in a folder to .css using the 'sass' command."
    )
    parser.add_argument("-s", "--scss", required=True, help="Input folder containing .scss files")
    parser.add_argument("-c", "--css", required=True, help="Output folder for .css files")
    parser.add_argument("-f", "--force", action="store_true", help="Create output folder if it does not exist")
    parser.add_argument("--version", action="version", version=f"scssto {VERSION}")

    args = parser.parse_args()

    compile_scss_to_css(args.scss, args.css, args.force)

if __name__ == "__main__":
    main()

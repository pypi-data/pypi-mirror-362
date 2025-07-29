import argparse
from .cli import compile_scss_to_css

def main():
    parser = argparse.ArgumentParser(description="Compile SCSS files to CSS")
    parser.add_argument("-scss", required=True, help="Input SCSS folder")
    parser.add_argument("-css", required=True, help="Output CSS folder")
    args = parser.parse_args()

    compile_scss_to_css(args.scss, args.css)

import sys, json, argparse
from pathlib import Path
from parser import Parser  # if this ever clashes with stdlib 'parser', rename your file/module

def main():
    ap = argparse.ArgumentParser(description="EduScript DSL → JSON")
    ap.add_argument("path", nargs="?", metavar="FILE",
                    help="-")
    args = ap.parse_args()

    # Read source (file or stdin)
    if not args.path or args.path == "-":
        src = sys.stdin.read()
        if not src.strip():
            ap.error("no input provided (pass FILE or use '-' with stdin)")
    else:
        p = Path(args.path)
        if not p.exists():
            ap.error(f"file not found: {p}")
        src = p.read_text(encoding="utf-8")

        result = None
        try:
            result = Parser(src).run()
            # Print JSON
            print(json.dumps(result.model_dump(exclude_none=True), ensure_ascii=False, indent=2))
        except ValueError as e:
            print(e)
            sys.exit(1)

if __name__ == "__main__":
    main()

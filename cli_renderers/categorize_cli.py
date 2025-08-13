# categorize_cli.py
import argparse, json, random, sys
from typing import Dict, List

def build_exercise() -> Dict:
    return {
        "mode": "single",
        "metadata": {
            "type": "categorize",
            "variation": "original",
            "instructions": "Do not die please",
            "category": "vocabulary",
            "difficulty": "beginner",
            "style": "nature",
            "title": "something like this",
            "packageId": "",
            "is_published": True
        },
        "exercises": [
            {
                "exercise": {
                    "content": [
                        {
                            "category": "<categorize, colors>\n\n  ANIMALS",
                            "items": ["Lion", "Chicken", "Tiger", "Dog", "Cat"],
                            "points": []
                        },
                        {
                            "category": "FRUITS",
                            "items": ["Banana", "apple", "Pear", "Orage", "Dragon Fruit"],
                            "points": []
                        },
                        {
                            "category": "COLORS",
                            "items": ["Blue", "Red", "White", "Green", "Black"],
                            "points": []
                        },
                        {
                            "category": "CLASSROOM",
                            "items": ["Pencil", "Notebook", "School Bag", "Computer", "Eraser"],
                            "points": []
                        }
                    ],
                    "distractors": ["beach", "happyness"]
                }
            }
        ]
    }

def _label(s: str) -> str:
    # Use the last non-empty line as the display label (handles the first category's prefix)
    parts = [ln.strip() for ln in s.splitlines() if ln.strip()]
    return parts[-1] if parts else s.strip()

def play_game(data: Dict, seed: int = None) -> int:
    if seed is not None:
        random.seed(seed)

    ex = data["exercises"][0]["exercise"]
    contents = ex["content"]
    distractors = ex.get("distractors", [])

    labels = [_label(c["category"]) for c in contents]
    label_to_items = { _label(c["category"]): set(c["items"]) for c in contents }

    # Build answer key (case-insensitive item -> label)
    answer: Dict[str, str] = {}
    for label, items in label_to_items.items():
        for it in items:
            answer[it.lower()] = label

    all_items: List[str] = []
    for items in label_to_items.values():
        all_items.extend(items)
    all_items.extend(distractors)

    random.shuffle(all_items)

    print("\n=== CATEGORIZE ===")
    print(data["metadata"]["instructions"])
    print("\nCategories:")
    for i, lb in enumerate(labels, 1):
        print(f"  {i}. {lb}")
    print("  d. DISTRACTOR (does not belong)")
    print("  q. Quit\n")

    total = len(all_items)
    correct = 0
    wrong: List[tuple] = []

    for idx, item in enumerate(all_items, 1):
        while True:
            choice = input(f"[{idx}/{total}] Where does '{item}' go? (1-{len(labels)}, d, q): ").strip()
            if choice.lower() == "q":
                print("\nBye!")
                summary(correct, idx - 1, wrong, answer)
                return 0
            if choice.lower() == "d":
                predicted = None
                break
            if choice.isdigit() and 1 <= int(choice) <= len(labels):
                predicted = labels[int(choice) - 1]
                break
            # also allow typing the category name directly
            if choice.upper() in labels or choice.title() in labels:
                predicted = choice.upper() if choice.upper() in labels else choice.title()
                break
            print("  Invalid choice. Try again.")

        key = item.lower()
        is_distractor = item in distractors
        if is_distractor:
            if predicted is None:
                correct += 1
                print("  ✓ Correct (distractor)\n")
            else:
                wrong.append((item, "DISTRACTOR", predicted))
                print(f"  ✗ Wrong — should be DISTRACTOR\n")
        else:
            gold = answer[key]
            if predicted == gold:
                correct += 1
                print("  ✓ Correct\n")
            else:
                wrong.append((item, gold, "DISTRACTOR" if predicted is None else predicted))
                print(f"  ✗ Wrong — should be {gold}\n")

    summary(correct, total, wrong, answer)
    return 0

def summary(correct: int, total: int, wrong: List[tuple], answer: Dict[str, str]):
    print("=== SUMMARY ===")
    print(f"Score: {correct}/{total} ({(correct/total*100 if total else 0):.1f}%)")
    if wrong:
        print("\nReview:")
        for item, should_be, picked in wrong:
            print(f"  - {item}: {picked} → {should_be}")

def main():
    ap = argparse.ArgumentParser(prog="categorize-cli", description="Build and play a categorize exercise.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="Print the JSON to stdout (use --out to write to file).")
    b.add_argument("--out", help="Path to write JSON")

    p = sub.add_parser("play", help="Play the exercise in the terminal.")
    p.add_argument("--file", help="JSON file to load; default uses built-in example.")
    p.add_argument("--seed", type=int, help="Random seed for deterministic order.")

    args = ap.parse_args()

    if args.cmd == "build":
        data = build_exercise()
        text = json.dumps(data, ensure_ascii=False, indent=2)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(text + "\n")
            print(f"Wrote {args.out}")
        else:
            print(text)
        return

    if args.cmd == "play":
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = build_exercise()
        sys.exit(play_game(data, seed=args.seed))

if __name__ == "__main__":
    main()

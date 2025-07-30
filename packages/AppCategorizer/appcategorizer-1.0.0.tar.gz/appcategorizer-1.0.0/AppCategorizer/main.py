import sys
import argparse
from .categorizer import process_app, batch_process, load_model

def main():
    parser = argparse.ArgumentParser(description="Application categorization tool")
    parser.add_argument("app_name", nargs="*", help="Application name(s) or use batch mode")
    parser.add_argument("-b", "--batch", action="store_true", help="Batch mode")

    args = parser.parse_args()

    if args.batch:
        if len(args.app_name) != 2:
            parser.error("Batch mode requires input and output file names")
        batch_process(args.app_name[0], args.app_name[1])
        print(f"Batch processing completed. Results saved to {args.app_name[1]}")
    elif args.app_name:
        app_name = ' '.join(args.app_name)
        print(f"Processing application: '{app_name}'")
        classifier = load_model()
        app_name, main_cat, ai_cat, sub_cats = process_app(app_name, classifier)
        print("\nResults:")
        print(f"Application: {app_name}")
        print(f"Rule-Based Category: {main_cat}")
        print(f"AI Category: {ai_cat}")
        print(f"Sub-Categories: {', '.join(sub_cats)}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
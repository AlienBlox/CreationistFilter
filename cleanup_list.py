import json
import os
import sys

# Define file path and required fields
FILE_NAME = "Creationists.json"
REQUIRED_FIELDS = ["domain", "category", "reason", "scientific_resource"]

def process_creationist_json():
    # 1. Check if the file exists
    if not os.path.exists(FILE_NAME):
        print(f"Error: {FILE_NAME} not found.")
        sys.exit(1)

    # 2. Try to parse the JSON file
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Critical Error: Invalid JSON formatting detected.\n{e}")
        sys.exit(1)

    if not isinstance(data, list):
        print("Critical Error: Top-level JSON structure must be a list of objects.")
        sys.exit(1)

    seen_domains = set()
    cleaned_data = []
    has_errors = False

    # 3. Formatter and Duplicate Filter Loop
    for index, item in enumerate(data):
        # Validate data type
        if not isinstance(item, dict):
            print(f"Error at item index {index}: Item is not a dictionary.")
            has_errors = True
            continue

        # Validate required keys
        missing_keys = [key for key in REQUIRED_FIELDS if key not in item]
        if missing_keys:
            print(f"Error at item index {index}: Missing keys {missing_keys}")
            has_errors = True
            continue

        # Clean domain string (lowercase, strip whitespace, remove 'www.')
        domain = item["domain"].strip().lower().replace("www.", "")
        item["domain"] = domain
        
        # Clean URLs and fields
        item["category"] = item["category"].strip()
        item["reason"] = item["reason"].strip()
        item["scientific_resource"] = item["scientific_resource"].strip()

        # Handle duplicates
        if domain in seen_domains:
            print(f"Duplicate Removed: {domain}")
            continue
            
        seen_domains.add(domain)
        cleaned_data.append(item)

    # Exit early if structural or validation errors exist
    if has_errors:
        print("Process aborted. Please fix the errors listed above before saving.")
        sys.exit(1)

    # 4. Alphabetical Sorting by Domain
    cleaned_data.sort(key=lambda x: x["domain"])

    # 5. Overwrite file with clean, formatted JSON
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
        f.write("\n")  # Add trailing newline for POSIX compliance

    print(f"Success! {FILE_NAME} has been formatted, deduplicated, and sorted.")

if __name__ == "__main__":
    process_creationist_json()

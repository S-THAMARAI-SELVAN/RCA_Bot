import os

# Create logs folder if not exists
os.makedirs("logs", exist_ok=True)

errors = []

required_files = [
    "index.html",
    "about.html",
    "contact.html",
    "blog.html",
    "discography.html",
    "tours.html",
    "videos.html"
]

required_folders = [
    "css",
    "js",
    "img"
]

# Check files
for file in required_files:
    if not os.path.isfile(file):
        errors.append(f"Missing file: {file}")

# Check folders
for folder in required_folders:
    if not os.path.isdir(folder):
        errors.append(f"Missing folder: {folder}")

# Validation Result
if errors:

    with open("logs/failure.log", "w", encoding="utf-8") as f:
        f.write("VALIDATION FAILED\n\n")

        for error in errors:
            f.write(error + "\n")

    print("Validation Failed")

    raise Exception("Website Validation Failed")

else:

    with open("logs/success.log", "w", encoding="utf-8") as f:
        f.write("Validation Successful")

    print("Validation Successful")
import os
from bs4 import BeautifulSoup

os.makedirs("logs", exist_ok=True)

errors = []

html_files = ["index.html", "timer.html"]

required_files = [
    "index.html",
    "timer.html",
    "templatemo-622-clearwave.css",
    "templatemo-622-clearwave.js"
]

required_folders = ["images"]

# Check required files
for file in required_files:
    if not os.path.isfile(file):
        errors.append(f"Missing file: {file}")

# Check required folders
for folder in required_folders:
    if not os.path.isdir(folder):
        errors.append(f"Missing folder: {folder}")

# Parse HTML files
for html_file in html_files:

    if not os.path.exists(html_file):
        continue

    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Check images
    for img in soup.find_all("img"):

        src = img.get("src")

        if src and not src.startswith(("http://", "https://")):
            if not os.path.exists(src):
                errors.append(
                    f"{html_file}: Missing image -> {src}"
                )

        if not img.get("alt"):
            errors.append(
                f"{html_file}: Image missing alt text -> {src}"
            )

    # Check CSS links
    for link in soup.find_all("link"):

        href = link.get("href")

        if href and href.endswith(".css"):
            if not os.path.exists(href):
                errors.append(
                    f"{html_file}: Missing CSS -> {href}"
                )

    # Check JS files
    for script in soup.find_all("script"):

        src = script.get("src")

        if src and not src.startswith(("http://", "https://")):
            if not os.path.exists(src):
                errors.append(
                    f"{html_file}: Missing JS -> {src}"
                )

    # Check local hyperlinks
    for a in soup.find_all("a"):

        href = a.get("href")

        if (
            href
            and not href.startswith(("#", "http://", "https://", "mailto:"))
        ):
            if not os.path.exists(href):
                errors.append(
                    f"{html_file}: Broken Link -> {href}"
                )

# Generate report
if errors:

    with open(
        "logs/failure.log",
        "w",
        encoding="utf-8"
    ) as f:

        f.write("WEBSITE VALIDATION FAILED\n\n")

        for error in errors:
            f.write(error + "\n")

    print("\nVALIDATION FAILED\n")

    for error in errors:
        print(error)

    raise Exception("Website Validation Failed")

else:

    with open(
        "logs/success.log",
        "w",
        encoding="utf-8"
    ) as f:

        f.write("Website Validation Successful")

    print("\nWebsite Validation Successful")
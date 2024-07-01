import os

EXCLUDED = {".git", ".github", "scripts", "README.md", "_config.yml"}


def generate_file_structure(base_path, path=""):
    result = []
    full_path = os.path.join(base_path, path)

    if os.path.basename(full_path) in EXCLUDED:
        return result

    if os.path.isdir(full_path):
        if path:  # Avoid root directory
            result.append(f"<details>\n<summary>{os.path.basename(path)}</summary>")
        for item in sorted(os.listdir(full_path)):
            item_path = os.path.join(path, item)
            result.extend(generate_file_structure(base_path, item_path))
        if path:  # Avoid root directory
            result.append("</details>")
    else:
        result.append(f'<a href="{path}">{os.path.basename(path)}</a>')
    return result


def update_readme(file_structure):
    readme_path = "README.md"
    with open(readme_path, "r") as readme_file:
        lines = readme_file.readlines()

    start_tag = "<!-- files -->"
    end_tag = "<!-- files-end -->"
    start_index = lines.index(start_tag + "\n") + 1
    end_index = lines.index(end_tag + "\n")

    new_lines = lines[:start_index] + file_structure + lines[end_index:]

    with open(readme_path, "w") as readme_file:
        readme_file.writelines(new_lines)


if __name__ == "__main__":
    base_path = "."
    file_structure = generate_file_structure(base_path)
    update_readme([line + "\n" for line in file_structure])

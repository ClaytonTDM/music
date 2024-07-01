import os
from mutagen import File

EXCLUDED = {".git", ".github", "scripts"}
AUDIO_EXTENSIONS = {".mp3", ".flac", ".m4a", ".wav", ".ogg"}


def get_track_number(file_path):
    try:
        audio = File(file_path)
        if audio:
            track_number = audio.tags.get("TRCK") or audio.tags.get("TRACKNUMBER")
            if track_number:
                # Ensure track_number is the first item if it's a list
                if isinstance(track_number, list):
                    track_number = track_number[0]
                    # Now safely access .text attribute
                    return int(track_number.text[0].split("/")[0])
    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")
    return None


def generate_file_structure(base_path, path=""):
    result = []
    full_path = os.path.join(base_path, path)

    if os.path.basename(full_path) in EXCLUDED:
        return result

    if os.path.isdir(full_path):
        if path:  # Avoid root directory
            result.append(f"<details>\n<summary>{os.path.basename(path)}</summary>")
        # Directories first
        directories = sorted(
            [
                d
                for d in os.listdir(full_path)
                if os.path.isdir(os.path.join(full_path, d))
            ]
        )
        total_items = len(
            directories
        )  # Initialize total_items with number of directories
        files = [
            f
            for f in os.listdir(full_path)
            if os.path.isfile(os.path.join(full_path, f))
        ]
        audio_files = [
            f for f in files if os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS
        ]
        other_files = [
            f for f in files if os.path.splitext(f)[1].lower() not in AUDIO_EXTENSIONS
        ]
        total_items += len(audio_files) + len(
            other_files
        )  # Add number of files to total_items

        # Process directories and files...
        # (Keep the existing logic for processing directories and files)

        if path:  # Avoid root directory
            # Check if the current item is not the last one before appending "</details><hr>"
            if (
                result[-1] != f"<details>\n<summary>{os.path.basename(path)}</summary>"
            ):  # Check if there are items added within <details>
                result.append("</details>")
                if not (
                    result[-1].startswith("<details>") or result[-1] == "</details>"
                ):  # Avoid appending <hr> if the next is <details> or it's the end
                    result.append("<hr>")

    else:
        result.append(f'<a href="{path}">{os.path.basename(path)}</a><br>')
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

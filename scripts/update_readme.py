def generate_file_structure(base_path, path=""):
    result = []
    full_path = os.path.join(base_path, path)

    # Check if the current path (directory or file) should be excluded
    if os.path.basename(path) in EXCLUDED or path in EXCLUDED:
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
                and os.path.join(path, d) not in EXCLUDED
            ]
        )
        for directory in directories:
            item_path = os.path.join(path, directory)
            result.extend(generate_file_structure(base_path, item_path))
        # Then files
        files = [
            f
            for f in os.listdir(full_path)
            if os.path.isfile(os.path.join(full_path, f))
            and os.path.join(path, f) not in EXCLUDED
        ]
        audio_files = [
            f for f in files if os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS
        ]
        other_files = [
            f for f in files if os.path.splitext(f)[1].lower() not in AUDIO_EXTENSIONS
        ]

        # Sort audio files by track number
        audio_files_with_tracks = [
            (f, get_track_number(os.path.join(full_path, f))) for f in audio_files
        ]
        audio_files_with_tracks.sort(
            key=lambda x: (x[1] is None, x[1])
        )  # None values should be at the end

        for file, track in audio_files_with_tracks:
            item_path = os.path.join(path, file)
            result.append(f'<a href="{item_path}">{file}</a><br>')

        # Add other files
        for file in sorted(other_files):
            item_path = os.path.join(path, file)
            result.append(f'<a href="{item_path}">{file}</a><br>')

        if path:  # Avoid root directory
            result.append("</details>")
    else:
        result.append(f'<a href="{path}">{os.path.basename(path)}</a><br>')
    return result

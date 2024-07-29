import fs from "fs";
import path from "path";
import { parseFile } from "music-metadata";
import util from "util";

const EXCLUDED = new Set([
    ".git",
    ".github",
    ".vscode",
    "assets",
    "node_modules",
    "scripts",
    "view",
    "_config.yml",
    ".gitignore",
    "desktop.ini",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "README.md"
]);
const AUDIO_EXTENSIONS = new Set([".mp3", ".flac", ".m4a", ".wav", ".ogg"]);

const readdir = util.promisify(fs.readdir);
const stat = util.promisify(fs.stat);

async function getTrackNumber(filePath) {
    try {
        const metadata = await parseFile(filePath);
        const trackNumber = metadata.common.track.no;
        return trackNumber;
    } catch (e) {
        console.error(`Error reading metadata from ${filePath}: ${e}`);
        return null;
    }
}

async function generateFileStructure(basePath, currentPath = "") {
    let result = [];
    const fullPath = path.join(basePath, currentPath);

    if (EXCLUDED.has(path.basename(fullPath))) {
        return result;
    }

    const stats = await stat(fullPath);
    if (stats.isDirectory()) {
        const directoryEntries = [];
        const fileEntries = [];

        if (currentPath) {
            // Avoid root directory
            directoryEntries.push(
                `<details>\n<hr>\n<summary>${path.basename(
                    currentPath
                )}</summary>`
            );
        }

        const items = await readdir(fullPath);
        for (const item of items) {
            if (EXCLUDED.has(item)) {
                // Skip excluded files
                continue;
            }

            const itemPath = path.join(currentPath, item);
            const itemFullPath = path.join(basePath, itemPath);
            const itemStats = await stat(itemFullPath);

            if (itemStats.isDirectory()) {
                const subDirectoryContent = await generateFileStructure(
                    basePath,
                    itemPath
                );
                directoryEntries.push(...subDirectoryContent);
            } else if (AUDIO_EXTENSIONS.has(path.extname(item).toLowerCase())) {
                const trackNumber = await getTrackNumber(itemFullPath);
                fileEntries.push({ itemPath, trackNumber });
            } else {
                fileEntries.push(
                    `<a class="link" href="${encodeURIComponent(itemPath)}">${item}</a><br>`
                );
            }
        }

        // Sort and format audio files
        const audioFiles = fileEntries.filter(
            (item) => typeof item === "object"
        );
        audioFiles.sort(
            (a, b) => (a.trackNumber || Infinity) - (b.trackNumber || Infinity)
        );
        audioFiles.forEach((file) => {
            fileEntries.push(
                `<a class="link" href="${encodeURIComponent(file.itemPath)}">${path.basename(
                    file.itemPath
                )}</a><br>`
            );
        });

        result = [
            ...directoryEntries,
            ...fileEntries.filter((item) => typeof item === "string"),
        ]; // Combine directories first, then files

        if (currentPath) {
            // Avoid root directory
            result.push("</details><hr>");
        }
    } else {
        result.push(
            `<a class="link" href="${encodeURIComponent(currentPath)}">${path.basename(
                currentPath
            )}</a><br>`
        );
    }
    return result;
}

async function updateReadme(fileStructure) {
    const readmePath = "README.md";
    const lines = fs.readFileSync(readmePath, "utf8").split("\n");

    const startTag = "<!-- files -->";
    const endTag = "<!-- files-end -->";
    const startIdx = lines.indexOf(startTag) + 1;
    const endIdx = lines.indexOf(endTag);

    const newLines = [
        ...lines.slice(0, startIdx),
        ...fileStructure,
        ...lines.slice(endIdx),
    ];
    fs.writeFileSync(readmePath, newLines.join("\n"));
}

async function main() {
    const basePath = ".";
    const fileStructure = await generateFileStructure(basePath);
    await updateReadme(fileStructure);
}

main().catch(console.error);

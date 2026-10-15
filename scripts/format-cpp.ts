import { format } from "@wasm-fmt/clang-format"
import { readdirSync, readFileSync, writeFileSync } from "node:fs"
import { extname, join, relative } from "node:path"
import { fileURLToPath } from "node:url"

/**
 * @summary Format C and C++ sources with clang-format.
 * @description Reads `.clang-format` and rewrites matching sources. `--check` exits with status 1 when a file would change.
 */
class FormatCpp {
    /**
     * @summary Repository root, the parent directory of this script.
     */
    private static readonly root = fileURLToPath(new URL("..", import.meta.url))

    /**
     * @summary Text of `.clang-format`.
     * @description Passed to clang-format as the style for every source.
     */
    private static readonly style = readFileSync(join(FormatCpp.root, ".clang-format"), "utf8")

    /**
     * @summary Whether the process was started with `--check`.
     */
    private static readonly check = process.argv.includes("--check")

    /**
     * @summary Extensions treated as C or C++ sources.
     */
    private static readonly extensions = new Set([".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx"])

    /**
     * @summary Directory names `collect` does not enter.
     * @description Logs preserve experiment evidence, including deliberately invalid source snapshots, unchanged.
     */
    private static readonly skipped = new Set(["node_modules", "dist", "build", "out", "pdfs", "submissions", "logs"])

    /**
     * @summary Blocks construction.
     * @description The script runs from the static block, not from an instance.
     */
    private constructor() {}

    /**
     * @summary Runs `init` when the class is evaluated.
     * @description Loading this file formats sources. The promise is discarded because `init` finishes during evaluation.
     */
    static {
        void this.init()
    }

    /**
     * @summary Collect C and C++ sources under `directory`.
     * @description Skips dot entries and `skipped` directories, and appends matching files to `files`.
     */
    private static collect(directory: string, files: string[]): void {
        for (const entry of readdirSync(directory, { withFileTypes: true })) {
            if (entry.name.startsWith(".") || this.skipped.has(entry.name)) {
                continue
            }

            const absolute = join(directory, entry.name)
            if (entry.isDirectory()) {
                this.collect(absolute, files)
                continue
            }

            if (this.extensions.has(extname(entry.name))) {
                files.push(absolute)
            }
        }
    }

    /**
     * @summary Format every collected source.
     * @description With `--check`, records paths and exits with status 1 instead of writing them.
     */
    private static async init(): Promise<void> {
        const files: string[] = []
        this.collect(this.root, files)

        const dirty: string[] = []
        for (const absolute of files) {
            const source = readFileSync(absolute, "utf8")
            const formatted = format(source, absolute, this.style)
            if (formatted === source) {
                continue
            }

            const path = relative(this.root, absolute)
            if (this.check) {
                dirty.push(path)
                continue
            }

            writeFileSync(absolute, formatted)
            console.log(path)
        }

        if (dirty.length > 0) {
            for (const path of dirty) {
                console.error(path)
            }
            process.exit(1)
        }
    }
}

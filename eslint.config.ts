import json from "@eslint/json"
import markdown from "@eslint/markdown"
import { defineConfig, globalIgnores } from "eslint/config"

/**
 * @summary Configuration of ESLint.
 * @description Specifies linting rules for JSON and Markdown files in all solutions.
 * @see {@link https://eslint.org/docs/latest/use/configure/configuration-files}
 */
export default defineConfig([
    /**
     * @remarks This repository shouldn't have any JavaScript/TypeScript files,
     * except this ESLint configuration.
     * @description Keep autofixes away from generated output, dependencies, and raw evidence.
     */
    globalIgnores([
        "**/node_modules/**",
        "**/dist/**",
        "**/build/**",
        "**/out/**",
        "**/_build/**",
        "**/.build/**",
        "**/.bundle/**",
        "**/.venv/**",
        "**/venv/**",
        "**/env/**",
        "**/__pycache__/**",
        "**/.cache/**",
        "**/coverage/**",
        "**/pdfs/**",
        "**/submissions/**",
        "**/logs/**",
        "**/wyniki/**",
        "**/bundles/**",
        "**/.idea/**",
        "**/.vscode/**",
        "**/.vs/**",
        "**/.cursor/**",
        "**/.claude/**",
        "**/.codex/**",
        "**/.ai/**",
        "**/package-lock.json",
        "**/yarn.lock",
        "**/pnpm-lock.yaml",
        "**/bun.lock",
    ]),
    {
        files: ["**/*.json"],
        plugins: { json },
        language: "json/json",
        extends: ["json/recommended"],
    },
    {
        files: ["**/*.jsonc"],
        plugins: { json },
        language: "json/jsonc",
        extends: ["json/recommended"],
    },
    {
        files: ["**/*.json5"],
        plugins: { json },
        language: "json/json5",
        extends: ["json/recommended"],
    },
    {
        files: ["**/*.md"],
        plugins: { markdown },
        language: "markdown/gfm",
        extends: ["markdown/recommended"],
        rules: {
            /**
             * @remarks This rule falsly triggers GFM-related tags (e.g. [!IMPORTANT], [!NOTE], etc.)
             * @description It's easier to simply turn it off rather than struggle later.
             */
            "markdown/no-missing-label-refs": "off",
        },
    },
])

import json from "@eslint/json"
import markdown from "@eslint/markdown"
import { defineConfig } from "eslint/config"

/**
 * @summary Configuration of ESLint.
 * @description Specifies linting rules for JSON and Markdown files in all solutions.
 * @see {@link https://eslint.org/docs/latest/use/configure/configuration-files}
 */
export default defineConfig([
    {
        ignores: ["**/*.js", "**/*.cjs", "**/*.mjs", "submissions/**", "solutions/**/.bundle/**"],
    },
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
            // This rule falsly triggers GFM-related tags (e.g. [!IMPORTANT], [!NOTE], etc.)
            "markdown/no-missing-label-refs": "off",
        },
    },
])

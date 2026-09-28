import { afterEach, expect, test } from "bun:test"
import {
    existsSync,
    mkdirSync,
    mkdtempSync,
    readFileSync,
    readdirSync,
    rmSync,
    symlinkSync,
    writeFileSync,
} from "node:fs"
import { tmpdir } from "node:os"
import { dirname, join } from "node:path"
import { bundle, contentDigest, parseManifest, runCommand, sections } from "./bundle"
import type { Artifact, Manifest, Runner } from "./bundle"

const roots: string[] = []
afterEach(() => {
    for (const root of roots.splice(0)) rmSync(root, { recursive: true, force: true })
})

function report(task: string): string {
    return (
        `---\ntitle: "Syntetyczny raport walidatora"\nauthor: "Kryptonim TiDPI: ALFA123"\ndate: "2026-09-28"\nlang: pl-PL\n---\n\n# Raport ${task}\n\n` +
        sections
            .map((section) => `## ${section}\n\nSyntetyczny test skryptu, nie wynik doświadczenia szkolnego. D01.\n`)
            .join("\n") +
        (task === "TiDPI_01" ? "\nDane fikcyjne: TC-01 TC-02 TC-03 TC-04 TC-05 TC-06.\n" : "")
    )
}

function fixture(task = "TiDPI_02") {
    const root = mkdtempSync(join(tmpdir(), "tidpi-bundle-test-"))
    roots.push(root)
    const taskDir = join(root, "solutions", task)
    mkdirSync(taskDir, { recursive: true })
    const put = (path: string, bytes: string | Buffer) => {
        const target = join(taskDir, path)
        mkdirSync(dirname(target), { recursive: true })
        writeFileSync(target, bytes)
    }
    const manifest: Manifest = {
        version: 1,
        task,
        codename: "ALFA123",
        levels: task === "TiDPI_01" ? [] : ["a"],
        extensions: [],
        reviewedContentSha256: null,
        artifacts: [{ path: "raport.md", role: "report" }],
    }
    put("raport.md", report(task))
    if (task === "TiDPI_01") {
        manifest.stages = [1, 2, 3]
        manifest.artifacts.push(
            { path: "wyniki.log", role: "raw-results", evidenceId: "D01" },
            { path: "raport.docx", role: "export-docx" },
            { path: "raport.pdf", role: "export-pdf" },
        )
        put("wyniki.log", "Syntetyczne dane fikcyjne. FAILURE 1.23\n")
    } else {
        manifest.artifacts.push(
            { path: "a/raport.md", role: "level-report", level: "a" },
            { path: "a/main.cpp", role: "source-cpp", level: "a" },
            { path: "a/wyniki.log", role: "raw-results", level: "a", evidenceId: "D01" },
        )
        put("a/raport.md", report(task))
        put("a/main.cpp", "// Synthetic packaging fixture, not a school solution.\nint main() { return 0; }\n")
        put("a/wyniki.log", "Synthetic evidence: 1.23\nFAILURE code=1\n")
    }
    const save = () => put("submission.json", JSON.stringify(manifest, null, 4) + "\n")
    const attest = () => {
        manifest.reviewedContentSha256 = contentDigest(
            manifest,
            manifest.artifacts.map((a) => ({
                path: a.path,
                bytes: readFileSync(a.shared ? join(root, "solutions", "general", a.path) : join(taskDir, a.path)),
            })),
        )
        save()
    }
    const execute = (options = {}) => bundle(task, { root, print: () => {}, ...options })
    const add = (artifact: Artifact, bytes: string | Buffer) => {
        manifest.artifacts.push(artifact)
        put(artifact.path, bytes)
    }
    save()
    return { root, taskDir, put, manifest, save, attest, execute, add }
}

const successful = (stdout = "", stderr = "") => ({ code: 0, stdout: Buffer.from(stdout), stderr: Buffer.from(stderr) })

async function docx(path: string, text = "Syntetyczny dokument") {
    const work = mkdtempSync(join(dirname(path), "docx-fixture-"))
    try {
        mkdirSync(join(work, "word"))
        writeFileSync(
            join(work, "word", "document.xml"),
            `<w:document xmlns:w="urn:fixture"><w:p><w:r><w:t>${text}</w:t></w:r></w:p></w:document>`,
        )
        writeFileSync(
            join(work, "[Content_Types].xml"),
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>',
        )
        expect((await runCommand("zip", ["-q", "-r", path, "word", "[Content_Types].xml"], work)).code).toBe(0)
    } finally {
        rmSync(work, { recursive: true, force: true })
    }
}

const mockExporter: Runner = async (command, args, cwd) => {
    if (command !== "pandoc") return runCommand(command, args, cwd)
    if (args.includes("--version")) return successful("pandoc synthetic test\n")
    const output = join(cwd, args[args.indexOf("-o") + 1])
    if (output.endsWith(".docx")) await docx(output)
    else
        writeFileSync(
            output,
            output.endsWith(".pdf")
                ? "%PDF-1.4\n% synthetic validation fixture\n%%EOF\n"
                : "<!doctype html><title>Test</title>",
        )
    return successful("", "Synthetic warning\n")
}

test("ZIP uses only reviewed whitelist and preserves raw bytes including failures", async () => {
    const f = fixture()
    f.add({ path: "a/stderr.log", role: "log", level: "a" }, "")
    f.put("unlisted-secret.txt", "never include this")
    f.put("build/app", "unlisted binary")
    f.put(".bundle/old.log", "unlisted diagnostics")
    mkdirSync(join(f.root, "solutions", "general"))
    writeFileSync(join(f.root, "solutions", "general", "environment.log"), "Synthetic public environment\n")
    f.manifest.artifacts.push({ path: "environment.log", role: "log", shared: "environment" })
    f.put("a/raport.md", report("TiDPI_02") + "\n[Środowisko](../environment.log)\n")
    f.attest()
    const checked = await f.execute({ check: true })
    expect(checked.errors).toEqual([])
    expect(existsSync(join(f.root, "submissions"))).toBe(false)
    const result = await f.execute()
    expect(result.errors).toEqual([])
    expect(result.ok).toBe(true)
    const list = await runCommand("unzip", ["-Z1", result.archive!], f.root)
    expect(list.stdout.toString()).not.toContain("unlisted")
    expect(list.stdout.toString()).not.toContain(".bundle")
    const raw = await runCommand("unzip", ["-p", result.archive!, "TiDPI_02_ALFA123/a/wyniki.log"], f.root)
    expect(raw.stdout).toEqual(readFileSync(join(f.taskDir, "a/wyniki.log")))
    expect(raw.stdout.toString()).toContain("FAILURE code=1")
})

test("review required, artifact and manifest mutations invalidate it", async () => {
    const f = fixture()
    const unreviewed = await f.execute()
    expect(unreviewed.digest).toHaveLength(64)
    expect(unreviewed.ok).toBe(false)
    expect(existsSync(join(f.root, "submissions"))).toBe(false)
    f.attest()
    f.put("a/wyniki.log", "changed synthetic evidence\n")
    expect((await f.execute({ check: true })).errors.join()).toContain("potwierdzenia")
    f.attest()
    f.manifest.artifacts[3].scenario = "changed-role"
    f.save()
    expect((await f.execute({ check: true })).ok).toBe(false)
    f.attest()
    expect((await f.execute({ check: true })).ok).toBe(true)
})

test("missing or empty task, unknown task and malformed manifests fail safely", async () => {
    const f = fixture()
    rmSync(join(f.taskDir, "submission.json"))
    expect((await f.execute()).ok).toBe(false)
    expect((await bundle("../TiDPI_02", { root: f.root, print: () => {} })).ok).toBe(false)
    for (const mutation of [
        { levels: ["b"] },
        { levels: ["a", "c"] },
        { extensions: undefined },
        { reviewedContentSha256: "bad" },
        { version: 2 },
        { codename: "TODO" },
        { surprisingField: true },
    ])
        expect(() => parseManifest({ ...f.manifest, ...mutation }, "TiDPI_02")).toThrow()
})

test.each([
    "../outside.txt",
    "/outside.txt",
    "build/file.txt",
    "pdfs/school.pdf",
    ".secret",
    "app.exe",
    "AGENTS.md",
    "a/CON",
    "a/file.zip",
    "a\\file.txt",
])("rejects unsafe artifact path %s", async (path) => {
    const f = fixture()
    f.manifest.artifacts.push({ path, role: "asset" })
    f.save()
    expect((await f.execute()).ok).toBe(false)
    expect(existsSync(join(f.root, "submissions"))).toBe(false)
})

test("rejects case collisions, missing source, logs and compiled magic", async () => {
    const f = fixture()
    f.add({ path: "A/MAIN.CPP", role: "source-cpp", level: "a" }, "// test")
    f.save()
    expect((await f.execute()).errors.join()).toContain("Kolizja")
    f.manifest.artifacts.pop()
    f.manifest.artifacts = f.manifest.artifacts.filter((a) => a.role !== "source-cpp")
    f.save()
    expect((await f.execute()).errors.join()).toContain("źródł")
    f.add({ path: "a/program", role: "source", level: "a" }, Buffer.from([0x7f, 0x45, 0x4c, 0x46, 0]))
    f.save()
    expect((await f.execute()).errors.join()).toContain("wykonywalny")
    rmSync(join(f.taskDir, "a/wyniki.log"))
    expect((await f.execute()).ok).toBe(false)
})

test.each(["leaf", "parent", "dangling", "task"])("rejects symlink %s", async (kind) => {
    const f = fixture()
    if (kind === "leaf" || kind === "dangling") {
        rmSync(join(f.taskDir, "a/wyniki.log"))
        symlinkSync(kind === "leaf" ? "main.cpp" : "nonexistent", join(f.taskDir, "a/wyniki.log"))
    } else if (kind === "parent") {
        const outside = join(f.root, "other")
        mkdirSync(outside)
        rmSync(join(f.taskDir, "a"), { recursive: true })
        symlinkSync(outside, join(f.taskDir, "a"))
    } else {
        const outside = join(f.root, "other")
        mkdirSync(outside)
        rmSync(f.taskDir, { recursive: true })
        symlinkSync(outside, f.taskDir)
    }
    expect((await f.execute()).ok).toBe(false)
})

test.each([
    ["heading", (s: string) => s.replace("## Procedura", "## Inny nagłówek")],
    ["date", (s: string) => s.replace("2026-09-28", "2026-99-99")],
    ["YAML", (s: string) => s.replace('title: "Syntetyczny raport walidatora"', "title: [broken")],
    ["placeholder", (s: string) => s + "\n{{ students_name }}"],
    ["link", (s: string) => s + "\n[Brak](missing.txt)"],
    ["escape", (s: string) => s + "\n[Brak](../../outside.txt)"],
    ["fence", (s: string) => s + "\n```text\nnot closed"],
    ["email", (s: string) => s + "\nprivate@example.org"],
    ["path", (s: string) => s + "\n/Users/private/Documents/file"],
] as const)("report validation rejects %s", async (_, mutate) => {
    const f = fixture()
    f.put("raport.md", mutate(report("TiDPI_02")))
    f.attest()
    const result = await f.execute({ check: true })
    expect(result.ok).toBe(false)
    expect(result.errors.length).toBeGreaterThan(0)
})

test("privacy checks logs, filenames, author identity, PDF and DOCX XML", async () => {
    const f = fixture()
    writeFileSync(join(f.root, "package.json"), JSON.stringify({ author: { name: "Private Identity" } }))
    f.put("a/wyniki.log", "Private Identity\n")
    f.add({ path: "name@example.org.txt", role: "evidence" }, "synthetic")
    f.add({ path: "raport.pdf", role: "export-pdf" }, "%PDF-1.4\n/Users/private/file\n%%EOF\n")
    f.manifest.artifacts.push({ path: "raport.docx", role: "export-docx" })
    await docx(join(f.taskDir, "raport.docx"), "private@example.org")
    f.attest()
    const result = await f.execute({ check: true })
    expect(result.errors.join()).toContain("autora repozytorium")
    expect(result.errors.join()).toContain("prywatną ścieżkę")
    expect(result.errors.some((e) => e.startsWith("raport.docx:") && e.includes("e-mail"))).toBe(true)
})

test("renamed school PDF is rejected and malformed existing exports never overwritten", async () => {
    const f = fixture()
    mkdirSync(join(f.root, "pdfs"))
    const pdf = "%PDF-1.4\nschool fixture\n%%EOF\n"
    writeFileSync(join(f.root, "pdfs", "original.pdf"), pdf)
    f.add({ path: "renamed.pdf", role: "evidence" }, pdf)
    f.add({ path: "raport.pdf", role: "export-pdf" }, "broken PDF")
    f.attest()
    const result = await f.execute()
    expect(result.errors.join()).toContain("szkolnego")
    expect(result.errors.join()).toContain("niepełny PDF")
    expect(readFileSync(join(f.taskDir, "raport.pdf"), "utf8")).toBe("broken PDF")
})

test("check never creates exports or diagnostics", async () => {
    const f = fixture("TiDPI_01")
    let calls = 0
    const run: Runner = async () => {
        calls++
        return successful()
    }
    const result = await f.execute({ check: true, run })
    expect(result.ok).toBe(false)
    expect(calls).toBe(0)
    expect(existsSync(join(f.taskDir, ".bundle"))).toBe(false)
    expect(existsSync(join(f.taskDir, "raport.pdf"))).toBe(false)
})

test("generate missing exports, preserve diagnostics, require review, reuse without Pandoc", async () => {
    const f = fixture("TiDPI_01")
    const generated = await f.execute({ run: mockExporter })
    expect(generated.errors.filter((e) => !e.includes("potwierdzenia"))).toEqual([])
    expect(generated.digest).toHaveLength(64)
    expect(generated.ok).toBe(false)
    expect(existsSync(join(f.taskDir, "raport.docx"))).toBe(true)
    expect(existsSync(join(f.taskDir, "raport.pdf"))).toBe(true)
    expect(existsSync(join(f.root, "submissions"))).toBe(false)
    const work = readdirSync(join(f.taskDir, ".bundle"))[0]
    expect(readFileSync(join(f.taskDir, ".bundle", work, "logs", "raport.pdf_stderr.txt"), "utf8")).toBe(
        "Synthetic warning\n",
    )
    f.attest()
    const run: Runner = (command, args, cwd) => {
        if (command === "pandoc") throw new Error("Must not overwrite existing exports")
        return runCommand(command, args, cwd)
    }
    expect((await f.execute({ run })).ok).toBe(true)
})

test.each(["exit", "timeout", "missing-output"])(
    "failed export %s retains streams and publishes no ZIP",
    async (mode) => {
        const f = fixture("TiDPI_01")
        const run: Runner = async (command, args, cwd) => {
            if (command !== "pandoc") return runCommand(command, args, cwd)
            if (args.includes("--version")) return successful("pandoc fixture")
            return {
                code: mode === "missing-output" ? 0 : mode === "timeout" ? 124 : 2,
                stdout: Buffer.from("raw dots: 1.23\n"),
                stderr: Buffer.from("raw failure\n"),
                timedOut: mode === "timeout",
            }
        }
        const result = await f.execute({ run })
        expect(result.ok).toBe(false)
        expect(existsSync(join(f.root, "submissions"))).toBe(false)
        const work = readdirSync(join(f.taskDir, ".bundle"))[0]
        expect(readFileSync(join(f.taskDir, ".bundle", work, "logs", "raport.docx_stdout.txt"), "utf8")).toBe(
            "raw dots: 1.23\n",
        )
        expect(
            JSON.parse(readFileSync(join(f.taskDir, ".bundle", work, "logs", "raport.docx_status.json"), "utf8"))
                .timedOut,
        ).toBe(mode === "timeout")
    },
)

test("HTML route generates HTML then requires manually prepared PDF", async () => {
    const f = fixture("TiDPI_01")
    f.manifest.pdfRoute = "html"
    f.manifest.artifacts.push({ path: "raport.html", role: "export-html" })
    f.save()
    const result = await f.execute({ run: mockExporter })
    expect(result.ok).toBe(false)
    expect(result.errors.join()).toContain("wydrukuj")
    expect(existsSync(join(f.taskDir, "raport.html"))).toBe(true)
    expect(existsSync(join(f.taskDir, "raport.pdf"))).toBe(false)
})

test("existing ZIP needs force; corrupt staged ZIP cannot replace it", async () => {
    const f = fixture()
    f.attest()
    const first = await f.execute()
    expect(first.ok).toBe(true)
    const original = readFileSync(first.archive!)
    expect((await f.execute()).errors.join()).toContain("--force")
    f.put("a/wyniki.log", "changed synthetic log\n")
    f.attest()
    const broken: Runner = async (command, args, cwd) => {
        if (command === "zip") {
            writeFileSync(join(cwd, "archive.zip"), "not a ZIP")
            return successful()
        }
        return runCommand(command, args, cwd)
    }
    expect((await f.execute({ force: true, run: broken })).ok).toBe(false)
    expect(readFileSync(first.archive!)).toEqual(original)
    expect((await f.execute({ force: true })).ok).toBe(true)
    expect(readFileSync(first.archive!)).not.toEqual(original)
    expect(readdirSync(join(f.root, "submissions"))).toEqual(["TiDPI_02_ALFA123.zip"])
})

test("source mutation during packaging fails without publishing ZIP", async () => {
    const f = fixture()
    f.attest()
    const run: Runner = async (command, args, cwd) => {
        const result = await runCommand(command, args, cwd)
        if (command === "zip") f.put("a/main.cpp", "// changed during zip\n")
        return result
    }
    expect((await f.execute({ run })).errors.join()).toContain("podczas pakowania")
    expect(readdirSync(join(f.root, "submissions"))).toEqual([])
})

test.each(["TiDPI_05", "TiDPI_06", "TiDPI_07"])("task-specific roles/scenarios required for %s", async (task) => {
    const f = fixture(task)
    f.manifest.levels.push("b")
    f.save()
    const result = await f.execute({ check: true })
    expect(result.ok).toBe(false)
    expect(result.errors.join()).toContain("scenario")
    expect(result.errors.join()).toContain(task)
})

test("extensions enforce selection and evidence coverage", async () => {
    const f = fixture("TiDPI_03")
    f.manifest.levels.push("b", "c", "d")
    f.manifest.extensions.push({ id: "allocation", level: "c", evidenceIds: ["D09"] })
    f.save()
    const result = await f.execute({ check: true })
    expect(result.errors.join()).toContain("dwóch")
    expect(result.errors.join()).toContain("D09")
    expect(result.errors.join()).toContain("własnego badania")
    expect(result.errors.join()).toContain("wykresu")
    expect(() =>
        parseManifest({ ...f.manifest, extensions: [{ id: "wrong", level: "c", evidenceIds: ["D01"] }] }, "TiDPI_03"),
    ).toThrow()
})

test.each(["TiDPI_05", "TiDPI_06", "TiDPI_07"])("complete synthetic A/B handoff passes for %s", async (task) => {
    const f = fixture(task)
    f.manifest.levels.push("b")
    f.add({ path: "b/raport.md", role: "level-report", level: "b" }, report(task))
    f.add({ path: "b/main.cpp", role: "source-cpp", level: "b" }, "// synthetic source\n")
    f.add({ path: "b/raw.log", role: "raw-results", level: "b", evidenceId: "D01" }, "synthetic evidence\n")
    const scenarios =
        task === "TiDPI_05"
            ? ["manual", "pass-1", "pass-2", "run-failure", "compile-failure", "restored"]
            : task === "TiDPI_06"
              ? [
                    "pass",
                    "invalid-number",
                    "missing-field",
                    "duplicate-row",
                    "wrong-version",
                    "failed-test",
                    "stale-csv",
                ]
              : ["run-1", "invalid", "run-2"]
    for (const scenario of scenarios)
        f.add(
            { path: `b/${scenario}.log`, role: "log", level: "b", evidenceId: "D01", scenario },
            "synthetic fixture, no school result\n",
        )
    if (task !== "TiDPI_06") f.add({ path: "a/automation.py", role: "automation", level: "a" }, "# synthetic fixture\n")
    if (task !== "TiDPI_05") f.add({ path: "a/results.csv", role: "csv", level: "a" }, "synthetic;fixture\n")
    if (task === "TiDPI_06") f.add({ path: "a/parser.py", role: "parser", level: "a" }, "# synthetic fixture\n")
    if (task === "TiDPI_07") {
        f.add({ path: "a/main.py", role: "source-python", level: "a" }, "# synthetic fixture\n")
        f.add({ path: "a/generator.py", role: "generator", level: "a" }, "# synthetic fixture\n")
        f.add({ path: "a/reproduce.md", role: "reproduction", level: "a" }, "Synthetic input reproduction fixture.\n")
        f.add({ path: "raport.pdf", role: "export-pdf" }, "%PDF-1.4\n% synthetic validation fixture\n%%EOF\n")
    }
    f.attest()
    const result = await f.execute()
    expect(result.errors).toEqual([])
    expect(result.ok).toBe(true)
})

test("Unicode codename and filenames survive ZIP verification", async () => {
    const f = fixture()
    f.manifest.codename = "ŻÓŁW123"
    for (const path of ["raport.md", "a/raport.md"])
        f.put(path, report("TiDPI_02").replace("ALFA123", f.manifest.codename))
    f.add({ path: "a/załącznik z danymi.txt", role: "evidence", level: "a", evidenceId: "D01" }, "Synthetic data\n")
    f.attest()
    const result = await f.execute()
    expect(result.errors).toEqual([])
    expect(result.ok).toBe(true)
    const bytes = readFileSync(result.archive!)
    const central = bytes.indexOf(Buffer.from([0x50, 0x4b, 0x01, 0x02]))
    expect(bytes.readUInt16LE(6) & 0x0800).toBe(0x0800)
    expect(bytes.readUInt16LE(central + 8) & 0x0800).toBe(0x0800)
})

test("unexpected ZIP directory entries fail before extraction", async () => {
    const f = fixture()
    f.attest()
    let extracted = false
    const run: Runner = async (command, args, cwd) => {
        if (command === "unzip" && args.includes("-d")) extracted = true
        const result = await runCommand(command, args, cwd)
        if (command === "zip") {
            const path = join(cwd, "archive.zip")
            const bytes = readFileSync(path)
            const original = Buffer.from("TiDPI_02_ALFA123/a/")
            for (
                let offset = bytes.indexOf(original);
                offset >= 0;
                offset = bytes.indexOf(original, offset + original.length)
            )
                Buffer.from("TiDPI_02_ALFA123/./").copy(bytes, offset)
            writeFileSync(path, bytes)
        }
        return result
    }
    expect((await f.execute({ run })).ok).toBe(false)
    expect(extracted).toBe(false)
})

test.skipIf(process.env.BUNDLE_INTEGRATION !== "1")(
    "real Pandoc/XeLaTeX produces checked exports and a verified ZIP",
    async () => {
        const f = fixture("TiDPI_01")
        const result = await f.execute()
        expect(result.errors.filter((e) => !e.includes("potwierdzenia"))).toEqual([])
        expect(result.digest).toHaveLength(64)
        expect(readFileSync(join(f.taskDir, "raport.pdf")).subarray(0, 5).toString()).toBe("%PDF-")
        f.attest()
        expect((await f.execute()).ok).toBe(true)
    },
    120_000,
)

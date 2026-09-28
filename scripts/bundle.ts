import { YAML } from "bun"
import { createHash } from "node:crypto"
import { spawn } from "node:child_process"
import {
    constants,
    existsSync,
    lstatSync,
    mkdirSync,
    mkdtempSync,
    readFileSync,
    readdirSync,
    realpathSync,
    renameSync,
    linkSync,
    rmSync,
    writeFileSync,
    accessSync,
} from "node:fs"
import { basename, dirname, extname, join, relative, resolve } from "node:path"
import { userInfo } from "node:os"
import { fileURLToPath } from "node:url"

export const sections = [
    "Kryptonim TiDPI i wykonany poziom",
    "Cel i hipoteza",
    "Środowisko oraz konfiguracja",
    "Zmienne i warunki eksperymentu",
    "Kontrola poprawności",
    "Procedura",
    "Surowe wyniki",
    "Opracowanie wyników",
    "Interpretacja",
    "Ograniczenia eksperymentu",
    "Wnioski",
    "Wykorzystanie AI i sposób weryfikacji",
] as const

const roles = [
    "report", "level-report", "source-cpp", "source-python", "source", "raw-results", "log", "input",
    "generator", "reproduction", "automation", "parser", "csv", "chart", "evidence", "asset",
    "export-docx", "export-pdf", "export-html", "docx-reference",
] as const
type Role = (typeof roles)[number]
type Level = "a" | "b" | "c" | "d"
export interface Artifact {
    path: string
    role: Role
    level?: Level
    evidenceId?: string
    scenario?: string
    shared?: "environment"
}
interface Extension {
    id: string
    level: "c" | "d" | "r"
    evidenceIds: string[]
}
export interface Manifest {
    version: 1
    task: string
    codename: string
    levels: Level[]
    stages?: number[]
    extensions: Extension[]
    artifacts: Artifact[]
    pdfRoute?: "xelatex" | "html"
    reviewedContentSha256: string | null
}
export interface CommandResult {
    code: number
    stdout: Buffer
    stderr: Buffer
    timedOut?: boolean
}
export type Runner = (command: string, args: string[], cwd: string) => Promise<CommandResult>
interface Snapshot {
    path: string
    source: string
    bytes: Buffer
    artifact?: Artifact
}
export interface Options {
    root?: string
    check?: boolean
    force?: boolean
    run?: Runner
    print?: (message: string) => void
}
export interface Result {
    ok: boolean
    errors: string[]
    digest?: string
    archive?: string
    files: string[]
}

const scriptRoot = fileURLToPath(new URL("..", import.meta.url))
const forbiddenDirectories = new Set([
    "pdfs", "node_modules", "build", "_build", "dist", "out", "submissions", "__pycache__",
])
const forbiddenExtensions = new Set([
    ".exe", ".dll", ".so", ".dylib", ".o", ".obj", ".pdb", ".ilk", ".a", ".lib", ".pyc", ".zip", ".7z", ".rar", ".ini",
])
const textExtensions = new Set([
    ".md", ".txt", ".log", ".csv", ".tsv", ".json", ".yaml", ".yml", ".xml", ".svg", ".html", ".htm",
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx", ".py", ".ts", ".js", ".sh", ".ps1", ".toml",
])
const sourceRoles: Role[] = ["source-cpp", "source-python", "source", "generator", "automation", "parser"]
const evidenceRoles: Role[] = ["raw-results", "log", "evidence", "chart", "csv", "input", "reproduction"]
const exportsByRole: Partial<Record<Role, string>> = {
    "export-docx": "raport.docx", "export-pdf": "raport.pdf", "export-html": "raport.html",
}
const cOptions: Record<string, string[]> = {
    TiDPI_03: ["allocation", "stack-limit", "x86-x64"],
    TiDPI_04: ["seeds", "early-exit", "almost-sorted"],
    TiDPI_05: ["repeat", "size", "file-manifest"],
    TiDPI_06: ["seed-v2", "completeness", "csv-escaping"],
    TiDPI_07: ["debug-release", "sizes", "warmup", "library", "rounds"],
}

export const sha256 = (bytes: Buffer | string): string => createHash("sha256").update(bytes).digest("hex")
const fail = (message: string): never => { throw new Error(message) }
const object = (value: unknown): value is Record<string, unknown> =>
    typeof value === "object" && value !== null && !Array.isArray(value)

function keys(value: Record<string, unknown>, allowed: string[], label: string): void {
    for (const key of Object.keys(value)) if (!allowed.includes(key)) fail(`${label}: nieznane pole ${key}.`)
}

/** Parse the explicit submission contract; never infer completed work from filenames. */
export function parseManifest(input: unknown, task: string): Manifest {
    if (!object(input)) fail("submission.json musi zawierać obiekt.")
    keys(input, ["version", "task", "codename", "levels", "stages", "extensions", "artifacts", "pdfRoute", "reviewedContentSha256"], "Manifest")
    if (input.version !== 1 || input.task !== task) fail("Manifest: wymagana wersja 1 i zgodny identyfikator zadania.")
    if (typeof input.codename !== "string" || !/^[\p{L}\p{N}][\p{L}\p{N}_-]{0,79}$/u.test(input.codename))
        fail("Kryptonim: użyj liter, cyfr, myślnika lub podkreślenia (maksymalnie 80 znaków).")
    if (/^(?:KRYPTONIM_TIDPI|TEST|EXAMPLE|TODO)$/i.test(input.codename)) fail("Zastąp przykładowy kryptonim przydzielonym kryptonimem.")
    if (!Array.isArray(input.levels)) fail("Manifest: levels musi być tablicą.")
    const levels = ["a", "b", "c", "d"]
    if (task === "TiDPI_01") {
        if (input.levels.length || JSON.stringify(input.stages) !== "[1,2,3]") fail("TiDPI_01 wymaga stages: [1, 2, 3] i levels: [].")
    } else if (!input.levels.length || input.levels.length > 4 || input.levels.some((v, i) => v !== levels[i]) || input.stages !== undefined) {
        fail("Poziomy muszą być ciągiem a–d zaczynającym się od a; stages dotyczy tylko TiDPI_01.")
    }
    if (input.pdfRoute !== undefined && !["xelatex", "html"].includes(String(input.pdfRoute))) fail("Nieznane pdfRoute.")
    if (input.reviewedContentSha256 !== null && (typeof input.reviewedContentSha256 !== "string" || !/^[a-f0-9]{64}$/.test(input.reviewedContentSha256)))
        fail("reviewedContentSha256 musi być null lub skrótem SHA-256.")
    if (!Array.isArray(input.artifacts) || !input.artifacts.length) fail("Manifest wymaga niepustej listy artifacts.")
    for (const value of input.artifacts) {
        if (!object(value)) fail("Artefakt musi być obiektem.")
        keys(value, ["path", "role", "level", "evidenceId", "scenario", "shared"], "Artefakt")
        if (typeof value.path !== "string" || !roles.includes(value.role as Role)) fail("Artefakt wymaga path oraz obsługiwanej role.")
        if (value.level !== undefined && !input.levels.includes(value.level)) fail("Artefakt przypisano do nieukończonego poziomu.")
        if (value.evidenceId !== undefined && (typeof value.evidenceId !== "string" || !/^D\d{2,}$/.test(value.evidenceId))) fail("evidenceId ma postać D01, D02…")
        if (value.scenario !== undefined && (typeof value.scenario !== "string" || !/^[a-z0-9-]+$/.test(value.scenario))) fail("Niepoprawny identyfikator scenario.")
        if (value.shared !== undefined && (value.shared !== "environment" || value.path !== "environment.log" || value.role !== "log" || value.level !== undefined || value.scenario !== undefined))
            fail("Jedyny współdzielony artefakt to environment.log o roli log, bez level/scenario.")
        if (value.path === "submission.json") fail("submission.json jest dołączany automatycznie.")
    }
    if (!Array.isArray(input.extensions)) fail("extensions musi być tablicą (również gdy jest pusta).")
    const extensionIds = new Set<string>()
    for (const value of input.extensions) {
        if (!object(value)) fail("Rozszerzenie musi być obiektem.")
        keys(value, ["id", "level", "evidenceIds"], "Rozszerzenie")
        if (typeof value.id !== "string" || !/^[A-Za-z0-9-]+$/.test(value.id) || extensionIds.has(value.id)) fail("Rozszerzenia wymagają różnych identyfikatorów.")
        extensionIds.add(value.id)
        if (!["c", "d", "r"].includes(String(value.level))) fail("Rozszerzenie: level to c, d lub r.")
        if (task === "TiDPI_01") {
            if (value.level !== "r" || !/^R[1-5]$/.test(value.id)) fail("TiDPI_01 obsługuje rozszerzenia R1–R5 o level: r.")
        } else {
            if (!input.levels.includes(value.level) || value.level === "r") fail("Rozszerzenie musi należeć do ukończonego c lub d.")
            if (value.level === "c" && !(cOptions[task] ?? []).includes(value.id)) fail(`Nieznane rozszerzenie C: ${value.id}.`)
        }
        if (!Array.isArray(value.evidenceIds) || !value.evidenceIds.length || value.evidenceIds.some(id => typeof id !== "string" || !/^D\d{2,}$/.test(id)) || new Set(value.evidenceIds).size !== value.evidenceIds.length)
            fail("Rozszerzenie wymaga niepustej listy różnych evidenceIds.")
    }
    return input as unknown as Manifest
}

/** Canonical relative names also keep zip entries portable across filesystems. */
function safePath(path: string): void {
    const parts = path.split("/")
    if (!path || path !== path.normalize("NFC") || path.includes("\\") || /[\x00-\x1f\x7f:*?"<>|]/.test(path) || parts.some(p => !p || p === "." || p === ".." || /[. ]$/.test(p) || p.startsWith(".") || forbiddenDirectories.has(p.toLowerCase()) || /^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)/i.test(p)))
        fail(`Niedozwolona nazwa lub ścieżka: ${path}.`)
    if (forbiddenExtensions.has(extname(path).toLowerCase()) || /^(?:BASE_RAPORT|AGENTS|CLAUDE)\.md$/i.test(basename(path))) fail(`Plik nie należy do paczki: ${path}.`)
}

/** Check every component, including a missing export's parent, without following symlinks. */
function confined(root: string, path: string, missing = false): string {
    safePath(path)
    let current = root
    if (!existsSync(root) || lstatSync(root).isSymbolicLink() || !lstatSync(root).isDirectory()) fail("Niepoprawny lub dowiązany katalog zadania.")
    const parts = path.split("/")
    for (const [i, part] of parts.entries()) {
        current = join(current, part)
        if (!existsSync(current)) {
            // lstat, unlike exists, detects dangling symlinks.
            try { if (lstatSync(current).isSymbolicLink()) fail(`Dowiązanie jest niedozwolone: ${path}.`) } catch (error) {
                if (!(object(error) && error.code === "ENOENT")) throw error
            }
            if (missing && i === parts.length - 1) return current
            fail(`Brak pliku lub katalogu: ${path}.`)
        }
        const stat = lstatSync(current)
        if (stat.isSymbolicLink() || (i < parts.length - 1 ? !stat.isDirectory() : !stat.isFile())) fail(`Dowiązanie lub niepoprawny typ pliku: ${path}.`)
    }
    return current
}

/** Run tools directly, preserve both streams, and stop the process group at the deadline. */
export const runCommand: Runner = (command, args, cwd) => new Promise((resolveResult, reject) => {
    const child = spawn(command, args, { cwd, shell: false, detached: process.platform !== "win32", env: { ...process.env, COPYFILE_DISABLE: "1" } })
    const stdout: Buffer[] = [], stderr: Buffer[] = []
    let timedOut = false
    const timer = setTimeout(() => {
        timedOut = true
        try { if (process.platform !== "win32" && child.pid) process.kill(-child.pid, "SIGKILL"); else child.kill("SIGKILL") } catch { /* The process may already have exited. */ }
    }, 120_000)
    child.stdout.on("data", chunk => stdout.push(Buffer.from(chunk)))
    child.stderr.on("data", chunk => stderr.push(Buffer.from(chunk)))
    child.once("error", error => { clearTimeout(timer); reject(error) })
    child.once("close", code => {
        clearTimeout(timer)
        resolveResult({ code: timedOut ? 124 : code ?? 1, stdout: Buffer.concat(stdout), stderr: Buffer.concat(stderr), timedOut })
    })
})

function available(command: string): boolean {
    return (process.env.PATH ?? "").split(process.platform === "win32" ? ";" : ":").some(dir => {
        try { accessSync(join(dir, command), constants.X_OK); return true } catch { return false }
    })
}

function identities(root: string): string[] {
    const result = [userInfo().username]
    if (existsSync(join(root, "package.json"))) {
        const pkg = JSON.parse(readFileSync(join(root, "package.json"), "utf8"))
        const name = typeof pkg.author === "object" ? pkg.author?.name : pkg.author
        if (typeof name === "string") result.push(name, ...name.split(/[()]/).map(s => s.trim()))
    }
    return result.filter(s => s.length >= 3).map(s => s.normalize("NFC").toLocaleLowerCase())
}

function privacy(text: string, path: string, names: string[]): string[] {
    const errors: string[] = []
    if (/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i.test(text)) errors.push(`${path}: znaleziono adres e-mail.`)
    if (/(?:\/(?:Users|home)\/[^\s/]+|[A-Z]:[\\/]Users[\\/][^\s\\/]+|file:\/\/|~\/)/i.test(text)) errors.push(`${path}: znaleziono prywatną ścieżkę.`)
    const normalized = text.normalize("NFC").toLocaleLowerCase()
    if (names.some(name => new RegExp(`(?<![\\p{L}\\p{N}_])${name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?![\\p{L}\\p{N}_])`, "u").test(normalized)))
        errors.push(`${path}: znaleziono nazwę konta lub dane autora repozytorium.`)
    return errors
}

function outsideCode(text: string): string {
    let fence: { char: string, length: number } | undefined
    const body = text.split(/\r?\n/).map(line => {
        const match = /^ {0,3}(`{3,}|~{3,})/.exec(line)
        if (!fence && match) { fence = { char: match[1][0], length: match[1].length }; return "" }
        if (fence) {
            if (new RegExp(`^ {0,3}${fence.char}{${fence.length},}\\s*$`).test(line)) fence = undefined
            return ""
        }
        return line
    }).join("\n")
    if (fence) fail("Raport zawiera niezamknięty blok kodu.")
    return body
}

function markdownLinks(text: string): string[] {
    const body = outsideCode(text)
    const links: string[] = []
    for (const match of body.matchAll(/!?\[[^\]\n]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+["'][^\n]*?["'])?\s*\)/g)) links.push(match[1] ?? match[2])
    for (const match of body.matchAll(/^ {0,3}\[[^\]\n]+\]:\s*(?:<([^>]+)>|([^\s]+))/gm)) links.push(match[1] ?? match[2])
    for (const match of body.matchAll(/\b(?:src|href)\s*=\s*["']([^"']+)["']/gi)) links.push(match[1])
    return links
}

function validateReport(file: Snapshot, manifest: Manifest, names: string[], paths: Set<string>): string[] {
    const text = file.bytes.toString("utf8")
    const errors = privacy(text, file.path, names)
    const frontmatter = /^\uFEFF?---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(text)
    let metadata: unknown
    try { if (frontmatter) metadata = YAML.parse(frontmatter[1]) } catch { errors.push(`${file.path}: niepoprawny YAML.`) }
    const date = object(metadata) && typeof metadata.date === "string" ? metadata.date : ""
    const parsedDate = new Date(date)
    if (!object(metadata) || typeof metadata.title !== "string" || !metadata.title.trim() || metadata.author !== `Kryptonim TiDPI: ${manifest.codename}` || metadata.lang !== "pl-PL" || !/^\d{4}-\d{2}-\d{2}$/.test(date) || !Number.isFinite(parsedDate.getTime()) || parsedDate.toISOString().slice(0, 10) !== date)
        errors.push(`${file.path}: wymagane title, author z kryptonimem, rzeczywista data YYYY-MM-DD i lang: pl-PL.`)
    const body = outsideCode(text.slice(frontmatter?.[0].length ?? 0))
    if ([...body.matchAll(/^#\s+.+$/gm)].length !== 1) errors.push(`${file.path}: wymagany dokładnie jeden nagłówek główny.`)
    const headings = [...body.matchAll(/^##\s+(.+?)\s*#*\s*$/gm)].map(m => m[1])
    if (JSON.stringify(headings) !== JSON.stringify(sections)) errors.push(`${file.path}: wymagane dwanaście sekcji w kolejności z BASE_RAPORT.md.`)
    if (/\{\{[^}]+\}\}|\b(?:YYYY-MM-DD|RRRR-MM-DD|KRYPTONIM_TIDPI|TODO|TBD)\b|\[(?:uzupełnij|wpisz|Dxx|z logu|oblicz|przydzielony kryptonim|NN[,\]])[^\]]*\]/i.test(text)) errors.push(`${file.path}: pozostawiono znacznik szablonu.`)
    if (manifest.task === "TiDPI_01" && file.artifact?.role === "report") {
        if (!/fikcyjn/i.test(text)) errors.push("TiDPI_01: raport musi jawnie oznaczać fikcyjne dane.")
        for (let i = 1; i <= 6; i++) if (!text.includes(`TC-0${i}`)) errors.push(`TiDPI_01: brak TC-0${i} w raporcie.`)
    }
    for (const id of new Set(manifest.artifacts.map(a => a.evidenceId).filter(Boolean))) {
        if (file.artifact?.role === "report" && !text.includes(id!)) errors.push(`${file.path}: brak odwołania do ${id}.`)
    }
    for (const link of markdownLinks(text)) {
        if (/^(?:https?:|mailto:)/i.test(link) || link.startsWith("#")) continue
        if (/^[a-z][a-z0-9+.-]*:/i.test(link) || link.startsWith("/")) { errors.push(`${file.path}: niedozwolone odwołanie lokalne.`); continue }
        try {
            const target = decodeURIComponent(link.split(/[?#]/)[0])
            const resolved = relative("/", resolve("/", dirname(file.path), target)).replaceAll("\\", "/")
            // Normalization alone would turn an escaping reference into an apparently safe name.
            if (resolve("/bundle", dirname(file.path), target) !== resolve("/bundle", resolved) || !paths.has(resolved)) errors.push(`${file.path}: odwołanie nie trafi do paczki: ${link}.`)
        } catch { errors.push(`${file.path}: niepoprawne odwołanie: ${link}.`) }
    }
    return errors
}

/** Check declared roles and evidence coverage; human review still checks experimental meaning. */
function requirements(manifest: Manifest): string[] {
    const errors: string[] = []
    const artifacts = manifest.artifacts
    const need = (condition: boolean, message: string) => { if (!condition) errors.push(message) }
    const has = (role: Role, level?: Level) => artifacts.some(a => a.role === role && (level === undefined || a.level === level))
    const scenario = (id: string) => artifacts.some(a => a.scenario === id && a.evidenceId && evidenceRoles.includes(a.role))
    need(artifacts.filter(a => a.role === "report").length === 1 && artifacts.some(a => a.role === "report" && a.path === "raport.md" && !a.level), "Wymagany jeden główny raport.md o roli report.")
    for (const a of artifacts) {
        if (exportsByRole[a.role]) need(a.path === exportsByRole[a.role] && !a.level && !a.shared, `Eksport ${a.role} musi mieć nazwę ${exportsByRole[a.role]} i dotyczyć raportu głównego.`)
        if (a.role === "source-cpp") need(/\.(c|cc|cpp|cxx|h|hh|hpp|hxx)$/i.test(a.path), `Niepoprawne źródło C++: ${a.path}.`)
        if (a.role === "source-python") need(/\.py$/i.test(a.path), `Niepoprawne źródło Python: ${a.path}.`)
        if (["report", "level-report", "reproduction"].includes(a.role)) need(/\.md$/i.test(a.path), `Rola ${a.role} wymaga pliku Markdown.`)
        if (a.role === "csv") need(/\.csv$/i.test(a.path), "Rola csv wymaga rozszerzenia .csv.")
        if (a.role === "docx-reference") need(/\.docx$/i.test(a.path), "Rola docx-reference wymaga .docx.")
    }
    need(artifacts.filter(a => a.role === "docx-reference").length <= 1, "Można wskazać najwyżej jeden referencyjny DOCX.")
    for (const level of manifest.levels) {
        need(artifacts.some(a => a.role === "level-report" && a.level === level && a.path === `${level}/raport.md`), `Poziom ${level}: brak ${level}/raport.md.`)
        need(artifacts.some(a => a.level === level && sourceRoles.includes(a.role)), `Poziom ${level}: brak źródła.`)
        if (["TiDPI_02", "TiDPI_03", "TiDPI_04"].includes(manifest.task)) need(has("source-cpp", level), `Poziom ${level}: wymagane źródło C++.`)
        need(artifacts.some(a => a.level === level && ["raw-results", "log"].includes(a.role) && a.evidenceId), `Poziom ${level}: brak surowego logu/wyników z evidenceId.`)
        for (const a of artifacts.filter(a => a.level === level)) need(a.path.startsWith(`${level}/`), `Poziom ${level}: artefakt musi znajdować się w ${level}/.`)
    }
    const ids = new Set(artifacts.filter(a => a.evidenceId && evidenceRoles.includes(a.role)).map(a => a.evidenceId))
    for (const extension of manifest.extensions) {
        for (const id of extension.evidenceIds) need(ids.has(id), `Rozszerzenie ${extension.id}: brak artefaktu dowodowego ${id}.`)
        if (extension.level !== "r") for (const id of extension.evidenceIds) need(artifacts.some(a => a.evidenceId === id && a.level === extension.level && evidenceRoles.includes(a.role)), `Rozszerzenie ${extension.id}: dowód ${id} musi należeć do poziomu ${extension.level}.`)
    }
    if (manifest.levels.includes("c") && cOptions[manifest.task]) need(manifest.extensions.filter(e => e.level === "c").length >= 2, "Poziom C wymaga dwóch udokumentowanych rozszerzeń.")
    if (manifest.levels.includes("d")) need(manifest.extensions.some(e => e.level === "d"), "Poziom D wymaga udokumentowanego własnego badania.")
    if ((manifest.task === "TiDPI_02" && manifest.levels.includes("c")) || (["TiDPI_03", "TiDPI_04"].includes(manifest.task) && manifest.levels.includes("b")))
        need(has("chart", manifest.task === "TiDPI_02" ? "c" : "b"), "Wybrany zakres wymaga wykresu.")
    if (manifest.task === "TiDPI_01") {
        need(has("raw-results") && artifacts.some(a => a.role === "raw-results" && a.evidenceId), "TiDPI_01: brak surowego fikcyjnego logu z evidenceId.")
        need(has("export-docx") && has("export-pdf"), "TiDPI_01: wymagane deklaracje eksportów DOCX i PDF.")
        const extensionRoles: Record<string, Role[]> = { R1: ["docx-reference", "evidence"], R2: ["source", "log"], R3: ["source-python", "evidence", "log"], R4: ["source-python", "log"], R5: ["evidence"] }
        for (const extension of manifest.extensions) for (const role of extensionRoles[extension.id]) need(has(role), `${extension.id}: brak roli ${role}.`)
    }
    if (manifest.pdfRoute === "html") need(has("export-pdf") && has("export-html"), "Trasa HTML wymaga eksportów HTML i ręcznie przygotowanego PDF.")
    if (manifest.task === "TiDPI_05") {
        need(has("source-cpp") && has("automation"), "TiDPI_05: wymagane źródło C++ i automat.")
        for (const id of ["manual", "pass-1", "pass-2", ...(manifest.levels.includes("b") ? ["run-failure", "compile-failure", "restored"] : [])]) need(scenario(id), `TiDPI_05: brak dowodu scenario: ${id}.`)
    }
    if (manifest.task === "TiDPI_06") {
        need(has("source-cpp") && has("parser") && has("csv") && has("raw-results"), "TiDPI_06: wymagane źródło C++, parser, CSV i surowe wyniki.")
        for (const id of ["pass", ...(manifest.levels.includes("b") ? ["invalid-number", "missing-field", "duplicate-row", "wrong-version", "failed-test", "stale-csv"] : [])]) need(scenario(id), `TiDPI_06: brak dowodu scenario: ${id}.`)
        if (manifest.levels.includes("d")) need(new Set(artifacts.filter(a => a.level === "d" && a.scenario && a.evidenceId && evidenceRoles.includes(a.role)).map(a => a.scenario)).size >= 10, "TiDPI_06 D: wymagane dowody co najmniej dziesięciu różnych fixture/scenario.")
    }
    if (manifest.task === "TiDPI_07") {
        for (const role of ["source-cpp", "source-python", "generator", "automation", "raw-results", "csv", "log"] as Role[]) need(has(role), `TiDPI_07: brak roli ${role}.`)
        need(has("input") || has("reproduction"), "TiDPI_07: brak wspólnych danych lub instrukcji ich odtworzenia.")
        need(has("export-docx") || has("export-pdf"), "TiDPI_07: wymagany eksport DOCX lub PDF.")
        need(artifacts.filter(a => a.role === "raw-results").length >= 2, "TiDPI_07: wymagane oddzielne surowe wyniki obu implementacji.")
        for (const id of ["run-1", ...(manifest.levels.includes("b") ? ["invalid", "run-2"] : [])]) need(scenario(id), `TiDPI_07: brak dowodu scenario: ${id}.`)
    }
    return errors
}

function collect(root: string, taskDir: string, manifest: Manifest, allowMissing: boolean): { files: Snapshot[], missing: Artifact[], errors: string[] } {
    const files: Snapshot[] = [], missing: Artifact[] = [], errors: string[] = []
    const names = new Set<string>(["submission.json"])
    for (const artifact of manifest.artifacts) {
        try {
            const normalized = artifact.path.normalize("NFC").toLocaleLowerCase()
            if (names.has(normalized)) fail(`Kolizja nazw: ${artifact.path}.`)
            names.add(normalized)
            const source = artifact.shared ? confined(join(root, "solutions", "general"), "environment.log") : confined(taskDir, artifact.path, Boolean(exportsByRole[artifact.role]))
            if (!existsSync(source)) {
                if (allowMissing && exportsByRole[artifact.role]) missing.push(artifact)
                else errors.push(`Brak wymaganego pliku: ${artifact.path}.`)
                continue
            }
            const bytes = readFileSync(source)
            // Empty stderr is valid evidence of a successful run, not a missing artifact.
            if (!bytes.length && !["log", "evidence"].includes(artifact.role)) fail(`Pusty artefakt: ${artifact.path}.`)
            // Executables without an extension are still build products.
            if (bytes.subarray(0, 4).equals(Buffer.from([0x7f, 0x45, 0x4c, 0x46])) || ["cffaedfe", "cefaedfe", "feedfacf", "feedface", "cafebabe"].includes(bytes.subarray(0, 4).toString("hex")) || bytes.subarray(0, 2).toString() === "MZ") fail(`Plik wykonywalny nie należy do paczki: ${artifact.path}.`)
            files.push({ path: artifact.path, source, bytes, artifact })
        } catch (error) { errors.push(error instanceof Error ? error.message : "Błąd odczytu artefaktu.") }
    }
    return { files, missing, errors }
}

async function validateFiles(root: string, manifest: Manifest, files: Snapshot[], run: Runner, paths: Set<string>): Promise<string[]> {
    const names = identities(root)
    const errors = privacy(JSON.stringify(manifest), "submission.json", names)
    const schoolHashes = new Set<string>()
    const schoolDir = join(root, "pdfs")
    if (existsSync(schoolDir) && !lstatSync(schoolDir).isSymbolicLink()) for (const entry of readdirSync(schoolDir, { withFileTypes: true })) {
        if (entry.isFile() && /\.pdf$/i.test(entry.name)) schoolHashes.add(sha256(readFileSync(join(schoolDir, entry.name))))
    }
    for (const file of files) {
        const role = file.artifact!.role
        errors.push(...privacy(file.path, file.path, names))
        if (schoolHashes.has(sha256(file.bytes))) errors.push(`${file.path}: kopia szkolnego materiału PDF.`)
        if (["report", "level-report", "reproduction"].includes(role)) {
            if (role !== "reproduction") errors.push(...validateReport(file, manifest, names, paths))
        }
        if (textExtensions.has(extname(file.path).toLowerCase()) || (!["export-pdf", "export-docx", "docx-reference", "chart", "asset", "evidence"].includes(role) && !file.bytes.includes(0))) {
            try { errors.push(...privacy(new TextDecoder("utf-8", { fatal: true }).decode(file.bytes), file.path, names)) } catch { errors.push(`${file.path}: plik tekstowy nie jest poprawnym UTF-8.`) }
        }
        if (["export-pdf"].includes(role)) {
            if (!file.bytes.subarray(0, 5).equals(Buffer.from("%PDF-")) || !file.bytes.subarray(-1024).includes(Buffer.from("%%EOF"))) errors.push(`${file.path}: niepoprawny lub niepełny PDF.`)
            // Compressed text, metadata and images require the hash-bound human review.
            errors.push(...privacy(file.bytes.toString("latin1"), file.path, names))
        }
        if (["export-docx", "docx-reference"].includes(role)) {
            const integrity = await run("unzip", ["-tqq", file.source], root)
            const entries = await run("unzip", ["-Z1", file.source], root)
            if (integrity.code || entries.code || !entries.stdout.toString().split(/\r?\n/).includes("word/document.xml")) { errors.push(`${file.path}: niepoprawny DOCX.`); continue }
            for (const name of entries.stdout.toString().trim().split(/\r?\n/).filter(n => /\.xml$/i.test(n))) {
                const xml = await run("unzip", ["-p", file.source, name], root)
                if (xml.code) { errors.push(`${file.path}: nie można sprawdzić zawartości DOCX.`); break }
                errors.push(...privacy(xml.stdout.toString("utf8"), file.path, names))
                const text = xml.stdout.toString("utf8").replace(/<[^>]*>/g, "").replace(/&#(x[0-9a-f]+|\d+);/gi, (_, n) => String.fromCodePoint(n[0].toLowerCase() === "x" ? parseInt(n.slice(1), 16) : Number(n))).replace(/&(?:amp|lt|gt|quot|apos);/g, match => ({ "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&apos;": "'" })[match]!)
                errors.push(...privacy(text, file.path, names))
            }
        }
    }
    return [...new Set(errors)]
}

/** Produce only missing exports. Keep diagnostics even when the export fails. */
async function exportMissing(taskDir: string, manifest: Manifest, missing: Artifact[], run: Runner): Promise<void> {
    if (!available("pandoc")) fail("Brak programu pandoc w PATH.")
    if (missing.some(a => a.role === "export-pdf") && manifest.pdfRoute !== "html" && !available("xelatex")) fail("Brak xelatex w PATH; można zadeklarować udokumentowaną trasę HTML.")
    const internal = join(taskDir, ".bundle")
    if (existsSync(internal) && (lstatSync(internal).isSymbolicLink() || !lstatSync(internal).isDirectory())) fail("Niepoprawny wewnętrzny katalog .bundle.")
    mkdirSync(internal, { recursive: true })
    const work = mkdtempSync(join(internal, "export-"))
    const diagnosticDir = join(work, "logs")
    mkdirSync(diagnosticDir)
    const version = await run("pandoc", ["--version"], taskDir)
    writeFileSync(join(diagnosticDir, "pandoc_stdout.txt"), version.stdout)
    writeFileSync(join(diagnosticDir, "pandoc_stderr.txt"), version.stderr)
    if (version.code) fail("Nie udało się sprawdzić Pandoca; diagnostyka pozostaje w .bundle.")
    const sorted = [...missing].sort((a, b) => Number(a.role === "export-pdf") - Number(b.role === "export-pdf"))
    for (const artifact of sorted) {
        if (artifact.role === "export-pdf" && manifest.pdfRoute === "html") fail("Trasa HTML: otwórz wygenerowany raport.html, wydrukuj go do raport.pdf i ponów polecenie.")
        const output = relative(taskDir, join(work, artifact.path))
        const args = ["raport.md", "--standalone", "--toc", "--number-sections", "--resource-path=.", "-o", output]
        if (artifact.role === "export-pdf") args.push("--pdf-engine=xelatex", "-V", "lang=pl-PL")
        const reference = manifest.artifacts.find(a => a.role === "docx-reference")
        if (reference && artifact.role === "export-docx") args.push("--reference-doc", reference.path)
        const result = await run("pandoc", args, taskDir)
        writeFileSync(join(diagnosticDir, `${artifact.path}_stdout.txt`), result.stdout)
        writeFileSync(join(diagnosticDir, `${artifact.path}_stderr.txt`), result.stderr)
        writeFileSync(join(diagnosticDir, `${artifact.path}_status.json`), JSON.stringify({ command: "pandoc", args, code: result.code, timedOut: Boolean(result.timedOut) }, null, 4) + "\n")
        if (result.code || !existsSync(join(taskDir, output))) fail(`Eksport ${artifact.path} nie powiódł się (kod ${result.code}); zachowano diagnostykę w .bundle.`)
        const target = confined(taskDir, artifact.path, true)
        // A file created concurrently must not be overwritten.
        linkSync(join(taskDir, output), target)
        rmSync(join(taskDir, output))
    }
}

function canonical(value: unknown): string {
    if (Array.isArray(value)) return "[" + value.map(canonical).join(",") + "]"
    if (object(value)) return "{" + Object.keys(value).sort().map(k => JSON.stringify(k) + ":" + canonical(value[k])).join(",") + "}"
    return JSON.stringify(value)
}

export function contentDigest(manifest: Manifest, files: { path: string, bytes: Buffer }[]): string {
    const { reviewedContentSha256: _, ...configuration } = manifest
    const hash = createHash("sha256")
    hash.update(canonical(configuration))
    for (const file of [...files].sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0)) {
        hash.update("\0" + file.path + "\0" + file.bytes.length + "\0" + sha256(file.bytes))
    }
    return hash.digest("hex")
}

async function archive(root: string, taskDir: string, manifest: Manifest, manifestBytes: Buffer, files: Snapshot[], run: Runner, force: boolean): Promise<string> {
    const output = join(root, "submissions")
    if (existsSync(output) && (lstatSync(output).isSymbolicLink() || !lstatSync(output).isDirectory())) fail("Niepoprawny katalog submissions.")
    mkdirSync(output, { recursive: true })
    const name = `${manifest.task}_${manifest.codename}`
    const destination = join(output, `${name}.zip`)
    try { const stat = lstatSync(destination); if (stat.isSymbolicLink() || !stat.isFile()) fail("Cel ZIP nie jest zwykłym plikiem."); if (!force) fail("ZIP już istnieje; użyj --force, aby go zastąpić.") } catch (error) { if (!(object(error) && error.code === "ENOENT")) throw error }
    const work = mkdtempSync(join(output, ".bundle-"))
    try {
        const snapshots = [...files, { path: "submission.json", source: join(taskDir, "submission.json"), bytes: manifestBytes }]
        for (const file of snapshots) {
            const target = join(work, name, file.path)
            mkdirSync(dirname(target), { recursive: true })
            writeFileSync(target, file.bytes)
        }
        const zipPath = join(work, "archive.zip")
        // Never recurse over the original task directory; only the reviewed whitelist is staged.
        const created = await run("zip", ["-q", "-X", "-r", "archive.zip", name], work)
        if (created.code) fail(`Tworzenie ZIP nie powiodło się (kod ${created.code}).`)
        const integrity = await run("unzip", ["-tqq", zipPath], work)
        const list = await run("unzip", ["-Z1", zipPath], work)
        const entries = list.stdout.toString("utf8").trim().split(/\r?\n/).filter(s => !s.endsWith("/"))
        const expected = snapshots.map(s => `${name}/${s.path}`).sort()
        if (integrity.code || list.code || JSON.stringify(entries.sort()) !== JSON.stringify(expected)) fail("ZIP nie przeszedł kontroli integralności lub listy plików.")
        const extracted = join(work, "verify")
        mkdirSync(extracted)
        const unpacked = await run("unzip", ["-qq", zipPath, "-d", extracted], work)
        if (unpacked.code) fail("Nie udało się kontrolnie rozpakować ZIP.")
        for (const file of snapshots) {
            if (sha256(readFileSync(join(extracted, name, file.path))) !== sha256(file.bytes)) fail(`ZIP zmienił zawartość: ${file.path}.`)
            const current = confined(file.artifact?.shared ? join(root, "solutions", "general") : taskDir, file.path)
            if (sha256(readFileSync(current)) !== sha256(file.bytes)) fail(`Plik zmienił się podczas pakowania: ${file.path}.`)
        }
        if (force) {
            try { const stat = lstatSync(destination); if (!stat.isFile() || stat.isSymbolicLink()) fail("Cel ZIP zmienił typ podczas pakowania.") } catch (error) { if (!(object(error) && error.code === "ENOENT")) throw error }
            renameSync(zipPath, destination)
        } else linkSync(zipPath, destination)
        return destination
    } finally { rmSync(work, { recursive: true, force: true }) }
}

/** Main API is injectable for isolated tests; CLI always locates the real repository itself. */
export async function bundle(task: string, options: Options = {}): Promise<Result> {
    const result: Result = { ok: false, errors: [], files: [] }
    const print = options.print ?? console.log
    try {
        if (!/^TiDPI_0[1-7]$/.test(task)) fail("Podaj dokładny identyfikator TiDPI_01–TiDPI_07.")
        const root = realpathSync(options.root ?? scriptRoot)
        const solutions = join(root, "solutions")
        if (lstatSync(solutions).isSymbolicLink() || !lstatSync(solutions).isDirectory()) fail("Niepoprawny katalog solutions.")
        const taskDir = join(solutions, task)
        const manifestPath = confined(taskDir, "submission.json")
        const manifestBytes = readFileSync(manifestPath)
        let parsed: unknown
        try { parsed = JSON.parse(manifestBytes.toString("utf8")) } catch { fail("submission.json nie jest poprawnym JSON.") }
        const manifest = parseManifest(parsed, task)
        const run = options.run ?? runCommand
        if (!options.run) for (const command of options.check ? ["unzip"] : ["zip", "unzip"]) if (!available(command)) fail(`Brak narzędzia ${command} w PATH.`)
        result.errors.push(...requirements(manifest))
        let collected = collect(root, taskDir, manifest, !options.check)
        result.errors.push(...collected.errors)
        const paths = new Set(manifest.artifacts.map(a => a.path))
        paths.add("submission.json")
        result.errors.push(...await validateFiles(root, manifest, collected.files, run, paths))
        if (result.errors.length) return result
        if (collected.missing.length) {
            print(`Generowanie brakujących eksportów: ${collected.missing.map(a => a.path).join(", ")}.`)
            await exportMissing(taskDir, manifest, collected.missing, run)
            collected = collect(root, taskDir, manifest, false)
            result.errors.push(...collected.errors, ...await validateFiles(root, manifest, collected.files, run, paths))
            if (result.errors.length) return result
        }
        result.files = [...collected.files.map(f => f.path), "submission.json"].sort()
        result.digest = contentDigest(manifest, collected.files)
        print(`Pliki paczki (${result.files.length}):\n${result.files.map(f => "  " + f).join("\n")}`)
        print(`reviewedContentSha256: ${result.digest}`)
        if (manifest.reviewedContentSha256 !== result.digest) {
            result.errors.push("Brak aktualnego potwierdzenia ręcznej kontroli. Sprawdź raport, eksporty, dowody i anonimizację, a następnie wpisz podany skrót do reviewedContentSha256 w submission.json.")
            return result
        }
        if (options.check) { result.ok = true; print("Kontrola paczki zakończona pomyślnie; nie utworzono ZIP."); return result }
        result.archive = await archive(root, taskDir, manifest, manifestBytes, collected.files, run, Boolean(options.force))
        result.ok = true
        print(`Gotowe: submissions/${basename(result.archive)}. Integralność i zawartość sprawdzone po rozpakowaniu.`)
    } catch (error) {
        // Filesystem errors may expose the account name in an absolute path.
        result.errors.push(error instanceof Error && !/(?:\/Users\/|\/home\/|[A-Z]:[\\/]Users[\\/])/i.test(error.message) ? error.message : "Błąd dostępu do pliku lub narzędzia; sprawdź lokalne pliki i uprawnienia.")
    }
    return result
}

async function main(): Promise<void> {
    const args = process.argv.slice(2)
    if (args.includes("--help")) {
        console.log("Użycie: bun run bundle TiDPI_01 [--check] [--force]\nManifest i procedura kontroli: scripts/BUNDLE.md\n--check: bez eksportów i ZIP; --force: zastąp istniejący ZIP.")
        return
    }
    if (!args[0] || args.slice(1).some(a => !["--check", "--force"].includes(a)) || new Set(args).size !== args.length || (args.includes("--check") && args.includes("--force"))) {
        console.error("Użycie: bun run bundle TiDPI_01 [--check | --force].")
        process.exitCode = 2
        return
    }
    const result = await bundle(args[0], { check: args.includes("--check"), force: args.includes("--force") })
    for (const error of result.errors) console.error(`BŁĄD: ${error}`)
    process.exitCode = result.ok ? 0 : 1
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) void main()

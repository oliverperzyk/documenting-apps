# Documenting Apps

This repository holds solutions for the remaining TiDPI tasks. Reports stay in Polish. School PDFs stay in gitignored `pdfs/` and are not committed.

## Layout

Task directories live under `solutions/`. When a task has levels, use `solutions/TiDPI_NN/raport.md` plus `a/`–`d/`, each with source, a raw log, and a level report. The top-level report is the single individual submission and includes or references all completed levels; level reports are supporting records, not separate school submissions. TiDPI 01 uses stages and optional R1–R5 extensions, not A–D levels.

## Report

YAML front matter:

```yaml
---
title: "..."
author: "Kryptonim TiDPI: {{ students_name }}"
date: "YYYY-MM-DD"
lang: pl-PL
---
```

Sections, in this order:

1. Kryptonim and the completed level.
2. Cel i hipoteza — state the hypothesis before the run. Do not pick a winner in advance.
3. Środowisko oraz konfiguracja — the toolchain that actually ran.
4. Zmienne i warunki eksperymentu — what changed, what was held fixed, and what the timer includes.
5. Kontrola poprawności — check full results against the task’s expected rule before any timing claim.
6. Procedura.
7. Surowe wyniki — evidence ids such as D01, with the raw log.
8. Opracowanie — minimum, maximum, rozstęp (max − min), and mediana. For an even trial count, the median is the mean of the two middle values after sorting.
9. Interpretacja — separate observation from conjecture. Do not claim a cause the run did not measure.
10. Ograniczenia — include one machine, one series, clock resolution, and anything the timer excluded. A time of 0 in the clock’s unit means the work was below that resolution.
11. Wnioski — only what this series shows.
12. Wykorzystanie AI i sposób weryfikacji — what the assistant wrote, and which log lines were rechecked.

A chart documents this series on this machine. It is not a universal law. Title it as a figure and point it at the table it came from.

## Rules

- The timer covers only the operation under test.
- Rotate variant order so one variant is not always first.
- Overlapping ranges are not a stable winner. A result missing from some trials is not a win.
- Every number comes from this task’s log, or is marked as exercise fiction. Hand-check arithmetic against the log. Do not fill tables from memory.
- Copy raw logs unchanged, including dots and failures. Prose and summary tables use the Polish decimal comma.
- After a sweep that edits a source constant, restore it.
- Report failures as they happened. Exit code 0 and “the file exists” do not prove the content is correct.
- Do not put personal data or directory paths in a report.

## Submission bundler

Use `bun run bundle TiDPI_NN` and the contract in `scripts/BUNDLE.md`. Each completed task has an explicit `submission.json`; declare only completed stages/levels, extensions, and the artifacts intended for handoff. The archive is a whitelist, not a recursive copy of the task folder. Keep the main report and supporting level reports separate; the bundler does not merge them or run experiments.

Report YAML is parsed with Bun's built-in `import { YAML } from "bun"`; do not add a third-party YAML dependency. Missing declared main-report exports may be generated with Pandoc/XeLaTeX. Existing exports are never overwritten. Preserve export diagnostics in the gitignored task-local `.bundle/` directory, outside the submission.

Before setting `reviewedContentSha256`, manually check the exact reported file list, logs, arithmetic, task-specific completeness, report/export consistency, visual layout, metadata, screenshots, and anonymization. The digest binds that review to artifact bytes and manifest configuration; it is not proof of semantic correctness. A changed file or configuration requires a new review. `--check` is read-only; `--force` authorizes replacing only the verified target ZIP. Output stays in gitignored `submissions/`; never submit externally without explicit authorization.

## Source materials and scope

These instructions summarize the local school PDFs. Read the relevant PDF again before implementing a task, especially its exercises, report requirements, and grading criteria. References below use PDF page numbers, starting at 1. Keep the PDFs and extracted copies out of commits. Do not upload school materials or publish them as part of a solution.

- `TiDPI_00a_Zasady_pracy_na_lekcji.pdf`, pp. 4–10: individual reports, honest evidence, AI disclosure, anonymization, and submission checks.
- `TiDPI_00b_Dlaczego_testujemy.pdf`, pp. 7–9: reproducible defect descriptions and independent verification of AI-generated work.
- `TiDPI_00c_Co_i_jak_testujemy.pdf`, pp. 4–11: correctness before performance; test purpose, scope, configuration, and frequency.
- `TiDPI_01_Dokumentacja_testow_w_Markdown_i_Pandoc.pdf`, pp. 9–19: fictional evidence package, report construction, export, and R1–R5.
- `TiDPI_02_Sortowanie_babelkowe_indeksy_i_wskazniki.pdf`, pp. 4–7, 13–15: full-result validation, timing design, levels, and report.
- `TiDPI_03_Tablice_statyczne_i_dynamiczne.pdf`, pp. 5–11, 13–15: memory experiment, levels, and report.
- `TiDPI_04_Dane_deterministyczne_powtarzalnosc_i_zlozonosc.pdf`, pp. 2–5, 9–12: reproducible inputs, counters, levels, and report.
- `TiDPI_05_Automatyzacja_kompilacji_uruchomienia_i_rejestracji_wyniku.pdf`, pp. 2–4, 9–14: build settings, automation failures, levels, and report.
- `TiDPI_06_Ustrukturyzowany_output_parser_CSV_i_walidacja_danych.pdf`, pp. 2–4, 13–16: data contract, parser outcomes, levels, and report.
- `TiDPI_07_Rzetelny_benchmark_Cpp_i_Python.pdf`, pp. 2–8: shared inputs, benchmark controls, levels, and deliverables.

Lessons 00a–00c provide background and classroom discussion exercises; the required individual report cycle is 01–07. Do not invent additional mandatory reports for lesson 00 or requirements for later team projects whose detailed briefs are absent.

For tasks 02–07, complete levels in order. A completed A can qualify for at most grade 3, A–B for 4, A–C for 5, and A–C plus a meaningful D for 6; partial A can qualify for 2. These are ceilings, not promised grades. Correctness, evidence, timeliness, anonymization, and the student's ability to explain the work still matter. Do not claim completion merely because matching filenames exist.

## Workflow for solving a task

1. Extract the actual acceptance criteria, required evidence, minimum trial counts, and selected extensions from the task brief. Establish expected functional results independently of the implementation.
2. Write the research question and hypothesis, variables, timer boundaries, and planned trial/order policy before running the experiment. For automation and parsing, define acceptance and rejection criteria instead of inventing a timing contest.
3. Preserve a working baseline. Implement the smallest correct core, validate it, and then add required levels or selected extensions. Preserve evidence of controlled failures in separate runs or clearly labeled fixtures; restore deliberately damaged code afterward.
4. Record the actual toolchain, source version, settings, inputs, seeds, and commands. Capture stdout, stderr, exit codes, and every required trial. Use separate run identifiers so later attempts cannot overwrite earlier evidence.
5. Check all results and dataset completeness before computing performance summaries. A malformed record, missing trial, or incorrect result must remain visible and must not silently disappear from the analysis.
6. Compute summaries from this task's logs, grouped by the factors that define one experiment. Add task-specific evidence and limitations to the shared report scaffold. Finish the consolidated report and inspect exported documents where required.
7. Recheck selected raw lines and arithmetic by hand, verify claims against source and logs, and record exactly how AI assistance was verified. The student must be able to explain every submitted fragment.

### Environment and evidence

The school examples target Visual Studio 2022, C++17 or newer, MSVC, and Developer PowerShell on Windows. Do not describe those tools as having run when the actual execution used another toolchain. If adapting to macOS, Clang, another debugger, or another architecture, record the real environment and the difference from the school procedure; an analogous run does not prove that a specifically required Visual Studio, Excel, or x86/x64 step was performed. Mark unavailable required steps as incomplete and preserve real diagnostics.

Use Debug for debugger observations and Release with actual optimization settings, without a debugger, for performance measurements. Do not infer optimization solely from `_DEBUG` being absent. Run compared programs sequentially, not concurrently. Preserve all trials and predefined warm-ups separately.

Use evidence IDs such as D01 and test IDs such as TC-01. Each claim, table, chart, and screenshot needs a caption and an explicit connection to evidence. Source files and text logs are primary artifacts; screenshots of code or tables do not replace them. Charts need a figure title, units, axis labels, a legend when applicable, and a reference to the source table.

Use only the teacher-assigned TiDPI codename. The `students_name` placeholder means that codename, never a personal name. Check report text, filenames, YAML, exported properties, logs, and screenshots for names, emails, account names, private paths, credentials, and other identifying information. Avoid capturing private paths in the first place; do not silently alter raw evidence to anonymize it. If a log already exposes personal data, keep the original private and label any separately prepared anonymized submission copy, explaining the redaction without changing results.

### Detected local environment (2026-09-28)

Read-only version and metadata checks are recorded in `solutions/general/environment.log`. This is an installed-environment snapshot, not evidence that a task or export has run. Recheck relevant versions before each experiment and report only the tools actually used.

- Host: macOS 27.0, build 26A428; native arm64 (Apple Silicon); Apple M4 Pro, 14 physical and 14 logical CPU cores; 25769803776 bytes RAM = 24 GiB. The checked native Python process uses 8-byte pointers. Do not relabel arm64 as x64.
- C++: Apple Clang 21.0.0 (`clang-2100.3.34.2`), target `arm64-apple-darwin27.0.0`; active developer tools are Command Line Tools, while Xcode 26.6 is also installed. The `g++` command identifies as Apple Clang, not GNU GCC. The task's language standard and Debug/Release optimization flags still need to be selected and recorded in its actual build.
- Python: default terminal `python3` is CPython 3.14.4; a separate Python 3.13.5 and system Python 3.9.6 are also available. The default is not the fictional lesson-01 Python version. Select one interpreter explicitly and preserve its version in each task's evidence.
- Debugger/editor: LLDB 2103.0.34.103, Visual Studio Code 1.139.1, Cursor 3.21.16, and PyCharm 2026.2.1 are available. Application versions establish installation only; no debugger exercise or Markdown preview is claimed by this inventory.
- Report publishing: Pandoc 3.11 and XeLaTeX (XeTeX 3.141592653-2.6-0.999998, TeX Live 2026, kpathsea 6.4.2) respond to version checks. `xelatex` is available for the lesson-01 direct PDF route, but successful export and visual correctness must still be tested. Pages 14.2, Numbers 14.2, and Google Chrome 149.0.7827.201 are installed. Pages/Numbers do not establish that Word/Excel requirements were performed.
- Automation/build helpers: PowerShell 7.5.4, CMake 4.1.0, Git 2.54.0 (Apple Git-157), Node.js 24.11.1, and Bun 1.4.0. macOS PowerShell is not Developer PowerShell with an initialized MSVC toolchain.
- Not found in the inspected terminal: `cl`, `cl.exe`, `gdb`, `ninja`, `pdftotext`, `pdftoppm`, `pdfinfo`, and `tectonic`. `pypandoc` and `pypandoc-binary` were not found in the checked default and separate Python 3.13.5 environments. This does not assert absence from every virtual environment or Windows guest.
- Word, Excel, LibreOffice, and Visual Studio were not found in the inspected standard macOS application directories. No Windows virtual machine/toolchain was inspected. Preserve that scope rather than asserting the computer cannot run those tools elsewhere.
- Default Python clock: `perf_counter` uses `mach_absolute_time()`, is monotonic and non-adjustable, and reports resolution `4.166666666666666e-08` seconds (approximately 41.67 ns). This is a runtime-reported clock resolution, not measured benchmark accuracy or proof of the C++ clock's resolution.

For local adaptations of lessons 02–07, use the verified native tools when suitable and explicitly document macOS/arm64/Clang/LLDB differences from the Windows/MSVC brief. Keep actual compiler flags, workload conditions, and completed tool-specific checks as task-specific evidence; do not prefill them from installation facts. Keep the fictional lesson-01 execution environment unchanged and describe the local environment only as its report-authoring/export environment.

## TiDPI 01 — Markdown and Pandoc

### Required core and solution method

This task documents the supplied fictional test run of a delivery-cost calculator. It is not a request to manufacture or rerun historical measurements. Clearly label the package as exercise fiction and distinguish its stated environment from the environment used to author/export the report.

The expected rule is `min(max(2 * distance_km, 0), 10)` in PLN. The fictional package has six cases TC-01–TC-06, one PASS and five FAIL, application 0.3.0, Windows 11 24H2, x86_64, Python 3.13.5, and execution date/time 2026-08-10 10:15:00. Copy the raw log from p. 9 unchanged. Recalculate expected values from the rule before transcribing the results. The revealed implementation is `min(distance_km + 2, 10)`; distinguish that evidence from assumptions about untested behavior.

1. Create `raport.md`: one main heading, at least four second-level sections, purpose paragraph, environment list, at least a two-case table, a fenced `text` log, a Pandoc documentation link, and a blockquote stating the fictional provenance.
2. Expand to all six cases with input, expected result, actual result, and status; an environment table; the unchanged log; at least two conclusions referencing case IDs; at least three limitations; and a proposed next test. Check the Markdown preview and seek the two-minute reader check described in the brief; do not invent a peer review.
3. Add YAML metadata. Record `pandoc --version` and exact export commands. Generate DOCX with a table of contents and section numbering, then PDF. Open both and inspect Polish characters, tables, code/log blocks, links, and page breaks. Document at least two presentation differences between MD, DOCX, and PDF.

Run exports in the report's working directory, using filenames without private paths:

```sh
pandoc --version
pandoc raport.md --standalone --toc --number-sections -o raport.docx
pandoc raport.md --pdf-engine=xelatex -V lang=pl-PL -o raport.pdf
```

The direct PDF command requires the specified installed engine. If it is unavailable, preserve the failure, generate standalone HTML with `pandoc raport.md --standalone -o raport.html`, print it to PDF in a browser, and record that route. Do not claim successful conversion from an exit code or artifact existence alone.

### Optional extensions and handoff

- R1: modify DOCX reference styles Title, Heading 1, Heading 2, Normal, and Source Code; submit the reference DOCX and styled output, documenting at least four intentional style changes.
- R2: write `export_reports.ps1` to check the source, show the Pandoc version, generate DOCX/standalone HTML, attempt PDF, and report each export's success/failure; document output inspection.
- R3: call Pandoc through `pypandoc`; submit script, DOCX, and console evidence. Explain the Pandoc binary dependency and `convert_text()` versus `convert_file()`.
- R4: write `check_report.py` to verify one main heading, required sections, TC-01–TC-06, balanced code fences, fictional-data notice, and a link; return 0 on success and nonzero on failure. Test a valid report and a deliberately damaged copy.
- R5: compare a fixture containing a table, task list, strikethrough, footnote, and YAML in VS Code, GitHub Flavored Markdown if available, and Pandoc HTML; record support and dialect differences.

Submit MD, DOCX, PDF, and HTML if the fallback was used, plus artifacts for completed R extensions. Do not apply the A–D grade ladder to this lesson.

## TiDPI 02 — Bubble sort: indices and pointers

Implement the same bubble-sort algorithm in indexed and pointer forms, including shrinking the unsorted suffix and `swapped` early exit. Handle fewer than two elements before unsigned `size - 1`; guard null pointers before dereferencing. Make independent copies of the same input for both variants and for `std::sort`. Compare entire results against the reference after every trial; sortedness alone cannot detect lost or duplicated values.

- A: run the baseline; manually trace each full pass of `{5, 2, 4, 1}`; use Debug breakpoints in both functions. Record `i`, `end`, compared values, and `swapped`; record `current`, `next`, dereferenced values, and `next - current`. Explain indexed/pointer equivalence and verify both results against `std::sort`.
- B: Release without debugger; five trials for each of 1000, 2000, and 4000 elements, for both implementations. Alternate which variant runs first. Measure only sorting with `steady_clock` in microseconds; exclude generation, copying, reference sorting, validation, and printing. Preserve all results; calculate min/max/range and the repository-required median. Compare variability and approximate growth when doubling the size.
- C: random, sorted, and reversed inputs; at least three sizes and five trials per input kind, size, and implementation. Keep alternating order, add a chart, and explain early exit and pass counts from evidence.
- D: one controlled study beyond the core, such as Release disassembly, two optimization settings, with/without early exit, or execution-order effects. Include hypothesis, changed/fixed factors, repeatable method, raw evidence, interpretation, and limitations.

Do not promise a pointer advantage, exact fourfold timings, or a measured cache/aliasing explanation without supporting measurements. Preserve debugger evidence separately from performance runs.

## TiDPI 03 — Local, global, and dynamic arrays

Compare local fixed-size `std::array`, global fixed-size `std::array` with static storage duration, and a dynamic `std::unique_ptr<std::uint32_t[]>`. Use equal sizes, identical contiguous element types, and the same `process_data` function. Restore `i % 1000` before every trial, including the global array. Check every initial element, then every final value against `i % 1000 + rounds`, and compare the full arrays. Checksums are additional evidence, not replacements for full validation. Do not confuse fixed size, scope, storage duration, and typical memory placement; do not use variable-length local arrays as standard C++.

- A: run the baseline; hand-calculate bytes as `element_count * sizeof(std::uint32_t)` and KiB as bytes/1024; compare with output. Observe all three addresses in Debug. Show initial/final/equality checks; deliberately change the expected value to prove rejection, then restore it. Explain local, global, local `static`, dynamic storage, and RAII.
- B: at least three `element_count` values, six trials each, all three variants; example sizes are 5000, 20000, and 50000. Recompile after changing the constant and restore it after the sweep. Keep `rounds` fixed within a series (baseline: 100). Rotate local/global/dynamic order over three positions. Time processing only in Release, excluding allocation, initialization, validation, checksums, and deallocation. Preserve all times, min/max/range/median, and a chart against element count.
- C: choose two: separate dynamic allocation plus deallocation experiment; gradual local-array limit study in a project copy recording bytes, largest successful size, and first failed size; identical Release series on x86 and x64 including `sizeof(void*)`. Do not invent an x86 run on unsupported hardware or turn an unobserved failure into a claimed boundary.
- D: one justified study, such as raw arrays versus RAII containers with allocation separated, RAII during early return/exception, diagnosing a controlled leak, or element-size effects.

Report real crashes and incomplete runs. A processing experiment does not measure allocation cost and does not establish that the heap or x64 is universally faster/slower.

## TiDPI 04 — Deterministic data and complexity

Use a fresh `std::mt19937(seed)` for each recreated pseudorandom input and the baseline mapping `generator() % 10000U`. Record generator, seed, size, type/range, mapping, input order, generator source version, and fingerprint algorithm. Modulo bias is a known limitation; this is not a randomness-quality or cryptography experiment. Prepare data, copies, fingerprints, and `std::sort` reference outside timing. Count comparisons, swaps, and passes inside the instrumented sort and validate the full result. Its timings include instrumentation overhead and cannot directly be compared with uninstrumented timings from another lesson.

- A: preserve the full baseline output. For n=500 and one seed, show five trials for each of sorted/reversed/pseudorandom input, with fingerprints and counters. Change one seed and show which inputs change; briefly change one generator instruction and show the fingerprint effect; restore the baseline. Distinguish identical input/results/counters from potentially different timings.
- B: seed 20260401; sizes 500, 1000, 2000, 4000; all three input orders; five trials per case. Rotate order and measure in Release without debugger. Analyze operation counts as primary complexity evidence, retaining all times and time summaries. Calculate comparison growth at each size doubling; check sorted comparisons against `n - 1` and reversed comparisons against `n * (n - 1) / 2`. Chart comparisons against n by input order.
- C: choose two: add at least three new seeds; compare with/without `!swapped` on identical inputs for all three orders; introduce almost-sorted data with an explicit disturbance count and method.
- D: one study such as comparison counts for `std::sort`, file-based replay, cross-toolchain input verification, or log-scale operation-growth analysis.

The baseline also includes seed 20260402; retain its output even though B's required analysis focuses on 20260401. Group by size/seed/order. Fingerprints and operation counts should repeat within a group; timing need not. Fingerprint equality is not mathematical proof of full-input equality. Mark growth ratios undefined when the denominator is zero. Separate auxiliary O(1) memory from O(n) total storage including input.

## TiDPI 05 — Build, run, and evidence automation

Use a C++ test program and Python `subprocess.run` with an argument list, `shell=False`, captured stdout/stderr, explicit working directory, timeouts, and `check=False` so failures can be logged. Define and record exit-code meanings. Before compilation, remove only the known previous generated executable or build into a fresh isolated output. Run only after successful compilation and confirmation of a fresh executable. Save separate compilation/execution streams and codes in unique run directories. Propagate failure to the script's exit code.

The school baseline uses MSVC `/nologo /std:c++17 /EHsc /W4 /permissive- /utf-8`, output options, and `/O2 /MD` for Release or `/Od /MDd` for Debug. `/O1 /MD` is the size-oriented alternative. Explain flags actually used; do not present other compilers' flags as MSVC settings. `/O1` does not automatically reduce array memory. The sample timeout code 124 is a script convention. Whole-process build/run times are metadata, not sorting benchmarks.

- A: confirm compiler/Python availability; manually compile/run and preserve commands and code. Run automated release/pass twice and prove distinct evidence directories with no overwrite. Explain `compile_stdout.txt`, `compile_stderr.txt`, `run_stdout.txt`, `run_stderr.txt`, and `summary.txt`; connect `passed` to the actual build/run evidence.
- B: release/fail must preserve output, diagnostic stderr, program code 1, and script code 1. Introduce a syntax error; show compile failure, `execution_attempted=false`, and absence of the stale executable. Missing run files are expected when execution was skipped. Restore source and obtain a successful run. Explain `environment_error`, `compile_failed`, and `run_failed`.
- C: choose two: `--repeat` from 1 to 10 with separate files/codes for every attempt and evidence retained after failures; validated `--size` forwarded as separate arguments and saved in the summary; source/executable byte-size and modification-time manifest with limitations. Test successful and unsuccessful behavior of selected extensions.
- D: one justified extension such as SHA-256 source/executable hashes, distinct timeout/unknown-code/missing-artifact statuses, validated JSON/YAML configuration, or a CI task preserving logs.

Describe intentional failure as a negative test of the automation. A timestamp or matching filename does not prove artifact contents.

## TiDPI 06 — Structured output, parser, CSV, validation

Implement this version-1 wire contract exactly; the two displayed lines are its protocol and header, not a results example:

```text
TIDPI_RESULTS;1
case;size;trial;time_us;comparisons;correct
```

Use `csv` with delimiter `;`. Validate readable UTF-8 (BOM supported), protocol/version, exact header order, six fields per record, integer types, `size >= 2`, `trial >= 1`, nonnegative `time_us` and `comparisons`, `case` in `sorted/reversed/random`, `correct` exactly `true/false`, unique `(case, size, trial)`, and at least one record. Do not silently skip malformed rows. Validate the whole dataset before publishing any CSV and ensure rejected input cannot leave a stale output. Keep input/output distinct so cleanup cannot delete the input. Use `csv.DictWriter`, `newline=''`, and the documented `utf-8-sig` output encoding.

Parser outcomes are distinct:

- 0: valid data, all tests successful, CSV created.
- 1: valid data with at least one `correct=false`, CSV created.
- 2: input/contract failure; no CSV published. A write failure is also an error and must not be reported as success.

- A: Release producer; preserve raw output and parser streams/code. Verify exactly 18 records from three cases × two sizes (16, 32) × three trials. Explain each field, parsing versus validation, and numeric cells without units. Inspect CSV in a text editor, import in Excel with explicit UTF-8/`;`, and reread with `csv` to count records.
- B: test `invalid-number`, `missing-field`, `duplicate-row`, and `wrong-version`: expect parser code 2, stderr identifying the rule/line, and no CSV. Leave a previously valid output before one rejection and prove its removal. Test `failed-test`: expect code 1 and a CSV retaining `correct=false`. Distinguish read, structure, value, and valid-test-failure cases; record expected and actual outcomes.
- C: choose two: version 2 with a seed field and rejection by the v1 parser; configurable completeness validation detecting missing and extra records; a `note` field containing semicolon and quote with correct producer/consumer CSV escaping. Keep contract, producer, parser, and tests consistent.
- D: at least ten varied fixtures, automatically run, covering boundaries and combined errors, with a justified data-risk model and acceptance/rejection evidence; possible additions include JSON validation reports, separate version parsers, unexpected blank/header rows and large values, or round-trip properties.

Generate faults using explicit producer modes or separate labeled fixtures. Preserve the original raw files. A producer can return 0 while emitting a deliberately malformed contract, so producer and parser codes are separate evidence. Small `time_us` values in this exercise are data-processing fields, not a reliable performance comparison.

## TiDPI 07 — A fair C++/Python benchmark

Generate one shared integer data file and read that same file in both implementations. Identical seeds in different languages do not guarantee identical sequences. Define one common manually implemented computation and expected checksum before measuring; the brief's demonstration sums squares over a fixed number of rounds, but the actual operation must be agreed with the teacher. Check integer range/overflow for the selected C++ type and validate against an independent expected value, not just agreement between two potentially wrong programs.

Read and prepare input before timing. Use C++ `steady_clock` converted to nanoseconds and Python `time.perf_counter_ns()`. Time only the computation, then print/check the observable checksum. Use the same rounds and workload in both languages. Record clock resolution separately from the unit; nanoseconds in a field name do not establish nanosecond experiment accuracy. Both producers use:

```text
language;trial;time_ns;checksum;correct
```

- A: shared file with at least 10000 integers; report element count, generator seed, and fingerprint/checksum. Implement the same manual loop in C++ and Python, with identical expected checksum. Use C++ Release, at least two predefined warm-ups and ten measured trials per implementation; preserve structured raw records. Rotate execution order and run sequentially.
- B: automate both runs, capturing stdout/stderr/codes. Validate header, types, trial counts, units, and checksums. Intentionally alter an implementation or input to show comparison rejection. Preserve every time; compute per-implementation minimum and median (also max/range per repository rules), explaining their different meanings. Repeat the entire experiment in a separate run and compare conclusions; do not pool the two runs without identifying them.
- C: choose two controlled studies: C++ Debug versus Release kept separate; at least three data sizes; no warm-up versus predefined warm-up; manual loop versus library computation labeled as different implementations; justified rounds adjustment to make an individual measurement long enough. Change one planned factor per study.
- D: one meaningful study, such as iteration calibration, reproducibly randomized order, full environment metadata, time-distribution chart, or library work executed outside the Python interpreter; include hypothesis, controls, validation, and limitations.

Submit report MD and generated DOCX or PDF; C++/Python sources; generator and shared input or an unambiguous reproduction procedure; automation script; raw results from both implementations; validated CSV; logs/exit codes; and cited evidence. Conclusions concern the measured implementations, data, configurations, and runs on this machine. They do not establish a universal language-speed ratio.

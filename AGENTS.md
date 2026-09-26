# Documenting Apps

This repository holds solutions for the remaining TiDPI tasks. Reports stay in Polish. School PDFs stay in gitignored `pdfs/` and are not committed.

## Layout

When a task has levels, use `TiDPI_NN/raport.md` plus `a/`–`d/`, each with source, a raw log, and a level report.

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

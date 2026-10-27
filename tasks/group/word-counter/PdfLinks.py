#!/usr/bin/env python3
"""Pandoc JSON filter used when exporting the report to LaTeX/PDF."""

import json
import re
import sys


class PdfLinks:
    @staticmethod
    def escapeLatex(text: str) -> str:
        special = {
            "\\": r"\textbackslash{}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
        }
        return "".join(
            special.get(character, "\\" + character) if character in "\\{}$&#%_^~" else character for character in text
        )

    @staticmethod
    def formatCode(text: str) -> dict:
        escaped = PdfLinks.escapeLatex(text)
        if " " in text:
            # seqsplit discards literal spaces: preserve them explicitly.
            escaped = escaped.replace(" ", r"\hspace*{0.525em}")
            latex = r"\texttt{" + escaped + "}"
        else:
            latex = r"\texttt{\seqsplit{" + escaped + "}}"
        return {"t": "RawInline", "c": ["latex", latex]}

    @staticmethod
    def rewriteLink(target: str) -> str:
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith(("#", "/")):
            return target
        return "../../" + target

    @staticmethod
    def transform(element):
        if isinstance(element, list):
            return [PdfLinks.transform(item) for item in element]
        if not isinstance(element, dict):
            return element

        result = {key: PdfLinks.transform(value) for key, value in element.items()}
        kind = result.get("t")
        if kind == "Link":
            result["c"][2][0] = PdfLinks.rewriteLink(result["c"][2][0])
        elif kind == "Code":
            return PdfLinks.formatCode(result["c"][1])
        elif kind == "Str" and result["c"] == "10⁻⁸":
            return {"t": "Math", "c": [{"t": "InlineMath"}, "10^{-8}"]}
        return result

    @staticmethod
    def init() -> int:
        try:
            document = json.load(sys.stdin)
            if not isinstance(document, dict) or not isinstance(document.get("blocks"), list):
                raise ValueError("Oczekiwano dokumentu JSON Pandoca z lista blocks")
            json.dump(PdfLinks.transform(document), sys.stdout, ensure_ascii=False)
            sys.stdout.write("\n")
        except (ValueError, KeyError, IndexError, TypeError) as error:
            print(f"Blad filtra PDF: {error}", file=sys.stderr)
            return 1
        return 0


if __name__ == "__main__":
    sys.exit(PdfLinks.init())

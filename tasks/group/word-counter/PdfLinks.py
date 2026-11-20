#!/usr/bin/env python3
"""Dostosowuje dokument JSON Pandoca do eksportu raportu przez LaTeX."""

import json
import re
import sys


class PdfLinks:
    """Przekształca odnośniki, kod i zapis wykładnika na potrzeby PDF."""

    @staticmethod
    def escapeLatex(text: str) -> str:
        """Zabezpiecza znaki specjalne w tekście przekazywanym do LaTeX-a.

        Args:
            text: Tekst przeznaczony do wstawienia jako zwykłe znaki.

        Returns:
            Tekst z sekwencjami LaTeX-a zastępującymi znaki specjalne.
        """
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
        r"""Formatuje kod śródtekstowy krojem o stałej szerokości.

        Zachowuje spacje za pomocą \hspace* i stosuje \seqsplit do łamania
        ciągów bez spacji.

        Args:
            text: Tekst kodu z węzła Code Pandoca.

        Returns:
            Słownik węzła RawInline z kodem LaTeX.
        """
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
        """Dostosowuje względną ścieżkę do położenia raportu w output/pdf/.

        Args:
            target: Oryginalny adres odnośnika.

        Returns:
            Względny adres poprzedzony ../../. Adresy ze schematem, ścieżki
            zaczynające się od ukośnika i odnośniki do kotwic zachowują postać.
        """
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith(("#", "/")):
            return target
        return "../../" + target

    @staticmethod
    def transform(element):
        """Przekształca węzły Pandoca rekurencyjnie.

        Aktualizuje cele odnośników, formatuje kod śródtekstowy i zamienia
        samodzielny węzeł tekstowy 10⁻⁸ na wzór śródtekstowy.

        Args:
            element: Słownik, lista lub wartość skalarna z dokumentu JSON.

        Returns:
            Przekształcona struktura JSON. Wartości skalarne zachowują postać.
        """
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
        """Czyta JSON Pandoca ze stdin i zapisuje wynik na stdout.

        Oczekuje obiektu z polem blocks będącym listą. Przy błędzie
        formatu wejścia wypisuje komunikat na stderr.

        Returns:
            Kod 0 przy powodzeniu lub 1 przy błędzie JSON albo struktury.
        """
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

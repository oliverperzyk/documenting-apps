#!/bin/sh
# Wariant C istniejącego eksportu; uruchom z katalogu TiDPI_07. Wymaga pandoc, XeLaTeX oraz fontów Arial i Menlo.
set -eu
mkdir -p _build
cat > _build/pdf_header.tex <<'TEX'
\usepackage{needspace}
\usepackage{etoolbox}
\BeforeBeginEnvironment{verbatim}{\Needspace{13\baselineskip}}
TEX
cat > _build/pdf_layout.lua <<'LUA'
function CodeBlock(el)
  local _, breaks = el.text:gsub("\n", "")
  local lines = breaks + 3
  return {pandoc.RawBlock("latex", "\\Needspace{" .. lines .. "\\baselineskip}"), el}
end
function Para(el)
  local text = pandoc.utils.stringify(el.content)
  if text:match("^C[12],") then
    return {pandoc.RawBlock("latex", "\\Needspace{17\\baselineskip}"), el}
  end
  if text == "cpp:" or text == "python:" or text:match("^Python %(D06") then
    return {pandoc.RawBlock("latex", "\\Needspace{16\\baselineskip}"), el}
  end
end
function Header(el)
  local text = pandoc.utils.stringify(el.content)
  if el.level == 3 and (text:match("^D12") or text:match("^D14")) then
    return {pandoc.RawBlock("latex", "\\Needspace{20\\baselineskip}"), el}
  elseif el.level == 3 then
    return {pandoc.RawBlock("latex", "\\Needspace{7\\baselineskip}"), el}
  elseif el.level == 2 and text:match("^3%.") then
    return {pandoc.RawBlock("latex", "\\Needspace{15\\baselineskip}"), el}
  elseif el.level == 2 and text:match("^7%.") then
    return {pandoc.RawBlock("latex", "\\Needspace{22\\baselineskip}"), el}
  elseif el.level == 2 then
    return {pandoc.RawBlock("latex", "\\Needspace{8\\baselineskip}"), el}
  end
end
function Blocks(blocks)
  local result = {}
  local group = false
  for _, el in ipairs(blocks) do
    if el.t == "Para" and pandoc.utils.stringify(el.content):match("^C[12],") then
      table.insert(result, pandoc.RawBlock("latex", "\\begin{minipage}{\\linewidth}"))
      group = true
    end
    table.insert(result, el)
    if group and el.t == "CodeBlock" then
      table.insert(result, pandoc.RawBlock("latex", "\\end{minipage}\\par\\medskip"))
      group = false
    end
  end
  return result
end

LUA
pandoc raport.md --from=markdown --pdf-engine=xelatex \
  -V mainfont=Arial -V monofont=Menlo -V fontsize=10pt \
  -V papersize=a4 -V geometry:margin=20mm \
  -V colorlinks=true -V urlcolor=blue \
  --lua-filter=_build/pdf_layout.lua --include-in-header=_build/pdf_header.tex -o raport.pdf

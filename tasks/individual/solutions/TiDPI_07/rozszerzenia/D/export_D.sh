#!/bin/sh
# Uruchom z TiDPI_07; oddzielny eksport D bez zmiany historycznych skryptów.
set -eu
mkdir -p _build
cat > _build/D_header.tex <<'TEX'
\usepackage{needspace}
\usepackage{float}
\floatplacement{figure}{H}
TEX
cat > _build/D_layout.lua <<'LUA'
-- Keep captions with full code blocks; avoid nested minipages and split logs.
function Blocks(blocks)
  local result = {}
  for i, el in ipairs(blocks) do
    local following = blocks[i+1]
    if el.t == "Para" and following and following.t == "CodeBlock" then
      local _, n = following.text:gsub("\n", "")
      table.insert(result, pandoc.RawBlock("latex", "\\Needspace{" .. (n+6) .. "\\baselineskip}"))
    elseif el.t == "CodeBlock" then
      local _, n = el.text:gsub("\n", "")
      table.insert(result, pandoc.RawBlock("latex", "\\Needspace{" .. (n+3) .. "\\baselineskip}"))
    elseif el.t == "Header" then
      local title = pandoc.utils.stringify(el.content)
      local lines = 7
      if el.level == 2 and title:match("^3%.") then lines = 15 end
      if el.level == 2 and title:match("^7%.") then lines = 22 end
      table.insert(result, pandoc.RawBlock("latex", "\\Needspace{" .. lines .. "\\baselineskip}"))
    end
    table.insert(result,el)
  end
  return result
end
LUA
pandoc raport.md --from=markdown --pdf-engine=xelatex \
  -V mainfont=Arial -V monofont=Menlo -V fontsize=10pt \
  -V papersize=a4 -V geometry:margin=20mm \
  -V colorlinks=true -V urlcolor=blue \
  --lua-filter=_build/D_layout.lua --include-in-header=_build/D_header.tex -o raport.pdf

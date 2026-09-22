# figures -> numbers -> PDF. Needs a TeX distribution (MiKTeX or TeX Live) and Python.
$ErrorActionPreference='Stop'
Set-Location $PSScriptRoot

if (-not (Test-Path 'data\receipts.json')) {
  Write-Host 'data\receipts.json missing: figures will SKIP and numbers stay ?? in the PDF.' -ForegroundColor Yellow
  Write-Host 'Run: python export_receipts.py --repo C:\Users\steph\szl-typesafe-triage --out data\receipts.json' -ForegroundColor Yellow
  python figures.py --demo --out figures
} else {
  python figures.py --receipts data\receipts.json --out figures
  python inject_numbers.py
}

if (-not (Get-Command latexmk -ErrorAction SilentlyContinue)) {
  throw 'latexmk not found: winget install --id MiKTeX.MiKTeX -e'
}
latexmk -pdf -interaction=nonstopmode main.tex
latexmk -c
Write-Host "`nPDF: $(Resolve-Path main.pdf)" -ForegroundColor Green
Get-Content figures\figure_manifest.json -Raw | Write-Host

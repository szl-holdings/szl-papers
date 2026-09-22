# Flagship paper build placeholder.
# This script intentionally refuses to compile before main.tex is evidence-complete.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

if (-not (Test-Path '.\main.tex')) {
    throw 'Build blocked: main.tex is not present. The flagship paper remains blocked until the local source census and evidence ledger are complete.'
}

if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    throw 'pdflatex not found. Install MiKTeX and run in normal PowerShell.'
}

pdflatex -interaction=nonstopmode -file-line-error main.tex
if ($LASTEXITCODE -ne 0) { throw 'First pdflatex pass failed. Read main.log.' }
pdflatex -interaction=nonstopmode -file-line-error main.tex
if ($LASTEXITCODE -ne 0) { throw 'Second pdflatex pass failed. Read main.log.' }

Write-Host "Built: $(Resolve-Path .\main.pdf)" -ForegroundColor Green

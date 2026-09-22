# Corrected private triage-note build. Run in normal PowerShell, not as Administrator.
# No latexmk or Perl required.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    throw 'pdflatex not found. Install MiKTeX, then re-run in a normal PowerShell window.'
}

pdflatex -interaction=nonstopmode -file-line-error main.tex
if ($LASTEXITCODE -ne 0) { throw 'First pdflatex pass failed. Read main.log.' }
pdflatex -interaction=nonstopmode -file-line-error main.tex
if ($LASTEXITCODE -ne 0) { throw 'Second pdflatex pass failed. Read main.log.' }

$pdf = Resolve-Path main.pdf
Write-Host "`nPRIVATE NOTE BUILT: $pdf" -ForegroundColor Green
Write-Host 'No DOI. Do not deposit. The public artifact card and gate report control the verdict.' -ForegroundColor Yellow
Start-Process $pdf

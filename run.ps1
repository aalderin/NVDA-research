# =============================================================================
# NVIDIA (NVDA) Valuation Application — Execution Script
# FIN 43900 — AI and Finance Project 1
# Runs full pro-forma forecast, FCFF engine, and peer comps using Python standard library.
# =============================================================================

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  NVIDIA (NVDA) CORPORATE FINANCE VALUATION ENGINE" -ForegroundColor Cyan
Write-Host "  Running complete 3-statement pro-forma, FCFF DCF, and peer comps..." -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Run 3-Statement Integrated Pro-Forma Forecast and Sensitivity Analysis
Write-Host "[1/3] Executing Integrated 3-Statement Pro-Forma Forecast (nvda_proforma.py)..." -ForegroundColor Yellow
python "$ScriptDir\nvda_proforma.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: nvda_proforma.py failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "3-Statement Pro-Forma and Articulation Checks Passed!" -ForegroundColor Green
Write-Host ""

# 2. Run FCFF DCF Engine, WACC Sensitivity and Reverse DCF
Write-Host "[2/3] Executing FCFF DCF Valuation Engine and Reverse DCF (dcf.py)..." -ForegroundColor Yellow
python "$ScriptDir\dcf.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: dcf.py failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "FCFF DCF Engine and Reverse DCF Completed!" -ForegroundColor Green
Write-Host ""

# 3. Run Comparable Company Multiples Valuation (P/E and EV)
Write-Host "[3/3] Executing Peer Comps Valuation (pe_comps.py)..." -ForegroundColor Yellow
python "$ScriptDir\pe_comps.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: pe_comps.py failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "Peer Comps Analysis Completed!" -ForegroundColor Green
Write-Host ""

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  EXECUTION SUCCESSFUL: ALL VALUATION MODELS COMPLETED CLEANLY" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan


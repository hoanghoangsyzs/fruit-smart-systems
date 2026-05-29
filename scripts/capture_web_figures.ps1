# Chup Hinh 2.8.5.5 va 2.8.5.6 (can backend + frontend dang chay)
# Yeu cau: da dang nhap tren trinh duyet hoac dung Swagger

$outDir = Join-Path $PSScriptRoot "..\docs\figures\2.8.5"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

Write-Host "=== Kiem tra server ===" -ForegroundColor Cyan
try {
    $h = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing -TimeoutSec 3
    Write-Host "Backend OK: $($h.StatusCode)"
} catch {
    Write-Host "Backend CHUA chay. Mo terminal:" -ForegroundColor Yellow
    Write-Host "  cd backend; .\.venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --reload --port 8000"
}

$fePorts = @(5173, 5174)
$feUrl = $null
foreach ($p in $fePorts) {
    try {
        $r = Invoke-WebRequest -Uri "http://localhost:$p/" -UseBasicParsing -TimeoutSec 2
        if ($r.StatusCode -eq 200) { $feUrl = "http://localhost:$p"; break }
    } catch { }
}
if ($feUrl) {
    Write-Host "Frontend OK: $feUrl"
} else {
    Write-Host "Frontend CHUA chay. Mo terminal:" -ForegroundColor Yellow
    Write-Host "  cd frontend; npm run dev"
}

Write-Host ""
Write-Host "=== Huong dan chup thu cong ===" -ForegroundColor Green
Write-Host "1. Dang nhap: $feUrl/login"
Write-Host "2. Hinh 2.8.5.5: $feUrl/analyze — chon anh, CHUA bam Phan tich"
Write-Host "3. Hinh 2.8.5.6: $feUrl/analyze — sau khi co ket qua hotspot"
Write-Host "4. Luu vao: $outDir"
Write-Host "   Hinh_2_8_5_5_web_gui.png"
Write-Host "   Hinh_2_8_5_6_web_ket_qua.png"
Write-Host ""
Write-Host "Hoac Swagger: http://127.0.0.1:8000/docs — POST /api/v1/analyze"

# Mo thu muc output
Start-Process explorer.exe $outDir

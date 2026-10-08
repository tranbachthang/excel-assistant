# Windows built-in OCR v2 - fixed WinRT async calls
param([string]$ImagePath)

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Runtime.WindowsRuntime

if (-not (Test-Path $ImagePath)) {
    Write-Host "[!] File khong ton tai: $ImagePath"
    exit 1
}

$img = [System.Drawing.Image]::FromFile($ImagePath)
Write-Host "[*] File: $ImagePath"
Write-Host "[*] Size: $($img.Width)x$($img.Height)"
Write-Host "=" * 60

try {
    # Load WinRT types
    [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
    [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
    [Windows.Storage.StorageFile, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
    [Windows.Storage.Streams.RandomAccessStreamReference, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null

    $path = (Resolve-Path $ImagePath).Path
    
    # Get file and open stream
    $storageFile = [Windows.Storage.StorageFile]::GetFileFromPathAsync($path)
    $task = $storageFile.AsTask()
    $task.Wait()
    $file = $task.Result
    
    $streamTask = $file.OpenReadAsync().AsTask()
    $streamTask.Wait()
    $stream = $streamTask.Result
    
    # Create BitmapDecoder
    $decoderTask = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).AsTask()
    $decoderTask.Wait()
    $decoder = $decoderTask.Result
    
    # Get SoftwareBitmap
    $bitmapTask = $decoder.GetSoftwareBitmapAsync().AsTask()
    $bitmapTask.Wait()
    $bitmap = $bitmapTask.Result
    
    # OCR Engine
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
    if (-not $engine) {
        $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
    }
    
    $ocrTask = $engine.RecognizeAsync($bitmap).AsTask()
    $ocrTask.Wait()
    $result = $ocrTask.Result
    
    Write-Host "[*] OCR: Windows Built-in"
    if ($result.Lines.Count -gt 0) {
        foreach ($line in $result.Lines) {
            Write-Host $line.Text
        }
    } else {
        Write-Host "[!] Khong tim thay text trong anh."
    }
} catch {
    Write-Host "[!] Windows OCR failed: $($_.Exception.Message)"
    Write-Host "[*] Can cai Tesseract: winget install UB-Mannheim.TesseractOCR"
}
finally {
    $img.Dispose()
}

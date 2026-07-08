# Gerador de assets para Futebol Runner (executar uma vez)
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent $PSScriptRoot
$imgDir = Join-Path $root "assets\images"
$sndDir = Join-Path $root "assets\sounds"
$fontDir = Join-Path $root "assets\fonts"
New-Item -ItemType Directory -Force -Path $imgDir, $sndDir, $fontDir | Out-Null

function Save-Png($bmp, $path) { $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose() }

function Draw-Shadow($g, $x, $y, $w, $h) {
    $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(90, 0, 0, 0))
    $g.FillEllipse($brush, $x, $y + $h - 8, $w, 14)
    $brush.Dispose()
}

function New-PlayerFrame($frame, $state) {
    $bmp = New-Object System.Drawing.Bitmap 64, 80
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = 'AntiAlias'
    $g.Clear([System.Drawing.Color]::Transparent)
    Draw-Shadow $g 8 10 48 60
    $body = [System.Drawing.Color]::FromArgb(30, 90, 200)
    $skin = [System.Drawing.Color]::FromArgb(255, 205, 165)
    $shorts = [System.Drawing.Color]::FromArgb(220, 220, 230)
    $leg = [Math]::Sin($frame * 0.8) * 6
    if ($state -eq 'fall') {
        $g.FillEllipse((New-Object System.Drawing.SolidBrush $body), 10, 45, 44, 22)
        $g.FillEllipse((New-Object System.Drawing.SolidBrush $skin), 40, 38, 20, 20)
    } else {
        $g.FillRectangle((New-Object System.Drawing.SolidBrush $body), 18, 22, 28, 30)
        $g.FillRectangle((New-Object System.Drawing.SolidBrush $shorts), 16, 48, 32, 16)
        $g.FillEllipse((New-Object System.Drawing.SolidBrush $skin), 21, 5, 22, 22)
        $g.FillRectangle((New-Object System.Drawing.SolidBrush $shorts), 20, 60, 10, (14 + $leg))
        $g.FillRectangle((New-Object System.Drawing.SolidBrush $shorts), 34, 60, 10, (14 - $leg))
    }
    $g.Dispose(); return $bmp
}

function New-EnemyFrame($frame, $variant, $state) {
    $colors = @(
        @([System.Drawing.Color]::FromArgb(200,40,40), [System.Drawing.Color]::FromArgb(180,30,30)),
        @([System.Drawing.Color]::FromArgb(40,160,60), [System.Drawing.Color]::FromArgb(30,130,50)),
        @([System.Drawing.Color]::FromArgb(200,140,30), [System.Drawing.Color]::FromArgb(170,110,20))
    )
    $body, $shorts = $colors[$variant % 3]
    $bmp = New-Object System.Drawing.Bitmap 64, 80
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = 'AntiAlias'
    $g.Clear([System.Drawing.Color]::Transparent)
    Draw-Shadow $g 8 10 48 60
    $skin = [System.Drawing.Color]::FromArgb(240, 190, 150)
    if ($state -eq 'slide') {
        $g.FillEllipse((New-Object System.Drawing.SolidBrush $body), 5, 50, 50, 18)
        $g.FillEllipse((New-Object System.Drawing.SolidBrush $skin), 43, 43, 18, 18)
    } else {
        $leg = [Math]::Sin($frame * 0.9 + $variant) * 7
        $g.FillRectangle((New-Object System.Drawing.SolidBrush $body), 18, 22, 28, 28)
        $g.FillRectangle((New-Object System.Drawing.SolidBrush $shorts), 16, 46, 32, 14)
        $g.FillEllipse((New-Object System.Drawing.SolidBrush $skin), 22, 5, 20, 20)
        $g.FillRectangle((New-Object System.Drawing.SolidBrush $shorts), 20, 58, 10, (14 + $leg))
        $g.FillRectangle((New-Object System.Drawing.SolidBrush $shorts), 34, 58, 10, (14 - $leg))
    }
    $g.Dispose(); return $bmp
}

function New-BallFrame($frame) {
    $bmp = New-Object System.Drawing.Bitmap 28, 28
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = 'AntiAlias'
    $g.Clear([System.Drawing.Color]::Transparent)
    $g.FillEllipse((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::White)), 3, 1, 22, 22)
    $pen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(30,30,30)), 2
    for ($i = 0; $i -lt 5; $i++) {
        $a = $frame * 0.6 + $i * 1.256
        $px = 14 + [Math]::Cos($a) * 7
        $py = 12 + [Math]::Sin($a) * 7
        $g.FillEllipse((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(30,30,30))), ($px-3), ($py-3), 6, 6)
    }
    $g.DrawEllipse($pen, 3, 1, 22, 22)
    $g.Dispose(); return $bmp
}

function Save-Sheet($frames, $fw, $fh, $path) {
    $count = $frames.Count
    $sheet = New-Object System.Drawing.Bitmap ($fw * $count), $fh
    $g = [System.Drawing.Graphics]::FromImage($sheet)
    $g.Clear([System.Drawing.Color]::Transparent)
    for ($i = 0; $i -lt $count; $i++) { $g.DrawImage($frames[$i], $i * $fw, 0) }
    $g.Dispose()
    Save-Png $sheet $path
    foreach ($f in $frames) { $f.Dispose() }
}

# Player sheets
@(@('idle',4), @('run',8), @('dribble',8), @('fall',6)) | ForEach-Object {
    $st, $n = $_
    $frames = 0..($n-1) | ForEach-Object { New-PlayerFrame $_ $(if($st -eq 'dribble'){'dribble'}else{$st}) }
    Save-Sheet $frames 64 80 (Join-Path $imgDir "player_$st.png")
}

# Enemy sheets
0..2 | ForEach-Object {
    $v = $_
    @(@('run',8), @('slide',5), @('recover',4)) | ForEach-Object {
        $st, $n = $_
        $frames = 0..($n-1) | ForEach-Object { New-EnemyFrame $_ $v $st }
        Save-Sheet $frames 64 80 (Join-Path $imgDir "enemy_${v}_$st.png")
    }
}

# Ball
$ballFrames = 0..7 | ForEach-Object { New-BallFrame $_ }
Save-Sheet $ballFrames 28 28 (Join-Path $imgDir "ball.png")

# Buttons
@(@('play',60,180,90), @('ranking',60,130,220), @('credits',200,160,50), @('exit',200,70,70), @('back',100,110,130)) | ForEach-Object {
    $name, $r, $g, $b = $_
    $bmp = New-Object System.Drawing.Bitmap 280, 56
    $gr = [System.Drawing.Graphics]::FromImage($bmp)
    $gr.SmoothingMode = 'AntiAlias'
    $gr.Clear([System.Drawing.Color]::Transparent)
    $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb($r,$g,$b))
    $gr.FillRectangle($brush, 0, 0, 280, 56)
    $gr.Dispose(); Save-Png $bmp (Join-Path $imgDir "btn_$name.png")
}

# Backgrounds
$sw, $sh = 1280, 720
foreach ($bgName in @('menu_bg','ranking_bg','gameover_bg')) {
    $bmp = New-Object System.Drawing.Bitmap $sw, $sh
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    for ($y = 0; $y -lt $sh; $y++) {
        $t = $y / $sh
        $c = [System.Drawing.Color]::FromArgb(([int](20+$t*30)), ([int](60+$t*80)), ([int](100+$t*40)))
        $pen = New-Object System.Drawing.Pen $c
        $g.DrawLine($pen, 0, $y, $sw, $y)
        $pen.Dispose()
    }
    $g.Dispose(); Save-Png $bmp (Join-Path $imgDir "$bgName.png")
}

# Field
$field = New-Object System.Drawing.Bitmap 1680, 500
$g = [System.Drawing.Graphics]::FromImage($field)
$tile = New-Object System.Drawing.Bitmap 128, 128
$gt = [System.Drawing.Graphics]::FromImage($tile)
for ($y=0; $y -lt 128; $y++) { for ($x=0; $x -lt 128; $x++) {
    $stripe = (([int](($x+$y)/16)) % 2)
    if ($stripe) { $c = [System.Drawing.Color]::FromArgb(42,138,58) } else { $c = [System.Drawing.Color]::FromArgb(36,118,50) }
    $tile.SetPixel($x,$y,$c)
}}
$gt.Dispose()
for ($x=0; $x -lt 1680; $x+=128) { for ($y=0; $y -lt 500; $y+=128) { $g.DrawImage($tile, $x, $y) }}
$tile.Dispose()
$g.Dispose(); Save-Png $field (Join-Path $imgDir "field.png")

# Icons, sign, particle, logo
foreach ($icon in @('score','time','speed','record')) {
    $bmp = New-Object System.Drawing.Bitmap 32, 32
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = 'AntiAlias'
    $g.Clear([System.Drawing.Color]::Transparent)
    $g.FillEllipse((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255,210,80))), 2, 2, 28, 28)
    $g.Dispose(); Save-Png $bmp (Join-Path $imgDir "icon_$icon.png")
}

$sign = New-Object System.Drawing.Bitmap 80, 100
$g = [System.Drawing.Graphics]::FromImage($sign)
$g.Clear([System.Drawing.Color]::Transparent)
$g.FillRectangle((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(180,140,60))), 10, 20, 60, 70)
$g.Dispose(); Save-Png $sign (Join-Path $imgDir "sign_goal.png")

$part = New-Object System.Drawing.Bitmap 8, 8
$g = [System.Drawing.Graphics]::FromImage($part)
$g.Clear([System.Drawing.Color]::Transparent)
$g.FillEllipse((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(200,255,255,200))), 0, 0, 8, 8)
$g.Dispose(); Save-Png $part (Join-Path $imgDir "particle.png")

# Logo
$logo = New-Object System.Drawing.Bitmap 500, 120
$g = [System.Drawing.Graphics]::FromImage($logo)
$g.SmoothingMode = 'AntiAlias'
$g.Clear([System.Drawing.Color]::Transparent)
$font = New-Object System.Drawing.Font 'Arial', 36, [System.Drawing.FontStyle]::Bold
$g.DrawString('FUTEBOL', $font, (New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::White)), 20, 10)
$g.DrawString('RUNNER', $font, (New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(80,220,120))), 200, 55)
$g.Dispose(); Save-Png $logo (Join-Path $imgDir "logo.png")

# WAV generator
function Write-Tone($path, $freq, $dur, $vol=0.4) {
    $rate = 22050
    $samples = [int]($rate * $dur)
    $ms = New-Object System.IO.MemoryStream
    $bw = New-Object System.IO.BinaryWriter $ms
    $bw.Write([char[]]@('R','I','F','F'))
    $bw.Write([int]0)
    $bw.Write([char[]]@('W','A','V','E','f','m','t',' '))
    $bw.Write([int]16); $bw.Write([int16]1); $bw.Write([int16]1)
    $bw.Write([int]$rate); $bw.Write([int]($rate*2)); $bw.Write([int16]2); $bw.Write([int16]16)
    $bw.Write([char[]]@('d','a','t','a'))
    $dataStart = $ms.Position; $bw.Write([int]0)
    for ($i=0; $i -lt $samples; $i++) {
        $t = $i / $rate
        $env = [Math]::Min(1.0, $t*20) * [Math]::Max(0.0, 1.0 - ($t/$dur)*0.8)
        $val = [Math]::Sin(2*[Math]::PI*$freq*$t) * $vol * $env
        $val = [Math]::Max(-1, [Math]::Min(1, $val))
        $bw.Write([int16]($val * 32767))
    }
    $dataEnd = $ms.Position
    $ms.Position = 4; $bw.Write([int]($dataEnd - 8))
    $ms.Position = $dataStart; $bw.Write([int]($dataEnd - $dataStart - 4))
    [IO.File]::WriteAllBytes($path, $ms.ToArray())
    $bw.Close(); $ms.Close()
}

Write-Tone (Join-Path $sndDir "click.wav") 880 0.08
Write-Tone (Join-Path $sndDir "kick.wav") 120 0.15 0.5
Write-Tone (Join-Path $sndDir "ball.wav") 300 0.1
Write-Tone (Join-Path $sndDir "slide.wav") 200 0.35 0.45
Write-Tone (Join-Path $sndDir "collision.wav") 80 0.4 0.6
Write-Tone (Join-Path $sndDir "gameover.wav") 150 0.8 0.4
Write-Tone (Join-Path $sndDir "menu_music.wav") 262 4.0 0.12
Write-Tone (Join-Path $sndDir "game_music.wav") 196 6.0 0.1

Write-Host "Assets gerados em $root"

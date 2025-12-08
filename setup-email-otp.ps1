# Quick Email OTP Setup Script
# This script helps you set up email configuration for OTP verification

Write-Host "`n==================================" -ForegroundColor Cyan
Write-Host "  AgriCure OTP Email Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

Write-Host "`nThis script will help you configure email for OTP verification.`n" -ForegroundColor Yellow

# Check if .env exists
$envPath = "$PSScriptRoot\.env"
if (-not (Test-Path $envPath)) {
  Write-Host "Error: .env file not found!" -ForegroundColor Red
  Write-Host "Please ensure you're in the Backend directory." -ForegroundColor Yellow
  exit 1
}

Write-Host "Found .env file: $envPath`n" -ForegroundColor Green

# Email service selection
Write-Host "Select Email Service:" -ForegroundColor Cyan
Write-Host "1. Gmail (Recommended for development)" -ForegroundColor White
Write-Host "2. Custom SMTP" -ForegroundColor White
Write-Host "3. Skip (Configure manually later)" -ForegroundColor Gray
$choice = Read-Host "`nEnter choice (1-3)"

if ($choice -eq "1") {
  Write-Host "`n--- Gmail Setup ---" -ForegroundColor Cyan
  Write-Host "Before proceeding, make sure you have:" -ForegroundColor Yellow
  Write-Host "1. Enabled 2-Step Verification on your Google Account" -ForegroundColor White
  Write-Host "2. Generated an App Password at: https://myaccount.google.com/apppasswords`n" -ForegroundColor White
    
  $continue = Read-Host "Have you completed these steps? (y/n)"
    
  if ($continue -eq "y" -or $continue -eq "Y") {
    $email = Read-Host "Enter your Gmail address"
    $password = Read-Host "Enter your App Password (16 characters)" -MaskInput
        
    # Update .env file
    $envContent = Get-Content $envPath -Raw
        
    # Remove existing email config if present
    $envContent = $envContent -replace "EMAIL_SERVICE=.*`n", ""
    $envContent = $envContent -replace "EMAIL_USER=.*`n", ""
    $envContent = $envContent -replace "EMAIL_PASSWORD=.*`n", ""
    $envContent = $envContent -replace "SMTP_HOST=.*`n", ""
    $envContent = $envContent -replace "SMTP_PORT=.*`n", ""
    $envContent = $envContent -replace "SMTP_SECURE=.*`n", ""
        
    # Add new email config
    $emailConfig = @"

# Email Configuration for OTP
EMAIL_SERVICE=gmail
EMAIL_USER=$email
EMAIL_PASSWORD=$password
"@
        
    $envContent = $envContent.TrimEnd() + $emailConfig
        
    Set-Content -Path $envPath -Value $envContent -NoNewline
        
    Write-Host "`n✅ Gmail configuration saved!" -ForegroundColor Green
    Write-Host "Email: $email" -ForegroundColor White
  }
  else {
    Write-Host "`nPlease complete the setup steps first:" -ForegroundColor Yellow
    Write-Host "1. Go to https://myaccount.google.com/security" -ForegroundColor White
    Write-Host "2. Enable 2-Step Verification" -ForegroundColor White
    Write-Host "3. Go to https://myaccount.google.com/apppasswords" -ForegroundColor White
    Write-Host "4. Create an App Password for 'Mail'" -ForegroundColor White
    Write-Host "5. Run this script again`n" -ForegroundColor White
    exit 0
  }
    
}
elseif ($choice -eq "2") {
  Write-Host "`n--- Custom SMTP Setup ---" -ForegroundColor Cyan
    
  $smtpHost = Read-Host "Enter SMTP Host (e.g., smtp.example.com)"
  $smtpPort = Read-Host "Enter SMTP Port (usually 587 or 465)"
  $smtpSecure = Read-Host "Use secure connection? (y/n)"
  $email = Read-Host "Enter email address"
  $password = Read-Host "Enter SMTP password" -MaskInput
    
  # Update .env file
  $envContent = Get-Content $envPath -Raw
    
  # Remove existing email config if present
  $envContent = $envContent -replace "EMAIL_SERVICE=.*`n", ""
  $envContent = $envContent -replace "EMAIL_USER=.*`n", ""
  $envContent = $envContent -replace "EMAIL_PASSWORD=.*`n", ""
  $envContent = $envContent -replace "SMTP_HOST=.*`n", ""
  $envContent = $envContent -replace "SMTP_PORT=.*`n", ""
  $envContent = $envContent -replace "SMTP_SECURE=.*`n", ""
    
  $secureValue = if ($smtpSecure -eq "y" -or $smtpSecure -eq "Y") { "true" } else { "false" }
    
  # Add new email config
  $emailConfig = @"

# Email Configuration for OTP
EMAIL_SERVICE=smtp
SMTP_HOST=$smtpHost
SMTP_PORT=$smtpPort
SMTP_SECURE=$secureValue
EMAIL_USER=$email
EMAIL_PASSWORD=$password
"@
    
  $envContent = $envContent.TrimEnd() + $emailConfig
    
  Set-Content -Path $envPath -Value $envContent -NoNewline
    
  Write-Host "`n✅ SMTP configuration saved!" -ForegroundColor Green
  Write-Host "Host: $smtpHost" -ForegroundColor White
  Write-Host "Port: $smtpPort" -ForegroundColor White
  Write-Host "Email: $email" -ForegroundColor White
    
}
else {
  Write-Host "`nSkipping automatic configuration." -ForegroundColor Yellow
  Write-Host "Please edit .env manually and add:" -ForegroundColor White
  Write-Host @"

EMAIL_SERVICE=gmail
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

"@ -ForegroundColor Gray
}

Write-Host "`n==================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Start the backend server: npm start" -ForegroundColor White
Write-Host "2. Test signup with OTP verification" -ForegroundColor White
Write-Host "3. Check your email for the OTP code" -ForegroundColor White
Write-Host "`nFor detailed documentation, see: EMAIL_OTP_SETUP.md`n" -ForegroundColor Cyan

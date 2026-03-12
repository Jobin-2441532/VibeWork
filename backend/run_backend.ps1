$env:EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
$env:EMAIL_HOST="smtp.gmail.com"
$env:EMAIL_PORT="587"
$env:EMAIL_USE_TLS="True"
$env:EMAIL_HOST_USER="jobin.sam@bcah.christuniversity.in"
$env:EMAIL_HOST_PASSWORD="wqgx ehaz efrq hyaz"
$env:DEFAULT_FROM_EMAIL="jobin.sam@bcah.christuniversity.in"

Write-Host "Starting Django Server with Real Email Delivery..." -ForegroundColor Green
venv\Scripts\python.exe manage.py runserver

param(
    [int]$Port = 8001
)

Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
python -m pip install -r requirements.txt

Write-Host "Applying database migrations..." -ForegroundColor Cyan
python manage.py migrate

Write-Host "Starting Django development server on port $Port..." -ForegroundColor Cyan
python manage.py runserver $Port


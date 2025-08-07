@echo off
REM Battery Repair ERP - Docker Startup Script for Windows
REM Just run this script - no configuration needed!

echo 🔋 Battery Repair ERP - Starting Docker Setup...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose not found. Please install Docker Compose.
    pause
    exit /b 1
)

echo ✅ Docker is ready

REM Stop any existing containers
echo 🛑 Stopping any existing containers...
docker-compose down

REM Build and start the application
echo 🏗️  Building and starting Battery Repair ERP...
docker-compose up -d --build

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check if services are running
docker-compose ps | findstr "Up" >nul
if not errorlevel 1 (
    echo ✅ Battery Repair ERP is now running!
    echo.
    echo 🌐 Access your application at: http://localhost:5000
    echo.
    echo 👤 Default Login Credentials:
    echo    Admin:      username: admin      password: admin123
    echo    Staff:      username: staff      password: staff123
    echo    Technician: username: technician password: tech123
    echo.
    echo 📝 Useful Commands:
    echo    View logs:    docker-compose logs -f web
    echo    Stop app:     docker-compose down
    echo    Restart app:  docker-compose restart
    echo.
    echo 🎉 Setup complete! Your Battery Repair ERP is ready to use.
) else (
    echo ❌ Something went wrong. Check the logs:
    echo    docker-compose logs
)

pause
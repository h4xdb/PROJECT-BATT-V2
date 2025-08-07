#!/bin/bash

# Battery Repair ERP - Docker Startup Script
# Just run this script - no configuration needed!

echo "🔋 Battery Repair ERP - Starting Docker Setup..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ Docker Compose not found. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker is ready"

# Stop any existing containers
echo "🛑 Stopping any existing containers..."
docker-compose down

# Build and start the application
echo "🏗️  Building and starting Battery Repair ERP..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Battery Repair ERP is now running!"
    echo ""
    echo "🌐 Access your application at: http://localhost:5000"
    echo ""
    echo "👤 Default Login Credentials:"
    echo "   Admin:      username: admin      password: admin123"
    echo "   Staff:      username: staff      password: staff123"
    echo "   Technician: username: technician password: tech123"
    echo ""
    echo "📝 Useful Commands:"
    echo "   View logs:    docker-compose logs -f web"
    echo "   Stop app:     docker-compose down"
    echo "   Restart app:  docker-compose restart"
    echo ""
    echo "🎉 Setup complete! Your Battery Repair ERP is ready to use."
else
    echo "❌ Something went wrong. Check the logs:"
    echo "   docker-compose logs"
fi
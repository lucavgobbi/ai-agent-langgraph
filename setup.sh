#!/bin/bash

# Setup script for Basic AI Agent with LangGraph and Azure OpenAI

echo "🚀 Setting up Basic AI Agent with LangGraph and Azure OpenAI"
echo "============================================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Check if virtual environment was created successfully
if [ ! -d "venv" ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📈 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Dependencies installed successfully!"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your Azure OpenAI credentials"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your Azure OpenAI credentials"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the agent: python agent.py"
echo ""
echo "To deactivate the virtual environment later, run: deactivate"

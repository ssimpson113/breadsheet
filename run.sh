#!/bin/bash
# Simple launcher for Breadsheet on Linux

echo "🍞 Starting Breadsheet Baking Calculator..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Streamlit not found. Installing..."
    pip install streamlit
    echo ""
fi

# Run the app
streamlit run app.py

#!/bin/bash
# Stop AgentSmith Web GUI
# Kills the Flask server, clears port, and cleans cache

echo "🛑 Stopping AgentSmith Web GUI..."
echo "================================"
echo ""

# Function to kill process on port
kill_port() {
    local port=$1
    echo "🔍 Checking port $port..."

    # Find process using the port
    local pid=$(lsof -ti:$port)

    if [ -n "$pid" ]; then
        echo "   Found process $pid on port $port"
        kill -9 $pid 2>/dev/null
        sleep 1

        # Verify it's killed
        if lsof -ti:$port > /dev/null 2>&1; then
            echo "   ⚠️  Process still running, trying harder..."
            sudo kill -9 $pid 2>/dev/null
        else
            echo "   ✅ Killed process on port $port"
        fi
    else
        echo "   No process on port $port"
    fi
}

# Kill Python processes running web_gui.py
echo "🔍 Looking for web_gui.py processes..."
pgrep -f "python.*web_gui.py" | while read pid; do
    echo "   Killing Python process: $pid"
    kill -9 $pid 2>/dev/null
done

# Kill processes on Flask default port (5000)
kill_port 5000

# Also check common alternative ports
kill_port 5001
kill_port 8080

echo ""
echo "🧹 Clearing cache..."

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null

# Clear Flask cache
rm -rf instance/ 2>/dev/null
rm -rf .webassets-cache/ 2>/dev/null

# Clear temporary files
rm -rf *.tmp 2>/dev/null
rm -rf /tmp/flask_* 2>/dev/null

echo "   ✅ Cache cleared"

echo ""
echo "🔍 Verifying shutdown..."

# Check if any processes are still running
if pgrep -f "python.*web_gui.py" > /dev/null; then
    echo "   ⚠️  Some processes may still be running"
    echo "   Active web_gui processes:"
    pgrep -lf "python.*web_gui.py"
else
    echo "   ✅ All web GUI processes stopped"
fi

# Check port status (but ignore system services)
if lsof -ti:5000 > /dev/null 2>&1; then
    # Check if it's our Flask app or system service
    flask_process=$(lsof -i:5000 | grep -i "python\|flask" || true)
    if [ -n "$flask_process" ]; then
        echo "   ⚠️  Flask still running on port 5000"
        echo "$flask_process"
    else
        system_process=$(lsof -i:5000 | grep -i "ControlCe" || true)
        if [ -n "$system_process" ]; then
            echo "   ℹ️  Port 5000 in use by macOS Control Center (safe to ignore)"
        else
            echo "   ⚠️  Port 5000 in use by unknown process"
            lsof -i:5000
        fi
    fi
else
    echo "   ✅ Port 5000 is free"
fi

echo ""
echo "================================"
echo "✅ Web GUI shutdown complete!"
echo ""
echo "💡 To start again, run: ./launch_web_gui.sh"
echo ""

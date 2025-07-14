#!/bin/bash

# shutdown-services.sh
# Comprehensive shutdown script for ValidatedPatterns RAG services

set -e

echo "🛑 Shutting down ValidatedPatterns RAG services..."

# Function to check if a process exists
process_exists() {
    pgrep -f "$1" > /dev/null 2>&1
}

# Function to kill processes by name pattern
kill_processes() {
    local pattern="$1"
    local service_name="$2"
    
    if process_exists "$pattern"; then
        echo "🔄 Stopping $service_name..."
        pkill -f "$pattern" 2>/dev/null || true
        sleep 2
        
        # Force kill if still running
        if process_exists "$pattern"; then
            echo "⚠️  Force killing $service_name..."
            pkill -9 -f "$pattern" 2>/dev/null || true
            sleep 1
        fi
        
        if ! process_exists "$pattern"; then
            echo "✅ $service_name stopped successfully"
        else
            echo "❌ Failed to stop $service_name"
        fi
    else
        echo "ℹ️  $service_name is not running"
    fi
}

# 1. Stop Flask Web UI processes
echo
echo "1️⃣ Stopping Flask Web UI..."
kill_processes "rag_web_ui.py" "Flask Web UI"
kill_processes "python.*rag_web_ui" "Flask Web UI processes"

# 2. Stop Podman container with llama-stack
echo
echo "2️⃣ Stopping Llama Stack container..."
if command -v podman &> /dev/null; then
    # Check if container is running
    if podman ps --format "{{.Names}}" | grep -q "llamastack" 2>/dev/null; then
        echo "🔄 Stopping llamastack container..."
        podman stop llamastack 2>/dev/null || true
        sleep 2
    fi
    
    # Check for any running containers with llama-stack distribution
    CONTAINERS=$(podman ps --format "{{.ID}} {{.Image}}" | grep "llamastack/distribution" | awk '{print $1}' || true)
    if [ -n "$CONTAINERS" ]; then
        echo "🔄 Stopping llama-stack containers..."
        echo "$CONTAINERS" | xargs -r podman stop 2>/dev/null || true
        sleep 2
    fi
    
    # Force kill any remaining podman processes related to llama-stack
    kill_processes "podman.*llamastack" "Podman llama-stack processes"
    
    echo "✅ Llama Stack container stopped"
else
    echo "ℹ️  Podman not found, skipping container shutdown"
fi

# 3. Stop Ollama processes
echo
echo "3️⃣ Stopping Ollama..."
kill_processes "ollama serve" "Ollama server"
kill_processes "ollama" "Ollama processes"

# 4. Clean up any remaining Python processes related to our project
echo
echo "4️⃣ Cleaning up remaining processes..."
kill_processes "python.*rag_agent" "RAG agent processes"
kill_processes "llama.*stack" "Llama stack processes"

# 5. Check for any remaining processes on ports 8080, 8321, 11434
echo
echo "5️⃣ Checking for processes on key ports..."
check_port() {
    local port="$1"
    local service="$2"
    
    if lsof -ti:$port > /dev/null 2>&1; then
        echo "⚠️  Port $port ($service) is still in use, attempting to free..."
        lsof -ti:$port | xargs -r kill -9 2>/dev/null || true
        sleep 1
        
        if lsof -ti:$port > /dev/null 2>&1; then
            echo "❌ Failed to free port $port"
        else
            echo "✅ Port $port freed"
        fi
    else
        echo "✅ Port $port is free"
    fi
}

check_port 8080 "Flask Web UI"
check_port 8321 "Llama Stack"
check_port 11434 "Ollama"

echo
echo "🎉 Shutdown complete!"
echo
echo "📊 Final process check:"
echo "Flask UI: $(pgrep -f 'rag_web_ui.py' | wc -l | xargs) processes"
echo "Ollama: $(pgrep -f 'ollama' | wc -l | xargs) processes"
echo "Podman: $(pgrep -f 'podman.*llamastack' | wc -l | xargs) processes"
echo

# Optional: Show any remaining related processes
REMAINING=$(pgrep -f "(rag_|ollama|llama.*stack)" 2>/dev/null | wc -l | xargs)
if [ "$REMAINING" -gt 0 ]; then
    echo "⚠️  $REMAINING related processes still running:"
    pgrep -f "(rag_|ollama|llama.*stack)" -l 2>/dev/null || true
    echo
    echo "💡 If needed, you can force kill them with:"
    echo "   pkill -9 -f 'rag_|ollama|llama.*stack'"
else
    echo "✅ All services successfully stopped"
fi

echo
echo "🚀 To restart services, run:"
echo "   1. ollama serve"
echo "   2. ./run-llama-server.sh"
echo "   3. python rag_web_ui.py" 
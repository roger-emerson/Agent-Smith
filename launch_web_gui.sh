#!/bin/bash
# Launch AgentSmith Web GUI

cd "$(dirname "$0")"
source venv/bin/activate
python web_gui.py

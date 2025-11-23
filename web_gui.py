"""
AgentSmith - Web-Based GUI
Modern web interface for Email AI Agent
"""

from flask import Flask, render_template, jsonify, request
import sys
import os
import threading
import json
import webbrowser
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent import EmailAgent
import prompts as prompt_module

app = Flask(__name__)
app.config['SECRET_KEY'] = 'agentsmith-secret-key'

# Global state
agent = None
emails = []
analysis_results = {}


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/connect', methods=['POST'])
def connect():
    """Connect to Gmail and Claude"""
    global agent
    try:
        if not agent:
            agent = EmailAgent()
        return jsonify({'success': True, 'message': 'Connected successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/fetch_emails', methods=['POST'])
def fetch_emails():
    """Fetch emails from Gmail"""
    global agent, emails
    try:
        if not agent:
            return jsonify({'success': False, 'error': 'Not connected. Please connect first.'})

        data = request.json
        max_emails = data.get('max_emails', 30)

        emails = agent.gmail.get_unread_emails(max_results=max_emails)

        email_list = [{
            'id': email['id'],
            'subject': email['subject'],
            'from': email['from'],
            'date': email['date'],
            'snippet': email['snippet']
        } for email in emails]

        return jsonify({'success': True, 'emails': email_list, 'count': len(emails)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/email/<email_id>')
def get_email(email_id):
    """Get email details"""
    global emails
    try:
        email = next((e for e in emails if e['id'] == email_id), None)
        if email:
            return jsonify({'success': True, 'email': email})
        else:
            return jsonify({'success': False, 'error': 'Email not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/analyze/<email_id>', methods=['POST'])
def analyze_email(email_id):
    """Analyze a single email"""
    global agent, emails, analysis_results
    try:
        if not agent:
            return jsonify({'success': False, 'error': 'Not connected'})

        email = next((e for e in emails if e['id'] == email_id), None)
        if not email:
            return jsonify({'success': False, 'error': 'Email not found'})

        analysis = agent.analyze_email(email)
        analysis_results[email_id] = analysis

        return jsonify({'success': True, 'analysis': analysis})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/analyze_all', methods=['POST'])
def analyze_all():
    """Analyze all emails"""
    global agent, emails, analysis_results
    try:
        if not agent:
            return jsonify({'success': False, 'error': 'Not connected'})

        results = []
        for email in emails:
            analysis = agent.analyze_email(email)
            analysis_results[email['id']] = analysis
            results.append({
                'email_id': email['id'],
                'analysis': analysis
            })

        return jsonify({'success': True, 'results': results, 'count': len(results)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/prompts')
def get_prompts():
    """Get available prompts"""
    return jsonify({
        'success': True,
        'prompts': {
            'email_analysis': 'Email Analysis',
            'reply_draft': 'Reply Draft',
            'summary': 'Inbox Summary',
            'smart_filter': 'Smart Filter'
        }
    })


@app.route('/api/prompt/<prompt_type>')
def get_prompt(prompt_type):
    """Get a specific prompt template"""
    try:
        sample_email = {
            'subject': 'Sample Subject',
            'from': 'sample@example.com',
            'body': 'Sample email body...',
            'snippet': 'Sample snippet...',
            'date': 'Today'
        }

        if prompt_type == 'email_analysis':
            prompt = prompt_module.get_email_analysis_prompt(sample_email)
        elif prompt_type == 'reply_draft':
            prompt = prompt_module.get_reply_draft_prompt(sample_email)
        elif prompt_type == 'summary':
            prompt = prompt_module.get_summary_prompt([sample_email])
        elif prompt_type == 'smart_filter':
            prompt = prompt_module.get_smart_filter_prompt(sample_email)
        else:
            return jsonify({'success': False, 'error': 'Unknown prompt type'})

        return jsonify({'success': True, 'prompt': prompt})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/stats')
def get_stats():
    """Get statistics"""
    global emails, analysis_results

    categories = {}
    priorities = {}

    for email_id, analysis in analysis_results.items():
        cat = analysis.get('category', 'Unknown')
        pri = analysis.get('priority', 'unknown')

        categories[cat] = categories.get(cat, 0) + 1
        priorities[pri] = priorities.get(pri, 0) + 1

    return jsonify({
        'success': True,
        'stats': {
            'total_emails': len(emails),
            'analyzed': len(analysis_results),
            'categories': categories,
            'priorities': priorities
        }
    })


def open_browser():
    """Open browser after a short delay"""
    import time
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')


def find_available_port(start_port=5000, max_attempts=10):
    """Find an available port starting from start_port"""
    import socket
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('127.0.0.1', port))
            sock.close()
            return port
        except OSError:
            continue
    return None


if __name__ == '__main__':
    # Find available port
    port = find_available_port(5000)

    if port is None:
        print("\n❌ Error: Could not find available port")
        print("Ports 5000-5010 are all in use.")
        print("Please free up a port or specify a different port range.\n")
        exit(1)

    # Update browser URL if not on default port
    def open_browser_with_port():
        import time
        time.sleep(1.5)
        webbrowser.open(f'http://127.0.0.1:{port}')

    # Open browser in a separate thread
    threading.Thread(target=open_browser_with_port, daemon=True).start()

    print("\n" + "=" * 60)
    print("🤖 AgentSmith Web GUI Starting...")
    print("=" * 60)
    print(f"\n📱 Opening browser at: http://127.0.0.1:{port}")
    if port != 5000:
        print(f"   ℹ️  Using port {port} (default 5000 was in use)")
    print("\n💡 Press Ctrl+C to stop the server\n")

    app.run(debug=False, port=port, host='127.0.0.1')

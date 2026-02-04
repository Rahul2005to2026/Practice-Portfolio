from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from datetime import datetime

app = Flask(__name__)

# Create necessary directories
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Sample data for API endpoints
PROJECTS = [
    {
        "id": 1,
        "title": "TaskFlow Dashboard",
        "description": "Productivity dashboard with real-time collaboration features",
        "tags": ["React", "Node.js", "MongoDB"],
        "type": "Web App"
    },
    {
        "id": 2,
        "title": "UrbanShop",
        "description": "Modern e-commerce platform with cart and payment integration",
        "tags": ["HTML/CSS", "JavaScript", "Stripe API"],
        "type": "E-commerce"
    },
    {
        "id": 3,
        "title": "WeatherWise App",
        "description": "Weather application with location-based forecasts",
        "tags": ["React Native", "API Integration", "UI Design"],
        "type": "Mobile"
    }
]

SKILLS = {
    "frontend": [
        {"name": "HTML5/CSS3", "level": 95},
        {"name": "JavaScript", "level": 90},
        {"name": "React", "level": 85}
    ],
    "backend": [
        {"name": "Python", "level": 88},
        {"name": "Node.js", "level": 82},
        {"name": "PostgreSQL", "level": 75}
    ],
    "tools": [
        {"name": "Git/GitHub", "level": 92},
        {"name": "VS Code", "level": 95},
        {"name": "Figma", "level": 80}
    ]
}

# Routes
@app.route('/')
def home():
    """Serve the main portfolio page"""
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def serve_css():
    """Serve CSS file"""
    return send_from_directory('.', 'style.css')

@app.route('/api/projects')
def get_projects():
    """API endpoint for projects"""
    return jsonify({
        "success": True,
        "projects": PROJECTS,
        "count": len(PROJECTS)
    })

@app.route('/api/skills')
def get_skills():
    """API endpoint for skills"""
    return jsonify({
        "success": True,
        "skills": SKILLS
    })

@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "No data received"
            }), 400
        
        # Get form data
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', 'No Subject').strip()
        message = data.get('message', '').strip()
        
        # Validate required fields
        if not name or not email or not message:
            return jsonify({
                "success": False,
                "message": "Please fill in all required fields"
            }), 400
        
        # Log the submission (in production, save to database)
        submission = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "ip": request.remote_addr
        }
        
        # Save to a JSON file (for demo purposes)
        try:
            with open('submissions.json', 'a') as f:
                f.write(json.dumps(submission) + '\n')
        except:
            pass  # Ignore file errors in demo
        
        print(f"New contact submission: {name} <{email}> - {subject}")
        
        return jsonify({
            "success": True,
            "message": "Thank you for your message! I'll get back to you soon."
        })
        
    except Exception as e:
        print(f"Error processing contact form: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An error occurred. Please try again later."
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get portfolio statistics"""
    return jsonify({
        "success": True,
        "stats": {
            "projects": len(PROJECTS),
            "experience_years": 4,
            "clients": 15,
            "skills": len(SKILLS['frontend']) + len(SKILLS['backend']) + len(SKILLS['tools'])
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "portfolio-backend",
        "timestamp": datetime.now().isoformat()
    })

# Static file serving
@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "File not found", 404

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    print("Starting Portfolio Server...")
    print("=" * 50)
    print("Local URL: http://localhost:5000")
    print("API Endpoints:")
    print("  - GET  /api/projects  - List all projects")
    print("  - GET  /api/skills    - List all skills")
    print("  - POST /api/contact   - Submit contact form")
    print("  - GET  /api/stats     - Portfolio statistics")
    print("  - GET  /health        - Health check")
    print("=" * 50)
    
    # Create empty submissions file if it doesn't exist
    if not os.path.exists('submissions.json'):
        with open('submissions.json', 'w') as f:
            f.write('')
    
    app.run(debug=True, port=5000)
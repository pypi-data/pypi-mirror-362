"""
DevMe Server - Web dashboard server
"""

from flask import Flask, render_template_string, jsonify
from .core import DevMe


def create_app():
    """Create Flask application"""
    app = Flask(__name__)
    
    @app.route('/')
    def dashboard():
        """Main dashboard page"""
        devme = DevMe()
        status = devme.get_status()
        
        # HTML template for dashboard
        template = """
<!DOCTYPE html>
<html>
<head>
    <title>DevMe - {{ status.project_name }}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; 
                  box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card h3 { margin-top: 0; color: #333; }
        .status-item { display: flex; justify-content: space-between; margin: 10px 0; }
        .status-good { color: #28a745; }
        .status-bad { color: #dc3545; }
        .status-neutral { color: #6c757d; }
        .timestamp { font-size: 0.9em; color: #666; }
        .branch { background: #e9ecef; padding: 4px 8px; border-radius: 4px; 
                  font-family: monospace; font-size: 0.9em; }
        .commit { background: #f8f9fa; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .commit-hash { font-family: monospace; color: #6c757d; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 DevMe - {{ status.project_name }}</h1>
            <p class="timestamp">Last updated: {{ status.last_updated }}</p>
        </div>
        
        <div class="grid">
            <!-- Git Status -->
            <div class="card">
                <h3>📁 Git Repository</h3>
                {% if status.git %}
                    <div class="status-item">
                        <span>Branch:</span>
                        <span class="branch">{{ status.git.current_branch }}</span>
                    </div>
                    <div class="status-item">
                        <span>Status:</span>
                        <span class="{{ 'status-bad' if status.git.is_dirty else 'status-good' }}">
                            {{ 'Dirty' if status.git.is_dirty else 'Clean' }}
                        </span>
                    </div>
                    <div class="status-item">
                        <span>Branches:</span>
                        <span>{{ status.git.total_branches }}</span>
                    </div>
                    <div class="status-item">
                        <span>Untracked files:</span>
                        <span class="{{ 'status-bad' if status.git.untracked_files > 0 else 'status-good' }}">
                            {{ status.git.untracked_files }}
                        </span>
                    </div>
                    
                    {% if status.git.latest_commit %}
                    <div class="commit">
                        <div class="commit-hash">{{ status.git.latest_commit.hash }}</div>
                        <div>{{ status.git.latest_commit.message }}</div>
                        <div class="timestamp">{{ status.git.latest_commit.author }} • {{ status.git.latest_commit.date }}</div>
                    </div>
                    {% endif %}
                {% else %}
                    <div class="status-item">
                        <span class="status-neutral">No git repository found</span>
                    </div>
                {% endif %}
            </div>
            
            <!-- File Status -->
            <div class="card">
                <h3>📄 Project Files</h3>
                <div class="status-item">
                    <span>README:</span>
                    <span class="{{ 'status-good' if status.files.readme else 'status-bad' }}">
                        {{ '✅' if status.files.readme else '❌' }}
                    </span>
                </div>
                <div class="status-item">
                    <span>Tests:</span>
                    <span class="{{ 'status-good' if status.files.tests else 'status-bad' }}">
                        {{ '✅' if status.files.tests else '❌' }}
                    </span>
                </div>
                <div class="status-item">
                    <span>Package config:</span>
                    <span class="{{ 'status-good' if status.files.package_config else 'status-bad' }}">
                        {{ '✅' if status.files.package_config else '❌' }}
                    </span>
                </div>
                <div class="status-item">
                    <span>Environment files:</span>
                    <span class="{{ 'status-good' if status.files.env_files else 'status-neutral' }}">
                        {{ '✅' if status.files.env_files else '➖' }}
                    </span>
                </div>
                <div class="status-item">
                    <span>CI/CD config:</span>
                    <span class="{{ 'status-good' if status.files.ci_config else 'status-neutral' }}">
                        {{ '✅' if status.files.ci_config else '➖' }}
                    </span>
                </div>
                <div class="status-item">
                    <span>Documentation:</span>
                    <span class="{{ 'status-good' if status.files.documentation else 'status-neutral' }}">
                        {{ '✅' if status.files.documentation else '➖' }}
                    </span>
                </div>
            </div>
            
            <!-- Environment Status -->
            <div class="card">
                <h3>🔧 Environment</h3>
                <div class="status-item">
                    <span>Python version:</span>
                    <span>{{ status.environment.python_version }}</span>
                </div>
                <div class="status-item">
                    <span>Virtual environment:</span>
                    <span class="{{ 'status-good' if status.environment.virtual_env else 'status-neutral' }}">
                        {{ '✅' if status.environment.virtual_env else '➖' }}
                    </span>
                </div>
                {% if status.environment.git_config %}
                <div class="status-item">
                    <span>Git user:</span>
                    <span>{{ status.environment.git_config.user_name }}</span>
                </div>
                <div class="status-item">
                    <span>Git email:</span>
                    <span>{{ status.environment.git_config.user_email }}</span>
                </div>
                {% endif %}
            </div>
            
            <!-- Project Stats -->
            <div class="card">
                <h3>📊 Project Stats</h3>
                <div class="status-item">
                    <span>Total files:</span>
                    <span>{{ status.file_count }}</span>
                </div>
                <div class="status-item">
                    <span>Project path:</span>
                    <span style="font-family: monospace; font-size: 0.9em;">{{ status.path }}</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        return render_template_string(template, status=status)
    
    @app.route('/api/status')
    def api_status():
        """API endpoint for status JSON"""
        devme = DevMe()
        status = devme.get_status()
        return jsonify(status)
    
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({"status": "healthy", "service": "devme"})
    
    return app


def serve_dashboard(host='localhost', port=8080, debug=False):
    """Start the DevMe dashboard server"""
    app = create_app()
    app.run(host=host, port=port, debug=debug)
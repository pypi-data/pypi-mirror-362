"""
DevMe Server - Web dashboard server with enhanced UI
"""

from flask import Flask, render_template_string, jsonify, request
from .core import DevMe


def create_app():
    """Create Flask application"""
    app = Flask(__name__)
    
    @app.route('/')
    def dashboard():
        """Main dashboard page"""
        devme = DevMe()
        status = devme.get_status()
        
        # Enhanced HTML template with vertical layout and dark mode
        template = """
<!DOCTYPE html>
<html>
<head>
    <title>DevMe - {{ status.project_name }}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --bg-tertiary: #e9ecef;
            --text-primary: #212529;
            --text-secondary: #6c757d;
            --text-muted: #adb5bd;
            --border: #dee2e6;
            --accent: #007bff;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --info: #17a2b8;
            --shadow: rgba(0, 0, 0, 0.1);
        }

        [data-theme="dark"] {
            --bg-primary: #1a1a1a;
            --bg-secondary: #2d2d2d;
            --bg-tertiary: #404040;
            --text-primary: #ffffff;
            --text-secondary: #adb5bd;
            --text-muted: #6c757d;
            --border: #495057;
            --accent: #4dabf7;
            --success: #51cf66;
            --warning: #ffd43b;
            --danger: #ff6b6b;
            --info: #22b8cf;
            --shadow: rgba(0, 0, 0, 0.3);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            transition: background-color 0.3s, color 0.3s;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header */
        .header {
            background: var(--bg-secondary);
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px var(--shadow);
            border: 1px solid var(--border);
            position: relative;
        }

        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--text-primary);
        }

        .header .subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
            margin-bottom: 15px;
        }

        .header .timestamp {
            color: var(--text-muted);
            font-size: 0.9rem;
        }

        .theme-toggle {
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 8px 12px;
            cursor: pointer;
            color: var(--text-primary);
            font-size: 1.2rem;
            transition: background-color 0.3s;
        }

        .theme-toggle:hover {
            background: var(--border);
        }

        /* Summary Banner */
        .summary-banner {
            background: var(--bg-secondary);
            padding: 20px 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            border: 1px solid var(--border);
            box-shadow: 0 2px 4px var(--shadow);
        }

        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .stat-item {
            text-align: center;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent);
            display: block;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 4px;
        }

        /* Section */
        .section {
            background: var(--bg-secondary);
            border-radius: 12px;
            margin-bottom: 30px;
            overflow: hidden;
            border: 1px solid var(--border);
            box-shadow: 0 2px 4px var(--shadow);
        }

        .section-header {
            padding: 20px 30px;
            background: var(--bg-tertiary);
            border-bottom: 1px solid var(--border);
        }

        .section-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0;
        }

        .section-content {
            padding: 30px;
        }

        /* Service Cards */
        .service-grid {
            display: grid;
            gap: 20px;
        }

        .service-card {
            background: var(--bg-primary);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .service-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px var(--shadow);
        }

        .service-header {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }

        .service-icon {
            font-size: 1.5rem;
            margin-right: 12px;
        }

        .service-name {
            font-weight: 600;
            color: var(--text-primary);
            flex: 1;
        }

        .service-status {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
        }

        .status-configured { background: var(--success); color: white; }
        .status-missing_config { background: var(--warning); color: white; }
        .status-unknown { background: var(--text-muted); color: white; }

        .service-details {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 8px;
        }

        .service-badges {
            margin-top: 12px;
            display: flex;
            gap: 8px;
        }

        .badge {
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.7rem;
            font-weight: 500;
        }

        .badge-config { background: var(--info); color: white; }
        .badge-packages { background: var(--success); color: white; }

        /* Status Items */
        .status-grid {
            display: grid;
            gap: 12px;
        }

        .status-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid var(--border);
        }

        .status-item:last-child {
            border-bottom: none;
        }

        .status-label {
            color: var(--text-primary);
            font-weight: 500;
        }

        .status-value {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-good { color: var(--success); }
        .status-bad { color: var(--danger); }
        .status-neutral { color: var(--text-muted); }

        /* Commit Display */
        .commit {
            background: var(--bg-primary);
            padding: 16px;
            border-radius: 8px;
            margin: 12px 0;
            border: 1px solid var(--border);
        }

        .commit-hash {
            font-family: 'Monaco', 'Menlo', monospace;
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-bottom: 8px;
        }

        .commit-message {
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9rem;
            margin: 8px 0;
            background: var(--bg-secondary);
            padding: 12px;
            border-radius: 6px;
            border-left: 3px solid var(--accent);
            white-space: pre-wrap;
            line-height: 1.4;
        }

        .commit-meta {
            color: var(--text-muted);
            font-size: 0.8rem;
            margin-top: 8px;
        }

        /* Branch Badge */
        .branch {
            background: var(--bg-tertiary);
            color: var(--text-primary);
            padding: 4px 8px;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9rem;
            border: 1px solid var(--border);
        }

        /* Project Type Tags */
        .project-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 12px;
        }

        .project-tag {
            background: var(--accent);
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: var(--text-secondary);
        }

        .empty-state-icon {
            font-size: 4rem;
            margin-bottom: 16px;
            opacity: 0.5;
        }
        
        .empty-state h2 {
            color: var(--text-primary);
            margin: 20px 0;
        }
        
        .empty-state h3 {
            color: var(--text-primary);
            margin: 20px 0;
        }
        
        .empty-state ul {
            list-style: none;
            padding: 0;
        }
        
        .empty-state li {
            margin: 12px 0;
            font-size: 0.95rem;
        }
        
        .empty-state code {
            background: var(--bg-tertiary);
            padding: 4px 8px;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', monospace;
            color: var(--accent);
            font-size: 0.9rem;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .section-content {
                padding: 20px;
            }
            
            .summary-stats {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <button class="theme-toggle" onclick="toggleTheme()">🌓</button>
            <h1>🔍 DevMe</h1>
            <div class="subtitle">{{ status.project_name }}</div>
            <div class="timestamp">Last updated: {{ status.last_updated }}</div>
        </div>

        {% if status.project_type.is_empty %}
        <!-- Empty Directory State -->
        <div class="section">
            <div class="section-content">
                <div class="empty-state">
                    <div class="empty-state-icon">📂</div>
                    <h2>Welcome to DevMe!</h2>
                    <p>This directory is empty. DevMe works best with an active project.</p>
                    <div style="margin-top: 30px;">
                        <h3>Getting Started:</h3>
                        <ul style="text-align: left; display: inline-block; margin-top: 20px;">
                            <li>Initialize a Git repository: <code>git init</code></li>
                            <li>Create a Python project: <code>python -m venv venv && echo "flask" > requirements.txt</code></li>
                            <li>Create a Node.js project: <code>npm init -y</code></li>
                            <li>Add a README: <code>echo "# My Project" > README.md</code></li>
                            <li>Configure DevMe: <code>devme init</code></li>
                        </ul>
                    </div>
                    <p style="margin-top: 30px; color: var(--text-muted);">
                        DevMe automatically discovers services, dependencies, and configuration<br>
                        once you have project files in this directory.
                    </p>
                </div>
            </div>
        </div>
        {% else %}
        <!-- Summary Banner -->
        {% if status.services.discovered %}
        <div class="summary-banner">
            <div class="summary-stats">
                <div class="stat-item">
                    <span class="stat-value">{{ status.services.summary.total_services }}</span>
                    <div class="stat-label">Services Detected</div>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{{ status.services.summary.configured_services|length }}</span>
                    <div class="stat-label">Configured</div>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{{ status.file_count }}</span>
                    <div class="stat-label">Project Files</div>
                </div>
                {% if status.git %}
                <div class="stat-item">
                    <span class="stat-value">{{ status.git.total_branches or 0 }}</span>
                    <div class="stat-label">Git Branches</div>
                </div>
                {% endif %}
            </div>
        </div>
        {% endif %}

        <!-- Project Type -->
        {% if status.project_type.languages %}
        <div class="section">
            <div class="section-header">
                <h3 class="section-title">📋 Project Information</h3>
            </div>
            <div class="section-content">
                <div class="status-item">
                    <span class="status-label">Languages:</span>
                    <div class="project-tags">
                        {% for lang in status.project_type.languages %}
                        <span class="project-tag">{{ lang }}</span>
                        {% endfor %}
                    </div>
                </div>
                {% if status.project_type.frameworks %}
                <div class="status-item">
                    <span class="status-label">Frameworks:</span>
                    <div class="project-tags">
                        {% for framework in status.project_type.frameworks %}
                        <span class="project-tag">{{ framework }}</span>
                        {% endfor %}
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
        {% endif %}

        <!-- External Services -->
        {% if status.services.discovered %}
        <div class="section">
            <div class="section-header">
                <h3 class="section-title">🔗 External Services</h3>
            </div>
            <div class="section-content">
                <div class="service-grid">
                    {% for service in status.services.discovered %}
                    <div class="service-card">
                        <div class="service-header">
                            <span class="service-icon">{{ service.icon }}</span>
                            <span class="service-name">{{ service.name }}</span>
                            <span class="service-status status-{{ service.status }}">
                                {{ service.status.replace('_', ' ').title() }}
                            </span>
                        </div>
                        <div class="service-details">{{ service.details }}</div>
                        <div class="service-badges">
                            {% if service.config_found %}
                            <span class="badge badge-config">Config Found</span>
                            {% endif %}
                            {% if service.packages_installed %}
                            <span class="badge badge-packages">Packages Installed</span>
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endif %}

        <!-- Git Repository -->
        <div class="section">
            <div class="section-header">
                <h3 class="section-title">📁 Git Repository</h3>
            </div>
            <div class="section-content">
                {% if status.git %}
                    <div class="status-grid">
                        <div class="status-item">
                            <span class="status-label">Branch:</span>
                            <span class="branch">{{ status.git.current_branch }}</span>
                        </div>
                        <div class="status-item">
                            <span class="status-label">Status:</span>
                            <span class="status-value {{ 'status-bad' if status.git.is_dirty else 'status-good' }}">
                                {{ '⚠️ Dirty' if status.git.is_dirty else '✅ Clean' }}
                            </span>
                        </div>
                        <div class="status-item">
                            <span class="status-label">Branches:</span>
                            <span class="status-value">{{ status.git.total_branches }}</span>
                        </div>
                        <div class="status-item">
                            <span class="status-label">Untracked files:</span>
                            <span class="status-value {{ 'status-bad' if status.git.untracked_files > 0 else 'status-good' }}">
                                {{ status.git.untracked_files }}
                            </span>
                        </div>
                    </div>
                    
                    {% if status.git.latest_commit %}
                    <div class="commit">
                        <div class="commit-hash">{{ status.git.latest_commit.hash }}</div>
                        <pre class="commit-message">{{ status.git.latest_commit.message }}</pre>
                        <div class="commit-meta">{{ status.git.latest_commit.author }} • {{ status.git.latest_commit.date }}</div>
                    </div>
                    {% endif %}
                {% else %}
                    <div class="empty-state">
                        <div class="empty-state-icon">📁</div>
                        <div>No git repository found</div>
                    </div>
                {% endif %}
            </div>
        </div>

        <!-- Project Files -->
        <div class="section">
            <div class="section-header">
                <h3 class="section-title">📄 Project Files</h3>
            </div>
            <div class="section-content">
                <div class="status-grid">
                    <div class="status-item">
                        <span class="status-label">README:</span>
                        <span class="status-value {{ 'status-good' if status.files.readme else 'status-bad' }}">
                            {{ '✅' if status.files.readme else '❌' }}
                        </span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Tests:</span>
                        <span class="status-value {{ 'status-good' if status.files.tests else 'status-bad' }}">
                            {{ '✅' if status.files.tests else '❌' }}
                        </span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Package config:</span>
                        <span class="status-value {{ 'status-good' if status.files.package_config else 'status-bad' }}">
                            {{ '✅' if status.files.package_config else '❌' }}
                        </span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Environment files:</span>
                        <span class="status-value {{ 'status-good' if status.files.env_files else 'status-neutral' }}">
                            {{ '✅' if status.files.env_files else '➖' }}
                        </span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">CI/CD config:</span>
                        <span class="status-value {{ 'status-good' if status.files.ci_config else 'status-neutral' }}">
                            {{ '✅' if status.files.ci_config else '➖' }}
                        </span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Documentation:</span>
                        <span class="status-value {{ 'status-good' if status.files.documentation else 'status-neutral' }}">
                            {{ '✅' if status.files.documentation else '➖' }}
                        </span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Total files:</span>
                        <span class="status-value">{{ status.file_count }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Environment -->
        <div class="section">
            <div class="section-header">
                <h3 class="section-title">🔧 Environment</h3>
            </div>
            <div class="section-content">
                <div class="status-grid">
                    <div class="status-item">
                        <span class="status-label">Python version:</span>
                        <span class="status-value">{{ status.environment.python_version }}</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Virtual environment:</span>
                        <span class="status-value {{ 'status-good' if status.environment.virtual_env else 'status-neutral' }}">
                            {{ '✅ Active' if status.environment.virtual_env else '➖ Not detected' }}
                        </span>
                    </div>
                    {% if status.environment.git_config %}
                    <div class="status-item">
                        <span class="status-label">Git user:</span>
                        <span class="status-value">{{ status.environment.git_config.user_name }}</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Git email:</span>
                        <span class="status-value">{{ status.environment.git_config.user_email }}</span>
                    </div>
                    {% endif %}
                    <div class="status-item">
                        <span class="status-label">Project path:</span>
                        <span class="status-value" style="font-family: monospace; font-size: 0.8em;">{{ status.path }}</span>
                    </div>
                </div>
            </div>
        </div>
        {% endif %}  <!-- End of not empty directory -->
    </div>

    <script>
        // Theme toggle functionality
        function toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('devme-theme', newTheme);
        }

        // Load saved theme
        const savedTheme = localStorage.getItem('devme-theme');
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
        } else {
            // Default to system preference
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
        }

        // Auto-refresh every 30 seconds
        setTimeout(() => {
            location.reload();
        }, 30000);
    </script>
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
    
    @app.route('/api/services/<service_id>/health')
    def check_service_health(service_id):
        """API endpoint to check specific service health"""
        devme = DevMe()
        try:
            import asyncio
            status = asyncio.run(devme.discovery.check_service_health(service_id))
            return jsonify({
                "service": service_id,
                "status": status.status,
                "details": status.details,
                "response_time": status.response_time,
                "error": status.error
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({"status": "healthy", "service": "devme"})
    
    return app


def serve_dashboard(host='localhost', port=6174, debug=False):
    """Start the DevMe dashboard server"""
    app = create_app()
    app.run(host=host, port=port, debug=debug)
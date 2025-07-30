"""
DevMe Service Discovery - Data-driven service detection and health checking
"""

import os
import re
import yaml
import json
import asyncio
import aiohttp
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass
import pkg_resources


@dataclass
class ServiceStatus:
    """Status information for a discovered service"""
    name: str
    icon: str
    category: str
    status: str  # 'healthy', 'unhealthy', 'unknown', 'missing_config'
    details: str
    response_time: Optional[float] = None
    error: Optional[str] = None
    config_found: bool = False
    packages_installed: bool = False


class ServiceDiscovery:
    """Data-driven service discovery using YAML configuration"""
    
    def __init__(self, project_path: Optional[str] = None):
        self.project_path = Path(project_path or os.getcwd())
        self.services_config = self._load_services_config()
        self.env_vars = self._load_env_vars()
        self.project_packages = self._get_project_packages()
        self.has_project_files = self._check_project_exists()
    
    def _load_services_config(self) -> Dict[str, Any]:
        """Load service patterns from YAML file"""
        config_path = Path(__file__).parent / "services.yaml"
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load services.yaml: {e}")
            return {"services": {}, "env_patterns": {}, "file_patterns": {}}
    
    def _check_project_exists(self) -> bool:
        """Check if this is an actual project directory with code files"""
        # Check for common project indicators
        project_indicators = [
            '*.py', '*.js', '*.ts', '*.jsx', '*.tsx',  # Code files
            '*.java', '*.go', '*.rs', '*.cpp', '*.c',  # More code files
            'requirements.txt', 'package.json', 'Cargo.toml', 'go.mod',  # Package files
            'setup.py', 'pyproject.toml', 'Makefile',  # Build files
            '.git', '.gitignore',  # Version control
            'README*', 'readme*',  # Documentation
        ]
        
        for pattern in project_indicators:
            if list(self.project_path.glob(pattern)):
                return True
        
        # Check if directory has any files at all (excluding hidden files)
        visible_files = [f for f in self.project_path.iterdir() 
                        if f.is_file() and not f.name.startswith('.')]
        return len(visible_files) > 0
    
    def _load_env_vars(self) -> Dict[str, str]:
        """Load environment variables from .env files in the project"""
        env_vars = {}
        
        # Only load from project .env files, not system environment
        env_files = ['.env', '.env.local', '.env.development']
        for env_file in env_files:
            env_path = self.project_path / env_file
            if env_path.exists():
                try:
                    with open(env_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#') and '=' in line:
                                key, value = line.split('=', 1)
                                env_vars[key.strip()] = value.strip().strip('"\'')
                except Exception:
                    pass
        
        return env_vars
    
    def _get_project_packages(self) -> Dict[str, Set[str]]:
        """Get packages that are actually used in this project"""
        packages = {
            'python': set(),
            'javascript': set()
        }
        
        # Python packages from requirements.txt
        req_files = ['requirements.txt', 'requirements-dev.txt', 'requirements.in']
        for req_file in req_files:
            req_path = self.project_path / req_file
            if req_path.exists():
                try:
                    with open(req_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # Extract package name (before any version specifier)
                                pkg_name = re.split(r'[<>=!]', line)[0].strip()
                                if pkg_name:
                                    packages['python'].add(pkg_name.lower())
                except Exception:
                    pass
        
        # Python packages from pyproject.toml
        pyproject_path = self.project_path / 'pyproject.toml'
        if pyproject_path.exists():
            try:
                try:
                    import tomllib  # Python 3.11+
                except ImportError:
                    import tomli as tomllib  # Fallback for older Python
                with open(pyproject_path, 'rb') as f:
                    pyproject = tomllib.load(f)
                    # Get dependencies
                    deps = pyproject.get('project', {}).get('dependencies', [])
                    for dep in deps:
                        pkg_name = re.split(r'[<>=!]', dep)[0].strip()
                        if pkg_name:
                            packages['python'].add(pkg_name.lower())
            except Exception:
                # Try to parse it as text if TOML parsing fails
                try:
                    with open(pyproject_path, 'r') as f:
                        content = f.read()
                        # Simple regex to find dependencies
                        deps_match = re.search(r'dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
                        if deps_match:
                            deps_str = deps_match.group(1)
                            for line in deps_str.split('\n'):
                                line = line.strip().strip('",')
                                if line:
                                    pkg_name = re.split(r'[<>=!]', line)[0].strip()
                                    if pkg_name:
                                        packages['python'].add(pkg_name.lower())
                except Exception:
                    pass
        
        # JavaScript packages from package.json
        package_json_path = self.project_path / "package.json"
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                    dependencies = package_data.get('dependencies', {})
                    dev_dependencies = package_data.get('devDependencies', {})
                    packages['javascript'].update(dependencies.keys())
                    packages['javascript'].update(dev_dependencies.keys())
            except Exception:
                pass
        
        return packages
    
    def _check_if_package_in_project(self, package_name: str, language: str) -> bool:
        """Check if a package is actually used in this project"""
        if language == 'python':
            return package_name.lower() in self.project_packages['python']
        elif language == 'javascript':
            return package_name in self.project_packages['javascript']
        return False
    
    def discover_services(self) -> List[ServiceStatus]:
        """Discover all services based on configuration patterns"""
        # If no project files, return empty list
        if not self.has_project_files:
            return []
        
        discovered_services = []
        services_config = self.services_config.get('services', {})
        
        for service_id, service_config in services_config.items():
            status = self._check_service(service_id, service_config)
            # Only include services that have actual project evidence
            if status.config_found or (status.packages_installed and self._is_service_relevant(service_id, service_config)):
                discovered_services.append(status)
        
        return discovered_services
    
    def _is_service_relevant(self, service_id: str, config: Dict[str, Any]) -> bool:
        """Check if a service is relevant to this project"""
        # Check if any of the service's packages are in the project
        packages_python = config.get('packages', {}).get('python', [])
        packages_js = config.get('packages', {}).get('javascript', [])
        
        for pkg in packages_python:
            if self._check_if_package_in_project(pkg, 'python'):
                return True
        
        for pkg in packages_js:
            if self._check_if_package_in_project(pkg, 'javascript'):
                return True
        
        return False
    
    def _check_service(self, service_id: str, config: Dict[str, Any]) -> ServiceStatus:
        """Check if a service is configured and available"""
        name = config.get('name', service_id)
        icon = config.get('icon', '🔧')
        category = config.get('category', 'other')
        
        # Check environment variables
        env_vars = config.get('env_vars', [])
        config_found = any(var in self.env_vars for var in env_vars)
        
        # Check installed packages - but only if they're in the project
        packages_python = config.get('packages', {}).get('python', [])
        packages_js = config.get('packages', {}).get('javascript', [])
        
        packages_installed = False
        # Only check if packages are in the project dependencies
        for pkg in packages_python:
            if self._check_if_package_in_project(pkg, 'python'):
                # Now check if it's actually installed
                try:
                    __import__(pkg)
                    packages_installed = True
                    break
                except ImportError:
                    pass
        
        if not packages_installed:
            for pkg in packages_js:
                if self._check_if_package_in_project(pkg, 'javascript'):
                    packages_installed = True
                    break
        
        # Check files
        files = config.get('files', [])
        files_found = any((self.project_path / file_pattern).exists() for file_pattern in files)
        
        # Determine overall configuration status
        if not (config_found or packages_installed or files_found):
            return ServiceStatus(
                name=name,
                icon=icon,
                category=category,
                status='unknown',
                details='Not detected in project',
                config_found=False,
                packages_installed=False
            )
        
        if config_found and not packages_installed:
            return ServiceStatus(
                name=name,
                icon=icon,
                category=category,
                status='missing_config',
                details='Configuration found but packages not installed',
                config_found=True,
                packages_installed=False
            )
        
        if packages_installed and not config_found:
            return ServiceStatus(
                name=name,
                icon=icon,
                category=category,
                status='missing_config',
                details='Packages in project but configuration missing',
                config_found=False,
                packages_installed=True
            )
        
        return ServiceStatus(
            name=name,
            icon=icon,
            category=category,
            status='configured',
            details='Configuration and packages found',
            config_found=True,
            packages_installed=True
        )
    
    async def check_service_health(self, service_id: str) -> ServiceStatus:
        """Perform health check for a specific service"""
        services_config = self.services_config.get('services', {})
        if service_id not in services_config:
            raise ValueError(f"Unknown service: {service_id}")
        
        config = services_config[service_id]
        status = self._check_service(service_id, config)
        
        # If no health check configured or service not configured, return current status
        health_check = config.get('health_check')
        if not health_check or status.status == 'unknown':
            return status
        
        # Perform health check
        try:
            url = self._substitute_env_vars(health_check.get('url', ''))
            method = health_check.get('method', 'GET')
            headers = health_check.get('headers', {})
            timeout = health_check.get('timeout', 10)
            
            # Substitute environment variables in headers
            for key, value in headers.items():
                headers[key] = self._substitute_env_vars(value)
            
            import time
            start_time = time.time()
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                if method == 'GET':
                    async with session.get(url, headers=headers) as response:
                        response_time = time.time() - start_time
                        if response.status == 200:
                            status.status = 'healthy'
                            status.details = f'Service responding ({response.status})'
                            status.response_time = response_time
                        else:
                            status.status = 'unhealthy'
                            status.details = f'Service error ({response.status})'
                            status.response_time = response_time
                elif method == 'POST':
                    async with session.post(url, headers=headers) as response:
                        response_time = time.time() - start_time
                        if response.status in [200, 201]:
                            status.status = 'healthy'
                            status.details = f'Service responding ({response.status})'
                            status.response_time = response_time
                        else:
                            status.status = 'unhealthy'
                            status.details = f'Service error ({response.status})'
                            status.response_time = response_time
        
        except asyncio.TimeoutError:
            status.status = 'unhealthy'
            status.details = 'Health check timeout'
            status.error = 'Timeout'
        except Exception as e:
            status.status = 'unhealthy'
            status.details = f'Health check failed: {str(e)}'
            status.error = str(e)
        
        return status
    
    def _substitute_env_vars(self, text: str) -> str:
        """Substitute environment variables in text using {VAR_NAME} format"""
        def replace_var(match):
            var_name = match.group(1)
            return self.env_vars.get(var_name, f"{{{var_name}}}")
        
        return re.sub(r'\{([^}]+)\}', replace_var, text)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of discovered services"""
        services = self.discover_services()
        
        summary = {
            'total_services': len(services),
            'by_status': {},
            'by_category': {},
            'configured_services': [s for s in services if s.status == 'configured'],
            'missing_config': [s for s in services if s.status == 'missing_config'],
            'has_project': self.has_project_files
        }
        
        # Count by status
        for service in services:
            status = service.status
            summary['by_status'][status] = summary['by_status'].get(status, 0) + 1
        
        # Count by category
        for service in services:
            category = service.category
            summary['by_category'][category] = summary['by_category'].get(category, 0) + 1
        
        return summary
    
    def detect_project_type(self) -> Dict[str, Any]:
        """Detect project type based on files and dependencies"""
        project_info = {
            'languages': [],
            'frameworks': [],
            'deployment': [],
            'databases': [],
            'is_empty': not self.has_project_files
        }
        
        if not self.has_project_files:
            return project_info
        
        # Language detection
        if (self.project_path / "requirements.txt").exists() or \
           (self.project_path / "pyproject.toml").exists() or \
           list(self.project_path.glob("*.py")):
            project_info['languages'].append('Python')
        
        if (self.project_path / "package.json").exists() or \
           list(self.project_path.glob("*.js")) or \
           list(self.project_path.glob("*.ts")):
            project_info['languages'].append('JavaScript/Node.js')
        
        if (self.project_path / "go.mod").exists():
            project_info['languages'].append('Go')
        
        if (self.project_path / "Cargo.toml").exists():
            project_info['languages'].append('Rust')
        
        # Framework detection based on project dependencies
        if 'fastapi' in self.project_packages['python']:
            project_info['frameworks'].append('FastAPI')
        if 'flask' in self.project_packages['python']:
            project_info['frameworks'].append('Flask')
        if 'django' in self.project_packages['python']:
            project_info['frameworks'].append('Django')
        if 'react' in self.project_packages['javascript']:
            project_info['frameworks'].append('React')
        if 'next' in self.project_packages['javascript']:
            project_info['frameworks'].append('Next.js')
        
        return project_info
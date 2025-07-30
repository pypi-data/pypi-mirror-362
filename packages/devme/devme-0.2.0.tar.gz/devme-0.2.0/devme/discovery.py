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
from typing import Dict, List, Optional, Any, Tuple
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
        self.installed_packages = self._get_installed_packages()
    
    def _load_services_config(self) -> Dict[str, Any]:
        """Load service patterns from YAML file"""
        config_path = Path(__file__).parent / "services.yaml"
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load services.yaml: {e}")
            return {"services": {}, "env_patterns": {}, "file_patterns": {}}
    
    def _load_env_vars(self) -> Dict[str, str]:
        """Load environment variables from .env files and system"""
        env_vars = dict(os.environ)
        
        # Load from .env files
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
    
    def _get_installed_packages(self) -> Dict[str, str]:
        """Get installed Python packages and their versions"""
        packages = {}
        try:
            installed = [d for d in pkg_resources.working_set]
            for package in installed:
                packages[package.project_name.lower()] = package.version
        except Exception:
            pass
        
        # Also check for JavaScript packages if package.json exists
        package_json_path = self.project_path / "package.json"
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                    dependencies = package_data.get('dependencies', {})
                    dev_dependencies = package_data.get('devDependencies', {})
                    packages.update(dependencies)
                    packages.update(dev_dependencies)
            except Exception:
                pass
        
        return packages
    
    def discover_services(self) -> List[ServiceStatus]:
        """Discover all services based on configuration patterns"""
        discovered_services = []
        services_config = self.services_config.get('services', {})
        
        for service_id, service_config in services_config.items():
            status = self._check_service(service_id, service_config)
            if status.config_found or status.packages_installed:
                discovered_services.append(status)
        
        return discovered_services
    
    def _check_service(self, service_id: str, config: Dict[str, Any]) -> ServiceStatus:
        """Check if a service is configured and available"""
        name = config.get('name', service_id)
        icon = config.get('icon', '🔧')
        category = config.get('category', 'other')
        
        # Check environment variables
        env_vars = config.get('env_vars', [])
        config_found = any(var in self.env_vars for var in env_vars)
        
        # Check installed packages
        packages_python = config.get('packages', {}).get('python', [])
        packages_js = config.get('packages', {}).get('javascript', [])
        packages_installed = (
            any(pkg.lower() in self.installed_packages for pkg in packages_python) or
            any(pkg in self.installed_packages for pkg in packages_js)
        )
        
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
                details='Packages installed but configuration missing',
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
            'databases': []
        }
        
        # Language detection
        if (self.project_path / "requirements.txt").exists() or \
           (self.project_path / "pyproject.toml").exists():
            project_info['languages'].append('Python')
        
        if (self.project_path / "package.json").exists():
            project_info['languages'].append('JavaScript/Node.js')
        
        if (self.project_path / "go.mod").exists():
            project_info['languages'].append('Go')
        
        if (self.project_path / "Cargo.toml").exists():
            project_info['languages'].append('Rust')
        
        # Framework detection based on dependencies
        if 'fastapi' in self.installed_packages:
            project_info['frameworks'].append('FastAPI')
        if 'flask' in self.installed_packages:
            project_info['frameworks'].append('Flask')
        if 'django' in self.installed_packages:
            project_info['frameworks'].append('Django')
        if 'react' in self.installed_packages:
            project_info['frameworks'].append('React')
        if 'next' in self.installed_packages:
            project_info['frameworks'].append('Next.js')
        
        return project_info
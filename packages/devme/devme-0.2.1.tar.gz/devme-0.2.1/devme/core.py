"""
DevMe Core - Main functionality for project analysis
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import git
from git.exc import InvalidGitRepositoryError
from .discovery import ServiceDiscovery


class DevMe:
    """Main DevMe class for analyzing project status"""
    
    def __init__(self, path: Optional[str] = None):
        self.path = Path(path or os.getcwd())
        self.config = self._load_config()
        self.repo = self._get_git_repo()
        self.discovery = ServiceDiscovery(str(self.path))
    
    def _load_config(self) -> Dict[str, Any]:
        """Load DevMe configuration from .devme.json"""
        config_file = self.path / '.devme.json'
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Default config
        return {
            "project_name": self.path.name,
            "ignore_patterns": [".git", "__pycache__", "node_modules", ".venv"],
            "external_services": {},
            "custom_checks": []
        }
    
    def _get_git_repo(self) -> Optional[git.Repo]:
        """Get git repository if available"""
        try:
            return git.Repo(self.path, search_parent_directories=True)
        except InvalidGitRepositoryError:
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive project status"""
        # Discover services
        discovered_services = self.discovery.discover_services()
        service_summary = self.discovery.get_summary()
        project_type = self.discovery.detect_project_type()
        
        status = {
            "project_name": self.config.get("project_name", self.path.name),
            "path": str(self.path),
            "timestamp": datetime.now().isoformat(),
            "git": self._get_git_status(),
            "files": self._get_file_status(),
            "environment": self._get_environment_status(),
            "services": {
                "discovered": [
                    {
                        "name": s.name,
                        "icon": s.icon,
                        "category": s.category,
                        "status": s.status,
                        "details": s.details,
                        "config_found": s.config_found,
                        "packages_installed": s.packages_installed
                    } for s in discovered_services
                ],
                "summary": service_summary
            },
            "project_type": project_type,
            "file_count": self._count_project_files(),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return status
    
    def _get_git_status(self) -> Dict[str, Any]:
        """Analyze git repository status"""
        if not self.repo:
            return {}
        
        try:
            # Basic git info
            git_info = {
                "name": self.repo.working_dir.split('/')[-1],
                "current_branch": self.repo.active_branch.name,
                "is_dirty": self.repo.is_dirty(),
                "untracked_files": len(self.repo.untracked_files),
            }
            
            # Recent commits
            commits = list(self.repo.iter_commits(max_count=10))
            git_info["recent_commits"] = len(commits)
            git_info["latest_commit"] = {
                "hash": commits[0].hexsha[:8],
                "message": commits[0].message.strip(),
                "author": commits[0].author.name,
                "date": commits[0].committed_datetime.strftime("%Y-%m-%d %H:%M:%S")
            } if commits else None
            
            # Branch info
            branches = [ref.name.split('/')[-1] for ref in self.repo.refs if ref.name.startswith('refs/heads/')]
            git_info["branches"] = branches
            git_info["total_branches"] = len(branches)
            
            # Remote info
            remotes = [remote.name for remote in self.repo.remotes]
            git_info["remotes"] = remotes
            
            return git_info
            
        except Exception as e:
            return {"error": str(e)}
    
    def _get_file_status(self) -> Dict[str, Any]:
        """Check for important files"""
        files = {}
        
        # README files
        readme_patterns = ['README.md', 'README.rst', 'README.txt', 'README']
        files["readme"] = any((self.path / pattern).exists() for pattern in readme_patterns)
        
        # Test files/directories
        test_patterns = ['tests/', 'test/', 'spec/', '*test*.py', '*spec*.py']
        files["tests"] = any(
            list(self.path.glob(pattern)) for pattern in test_patterns
        )
        
        # Package configuration
        package_patterns = ['setup.py', 'pyproject.toml', 'package.json', 'Cargo.toml', 'go.mod']
        files["package_config"] = any((self.path / pattern).exists() for pattern in package_patterns)
        
        # Environment files
        env_patterns = ['.env', '.env.example', '.env.local', '.envrc']
        files["env_files"] = any((self.path / pattern).exists() for pattern in env_patterns)
        
        # CI/CD files
        ci_patterns = ['.github/', '.gitlab-ci.yml', '.travis.yml', 'Jenkinsfile']
        files["ci_config"] = any(
            (self.path / pattern).exists() for pattern in ci_patterns
        )
        
        # Documentation
        doc_patterns = ['docs/', 'doc/', 'documentation/']
        files["documentation"] = any((self.path / pattern).exists() for pattern in doc_patterns)
        
        return files
    
    def _get_environment_status(self) -> Dict[str, Any]:
        """Check environment and configuration status"""
        env_status = {
            "python_version": self._get_python_version(),
            "virtual_env": self._check_virtual_env(),
            "git_config": self._check_git_config(),
        }
        
        return env_status
    
    def _get_python_version(self) -> str:
        """Get Python version"""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    def _check_virtual_env(self) -> bool:
        """Check if running in virtual environment"""
        return hasattr(os.sys, 'real_prefix') or (
            hasattr(os.sys, 'base_prefix') and os.sys.base_prefix != os.sys.prefix
        )
    
    def _check_git_config(self) -> Dict[str, Any]:
        """Check git configuration"""
        if not self.repo:
            return {}
        
        try:
            config = self.repo.config_reader()
            return {
                "user_name": config.get_value("user", "name", fallback="Not set"),
                "user_email": config.get_value("user", "email", fallback="Not set"),
            }
        except Exception:
            return {}
    
    def _count_project_files(self) -> int:
        """Count total project files (excluding ignored patterns)"""
        count = 0
        ignore_patterns = self.config.get("ignore_patterns", [])
        
        for file_path in self.path.rglob("*"):
            if file_path.is_file():
                # Skip ignored patterns
                if not any(pattern in str(file_path) for pattern in ignore_patterns):
                    count += 1
        
        return count
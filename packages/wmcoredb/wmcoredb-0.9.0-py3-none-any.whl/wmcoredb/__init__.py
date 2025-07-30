"""
WMCore Database Schema Package

A Python package providing access to WMCore database schema files
for both Oracle and MariaDB backends.
"""

from importlib.metadata import version, PackageNotFoundError
import os
import importlib.resources
from pathlib import Path
from typing import List, Optional

try:
    __version__ = version("wmcoredb")
except PackageNotFoundError:
    __version__ = "unknown"

__author__ = "WMCore Team"
__email__ = "cms-wmcore-team@cern.ch"


def get_sql_file(module_name: str, file_name: str, backend: str = "mariadb") -> str:
    """
    Get the path to a specific SQL file.
    
    Args:
        module_name: The module name (e.g., 'wmbs', 'agent', 'bossair')
        file_name: The SQL file name (e.g., 'create_wmbs_tables.sql')
        backend: The database backend ('mariadb' or 'oracle')
    
    Returns:
        The absolute path to the SQL file
    
    Raises:
        FileNotFoundError: If the SQL file doesn't exist
    """
    resource_path = f"sql/{backend}/{module_name}/{file_name}"
    
    try:
        # Use the modern importlib.resources API
        files = importlib.resources.files('wmcoredb')
        file_path = files / resource_path
        
        if file_path.exists():
            return str(file_path)
        else:
            raise FileNotFoundError(f"SQL file not found: {resource_path}")
    except Exception as e:
        raise FileNotFoundError(f"SQL file not found: {resource_path}") from e


def list_sql_files(module_name: Optional[str] = None, backend: str = "mariadb") -> List[str]:
    """
    List available SQL files.
    
    Args:
        module_name: Optional module name to filter by
        backend: The database backend ('mariadb' or 'oracle')
    
    Returns:
        List of SQL file paths
    """
    sql_files = []
    
    try:
        # Use importlib.resources to list files
        with importlib.resources.path('wmcoredb', 'sql') as sql_dir:
            backend_dir = sql_dir / backend
            
            if not backend_dir.exists():
                return []
            
            # Walk through the directory structure
            for sql_file in backend_dir.rglob("*.sql"):
                relative_path = sql_file.relative_to(backend_dir)
                
                # Filter by module if specified
                if module_name is None or str(relative_path).startswith(f"{module_name}/"):
                    sql_files.append(str(relative_path))
        
        return sorted(sql_files)
    
    except Exception:
        return []


def get_sql_content(module_name: str, file_name: str, backend: str = "mariadb") -> str:
    """
    Get the content of a SQL file.
    
    Args:
        module_name: The module name (e.g., 'wmbs', 'agent', 'bossair')
        file_name: The SQL file name (e.g., 'create_wmbs_tables.sql')
        backend: The database backend ('mariadb' or 'oracle')
    
    Returns:
        The SQL file content as a string
    
    Raises:
        FileNotFoundError: If the SQL file doesn't exist
    """
    file_path = get_sql_file(module_name, file_name, backend)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def list_modules(backend: str = "mariadb") -> List[str]:
    """
    List available modules for a backend.
    
    Args:
        backend: The database backend ('mariadb' or 'oracle')
    
    Returns:
        List of module names
    """
    try:
        with importlib.resources.path('wmcoredb', 'sql') as sql_dir:
            backend_dir = sql_dir / backend
            
            if not backend_dir.exists():
                return []
            
            modules = []
            for item in backend_dir.iterdir():
                if item.is_dir():
                    modules.append(item.name)
            
            return sorted(modules)
    
    except Exception:
        return []


def list_backends() -> List[str]:
    """
    List available database backends.
    
    Returns:
        List of backend names
    """
    try:
        with importlib.resources.path('wmcoredb', 'sql') as sql_dir:
            if not sql_dir.exists():
                return []
            
            backends = []
            for item in sql_dir.iterdir():
                if item.is_dir():
                    backends.append(item.name)
            
            return sorted(backends)
    
    except Exception:
        return [] 
"""
Configuration Management Module

Handles loading and managing configuration files for templates, 
standard responses, and company information.
"""

import json
import os
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages configuration files for the templated communication system"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self._templates = None
        self._standard_responses = None
        self._company_config = None
    
    def _load_json_file(self, filename: str) -> Dict[str, Any]:
        """Load and parse a JSON configuration file"""
        filepath = os.path.join(self.base_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file '{filename}' not found in {self.base_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file '{filename}': {str(e)}")
    
    @property
    def templates(self) -> Dict[str, str]:
        """Get template prompts configuration"""
        if self._templates is None:
            self._templates = self._load_json_file("templates_config.json")
        return self._templates
    
    @property
    def standard_responses(self) -> Dict[str, str]:
        """Get standard responses configuration"""
        if self._standard_responses is None:
            self._standard_responses = self._load_json_file("standard_responses.json")
        return self._standard_responses
    
    @property
    def company_config(self) -> Dict[str, Any]:
        """Get company configuration"""
        if self._company_config is None:
            self._company_config = self._load_json_file("company_config.json")
        return self._company_config
    
    def get_department_info(self, department_key: str = "customer_service") -> Dict[str, str]:
        """Get department-specific company information"""
        config = self.company_config
        
        base_info = {
            "company_name": config.get("company_name", "Our Company"),
            "company_type": config.get("company_type", "Organization"),
            "company_address": config.get("company_address", ""),
            "company_website": config.get("company_website", ""),
            "company_phone": config.get("company_phone", ""),
            "company_email": config.get("company_email", "")
        }
        
        # Add department-specific information
        departments = config.get("departments", {})
        if department_key in departments:
            dept_info = departments[department_key]
            base_info.update(dept_info)
        else:
            # Default department info
            base_info.update({
                "department": "Customer Service",
                "representative_name": "Customer Service Team",
                "contact_phone": base_info["company_phone"],
                "contact_email": base_info["company_email"],
                "hours": "Business hours"
            })
        
        return base_info
    
    def get_available_departments(self) -> Dict[str, str]:
        """Get list of available departments"""
        departments = self.company_config.get("departments", {})
        return {
            key: dept_info.get("department", key.replace('_', ' ').title())
            for key, dept_info in departments.items()
        }
    
    def reload_configs(self):
        """Reload all configuration files"""
        self._templates = None
        self._standard_responses = None
        self._company_config = None
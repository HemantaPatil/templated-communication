"""
Communication Orchestrator Module

Main orchestrator that coordinates all components of the templated communication system.
"""

from typing import Optional
from .config_manager import ConfigManager
from .communication_engine import CommunicationEngine
from .response_processor import ResponseProcessor
from .user_interface import UserInterface


class CommunicationOrchestrator:
    """Main orchestrator for the templated communication system"""
    
    def __init__(self, api_key: Optional[str] = None, base_path: str = "."):
        # Initialize core components
        self.config_manager = ConfigManager(base_path)
        self.communication_engine = CommunicationEngine(api_key)
        self.response_processor = ResponseProcessor(self.config_manager, self.communication_engine)
        self.user_interface = UserInterface(self.config_manager)
    
    def run(self):
        """Main application loop"""
        try:
            # Display welcome message
            self.user_interface.display_welcome()
            
            # Select department
            selected_dept = self.user_interface.select_department()
            company_info = self.config_manager.get_department_info(selected_dept)
            self.user_interface.display_company_profile(company_info)
            
            # Select template
            selected_template, template_index = self.user_interface.select_template()
            if selected_template is None:
                if template_index == -1:  # User chose to exit
                    print("Goodbye!")
                    return
                else:  # Invalid selection
                    return
            
            # Get customer inquiry
            customer_inquiry = self.user_interface.get_customer_inquiry(selected_template)
            if customer_inquiry is None:
                return
            
            # Select deviation tolerance
            deviation_tolerance = self.user_interface.select_deviation_tolerance()
            
            # Collect customer data
            template_fields = self.response_processor.get_template_fields(selected_template)
            customer_data = self.user_interface.collect_customer_data(template_fields)
            
            # Generate response
            result = self.response_processor.generate_response(
                template_type=selected_template,
                customer_inquiry=customer_inquiry,
                customer_data=customer_data,
                company_info=company_info,
                deviation_tolerance=deviation_tolerance
            )
            
            # Display results
            self.user_interface.display_response_result(result, company_info)
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
        except Exception as e:
            self.user_interface.display_error(str(e))
    
    def generate_single_response(
        self,
        template_type: str,
        customer_inquiry: str,
        customer_data: dict = None,
        department: str = "customer_service",
        deviation_tolerance: str = "minimal"
    ):
        """Generate a single response programmatically (for API usage)"""
        try:
            company_info = self.config_manager.get_department_info(department)
            
            result = self.response_processor.generate_response(
                template_type=template_type,
                customer_inquiry=customer_inquiry,
                customer_data=customer_data or {},
                company_info=company_info,
                deviation_tolerance=deviation_tolerance
            )
            
            return result
            
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    def get_available_templates(self) -> list:
        """Get list of available template types"""
        return list(self.config_manager.templates.keys())
    
    def get_available_departments(self) -> dict:
        """Get list of available departments"""
        return self.config_manager.get_available_departments()
    
    def reload_configurations(self):
        """Reload all configuration files"""
        self.config_manager.reload_configs()
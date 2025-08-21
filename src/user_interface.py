"""
User Interface Module

Handles all user interactions, input collection, and output display.
"""

from typing import Dict, List, Tuple, Any


class UserInterface:
    """Manages user interactions and display formatting"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
    
    def display_welcome(self):
        """Display welcome message and system description"""
        print("=== Corporate Customer Communication System ===")
        print("Generate professional corporate responses to customer inquiries and complaints.")
        print("Representing your organization's official voice in customer communications.\n")
    
    def select_department(self) -> str:
        """Allow user to select department and return department key"""
        print("=== Available Departments ===")
        departments = self.config_manager.get_available_departments()
        dept_list = list(departments.keys())
        
        if dept_list:
            for i, (dept_key, dept_name) in enumerate(departments.items(), 1):
                print(f"{i}. {dept_name}")
            
            print(f"\nSelect department (1-{len(dept_list)}) or press Enter for Customer Service:")
            dept_choice = input().strip()
            
            try:
                if dept_choice:
                    dept_index = int(dept_choice) - 1
                    if 0 <= dept_index < len(dept_list):
                        return dept_list[dept_index]
                return "customer_service"
            except ValueError:
                return "customer_service"
        else:
            return "customer_service"
    
    def display_company_profile(self, company_info: Dict[str, str]):
        """Display selected company/department profile"""
        print(f"\nCorporate Profile: {company_info['company_name']} - {company_info['department']}")
        print(f"Contact: {company_info['contact_phone']} | {company_info['contact_email']}\n")
    
    def select_template(self) -> Tuple[str, int]:
        """Allow user to select communication template"""
        print("Available Response Templates:")
        templates = list(self.config_manager.templates.keys())
        
        for i, template_type in enumerate(templates, 1):
            print(f"{i}. {template_type.replace('_', ' ').title()}")
        
        print("\nSelect a template number (or type 'exit' to quit):")
        user_input = input().strip()
        
        if user_input.lower() == 'exit':
            return None, -1
        
        try:
            template_index = int(user_input) - 1
            if 0 <= template_index < len(templates):
                return templates[template_index], template_index
            else:
                print("Invalid template number!")
                return None, -2
        except ValueError:
            # Try direct template name input
            selected_template = user_input.lower().replace(' ', '_') + '_response'
            if selected_template in templates:
                return selected_template, templates.index(selected_template)
            else:
                print(f"Template not found. Available templates: {[t.replace('_', ' ').title() for t in templates]}")
                return None, -2
    
    def get_customer_inquiry(self, template_name: str) -> str:
        """Get customer inquiry from user"""
        print(f"\nSelected template: {template_name.replace('_', ' ').title()}")
        print("\nEnter the customer's question, inquiry, or complaint:")
        customer_inquiry = input().strip()
        
        if not customer_inquiry:
            print("No customer inquiry provided!")
            return None
        
        return customer_inquiry
    
    def select_deviation_tolerance(self) -> str:
        """Allow user to select deviation tolerance"""
        print("\n=== Deviation Tolerance Settings ===")
        print("How much should the AI be allowed to deviate from your standard response?")
        print("1. Strict (0-10% deviation) - Follow standard exactly")
        print("2. Minimal (0-25% deviation) - Minor modifications allowed")
        print("3. Moderate (0-50% deviation) - Moderate personalization allowed")
        print("4. Flexible (0-70% deviation) - Significant customization allowed")
        
        tolerance_choice = input("Select deviation tolerance (1-4): ").strip()
        deviation_map = {"1": "strict", "2": "minimal", "3": "moderate", "4": "flexible"}
        deviation_tolerance = deviation_map.get(tolerance_choice, "minimal")
        
        print(f"Selected: {deviation_tolerance.title()} deviation tolerance")
        return deviation_tolerance
    
    def collect_customer_data(self, template_fields: List[str]) -> Dict[str, str]:
        """Collect customer data based on template requirements"""
        if not template_fields:
            return {}
        
        print(f"\n=== Customer Data Collection ===")
        print("Please provide the following customer information:")
        
        customer_data = {}
        for field in template_fields:
            field_display = field.replace('_', ' ').title()
            value = input(f"{field_display}: ").strip()
            customer_data[field] = value or f"[{field_display}]"
        
        return customer_data
    
    def display_response_result(self, result: Dict[str, Any], company_info: Dict[str, str]):
        """Display the generated response and analysis"""
        print(f"\nGenerating corporate response from {company_info['company_name']} with {result['deviation_tolerance']} deviation tolerance...")
        
        # Display generated response
        print(f"\n{'='*60}")
        print(f"OFFICIAL CORPORATE RESPONSE")
        print(f"{company_info['company_name']} - {company_info['department']}")
        print(f"{'='*60}")
        print(result['generated_response'])
        print(f"{'='*60}")
        
        # Display standard response and analysis
        print(f"\n{'='*60}")
        print(f"ORGANIZATION'S STANDARD RESPONSE")
        print(f"{'='*60}")
        print(result['standard_response'])
        print(f"{'='*60}")
        
        # Display deviation analysis
        print(f"📊 DEVIATION ANALYSIS: {result['deviation_percentage']:.1f}% deviation from standard response")
        print(f"🎯 Target: Stay within {result['max_allowed_deviation']}% deviation ({result['deviation_tolerance']} tolerance)")
        print(result['compliance_message'])
        
        if not result['is_compliant']:
            print("Consider adjusting deviation tolerance or reviewing standard response")
        
        print(f"{'='*60}")
        
        # Display contact information
        print(f"Generated by: {company_info['representative_name']}")
        print(f"Contact: {company_info['contact_phone']} | {company_info['contact_email']}")
    
    def display_error(self, error_message: str):
        """Display error message to user"""
        print(f"Error: {error_message}")
    
    def confirm_exit(self) -> bool:
        """Confirm if user wants to exit"""
        return True  # For now, just exit immediately
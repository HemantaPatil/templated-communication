"""
Response Processor Module

Handles response preparation, placeholder replacement, and analysis.
"""

from typing import Dict, Any, Optional


class ResponseProcessor:
    """Processes and prepares responses for generation"""
    
    def __init__(self, config_manager, communication_engine):
        self.config_manager = config_manager
        self.communication_engine = communication_engine
    
    def prepare_standard_response(
        self, 
        template_type: str, 
        customer_data: Dict[str, str], 
        company_info: Dict[str, str]
    ) -> str:
        """Prepare standard response with customer and company data filled in"""
        
        if template_type not in self.config_manager.standard_responses:
            raise ValueError(f"Template type '{template_type}' not found in standard responses")
        
        standard_response = self.config_manager.standard_responses[template_type]
        
        # Replace customer data placeholders
        if customer_data:
            for field, value in customer_data.items():
                placeholder = f"[{field.replace('_', ' ').title()}]"
                standard_response = standard_response.replace(placeholder, value)
        
        # Replace company info placeholders
        if company_info:
            for field, value in company_info.items():
                placeholder = f"[{field.replace('_', ' ').title()}]"
                standard_response = standard_response.replace(placeholder, value)
        
        return standard_response
    
    def generate_response(
        self,
        template_type: str,
        customer_inquiry: str,
        customer_data: Dict[str, str],
        company_info: Dict[str, str],
        deviation_tolerance: str = "minimal"
    ) -> Dict[str, Any]:
        """Generate a complete response with analysis"""
        
        # Prepare standard response
        standard_response = self.prepare_standard_response(
            template_type, customer_data, company_info
        )
        
        # Generate personalized response
        generated_response = self.communication_engine.generate_personalized_response(
            customer_inquiry=customer_inquiry,
            standard_response=standard_response,
            deviation_tolerance=deviation_tolerance
        )
        
        # Calculate deviation
        deviation_percentage = self.communication_engine.calculate_deviation_percentage(
            generated_response, standard_response
        )
        
        # Analyze compliance
        max_allowed = self.communication_engine.get_deviation_tolerance_limit(deviation_tolerance)
        is_compliant = deviation_percentage <= max_allowed
        
        # Determine compliance level
        if deviation_percentage <= 10:
            compliance_level = "excellent"
            compliance_message = "✅ Excellent: Response closely follows organization standards"
        elif deviation_percentage <= 25:
            compliance_level = "good"
            compliance_message = "✅ Good: Response stays within acceptable deviation range"
        elif deviation_percentage <= max_allowed:
            compliance_level = "acceptable"
            compliance_message = "✅ Acceptable: Response meets deviation tolerance requirements"
        else:
            compliance_level = "warning"
            compliance_message = f"❌ Warning: Response exceeds {deviation_tolerance} tolerance limit ({max_allowed}%)"
        
        return {
            "generated_response": generated_response,
            "standard_response": standard_response,
            "deviation_percentage": deviation_percentage,
            "max_allowed_deviation": max_allowed,
            "is_compliant": is_compliant,
            "compliance_level": compliance_level,
            "compliance_message": compliance_message,
            "template_type": template_type,
            "deviation_tolerance": deviation_tolerance
        }
    
    def get_template_fields(self, template_type: str) -> list:
        """Get required customer data fields for a template type"""
        template_fields = {
            "customer_inquiry_response": ["customer_name", "account_number"],
            "complaint_resolution_letter": ["customer_name", "complaint_number"],
            "policy_cancellation_response": ["customer_name", "policy_number", "policy_type", "effective_date", "refund_amount"],
            "claim_processing_update": ["customer_name", "claim_number", "policy_number", "incident_date", "claim_status", "next_steps"],
            "claim_approval_notification": ["customer_name", "claim_number", "approved_amount", "payment_date", "settlement_details"],
            "claim_denial_notification": ["customer_name", "claim_number", "policy_number", "denial_reason", "policy_section", "appeal_process"],
            "billing_inquiry_response": ["customer_name", "account_number", "billing_period", "amount_due", "due_date", "payment_methods"],
            "premium_adjustment_notice": ["customer_name", "policy_number", "current_premium", "new_premium", "effective_date", "increase_reason"],
            "coverage_modification_notice": ["customer_name", "policy_number", "coverage_changes", "effective_date", "premium_impact"],
            "new_customer_welcome": ["customer_name", "policy_number", "agent_name", "agent_contact", "coverage_summary", "important_dates"]
        }
        
        return template_fields.get(template_type, [])
    
    def format_customer_data(self, customer_data: Dict[str, str]) -> str:
        """Format customer data for display purposes"""
        if not customer_data:
            return "No customer data provided"
        
        formatted_data = []
        for key, value in customer_data.items():
            formatted_data.append(f"{key}: {value}")
        return "; ".join(formatted_data)
"""
Communication Engine Module

Handles OpenAI API interactions and response generation logic.
"""

import re
import os
from typing import Dict, Optional
from openai import OpenAI


class CommunicationEngine:
    """Handles OpenAI communication and response generation"""
    
    def __init__(self, api_key: Optional[str] = None):
        # Get API key from parameter, environment variable, or raise error
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable or pass api_key parameter.")
        self.client = OpenAI(api_key=api_key)
        self.deviation_tolerance_settings = {
            "strict": {
                "limit": 10,
                "instruction": "Follow the standard response EXACTLY. Make only minimal changes necessary to address the specific customer inquiry. Deviation should be less than 10%."
            },
            "minimal": {
                "limit": 25,
                "instruction": "Follow the standard response closely but allow minor modifications to better address the customer inquiry. Deviation should be less than 25%."
            },
            "moderate": {
                "limit": 50,
                "instruction": "Use the standard response as a strong guideline but allow moderate changes to personalize and improve the response. Deviation should be less than 50%."
            },
            "flexible": {
                "limit": 70,
                "instruction": "Use the standard response as a foundation but feel free to significantly modify to create the best possible response. Deviation can be up to 70%."
            }
        }
    
    def generate_personalized_response(
        self,
        customer_inquiry: str,
        standard_response: str,
        deviation_tolerance: str = "minimal",
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 800
    ) -> str:
        """Generate a personalized response based on standard template and customer inquiry"""
        
        tolerance_config = self.deviation_tolerance_settings.get(
            deviation_tolerance, 
            self.deviation_tolerance_settings["minimal"]
        )
        
        prompt = f"""
        Customer Inquiry: {customer_inquiry}
        
        Organization's Standard Response Template:
        {standard_response}
        
        Deviation Guidelines: {tolerance_config['instruction']}
        
        Using the standard response above as your base template, generate a personalized response that addresses the specific customer inquiry while staying within the allowed deviation tolerance. Maintain the organization's professional tone and include all required corporate elements.
        """
        
        try:
            print(prompt)
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a corporate customer service representative. You MUST use the provided standard response as your base template and stay within the specified deviation tolerance. Personalize the standard response to address the specific customer inquiry while maintaining the organization's approved language, tone, and structure. Do not deviate beyond the allowed percentage."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Error generating communication: {str(e)}")
    
    def calculate_deviation_percentage(self, generated_response: str, standard_response: str) -> float:
        """Calculate how much the generated response deviates from the standard response"""
        try:
            comparison_prompt = f"""
            Compare these two responses and calculate the percentage of deviation from the standard response.
            Consider differences in:
            - Content structure and organization
            - Tone and language style
            - Information completeness
            - Professional formality
            - Specific details and procedures
            
            Standard Response:
            {standard_response}
            
            Generated Response:
            {generated_response}
            
            Provide ONLY a numeric percentage (0-100) representing how much the generated response deviates from the standard.
            0% means identical, 100% means completely different.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert text comparison analyst. Provide only the numeric percentage of deviation."
                    },
                    {"role": "user", "content": comparison_prompt}
                ],
                max_tokens=50,
                temperature=0.1
            )
            
            # Extract percentage from response
            result = response.choices[0].message.content.strip()
            percentage_match = re.search(r'(\d+(?:\.\d+)?)', result)
            if percentage_match:
                return float(percentage_match.group(1))
            return 0.0
            
        except Exception as e:
            print(f"Error calculating deviation: {e}")
            return 0.0
    
    def get_deviation_tolerance_limit(self, tolerance: str) -> int:
        """Get the maximum allowed deviation percentage for a tolerance level"""
        return self.deviation_tolerance_settings.get(tolerance, self.deviation_tolerance_settings["minimal"])["limit"]
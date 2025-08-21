#!/usr/bin/env python3
"""
Templated Corporate Communication System

A modular system for generating personalized corporate responses to customer 
inquiries while maintaining organizational standards and measuring deviation tolerance.

Author: AI Assistant
Version: 2.0 (Refactored)
"""

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the main orchestrator
from src.communication_orchestrator import CommunicationOrchestrator


def main():
    """Main entry point for the application"""
    try:
        # Initialize the orchestrator with current directory as base path
        orchestrator = CommunicationOrchestrator(base_path=".")
        
        # Run the interactive application
        orchestrator.run()
        
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")


if __name__ == "__main__":
    main()

# Templated Corporate Communication System - Architecture

## Overview

The system has been refactored into a modular architecture with clear separation of concerns. Each module has a specific responsibility and well-defined interfaces.

## Module Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                               main.py                               │
│                         (Entry Point)                              │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────┐
│                CommunicationOrchestrator                           │
│                    (Main Coordinator)                              │
└─────┬─────────────┬─────────────┬─────────────┬─────────────────────┘
      │             │             │             │
┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
│ConfigManager│ │CommunicationEngine│ │ResponseProcessor│ │UserInterface│
│             │ │           │       │ │               │ │             │
│- Templates  │ │- OpenAI   │       │ │- Standard     │ │- User Input │
│- Responses  │ │- Deviation│       │ │  Response     │ │- Display    │
│- Company    │ │- Generation│      │ │- Analysis     │ │- Formatting │
│  Config     │ │           │       │ │- Placeholders │ │             │
└─────────────┘ └───────────────────┘ └───────────────┘ └─────────────┘
```

## Module Responsibilities

### 1. ConfigManager (`src/config_manager.py`)
**Purpose**: Centralized configuration management

**Responsibilities**:
- Load and parse JSON configuration files
- Cache configurations for performance
- Provide department-specific company information
- Handle configuration errors gracefully

**Key Methods**:
- `templates` - Get template prompts
- `standard_responses` - Get standard response templates
- `company_config` - Get company configuration
- `get_department_info()` - Get department-specific info
- `reload_configs()` - Refresh all configurations

### 2. CommunicationEngine (`src/communication_engine.py`)
**Purpose**: OpenAI API interactions and AI communication logic

**Responsibilities**:
- Manage OpenAI client connections
- Generate personalized responses with deviation control
- Calculate deviation percentages between responses
- Handle API errors and retries

**Key Methods**:
- `generate_personalized_response()` - Main response generation
- `calculate_deviation_percentage()` - Compare responses
- `get_deviation_tolerance_limit()` - Get tolerance limits

### 3. ResponseProcessor (`src/response_processor.py`)
**Purpose**: Response preparation and analysis coordination

**Responsibilities**:
- Prepare standard responses with data substitution
- Coordinate response generation workflow
- Analyze compliance and deviation
- Manage template field requirements

**Key Methods**:
- `prepare_standard_response()` - Fill placeholders in templates
- `generate_response()` - Complete response generation workflow
- `get_template_fields()` - Get required fields for templates

### 4. UserInterface (`src/user_interface.py`)
**Purpose**: User interaction and display management

**Responsibilities**:
- Handle all user input collection
- Format and display outputs
- Manage interactive workflows
- Error message display

**Key Methods**:
- `select_department()` - Department selection interface
- `select_template()` - Template selection interface
- `collect_customer_data()` - Customer data collection
- `display_response_result()` - Format final output

### 5. CommunicationOrchestrator (`src/communication_orchestrator.py`)
**Purpose**: Main coordinator and public API

**Responsibilities**:
- Coordinate all modules
- Provide main application workflow
- Expose programmatic API
- Handle top-level error management

**Key Methods**:
- `run()` - Interactive application mode
- `generate_single_response()` - Programmatic API
- `get_available_templates()` - List available templates

## Data Flow

1. **Initialization**: Orchestrator initializes all modules
2. **Configuration Loading**: ConfigManager loads all JSON configs
3. **User Interaction**: UserInterface handles input collection
4. **Response Processing**: ResponseProcessor prepares templates
5. **AI Generation**: CommunicationEngine calls OpenAI
6. **Analysis**: Response deviation is calculated
7. **Display**: UserInterface formats and shows results

## Configuration Files

### templates_config.json
Contains AI prompt templates for different communication types.

### standard_responses.json
Organization-approved response templates with placeholders.

### company_config.json
Company information, department details, and corporate policies.

## Benefits of This Architecture

1. **Separation of Concerns**: Each module has a single responsibility
2. **Testability**: Modules can be tested independently
3. **Maintainability**: Changes are isolated to specific modules
4. **Reusability**: Modules can be used independently
5. **Scalability**: Easy to extend with new features
6. **Error Isolation**: Errors are contained within modules
# LLM Payroll Integration Refactoring Guide

## Overview

This document describes the refactoring of the DataCollectorAgent and LLM client to follow the project's dependency injection patterns and integrate with the FastAPI application.

## Key Changes

### 1. Interface-Based Design

#### LLM Client Interface (`app/adapters/llm/llm_client_interface.py`)
- Created `ILLMClient` interface for LLM client implementations
- Follows the project's interface segregation pattern

#### Data Source Interfaces (`app/adapters/llm/data_source_interface.py`)
- `IEmployeeDataSource`: Interface for employee data sources
- `ICountryRulesDataSource`: Interface for country rules data sources

### 2. Refactored LLM Client (`app/adapters/llm/llm_client.py`)

**Before:**
- Global variables and functions
- Direct API key access
- No dependency injection

**After:**
- `LLMSettings` class using Pydantic for configuration
- `GeminiLLMClient` class implementing `ILLMClient`
- Proper error handling and retry logic
- Async support

### 3. Refactored Data Sources (`app/adapters/llm/data_sources.py`)

**Before:**
- Global dictionaries (`EMPLOYEE_DB`, `COUNTRY_RULES`)
- No abstraction

**After:**
- `StaticEmployeeDataSource` implementing `IEmployeeDataSource`
- `StaticCountryRulesDataSource` implementing `ICountryRulesDataSource`
- Async methods for data retrieval
- Maintains backward compatibility with legacy constants

### 4. Refactored Payroll Agents (`app/adapters/llm/payroll_agent.py`)

**Key Changes:**
- `AgentBase` now accepts `ILLMClient` via dependency injection
- `DataCollectorAgent` uses injected data sources
- `PayrollCrewOrchestrator` accepts all dependencies via constructor
- All methods are now async

### 5. Dependency Injection Container (`app/infrastructure/depency_container.py`)

**Added Functions:**
- `get_llm_settings()`: Returns LLM configuration
- `get_llm_client()`: Returns configured LLM client
- `get_employee_data_source()`: Returns employee data source
- `get_country_rules_data_source()`: Returns country rules data source
- `get_payroll_crew_orchestrator()`: Returns configured orchestrator

### 6. FastAPI Integration

#### New Route (`app/adapters/incoming/routes/llm_payroll.py`)
- `POST /api/v1/llm/calculate`: LLM-based payroll calculation endpoint
- Uses dependency injection for all components
- Proper error handling and HTTP status codes

#### Updated Main Application (`main.py`)
- Added LLM payroll router
- Organized routes with `/api/v1` prefix

## Usage Examples

### 1. Direct Usage (Programmatic)

```python
from app.infrastructure.depency_container import get_payroll_crew_orchestrator

# Create orchestrator
orchestrator = get_payroll_crew_orchestrator(
    employee_id="008-102",
    pay_period_start_date="2025-01-01",
    pay_period_end_date="2025-01-31",
    country_code="EC",
)

# Run payroll calculation
result = await orchestrator.run_payroll()
```

### 2. API Usage (HTTP)

```bash
curl -X POST "http://localhost:8000/api/v1/llm/calculate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "employee_id": "008-102",
    "pay_period_start_date": "2025-01-01",
    "pay_period_end_date": "2025-01-31",
    "country_code": "EC"
  }'
```

## Environment Variables

Add these to your `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

## Testing

Run the integration test:

```bash
python test_llm_integration.py
```

## Architecture Benefits

1. **Dependency Injection**: All dependencies are injected, making testing easier
2. **Interface Segregation**: Clear contracts for all components
3. **Async Support**: Full async/await support for better performance
4. **Configuration Management**: Centralized settings using Pydantic
5. **Error Handling**: Proper error handling and retry logic
6. **FastAPI Integration**: Seamless integration with the existing FastAPI application
7. **Backward Compatibility**: Legacy code still works with global constants

## File Structure

```
app/adapters/llm/
├── llm_client_interface.py      # LLM client interface
├── llm_client.py               # Gemini LLM client implementation
├── data_source_interface.py   # Data source interfaces
├── data_sources.py            # Static data source implementations
└── payroll_agent.py          # Refactored payroll agents

app/adapters/incoming/routes/
└── llm_payroll.py            # New LLM payroll API route

app/infrastructure/
└── depency_container.py      # Updated with LLM dependencies
```

## Migration Notes

- All existing code continues to work due to backward compatibility
- New LLM-based payroll processing is available via the new API endpoint
- The refactored components follow the project's established patterns
- Configuration is now centralized and environment-based

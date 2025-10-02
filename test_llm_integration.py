#!/usr/bin/env python3
"""
Test script to verify the LLM payroll integration works correctly.
"""

import asyncio
import json
from app.infrastructure.depency_container import get_payroll_crew_orchestrator


async def test_llm_payroll_integration():
    """Test the LLM payroll integration."""
    print("Testing LLM Payroll Integration...")

    try:
        # Create orchestrator with test data
        orchestrator = get_payroll_crew_orchestrator(
            employee_id="008-102",
            pay_period_start_date="2025-01-01",
            pay_period_end_date="2025-01-31",
            country_code="EC",
        )

        print("Orchestrator created successfully!")
        print("Running payroll calculation...")

        # Run the payroll calculation
        result = await orchestrator.run_payroll()

        print("Payroll calculation completed!")
        print("Result:")
        print(json.dumps(json.loads(result), indent=2))

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_llm_payroll_integration())

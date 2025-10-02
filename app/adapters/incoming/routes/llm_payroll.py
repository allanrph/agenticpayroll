from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.infrastructure.depency_container import get_payroll_crew_orchestrator
from app.utils.security import verify_api_key

router = APIRouter()


class LLMPayrollRequest(BaseModel):
    """Request model for LLM-based payroll processing."""

    employee_id: str
    pay_period_start_date: str
    pay_period_end_date: str
    country_code: str


@router.post("/llm/calculate", dependencies=[Depends(verify_api_key)])
async def calculate_payroll_with_llm(request: LLMPayrollRequest):
    """
    Calculate payroll using LLM-based crew agents.
    """
    try:
        orchestrator = get_payroll_crew_orchestrator(
            employee_id=request.employee_id,
            pay_period_start_date=request.pay_period_start_date,
            pay_period_end_date=request.pay_period_end_date,
            country_code=request.country_code,
        )

        result = await orchestrator.run_payroll()
        return {"result": result}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

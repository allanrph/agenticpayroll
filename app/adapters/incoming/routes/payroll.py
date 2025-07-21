from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse
from app.domains.payroll_record import PayrollRecord
from app.domains.employee import PayrollRequest
from app.infrastructure.database.session import get_async_db
from app.use_cases.calculate_payroll_use_case import CalculatePayrollUseCase
from app.infrastructure.depency_container import get_calculate_payroll_use_case
from app.utils.security import verify_api_key

router = APIRouter()

@router.post("/calculate", dependencies=[Depends(verify_api_key)])
async def calculate_payroll(
    request: PayrollRequest, calculate_payroll_use_case: CalculatePayrollUseCase = Depends(get_calculate_payroll_use_case)
):
    await calculate_payroll_use_case.execute(request)


@router.get("/payslip/{record_id}", dependencies=[Depends(verify_api_key)])
async def get_payslip(record_id: str, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(
        PayrollRecord.__table__.select().where(PayrollRecord.id == record_id)
    )
    record = result.fetchone()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found.")
    return FileResponse(record.payslip_path, media_type='application/pdf', filename="payslip.pdf")
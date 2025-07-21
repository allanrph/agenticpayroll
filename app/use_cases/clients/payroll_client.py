from abc import ABC


class IPayrollClient(ABC):
    async def update_payroll_run(self, company_id, body):
        pass

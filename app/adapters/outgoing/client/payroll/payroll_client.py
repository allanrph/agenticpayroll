import os

from app.infrastructure.HttpClientBase import HttpClientBase
from app.use_cases.clients.payroll_client import IPayrollClient


class PayrollClient(HttpClientBase, IPayrollClient):
    BASE_URL = os.environ.get('PAYROLL_API_URL', 'https://payroll.io')

    async def update_payroll_run(self, company_id, body):
        url = f'/company/{company_id}/payroll'
        response = await self.request('POST', url, json=body)
        return response.json()

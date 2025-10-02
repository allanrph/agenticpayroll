from payroll_agent import PayrollCrewOrchestrator

if __name__ == "__main__":
    employee_to_process = '008-102'
    payroll_start_date = "2025-09-01"
    payroll_end_date = "2025-09-30"
    country_context = "EC" 
    
    print(f"--- AI Agent Payroll System (Gemini Crew Model: {country_context}) ---")
    print("WARNING: This code is highly redundant for arithmetic but fulfills the Crew Model request.")
    
    orchestrator = PayrollCrewOrchestrator(employee_to_process, payroll_start_date, payroll_end_date, country_context)
    json_output = orchestrator.run_payroll()
    
    print("\n--- Final JSON Payroll Report ---\n")
    print(json_output)
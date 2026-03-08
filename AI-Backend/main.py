from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime, timedelta
import uvicorn

app = FastAPI(
    title="Sayam AI Backend",
    description="AI-powered forecasting and risk analysis for SME decisions",
    version="1.0.0"
)

# --------- CORS Configuration ---------
# Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- Models ---------

class ScenarioInfo(BaseModel):
    scenario_type: str = Field(..., description="Type: 'hiring' or 'inventory'")
    scenario_desc: str = Field(..., description="Description of the scenario")

class Expense(BaseModel):
    category: str = Field(..., example="Salary")
    amount: float = Field(..., gt=0, example=25000)

class ForecastInput(BaseModel):
    scenario_info: ScenarioInfo
    current_cash_balance: float = Field(..., gt=0, description="Current cash in hand")
    monthly_revenue: float = Field(..., gt=0, description="Monthly revenue in rupees")
    expenses: List[Expense] = Field(..., description="List of monthly expenses")
    decision_cost: float = Field(..., ge=0, description="One-time cost of the decision")
    decision_start_day: int = Field(..., ge=1, le=90, description="Day when decision takes effect")
    
    class Config:
        json_schema_extra = {
            "example": {
                "scenario_info": {
                    "scenario_type": "hiring",
                    "scenario_desc": "Hire Sales Associate"
                },
                "current_cash_balance": 450000,
                "monthly_revenue": 150000,
                "expenses": [
                    {"category": "Rent", "amount": 20000},
                    {"category": "Utilities", "amount": 5000},
                    {"category": "Inventory", "amount": 40000}
                ],
                "decision_cost": 25000,
                "decision_start_day": 7
            }
        }

class DailyProjection(BaseModel):
    day: int
    cash: float

class ForecastOutput(BaseModel):
    success: bool
    scenario: ScenarioInfo
    baseline_projection: List[dict]
    decision_projection: List[dict]
    disturbance_day: Optional[int]
    lowest_cash_point: float
    lowest_cash_day: int
    risk: bool

# --------- Routes ---------

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "Sayam AI Backend is running",
        "version": "1.0.0",
        "endpoints": {
            "forecast": "/forecast",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.post("/forecast", response_model=ForecastOutput, tags=["Forecasting"])
def generate_forecast(data: ForecastInput):
    """
    Generate 90-day cash flow forecast comparing baseline vs decision impact
    
    Returns two projections:
    - Baseline: Business as usual (no decision)
    - Decision: With the decision applied on specified day
    """
    
    try:
        # Calculate daily cash flow
        monthly_revenue = data.monthly_revenue
        total_expenses = sum(exp.amount for exp in data.expenses)
        
        daily_revenue = monthly_revenue / 30
        daily_expenses = total_expenses / 30
        
        # Initialize cash balances
        baseline_cash = data.current_cash_balance
        decision_cash = data.current_cash_balance
        
        # Generate projections
        baseline_projection = []
        decision_projection = []
        
        # Baseline projection (no decision)
        for day in range(1, 91):
            baseline_cash += daily_revenue
            baseline_cash -= daily_expenses
            
            baseline_projection.append({
                "day": day,
                "cash": round(baseline_cash, 2)
            })
        
        # Decision projection (with decision cost)
        for day in range(1, 91):
            decision_cash += daily_revenue
            decision_cash -= daily_expenses
            
            # Apply decision cost on specified day
            if day == data.decision_start_day:
                decision_cash -= data.decision_cost
            
            decision_projection.append({
                "day": day,
                "cash": round(decision_cash, 2)
            })
        
        # Detect disturbance day (when decision impact first appears)
        disturbance_day = None
        for base, dec in zip(baseline_projection, decision_projection):
            if dec["cash"] < base["cash"]:
                disturbance_day = dec["day"]
                break
        
        # Find lowest cash point in decision projection
        lowest_cash = min(p["cash"] for p in decision_projection)
        lowest_day = next(p["day"] for p in decision_projection if p["cash"] == lowest_cash)
        
        # Risk flag: cash goes negative
        risk_flag = lowest_cash < 0
        
        return ForecastOutput(
            success=True,
            scenario=data.scenario_info,
            baseline_projection=baseline_projection,
            decision_projection=decision_projection,
            disturbance_day=disturbance_day,
            lowest_cash_point=round(lowest_cash, 2),
            lowest_cash_day=lowest_day,
            risk=risk_flag
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast generation failed: {str(e)}")

# --------- Run Server ---------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )
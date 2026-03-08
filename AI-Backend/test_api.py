"""
Test file for Sayam AI Backend - Decision Impact Simulator
Run with: pytest test_api.py -v
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Sayam AI Backend is running" in response.json()["status"]


def test_forecast_basic():
    """Test basic forecast generation"""
    payload = {
        "scenario_info": {
            "scenario_type": "hiring",
            "scenario_desc": "Hire Sales Associate"
        },
        "current_cash_balance": 450000,
        "monthly_revenue": 150000,
        "expenses": [
            {"category": "Rent", "amount": 20000},
            {"category": "Utilities", "amount": 5000}
        ],
        "decision_cost": 25000,
        "decision_start_day": 7
    }
    
    response = client.post("/forecast", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] == True
    assert len(data["baseline_projection"]) == 90
    assert len(data["decision_projection"]) == 90
    assert data["disturbance_day"] == 7  # Decision applied on day 7


def test_forecast_no_risk():
    """Test forecast with healthy cash flow (no risk)"""
    payload = {
        "scenario_info": {
            "scenario_type": "hiring",
            "scenario_desc": "Hire Junior Staff"
        },
        "current_cash_balance": 500000,
        "monthly_revenue": 200000,
        "expenses": [
            {"category": "Rent", "amount": 30000},
            {"category": "Utilities", "amount": 10000}
        ],
        "decision_cost": 20000,
        "decision_start_day": 1
    }
    
    response = client.post("/forecast", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] == True
    assert data["risk"] == False  # No risk
    assert data["lowest_cash_point"] > 0  # Cash stays positive


def test_forecast_with_risk():
    """Test forecast that triggers risk (cash goes negative)"""
    payload = {
        "scenario_info": {
            "scenario_type": "expansion",
            "scenario_desc": "Store Expansion"
        },
        "current_cash_balance": 100000,
        "monthly_revenue": 80000,
        "expenses": [
            {"category": "Rent", "amount": 40000},
            {"category": "Salaries", "amount": 50000}
        ],
        "decision_cost": 150000,  # Large cost
        "decision_start_day": 5
    }
    
    response = client.post("/forecast", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] == True
    assert data["risk"] == True  # Risk detected
    assert data["lowest_cash_point"] < 0  # Cash goes negative


def test_forecast_decision_impact():
    """Test that decision projection differs from baseline"""
    payload = {
        "scenario_info": {
            "scenario_type": "inventory",
            "scenario_desc": "Buy Stock"
        },
        "current_cash_balance": 300000,
        "monthly_revenue": 150000,
        "expenses": [
            {"category": "Rent", "amount": 20000}
        ],
        "decision_cost": 50000,
        "decision_start_day": 10
    }
    
    response = client.post("/forecast", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    
    # Before decision day, both should be equal
    baseline_day_5 = data["baseline_projection"][4]["cash"]
    decision_day_5 = data["decision_projection"][4]["cash"]
    assert baseline_day_5 == decision_day_5
    
    # After decision day, decision should be lower
    baseline_day_15 = data["baseline_projection"][14]["cash"]
    decision_day_15 = data["decision_projection"][14]["cash"]
    assert decision_day_15 < baseline_day_15


def test_forecast_invalid_input():
    """Test forecast with invalid input"""
    payload = {
        "scenario_info": {
            "scenario_type": "test",
            "scenario_desc": "Invalid"
        },
        "current_cash_balance": -1000,  # Invalid: negative
        "monthly_revenue": 100000,
        "expenses": [],
        "decision_cost": 10000,
        "decision_start_day": 1
    }
    
    response = client.post("/forecast", json=payload)
    assert response.status_code == 422  # Validation error


def test_forecast_disturbance_detection():
    """Test disturbance day detection"""
    payload = {
        "scenario_info": {
            "scenario_type": "hiring",
            "scenario_desc": "Hire Manager"
        },
        "current_cash_balance": 400000,
        "monthly_revenue": 150000,
        "expenses": [
            {"category": "Rent", "amount": 25000}
        ],
        "decision_cost": 30000,
        "decision_start_day": 15
    }
    
    response = client.post("/forecast", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["disturbance_day"] == 15  # Should match decision start day


if __name__ == "__main__":
    print("Running Sayam AI Backend Tests...\n")
    
    print("✓ Testing health check...")
    test_health_check()
    
    print("✓ Testing basic forecast...")
    test_forecast_basic()
    
    print("✓ Testing no risk scenario...")
    test_forecast_no_risk()
    
    print("✓ Testing risk scenario...")
    test_forecast_with_risk()
    
    print("✓ Testing decision impact...")
    test_forecast_decision_impact()
    
    print("✓ Testing invalid input...")
    test_forecast_invalid_input()
    
    print("✓ Testing disturbance detection...")
    test_forecast_disturbance_detection()
    
    print("\n✅ All tests passed! Sayam AI is ready.")

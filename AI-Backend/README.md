# Sayam AI Backend

FastAPI-based AI service for forecasting and risk analysis.

## Features

- **Decision Impact Simulation** - Compare baseline vs decision scenarios
- **90-Day Cash Flow Projection** - Deterministic daily projections
- **Disturbance Detection** - Identify when decision impact begins
- **Risk Detection** - Flag when cash goes negative
- **Graph-Ready Output** - Two projections for visualization

## Setup

### 1. Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Server

```bash
# Development (with auto-reload)
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access API

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
```bash
GET /
```

### Generate Forecast
```bash
POST /forecast
```

**Request Body:**
```json
{
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
```

**Response:**
```json
{
  "success": true,
  "scenario": {...},
  "baseline_projection": [
    {"day": 1, "cash": 454166.67},
    {"day": 2, "cash": 458333.33},
    ...90 days
  ],
  "decision_projection": [
    {"day": 1, "cash": 454166.67},
    {"day": 7, "cash": 429166.67},  // Decision cost applied
    ...90 days
  ],
  "disturbance_day": 7,
  "lowest_cash_point": 429166.67,
  "lowest_cash_day": 7,
  "risk": false
}
```

## Testing

### Manual Testing with curl

```bash
curl -X POST "http://localhost:8000/forecast" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

### Using Swagger UI

1. Go to http://localhost:8000/docs
2. Click on `/forecast` endpoint
3. Click "Try it out"
4. Edit the request body
5. Click "Execute"

## Project Structure

```
AI-Backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── venv/               # Virtual environment (gitignored)
└── .env                # Environment variables (future)
```

## Future Enhancements

- [ ] Add ML models (Scikit-learn)
- [ ] Integrate with AWS SageMaker
- [ ] Add pattern recognition
- [ ] Historical data analysis
- [ ] Seasonal trend detection
- [ ] Database integration
- [ ] Authentication/Authorization
- [ ] Rate limiting
- [ ] Caching

## Development

### Add New Endpoint

```python
@app.post("/new-endpoint", tags=["Category"])
def new_endpoint(data: InputModel):
    # Your logic here
    return {"result": "success"}
```

### Run Tests (Future)

```bash
pytest
```

## Deployment

### Docker (Future)

```bash
docker build -t sayam-ai .
docker run -p 8000:8000 sayam-ai
```

### AWS Lambda (Future)

Use Mangum adapter for serverless deployment.

## Notes

- Currently using rule-based forecasting
- ML models will be added in v1.1
- Keep it simple for MVP!

---

Built with ❤️ using FastAPI

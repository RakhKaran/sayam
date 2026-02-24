# Sayam Platform

> AI-powered decision visibility platform for Indian SMEs and retailers

**Tagline:** See Your Future, Decide with Confidence

## Overview

Sayam helps Indian small business owners simulate tactical decisions (hiring, inventory purchases, store launches) before committing resources. The platform provides cash flow projections, risk alerts, and comparative analysis to transform uncertain business decisions into data-backed strategic moves.

## Project Structure

```
sayam-platform/
├── frontend/          # React Native mobile app
├── backend/           # Node.js/Express API server
├── ai-backend/        # Python ML services (future)
├── docs/              # Documentation
├── design/            # Design assets
├── firebase/          # Firebase configuration
└── scripts/           # Utility scripts
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed structure.

## Current Phase: MVP

**Timeline:** 4 months  
**Target:** 20 pilot users, 70%+ satisfaction

### MVP Features
- ✅ Phone authentication (OTP)
- ✅ Business profile setup
- ✅ Hiring scenario simulation
- ✅ Inventory purchase simulation
- ✅ Cash flow visualization
- ✅ Risk alerts
- ✅ Scenario comparison
- ✅ Hindi + English support
- ✅ Android app

### Not in MVP
- ❌ Voice interface
- ❌ Offline capability
- ❌ ML-powered forecasting
- ❌ Third-party integrations
- ❌ iOS app

## Tech Stack

### Frontend
- **Expo** (React Native)
- TypeScript
- React Native Paper
- Expo Router
- Axios

### Backend
- **LoopBack 4** (Node.js)
- TypeScript
- Firebase (Auth + Firestore)
- OpenAPI 3.0

### AI Backend (Future)
- **FastAPI** (Python)
- Scikit-learn
- AWS SageMaker
- TensorFlow

## Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn
- React Native CLI
- Android Studio (for Android development)
- Python 3.9+ (for AI backend, future)
- Firebase account

### Setup

1. **Clone repository**
```bash
git clone <repository-url>
cd sayam-platform
```

2. **Run setup script**
```bash
# Mac/Linux
chmod +x scripts/setup-project.sh
./scripts/setup-project.sh

# Windows
scripts\setup-project.bat
```

3. **Setup Frontend**
```bash
cd frontend
npx react-native init SayamApp --template react-native-template-typescript
# Move files to current directory
npm install
```

4. **Setup Backend**
```bash
cd backend
npm init -y
npm install express cors dotenv firebase-admin
npm install --save-dev typescript @types/node @types/express ts-node nodemon
```

5. **Setup Firebase**
- Create project at [Firebase Console](https://console.firebase.google.com)
- Enable Authentication (Phone)
- Create Firestore database
- Download service account key
- Add credentials to `.env` files

6. **Configure Environment Variables**
```bash
# Copy example files
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env

# Edit with your Firebase credentials
```

7. **Start Development**
```bash
# Terminal 1: Start backend
cd backend
npm run dev

# Terminal 2: Start frontend
cd frontend
npm start
npm run android
```

## Documentation

- [Requirements](docs/mvp-requirements.md) - MVP requirements
- [Design](docs/mvp-design.md) - MVP technical design
- [Figma Specs](docs/figma-design-prompt.md) - UI design specifications
- [Project Structure](PROJECT_STRUCTURE.md) - Folder organization
- [API Documentation](docs/api/) - API endpoints (coming soon)

## Development Workflow

### Frontend Development (Expo)
```bash
cd frontend
npx expo start      # Start dev server
# Press 'a' for Android, 'i' for iOS
npm test            # Run tests
```

### Backend Development (LoopBack 4)
```bash
cd backend
npm start           # Start LB4 server
npm run dev         # Start with auto-reload
npm test            # Run tests
```

### AI Backend Development (FastAPI)
```bash
cd ai-backend
source venv/bin/activate
uvicorn src.api.main:app --reload
pytest              # Run tests
```

## Team

- **Frontend Developer** - React Native mobile app
- **Backend Developer** - API server & business logic
- **Designer** - UI/UX design
- **Product Manager** - Requirements & user testing

## Roadmap

### MVP (Months 1-4)
- [x] Project setup
- [ ] Backend API development
- [ ] Frontend UI development
- [ ] Integration & testing
- [ ] Play Store launch

### v1.1 (Months 5-6)
- [ ] iOS app
- [ ] Store launch scenario
- [ ] Basic ML forecasting
- [ ] Decision tracking

### v1.2 (Months 7-8)
- [ ] Offline capability
- [ ] 3 more regional languages
- [ ] CSV import
- [ ] Enhanced visualizations

### v2.0 (Months 9-12)
- [ ] Voice interface
- [ ] Advanced ML models
- [ ] Third-party integrations
- [ ] Pattern recognition

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m 'feat(frontend): add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Create Pull Request

### Commit Convention
- `feat(scope)`: New feature
- `fix(scope)`: Bug fix
- `docs`: Documentation changes
- `chore`: Maintenance tasks
- `test`: Test changes

## License

Proprietary - All rights reserved

## Contact

- **Email**: support@sayam.app (placeholder)
- **Website**: https://sayam.app (placeholder)

---

Built with ❤️ for Indian SMEs

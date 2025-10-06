# Contributing to GRE Mentor

## Development Setup

1. Fork the repository
2. Clone your fork
3. Follow SETUP.md for local development
4. Create a feature branch: `git checkout -b feature/amazing-feature`

## Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Run tests before committing

**TypeScript/React:**
- Use functional components with hooks
- Follow existing component patterns
- Use TypeScript strict mode
- Keep components small and focused

## Testing

All new features must include tests:

**Backend:**
```bash
cd backend
pytest tests/test_your_feature.py
```

**Frontend:**
```bash
cd frontend
npm test
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description

## Areas for Contribution

- Additional practice modes (multiple choice, typing)
- Voice command integration
- Enhanced analytics dashboard
- Question bank UI
- Mobile responsive improvements
- Additional import formats
- Improved mnemonic generation prompts

## Questions?

Open an issue for discussion before starting major changes.

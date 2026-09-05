# Contributing Guide

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ai-drama-generator.git`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Install dependencies: `pip install -r requirements.txt`

## Development Setup

```bash
# Install in development mode
pip install -e .

# Install dev dependencies
pip install pytest pytest-asyncio black flake8
```

## Making Changes

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings to all functions
- Keep functions small and focused

### Testing
```bash
pytest tests/
```

### Commit Messages
- Use clear, descriptive commit messages
- Format: `feat/fix/docs/test: description`
- Example: `feat: add subtitle support to video editor`

## Pull Request Process

1. Update README.md with any new features
2. Add/update tests for new functionality
3. Ensure all tests pass: `pytest`
4. Run linter: `black src/ && flake8 src/`
5. Submit PR with detailed description

## Areas for Contribution

### High Priority
- [ ] Improve video generation quality
- [ ] Add more drama genres
- [ ] Optimize processing speed
- [ ] Add batch processing UI

### Medium Priority
- [ ] Multi-language support
- [ ] Web interface
- [ ] Real-time preview
- [ ] Advanced subtitle generation

### Nice to Have
- [ ] 3D character animation
- [ ] Live streaming integration
- [ ] Mobile app
- [ ] Cloud deployment

## Reporting Issues

- Check existing issues first
- Include your environment (OS, Python version, GPU info)
- Provide minimal reproducible example
- Include error logs and screenshots

## Questions?

Open a GitHub discussion or issue with questions!

Thank you for contributing! 🚀

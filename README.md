# Pomodoro Timer

A clean architecture implementation of a Pomodoro Timer with menu bar integration.

## Installation

### Production
```bash
pip install -r requirements.txt
python run.py
```


### Development
#### Install development dependencies
```bash
pip install -r requirements-dev.txt
```

#### Run tests
```bash
make test
```

#### Run linter
```bash
make lint
```

#### Run formatter
```bash
make format
```

#### Clean up cache files
```bash
make clean
```

This project uses:
- `pytest` for testing
- `black` for code formatting
- `isort` for import sorting
- `flake8` for linting
- `mypy` for type checking

### Project Structure
```
pomodoro_timer/
├── src/
│ ├── domain/ # Business logic and interfaces
│ ├── application/ # Use cases and application services
│ ├── infrastructure/ # External implementations
│ └── presentation/ # UI components
├── tests/ # Test files
├── requirements.txt # Production dependencies
└── requirements-dev.txt # Development dependencies
```

### Running Tests
```bash
make test
```


### Run specific test file
```bash
pytest tests/test_domain/test_entities.py
```

### Run tests with verbose output
```bash
pytest -v
```


## Features

- Clean Architecture implementation
- Menu bar integration
- Configurable work/rest durations
- Sound notifications
- Settings persistence
- Multi-process architecture

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Format your code (`make format`)
4. Ensure tests pass (`make test`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

MIT

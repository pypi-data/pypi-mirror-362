# nb-ui: Beautiful Components for Jupyter Notebooks

Modern UI components for Jupyter notebooks with auto-rendering support. No HTML/CSS required.

## 🚀 Quick Start

```python
from nb_ui import Header, Card, CodeBlock, Typography, Container
from nb_ui import success, warning, error, info, set_theme

# Set theme and create components
set_theme("material")
Header("My Analysis", subtitle="Data Science Report")
Card("Key findings here", title="Results")
success("Model training completed!")
```

## 📦 Components

- **Header** - Section titles and subtitles
- **Card** - Content containers with titles
- **Alert/success/warning/error/info** - Status messages
- **CodeBlock** - Syntax-highlighted code
- **Typography** - Professional text styling
- **Container** - Centered layout wrapper

## 🎨 Themes

Available themes: `material`, `antd`, `dark`

```python
set_theme("material")  # or "antd", "dark"
```

**Note**: Themes are inspired by Material Design and Ant Design principles and are subject to change in future versions.

## 🧪 Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_cards.py -v

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing
```

## 📝 Development

```bash
# Install in development mode
pip install -e .

# Run example notebook
jupyter notebook demo_usage.ipynb
```

## 📄 License

MIT License

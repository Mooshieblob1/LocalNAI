# LocalNAI

A modern local client for NovelAI image generation with advanced features and intuitive UI built with PyQt6.

## Features

- 🎨 **Modern Dark UI** - Clean, professional interface with glassmorphism effects
- 🏷️ **Smart Tag Autocomplete** - 93k+ tag database with real-time suggestions and category highlighting
- ⚖️ **Advanced Weighting** - Ctrl+Up/Down to adjust tag weights with `weight::tag::` format
- 🖼️ **Image Management** - Right-click context menu for copy/save operations with metadata
- ⚙️ **Full Parameter Control** - All NovelAI generation parameters (model, sampler, scheduler, etc.)
- 🔄 **Opus Limits** - Built-in resolution limits for Opus subscriptions
- 💾 **Metadata Support** - Full EXIF data preservation and clipboard operations
- 🎯 **Quality Presets** - One-click quality enhancement and filtering tags

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Mooshieblob1/LocalNAI.git
cd LocalNAI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your NovelAI credentials:
   - Create a `.env` file in the project root
   - Add your NovelAI token: `NOVELAI_TOKEN=your_token_here`

4. Run the application:
```bash
python main.py
```

## Configuration

The application automatically loads tag data from `tags/tags.csv` for autocomplete functionality. The included database contains 93,908 tags with categories and usage counts.

## Usage

### Basic Generation
1. Enter your prompt in the text field (with autocomplete suggestions)
2. Adjust parameters as needed (resolution, steps, CFG, etc.)
3. Click "🚀 Generate Image"
4. Right-click generated images for save/copy options

### Tag Weighting
- Highlight any tag and use **Ctrl+↑** to increase weight by 0.1
- Use **Ctrl+↓** to decrease weight by 0.1
- Displays as: `(masterpiece:1.2)` 
- Sends to API as: `1.2::masterpiece::`

### Tag Autocomplete
- Start typing any tag name
- Use arrow keys to navigate suggestions
- Press Enter or click to insert
- Tags are automatically formatted (underscores removed, parentheses escaped)

### Quality Settings
- **Enhanced Quality**: Adds positive quality tags automatically
- **Quality Filtering**: Adds negative quality tags to reduce artifacts

## Project Structure

```
LocalNAI/
├── main.py                 # Application entry point
├── config.py              # Configuration management
├── novelai_api.py         # NovelAI API wrapper
├── requirements.txt       # Python dependencies
├── .env                   # API credentials (create this)
├── api/
│   └── novelai.py        # Core API client
├── gui/
│   ├── main_window.py    # Main application window
│   ├── tag_autocomplete.py # Tag completion widget
│   ├── image_viewer.py   # Image display and context menu
│   ├── custom_widgets.py # Custom UI components
│   └── styles.py         # Application styling
├── utils/
│   ├── tag_manager.py    # Tag database management
│   ├── image_handler.py  # Image processing utilities
│   └── prompt_converter.py # Weight format conversion
└── tags/
    └── tags.csv          # Tag database (93k+ tags)
```

## Requirements

- Python 3.7+
- PyQt6
- NovelAI subscription with API access
- At least 4GB RAM recommended

## Supported Models

- nai-diffusion-4-5-full
- nai-diffusion-4-5-curated
- nai-diffusion-4-full
- nai-diffusion-4-curated-preview
- nai-diffusion-3
- nai-diffusion-furry-3

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

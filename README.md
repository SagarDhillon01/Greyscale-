# Grayscale Image Converter

This project provides a very simple Python app that converts a colored image into a grayscale image using OpenCV.

## Overview

The app can be used in two ways:

- As a Python function to convert image files on disk
- As a small web app where you upload an image and download the grayscale version

## Installation

```bash
git clone https://github.com/yourusername/opencv-grayscale-project.git
cd opencv-grayscale-project
pip install -r requirements.txt
```

## Usage

### Python example

```python
from src.grayscale_converter import convert_to_grayscale

convert_to_grayscale("path/to/colored_image.jpg", "path/to/output_image.jpg")
```

### Web app example

```bash
python src/grayscale_converter.py
```

Then open your browser at http://localhost:5000 and upload an image.

## Running Tests

```bash
python -m unittest discover -s tests -v
```

## GitHub and deployment

1. Push this repository to GitHub.
2. Connect it to a hosting service such as Render, Heroku, or Railway.
3. Use the existing Procfile so the app starts with:

```bash
python src/grayscale_converter.py
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
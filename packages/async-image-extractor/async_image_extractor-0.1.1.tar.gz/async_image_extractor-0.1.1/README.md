# medimage-extractor

**medimage-extractor** is a Python package that uses Google's Gemini API to extract structured text from a batch of images. It supports async batch processing, customizable prompts, and model selection.

---

## 🚀 Features

- 🔍 Extracts English text from images using Gemini.
- ✅ Special handling for forms, checkboxes, and tables.
- ⚡ Asynchronous batch processing for speed.
- 🧠 Customizable prompt and model.
- 📦 Easy to use and extend.

---
## 🧾 Input Format
Each image in the list should be a format accepted by the Gemini API:

- Base64-encoded image string
- File-like object
- Raw image bytes
- You can preprocess PIL or OpenCV images to bytes/base64 before passing


---

##  Installation

Install using `pip`

For the latest stable release:

```bash
pip install medimage-extractor
```

## Usage

Initialize the extractor

``` python
from async_image_extractor import ImageTextExtractor
import asyncio
import time
from google import genai

# Setup Gemini client
# Setup Gemini client
client = genai.Client(api_key="GEMINI_API_KEY")

# Initialize extractor
extractor = ImageTextExtractor(
    client=client,
    model="gemini-2.0-flash",
    prompt="Extract all text from this medical image, preserving structure."
)

```

Run the extractor on a list of images

``` python
# images: a list of image objects (e.g., base64 strings or Gemini-compatible input)
results = asyncio.run(extractor.process_images(images))
```

The output will be in a list format, each item represents an image

``` bash
[
  "Patient Name: James\nAge: 32\nDiagnosis: Diabetes \n...",
  "Results:\n- Glucose: High\n- Hemoglobin: Normal\n...",
  "Discharge Instructions:\nTake insulin twice a day.\nFollow up in 1 week.\n...",
  ...
]
```
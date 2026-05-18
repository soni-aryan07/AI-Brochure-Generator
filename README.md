# AI Brochure Generator

This is a beginner-friendly Python project that creates brochure-style text using the OpenAI API.

## What this project does

- Gets content from a website
- Uses AI to turn that content into brochure-style text
- Reads your API key from a `.env` file
- Can be run in a Python script or a Jupyter notebook

## Tools used

- Python
- OpenAI
- requests
- BeautifulSoup
- python-dotenv
- Jupyter Notebook

## Files in this project

- `main.py` — main Python file
- `build_brochure.py` — Python version of the project
- `build_brochure.ipynb` — notebook version of the project
- `pyproject.toml` — project setup file
- `uv.lock` — dependency lock file
- `.env` — file for your API key
- `.gitignore` — file that keeps secret files out of GitHub

## How to set up

1. Open the project folder in VS Code.
2. Make sure the required packages are installed.
3. Create a `.env` file in the project folder.
4. Add your API key inside the `.env` file like this:

```env
OPENAI_API_KEY=your_api_key_here
```

## How to run

If you are using the Python file:

```bash
python main.py
```

If you are using the notebook, open:

```bash
build_brochure.ipynb
```

## Important note

Do not upload your `.env` file to GitHub because it contains your private API key.

## What I learned

This project helped me learn:

- How to use APIs
- How to keep API keys safe
- How to work with web scraping
- How to use AI in Python
- How to build a small Python project

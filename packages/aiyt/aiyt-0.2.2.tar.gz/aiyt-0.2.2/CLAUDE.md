# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
- `uv run streamlit run aiyt/main.py` - Run the Streamlit app directly
- `aiyt` - Run via entry point (after installation)
- `uvx aiyt` - Run with uvx without installation
- `uv tool install aiyt` - Install locally as a tool

### Development Tools
- `ruff check` - Run linting (configured in pyproject.toml)
- `ruff format` - Format code
- `pytest` - Run tests (dev dependency)

### Package Management
- `uv sync` - Sync dependencies
- `uv add <package>` - Add new dependency
- `uv add --dev <package>` - Add development dependency

## Architecture

This is a Python Streamlit application for transcribing, chatting with, and summarizing YouTube videos using Google's Gemini AI.

### Core Components

**Entry Point**: `launcher.py`
- Simple Click-based CLI that launches the Streamlit app
- Main entry point defined in pyproject.toml as `aiyt = "launcher:main"`

**Main Application**: `aiyt/main.py`
- Sets up the Streamlit app with CSS styling
- Handles API key input and YouTube URL validation
- Routes to either caption extraction or audio transcription based on availability

**UI Components**: `aiyt/ui.py`
- `app_header()` - Renders the main header with icon and description
- `caption_ui()` - Interface for extracting existing captions (srt, txt, ai formatted)
- `transcribe_ui()` - Interface for transcribing audio when captions aren't available
- `divider()` - Simple divider component

**Core Utilities**: `aiyt/utils.py`
- `youtube_obj()` - Creates and validates YouTube objects
- `add_punctuation()` - Uses Gemini to add punctuation to raw transcripts
- `download_yt_audio()` - Downloads lowest quality audio stream to buffer
- `upload_gemini_audio()` - Uploads audio to Gemini cloud storage
- `transcribe()` - Transcribes audio using Gemini API

### Key Dependencies
- `streamlit` - Web UI framework
- `pytubefix` - YouTube video/audio downloading
- `google-genai` - Google Gemini AI client
- `click` - CLI framework for launcher
- `watchdog` - File system monitoring (likely for development)

### Data Flow
1. User inputs Gemini API key and YouTube URL
2. App validates URL and creates YouTube object
3. If captions exist → extract and optionally format with AI
4. If no captions → download audio → upload to Gemini → transcribe
5. Display results in Streamlit text area

### Configuration
- Ruff linting configured in pyproject.toml with specific ignores
- Project metadata and dependencies managed via pyproject.toml
- CSS styling loaded from root-level `style.css`
# Prospector Tool Documentation

## Overview

`prospector.py` is a Python script designed to extract company prospect data from a specific Microsoft blog post URL. It can scrape company names, associated URLs, and descriptions. Additionally, it offers functionality to:

*   Save the extracted data to a file (`data_file.txt`).
*   Recursively scrape the content of the extracted URLs.
*   Summarize the scraped web content using the Google Gemini Pro 2.5 AI model.
*   Print only the extracted URLs to the console.

## Dependencies

The script relies on the following Python libraries:

*   `requests-html`: For web scraping and HTML parsing.
*   `regex`: For text manipulation (specifically cleaning extracted text).
*   `argparse`: For handling command-line arguments.
*   `logging`: For managing log output levels.
*   `python-dotenv`: For loading environment variables from a `.env` file.
*   `google-generativeai`: For interacting with the Google Gemini API.

Install dependencies using pip:
```bash
pip install requests-html regex argparse python-dotenv google-generativeai
```

## Setup

1.  **Environment Variables:** The script requires a Google API key for the summarization feature.
    *   Create a file named `.env` in the same directory as the script.
    *   Add your Google API key to the `.env` file:
        ```
        GOOGLE_API_KEY=YOUR_API_KEY_HERE
        ```
    *   Replace `YOUR_API_KEY_HERE` with your actual key. **Do not commit the `.env` file to version control.**

## Usage

Run the script from the command line using `python prospector.py` followed by options:

```bash
python prospector.py [options]
```

### Command-Line Options

*   **`-h`, `--help`**: Show the help message and exit.
*   **`-d`, `--datafile`**: Extract data and write it to `data_file.txt`. Each entry is saved as a Python dictionary string on a new line.
*   **`-p`, `--printonly`**: Extract data and print only the company URLs to the standard output.
*   **`-r`, `--readurl`**: Extract data, then scrape each extracted URL, display the first 2000 characters of its text content, and provide an AI-generated summary using Google Gemini.
*   **`-v`, `--verbose`**: Enable verbose logging output. By default, logging is disabled.
*   **`-x`, `--xray`**: (Currently not implemented) Intended for dumping detailed debug data structures.

### Examples

1.  **Extract data and save to file:**
    ```bash
    python prospector.py -d
    ```
2.  **Extract URLs, scrape content, and summarize:**
    ```bash
    python prospector.py -r
    ```
3.  **Print only extracted URLs:**
    ```bash
    python prospector.py -p
    ```
4.  **Save to file with verbose logging:**
    ```bash
    python prospector.py -d -v
    ```

If run with no options, the script will print the help message.

## Functionality Details

*   **`extract_data()`**: Connects to the hardcoded Microsoft blog URL, parses the HTML using XPath selectors to find lists of companies, extracts company names, URLs, and descriptions, cleans the text, and returns a list of dictionaries.
*   **`summarize_text_with_gemini(text)`**: Takes text (up to 2000 characters) as input, sends it to the Google Gemini Pro 2.5 API via the `google-generativeai` library, and returns a concise summary. Requires a valid `GOOGLE_API_KEY` in the `.env` file.
*   **`scrape_and_display_text(url)`**: Takes a URL, scrapes its text content using `requests-html`, displays the first 1000 characters, calls `summarize_text_with_gemini` to get a summary, and prints the summary.
*   **`main()`**: Parses command-line arguments, sets the logging level, calls `extract_data()`, and then performs actions based on the provided arguments (writing to file, printing URLs, or scraping/summarizing).
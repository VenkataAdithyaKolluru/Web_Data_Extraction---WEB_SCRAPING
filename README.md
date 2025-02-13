## Overview
This project is a Flask web application that allows users to scrape web pages, perform sentiment analysis, text classification, and language detection on the extracted data.

## Features
- Web scraping using BeautifulSoup
- Sentiment analysis with TextBlob
- Text classification using Hugging Face Transformers
- Language detection with langdetect
- Downloadable CSV file of the extracted data

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd MP_09
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python app2.py
   ```

2. Open your web browser and go to `http://127.0.0.1:3000`.

3. Enter the URL, tag, class name, and file name in the form, and select any additional analysis options.

4. Click the "Scrape" button to extract data and download the results as a CSV file.

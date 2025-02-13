from flask import Flask, request, render_template, send_file
import pandas as pd
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob  # Import TextBlob for sentiment analysis
from transformers import pipeline  # Import transformers pipeline for text classification
from langdetect import detect, LangDetectException  # Import langdetect for language detection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    # Get form data
    url = request.form['url']
    tag = request.form['tag']
    file_name = request.form['file_name']
    perform_sentiment = 'sentiment_analysis' in request.form  # Check if sentiment analysis is requested
    perform_classification = 'text_classification' in request.form  # Check if text classification is requested
    perform_language_detection = 'language_detection' in request.form  # Check if language detection is requested

    # Fetch the webpage content
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}", 500

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract data based on the provided tag
    data = soup.find_all(tag)

    # Extract text from the HTML elements
    extracted_data = [item.get_text(strip=True) for item in data]

    # Perform sentiment analysis if requested
    if perform_sentiment:
        sentiment_scores = []
        for text in extracted_data:
            blob = TextBlob(text)
            sentiment_scores.append(blob.sentiment.polarity)  # Get sentiment polarity

        # Create a DataFrame with the extracted data and sentiment scores
        df = pd.DataFrame({
            'Data': extracted_data,
            'Sentiment': sentiment_scores
        })
    else:
        # Create a DataFrame with only the extracted data
        df = pd.DataFrame(extracted_data, columns=['Data'])

    # Perform text classification if requested
    if perform_classification:
        try:
            classifier = pipeline('text-classification')
            classification_results = [classifier(text)[0]['label'] for text in extracted_data]
            df['Classification'] = classification_results
        except Exception as e:
            print(f"Error during text classification: {e}")
            df['Classification'] = ['Error'] * len(extracted_data)

    # Perform language detection if requested
    if perform_language_detection:
        try:
            languages = []
            for text in extracted_data:
                try:
                    languages.append(detect(text))
                except LangDetectException:
                    languages.append('Unknown')
            df['Language'] = languages
        except Exception as e:
            print(f"Error during language detection: {e}")
            df['Language'] = ['Error'] * len(extracted_data)

    # Export the DataFrame to a CSV file
    csv_path = f"{file_name}.csv"
    df.to_csv(csv_path, index=False)

    # Send the CSV file as a downloadable attachment
    return send_file(csv_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
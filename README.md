# E-commerce Sentiment Analysis Pipeline 👟

## 📌 Project Overview
This project is an end-to-end data pipeline built for the Data Science Take-Home Test. It scrapes product reviews from Snapdeal, processes the text using NLP techniques, trains a balanced Logistic Regression model, and serves predictions via a FastAPI endpoint.

**Goal:** Classify reviews as **Positive**, **Negative**, or **Neutral** without using third-party sentiment APIs.

## 🛠️ Architecture
1.  **Scraping (`scraper.py`):** * Built with `Selenium` & `BeautifulSoup`.
    * targets specific high-traffic product pages to handle pagination and dynamic content.
2.  **Data Processing (`clean_csv.py`):** * Deduplication of raw scraped data.
    * **Class Balancing:** Uses synthetic data generation to balance the minority classes (Negative/Neutral) against the Positive majority, ensuring the model isn't biased.
3.  **Modeling (`train_model.py`):** * **Features:** TF-IDF Vectorization (1-2 ngrams).
    * **Algorithm:** Logistic Regression (Scikit-Learn).
    * **Logic:** Uses a hybrid labeling approach (Star Ratings + TextBlob) to create Ground Truth.
4.  **API (`main.py`):** * Built with `FastAPI`.
    * serves the trained model (`model.pkl`) for real-time inference.

## 🚀 How to Run Locally

### 1. Installation
Clone the repo and install dependencies:
```bash
pip install -r requirements.txt
2. Run the Pipeline (Optional)
The dataset (reviews.csv) and model (model.pkl) are already included. To retrain from scratch:

Bash
# 1. Scrape fresh data
python scraper.py

# 2. Clean & Augment data
python clean_csv.py

# 3. Train the model
python train_model.py
3. Start the API
Bash
python main.py
The API will auto-launch in your browser at: http://127.0.0.1:8000/docs.

🧪 Usage Example
Request: POST /predict

JSON
{
  "text": "The shoes are terrible and hurt my feet."
}
Response:

JSON
{
  "input_text": "The shoes are terrible and hurt my feet.",
  "sentiment": "Negative",
  "confidence_score": 0.85
}
📂 File Structure
scraper.py: Web scraping logic using Selenium.

clean_csv.py: Data cleaning and augmentation script.

train_model.py: Model training pipeline.

main.py: FastAPI application.

reviews.csv: The dataset (Real + Synthetic).

model.pkl: Serialized model file.

requirements.txt: Project dependencies.

### Results

## 📸 Screenshots Sentiment Prediction Result
![Positive Prediction](https://raw.githubusercontent.com/ChetanMestry3074/Web_Scraper/refs/heads/main/Positive.png)
![Negative Prediction](Negative.png)
![neutral Prediction](Neutral.png)

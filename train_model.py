import pandas as pd
import re
import pickle
from textblob import TextBlob
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# --- 1. LOAD DATA ---
print("🚀 Loading 'reviews.csv'...")
try:
    df = pd.read_csv("reviews.csv")
except FileNotFoundError:
    print("❌ Error: File not found. Run 'clean_csv.py' first.")
    exit()

print(f"Total Rows: {len(df)}")

# --- 2. CLEAN TEXT ---
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'^[A-Z][a-z]{2}\s\d{1,2},\s\d{4}\.\s', '', text)
    text = text.replace("verified buyer", "")
    text = re.sub(r'[^a-zA-Z\s]', '', text) 
    return text.strip()

df['Clean_Text'] = df['Review Text'].apply(clean_text)

# --- 3. GENERATE LABELS (Smart Logic) ---
print("🧪 Generating Sentiment Labels...")

def get_smart_label(row):
    rating = row['Review Rating']
    text = row['Clean_Text']
    
    # 1. Trust the Synthetic Ratings we added in clean_csv.py
    if rating == 1: return "Negative"
    if rating == 3: return "Neutral"
    
    # 2. For everything else (Rating 0 or 5), use TextBlob
    score = TextBlob(text).sentiment.polarity
    if score > 0.1: return "Positive"
    if score < -0.05: return "Negative"
    return "Neutral"

# Apply function to every row
df['Sentiment'] = df.apply(get_smart_label, axis=1)

# --- 4. TRAIN MODEL (3 Classes) ---
print("\n--- Class Balance ---")
print(df['Sentiment'].value_counts())

print("\n🧠 Training Model on Positive, Negative, AND Neutral...")

# TF-IDF
vectorizer = TfidfVectorizer(max_features=2000, stop_words='english', ngram_range=(1,2))
X = vectorizer.fit_transform(df['Clean_Text'])
y = df['Sentiment']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_train, y_train)

# --- 5. EVALUATE ---
y_pred = model.predict(X_test)
print("\n📊 Model Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred))

# --- 6. SAVE ---
print("💾 Saving model...")
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ DONE! Restart your API to test the new Neutral class.")
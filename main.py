from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import uvicorn
import re
import webbrowser
from threading import Timer

# 1. INITIALIZE APP
app = FastAPI(
    title="Sentiment Analysis API",
    description="A simple API to classify e-commerce reviews as Positive, Negative, or Neutral.",
    version="1.0"
)

# 2. LOAD MODEL ARTIFACTS
print("⏳ Loading model...")
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("❌ ERROR: 'model.pkl' or 'vectorizer.pkl' not found. Run train_model.py first.")
    model = None

# 3. DEFINE INPUT FORMAT
class ReviewInput(BaseModel):
    text: str

# 4. PREPROCESSING FUNCTION 
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text) 
    return text.strip()

# 5. API ENDPOINTS
@app.get("/")
def home():
    return {"message": "Sentiment API is running. The documentation should have opened automatically. If not, go to /docs"}

@app.post("/predict")
def predict_sentiment(review: ReviewInput):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # A. Clean Input
    cleaned_text = clean_text(review.text)
    
    # B. Vectorize
    vec_text = vectorizer.transform([cleaned_text])
    
    # C. Predict
    prediction = model.predict(vec_text)[0]
    
    # D. Confidence Score (Probability)
    probs = model.predict_proba(vec_text)[0]
    confidence = float(max(probs)) 
    
    return {
        "input_text": review.text,
        "sentiment": prediction,
        "confidence_score": round(confidence, 2)
    }

# --- AUTO-DOCS LOGIC ---
def open_browser():
    """Opens the interactive Swagger UI automatically."""
    webbrowser.open("http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    Timer(1.5, open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
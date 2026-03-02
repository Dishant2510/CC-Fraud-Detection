# CC-Fraud Detection

A lightweight credit card fraud detection web app. Upload a CSV of transactions and the app flags suspicious entries in real time using a custom-trained ML model.

##  Features
- **Upload & predict**: Drag-and-drop a `.csv` and get per-transaction fraud predictions.
- **Probabilities + confidence tiers**: Returns `confidence_score` and human-readable `confidence_level` (`high`, `medium_high`, `medium`, `low_medium`, `low`).
- **Production-ready**: Works locally and is prepped for free-tier deploys (Render/Railway) with `Procfile` and `render.yaml`.

##  Tech Stack
- **Backend**: Flask, scikit-learn, joblib
- **Data**: Pandas, NumPy
- **Model**: Custom-trained classifier saved as `fraud_detection_model.pkl`
- **Serving**: gunicorn (for production)

##  Project Structure
CCFRAUD/
├─ CCFraud/
│ ├─ templates/
│ │ └─ index.html
│ ├─ uploads/ # auto-created; user CSVs land here
│ ├─ app.py # Flask app (routes: "/", "/predict")
│ ├─ fraud_detection_model.pkl
│ ├─ Procfile
│ ├─ render.yaml
│ └─ requirements.txt


##  Quick Start (Local)

1. **Create & activate env**
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
Install deps


pip install -r requirements.txt
Run



cd CCFraud
python app.py
App starts at http://127.0.0.1:5000/.

Note: The app expects fraud_detection_model.pkl in the same folder as app.py.



 CSV Format (required columns)
Your CSV must contain:

Time, V1, V2, ..., V28, Amount
If Class exists, it will be ignored (dropped before prediction).

Only .csv uploads are allowed.

 Web UI
GET / serves templates/index.html with a simple upload form that posts to /predict.

 Deployment
Render (example)
Repo should include Procfile and render.yaml.

Procfile (web):

web: gunicorn app:app

Set Root Directory to CCFRAUD/CCFraud (where app.py lives) when creating the service, or adjust paths accordingly.

Python build command: pip install -r requirements.txt


 Notes & Best Practices
Add a .gitignore to avoid committing large CSVs and uploads:

.venv/
__pycache__/
uploads/
*.pyc
Validate CSVs server-side (current code checks columns and extension).

Consider rate limiting, auth, and server-side file size limits for production.

⚠️ Limitations / Future Work
Current scaler is fit per-upload on Amount only; consider persisting a training-time scaler for consistent scaling.

Add threshold tuning to reduce false positives based on business cost.

Expand UI to preview top risky transactions and export results.

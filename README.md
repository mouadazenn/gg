# Ventec KPI Dashboard – Streamlit HTML Wrapper

This project deploys a full HTML/CSS/JavaScript dashboard through Streamlit.

## Files

- `app.py`: Streamlit wrapper
- `index.html`: your original HTML dashboard
- `requirements.txt`: Streamlit dependency

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Push these files to GitHub.
2. Go to Streamlit Cloud.
3. Create a new app.
4. Select your repository.
5. Main file path: `app.py`
6. Deploy.

Note: the dashboard uses external CDN scripts for Chart.js and xlsx-js-style, so the deployed app needs internet access.

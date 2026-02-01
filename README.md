# Olympics-Insights

Interactive Streamlit app to explore historical Olympic data (medals, athletes, events, country-wise analysis).

Quick start

1. Create a virtual environment and activate it.

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the app locally:

```bash
streamlit run app.py
```

Notes
- The dataset `athlete_events.csv` is large and should NOT be committed to the repository in most cases. If you plan to include it, be aware of repository size limits.
- See `helper.py` and `preprocessor.py` for data handling logic.

Contributing
- Please open issues or pull requests. See `CONTRIBUTING.md` for guidelines.

License
- MIT

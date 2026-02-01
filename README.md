# Olympics-Insights

Simple Streamlit app to explore Olympic data (medals, athletes, events). This repository is structured so beginners can run the app locally and understand the code.

Prerequisites

- Python 3.10+ installed
- A copy of the datasets `athlete_events.csv` and `noc_regions.csv` placed in the project root (they are intentionally excluded from the repository to keep it small).

Quick start (Windows)

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Project layout (important files)

- `app.py`: Streamlit app entrypoint
- `helper.py`: data aggregation and helper functions used by the app
- `preprocessor.py`: small preprocessing helpers
- `requirements.txt`: runtime dependencies
- `dev-requirements.txt`: dev tools (formatting, linting, tests)

Notes for beginners

- Do not commit large CSV datasets to the repo. Place `athlete_events.csv` and `noc_regions.csv` in the project root before running the app.
- Use `venv` and `dev-requirements.txt` to run formatters and tests: `pip install -r dev-requirements.txt && black . && pytest`.

If you'd like, I can also add a small script to download the sample dataset automatically for newcomers.

# Ventec KPI Dashboard – Streamlit fixed wrapper

This version fixes the issue where some functions such as "Gérer mes KPIs" seem broken after Streamlit deployment.

The problem was not the HTML dashboard itself. It was the Streamlit iframe height.
A very large iframe height makes CSS `position: fixed` elements such as modals appear far away inside the iframe.

## Files

- `app.py`
- `index.html`
- `requirements.txt`

## Deploy

On Streamlit Cloud, use:

```text
Main file path: app.py
```

## Login code

```text
ventec2026
```

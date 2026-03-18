# RGB Gradient Wheel

A simple Flask application that generates a **mixed 3-color gradient wheel** using CSS. It stores a history of created gradients in the browser session cookie and remembers the last used colors in the form.

## Features

- Uses **POST** for form submission.
- Uses a separate file (`colors.txt`) containing **100 valid color names**.
- Validates color names on the server side (only values in `colors.txt` are accepted).
- Stores gradient history in the **session cookie** (per window / per browser profile).
- No JavaScript is used; the site is fully server-rendered.

## Running locally (Windows)

1. Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python app.py
```

4. Open http://127.0.0.1:5000 in your browser.

## Notes

- Opening a new browser profile or incognito window will create a fresh session (new cookies).
- The app persists only in the browser cookie; restarting the server will reset session history.

import os
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, session


def load_colors(path: str) -> list[str]:
    """Load the list of valid color names from a text file."""
    p = Path(path)
    if not p.exists():
        return []
    return [line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


BASE_DIR = os.path.dirname(__file__)
COLORS = load_colors(os.path.join(BASE_DIR, "colors.txt"))
COLOR_MAP = {c.lower(): c for c in COLORS}


def normalize_color(name: str | None) -> str | None:
    """Return the canonical color name if it exists in the known list."""
    if not name:
        return None
    return COLOR_MAP.get(name.strip().lower())


def make_gradient(colors: list[str]) -> str:
    """Create a CSS linear gradient string for the three given colors."""
    # Use a horizontal linear gradient with the three colors.
    return f"linear-gradient(90deg, {colors[0]}, {colors[1]}, {colors[2]})"


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    # Keep last used colors in session (remember between posts)
    last_colors = session.get("last_colors", ["", "", ""])
    history = session.get("history", [])
    gradient_css = None

    if request.method == "POST":
        c1 = request.form.get("color1", "").strip()
        c2 = request.form.get("color2", "").strip()
        c3 = request.form.get("color3", "").strip()
        chosen = []

        for label, raw in [("color1", c1), ("color2", c2), ("color3", c3)]:
            normalized = normalize_color(raw)
            if not normalized:
                error = (
                    f"Invalid value for {label}: {raw!r}. "
                    "Please choose one of the listed colors."
                )
                break
            chosen.append(normalized)

        if not error:
            last_colors = chosen
            session["last_colors"] = last_colors

            entry = {
                "colors": last_colors,
                "created": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            }
            history = [entry] + history
            history = history[:20]
            session["history"] = history
            gradient_css = make_gradient(last_colors)

    else:
        if last_colors and len(last_colors) == 3:
            gradient_css = make_gradient(last_colors)

    return render_template(
        "index.html",
        colors=COLORS,
        last_colors=last_colors,
        gradient_css=gradient_css,
        history=history,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)

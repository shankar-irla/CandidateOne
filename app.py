"""
CandidateOne Web Application

Flask application for CandidateOne ETL Pipeline.

Features
--------
• Upload Resume
• Upload ATS JSON
• Upload GitHub JSON
• Upload LinkedIn JSON
• Upload Recruiter CSV
• Execute Pipeline
• Display Results
• Download Outputs

Author:
    Shankar Irla
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for
)

from werkzeug.utils import secure_filename

from pipeline import CandidatePipeline
from utils.logger import get_logger


# ==========================================================
# Flask App
# ==========================================================

app = Flask(__name__)

app.secret_key = "candidateone-secret-key"

logger = get_logger(__name__)


# ==========================================================
# Directories
# ==========================================================

BASE_DIR = Path(__file__).parent

INPUT_DIR = BASE_DIR / "sample_input"

OUTPUT_DIR = BASE_DIR / "output"

INPUT_DIR.mkdir(
    exist_ok=True
)

OUTPUT_DIR.mkdir(
    exist_ok=True
)


# ==========================================================
# Upload Configuration
# ==========================================================

UPLOAD_FIELDS = {

    "resume": "resume.pdf",

    "ats": "ats.json",

    "linkedin": "linkedin.json",

    "github": "github.json",

    "csv": "recruiter.csv"

}


# ==========================================================
# Allowed Extensions
# ==========================================================

ALLOWED_EXTENSIONS = {

    "resume": {"pdf"},

    "ats": {"json"},

    "linkedin": {"json"},

    "github": {"json"},

    "csv": {"csv"}

}


# ==========================================================
# Helper Functions
# ==========================================================

def allowed_file(
    filename: str,
    category: str
) -> bool:
    """
    Validates uploaded file extension.
    """

    if "." not in filename:

        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in ALLOWED_EXTENSIONS.get(
        category,
        set()
    )


def save_upload(
    uploaded_file,
    category: str
) -> bool:
    """
    Saves uploaded file into sample_input directory.
    """

    if uploaded_file is None:

        return False

    if uploaded_file.filename == "":

        return False

    if not allowed_file(
        uploaded_file.filename,
        category
    ):

        return False

    filename = secure_filename(

        UPLOAD_FIELDS[category]

    )

    destination = INPUT_DIR / filename

    uploaded_file.save(destination)

    logger.info(

        "%s uploaded.",

        filename

    )

    return True


def load_json(
    filename: str
):
    """
    Reads a JSON file.

    Returns None if file is unavailable.
    """

    path = OUTPUT_DIR / filename

    if not path.exists():

        return None

    with open(

        path,

        "r",

        encoding="utf-8"

    ) as file:

        return json.load(file)


# ==========================================================
# Home Page
# ==========================================================

@app.route(
    "/",
    methods=["GET"]
)
def index():
    """
    Landing page.
    """

    return render_template(

        "index.html"

    )


# ==========================================================
# About Page
# ==========================================================

@app.route(
    "/about",
    methods=["GET"]
)
def about():
    """
    Simple project information.
    """

    return render_template(

        "about.html"

    )
# ==========================================================
# Process Candidate
# ==========================================================

@app.route(
    "/process",
    methods=["POST"]
)
def process():
    """
    Uploads input files and executes the complete
    CandidateOne ETL Pipeline.
    """

    try:

        # --------------------------------------------------
        # Save Uploaded Files
        # --------------------------------------------------

        uploaded = {

            "resume": request.files.get("resume"),

            "ats": request.files.get("ats"),

            "linkedin": request.files.get("linkedin"),

            "github": request.files.get("github"),

            "csv": request.files.get("csv")

        }

        uploaded_count = 0

        for category, file in uploaded.items():

            if file and file.filename:

                if save_upload(file, category):

                    uploaded_count += 1

                else:

                    flash(

                        f"Invalid {category} file.",

                        "warning"

                    )

        logger.info(

            "%d file(s) uploaded.",

            uploaded_count

        )

        # --------------------------------------------------
        # Execute Pipeline
        # --------------------------------------------------

        pipeline = CandidatePipeline(

            input_directory=str(INPUT_DIR),

            output_directory=str(OUTPUT_DIR),

            config_file="config/default_config.json"

        )

        result = pipeline.run()

        logger.info(

            "Pipeline executed successfully."

        )

        # --------------------------------------------------
        # Read Generated Output
        # --------------------------------------------------

        canonical = load_json(

            "canonical_profile.json"

        )

        projected = load_json(

            "projected_profile.json"

        )

        statistics = result.get(

            "statistics",

            {}

        )

        # --------------------------------------------------
        # Render Result Page
        # --------------------------------------------------

        return render_template(

            "result.html",

            canonical=canonical,

            projected=projected,

            statistics=statistics,

            files=result.get(

                "files",

                {}

            )

        )

    except Exception as exc:

        logger.exception(

            "Pipeline execution failed."

        )

        flash(

            str(exc),

            "danger"

        )

        return redirect(

            url_for(

                "index"

            )

        )


# ==========================================================
# View Canonical JSON
# ==========================================================

@app.route(
    "/canonical",
    methods=["GET"]
)
def canonical():
    """
    Displays canonical profile.
    """

    profile = load_json(

        "canonical_profile.json"

    )

    if profile is None:

        flash(

            "Canonical profile not found.",

            "warning"

        )

        return redirect(

            url_for(

                "index"

            )

        )

    return render_template(

        "result.html",

        canonical=profile,

        projected=None,

        statistics=None,

        files=None

    )


# ==========================================================
# View Projected JSON
# ==========================================================

@app.route(
    "/projected",
    methods=["GET"]
)
def projected():
    """
    Displays projected profile.
    """

    profile = load_json(

        "projected_profile.json"

    )

    if profile is None:

        flash(

            "Projected profile not found.",

            "warning"

        )

        return redirect(

            url_for(

                "index"

            )

        )

    return render_template(

        "result.html",

        canonical=None,

        projected=profile,

        statistics=None,

        files=None

    )
# ==========================================================
# Download Canonical Profile
# ==========================================================

@app.route(
    "/download/canonical",
    methods=["GET"]
)
def download_canonical():
    """
    Downloads canonical profile JSON.
    """

    file_path = OUTPUT_DIR / "canonical_profile.json"

    if not file_path.exists():

        flash(
            "Canonical profile not found.",
            "warning"
        )

        return redirect(
            url_for("index")
        )

    return send_file(
        file_path,
        as_attachment=True,
        download_name="canonical_profile.json",
        mimetype="application/json"
    )


# ==========================================================
# Download Projected Profile
# ==========================================================

@app.route(
    "/download/projected",
    methods=["GET"]
)
def download_projected():
    """
    Downloads projected profile JSON.
    """

    file_path = OUTPUT_DIR / "projected_profile.json"

    if not file_path.exists():

        flash(
            "Projected profile not found.",
            "warning"
        )

        return redirect(
            url_for("index")
        )

    return send_file(
        file_path,
        as_attachment=True,
        download_name="projected_profile.json",
        mimetype="application/json"
    )


# ==========================================================
# Health Check
# ==========================================================

@app.route(
    "/health",
    methods=["GET"]
)
def health():
    """
    Returns application health.
    """

    pipeline = CandidatePipeline()

    return {

        "application": "CandidateOne",

        "status": "Running",

        "pipeline": pipeline.health(),

        "available_sources": pipeline.available_sources()

    }


# ==========================================================
# Error Handlers
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):
    """
    Handles 404 errors.
    """

    logger.warning(
        "404 - Page Not Found."
    )

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    Handles internal server errors.
    """

    logger.exception(
        "500 - Internal Server Error."
    )

    return render_template(
        "500.html"
    ), 500


# ==========================================================
# Application Entry Point
# ==========================================================

def main():
    """
    Starts the Flask application.
    """

    logger.info("=" * 70)
    logger.info("CandidateOne Web Application Started")
    logger.info("=" * 70)

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )


if __name__ == "__main__":

    main()
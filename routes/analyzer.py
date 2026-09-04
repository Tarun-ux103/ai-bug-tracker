from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from services.ai_service import analyze_code

from models import db
from models.bug import Bug
from models.analysis_report import AnalysisReport


analyzer_bp = Blueprint(
    "analyzer",
    __name__
)


@analyzer_bp.route(
    "/analyze",
    methods=["GET", "POST"]
)
@login_required
def analyze():

    if request.method == "POST":

        code = request.form.get(
            "code",
            ""
        ).strip()

        language = request.form.get(
            "language",
            ""
        ).strip()


        if not code:

            flash(
                "Please enter some code to analyze.",
                "error"
            )

            return redirect(
                url_for("analyzer.analyze")
            )


        # Analyze the submitted code using AI
        analysis = analyze_code(
            code,
            language
        )


        # Stop if the AI analysis failed
        if analysis.get("error"):

            flash(
                "Unable to analyze the code.",
                "error"
            )

            return render_template(
                "analysis_result.html",
                analysis=analysis,
                language=language,
                code=code,
                analysis_report=None
            )


        # Create one analysis report automatically
        report = AnalysisReport(

            title="Code Analysis",

            language=language,

            source_code=code,

            summary=analysis.get(
                "summary",
                ""
            ),

            user_id=current_user.id
        )


        db.session.add(report)

        db.session.commit()


        # Display the results and keep the report ID
        return render_template(
            "analysis_result.html",

            analysis=analysis,

            language=language,

            code=code,

            analysis_report=report
        )


    return render_template(
        "analyzer.html"
    )


@analyzer_bp.route(
    "/save-ai-bug",
    methods=["POST"]
)
@login_required
def save_ai_bug():

    title = request.form.get(
        "title"
    )

    issue_type = request.form.get(
        "issue_type"
    )

    severity = request.form.get(
        "severity"
    )

    description = request.form.get(
        "description"
    )

    suggested_fix = request.form.get(
        "suggested_fix"
    )

    analysis_report_id = request.form.get(
        "analysis_report_id"
    )


    if not title:

        flash(
            "Unable to save the AI issue.",
            "error"
        )

        return redirect(
            url_for("analyzer.analyze")
        )


    full_description = f"""
AI Detected Issue

Issue Type:
{issue_type}

Description:
{description}

Suggested Fix:
{suggested_fix}
"""


    bug = Bug(

        title=title,

        description=full_description,

        priority=severity,

        user_id=current_user.id,

        analysis_report_id=analysis_report_id
    )


    db.session.add(bug)

    db.session.commit()


    flash(
        "AI-detected issue saved successfully!",
        "success"
    )


    return redirect(
        url_for("main.dashboard")
    )
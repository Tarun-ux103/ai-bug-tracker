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
            "code"
        )

        language = request.form.get(
            "language"
        )


        if not code:

            flash(
                "Please enter some code to analyze.",
                "error"
            )

            return redirect(
                url_for(
                    "analyzer.analyze"
                )
            )


        analysis = analyze_code(
            code,
            language
        )


        if analysis.get("error"):

            return render_template(
                "analysis_result.html",
                analysis=analysis,
                report=None,
                saved_bug_titles=[]
            )


        report = AnalysisReport(

            title="Code Analysis",

            language=language,

            source_code=code,

            summary=analysis.get(
                "summary",
                ""
            ),

            issues=analysis.get(
                "issues",
                []
            ),

            user_id=current_user.id
        )


        try:

            db.session.add(
                report
            )

            db.session.commit()


        except Exception:

            db.session.rollback()

            flash(
                "Unable to save the analysis report.",
                "error"
            )

            return redirect(
                url_for(
                    "analyzer.analyze"
                )
            )


        return redirect(
            url_for(
                "analyzer.analysis_results",
                report_id=report.id
            )
        )


    return render_template(
        "analyzer.html"
    )


@analyzer_bp.route(
    "/analysis-results/<int:report_id>"
)
@login_required
def analysis_results(report_id):

    report = db.session.get(
        AnalysisReport,
        report_id
    )


    if not report:

        flash(
            "Analysis report not found.",
            "error"
        )

        return redirect(
            url_for(
                "analyzer.analyze"
            )
        )


    if report.user_id != current_user.id:

        flash(
            "You are not authorized to view this report.",
            "error"
        )

        return redirect(
            url_for(
                "main.dashboard"
            )
        )


    analysis = {

        "summary": report.summary,

        "issues": report.issues or []

    }


    saved_bugs = Bug.query.filter_by(

        analysis_report_id=report.id,

        user_id=current_user.id

    ).all()


    saved_bug_titles = [

        bug.title

        for bug in saved_bugs

    ]


    return render_template(

        "analysis_result.html",

        analysis=analysis,

        report=report,

        saved_bug_titles=saved_bug_titles

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


    if not title or not analysis_report_id:

        flash(
            "Unable to save the AI issue.",
            "error"
        )

        return redirect(
            url_for(
                "analyzer.analyze"
            )
        )


    try:

        analysis_report_id = int(
            analysis_report_id
        )

    except ValueError:

        flash(
            "Invalid analysis report.",
            "error"
        )

        return redirect(
            url_for(
                "analyzer.analyze"
            )
        )


    report = db.session.get(

        AnalysisReport,

        analysis_report_id

    )


    if not report:

        flash(
            "Analysis report not found.",
            "error"
        )

        return redirect(
            url_for(
                "analyzer.analyze"
            )
        )


    if report.user_id != current_user.id:

        flash(
            "You are not authorized to modify this report.",
            "error"
        )

        return redirect(
            url_for(
                "main.dashboard"
            )
        )


    existing_bug = Bug.query.filter_by(

        title=title,

        analysis_report_id=analysis_report_id,

        user_id=current_user.id

    ).first()


    if existing_bug:

        flash(
            "This AI issue has already been saved as a bug.",
            "info"
        )

        return redirect(
            url_for(

                "analyzer.analysis_results",

                report_id=analysis_report_id

            )
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


    try:

        db.session.add(
            bug
        )

        db.session.commit()


        flash(
            "AI-detected issue saved successfully as a bug!",
            "success"
        )


    except Exception:

        db.session.rollback()


        flash(
            "Unable to save the AI issue.",
            "error"
        )


    return redirect(
        url_for(

            "analyzer.analysis_results",

            report_id=analysis_report_id

        )
    )
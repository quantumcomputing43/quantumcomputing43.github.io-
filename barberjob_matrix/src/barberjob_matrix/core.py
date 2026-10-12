"""Deterministic CV, role-fit, and application-draft helpers. No email sending."""
from __future__ import annotations
import re
from typing import Any

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_profile(profile: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not str(profile.get("full_name", "")).strip():
        errors.append("full_name is required")
    years = profile.get("years_experience")
    if years is not None and (not isinstance(years, int) or years < 0 or years > 80):
        errors.append("years_experience must be 0..80 or null")
    if not isinstance(profile.get("skills", []), list):
        errors.append("skills must be a list")
    contact = profile.get("contact", {})
    if not isinstance(contact, dict):
        errors.append("contact must be an object")
    elif contact.get("email") and not EMAIL_RE.match(str(contact["email"]).strip()):
        errors.append("contact.email is invalid")
    return errors


def render_cv_markdown(profile: dict[str, Any]) -> str:
    errors = validate_profile(profile)
    if errors:
        raise ValueError("; ".join(errors))

    def show(value: Any, fallback: str = "[To be completed]") -> str:
        return str(value).strip() if value not in (None, "", []) else fallback

    lines = [
        f"# {show(profile.get('full_name'))}",
        f"**{show(profile.get('professional_title'), 'Experienced Barber')}**",
        "",
        f"Location: {show(profile.get('base_location'))}",
        f"Email: {show(profile.get('contact', {}).get('email'))}",
        f"Phone: {show(profile.get('contact', {}).get('phone'))}",
        "",
        "## Professional Profile",
        show(profile.get("professional_summary")),
        "",
        "## Experience",
    ]
    history = profile.get("employment_history") or []
    if history:
        for job in history:
            lines.extend([
                f"### {show(job.get('role'))} — {show(job.get('employer'))}",
                f"{show(job.get('start_date'))} – {show(job.get('end_date'), 'Present / confirm')}",
                show(job.get("description")),
                "",
            ])
    else:
        lines.append("[Add employers, locations, dates, and verifiable responsibilities.]")
    lines.extend(["", "## Barbering Skills"])
    lines.extend([f"- {x}" for x in (profile.get("skills") or [])] or ["- [Add demonstrable skills]"])
    lines.extend(["", "## Languages"])
    lines.extend([f"- {x}" for x in (profile.get("languages") or [])] or ["- [Language and proficiency]"])
    lines.extend(["", "## Certifications"])
    lines.extend([f"- {x}" for x in (profile.get("certifications") or [])] or ["- [Verified certificates only]"])
    lines.extend(["", "## Portfolio"])
    lines.extend([f"- {x}" for x in (profile.get("portfolio_links") or [])] or ["- [Optional portfolio link]"])
    lines.extend(["", "## Availability and Work Authorization", show(profile.get("availability")), show(profile.get("work_authorization"), "Not confirmed")])
    return "\n".join(lines).strip() + "\n"


def score_role(profile: dict[str, Any], role: dict[str, Any]) -> dict[str, Any]:
    """Return an explainable score, not a probability of being hired."""
    skills = {str(x).strip().casefold() for x in profile.get("skills", [])}
    required = {str(x).strip().casefold() for x in role.get("required_skills", [])}
    matched = sorted(skills & required)
    skill_score = 60 * len(matched) / max(1, len(required))
    targets = {str(x).casefold() for x in profile.get("target_regions", [])}
    region = str(role.get("region", "")).casefold()
    region_score = 20 if region and any(x in region or region in x for x in targets) else 0
    url_score = 20 if str(role.get("official_job_url", "")).startswith("https://") else 0
    return {
        "score": round(min(100, skill_score + region_score + url_score), 1),
        "matched_skills": matched,
        "unmatched_required_skills": sorted(required - skills),
        "interpretation": "rule-based fit score, not hiring probability",
    }


def draft_application_email(profile: dict[str, Any], company: dict[str, Any]) -> str:
    """Prepare a personalized draft for human review; never send email."""
    errors = validate_profile(profile)
    if errors:
        raise ValueError("; ".join(errors))
    company_name = str(company.get("company_name", "")).strip()
    role = str(company.get("job_title", "Barber")).strip()
    if not company_name:
        raise ValueError("company_name is required")
    name = str(profile.get("full_name", "")).strip()
    years = profile.get("years_experience")
    experience = (
        f"I have {years} years of barbering experience."
        if isinstance(years, int)
        else "I would be glad to share my experience and portfolio."
    )
    skills = ", ".join(profile.get("skills", [])[:5]) or "professional barbering"
    return (
        f"Subject: Application for {role} — {name}\n\n"
        f"Dear {company_name} Recruitment Team,\n\n"
        f"I am contacting you to ask whether you are considering candidates for a {role} position. "
        f"{experience} My relevant skills include {skills}.\n\n"
        "I can provide my CV and portfolio and would welcome the opportunity to discuss the role "
        "and any work-authorization requirements.\n\n"
        f"Thank you for your time.\nKind regards,\n{name}"
    )


def is_contactable(company: dict[str, Any]) -> tuple[bool, str]:
    """Fail closed; eligibility still requires human review before contact."""
    if company.get("do_not_contact") is True:
        return False, "blocked: do_not_contact"
    if not str(company.get("company_name", "")).strip():
        return False, "blocked: missing company_name"
    if not str(company.get("contact_source", "")).strip():
        return False, "blocked: missing contact_source"
    email = str(company.get("public_contact_email", "")).strip()
    if email and not EMAIL_RE.match(email):
        return False, "blocked: invalid email format"
    if not email and not str(company.get("official_job_url", "")).startswith("https://"):
        return False, "blocked: no verified public email or official job URL"
    return True, "eligible for human review; not authorization to send"

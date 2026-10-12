from barberjob_matrix.core import draft_application_email, is_contactable, render_cv_markdown, score_role, validate_profile

PROFILE = {
    "full_name": "Test Barber", "professional_title": "Experienced Barber",
    "years_experience": 12, "base_location": "Morocco",
    "skills": ["skin fades", "beard grooming", "scissor cuts"],
    "languages": ["Arabic — native"], "employment_history": [],
    "certifications": [], "portfolio_links": [], "target_regions": ["Europe", "Gulf"],
    "contact": {"email": "test@example.com", "phone": ""},
}


def test_profile_validation_passes():
    assert validate_profile(PROFILE) == []


def test_profile_rejects_invalid_email():
    profile = {**PROFILE, "contact": {"email": "not-an-email"}}
    assert validate_profile(profile)


def test_cv_does_not_invent_work_history():
    cv = render_cv_markdown(PROFILE)
    assert "Test Barber" in cv
    assert "Add employers" in cv


def test_email_is_draft_and_personalized():
    draft = draft_application_email(PROFILE, {"company_name": "Example Salon", "job_title": "Senior Barber"})
    assert "Example Salon" in draft
    assert "12 years of barbering experience" in draft


def test_role_score_is_explainable():
    result = score_role(PROFILE, {"region": "Europe", "required_skills": ["skin fades", "hair coloring"], "official_job_url": "https://example.com/jobs/1"})
    assert result["score"] == 70.0
    assert result["matched_skills"] == ["skin fades"]
    assert result["unmatched_required_skills"] == ["hair coloring"]


def test_opt_out_is_hard_block():
    ok, reason = is_contactable({"company_name": "Example", "contact_source": "https://example.com", "public_contact_email": "jobs@example.com", "do_not_contact": True})
    assert not ok and "blocked" in reason


def test_contact_source_is_required():
    ok, reason = is_contactable({"company_name": "Example", "public_contact_email": "jobs@example.com"})
    assert not ok and "contact_source" in reason

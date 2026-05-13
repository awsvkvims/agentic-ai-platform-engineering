from src.tools.ci_cd_tools import review_cicd_pipeline


def test_cicd_detects_all_three_risks():
    pipeline = """
stages:
  - name: build
    run: docker build .
  - name: deploy
    run: kubectl apply -f deployment.yaml
"""
    result = review_cicd_pipeline(pipeline)
    assert "Quality risk: no test stage detected" in result
    assert "Security risk: no security scan stage detected" in result
    assert "Reliability risk: deploy stage exists without a rollback step" in result


def test_cicd_clean_pipeline_reports_no_issues():
    pipeline = """
stages:
  - name: test
    run: pytest
  - name: security-scan
    run: trivy scan .
  - name: deploy
    run: kubectl apply -f deployment.yaml
  - name: rollback
    run: kubectl rollout undo deployment/app
"""
    result = review_cicd_pipeline(pipeline)
    assert result == "No obvious CI/CD pipeline risks detected."


def test_cicd_empty_string_reports_no_test_and_no_security():
    result = review_cicd_pipeline("")
    assert "Quality risk: no test stage detected" in result
    assert "Security risk: no security scan stage detected" in result
    assert "rollback" not in result.lower()

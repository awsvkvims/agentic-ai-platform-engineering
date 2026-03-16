from src.ai.tool_definition import Tool


def review_cicd_pipeline(pipeline_text: str) -> str:
    findings = []

    text = pipeline_text.lower()
    
    test_indicators = [
    "name: test",
    "run: pytest",
    "run: npm test",
    "run: mvn test",
    "run: go test",
]

    if not any(indicator in text for indicator in test_indicators):
        findings.append("Quality risk: no test stage detected")

    if "security" not in text and "scan" not in text:
        findings.append("Security risk: no security scan stage detected")

    if "deploy" in text and "rollback" not in text:
        findings.append("Reliability risk: deploy stage exists without a rollback step")

    if not findings:
        return "No obvious CI/CD pipeline risks detected."

    result = "CI/CD pipeline review detected the following issues:\n\n"

    for item in findings:
        result += f"- {item}\n"

    return result


cicd_pipeline_reviewer_tool = Tool(
    name="cicd_pipeline_reviewer",
    description="Use this when the user asks to review a CI/CD pipeline, analyze pipeline quality, or identify delivery risks in pipeline configuration.",
    func=review_cicd_pipeline,
)
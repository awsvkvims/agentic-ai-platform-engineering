from src.ai.tool_definition import Tool


def summarize_pr_diff(diff_text: str) -> str:
    """Identify infrastructure resource changes and security risks in a Terraform PR diff."""
    text = diff_text.lower()

    findings = []
    changes = []

    if "aws_security_group" in text:
        changes.append("Security group configuration changed")

    if "aws_s3_bucket" in text:
        changes.append("S3 bucket configuration changed")

    if "aws_db_instance" in text:
        changes.append("Database configuration changed")

    if "0.0.0.0/0" in text:
        findings.append("Security risk: open access to 0.0.0.0/0 detected")

    if "public = true" in text:
        findings.append("Security risk: resource marked as public")

    if "versioning" not in text and "aws_s3_bucket" in text:
        findings.append("Best practice: S3 bucket versioning not enabled")

    if "storage_encrypted" not in text and "aws_db_instance" in text:
        findings.append("Security risk: database encryption not enabled")

    if not changes:
        changes.append("No major infrastructure changes detected")

    result = "PR infrastructure summary:\n\n"

    result += "Changes detected:\n"
    for c in changes:
        result += f"- {c}\n"

    result += "\nRisks and observations:\n"
    if findings:
        for f in findings:
            result += f"- {f}\n"
    else:
        result += "- No obvious risks detected\n"

    return result


pr_infra_summarizer_tool = Tool(
    name="pr_infra_summarizer",
    description="Use this when the user asks to summarize infrastructure changes in a pull request or analyze a Terraform or infrastructure diff.",
    func=summarize_pr_diff,
)

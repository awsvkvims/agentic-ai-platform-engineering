from src.ai.tool_definition import Tool

def analyze_terraform(tf_text: str) -> str:
    findings = []

    if "0.0.0.0/0" in tf_text:
        findings.append("Security risk: security group allows access from 0.0.0.0/0")

    if "public = true" in tf_text:
        findings.append("Security risk: resource configured as public")

    if "aws_s3_bucket" in tf_text and "versioning" not in tf_text:
        findings.append("Best practice: S3 bucket versioning not configured")

    if "aws_db_instance" in tf_text and "storage_encrypted" not in tf_text:
        findings.append("Security risk: database storage encryption not enabled")

    if not findings:
        return "No obvious Terraform risks detected."

    result = "Terraform analysis detected the following issues:\n\n"

    for item in findings:
        result += f"- {item}\n"

    return result


terraform_analyzer_tool = Tool(
    name="terraform_analyzer",
    description="Use this when the user asks to analyze Terraform, review Terraform configuration, or identify infrastructure risks in Terraform code.",
    func=analyze_terraform,
)

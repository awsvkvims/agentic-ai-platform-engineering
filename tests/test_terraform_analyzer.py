from src.tools.terraform_analyzer import analyze_terraform


def test_terraform_detects_multiple_risks():
    tf = """
resource "aws_security_group" "web" {
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_s3_bucket" "data" {
  bucket = "my-bucket"
}
resource "aws_db_instance" "main" {
  instance_class = "db.t3.micro"
}
"""
    result = analyze_terraform(tf)
    assert "Security risk: security group allows access from 0.0.0.0/0" in result
    assert "Best practice: S3 bucket versioning not configured" in result
    assert "Security risk: database storage encryption not enabled" in result


def test_terraform_encrypted_db_has_no_encryption_finding():
    tf = """
resource "aws_db_instance" "main" {
  instance_class   = "db.t3.micro"
  storage_encrypted = true
}
"""
    result = analyze_terraform(tf)
    assert "database storage encryption not enabled" not in result


def test_terraform_empty_string_reports_no_risks():
    result = analyze_terraform("")
    assert result == "No obvious Terraform risks detected."

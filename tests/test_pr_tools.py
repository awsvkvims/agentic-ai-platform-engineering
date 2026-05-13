from src.tools.pr_tools import summarize_pr_diff


def test_pr_diff_detects_changes_and_security_risks():
    diff = """
+resource "aws_security_group" "web" {
+  ingress {
+    cidr_blocks = ["0.0.0.0/0"]
+  }
+}
+resource "aws_s3_bucket" "data" {
+  bucket = "my-bucket"
+}
"""
    result = summarize_pr_diff(diff)
    assert "Security group configuration changed" in result
    assert "S3 bucket configuration changed" in result
    assert "Security risk: open access to 0.0.0.0/0 detected" in result
    assert "Best practice: S3 bucket versioning not enabled" in result


def test_pr_diff_s3_with_versioning_has_no_versioning_risk():
    diff = """
+resource "aws_s3_bucket" "data" {
+  bucket = "my-bucket"
+  versioning {
+    enabled = true
+  }
+}
"""
    result = summarize_pr_diff(diff)
    assert "S3 bucket configuration changed" in result
    assert "versioning not enabled" not in result.lower()


def test_pr_diff_empty_string_reports_no_changes_and_no_risks():
    result = summarize_pr_diff("")
    assert "No major infrastructure changes detected" in result
    assert "No obvious risks detected" in result

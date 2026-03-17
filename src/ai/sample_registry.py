TOOL_SAMPLE_PATHS = {
    "backlog_analysis": "samples/backlog/sample_backlog.txt",
    "terraform_analyzer": "samples/terraform/sample_terraform.tf",
    "cicd_pipeline_reviewer": "samples/pipeline/sample_pipeline.yml",
    "pr_infra_summarizer": "samples/pr/sample_pr.diff",
}

CLI_SAMPLE_COMMANDS = {
    "analyze backlog": "samples/backlog/sample_backlog.txt",
    "analyze terraform": "samples/terraform/sample_terraform.tf",
    "analyze pipeline": "samples/pipeline/sample_pipeline.yml",
    "analyze pr": "samples/pr/sample_pr.diff",
}

def read_sample_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()
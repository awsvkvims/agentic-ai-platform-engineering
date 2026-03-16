resource "aws_security_group" "web" {
  name = "web-sg"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "app_data" {
  bucket = "my-app-data-bucket"
}

resource "aws_db_instance" "app_db" {
  identifier = "app-db"
  engine     = "postgres"
}

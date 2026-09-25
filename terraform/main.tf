terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ---------------------------------------------------------
# ECR Repository
# ---------------------------------------------------------

resource "aws_ecr_repository" "aegisops" {
  name                 = var.project_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Project     = "AegisOps AI"
    Environment = "development"
    ManagedBy   = "Terraform"
  }
}

# ---------------------------------------------------------
# ECS Cluster
# ---------------------------------------------------------

resource "aws_ecs_cluster" "aegisops" {
  name = "${var.project_name}-cluster"

  tags = {
    Project     = "AegisOps AI"
    Environment = "development"
    ManagedBy   = "Terraform"
  }
}

# ---------------------------------------------------------
# ECS Task Execution Role
# ---------------------------------------------------------

resource "aws_iam_role" "ecs_task_execution" {
  name = "${var.project_name}-ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Project     = "AegisOps AI"
    Environment = "development"
    ManagedBy   = "Terraform"
  }
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ---------------------------------------------------------
# Security Group
# ---------------------------------------------------------

resource "aws_security_group" "aegisops" {
  name        = "${var.project_name}-sg"
  description = "Security group for AegisOps AI ECS service"
  vpc_id      = "vpc-061519d6349b3723c"

  ingress {
    description = "AegisOps AI API"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["127.0.0.1/32"]
  }

  egress {
    description = "Allow outbound internet traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Project     = "AegisOps AI"
    Environment = "development"
    ManagedBy   = "Terraform"
  }
}

# ---------------------------------------------------------
# CloudWatch Logs
# ---------------------------------------------------------

resource "aws_cloudwatch_log_group" "aegisops" {
  name              = "/ecs/${var.project_name}"
  retention_in_days = 7

  tags = {
    Project     = "AegisOps AI"
    Environment = "development"
    ManagedBy   = "Terraform"
  }
}

# ---------------------------------------------------------
# ECS Task Definition
# ---------------------------------------------------------

resource "aws_ecs_task_definition" "aegisops" {
  family                   = var.project_name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]

  cpu    = "256"
  memory = "512"

  execution_role_arn = aws_iam_role.ecs_task_execution.arn

  container_definitions = jsonencode([
    {
      name      = var.project_name
      image     = "${aws_ecr_repository.aegisops.repository_url}:1.0"
      essential = true

      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        }
      ]

      environment = [
        {
          name  = "PORT"
          value = "8000"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"

        options = {
          awslogs-group         = aws_cloudwatch_log_group.aegisops.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])

  tags = {
    Project     = "AegisOps AI"
    Environment = "development"
    ManagedBy   = "Terraform"
  }
}

# ---------------------------------------------------------
# ECS Service
# ---------------------------------------------------------

resource "aws_ecs_service" "aegisops" {
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.aegisops.id
  task_definition = aws_ecs_task_definition.aegisops.arn

  desired_count = 1

  launch_type = "FARGATE"

  network_configuration {
    subnets = [
      "subnet-0311300cae053aad4",
      "subnet-0b15c7382990e2867",
      "subnet-0d357e3874c2dd37c"
    ]

    security_groups = [
      aws_security_group.aegisops.id
    ]

    assign_public_ip = true
  }

  tags = {
    Project     = "AegisOps AI"
    Environment = "development"
    ManagedBy   = "Terraform"
  }

  depends_on = [
    aws_iam_role_policy_attachment.ecs_task_execution
  ]
}
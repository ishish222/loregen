
resource "aws_cloudwatch_log_group" "loregen_front_dashboard-logs" {
  name = "/ecs/loregen_front_dashboard"
  retention_in_days = 30

  tags = {
    Name = "/ecs/loregen_front_dashboard"
  }
}

resource "aws_ecs_task_definition" "loregen_front_dashboard-task" {
  family                   = "loregen_front_dashboard"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_execution_role_for_loregen_front_dashboard.arn
  task_role_arn            = aws_iam_role.ecs_task_role_for_loregen_front_dashboard.arn

  container_definitions = jsonencode([{
    name  = "loregen_front_dashboard-container",
    image = var.dashboard_image,
    portMappings = [{
      containerPort = 80
      hostPort      = 80
    }],
    secrets = [{
      name      = "OPENAI_API_KEY"
      valueFrom = data.aws_secretsmanager_secret.openai_api_key.arn
    },
    {
      name      = "OPENROUTER_API_KEY"
      valueFrom = data.aws_secretsmanager_secret.openrouter_api_key.arn
    },
    # {
    #   name      = "ANTHROPIC_API_KEY"
    #   valueFrom = data.aws_secretsmanager_secret.anthropic_api_key.arn
    # },
    # {
    #   name      = "MISTRAL_API_KEY"
    #   valueFrom = data.aws_secretsmanager_secret.mistral_api_key.arn
    # },
    # {
    #   name      = "GOOGLE_API_KEY"
    #   valueFrom = data.aws_secretsmanager_secret.google_api_key.arn
    # },
    # {
    #   name      = "GROQ_API_KEY"
    #   valueFrom = data.aws_secretsmanager_secret.groq_api_key.arn
    # },
    # {
    #   name      = "DEEPSEEK_API_KEY"
    #   valueFrom = data.aws_secretsmanager_secret.deepseek_api_key.arn
    # },
    # {
    #   name      = "XAI_API_KEY"
    #   valueFrom = data.aws_secretsmanager_secret.xai_api_key.arn
    # },
    # {
    #   name      = "LANGCHAIN_API_KEY"
    #   valueFrom = data.aws_secretsmanager_secret.langsmith_api_key.arn
    # },
    ],
    environment = [{
      name  = "SCRIPT_NAME"
      value = var.script_name
    }, 
    {
      name  = "ENVIRONMENT"
      value = var.environment
    }, 
    {
      name  = "APP_PORT"
      value = var.app_port
    }, 
    {
      name  = "APP_HOST"
      value = var.app_host
    }, 
    {
      name  = "AWS_REGION"
      value = var.aws_region
    },
    {
      name  = "AWS_CACHE_BUCKET"
      value = var.cache_bucket
    },
    {
      name  = "AWS_CACHE_PREFIX"
      value = var.cache_prefix
    },
    {
      name  = "TOKEN_COUNTER_TABLE"
      value = var.dynamodb_table_name
    },
    {
      name  = "TOKEN_COUNTER_DEFAULT_ITEM_ID"
      value = var.dynamodb_default_item
    },
    {
      name = "COGNITO_DOMAIN"
      value = var.cognito_domain
    },
    {
      name = "COGNITO_DOMAIN_CLIENT_ID"
      value = var.cognito_domain_client_id
    },
    {
      name = "COGNITO_DOMAIN_REDIRECT_URI_LOGIN"
      value = var.cognito_domain_redirect_uri_login
    },
    {
      name = "COGNITO_DOMAIN_REDIRECT_URI_LOGOUT"
      value = var.cognito_domain_redirect_uri_logout
    },
    {
      name = "COGNITO_DOMAIN_USER_POOL_ID"
      value = var.cognito_domain_user_pool_id
    },
    {
      name = "COGNITO_DOMAIN_REGION"
      value = var.cognito_domain_region
    },
    # {
    #   name = "DB_HOST"
    #   value = aws_rds_cluster.loregen_front_aurora_cluster.endpoint
    # },
    {
      name = "DB_PORT"
      value = var.db_port
    },
    {
      name = "DB_NAME"
      value = var.db_name
    },
    {
      name = "DB_USERNAME"
      value = var.db_username
    },
    # {
    #   name = "DB_SECRET_ARN"
    #   value = "arn:aws:secretsmanager:${var.aws_region}:${var.aws_account}:secret:/loregen_front_db/password"
    # },
    ],
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = aws_cloudwatch_log_group.loregen_front_dashboard-logs.name
        awslogs-region        = "eu-central-1"
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}

resource "aws_ecs_cluster" "loregen_front_dashboard-cluster" {
  name = "loregen_front_dashboard"
}

resource "aws_ecs_service" "loregen_front_dashboard-service" {
  name            = "loregen_front_dashboard_service"
  cluster         = aws_ecs_cluster.loregen_front_dashboard-cluster.id
  task_definition = aws_ecs_task_definition.loregen_front_dashboard-task.arn
  launch_type     = "FARGATE"

  network_configuration {
    subnets = [
      aws_subnet.loregen_front_dashboard_subnet_private_1a.id,
      aws_subnet.loregen_front_dashboard_subnet_private_1b.id
      ]
    
    security_groups = [aws_security_group.loregen_front_dashboard-service-sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.loregen_front_dashboard_tg.arn
    container_name   = "loregen_front_dashboard-container"
    container_port   = 80
  }

  depends_on = [
    aws_lb_listener.loregen_front_dashboard_https_listener
  ]
  desired_count = 1

}


## IAM
#

resource "aws_iam_role" "ecs_task_role_for_loregen_front_dashboard" {
  name = "ecs_task_role_for_loregen_front_dashboard"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy" "ecs_task_policy_for_loregen_front_dashboard" {
  name = "ecs_task_policy_for_loregen_front_dashboard"
  role = aws_iam_role.ecs_task_role_for_loregen_front_dashboard.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:*"
        ],
        Effect = "Allow",
        Resource = [
          "*"
        ]
      },
      {
        Action = [
          "textract:*",      # TS TODO: tailor these
        ],
        Effect = "Allow",
        Resource = "*"
      },
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem"
        ],
        Effect = "Allow",
        Resource = "arn:aws:dynamodb:${var.aws_region}:${var.aws_account}:table/${var.dynamodb_table_name}"
      },
      {
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ],
        Effect = "Allow",
        Resource = "*" # adjust later
      },
      {
        Action = [
          "rds:DescribeDBClusters",
          "rds:DescribeDBInstances"
        ],
        Effect = "Allow",
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ],
        Resource = "arn:aws:dynamodb:${var.aws_region}:${var.aws_account}:table/ssrf_requests"
      }
    ]
  })
}

resource "aws_iam_role" "ecs_execution_role_for_loregen_front_dashboard" {
  name = "ecs_execution_role_for_loregen_front_dashboard"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy" "ecs_execution_policy_for_loregen_front_dashboard" {
  name = "ecs_execution_policy_for_loregen_front_dashboard"
  role = aws_iam_role.ecs_execution_role_for_loregen_front_dashboard.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ],
        Effect = "Allow",
        Resource = "*"
      },
      {
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect = "Allow",
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ],
        Effect   = "Allow",
        Resource = [
          data.aws_secretsmanager_secret.openai_api_key.arn, 
          data.aws_secretsmanager_secret.openrouter_api_key.arn,
          data.aws_secretsmanager_secret.anthropic_api_key.arn,
          data.aws_secretsmanager_secret.mistral_api_key.arn,
          data.aws_secretsmanager_secret.google_api_key.arn,
          data.aws_secretsmanager_secret.groq_api_key.arn,
          data.aws_secretsmanager_secret.deepseek_api_key.arn,
          data.aws_secretsmanager_secret.xai_api_key.arn,
          data.aws_secretsmanager_secret.langsmith_api_key.arn,
          ]
      },
    ]
  })
}

## SGs
#

resource "aws_security_group" "loregen_front_dashboard-service-sg" {
  name        = "loregen_front_dashboard_public_http_access_1"
  description = "Allow public access to HTTP on port 80 and 8000"
  vpc_id      = aws_vpc.loregen_front_vpc.id

  ingress {
    description = "HTTP"
    from_port   = var.app_port  # differentiate to external and internal later
    to_port     = var.app_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "loregen_front_dashboard_public_http_access"
  }
}

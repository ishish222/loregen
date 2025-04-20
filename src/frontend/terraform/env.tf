data "aws_secretsmanager_secret" "openai_api_key" {
  name = "/api_keys/openai_1"
}

data "aws_secretsmanager_secret" "openrouter_api_key" {
  name = "/api_keys/openrouter_1"
}

data "aws_secretsmanager_secret" "anthropic_api_key" {
  name = "/api_keys/anthropic_1"
}

data "aws_secretsmanager_secret" "mistral_api_key" {
  name = "/api_keys/mistral"
}

data "aws_secretsmanager_secret" "google_api_key" {
  name = "/api_keys/google_1"
}

data "aws_secretsmanager_secret" "groq_api_key" {
  name = "/api_keys/groq_1"
}

data "aws_secretsmanager_secret" "deepseek_api_key" {
  name = "/api_keys/deepseek_1"
}

data "aws_secretsmanager_secret" "xai_api_key" {
  name = "/api_keys/xai_1"
}

data "aws_secretsmanager_secret" "langsmith_api_key" {
  name = "/api_keys/langsmith/ai-navigator-prod"
}

data "aws_secretsmanager_secret" "loregen_front_db_password" {
  name = "/loregen_front_db/password"
}

data "aws_secretsmanager_secret_version" "loregen_front_db_password_version" {
  secret_id = data.aws_secretsmanager_secret.loregen_front_db_password.id
}

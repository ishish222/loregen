resource "aws_api_gateway_rest_api" "stripe_webhook_api" {
  name        = "stripe_webhook_api"
  description = "API for servicing callbacks from Stripe"
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "notify_resource" {
  rest_api_id = aws_api_gateway_rest_api.stripe_webhook_api.id
  parent_id   = aws_api_gateway_rest_api.stripe_webhook_api.root_resource_id
  path_part   = "notify"
}

# GET
resource "aws_api_gateway_method" "get_method" {
  rest_api_id   = aws_api_gateway_rest_api.stripe_webhook_api.id
  resource_id   = aws_api_gateway_resource.notify_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "stripe_webhook_api_lambda_integration_get" {
  rest_api_id             = aws_api_gateway_rest_api.stripe_webhook_api.id
  resource_id             = aws_api_gateway_resource.notify_resource.id
  http_method             = aws_api_gateway_method.get_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.lambda_service_strapi_webhook.arn}/invocations"
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_service_strapi_webhook.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.stripe_webhook_api.execution_arn}/*/GET/notify"
}

# POST
resource "aws_api_gateway_method" "post_method" {
  rest_api_id   = aws_api_gateway_rest_api.stripe_webhook_api.id
  resource_id   = aws_api_gateway_resource.notify_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "stripe_webhook_api_lambda_integration_post" {
  rest_api_id             = aws_api_gateway_rest_api.stripe_webhook_api.id
  resource_id             = aws_api_gateway_resource.notify_resource.id
  http_method             = aws_api_gateway_method.post_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.lambda_service_strapi_webhook.arn}/invocations"
}

resource "aws_lambda_permission" "apigw_lambda_post" {
  statement_id  = "AllowAPIGatewayInvokePOST"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_service_strapi_webhook.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.stripe_webhook_api.execution_arn}/*/POST/notify"
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on  = [
    aws_api_gateway_integration.stripe_webhook_api_lambda_integration_get,
    aws_api_gateway_integration.stripe_webhook_api_lambda_integration_post
  ]
  rest_api_id = aws_api_gateway_rest_api.stripe_webhook_api.id
}

resource "aws_api_gateway_domain_name" "callback_custom_domain" {
  domain_name              = var.callback_custom_domain
  regional_certificate_arn = var.certificate_arn_subdomains

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_base_path_mapping" "callback_domain_mapping" {
  domain_name = aws_api_gateway_domain_name.callback_custom_domain.domain_name
  api_id      = aws_api_gateway_rest_api.stripe_webhook_api.id
  stage_name  = aws_api_gateway_deployment.deployment.stage_name
}

resource "aws_route53_record" "callback_custom_domain_record" {
  zone_id = var.dns_zone_id
  name    = aws_api_gateway_domain_name.callback_custom_domain.domain_name
  type    = "A"

  alias {
    name                   = aws_api_gateway_domain_name.callback_custom_domain.regional_domain_name
    zone_id                = aws_api_gateway_domain_name.callback_custom_domain.regional_zone_id
    evaluate_target_health = false
  }
}

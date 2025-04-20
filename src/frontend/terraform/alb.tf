# Application Load Balancer (ALB), Target Group, and Listener

resource "aws_security_group" "alb_sg" {
  name        = "loregen_front_dashboard_public_alb_sg"
  description = "Allow public access to HTTP and HTTPS on port 80 and 443"
  vpc_id      = aws_vpc.navigator_vpc.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    description      = "HTTPS"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
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

resource "aws_lb" "loregen_front_dashboard_alb" {
  name               = "navi-dashboard-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = [
	aws_subnet.loregen_front_dashboard_subnet_public_1a.id,
	aws_subnet.loregen_front_dashboard_subnet_public_1b.id
	]
  security_groups    = [aws_security_group.alb_sg.id]
}

resource "aws_lb_target_group" "loregen_front_dashboard_tg" {
  name     = "navi-dashboard-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.navigator_vpc.id
  target_type = "ip"

health_check {
    enabled             = true
    healthy_threshold   = 3
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    path                = "/health"
#    path                = "/"
    protocol            = "HTTP"
    matcher             = "200"
  }
}

resource "aws_lb_listener" "loregen_front_dashboard_https_listener" {
  load_balancer_arn = aws_lb.loregen_front_dashboard_alb.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.loregen_front_dashboard_tg.arn
  }
}

resource "aws_lb_listener" "loregen_front_dashboard_listener" {
  load_balancer_arn = aws_lb.loregen_front_dashboard_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      protocol   = "HTTPS"
      port       = "443"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_route53_record" "loregen_front_dashboard_dns" {
  zone_id = var.dns_zone_id
  name    = var.alb_domain_name
  type    = "A"

  alias {
    name                   = aws_lb.loregen_front_dashboard_alb.dns_name
    zone_id                = aws_lb.loregen_front_dashboard_alb.zone_id
    evaluate_target_health = true
  }
}

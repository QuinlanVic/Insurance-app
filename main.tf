variable "access_key_aws" {
  description = "access key for AWS account"
  type        = string
}

variable "secret_key_aws" {
  description = "secret key for AWS account"
  type        = string
}

variable "token_session" {
  description = "session token for AWS account"
  type        = string
}

variable "subnet_ids" {
  description = "IDs of subnets"
  type        = list(string)
}

variable "vpc_id" {
  description = "ID for VPC"
  type        = string
}

provider "aws" {
  region = "eu-north-1"
  # implement safer storage later 
  access_key = var.access_key_aws
  secret_key = var.secret_key_aws
  token      = var.token_session
}

# Create ECR repository if not existing (using existing)
resource "aws_ecr_repository" "my_app_repo" {
  name = "quinlan/insurance-app"
}

# ECS Cluster
resource "aws_ecs_cluster" "my_app_cluster" {
  name = "my-app-cluster"
}

# TEST UP UNTIL HERE

# Security group for load balancer
resource "aws_security_group" "lb_sg" {
  name        = "load_balancer_sg"
  description = "Security group for the ALB"
  vpc_id      = var.vpc_id # Reference your VPC (can manage in terraform)

  # Allow incoming HTTP traffic on port 80 from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allows traffic from anywhere (Internet)
  }

  # Allow incoming HTTP traffic on port 8000 from anywhere
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allows traffic from anywhere (Internet)
  }

  # Allow all outbound traffic (so the ALB can communicate with other services)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "load_balancer_security_group"
  }
}

# Application Load Balancer
resource "aws_lb" "app_lb" {
  name               = "app-load-balancer"
  internal           = false
  load_balancer_type = "application"                 # or "network" for NLB
  security_groups    = [aws_security_group.lb_sg.id] # Attaches the security group defined above here
  subnets            = var.subnet_ids                # Attach it to your public subnets (can manage in Terraform)

  enable_deletion_protection = false

  tags = {
    Name = "app-load-balancer"
  }
}

# HTTP Listener on port 8000 for Load Balancer
resource "aws_lb_listener" "http" {
  # the ARN (Amazon Resource Name) is a property that Terraform outputs after creating the resource     
  load_balancer_arn = aws_lb.app_lb.arn # this is created by terraform through our load balancer configuration
  port              = "8000"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.my_app_tg.arn
  }
}

# Target Group for Load balancer
resource "aws_lb_target_group" "my_app_tg" {
  name        = "my-app-tg"
  port        = 5000 # where load balancer is going to send traffic to
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  tags = {
    Name = "app-target-group"
  }
}


# ECS Task Definition
resource "aws_ecs_task_definition" "my_app_task" {
  family       = "my-app-task"
  network_mode = "awsvpc"
  container_definitions = jsonencode([
    {
      name      = "my-app"
      image     = "${aws_ecr_repository.my_app_repo.repository_url}:latest3.0" # reference the existing repo URL
      memory    = 512
      cpu       = 256
      essential = true
      portMappings = [{
        containerPort = 5000 # port of container run by task
        hostPort      = 5000
        protocol      = "tcp"
      }]
    }
  ])
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
  cpu                      = "256"
  memory                   = "512"
}

# Security group for ECS tasks in ECS service
resource "aws_security_group" "ecs_tasks_sg" {
  name        = "ecs_tasks_sg"
  description = "Security group for ECS tasks"
  vpc_id      = var.vpc_id # Reference your VPC (can be managed through terraform)

  # Ingress rule: Allow traffic from the Load Balancer (All traffic)
  ingress {
    from_port       = 0 # Port for HTTPS traffic (if applicable)
    to_port         = 0
    protocol        = "tcp"
    security_groups = [aws_security_group.lb_sg.id] # Allows traffic from ELB security group
  }

  # Ingress rule: Allow traffic from the Load Balancer (HTTP)
  ingress {
    from_port   = 80 # Port for HTTP traffic
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["197.98.201.109/32"] # Allows traffic from my local IP address
  }

  # Ingress rule: Allow traffic from the Load Balancer (Custom TCP)
  ingress {
    from_port   = 5000 # Port for docker container access
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allows traffic from anywhere (Internet)
  }

  # Egress rule: Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"          # "-1" allows all protocols
    cidr_blocks = ["0.0.0.0/0"] # Allow outbound traffic to anywhere
  }

  tags = {
    Name = "ecs_tasks_security_group"
  }
}

# ECS Service
resource "aws_ecs_service" "my_app_service" {
  name            = "my-app-service"
  cluster         = aws_ecs_cluster.my_app_cluster.id
  task_definition = aws_ecs_task_definition.my_app_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = [aws_security_group.ecs_tasks_sg.id] # Attaches the security group for the ECS tasks defined above here
    assign_public_ip = true
  }

  # (forward traffic to port 5000 where container is)
  load_balancer {
    target_group_arn = aws_lb_target_group.my_app_tg.arn
    container_name   = "my-app"
    container_port   = 5000
  }
  # Ensure the ALB listener is created before the ECS service (so it doesn't try use it before it's created)
  depends_on = [aws_lb_listener.http]
}

# IAM role for the task execution
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com" # ECS tasks are allowed to assume this role
        }
      }
    ]
  })
}

# Attach the ECS Task Execution Role policy to the role
resource "aws_iam_role_policy_attachment" "ecs_execution_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  role       = aws_iam_role.ecs_task_execution_role.name
}

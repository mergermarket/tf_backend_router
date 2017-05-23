# required
variable "dns_domain" {
  description = ""
  type        = "string"
  default     = "mmgapi.net"
}

variable "aws_region" {
  description = "AWS Region"
  default     = "eu-west-1"
}

variable "env" {
  description = "Environment name"
}

variable "team" {
  description = "Team that owns the service"
}

variable "component" {
  description = "Component name"
}

variable "platform_config" {
  description = "Platform configuration"
  type        = "map"
  default     = {}
}

# optional
variable "extra_security_groups" {
  description = "Extra Security Groups to attach to the ALB"
  type        = "list"
  default     = []
}

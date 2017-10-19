Backend Router terraform module
===============================

[![Build Status](https://travis-ci.org/mergermarket/tf_backend_router.svg?branch=master)](https://travis-ci.org/mergermarket/tf_backend_router)

This module creates a Backend Router service which, in effect, is a shared ALB to which individual services can be attached.
Ideally, there should be a single Backend Router per Team (e.g. platform-backend-router).

The Backend Router consists of:
- an ALB
- default, HTTPS Listener, with a certificate as per `dns_domain` parameter, by default diverting traffic to `404` ECS Service
- 404 ECS Service which deploys all the required components (404 ECS Service, 404 Target Group, 404 IAM Role and Policy and) and runs a tiny binary which returns 404 to every call

Services attached to this ALB should be using `host-based` conditions for routing, rather than `path-based`.

Module Input Variables
----------------------

- `team` - (string) - **REQUIRED** - Name of Team deploying the ALB - will affect ALBs name
- `env` - (string) - **REQUIRED** - Environment deployed to
- `component` - (string) - **REQUIRED** - component name
- `platform_config` - (map) - **REQUIRED** - Mergermarket Platform config dictionary (see tests for example one)
- `dns_domain` - (string) - **REQUIRED** - domain to be used when looking up SSL Certificate
- `alb_internal` - (bool) - If true, the ALB will be internal (default: `true`)

Usage
-----
```hcl

# the below platform_config map can be passed as a TF var-file (eg. JSON file)
variable "platform_config" {
  type = "map"
  default  = {
    platform_config: {
      azs: "eu-west-1a,eu-west-1b,eu-west-1c",
      elb_certificates.domain_com: "arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012",
      route53_zone_id.domain_com: "AAAAAAAAAAAAA",
      ecs_cluster.default.client_security_group: "sg-00000000",
      ecs_cluster.default.security_group: "sg-11111111",
      vpc: "vpc-12345678",
      private_subnets: "subnet-00000000,subnet-11111111,subnet-22222222"
      public_subnets: "subnet-333333333,subnet-44444444,subnet-55555555"
    }
  }
}

module "backend_router" {
  source = "../.."

  team            = "footeam"
  env             = "fooenv"
  component       = "foocomponent"
  platform_config = "${var.platform_config}"
  dns_domain      = "domain.com"
}
```

Outputs
-------
- `alb_dns_name` - The DNS name of the load balancer
- `alb_arn` - The AWS ARN of the load balancer
- `alb_listener_arn` - The ARN of the load balancer listener

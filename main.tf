module "404_container_definition" {
  source = "git::https://github.com/mergermarket/tf_ecs_container_definition.git?ref=PLAT-915_first_implementation"

  name  = "404"
  image = "mergermarket/404"
}

module "404_task_definition" {
  source = "github.com/mergermarket/tf_ecs_task_definition"

  family                = "404"
  container_definitions = ["${module.404_container_definition.rendered}"]
}

module "404_ecs_service" {
  source = "github.com/mergermarket/tf_load_balanced_ecs_service"

  name            = "${format("%s-%s-404", var.env, var.component)}"
  vpc_id          = "${var.platform_config["vpc"]}"
  task_definition = "${module.404_task_definition.arn}"
}

module "alb" {
  source = "github.com/mergermarket/tf_alb"

  name                     = "${format("%s-%s-router", var.env, var.component)}"
  vpc_id                   = "${var.platform_config["vpc"]}"
  subnet_ids               = ["${var.platform_config["private_subnets"]}"]
  extra_security_groups    = "${var.extra_security_groups}"
  certificate_arn          = "${var.platform_config["elb_certificates.${replace(var.dns_domain, "/\\./", "_")}"]}"
  default_target_group_arn = "${module.404_ecs_service.target_group_arn}"
}

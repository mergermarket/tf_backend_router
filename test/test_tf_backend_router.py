import unittest
from subprocess import check_call, check_output


class TestTFBackendRouter(unittest.TestCase):

    def setUp(self):
        check_call(['terraform', 'get', 'test/infra'])

    def test_create_backend_router_number_of_resources_to_add(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var', 'aws_region=eu-west-1',
            '-var-file=test/platform-config/eu-west-1.json',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
Plan: 8 to add, 0 to change, 0 to destroy.
        """.strip() in output

    def test_create_alb(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var', 'aws_region=eu-west-1',
            '-var-file=test/platform-config/eu-west-1.json',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_router.alb.aws_alb.alb
    arn:                        "<computed>"
    arn_suffix:                 "<computed>"
    dns_name:                   "<computed>"
    enable_deletion_protection: "false"
    idle_timeout:               "60"
    internal:                   "true"
    ip_address_type:            "<computed>"
    name:                       "dev-foobar-router"
    security_groups.#:          "<computed>"
    subnets.#:                  "1"
    subnets.2516719898:         "subnet-00000000,subnet-11111111,subnet-22222222"
    vpc_id:                     "<computed>"
    zone_id:                    "<computed>"
        """.strip() in output # noqa

    def test_create_alb_listener(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var', 'aws_region=eu-west-1',
            '-var-file=test/platform-config/eu-west-1.json',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_router.alb.aws_alb_listener.https
    arn:                               "<computed>"
    certificate_arn:                   "arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012"
    default_action.#:                  "1"
    default_action.0.target_group_arn: "${var.default_target_group_arn}"
    default_action.0.type:             "forward"
    load_balancer_arn:                 "${aws_alb.alb.arn}"
    port:                              "443"
    protocol:                          "HTTPS"
    ssl_policy:                        "<computed>"
        """.strip() in output # noqa

    def test_create_alb_security_group(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var', 'aws_region=eu-west-1',
            '-var-file=test/platform-config/eu-west-1.json',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_router.alb.aws_security_group.default
    description:                           "Managed by Terraform"
    egress.#:                              "1"
    egress.482069346.cidr_blocks.#:        "1"
    egress.482069346.cidr_blocks.0:        "0.0.0.0/0"
    egress.482069346.from_port:            "0"
    egress.482069346.ipv6_cidr_blocks.#:   "0"
    egress.482069346.prefix_list_ids.#:    "0"
    egress.482069346.protocol:             "-1"
    egress.482069346.security_groups.#:    "0"
    egress.482069346.self:                 "false"
    egress.482069346.to_port:              "0"
    ingress.#:                             "1"
    ingress.2617001939.cidr_blocks.#:      "1"
    ingress.2617001939.cidr_blocks.0:      "0.0.0.0/0"
    ingress.2617001939.from_port:          "443"
    ingress.2617001939.ipv6_cidr_blocks.#: "0"
    ingress.2617001939.protocol:           "tcp"
    ingress.2617001939.security_groups.#:  "0"
    ingress.2617001939.self:               "false"
    ingress.2617001939.to_port:            "443"
    name:                                  "<computed>"
    owner_id:                              "<computed>"
    vpc_id:                                "vpc-12345678"
        """.strip() in output # noqa

    def test_create_404_service_task_definition(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var', 'aws_region=eu-west-1',
            '-var-file=test/platform-config/eu-west-1.json',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_router.404_task_definition.aws_ecs_task_definition.taskdef
    arn:                   "<computed>"
    container_definitions: "7599fdbfa93c9a10d50af7e18b88d4c51e8e9179"
    family:                "404"
    network_mode:          "<computed>"
    revision:              "<computed>"
        """.strip() in output

    def test_create_404_service_target_group(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var', 'aws_region=eu-west-1',
            '-var-file=test/platform-config/eu-west-1.json',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_router.404_ecs_service.aws_alb_target_group.target_group
    arn:                                "<computed>"
    arn_suffix:                         "<computed>"
    deregistration_delay:               "10"
    health_check.#:                     "1"
    health_check.0.healthy_threshold:   "2"
    health_check.0.interval:            "5"
    health_check.0.matcher:             "200-299"
    health_check.0.path:                "/internal/healthcheck"
    health_check.0.port:                "traffic-port"
    health_check.0.protocol:            "HTTP"
    health_check.0.timeout:             "4"
    health_check.0.unhealthy_threshold: "2"
    name:                               "dev-foobar-404"
    port:                               "31337"
    protocol:                           "HTTP"
    stickiness.#:                       "<computed>"
    vpc_id:                             "vpc-12345678"
        """.strip() in output

    def test_create_404_service_ecs_service(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var', 'aws_region=eu-west-1',
            '-var-file=test/platform-config/eu-west-1.json',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_router.404_ecs_service.aws_ecs_service.service
    cluster:                                    "default"
    deployment_maximum_percent:                 "200"
    deployment_minimum_healthy_percent:         "100"
    desired_count:                              "1"
    iam_role:                                   "${aws_iam_role.role.arn}"
    load_balancer.#:                            "1"
    load_balancer.~2788651468.container_name:   "app"
    load_balancer.~2788651468.container_port:   "8000"
    load_balancer.~2788651468.elb_name:         ""
    load_balancer.~2788651468.target_group_arn: "${aws_alb_target_group.target_group.arn}"
    name:                                       "dev-foobar-404"
    placement_strategy.#:                       "2"
    placement_strategy.2093792364.field:        "attribute:ecs.availability-zone"
    placement_strategy.2093792364.type:         "spread"
    placement_strategy.3946258308.field:        "instanceId"
    placement_strategy.3946258308.type:         "spread"
    task_definition:                            "${var.task_definition}"
        """.strip() in output # noqa

    def test_create_404_service_iam_role(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var', 'aws_region=eu-west-1',
            '-var-file=test/platform-config/eu-west-1.json',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_router.404_ecs_service.aws_iam_role.role
    arn:                "<computed>"
        """.strip() in output # noqa

        assert """
    create_date:        "<computed>"
    name:               "<computed>"
    name_prefix:        "dev-foobar-404-service-role"
    path:               "/"
    unique_id:          "<computed>"
        """.strip() in output # noqa

    def test_create_404_service_iam_role_policy(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var', 'aws_region=eu-west-1',
            '-var-file=test/platform-config/eu-west-1.json',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_router.404_ecs_service.aws_iam_role_policy.policy
    name:        "<computed>"
    name_prefix: "dev-foobar-404-service-policy"
        """.strip() in output # noqa

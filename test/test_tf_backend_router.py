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
            '-target=module.backend_router.module.alb',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
Plan: 4 to add, 0 to change, 0 to destroy.
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
            '-target=module.backend_router.module.alb',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_router.alb.aws_alb.alb
    access_logs.#:              "1"
    access_logs.0.enabled:      "false"
    arn:                        "<computed>"
    arn_suffix:                 "<computed>"
    dns_name:                   "<computed>"
    enable_deletion_protection: "false"
    idle_timeout:               "60"
    internal:                   "true"
    ip_address_type:            "<computed>"
    name:                       "dev-foobar-router"
    security_groups.#:          "<computed>"
    subnets.#:                  "3"
        """.strip() in output # noqa

        assert """
    subnets.#:                  "3"
    subnets.1120168869:         "subnet-11111111"
    subnets.155686431:          "subnet-00000000"
    subnets.2655022443:         "subnet-22222222"
        """.strip() in output # noqa

        assert """
    tags.%:                     "3"
    tags.component:             "foobar"
    tags.environment:           "dev"
    tags.team:                  "foobar"
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
            '-target=module.backend_router.module.alb',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_router.alb.aws_alb_listener.https
    arn:                               "<computed>"
    certificate_arn:                   "${module.aws_acm_certificate_arn.arn}"
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
            '-target=module.backend_router.module.alb',
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
    ingress.#:                             "2"
    ingress.2214680975.cidr_blocks.#:      "1"
    ingress.2214680975.cidr_blocks.0:      "0.0.0.0/0"
    ingress.2214680975.from_port:          "80"
    ingress.2214680975.ipv6_cidr_blocks.#: "0"
    ingress.2214680975.protocol:           "tcp"
    ingress.2214680975.security_groups.#:  "0"
    ingress.2214680975.self:               "false"
    ingress.2214680975.to_port:            "80"
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

    def test_create_external_alb(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var', 'aws_region=eu-west-1',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_router_external.module.alb',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_router_external.alb.aws_alb.alb
    access_logs.#:              "1"
    access_logs.0.enabled:      "false"
    arn:                        "<computed>"
    arn_suffix:                 "<computed>"
    dns_name:                   "<computed>"
    enable_deletion_protection: "false"
    idle_timeout:               "60"
    internal:                   "false"
    ip_address_type:            "<computed>"
    name:                       "dev-foobar-router"
    security_groups.#:          "<computed>"
    subnets.#:                  "3"
        """.strip() in output # noqa

        assert """
    subnets.#:                  "3"
    subnets.2377178398:         "subnet-555555555"
    subnets.3586363601:         "subnet-33333333"
    subnets.4231620278:         "subnet-44444444"
        """.strip() in output # noqa

    def test_default_target_group(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'component=foobar',
            '-var', 'team=foobar',
            '-var', 'aws_region=eu-west-1',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_router',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_router.aws_alb_target_group.default_target_group
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
    name:                               "dev-default-foobar"
    port:                               "31337"
    protocol:                           "HTTP"
    stickiness.#:                       "<computed>"
    vpc_id:                             "vpc-12345678"
        """.strip() in output # noqa

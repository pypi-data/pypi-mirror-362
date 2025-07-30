import warnings
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.template import loader

from open_api_framework.conf.utils import EnvironmentVariable


def convert_variables_to_rst(variables: list[EnvironmentVariable]) -> str:
    template = loader.get_template("open_api_framework/env_config.rst")
    grouped_vars = defaultdict(list)
    for var in variables:
        if not var.help_text:
            warnings.warn(f"missing help_text for environment variable {var}")
        grouped_vars[var.group].append(var)
    return template.render({"vars": grouped_vars.items()})


class Command(BaseCommand):
    help = "Generate documentation for all used envvars"

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            "--file",
            help="Name and path of the file to which the documentation will be written.",
            nargs="?",
            default="docs/env_config.rst",
        )
        parser.add_argument(
            "--exclude-group",
            help="Names of groups that should not be excluded in the generated docs.",
            action="append",
        )

    def handle(self, *args, **options):
        from open_api_framework.conf.utils import ENVVAR_REGISTRY

        file_path = options["file"]
        exclude_groups = options["exclude_group"] or []

        def _sort(envvar):
            match envvar.group:
                case "Required":
                    return 0
                case "Optional":
                    return 2
                case _:
                    return 1

        sorted_registry = sorted(
            [var for var in ENVVAR_REGISTRY if var.group not in exclude_groups],
            key=_sort,
        )
        with open(file_path, "w") as f:
            f.write(convert_variables_to_rst(sorted_registry))

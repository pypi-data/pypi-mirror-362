{% set template_domain_import = "shared.domain"|compute_base_path(template.name) %}
from {{ general.source_name }}.{{ template_domain_import }}.exceptions.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from {{ general.source_name }}.{{ template_domain_import }}.exceptions.required_value_error import (
    RequiredValueError,
)
from {{ general.source_name }}.{{ template_domain_import }}.value_object.value_object import ValueObject


class StringValueObject(ValueObject[str]):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def _validate(self, value: str) -> None:
        if value is None:
            raise RequiredValueError
        if not isinstance(value, str):
            raise IncorrectValueTypeError

from pancham.data_frame_field import DataFrameField
from pancham.tool.str_tools import remove_and_split
from .field_parser import FieldParser

class SplitFieldParser(FieldParser):
    """
    Parser for fields that require splitting strings based on a specific character or pattern.

    This class extends the FieldParser and provides functionality to parse fields with
    splitting logic. It determines if a field can be parsed by verifying the presence
    of a specific key and function ID. The splitting operation can optionally remove
    specific patterns from the source value before splitting. The resulting segments
    are then stripped of whitespace and empty entries are excluded.

    :ivar FUNCTION_ID: Unique identifier for the split operation as required by the
        field configuration.
    :type FUNCTION_ID: str
    """

    FUNCTION_ID = "split"

    def can_parse_field(self, field: dict) -> bool:
        return self.has_function_key(field, self.FUNCTION_ID)

    def parse_field(self, field: dict) -> DataFrameField:
        properties = field[self.FUNCTION_KEY][self.FUNCTION_ID]
        split_char = properties["split_char"]
        remove_pattern = properties.get("remove_pattern", None)
        source_name = self.get_source_name(field)
        field[self.FIELD_TYPE_KEY] = list[str]

        def extract(data: dict) -> list[str|int|float]:
            value = data[source_name]

            return remove_and_split(value, split_char, remove_pattern)

        return self.build_func_field(field, extract)


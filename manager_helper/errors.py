from typing import List

import constants


def rate_column_error(file_path: str, found_headers: List[str]) -> str:
    return constants.HEADERS_ERROR.format(
        file_path,
        ', '.join(found_headers)
    )


def missing_columns_error(missing: set, file_path: str) -> str:
    return constants.MISSING_COLUMN_ERROR.format(
        ', '.join(missing),
        file_path
    )

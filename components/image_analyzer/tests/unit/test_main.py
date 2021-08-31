from datetime import datetime
from unittest.mock import MagicMock, patch

from image_analyzer.main import main


@patch("builtins.print")
def test_run(print_mock: MagicMock):
    # Given
    from_datetime = datetime.strptime("2021-01-01", "%Y-%m-%d").date()
    # When
    main(from_datetime)

    # Then
    print_mock.assert_called_once_with("Run on date from '2021-01-01'")

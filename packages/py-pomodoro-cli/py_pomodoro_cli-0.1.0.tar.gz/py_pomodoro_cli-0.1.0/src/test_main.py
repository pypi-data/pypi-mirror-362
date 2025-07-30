from unittest.mock import MagicMock, patch

from main import run_pomodoro


def test_run_pomodoro_completes_and_displays_message():
    """
    Tests that the Pomodoro timer completes and displays the correct
    completion message.
    """
    interval = 1  # 1 minute for testing
    mock_console = MagicMock()
    mock_progress = MagicMock()

    with patch("main.console", mock_console), patch(
        "main.Progress", return_value=mock_progress
    ), patch("main.time.sleep"), patch(
        "main.datetime"
    ) as mock_datetime, patch(
        "main.time.time"
    ):
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2025-01-01 12:01:00"
        mock_datetime.now.return_value = mock_now

        run_pomodoro(interval)

    # Check that the start message was printed
    mock_console.print.assert_any_call(
        "🚀 Starting Pomodoro timer...", style="bold #5E81AC"
    )

    # Check that the completion message was printed
    mock_console.print.assert_any_call(
        "🎉 The current Pomodoro interval has completed - 2025-01-01 12:01:00",
        style="bold #8FBCBB",
    )

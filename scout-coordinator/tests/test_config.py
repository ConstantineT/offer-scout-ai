import pytest

from scout_coordinator.config import Settings


def test_settings_reads_combined_resend_credentials() -> None:
    settings = Settings(
        resend_credentials='{"api_key":"resend-key","webhook_secret":"whsec_test"}',
    )

    assert settings.resend_api_key == "resend-key"
    assert settings.resend_webhook_secret == "whsec_test"


def test_settings_reads_combined_gmail_json_credentials() -> None:
    settings = Settings(
        gmail_smtp_credentials='{"username":"sender@gmail.com","app_password":"app-password"}',
    )

    assert settings.gmail_smtp_username == "sender@gmail.com"
    assert settings.gmail_smtp_app_password == "app-password"


def test_settings_reads_combined_gmail_colon_credentials() -> None:
    settings = Settings(
        gmail_smtp_credentials="sender@gmail.com:app-password",
    )

    assert settings.gmail_smtp_username == "sender@gmail.com"
    assert settings.gmail_smtp_app_password == "app-password"


def test_settings_keeps_split_credentials_when_combined_values_are_missing() -> None:
    settings = Settings(
        resend_api_key="resend-key",
        resend_webhook_secret="whsec_test",
        gmail_smtp_username="sender@gmail.com",
        gmail_smtp_app_password="app-password",
    )

    assert settings.resend_api_key == "resend-key"
    assert settings.resend_webhook_secret == "whsec_test"
    assert settings.gmail_smtp_username == "sender@gmail.com"
    assert settings.gmail_smtp_app_password == "app-password"


def test_settings_rejects_invalid_combined_resend_credentials() -> None:
    with pytest.raises(ValueError, match="RESEND_CREDENTIALS must be valid JSON"):
        Settings(resend_credentials="not-json")


def test_settings_rejects_invalid_combined_gmail_credentials() -> None:
    with pytest.raises(ValueError, match="GMAIL_SMTP_CREDENTIALS must be JSON or username:app_password"):
        Settings(gmail_smtp_credentials="sender@gmail.com")

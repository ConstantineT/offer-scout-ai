import pytest

from scout_coordinator.config import Settings


def test_settings_reads_combined_resend_credentials() -> None:
    settings = Settings(
        resend_credentials=(
            '{"api_key":"resend-key","webhook_secret":"whsec_test",'
            '"from_email":"Offer Scout <scout@example.com>"}'
        ),
    )

    assert settings.resend_api_key == "resend-key"
    assert settings.resend_webhook_secret == "whsec_test"
    assert settings.resend_from_email == "Offer Scout <scout@example.com>"


def test_settings_keeps_split_credentials_when_combined_values_are_missing() -> None:
    settings = Settings(
        resend_api_key="resend-key",
        resend_webhook_secret="whsec_test",
        resend_from_email="Offer Scout <scout@your-domain>",
    )

    assert settings.resend_api_key == "resend-key"
    assert settings.resend_webhook_secret == "whsec_test"
    assert settings.resend_from_email == "Offer Scout <scout@your-domain>"


def test_settings_rejects_invalid_combined_resend_credentials() -> None:
    with pytest.raises(ValueError, match="RESEND_CREDENTIALS must be valid JSON"):
        Settings(resend_credentials="not-json")

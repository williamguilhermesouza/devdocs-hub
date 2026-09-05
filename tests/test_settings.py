from devdocs_hub.settings import Settings


class TestSettings:
    def test_settings_create(self):
        settings = Settings(_env_file="tests/.env_test")

        assert settings.environment == 'TEST'

from config.settings import UIConfigSettings


class TestUIConfigSettings:
    def test_default_orchestrator_url(self, monkeypatch):
        monkeypatch.delenv('ORCHESTRATOR_URL', raising=False)
        settings = UIConfigSettings()
        assert settings.orchestrator_url == 'http://localhost:8000'

    def test_orchestrator_url_from_env(self, monkeypatch):
        monkeypatch.setenv('ORCHESTRATOR_URL', 'http://custom-host:9000')
        settings = UIConfigSettings()
        assert settings.orchestrator_url == 'http://custom-host:9000'

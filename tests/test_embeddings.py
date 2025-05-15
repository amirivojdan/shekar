from shekar import Embedder
import requests
import time


def test_model_urls():
    for model_name, url in Embedder.available_models.items():
        response = requests.head(url)
        assert response.status_code == 200, (
            f"Model {model_name} URL {url} is not reachable"
        )


def test_load_model():
    embedding = Embedder()
    time.sleep(5)
    if embedding.model is not None:
        assert embedding.model.doesnt_match("خیار گوجه سنگ کاهو".split()) == "سنگ"

import pytest

from fastapi_jwt_harmony import JWTHarmony
from fastapi_jwt_harmony.config import JWTHarmonyConfig
from tests.user_models import SimpleUser


@pytest.fixture(scope='function')
def authorize_fixture() -> JWTHarmony[SimpleUser]:
    JWTHarmony._config = None
    JWTHarmony._user_model_class = SimpleUser
    JWTHarmony.configure(SimpleUser, JWTHarmonyConfig(authjwt_secret_key='testing'))
    return JWTHarmony[SimpleUser]()

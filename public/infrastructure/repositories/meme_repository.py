from infrastructure.models import Meme
from meme.schemas import MemeUpdate, MemeCreate, MemeResponse

from .AbstractRepository import AbstractRepo


class MemeRepo(AbstractRepo):
    model = Meme
    update_schema = MemeUpdate
    create_schema = MemeCreate
    get_schema = MemeResponse


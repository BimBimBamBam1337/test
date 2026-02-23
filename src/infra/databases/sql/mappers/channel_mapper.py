from src.domain.entities import Channel
from src.infra.databases.sql.models import ChannelORM


class ChannelMapper:

    @staticmethod
    def to_entity(orm: ChannelORM) -> Channel:
        return Channel(
            id=orm.id,
            title=orm.title,
            created_at=orm.created_at,
            is_scam=orm.is_scam,
        )

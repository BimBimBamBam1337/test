from src.domain.entities import Channel
from src.infra.databases.sql.models import ChannelORM


class ChannelMapper:
    @staticmethod
    def to_orm(entity: Channel) -> ChannelORM:
        return ChannelORM(
            id=entity.id,
            language=entity.language,
            title=entity.title,
            link=entity.link,
            created_at=entity.created_at,
            is_verified=entity.is_verified,
            is_scam=entity.is_scam,
        )

    @staticmethod
    def to_entity(orm: ChannelORM) -> Channel:
        return Channel(
            id=orm.id,
            language=orm.language,
            title=orm.title,
            link=orm.link,
            type=None,
            created_at=orm.created_at,
            is_verified=orm.is_verified,
            is_scam=orm.is_scam,
        )

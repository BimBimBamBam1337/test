from src.domain.entities import User
from src.infra.databases.sql.models import UserORM


class UserMapper:
    @staticmethod
    def to_entity(orm: UserORM) -> User:
        return User(
            id=orm.id,
            role=orm.role,
            name=orm.name,
            username=orm.username,
            created_at=orm.created_at,
        )

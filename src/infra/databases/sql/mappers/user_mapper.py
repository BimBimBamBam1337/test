from src.domain.entities import User
from src.infra.databases.sql.models import UserORM


class UserMapper:
    @staticmethod
    def to_entity(orm: UserORM) -> User:
        return User(
            id=orm.id,
            role=orm.role,
            first_name=orm.first_name,
            last_name=orm.last_name,
            full_name=orm.first_name if orm.first_name and orm.last_name else None,
            username=orm.username,
            created_at=orm.created_at,
        )

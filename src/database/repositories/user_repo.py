from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.database.exceptions import (
    UserAlreadyExistsError,
    UserError,
    UserNotFoundError,
)
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.database.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session()

    async def create_user(self, user: User) -> User:
        try:
            self.session.add(user)
            await self.session.commit()
            return user
        except IntegrityError:
            await self.session.rollback()
            raise UserAlreadyExistsError(f"{user} already exists.")
        except Exception as e:
            await self.session.rollback()
            raise UserError(f"Error creating {user}: {e}")

    async def get_user_by_id(self, user_id: int) -> User:
        try:
            result = await self.session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one()
            return user
        except NoResultFound:
            raise UserNotFoundError(f"User with id {user_id} not found.")
        except Exception as e:
            raise UserError(f"Error getting user with id {user_id}: {e}")

    async def get_user_by_username(self, username: str) -> User:
        try:
            result = await self.session.execute(
                select(User).where(User.username == username)
            )
            user = result.scalar_one()
            return user
        except NoResultFound:
            raise UserNotFoundError(f"User with username {username} not found.")
        except Exception as e:
            raise UserError(f"Error getting user with username {username}: {e}")

    async def update_user(self, user: User) -> User:
        try:
            await self.session.execute(
                update(User)
                .where(User.id == user.id)
                .values(
                    username=user.username,
                    full_name=user.full_name,
                    language_code=user.language_code,
                )
            )
            await self.session.commit()
            return await self.get_user_by_id(user.id)
        except NoResultFound:
            await self.session.rollback()
            raise UserNotFoundError(f"User with id {user.id} not found.")
        except Exception as e:
            await self.session.rollback()
            raise UserError(f"Error updating user with id {user.id}: {e}")

    async def delete_user(self, user_id: int) -> User:
        try:
            user = await self.get_user_by_id(user_id)
            await self.session.execute(delete(User).where(User.id == user_id))
            await self.session.commit()
            return user
        except NoResultFound:
            await self.session.rollback()
            raise UserNotFoundError(f"User with id {user_id} not found.")
        except Exception as e:
            await self.session.rollback()
            raise UserError(f"Error deleting user with id {user_id}: {e}")

    async def get_users(self) -> list[User]:
        try:
            result = await self.session.execute(select(User))
            return result.scalars().all()
        except Exception as e:
            raise UserError(f"Error getting users: {e}")

from datetime import datetime
from typing import override

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, OperationalError

from app.models.user import User
from app.utils import Hasher, LogHandler

from .repository import Repository

logger = LogHandler.logger(__name__)


class UserRepository(Repository):
    """Class for querying the users table."""

    @override
    def add(self, users: list[User]) -> bool:
        """
        Adds an item/list of items to the database.
        """

        self.hasher = Hasher()
        try:
            with self.db.session as s:
                s.add_all(users)
                s.commit()
                logger.info(msg=f"Added {len(users)} objects to the database")
                return True
        except IntegrityError as err:
            logger.warning(err)
            return False
        except OperationalError as err:
            logger.critical(err)
            return False

    @override
    def get(
        self,
        id: int | None = None,
        *,
        username: str | None = None,
        email: str | None = None,
        date_added: str | None = None,
        is_active: bool | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        count: int = 0,
    ) -> list[User]:
        """
        Retrieve items from the database using given constraints.
        The 'date_from' constraint is the starting date up to the
        'date_to' constraint. If 'date_to' constraint is not set.
        It will default to the current date.

        The 'count' constraint refers to the number of items it will retrieve.
        Defaults to '0' and will retrieve all occurences of constraints.
        """
        # The argument list is not changed to **kwargs for the parameter list to appear on intellisense.
        # Im lazy to type the needed parameters on the docs if i use **kwargs.
        if date_to is None:
            date_to = datetime.now().strftime("%Y-%m-%d")
        try:
            with self.db.session as s:
                stmt = select(User)
                filters = []
                if id is not None:
                    filters.append(User.id == id)
                if email is not None:
                    filters.append(User.email.ilike(f"%{email}%"))
                if is_active is not None:
                    filters.append(User.is_active.ilike(f"%{is_active}%"))
                if date_from is not None:
                    filters.append(User.date_added >= date_from)
                if date_to is not None:
                    filters.append(User.date_added <= date_to)
                if filters:
                    stmt = stmt.where(*filters)
                stmt = stmt.order_by(User.id)
                if count > 0:
                    stmt = stmt.limit(count)
                return list(s.scalars(stmt).all())
        except IntegrityError as err:
            logger.warning(err)
            return []
        except OperationalError as err:
            logger.critical(err)
            return []

    @override
    def update(self, user: User) -> bool:
        """ "
        Updates single user parameters with the given product id.
        """
        # If a batch update is needed, you need to create a batch_update function.
        # This function leaves a performance hit for batch update using for loops on a list of Products.
        # I kept this function as it is because the ui is only used to update a single item at a time.
        if user.id is None:
            logger.warning("Cannot process transaction without a User ID.")
            return False
        try:
            with self.db.session as s:
                merged_user = s.merge(user)
                s.commit()
                logger.info(msg=f"Updated user values with id {merged_user.id}.")
                return True
        except IntegrityError as err:
            logger.warning(err)
            return False
        except OperationalError as err:
            logger.critical(err)
            return False

    @override
    def delete(self, user_id: int) -> bool:
        """
        Disables a user with the given ID.
        Disabling is preferred over permanent deletion in case of cascading domino effects.
        """
        try:
            with self.db.session as s:
                stmt = update(User).where(User.id == user_id).values(is_active=False)
                s.execute(stmt)
                s.commit()
                logger.info(f"Updated user availability with id {user_id}.")
                return True
        except IntegrityError as err:
            logger.warning(err)
            return False
        except OperationalError as err:
            logger.critical(err)
            return False

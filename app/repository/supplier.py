from datetime import datetime
from typing import override

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, OperationalError

from app.models import Supplier
from app.utils import LogHandler

from .repository import Repository

logger = LogHandler.logger(__name__)


class SuppliersRepository(Repository):
    """
    Class for querying the suppliers table.
    """

    @override
    def add(self, suplliers: list[Supplier]) -> bool:
        """
        Adds an item/list of items to the database.
        """
        try:
            with self.db.session as s:
                s.add_all(suplliers)
                s.commit()
                logger.info(msg=f"Added {len(suplliers)} objects to the database")
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
        name: str | None = None,
        address: str | None = None,
        date_added: str | None = None,
        is_active: bool | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        count: int = 0,
    ) -> list[Supplier]:
        """
        Retrieve items from the database using given constraints.

        The 'date_from' constraint is the starting date up to the
        'date_to' constraint. If 'date_to' constraint is not set.
        It will default to the current date.

        The 'count' constraint refers to the number of items it will retrieve.
        Defaults to '0' and will retrieve all occurences of constraints.
        """

        # The argument list is not changed to **kwargs for the parameter list to appear on the intellisense.
        # Im lazy to type the needed parameters on the docs if i use **kwargs.

        if date_to is None:
            date_to = datetime.now().strftime("%Y-%m-%d")

        try:
            with self.db.session as s:
                stmt = select(Supplier)
                filters = []

                if id is not None:
                    filters.append(Supplier.id == id)
                if name is not None:
                    filters.append(Supplier.name.ilike(f"%{name}%"))
                if address is not None:
                    filters.append(Supplier.address.ilike(f"%{address}%"))
                if date_added is not None:
                    filters.append(Supplier.date_added == date_added)
                if is_active is not None:
                    filters.append(Supplier.is_active == is_active)

                if date_from is not None:
                    filters.append(Supplier.date_added >= date_from)
                if date_to is not None:
                    filters.append(Supplier.date_added <= date_to)

                if filters:
                    stmt = stmt.where(*filters)

                stmt = stmt.order_by(Supplier.id)
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
    def update(self, supplier: Supplier) -> bool:
        """ "
        Updates single supplier parameters with the given supplier id.
        """

        # If a batch update is needed, you need to create a batch_update function.
        # This function leaves a performance hit for batch update using for loops on a list of Products.
        # I kept this function as it is because the ui is only used to update a single item at a time.

        if supplier.id is None:
            logger.warning("Cannot process transaction without a Supplier ID.")
            return False

        try:
            with self.db.session as s:
                merged_supplier = s.merge(supplier)
                s.commit()
                logger.info(
                    msg=f"Updated supplier values with id {merged_supplier.id}."
                )
                return True
        except IntegrityError as err:
            logger.warning(err)
            return False
        except OperationalError as err:
            logger.critical(err)
            return False

    @override
    def delete(self, supplier_id: int) -> bool:
        """
        Disables a supplier with the given ID.

        Disabling is preferred over permanent deletion in case of cascading domino effects.
        """

        try:
            with self.db.session as s:
                stmt = (
                    update(Supplier)
                    .where(Supplier.id == supplier_id)
                    .values(is_available=False)
                )
                s.execute(stmt)
                s.commit()
                logger.info(f"Updated supplier availability with id {supplier_id}.")
                return True
        except IntegrityError as err:
            logger.warning(err)
            return False
        except OperationalError as err:
            logger.critical(err)
            return False

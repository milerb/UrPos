from datetime import datetime
from typing import override

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, OperationalError

from app.models import Sale
from app.utils import LogHandler

from .repository import Repository

logger = LogHandler.logger(__name__)


class SalesRepository(Repository):
    """
    Class for querying the sales table.
    """

    @override
    def add(self, sales: list[Sale]) -> bool:
        """
        Adds an item/list of items to the database.
        """
        try:
            with self.db.session as s:
                s.add_all(sales)
                s.commit()
                logger.info(msg=f"Added {len(sales)} objects to the database")
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
        quantity: int | None = None,
        product_id: int | None = None,
        price: float | None = None,
        date: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        count: int = 0,
    ) -> list[Sale]:
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
                stmt = select(Sale)
                filters = []

                if id is not None:
                    filters.append(Sale.id == id)
                if quantity is not None:
                    filters.append(Sale.quantity.ilike(f"%{quantity}%"))
                if product_id is not None:
                    filters.append(Sale.product_id.ilike(f"%{product_id}%"))
                if price is not None:
                    filters.append(Sale.price.ilike(f"%{price}%"))
                if date is not None:
                    filters.append(Sale.date == date)

                if date_from is not None:
                    filters.append(Sale.date >= date_from)
                if date_to is not None:
                    filters.append(Sale.date <= date_to)

                if filters:
                    stmt = stmt.where(*filters)

                stmt = stmt.order_by(Sale.id)
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
    def update(self, sale: Sale) -> bool:
        """ "
        Updates single sale parameters with the given product id.
        """

        # If a batch update is needed, you need to create a batch_update function.
        # This function leaves a performance hit for batch update using for loops on a list of Products.
        # I kept this function as it is because the ui is only used to update a single item at a time.

        if sale.id is None:
            logger.warning("Cannot process transaction without a Sale ID.")
            return False

        try:
            with self.db.session as s:
                merged_sale = s.merge(sale)
                s.commit()
                logger.info(msg=f"Updated product values with id {merged_sale.id}.")
                return True
        except IntegrityError as err:
            logger.warning(err)
            return False
        except OperationalError as err:
            logger.critical(err)
            return False

    @override
    def delete(self, sale_id: int) -> bool:
        """
        Disables a sale with the given ID.

        Disabling is preferred over permanent deletion in case of cascading domino effects.
        """

        try:
            with self.db.session as s:
                stmt = update(Sale).where(Sale.id == sale_id).values(is_available=False)
                s.execute(stmt)
                s.commit()
                logger.info(f"Updated product availability with id {sale_id}.")
                return True
        except IntegrityError as err:
            logger.warning(err)
            return False
        except OperationalError as err:
            logger.critical(err)
            return False

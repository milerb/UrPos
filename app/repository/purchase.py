from datetime import datetime
from typing import override

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError, OperationalError

from app.models import Purchase
from app.utils import LogHandler

from .repository import Repository

logger = LogHandler.logger(__name__)


class PurchaseRepository(Repository):
    """
    Class for querying the purchases table.
    """

    @override
    def add(self, purchase: list[Purchase]) -> bool:
        """
        Adds an item/list of purchases to the database.
        """

        try:
            with self.db.session as s:
                s.add_all(purchase)
                s.commit()
                logger.info(msg=f"Added {len(purchase)} objects to the database")
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
        product_id: int | None = None,
        purchase_date: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        supplier: int | None = None,
        count: int = 0,
    ) -> list[Purchase]:
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
                stmt = select(Purchase)
                filters = []

                if id is not None:
                    filters.append(Purchase.id == id)
                if product_id is not None:
                    filters.append(Purchase.product_id == product_id)
                if purchase_date is not None:
                    filters.append(Purchase.purchase_date == purchase_date)

                if date_from is not None:
                    filters.append(Purchase.purchase_date >= date_from)
                if date_to is not None:
                    filters.append(Purchase.purchase_date <= date_to)

                if filters:
                    stmt = stmt.where(*filters)

                stmt = stmt.order_by(Purchase.purchase_date)
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
    def update(self, purchase: Purchase) -> bool:
        """ "
        Updates single product parameters with the given product id.
        """

        # If a batch update is needed, you need to create a batch_update function.
        # This function leaves a performance hit for batch update using for loops on a list of Products.
        # I kept this function as it is because the ui is only used to update a single item at a time.

        if purchase.id is None:
            logger.warning("Cannot process transaction without a Purchase ID.")
            return False

        try:
            with self.db.session as s:
                merged_purchase = s.merge(purchase)
                s.commit()
                logger.info(msg=f"Updated product values with id {merged_purchase.id}.")
                return True
        except IntegrityError as err:
            logger.warning(err)
            return False
        except OperationalError as err:
            logger.critical(err)
            return False

    @override
    def delete(self, product_id: int) -> bool:
        """
        Deletes a purchase with the given ID.
        """

        try:
            with self.db.session as s:
                stmt = delete(Purchase).where(Purchase.id == product_id)
                s.execute(stmt)
                s.commit()
                logger.info(f"Deleted purchase with id {product_id}.")
                return True
        except IntegrityError as err:
            logger.warning(err)
            return False
        except OperationalError as err:
            logger.critical(err)
            return False

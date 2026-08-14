from datetime import datetime
from typing import override

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, OperationalError

from app.models import Product
from app.utils import LogHandler

from .repository import Repository

logger = LogHandler.logger(__name__)


class ProductRepository(Repository):
    """
    Class for querying the products table.
    """

    @override
    def add(self, products: list[Product]) -> bool:
        """
        Adds an item/list of items to the database.
        """
        try:
            with self.db.session as s:
                s.add_all(products)
                s.commit()
                logger.info(msg=f"Added {len(products)} objects to the database")
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
        manufacturer: str | None = None,
        name: str | None = None,
        packaging: str | None = None,
        unit_per_pack: int | float | None = None,
        price_per_unit: int | float | None = None,
        date_added: str | None = None,
        is_available: bool | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        count: int = 0,
    ) -> list[Product]:
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
                stmt = select(Product)
                filters = []

                if id is not None:
                    filters.append(Product.id == id)
                if manufacturer is not None:
                    filters.append(Product.manufacturer.ilike(f"%{manufacturer}%"))
                if name is not None:
                    filters.append(Product.name.ilike(f"%{name}%"))
                if packaging is not None:
                    filters.append(Product.packaging.ilike(f"%{packaging}%"))
                if unit_per_pack is not None:
                    filters.append(Product.unit_per_pack == unit_per_pack)
                if price_per_unit is not None:
                    filters.append(Product.price_per_unit == price_per_unit)
                if date_added is not None:
                    filters.append(Product.date_added == date_added)
                if is_available is not None:
                    filters.append(Product.is_available == is_available)

                if date_from is not None:
                    filters.append(Product.date_added >= date_from)
                if date_to is not None:
                    filters.append(Product.date_added <= date_to)

                if filters:
                    stmt = stmt.where(*filters)

                stmt = stmt.order_by(Product.id)
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
    def update(self, product: Product) -> bool:
        """ "
        Updates single product parameters with the given product id.
        """

        # If a batch update is needed, you need to create a batch_update function.
        # This function leaves a performance hit for batch update using for loops on a list of Products.
        # I kept this function as it is because the ui is only used to update a single item at a time.

        if product.id is None:
            logger.warning("Cannot process transaction without a Product ID.")
            return False

        try:
            with self.db.session as s:
                merged_product = s.merge(product)
                s.commit()
                logger.info(msg=f"Updated product values with id {merged_product.id}.")
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
        Disables a product with the given ID.

        Disabling is preferred over permanent deletion in case of cascading domino effects.
        """

        try:
            with self.db.session as s:
                stmt = (
                    update(Product)
                    .where(Product.id == product_id)
                    .values(is_available=False)
                )
                s.execute(stmt)
                s.commit()
                logger.info(f"Updated product availability with id {product_id}.")
                return True
        except IntegrityError as err:
            logger.warning(err)
            return False
        except OperationalError as err:
            logger.critical(err)
            return False

from pathlib import Path
import pandas as pd


class Olist:
    """
    The Olist class provides methods to interact with Olist's e-commerce data.
    """

    def get_data(self):
        """
        Loads Olist CSV files from ~/.workintech/olist/data/csv and returns them as a dict of DataFrames.
        Keys are short dataset names (e.g. 'orders', 'order_items', 'sellers', ...).
        """

        data_dir = Path.home() / ".workintech" / "olist" / "data" / "csv"

        files = {
            "customers": "olist_customers_dataset.csv",
            "geolocation": "olist_geolocation_dataset.csv",
            "order_items": "olist_order_items_dataset.csv",
            "order_payments": "olist_order_payments_dataset.csv",
            "order_reviews": "olist_order_reviews_dataset.csv",
            "orders": "olist_orders_dataset.csv",
            "products": "olist_products_dataset.csv",
            "sellers": "olist_sellers_dataset.csv",
            "product_category_name_translation": "product_category_name_translation.csv",
        }

        data = {}
        for key, filename in files.items():
            path = data_dir / filename
            data[key] = pd.read_csv(path)

        return data

    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")

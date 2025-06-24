import pandas as pd
import os
import logging
from sqlalchemy import create_engine, text

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# --- Config ---
ENGINE_URL = "postgresql://postgres:password@localhost:0000/olist_data"
BASE_PATH = "C:/path.."

TABLES = {
    "olist_customers": {
        "csv": "olist_customers_dataset.csv",
        "create": """
            CREATE TABLE olist_customers (
                customer_id TEXT PRIMARY KEY,
                customer_unique_id TEXT,
                customer_zip_code_prefix TEXT,
                customer_city TEXT,
                customer_state TEXT
            );
        """,
        "dates": [], "pk": "customer_id"
    },
    "olist_geolocation": {
        "csv": "olist_geolocation_dataset.csv",
        "create": """
            CREATE TABLE olist_geolocation (
                geolocation_zip_code_prefix TEXT,
                geolocation_lat FLOAT,
                geolocation_lng FLOAT,
                geolocation_city TEXT,
                geolocation_state TEXT
            );
        """,
        "dates": [], "pk": None
    },
    "olist_order_items": {
        "csv": "olist_order_items_dataset.csv",
        "create": """
            CREATE TABLE olist_order_items (
                order_id TEXT,
                order_item_id INTEGER,
                product_id TEXT,
                seller_id TEXT,
                shipping_limit_date TIMESTAMP,
                price NUMERIC,
                freight_value NUMERIC,
                PRIMARY KEY (order_id, order_item_id)
            );
        """,
        "dates": ["shipping_limit_date"],
        "pk": None
    },
    "olist_orders": {
        "csv": "olist_orders_dataset.csv",
        "create": """
            CREATE TABLE olist_orders (
                order_id TEXT PRIMARY KEY,
                customer_id TEXT,
                order_status TEXT,
                order_purchase_timestamp TIMESTAMP,
                order_approved_at TIMESTAMP,
                order_delivered_carrier_date TIMESTAMP,
                order_delivered_customer_date TIMESTAMP,
                order_estimated_delivery_date TIMESTAMP
            );
        """,
        "dates": [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ],
        "pk": "order_id"
    },
    "olist_order_payments": {
        "csv": "olist_order_payments_dataset.csv",
        "create": """
            CREATE TABLE olist_order_payments (
                order_id TEXT,
                payment_sequential INTEGER,
                payment_type TEXT,
                payment_installments INTEGER,
                payment_value NUMERIC
            );
        """,
        "dates": [], "pk": None
    },
    "olist_order_reviews": {
        "csv": "olist_order_reviews_dataset.csv",
        "create": """
            CREATE TABLE olist_order_reviews (
                review_id TEXT PRIMARY KEY,
                order_id TEXT,
                review_score INTEGER,
                review_comment_title TEXT,
                review_comment_message TEXT,
                review_creation_date DATE,
                review_answer_timestamp TIMESTAMP
            );
        """,
        "dates": ["review_creation_date", "review_answer_timestamp"],
        "pk": "review_id"
    },
    "olist_products": {
        "csv": "olist_products_dataset.csv",
        "create": """
            CREATE TABLE olist_products (
                product_id TEXT PRIMARY KEY,
                product_category_name TEXT,
                product_name_length INTEGER,
                product_description_lenght INTEGER,
                product_photos_qty INTEGER,
                product_weight_g INTEGER,
                product_length_cm INTEGER,
                product_height_cm INTEGER,
                product_width_cm INTEGER
            );
        """,
        "dates": [], "pk": "product_id"
    },
    "olist_sellers": {
        "csv": "olist_sellers_dataset.csv",
        "create": """
            CREATE TABLE olist_sellers (
                seller_id TEXT PRIMARY KEY,
                seller_zip_code_prefix TEXT,
                seller_city TEXT,
                seller_state TEXT
            );
        """,
        "dates": [], "pk": "seller_id"
    },
    "product_category_name_translation": {
        "csv": "product_category_name_translation.csv",
        "create": """
            CREATE TABLE product_category_name_translation (
                product_category_name TEXT PRIMARY KEY,
                product_category_name_english TEXT
            );
        """,
        "dates": [], "pk": "product_category_name"
    },
    "olist_marketing_qualified_leads": {
        "csv": "olist_marketing_qualified_leads_dataset.csv",
        "create": """
            CREATE TABLE olist_marketing_qualified_leads (
                mql_id TEXT PRIMARY KEY,
                first_contact_date DATE,
                landing_page_id TEXT,
                origin TEXT
            );
        """,
        "dates": ["first_contact_date"], "pk": "mql_id"
    },
    "olist_closed_deals": {
        "csv": "olist_closed_deals_dataset.csv",
        "create": """
            CREATE TABLE olist_closed_deals (
                mql_id TEXT PRIMARY KEY,
                seller_id TEXT,
                sdr_id TEXT,
                sr_id TEXT,
                won_date TIMESTAMP,
                business_segment TEXT,
                lead_type TEXT,
                lead_behaviour_profile TEXT,
                has_company TEXT,
                has_gtin TEXT,
                average_stock TEXT,
                business_type TEXT,
                declared_product_catalog_size TEXT,
                declared_monthly_revenue TEXT
            );
        """,
        "dates": ["won_date"], "pk": "mql_id"
    }
}

# --- Main Logic ---
def main():
    engine = create_engine(ENGINE_URL)
    with engine.begin() as conn:
        logging.info("Dropping & recreating all tables")
        for tbl, meta in TABLES.items():
            conn.execute(text(f"DROP TABLE IF EXISTS {tbl} CASCADE"))
            conn.execute(text(meta["create"]))
    logging.info("All tables recreated\n")

    for tbl, meta in TABLES.items():
        path = os.path.join(BASE_PATH, meta["csv"])
        logging.info(f"Processing `{tbl}` from `{path}`")

        if not os.path.isfile(path):
            logging.error(f"File not found: {path}")
            continue

        try:
            df = pd.read_csv(path, parse_dates=meta["dates"])
            df.columns = [c.strip() for c in df.columns]

            pk = meta["pk"]
            if pk and pk in df.columns:
                df = df.dropna(subset=[pk]).drop_duplicates(subset=[pk])

            logging.info(f"{tbl} → {len(df)} rows, {len(df.columns)} columns")
            df.to_sql(tbl, engine, index=False, if_exists="append", method="multi", chunksize=5000)
            logging.info(f"Imported {len(df)} rows into `{tbl}`\n")

        except Exception as e:
            logging.exception(f"Failed `{tbl}`: {e}\n")

if __name__ == "__main__":
    main()

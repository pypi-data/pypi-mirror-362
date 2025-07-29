"""AKShare utils directory."""
import os
from openbb_core.app.utils import get_user_cache_directory

def get_cache_path() -> str:
    """
    Get the path for AKShare cache database.

    Returns:
        str: The path to the AKShare cache database.
    """
    db_dir = f"{get_user_cache_directory()}/akshare"
    db_path = f"{db_dir}/equity.db"

    os.makedirs(db_dir, exist_ok=True)

    return db_path
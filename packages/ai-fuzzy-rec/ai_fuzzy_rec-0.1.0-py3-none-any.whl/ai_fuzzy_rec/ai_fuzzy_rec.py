import sqlite3
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from collections import defaultdict
import itertools
import logging
from datetime import datetime

class FuzzyRecommender:
    """A class for fuzzy logic-based item recommendations from a SQLite database."""
    
    def __init__(
        self,
        db_path,
        table_name='purchases',
        user_col='user_id',
        item_col='item_id',
        fuzzy_weights=(0.2, 0.3, 0.5),
        log_file='recommendations.log',
        enable_logging=True
    ):
        """
        Initialize the recommender with database and fuzzy logic parameters.
        
        Args:
            db_path (str): Path to the SQLite database file.
            table_name (str): Name of the table containing user-item interactions.
            user_col (str): Name of the column for user IDs.
            item_col (str): Name of the column for item IDs.
            fuzzy_weights (tuple): Weights for low, medium, high fuzzy memberships (default: (0.2, 0.3, 0.5)).
            log_file (str): Path to the log file (default: 'recommendations.log').
            enable_logging (bool): Whether to enable logging (default: True).
        """
        self.db_path = db_path
        self.table_name = table_name
        self.user_col = user_col
        self.item_col = item_col
        self.fuzzy_weights = fuzzy_weights
        self.log_file = log_file
        self.enable_logging = enable_logging
        self.conn = None
        self.cursor = None
        self.fuzzy_similarity = None
        
        # Set up logging
        if self.enable_logging:
            logging.basicConfig(
                filename=self.log_file,
                level=logging.INFO,
                format='%(asctime)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        # Connect to database
        self._connect()

    def _connect(self):
        """Connect to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            if self.enable_logging:
                logging.error(f"Database connection failed: {e}")
            raise

    def calculate_fuzzy_item_similarity(self):
        """Calculate fuzzy item similarity based on co-occurrence."""
        try:
            # Load data into a pandas DataFrame
            query = f'SELECT {self.user_col}, {self.item_col} FROM {self.table_name}'
            df = pd.read_sql_query(query, self.conn)
            
            # Check if database is empty
            if df.empty:
                print("Warning: Database is empty. No recommendations possible.")
                if self.enable_logging:
                    logging.warning("Database is empty. No recommendations generated.")
                return defaultdict(lambda: defaultdict(float))
            
            # Create co-occurrence counts
            co_occurrence = defaultdict(lambda: defaultdict(int))
            for user, group in df.groupby(self.user_col):
                items = group[self.item_col].tolist()
                for item1, item2 in itertools.combinations(items, 2):
                    co_occurrence[item1][item2] += 1
                    co_occurrence[item2][item1] += 1
            
            # Normalize co-occurrence to [0, 1] for fuzzy membership
            max_co_occurrence = max(max(counts.values()) for counts in co_occurrence.values()) if co_occurrence else 1
            fuzzy_similarity = defaultdict(lambda: defaultdict(float))
            
            # Define fuzzy membership functions
            x_co = np.arange(0, max_co_occurrence + 1, 1)
            low = fuzz.trimf(x_co, [0, 0, max_co_occurrence / 2])  # Low similarity
            medium = fuzz.trimf(x_co, [0, max_co_occurrence / 2, max_co_occurrence])  # Medium similarity
            high = fuzz.trimf(x_co, [max_co_occurrence / 2, max_co_occurrence, max_co_occurrence])  # High similarity
            
            # Apply fuzzy membership to co-occurrence counts
            for item1 in co_occurrence:
                for item2, count in co_occurrence[item1].items():
                    low_mem = fuzz.interp_membership(x_co, low, count)
                    med_mem = fuzz.interp_membership(x_co, medium, count)
                    high_mem = fuzz.interp_membership(x_co, high, count)
                    # Combine memberships with user-specified weights
                    fuzzy_similarity[item1][item2] = (
                        self.fuzzy_weights[0] * low_mem +
                        self.fuzzy_weights[1] * med_mem +
                        self.fuzzy_weights[2] * high_mem
                    )
            
            self.fuzzy_similarity = fuzzy_similarity
            return fuzzy_similarity
        except sqlite3.Error as e:
            print(f"Error accessing database: {e}")
            if self.enable_logging:
                logging.error(f"Database query failed in calculate_fuzzy_item_similarity: {e}")
            return defaultdict(lambda: defaultdict(float))

    def recommend_items_for_item(self, item_id, top_n=3):
        """Recommend items based on a given item ID."""
        if self.fuzzy_similarity is None:
            self.calculate_fuzzy_item_similarity()
        
        # Check if item_id exists in the database
        query = f'SELECT DISTINCT {self.item_col} FROM {self.table_name} WHERE {self.item_col} = ?'
        self.cursor.execute(query, (item_id,))
        if not self.cursor.fetchone():
            print(f"Error: Item ID {item_id} not found in the database.")
            if self.enable_logging:
                logging.error(f"Item ID {item_id} not found in the database.")
            return []
        
        if item_id not in self.fuzzy_similarity:
            print(f"Warning: No similarity data for item ID {item_id}.")
            if self.enable_logging:
                logging.warning(f"No similarity data for item ID {item_id}.")
            return []
        
        # Sort items by fuzzy similarity score
        recommendations = sorted(
            self.fuzzy_similarity[item_id].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Return top N items with scores
        top_recommendations = recommendations[:top_n]
        if self.enable_logging:
            logging.info(f"Recommendations for item {item_id}: {top_recommendations}")
        return top_recommendations

    def recommend_items_for_user(self, user_id, top_n=3):
        """Recommend items for a user based on their purchased items."""
        if self.fuzzy_similarity is None:
            self.calculate_fuzzy_item_similarity()
        
        # Check if user_id exists in the database
        query = f'SELECT DISTINCT {self.user_col} FROM {self.table_name} WHERE {self.user_col} = ?'
        self.cursor.execute(query, (user_id,))
        if not self.cursor.fetchone():
            print(f"Error: User ID {user_id} not found in the database.")
            if self.enable_logging:
                logging.error(f"User ID {user_id} not found in the database.")
            return []
        
        # Get items the user has already purchased
        try:
            query = f'SELECT {self.item_col} FROM {self.table_name} WHERE {self.user_col} = ?'
            user_items = pd.read_sql_query(query, self.conn, params=(user_id,))[self.item_col].tolist()
        except sqlite3.Error as e:
            print(f"Error querying user purchases: {e}")
            if self.enable_logging:
                logging.error(f"Database query failed for user {user_id}: {e}")
            return []
        
        if not user_items:
            print(f"Warning: User ID {user_id} has no purchases.")
            if self.enable_logging:
                logging.warning(f"User ID {user_id} has no purchases.")
            return []
        
        # Collect recommendations based on all items the user has
        recommendations = defaultdict(float)
        for item in user_items:
            for rec_item, score in self.fuzzy_similarity[item].items():
                if rec_item not in user_items:  # Exclude items already purchased
                    recommendations[rec_item] += score
        
        # Sort recommendations by total fuzzy similarity score
        sorted_recommendations = sorted(
            recommendations.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Return top N items with scores
        top_recommendations = sorted_recommendations[:top_n]
        if self.enable_logging:
            logging.info(f"Recommendations for user {user_id}: {top_recommendations}")
        return top_recommendations

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            if self.enable_logging:
                logging.info("Database connection closed.")

    def __enter__(self):
        """Support context manager for automatic connection handling."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection when exiting context manager."""
        self.close()

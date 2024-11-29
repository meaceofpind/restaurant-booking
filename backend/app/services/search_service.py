from sqlalchemy.orm import Session
from sqlalchemy import String, Text, or_, inspect
from typing import Dict, Any
from sqlalchemy.orm.query import Query
import logging

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self, db: Session, model_class):
        self.db = db
        self.model_class = model_class

    def search(self, filters: Dict[str, Any], page: int = 1, page_size: int = 10):
        # Start with the base query for the provided model
        query = self.db.query(self.model_class)

        # Loop through the filters to dynamically apply them
        for field, value in filters.items():
            if hasattr(self.model_class, field):  # Check if the model has this field
                column = getattr(self.model_class, field)
                if isinstance(value, str):  # Handle LIKE functionality for text fields
                    query = query.filter(column.ilike(f"%{value}%"))
                elif isinstance(value, dict):  # Handle numeric range filters (e.g., rating, cost_for_two)
                    if 'min' in value and 'max' in value:
                        query = query.filter(column >= value['min'], column <= value['max'])
                    elif 'min' in value:  # Handle only min value filter
                        query = query.filter(column >= value['min'])
                    elif 'max' in value:  # Handle only max value filter
                        query = query.filter(column <= value['max'])

        # Plain text search across multiple fields
        if "plain_text" in filters:
            plain_text = filters["plain_text"]
            query = query.filter(
                or_(
                    *[column.ilike(f"%{plain_text}%") for column in self.get_text_columns()]
                )
            )


        # Sorting by rating descending (you can change this based on your needs)
        query = query.order_by(self.get_sort_column().desc())

        # Pagination
        query = query.offset((page - 1) * page_size).limit(page_size)

        # Execute the query and return results
        return query.all()

    def get_text_columns(self):
        """Returns a list of text-based columns to support the plain_text search"""
        return [
        column for column in inspect(self.model_class).columns.values()
        if isinstance(column.type, (String, Text))
    ]

    def get_sort_column(self):
        """Returns the column to sort by (e.g., rating in descending order)"""
        return getattr(self.model_class, 'rating', None)

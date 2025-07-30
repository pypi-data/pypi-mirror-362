"""
Basic models
"""
from pydantic import BaseModel


class BaseQuery(BaseModel):
    """
    basic query with nothing
    """


class PageQuery(BaseQuery):
    """
    basic pageable query
    """
    page: int = 1
    limit: int = 20

    def setPageable(self, flag):
        if not flag:
            self.page = -1
            self.limit = -1

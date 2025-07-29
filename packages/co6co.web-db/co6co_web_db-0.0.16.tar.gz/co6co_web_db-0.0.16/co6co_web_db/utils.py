from co6co_sanic_ext.utils import JSON_util
from typing import Any 
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.engine.result import ChunkedIteratorResult

class DbJSONEncoder(JSON_util):
    def default(self, obj: Any) -> Any: 
        result=super().default(obj)
        if result!=None:return result
        return None
'''
        if isinstance(obj, RowMapping): 
            result =[a  for a in  obj] 
            return result.__dict__ 
        if isinstance(obj, ChunkedIteratorResult): 
            result =[dict(zip(a._fields,a))  for a in  obj] 
            return result.__dict__  
        return None'''
    
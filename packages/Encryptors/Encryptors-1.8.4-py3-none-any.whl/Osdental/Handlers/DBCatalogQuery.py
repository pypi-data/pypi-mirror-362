from typing import Dict
from Osdental.Handlers.Instances import db_catalog
from Osdental.Models.Catalog import Catalog

class DBCatalogQuery:
    
    @staticmethod
    async def get_catalog_data(catalog_name:str) -> Dict[str,str]:
        rows = await db_catalog.execute_query_return_data('EXEC CATALOG.sps_GetCatalogByName @i_nameCatalog = :catalog_name', {'catalog_name': catalog_name})
        items = [Catalog.from_db(row) for row in rows if row.get('value')]
        return {item.code: item.value for item in items if item.value is not None}
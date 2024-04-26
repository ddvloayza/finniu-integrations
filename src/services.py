from .db import FinniuDB
from .queries import query_contract_update, query_get_pre_investments, query_create_disable_preinvestment
from decimal import Decimal
from datetime import datetime
import uuid


class ContractUpdate:

    @classmethod
    def execute(cls, contract_uuid, file_url):
        db = FinniuDB()
        db.update(query_contract_update(contract_uuid, file_url))
        db.close()


class PreInvestment:

    @classmethod
    def execute(cls, status, limit):
        db = FinniuDB()
        __pre_investment = db.get_list(query_get_pre_investments(status, limit))
        print("__pre_investment", __pre_investment)
        values = []
        for row in __pre_investment:
            row_values = []
            row_values.append(f"'{uuid.uuid4()}'")
            for value in row.values():
                if isinstance(value, Decimal):
                    value = str(value)
                elif isinstance(value, datetime):
                    value = f"'{value.strftime('%Y-%m-%d %H:%M:%S.%f')}'"
                elif isinstance(value, int):
                    value = str(value)
                elif value is None:
                    value = 'NULL'
                elif isinstance(value, str):
                    value = f"'{value}'"
                row_values.append(value)
            row_values.append(f"'{True}'")

            values.append(f"({', '.join(row_values)})")
        db.insert(query_create_disable_preinvestment(values))
        db.close()

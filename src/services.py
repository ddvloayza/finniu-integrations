from .db import FinniuDB
from .investment.queries import query_create_investment, query_get_last_investments
from .queries import (
    query_contract_update,
    query_get_pre_investments,
    query_create_disable_preinvestment, query_get_list_pre_investments
)
from decimal import Decimal
from datetime import datetime
import uuid

from .re_investment.queries import query_get_re_investments, query_activate_pre_investment, \
    query_update_is_active_re_investment


class ContractUpdate:

    @classmethod
    def execute(cls, contract_uuid, file_url):
        db = FinniuDB()
        db.update(query_contract_update(contract_uuid, file_url))
        db.close()

class Investment:
    @classmethod
    def execute_create_investment(cls, uuid, operation_code, pre_investment_id, start_investment, end_investment, created_at):
        db = FinniuDB()
        db.insert(
            query_create_investment(
                uuid,
                operation_code,
                pre_investment_id,
                start_investment,
                end_investment,
                created_at
            )
        )
        db.close()

    @classmethod
    def execute_get_last_investments(cls, limit):
        db = FinniuDB()
        __investments = db.get_list(query_get_last_investments(limit))
        db.close()
        return __investments

class Reinvestment:
    @classmethod
    def execute_get_end_reinvestment(cls, limit):
        db = FinniuDB()
        __re_investments = db.get_list(query_get_re_investments(limit))
        db.close()
        return __re_investments

    @classmethod
    def execute_update_active_re_investment(cls, uuid, is_active):
        db = FinniuDB()
        db.update(query_update_is_active_re_investment(uuid, is_active))
        db.close()
        return 'a'

    @classmethod
    def execute_activate_pre_investment(cls, uuid):
        db = FinniuDB()
        __activate = db.update(query_activate_pre_investment(uuid))
        db.close()

class PreInvestment:

    @classmethod
    def execute_get_pre_investment(cls, status, limit):
        db = FinniuDB()
        __pre_investment = db.get_list(query_get_pre_investments(status, limit))
        db.close()
        return __pre_investment

    @classmethod
    def execute_get_list_pre_investment(cls, uuid_list):
        db = FinniuDB()
        uuid_str = ', '.join(f"'{uuid}'" for uuid in uuid_list)
        __list_pre_investment = db.get_list(query_get_list_pre_investments(uuid_str))
        db.close()
        return __list_pre_investment

    @classmethod
    def execute(cls, status, limit):
        db = FinniuDB()
        __pre_investment = db.get_list(query_get_pre_investments(status, limit))
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

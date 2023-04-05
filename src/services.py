from .db import FinniuDB
from .queries import query_contract_update


class ContractUpdate:

    @classmethod
    def execute(cls, contract_uuid, file_url):
        db = FinniuDB()
        db.update(query_contract_update(contract_uuid, file_url))
        db.close()
def query_contract_update(uuid, contract):
    return f"""
        UPDATE investment_preinvestment
        SET contract = '{contract}'
        WHERE investment_preinvestment.uuid = '{uuid}'
    """
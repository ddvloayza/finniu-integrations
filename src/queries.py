def query_contract_update(uuid, contract):
    return f"""
        UPDATE investment_preinvestment
        SET contract = '{contract}'
        WHERE investment_preinvestment.uuid = '{uuid}'
    """


def query_get_pre_investments(status, limit):
    return f"""
        SELECT 
            investment_preinvestment.user_id,
            investment_preinvestment.plan_id,
            investment_preinvestment.amount,
            investment_preinvestment.deadline_id,
            investment_preinvestment.coupon_id,
            investment_preinvestment.currency,
            investment_preinvestment.created_at
        FROM investment_preinvestment
        WHERE investment_preinvestment.status = '{status}'
        LIMIT {limit}
    """

def query_create_disable_preinvestment(
        data
):
    return f"""
        INSERT INTO investment_disablepreinvestment (
            uuid,
            user_id,
            plan_id,
            amount,
            deadline_id,
            coupon_id,
            currency,
            date_to_create_pre_investment,
            is_active
        ) VALUES {', '.join(data)}
    """
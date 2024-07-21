def query_create_investment(
    uuid,
    operation_code,
    pre_investment_id,
    start_investment,
    end_investment,
    created_at,
):
    return f"""
        INSERT INTO investment_investment (
            uuid,
            approved_by_id,
            operation_code,
            pre_investment_id,
            start_investment,
            end_investment,
            created_at,
            is_deleted,
            is_active
        ) VALUES (
            '{uuid}',
            1,
            '{operation_code}',
            '{pre_investment_id}',
            '{start_investment}',
            '{end_investment}',
            '{created_at}',
            FALSE,
            TRUE
        )
    """


def query_get_last_investments(limit):
    return f"""
        SELECT operation_code
        FROM investment_investment
        ORDER BY created_at DESC
        LIMIT {limit};
    """



def query_get_re_investments(limit):
    return f"""
        SELECT 
            investment_reinvestment.uuid,
            investment_reinvestment.new_pre_investment_id,
            investment_reinvestment.old_pre_investment_id,
            investment_reinvestment.start_re_investment,
            investment_reinvestment.end_re_investment
        FROM investment_reinvestment
        JOIN investment_preinvestment ON investment_reinvestment.old_pre_investment_id = investment_preinvestment.uuid
        WHERE investment_reinvestment.is_active = FALSE
            AND investment_reinvestment.start_re_investment <= CURRENT_DATE
            AND investment_preinvestment.action_status = 're_inversion_activada'
        LIMIT {limit}
    """

def query_update_is_active_re_investment(uuid, is_active):
    return f"""
        UPDATE investment_reinvestment
        SET is_active = '{is_active}'
        WHERE investment_reinvestment.uuid = '{uuid}'
    """

def query_activate_pre_investment(uuid):
    return f"""
        UPDATE investment_preinvestment
        SET status = 'active'
        WHERE investment_preinvestment.uuid = '{uuid}'
        AND investment_preinvestment.is_active = TRUE
    """
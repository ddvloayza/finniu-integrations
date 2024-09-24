def query_get_re_investments(limit):
    return f"""
        SELECT 
            investment_reinvestment.uuid,
            investment_reinvestment.new_pre_investment_id,
            investment_reinvestment.old_pre_investment_id,
            investment_reinvestment.start_re_investment,
            investment_reinvestment.end_re_investment,
            "deadline"."value" AS "value"
        FROM investment_reinvestment
        LEFT JOIN investment_preinvestment AS "New Pre Investment" ON investment_reinvestment.new_pre_investment_id = "New Pre Investment"."uuid"
            LEFT JOIN investment_preinvestment AS "Old Pre Investment" ON investment_reinvestment.old_pre_investment_id = "Old Pre Investment"."uuid"
                LEFT JOIN onboarding_deadline AS "deadline" ON "New Pre Investment".deadline_id = "deadline"."uuid"
        WHERE investment_reinvestment.is_active = FALSE
            AND "New Pre Investment".status == 'pending'
            AND investment_reinvestment.start_re_investment <= CURRENT_DATE
            AND "Old Pre Investment"."action_status" = 're_inversion_activada'
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
        SET status = 'active', is_investment = TRUE
        WHERE investment_preinvestment.uuid = '{uuid}'
        AND investment_preinvestment.is_active = TRUE
    """

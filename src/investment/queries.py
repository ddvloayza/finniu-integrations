from datetime import date, timedelta
def query_create_investment(
    uuid,
    operation_code,
    pre_investment_id,
    start_investment,
    end_investment,
    payment_capital,
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
            payment_capital,
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
            '{payment_capital}',
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


def query_get_finish_investments(limit, days_until_end):
    """
        query_get_finish_investments(1, 100)
        query_get_finish_investments(3, 100)
        query_get_finish_investments(5, 100)
    """
    target_date = date.today() + timedelta(days=days_until_end)
    print("target_date", target_date)
    return f"""
        SELECT
          "public"."investment_investment"."end_investment" AS "end_investment",
          "public"."investment_investment"."start_investment" AS "start_investment",
          "public"."investment_investment"."operation_code" AS "operation_code",
          "public"."investment_investment"."payment_capital" AS "payment_capital",
          "pre_investment"."amount" AS "pre_investment__amount",
          "pre_investment"."deadline_id" AS "pre_investment__deadline_id",
          "pre_investment"."coupon_id" AS "pre_investment__coupon_id",
          "pre_investment"."currency" AS "pre_investment__currency",
          "custom_user"."email" AS "custom_user__email",
          "user_profile"."first_name" AS "user_profile__first_name",
          "user_profile"."last_name" AS "user_profile__last_name",
          "coupon"."code" AS "coupon__code",
          "coupon"."discount_percent" AS "coupon__discount_percent",
          "deadline"."value" AS "deadline__value",
          "plan"."twelve_months_return" AS "plan__twelve_months_return",
          "plan"."six_months_return" AS "plan__six_months_return",
          "plan"."return_forty_eight_months" AS "plan__return_forty_eight_months",
          "plan"."return_thirty_six_months" AS "plan__return_thirty_six_months",
          "plan"."return_twenty_four_months" AS "plan__return_twenty_four_months",
          "plan"."value" AS "plan__value",
          CASE
            WHEN "deadline"."value" = 6 THEN "plan"."six_months_return"
            WHEN "deadline"."value" = 12 THEN "plan"."twelve_months_return"
            WHEN "deadline"."value" = 24 THEN "plan"."return_twenty_four_months"
            ELSE 0
          END + COALESCE("coupon"."discount_percent", 0) AS "percentage",
          '{days_until_end}' AS "days_until_end"
        FROM
          "public"."investment_investment"
        LEFT JOIN "public"."investment_preinvestment" AS "pre_investment" ON "public"."investment_investment"."pre_investment_id" = "pre_investment"."uuid"
        LEFT JOIN "public"."customuser_customuser" AS "custom_user" ON "pre_investment"."user_id" = "custom_user"."id"
        LEFT JOIN "public"."customuser_userprofile" AS "user_profile" ON "custom_user"."id" = "user_profile"."user_id"
        LEFT JOIN "public"."investment_coupon" AS "coupon" ON "pre_investment"."coupon_id" = "coupon"."uuid"
        LEFT JOIN "public"."onboarding_deadline" AS "deadline" ON "pre_investment"."deadline_id" = "deadline"."uuid"
        LEFT JOIN "public"."onboarding_plan" AS "plan" ON "pre_investment"."plan_id" = "plan"."uuid"
        WHERE
          DATE("public"."investment_investment"."end_investment") = '{target_date}'
          AND "pre_investment"."action_status" = 're_inversion_default'
        LIMIT {limit};
    """

def query_get_closed_investments(limit):
    """
        query_get_finish_investments(1, 100)
        query_get_finish_investments(3, 100)
        query_get_finish_investments(5, 100)
    """
    return f"""
        SELECT
          "public"."investment_investment"."payment_capital" AS "payment_capital",
          "public"."investment_investment"."start_investment" AS "start_investment",
          "public"."investment_investment"."operation_code" AS "operation_code",
          "public"."investment_investment"."payment_capital" AS "payment_capital",
          "pre_investment"."uuid" AS "pre_investment__uuid",
          "pre_investment"."amount" AS "pre_investment__amount",
          "pre_investment"."deadline_id" AS "pre_investment__deadline_id",
          "pre_investment"."coupon_id" AS "pre_investment__coupon_id",
          "pre_investment"."currency" AS "pre_investment__currency",
          "custom_user"."email" AS "custom_user__email",
          "user_profile"."first_name" AS "user_profile__first_name",
          "user_profile"."last_name" AS "user_profile__last_name",
          "coupon"."code" AS "coupon__code",
          "coupon"."discount_percent" AS "coupon__discount_percent",
          "deadline"."value" AS "deadline__value",
          "plan"."twelve_months_return" AS "plan__twelve_months_return",
          "plan"."six_months_return" AS "plan__six_months_return",
          "plan"."return_forty_eight_months" AS "plan__return_forty_eight_months",
          "plan"."return_thirty_six_months" AS "plan__return_thirty_six_months",
          "plan"."return_twenty_four_months" AS "plan__return_twenty_four_months",
          "plan"."value" AS "plan__value",
          CASE
            WHEN "deadline"."value" = 6 THEN "plan"."six_months_return"
            WHEN "deadline"."value" = 12 THEN "plan"."twelve_months_return"
            WHEN "deadline"."value" = 24 THEN "plan"."return_twenty_four_months"
            ELSE 0
          END + COALESCE("coupon"."discount_percent", 0) AS "percentage"
        FROM
          "public"."investment_investment"
        LEFT JOIN "public"."investment_preinvestment" AS "pre_investment" ON "public"."investment_investment"."pre_investment_id" = "pre_investment"."uuid"
        LEFT JOIN "public"."customuser_customuser" AS "custom_user" ON "pre_investment"."user_id" = "custom_user"."id"
        LEFT JOIN "public"."customuser_userprofile" AS "user_profile" ON "custom_user"."id" = "user_profile"."user_id"
        LEFT JOIN "public"."investment_coupon" AS "coupon" ON "pre_investment"."coupon_id" = "coupon"."uuid"
        LEFT JOIN "public"."onboarding_deadline" AS "deadline" ON "pre_investment"."deadline_id" = "deadline"."uuid"
        LEFT JOIN "public"."onboarding_plan" AS "plan" ON "pre_investment"."plan_id" = "plan"."uuid"
        WHERE
          DATE("public"."investment_investment"."payment_capital") = CURRENT_DATE
          AND "pre_investment"."action_status" = 're_inversion_default'
          AND "pre_investment"."status" = 'active'
          AND "pre_investment"."is_investment" = True
        LIMIT {limit};
    """

def query_set_status_pre_investment(uuid, status):
    return f"""
        UPDATE investment_preinvestment
        SET status = '{status}'
        WHERE investment_preinvestment.uuid = '{uuid}'
    """
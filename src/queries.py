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
            investment_preinvestment.created_at,
            investment_preinvestment.status
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

def query_get_list_pre_investments(uuid_str):
    print("uuid_str", uuid_str)
    return f"""
        SELECT
          "public"."investment_preinvestment"."uuid" AS "uuid",
          "public"."investment_preinvestment"."created_at" AS "created_at",
          "public"."investment_preinvestment"."updated_at" AS "updated_at",
          "public"."investment_preinvestment"."is_active" AS "is_active",
          "public"."investment_preinvestment"."amount" AS "amount",
          "public"."investment_preinvestment"."is_investment" AS "is_investment",
          "public"."investment_preinvestment"."currency" AS "currency",
          "public"."investment_preinvestment"."operation_code" AS "operation_code",
          "public"."investment_preinvestment"."action_status" AS "action_status",
          "Onboarding Plan - Plan"."value" AS "plan_value",
          "Investment Coupon - Coupon"."discount_percent" AS "coupon_discount",
          "Onboarding Deadline - Deadline"."value" AS "deadline_value",
          "Customuser Customuser - User"."email" AS "email",
          "Customuser Userprofile - User"."first_name" AS "first_name",
          "Customuser Userprofile - User"."last_name" AS "last_name",
          CASE
            WHEN "Onboarding Deadline - Deadline"."value" = 6 THEN "Onboarding Plan - Plan"."six_months_return"
            WHEN "Onboarding Deadline - Deadline"."value" = 12 THEN "Onboarding Plan - Plan"."twelve_months_return"
            WHEN "Onboarding Deadline - Deadline"."value" = 24 THEN "Onboarding Plan - Plan"."return_twenty_four_months"
            WHEN "Onboarding Deadline - Deadline"."value" = 36 THEN "Onboarding Plan - Plan"."return_thirty_six_months"
            WHEN "Onboarding Deadline - Deadline"."value" = 48 THEN "Onboarding Plan - Plan"."return_forty_eight_months"
            ELSE NULL
          END AS "profitability_percent"
        FROM
          "public"."investment_preinvestment"
        LEFT JOIN "public"."onboarding_plan" AS "Onboarding Plan - Plan" ON "public"."investment_preinvestment"."plan_id" = "Onboarding Plan - Plan"."uuid"
        LEFT JOIN "public"."investment_coupon" AS "Investment Coupon - Coupon" ON "public"."investment_preinvestment"."coupon_id" = "Investment Coupon - Coupon"."uuid"
        LEFT JOIN "public"."onboarding_deadline" AS "Onboarding Deadline - Deadline" ON "public"."investment_preinvestment"."deadline_id" = "Onboarding Deadline - Deadline"."uuid"
        LEFT JOIN "public"."customuser_customuser" AS "Customuser Customuser - User" ON "public"."investment_preinvestment"."user_id" = "Customuser Customuser - User"."id"
        LEFT JOIN "public"."customuser_userprofile" AS "Customuser Userprofile - User" ON "public"."investment_preinvestment"."user_id" = "Customuser Userprofile - User"."user_id"
        WHERE investment_preinvestment.uuid IN ({uuid_str});
    """
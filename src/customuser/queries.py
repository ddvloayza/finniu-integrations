

def query_get_users(emails_str, limit):
    return f"""
        SELECT
          "public"."customuser_customuser"."email" AS "email",
          "Customuser Userprofile"."first_name" AS "first_name"
        FROM
          "public"."customuser_customuser"
        LEFT JOIN "public"."customuser_userprofile" AS "Customuser Userprofile" ON "public"."customuser_customuser"."id" = "Customuser Userprofile"."user_id"
        WHERE
          "public"."customuser_customuser"."email" IN ({emails_str})
        LIMIT
          {limit};
    """
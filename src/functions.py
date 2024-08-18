import logging
import uuid
from datetime import datetime, timezone

from src.integrations.sengrid import SendgridMail
from src.services import Investment, PreInvestment, Reinvestment, CustomUser
from src.utils import adjust_date

logger = logging.getLogger()


def draft_pre_investments(event, context):
    success = False
    try:
        list_pre_investments = PreInvestment.execute_get_pre_investment("draft", 10)
        logger.info("list_pre_investments", list_pre_investments)
        success = True
    except Exception as e:
        logger.exception("Failed Lambda ***purge_pre_investments", e)
    return success

def closed_investments(event, context):
    success = False
    try:
        list_investments = Investment.execute_get_closed_investments(
            100
        )
        print("list_investments", list_investments)
        to_emails_fields = []
        for investment in list_investments:
            finish_investment = Investment.execute_change_status_investments(
                investment["pre_investment__uuid"], "finished"
            )
            print("finish_investment", finish_investment)
            currency_symbol = (
                "S/. " if investment["pre_investment__currency"] == "nuevo sol" else "$ "
            )
            mailer_template_data = {
                "email": investment["custom_user__email"],
                "fields": {
                    "full_name": investment["user_profile__first_name"]
                                 + " "
                                 + investment["user_profile__last_name"],
                    "amount": currency_symbol + str(investment["pre_investment__amount"]),
                    "deadline": str(investment["deadline__value"]) + " meses",
                    "investment_start_date": investment["start_investment"].strftime(
                        "%d/%m/%Y"
                    ),
                    "investment_payment_capital_date": investment["payment_capital"].strftime(
                        "%d/%m/%Y"
                    ),
                    "rentability": str(investment["percentage"]),
                },
            }
            to_emails_fields.append(mailer_template_data)
        params = {
            "template_id": "d-8f3d8dd38e864bfeba46a4956a2f2517",
            "subject": "Finalizacion de Inversion",
        }
        init_mails = SendgridMail()
        sender_emails = init_mails.send_email(
            to_emails_fields, params.get("subject"), params.get("template_id")
        )
        print("sender_emails", sender_emails)
        logger.info("list_investments", list_investments)
        success = True
    except Exception as e:
        logger.exception("Failed Lambda ***purge_pre_investments", e)
    return success


def activate_re_investments(event, context):
    success = False
    try:
        list_re_investments = Reinvestment.execute_get_end_reinvestment(100)
        print("list_re_investments", list_re_investments)
        list_new_pre_investments_uuids = []
        to_emails_fields = []
        if list_re_investments:
            for re_investment in list_re_investments:
                Reinvestment.execute_update_active_re_investment(
                    re_investment["uuid"], True
                )
                Reinvestment.execute_activate_pre_investment(
                    re_investment["new_pre_investment_id"]
                )
                __operation_code = Investment.execute_get_last_investments(1)[0][
                    "operation_code"
                ]
                logger.info("***__operation_code", __operation_code)
                prefix = "INV"
                number = int(__operation_code[3:]) + 1
                new_operation_code = f"{prefix}{number:04d}"
                payment_capital = adjust_date(
                    re_investment["value"], re_investment["start_re_investment"]
                )
                print("****payment_capital***", payment_capital)
                Investment.execute_create_investment(
                    str(uuid.uuid4()),
                    new_operation_code,
                    re_investment["new_pre_investment_id"],
                    re_investment["start_re_investment"],
                    re_investment["end_re_investment"],
                    payment_capital,
                    datetime.now(timezone.utc),
                )
                list_new_pre_investments_uuids.append(
                    re_investment["new_pre_investment_id"]
                )
            list_new_pre_investments = PreInvestment.execute_get_list_pre_investment(
                list_new_pre_investments_uuids
            )
            print("list_new_pre_investments", list_new_pre_investments)

            for investment in list_new_pre_investments:
                currency_symbol = (
                    "S/. " if investment["currency"] == "nuevo sol" else "$ "
                )
                mailer_template_data = {
                    "email": "ddvloayza@gmail.com",
                    "fields": {
                        "full_name": investment["first_name"]
                        + " "
                        + investment["last_name"],
                        "amount": currency_symbol + str(investment["amount"]),
                        "deadline": str(investment["deadline_value"]) + " meses",
                        "investment_start_date": datetime.now(timezone.utc).strftime(
                            "%d/%m/%Y"
                        ),
                        "rentability": str(investment["profitability_percent"]),
                        "contract_url": str(investment["contract"]),
                    },
                }
                to_emails_fields.append(mailer_template_data)
        params = {
            "template_id": "d-d543e94efac241f9b3cf317840d48492",
            "subject": "Re Investment Register",
        }
        init_mails = SendgridMail()
        print("to_emails_fields", to_emails_fields)
        sender_emails = init_mails.send_email(
            to_emails_fields, params.get("subject"), params.get("template_id")
        )
        if sender_emails.status_code == 202:
            print("sender_emails.status_code", sender_emails.status_code)
        logger.info("***list_re_investments", list_re_investments)
        success = True
    except Exception as e:
        logger.exception("Failed Lambda ***activate_re_investments", e)
    return success


def send_mail_reinvestment(event, context):
    success = False
    try:

        list_investments_1 = Investment.execute_get_finish_investments(
            100, 1
        )
        list_investments_3 = Investment.execute_get_finish_investments(
            100, 3
        )
        list_investments_5 = Investment.execute_get_finish_investments(
            100, 5
        )
        list_investments = list_investments_1 + list_investments_3 + list_investments_5
        print("list_investments", list_investments)
        to_emails_fields = []
        number = 1
        for investment in list_investments:
            currency_symbol = (
                "S/. " if investment["pre_investment__currency"] == "nuevo sol" else "$ "
            )
            mailer_template_data = {
                "email": investment["custom_user__email"],
                "fields": {
                    "full_name": investment["user_profile__first_name"]
                                 + " "
                                 + investment["user_profile__last_name"],
                    "amount": currency_symbol + str(investment["pre_investment__amount"]),
                    "deadline": str(investment["deadline__value"]) + " meses",
                    "investment_start_date": investment["start_investment"].strftime(
                        "%d/%m/%Y"
                    ),
                    "investment_end_date": investment["end_investment"].strftime(
                        "%d/%m/%Y"
                    ),
                    "rentability": str(investment["percentage"]),
                    "days_remaining": investment["days_until_end"],
                },
            }
            to_emails_fields.append(mailer_template_data)
            number += 1
        params = {
            "template_id": "d-f9d9ccdb4c1641ffb452a68fa8450940",
            "subject": "¡Ya puedes reinvertir!",
        }
        init_mails = SendgridMail()
        sender_emails = init_mails.send_email(
            to_emails_fields, params.get("subject"), params.get("template_id")
        )
        success = True
    except Exception as e:
        print("**ERROR**", str(e))
        logger.info("Error in send_mail", str(e))
    return success


def send_mail_inversionistas(event, context):


    list_emails = ['ddvloayza@gmail.com', 'olenkanajera@gmail.com']
    # no_estan_en_lista_2 = [email for email in list_emails if email not in list_emails2]
    # no_estan_en_lista_1 = [email for email in list_emails2 if email not in list_emails]
    #
    # print("no_estan_en_lista_2", no_estan_en_lista_2)
    # print("no_estan_en_lista_1", no_estan_en_lista_1)
    emails_str = ", ".join([f"'{email}'" for email in list_emails])
    list_users = CustomUser.execute_query_get_users(
        emails_str, 1000
    )
    print("list_users", list_users)
    to_emails_fields = []
    for users in list_users:
        mailer_template_data = {
            "email": users["email"],
            "fields": {
                "full_name": "Olenka Jael Nájera Gálvez",
                "investment_start_date": "09 de Agosto del 2024",
                "amount": "S/. 14,000.00",
                "deadline": "12 meses",
                "rentability": "18"
            },
        }
        to_emails_fields.append(mailer_template_data)


    params = {
        "template_id": "d-d543e94efac241f9b3cf317840d48492",
        "subject": "Finalizacion de Contrato",
    }
    init_mails = SendgridMail()
    sender_emails = init_mails.send_email(
        to_emails_fields, params.get("subject"), params.get("template_id")
    )


# if __name__ == "__main__":
#     event = {}
#     context = {}
#     closed_investments(event, context)

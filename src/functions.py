from src.integrations.sengrid import SendgridMail
from src.services import PreInvestment, Reinvestment, Investment
import logging
import uuid
from datetime import datetime, timezone
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


def activate_re_investments(event, context):
    success = False
    try:
        list_re_investments = Reinvestment.execute_get_end_reinvestment(100)
        print("list_re_investments", list_re_investments)
        list_new_pre_investments_uuids = []
        to_emails_fields = []
        if list_re_investments:
            for re_investment in list_re_investments:
                Reinvestment.execute_update_active_re_investment(re_investment['uuid'], True)
                Reinvestment.execute_activate_pre_investment(re_investment['new_pre_investment_id'])
                __operation_code = Investment.execute_get_last_investments(1)[0]['operation_code']
                logger.info("***__operation_code", __operation_code)
                prefix = "INV"
                number = int(__operation_code[3:]) + 1
                new_operation_code = f"{prefix}{number:04d}"
                Investment.execute_create_investment(
                    str(uuid.uuid4()),
                    new_operation_code,
                    re_investment['new_pre_investment_id'],
                    re_investment['start_re_investment'],
                    re_investment['end_re_investment'],
                    datetime.now(timezone.utc),
                )
                list_new_pre_investments_uuids.append(re_investment['new_pre_investment_id'])
            list_new_pre_investments = PreInvestment.execute_get_list_pre_investment(list_new_pre_investments_uuids)
            print("list_new_pre_investments", list_new_pre_investments)

            for investment in list_new_pre_investments:
                currency_symbol = "S/. " if investment['currency'] == 'nuevo sol' else "$ "
                mailer_template_data = {
                    "email": investment['email'],
                    "fields": {
                        "full_name": investment['first_name'] + " " + investment['last_name'],
                        "amount": currency_symbol + str(investment['amount']),
                        "deadline": str(investment['deadline_value']) + " meses",
                        "investment_start_date": datetime.now(timezone.utc).strftime("%d/%m/%Y"),
                        "rentability": str(investment['profitability_percent']),
                    }
                }
                to_emails_fields.append(mailer_template_data)
        params = {
            "template_id": "d-d543e94efac241f9b3cf317840d48492",
            "subject": "Re Investment Register",
        }
        init_mails = SendgridMail()
        print("to_emails_fields", to_emails_fields)
        sender_emails = init_mails.send_email(to_emails_fields, params.get("subject"), params.get("template_id"))
        if sender_emails.status_code == 202:
            print("sender_emails.status_code", sender_emails.status_code)
        logger.info("***list_re_investments", list_re_investments)
        success = True
    except Exception as e:
        logger.exception("Failed Lambda ***activate_re_investments", e)
    return success

def send_mail_reinvestment(event, context):

    try:
        to_emails_fields = [
            {
                "email": 'ddvloayza@gmail.com',
                "fields": {
                    "full_name": 'Diego De la vega',
                    "plan_name": "plan de prueba",
                    "amount": 1000,
                    "currency": 'Nuevos Soles',
                    "status": 'Pendiente de aprobacion',
                },
            }
        ]
        params = {
            "template_id": "d-9c312be3b63c4677adc48996bde407aa",
            "subject": "Re Investment Register",
        }
        init_mails = SendgridMail()
        sender_emails = init_mails.send_email(to_emails_fields, params.get("subject"), params.get("template_id"))
        if sender_emails.status_code == 202:
            success_send_mail = True
    except Exception as e:
        print("**ERROR**", str(e))
        logger.info("Error in send_mail", str(e))


if __name__ == "__main__":
    event = {}
    context = {}
    activate_re_investments(event, context)

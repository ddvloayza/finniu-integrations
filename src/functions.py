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
        logger.info("***list_re_investments", list_re_investments)
        success = True
    except Exception as e:
        logger.exception("Failed Lambda ***activate_re_investments", e)
    return success


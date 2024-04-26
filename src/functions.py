from src.services import PreInvestment
import logging
logger = logging.getLogger()


def purge_pre_investments(event, context):
    success = False
    print("entro")
    try:
        list_pre_investments = PreInvestment.execute("draft", 5)
        logger.info("list_pre_investments", list_pre_investments)
        success = True
    except Exception as e:
        logger.exception("Failed Lambda ***purge_pre_investments", e)
    return success

import json
from datetime import datetime


def handler(event, context):
    current_time = datetime.now().isoformat()
    print(f"The current time is {current_time}")
    return {
        'statusCode': 200,
        'body': json.dumps(f"The current time is {current_time}")
    }


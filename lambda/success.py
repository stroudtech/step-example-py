import json

def handler(event, context):
    print(f"event: {json.dumps(event)}")
    return event
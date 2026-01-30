from pymongo.errors import DuplicateKeyError

def insert_if_new(event_data, collection):
    try:
        collection.insert_one(event_data)
        return True
    except DuplicateKeyError:
        print(f"Duplicate ignored: {event_data['request_id']}")
        return False
    except Exception as e:
        print(f"Insert error: {e}")
        return False

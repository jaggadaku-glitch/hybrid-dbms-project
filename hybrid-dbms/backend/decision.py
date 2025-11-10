KNOWN_SCHEMA_KEYS = {'name','email','age','price','quantity','category'}

def should_store_in_mongo(payload: dict) -> bool:
    if payload.get('has_file'):
        return True
    text = payload.get('text') or ''
    if isinstance(text, str) and len(text) > 200:
        return True
    data_keys = set((payload.get('data') or {}).keys())
    if len(data_keys) > 0 and not (data_keys & KNOWN_SCHEMA_KEYS):
        return True
    return False

async def simplify_discharge(bundle: dict) -> dict:
    return {"simplified": f"Simplified version of discharge for {bundle.get('entry', [{}])[0].get('resource', {}).get('id', 'unknown')}"}

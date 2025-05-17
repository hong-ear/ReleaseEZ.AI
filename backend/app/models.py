from pydantic import BaseModel
from typing import List

class FHIRBundle(BaseModel):
    resourceType: str
    type: str
    entry: List[dict]
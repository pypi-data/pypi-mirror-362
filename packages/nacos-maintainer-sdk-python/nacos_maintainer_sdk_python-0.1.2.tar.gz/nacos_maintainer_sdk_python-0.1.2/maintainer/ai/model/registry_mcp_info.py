from typing import Optional

from pydantic import BaseModel


class Repository(BaseModel):
	pass

class ServerVersionDetail(BaseModel):
	version: Optional[str]=None
	release_date: Optional[str]=None
	is_latest: Optional[bool]=None
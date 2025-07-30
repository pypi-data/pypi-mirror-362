
from pydantic import BaseModel


class PageModel(BaseModel):
    uri: str
    host: str
    subdomain: str
    domain: str
    path: str
    dirs: list[str]
    node: str
    name: str
    root: str
    perms: list[str]
    perms_ext: list[str]


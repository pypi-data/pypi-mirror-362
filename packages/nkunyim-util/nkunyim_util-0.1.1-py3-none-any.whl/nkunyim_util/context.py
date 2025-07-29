from django.http import HttpRequest

from nkunyim_util.models.context_model import ContextModel
from nkunyim_util.services.context_service import ContextService


class Context:
    
    def __init__(self, req: HttpRequest) -> None:
        service = ContextService(req=req)
        self.model = service.create()
        
        
    def get(self) -> ContextModel:
        return self.model
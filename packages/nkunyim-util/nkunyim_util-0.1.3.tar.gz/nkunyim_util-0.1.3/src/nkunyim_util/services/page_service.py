from django.http import HttpRequest

from nkunyim_util.models.page_model import PageModel


class PageService:
    
    def __init__(self, req: HttpRequest) -> None:
        self.req = req
        
        
    def get(self) -> PageModel:      
        uri = self.req.build_absolute_uri()
        host = self.req.get_host()
        host_parts = host.lower().split('.')
        subdomain = host_parts[-3] if len(host_parts) > 2 else "www"
        domain = f"{host_parts[-2]}.{host_parts[-1]}"
        path = self.req.path.lower()
        dirs = path.strip('/').split('/') if path.strip('/') else ['/']
        node = dirs[-1] if dirs else "index"

        data = {
            "uri": uri,
            'host': host,
            'subdomain': subdomain,
            'domain': domain,
            'root': f"{subdomain}.{domain}",
            "path": path,
            "dirs": dirs,
            "node": node,
            "name": f"{node.title()}Page"
        }
        
        return PageModel(**data)
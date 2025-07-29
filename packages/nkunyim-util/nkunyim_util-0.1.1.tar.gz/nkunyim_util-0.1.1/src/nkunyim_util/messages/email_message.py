from typing import Union
from django.core.mail import EmailMultiAlternatives


class EmailMessage(object):
    
    def compose(self, from_email: str, to_emails:list[str], subject: str, body: str) -> None:
        self.from_email = from_email
        self.to_emails = to_emails
        self.subject = subject
        self.body = body
        self.cc: Union[list[str], None] = None
        self.bcc: Union[list[str], None] = None
        self.attachments = []
        self.html = None
        
    def add_cc(self, cc_address: str) -> None:
        if not self.cc:
            self.cc = []
        self.cc.append(cc_address)
        
    def add_bc(self, bc_address: str) -> None:
        if not self.bcc:
            self.bcc = []
        self.bcc.append(bc_address)
        
    def add_html(self, html: str) -> None:
        self.html = html
        
    def add_attachment(self, attachment: str) -> None:
        self.attachments.append(attachment)
        
    def send(self) -> None:
        email = EmailMultiAlternatives(
            subject=self.subject,
            body=self.body,
            from_email=self.from_email,
            to=self.to_emails
        )
        if self.cc:
            email.cc = self.cc
            
        if self.attachments:
            email.attachments = self.attachments
            
        if self.bcc:
            email.bcc = self.bcc
            
        if self.html:
            email.attach_alternative(content=self.html, mimetype='text/html')
            
        email.send()
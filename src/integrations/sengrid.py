import base64
import logging
import mimetypes
import os
from typing import List, Optional

import sendgrid

logger = logging.getLogger(__name__)


class SendgridMail:
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])
        print("self.sg ", os.environ["SENDGRID_API_KEY"])
        self.DEFAULT_FROM_EMAIL = "hola@finniu.com"
        self.DEFAULT_FROM_NAME = "Finniu App"

    @classmethod
    def build_email(cls, email):
        return {"email": email}

    @classmethod
    def build_fields(cls, fields):
        return {f"{k}": v for k, v in fields.items()}

    @classmethod
    def get_attachment_content(cls, filename):
        with open(filename, "rb") as f:
            data = f.read()
            f.close()
        return base64.b64encode(data).decode()

    @classmethod
    def get_attachment_basename(cls, filename):
        return os.path.basename(filename)

    @classmethod
    def get_attachment_file_type(cls, basename):
        return mimetypes.guess_type(basename)[0]

    @classmethod
    def build_attachment(cls, filename):
        basename = cls.get_attachment_basename(filename)
        return {
            "content": cls.get_attachment_content(filename),
            "content_id": basename,
            "disposition": "attachment",
            "filename": basename,
            "name": basename,
            "type": cls.get_attachment_file_type(basename),
        }

    @classmethod
    def build_to_emails(cls, emails):
        to_emails = []
        for x in emails:
            to_emails.append({"to": [{"email": x}]})
        return to_emails

    @classmethod
    def build_personalization(cls, personalizations, subject, is_field):
        p = []
        for x in personalizations:
            y = {"to": [cls.build_email(x["email"])]}
            if x.get("fields") and is_field:
                y["dynamic_template_data"] = cls.build_fields(x["fields"])
                y["dynamic_template_data"].update({"subject": subject})
            p.append(y)
        return p

    @classmethod
    def create_attach_content_id(cls, filename):
        return os.path.basename(filename)

    @classmethod
    def send_email(
        cls,
        to_emails_fields: List,
        subject: str,
        template_id: Optional[id] = None,
        content: Optional[str] = "",
        cc_emails: Optional[List] = [],
        attachments: Optional[List] = [],
    ):
        """
        Parameters
        ______

        to_emails_fields:: [List]
            {email: "user email", "fields": "if has template id, you can use fields}
        content:: [str]
            if you use content, you shouldn't use template_id

        Example input
        ------
        to_emails_fields=[
            {"email": "email123@gmail.com", "fields": {"nombre": "juan"}},
            {"email": "email321@hotmail.com", "fields": {"nombre": "jhon"}}
        ]
        subject="subject prueba"
        template_id="ffc00240-d668-4809-8856-316e74cd3218"
        attachments=[
            "/www/media/test/images/customuser/cdafc73b/7102ca7f.jpeg",
            "/www/media/test/images/customuser/f97949ba/80376401.jpeg",
        ]
        content="prueba content

        Return
        _____
        response::
            response.status_code
            response.body
            response.headers
        """
        data = {
            "personalizations": cls.build_personalization(
                to_emails_fields, subject, is_field=bool(template_id)
            ),
            "from": {
                "email": cls().DEFAULT_FROM_EMAIL,
                "name": cls().DEFAULT_FROM_NAME,
            },
            "subject": subject,
        }
        print("data", data)
        if template_id:
            data["template_id"] = template_id
        else:
            data["content"] = [{"type": "text/plain", "value": content}]
        if cc_emails:
            data["cc"] = [cls.build_email(x) for x in cc_emails]
        if attachments:
            data["attachments"] = [
                cls.build_attachment(path_filename) for path_filename in attachments
            ]
        response = cls().sg.client.mail.send.post(request_body=data)
        print("response", response)
        return response

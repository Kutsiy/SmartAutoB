from fastapi_mail import NameEmail, ConnectionConfig, MessageSchema, FastMail, MessageType
from pydantic import BaseModel
from config import MAIL_PASSWORD, MAIL_USERNAME, MAIL_FROM
from starlette.responses import JSONResponse
from fastapi import HTTPException, status

class EmailSchema(BaseModel):
    email: list[NameEmail]

config = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT = 587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


async def send_email(email: EmailSchema, code: str):
    try:
        html = f"""
            <p>Yor code is {code}</p> 
        """

        message = MessageSchema(
            subject="Fastapi-Mail module",
            recipients=email.dict().get("email"),
            body=html,
            subtype=MessageType.html)

        fm = FastMail(config)
        await fm.send_message(message)
    except Exception:
        raise HTTPException(detail="Error in email service", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
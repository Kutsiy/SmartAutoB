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


def generate_html_for_mail(code):
    return f"""
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background-color:#f4f4f7;font-family:Arial,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 0;background:#f4f4f7;">
<tr>
<td align="center">

<table width="420" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;padding:30px;">
    
<tr>
<td align="center" style="font-size:22px;font-weight:bold;color:#333;">
Verification Code
</td>
</tr>

<tr>
<td align="center" style="padding-top:15px;color:#555;font-size:14px;">
Use the code below to complete your action
</td>
</tr>

<tr>
<td align="center" style="padding:25px 0;">
<span style="
font-size:32px;
font-weight:bold;
letter-spacing:6px;
color:#111;
background:#f2f3f5;
padding:12px 24px;
border-radius:6px;
display:inline-block;
">
{code}
</span>
</td>
</tr>

<tr>
<td align="center" style="font-size:12px;color:#888;padding-top:10px;">
If you didn't request this code, you can safely ignore this email.
</td>
</tr>

</table>

</td>
</tr>
</table>

</body>
</html>
"""


async def send_email(email: EmailSchema, code: str):
    try:
        html = generate_html_for_mail(code)

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
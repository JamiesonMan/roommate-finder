import smtplib
from email.mime.text import MIMEText

#Using a service called 'Mailtrap' to simuate sending/receiving password reset so we're not using real email accounts'
# website in case we need to login: mailtrap.io
#                 email to sign in: dfprpthqxvuintnuqv@ytnhy.com
#                         password: 322Roommateapp!    

def send_reset_email(email, reset_link, username):
    smtp_user = "87ef380e2d8891"
    smtp_pass = "000cef743a6709"

    msg = MIMEText(f"""Hello,\n\n
    To reset your password click the link below.\n In case you forgot your username it is listed below.
    Your username: {username}
    Reset your password using the link below:\n
    {reset_link}""")

    msg['Subject'] = "Roommate Finder Recover Account"
    msg['From'] = "roommatefinderapp@fakeemail.com"
    msg['To'] = email

    with smtplib.SMTP("smtp.mailtrap.io", 587) as server:
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

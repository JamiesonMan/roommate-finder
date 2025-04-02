import smtplib
from email.mime.text import MIMEText

#Using a service called 'Mailtrap' to simuate sending/receiving password reset so we're not using real accounts'
# website in case we need to login: mailtrap.io
#                 email to sign in: dfprpthqxvuintnuqv@ytnhy.com
#                         password: 322Roommateapp!    

def send_reset_email(email, reset_link):
    smtp_user = "87ef380e2d8891"
    smtp_pass = "000cef743a6709"

    msg = MIMEText(f"Hello User,\n\nClick the link below to reset your password:\n{reset_link}\n")

    msg['Subject'] = "Roommate Finder Recover Account"
    msg['From'] = "roommatefinderapp@fakeemail.com"
    msg['To'] = email

    with smtplib.SMTP("smtp.mailtrap.io", 587) as server:
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

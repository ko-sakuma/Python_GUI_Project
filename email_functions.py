import smtplib
import ssl
import certifi
# the package certfi must be installed for email functionality to work


def send_email(receiver_mail, email_body):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "patient.management.ucl@gmail.com"
    sender_pass = "ManicMondays1"

    context = ssl.create_default_context(cafile=certifi.where())

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, receiver_mail, email_body)
    except Exception as e:
        print(e)
    finally:
        server.quit()


if __name__ == '__main__':

    def main():
        # You can test it for yourself by sending this message you your email
        message = """\
           Subject: Hi there

           This message is sent from Python."""

        your_email = ''
        send_email(your_email, message)


    main()

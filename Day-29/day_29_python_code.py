import pywhatkit as kit
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import datetime
import os
import csv
import sys

# === CONFIGURATION ===
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
IMAGE_PATH = "Happy Birthday Minion Watercolor Art – Fun and Lively Birthday Card Idea.jpg"
CSV_FILE = "birthdays.csv"
COUNTRY_CODE = "+91"
SENDER_NAME = "Ashvini Patil"
TODAY = datetime.date.today().strftime("%d-%m")

# === Initialize SMTP Connection ===
def setup_smtp_connection():
    try:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        return smtp
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Check your email or app password.")
        sys.exit()
    except Exception as e:
        print(f"❌ Failed to set up SMTP connection: {e}")
        sys.exit()

# === Construct Email Message with Optional Image or File ===
def construct_email(subject, html_body, image=None, attachment=None):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS

    msg.attach(MIMEText(html_body, 'html'))

    if image:
        images = [image] if isinstance(image, str) else image
        for img in images:
            with open(img, 'rb') as f:
                msg.attach(MIMEImage(f.read(), name=os.path.basename(img)))

    if attachment:
        attachments = [attachment] if isinstance(attachment, str) else attachment
        for file_path in attachments:
            with open(file_path, 'rb') as f:
                file = MIMEApplication(f.read(), name=os.path.basename(file_path))
                file['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                msg.attach(file)

    return msg

# === Email HTML Body ===
def birthday_email_html(name, sender):
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #333;">
        <p>Hey <strong>{name}</strong>,</p>
        <p>Wishing you a day filled with joy, laughter, and love — because someone as wonderful as you deserves nothing less! 🌟🎈</p>
        <p>May this year bring you countless moments of happiness, endless success, and the strength to chase your dreams. Keep shining, smiling, and spreading your light wherever you go. 🌻💪</p>
        <blockquote style="font-style: italic; color: #555;">"Count your life by smiles, not tears. Count your age by friends, not years." – John Lennon</blockquote>
        <p>🎂💖 Happy Birthday once again!<br>May your cake be sweet, your memories sweeter, and your future the sweetest of all. 🎁🎊</p>
        <p>Warmest wishes,<br><strong>{sender}</strong></p>
    </body>
    </html>
    """

# === WhatsApp Message ===
def birthday_whatsapp_message(name, sender):
    return f"""
🎉 Hey {name},

Wishing you a day filled with joy, laughter, and love — because someone as wonderful as you deserves nothing less! 🌟🎈

May this year bring you countless moments of happiness, endless success, and the strength to chase your dreams. Keep shining, smiling, and spreading your light wherever you go. 🌻💪

"Count your life by smiles, not tears. Count your age by friends, not years." – John Lennon

🎂💖 Happy Birthday once again!
May your cake be sweet, your memories sweeter, and your future the sweetest of all. 🎁🎊

Warmest wishes,
{sender}
"""

# === Process CSV and Send Wishes ===
def send_birthday_wishes(file_name):
    smtp = setup_smtp_connection()

    try:
        with open(file_name, mode='r', newline='', encoding='utf-8') as f:
            csv_file = csv.reader(f)
            header = next(csv_file)

            for row in csv_file:
                name, email, phone, birthday = row[0], row[1], row[2], row[3]

                if birthday == TODAY:
                    print(f"🎉 Sending wishes to {name}...")

                    # Send email
                    email_body = birthday_email_html(name, SENDER_NAME)
                    msg = construct_email("🎉✨ A Heartfelt Wish Just for You – Happy Birthday! 🎂💫", email_body, image=IMAGE_PATH)
                    smtp.sendmail(from_addr=EMAIL_ADDRESS, to_addrs=email, msg=msg.as_string())
                    print(f"✅ Email sent to {name}")

                    # Send WhatsApp text
                    kit.sendwhatmsg_instantly(COUNTRY_CODE + phone, birthday_whatsapp_message(name, SENDER_NAME), wait_time=20, tab_close=True)
                    print(f"✅ WhatsApp text sent to {name}")

                    # Send WhatsApp image
                    kit.sendwhats_image(COUNTRY_CODE + phone, IMAGE_PATH, "🎉✨ A Heartfelt Wish Just for You – Happy Birthday! 🎂💫", wait_time=20, tab_close=True)
                    print(f"✅ WhatsApp image sent to {name}\n")

                else:
                    print(f"{name}: 🎂 No birthday today. But it's always a good day to spread joy 😊")

    except FileNotFoundError:
        print("❌ CSV file not found.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        smtp.quit()

# === Run the Script ===
if __name__ == "__main__":
    send_birthday_wishes(CSV_FILE)


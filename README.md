# SmtpMail

The `SmtpMail` class is designed to simplify sending emails through SMTP with support for multiple recipients, HTML or 
plain-text messages and file attachments. This README provides an overview of each method, usage examples, and 
customization instructions.

## Prerequisites

- **Python 3.8+**: Ensure Python 3.8 or higher is installed on your system.

- **Email Provider Configuration**: Obtain SMTP server settings and an application-specific password if necessary 
(e.g., for Gmail accounts with two-factor authentication).

- **Application-Specific Password (if applicable)**: If using an account with two-factor authentication, you may need to 
generate an App Password specifically for this application.

- **Internet Access**: An internet connection is required to connect to the SMTP server and send emails.

- **Install Required Dependencies**: This project only requires Python's standard library. For logging purposes, ensure 
`logging` is configured if you wish to capture errors.

## Example

```python
import os
from dotenv import load_dotenv
from smtpmail import SmtpMessage, SmtpClient

load_dotenv()

# Example usage of SmtpMessage and SmtpClient classes

# Create a message object and set its properties
# Note: The SmtpMessage class is designed to be used with the SmtpClient class for sending emails.
msg = SmtpMessage()
msg.set_date() 
msg.set_from_addr("Your Name <youraddress@gmail.com>") # Or msg['From'] = "Your Name <youraddress@gmail.com>"
msg.set_recipients(["toaddress@gmail.com"], ["ccaddress@gmail.com"], ["bccaddress@gmail.com"])
msg.set_subject("Test Subject")
msg.set_content(text="This is the text content", html="<h1>This is the HTML content</h1>")
msg.add_attachment(["path/to/attachment1", "path/to/attachment2"])
msg.set_message_id(("unique_id", "gmail.com"))
msg.set_list_unsubscribe("https://gmail.com/unsubscribe")
print(msg)

# Send the email using SmtpClient
# Note: The SmtpClient class is designed to be used with the SmtpMessage class for sending emails.
# Make sure to set your environment variables for GMAIL_USERNAME and GMAIL_PASSWORD
username = os.getenv("GMAIL_USERNAME")
password = os.getenv("GMAIL_PASSWORD")
with SmtpClient(username, password, smtp_host="smtp.gmail.com", smtp_port=587) as client:
    client.send_email(msg)
    print("Email sent successfully!")
```
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

## Installation

1. **Clone the Repository**: Clone this repository to your local machine.
   ```bash
   git clone https://github.com/yourusername/smtp-mail.git
   cd smtp-mail
   ```

2. **Install Dependencies**: Install required packages (if any).
   ```bash
   pip install -r requirements.txt
   ```

   *Note*: If the `requirements.txt` file is not provided, this class may not need any external packages beyond Python’s standard library.

3. **Configuration**: Update your `.env` or environment variables with SMTP credentials as needed.

## Initialization

### `__init__`
Initializes the `SmtpMail` object with user credentials and server configuration.

**Parameters:**
- `in_username`: The SMTP server username for authentication.
- `in_password`: The SMTP server password for authentication.
- `in_server` (optional): A tuple containing the SMTP server address and port. Default is set to Gmail 
(`("smtp.gmail.com", 587)`).
- `use_SSL` (optional): Boolean indicating whether to use SSL for the connection. Defaults to `False`, meaning it will use TLS.

**Example Usage:**
```python
from smtpmail import SmtpMail

smtp_client = SmtpMail(
    in_username="username@example.com",
    in_password="password",
    in_server=("smtp.example.com", 587),
    use_SSL=False
)
```

## Methods

### `connect()`
Establishes a connection with the SMTP server, using SSL or TLS based on the `use_SSL` parameter. This method should be called before attempting to send any emails.

**Raises:** `smtplib.SMTPException` if there is an error during the connection.

**Example Usage:**
```python
smtp_client.connect()
```

---

### `disconnect()`
Closes the connection with the SMTP server. This method can be called after sending the email to free up resources or after any issues with the connection.

**Example Usage:**
```python
smtp_client.disconnect()
```

---

### `set_message(subject, from_addr=None, body_text=None, plaintext=None, attachment_paths=None)`
Sets up the email content, including the subject, body, and optional attachments. 

**Parameters:**
- `subject`: Subject of the email.
- `from_addr` (optional): Sender’s email address. If `None`, it defaults to `in_username`.
- `body_text` (optional): Main content of the email, formatted as HTML.
- `plaintext` (optional): Plain text alternative for clients that do not support HTML.
- `attachment_paths` (optional): List of file paths for attachments.

**Example Usage:**
```python
smtp_client.set_message(
    subject="Monthly Report",
    from_addr="User <username@example.com>",
    body_text="<h1>Report</h1><p>Here is your monthly report.</p>",
    plaintext="Here is your monthly report.",
    attachment_paths=["path/to/report.pdf"]
)
```

**Note:** Attachments are checked for existence before being attached. If a file path is invalid, it will print an error message.

---

### `set_recipients(to=None, cc=None, bcc=None)`
Defines the list of recipients for the email, supporting `To`, `CC`, and `BCC` fields.

**Parameters:**
- `to` (optional): List of primary recipients’ email addresses.
- `cc` (optional): List of CC recipients’ email addresses.
- `bcc` (optional): List of BCC recipients’ email addresses.

**Example Usage:**
```python
smtp_client.set_recipients(
    to=["primary@example.com"],
    cc=["cc_recipient@example.com"],
    bcc=["bcc_recipient@example.com"]
)
```

**Note:** If a single email address is provided instead of a list, it will automatically convert it to a list.

---

### `send(close_connection=True)`

Sends the email to all specified recipients. Optionally closes the connection after sending based on the 
`close_connection` parameter.

**Parameters:**
- `close_connection` (optional): Boolean indicating if the SMTP connection should be closed after sending. Defaults to `True`.

**Raises:**
- `ConnectionError` if no active connection to the server exists. Call `connect()` first.
- `ValueError` if no recipients were specified in `set_recipients()`.

**Example Usage:**
```python
smtp_client.send()
```

---

**Full Example of Sending an Email:**
Here’s a complete workflow using all methods to send an email with `SmtpMail`.

```python
from smtpmail import SmtpMail

# Initialize the SMTP client
smtp_client = SmtpMail(
    in_username="username@example.com",
    in_password="password",
    in_server=("smtp.example.com", 587),
    use_SSL=False
)

# Connect to the SMTP server
smtp_client.connect()

# Set up the message content
smtp_client.set_message(
    subject="Monthly Report",
    from_addr="User <username@example.com>",
    body_text="<h1>Report</h1><p>Here is your monthly report.</p>",
    plaintext="Here is your monthly report.",
    attachment_paths=["path/to/report.pdf"]
)

# Define recipients
smtp_client.set_recipients(
    to=["primary@example.com"],
    cc=["cc_recipient@example.com"],
    bcc=["bcc_recipient@example.com"]
)

# Send the email and disconnect
smtp_client.send()
```

## Additional Notes and Customizations

- **Server Configuration**: You can modify the server address and port in `__init__()` if you are using a different 
email provider.

- **SSL vs. TLS**: By default, `SmtpMail` uses TLS. Set `use_SSL=True` in the constructor to enable SSL, which may be 
required for some servers.

- **Error Handling**: The class includes basic error handling with print statements for attachment issues. For more 
robust error handling, consider adding `try`/`except` blocks in `set_message()` and `send()` as needed.

### Error Handling Recommendations

- Use `try/except` when calling `connect()` and `send()` to handle SMTP exceptions more gracefully in production code.
  
This `SmtpMail` class provides an easy-to-use interface for sending emails with support for customization, attachments, 
and multiple recipient types.

### Recommended Configurations and Best Practices

#### 1. **Environment Variables for Sensitive Information**

For security, avoid hardcoding sensitive information such as the SMTP username and password directly in the code. 
Instead, store these in environment variables and load them in your script.

**Example**:
```python
import os
from smtpmail import SmtpMail

username = os.getenv("SMTP_USERNAME")
password = os.getenv("SMTP_PASSWORD")

smtp_client = SmtpMail(
    in_username=username,
    in_password=password
)
```

This approach protects your credentials and allows for easier changes in configuration without modifying the source code.

#### 2. **Server and Port Configurations**

Different email providers use different SMTP servers and ports. Here are some common configurations:

- **Gmail**: `smtp.gmail.com`, port `587` (TLS) or `465` (SSL)
- **Outlook/Office365**: `smtp.office365.com`, port `587` (TLS)
- **Yahoo**: `smtp.mail.yahoo.com`, port `465` (SSL)
- **Zoho Mail**: `smtp.zoho.com`, port `465` (SSL)

Always verify the SMTP configuration with your email provider’s documentation, as these details may change.

#### 3. **Enable Application-Specific Passwords for Secure Authentication**

If you’re using Gmail or another provider with two-factor authentication (2FA), create an **App Password** specifically 
for your application. This enhances security and allows email sending without using your primary account password.

#### 4. **Testing the Connection**

Before deploying, test the SMTP connection in a development environment to verify server settings, authentication, and 
any network/firewall restrictions that could prevent email sending. A simple call to `smtp_client.connect()` followed by
 `smtp_client.disconnect()` will help ensure connectivity.

#### 5. **Logging and Error Handling**

For production environments, integrate logging and more advanced error handling to ensure any issues with the email 
sending process are captured and can be debugged later. Consider using the `logging` library to capture connection 
errors, recipient errors, and attachment issues.

**Example**:
```python
import logging

logging.basicConfig(filename='smtp_errors.log', level=logging.ERROR)
try:
    smtp_client.connect()
except Exception as e:
    logging.error(f"Connection failed: {e}")
```

#### 6. **Rate Limiting and Throttling**

Some SMTP servers (like Gmail) have sending limits. For high email volumes, consider:
   - **Throttling** email sending frequency (e.g., adding a delay between emails)
   - **Using a dedicated SMTP service** like SendGrid, Mailgun, or Amazon SES for bulk or automated sending, which are 
   designed to handle larger volumes and provide additional tracking capabilities.

#### 7. **Handling Attachments Carefully**

To avoid sending large or unnecessary attachments:
   - **Compress files** where possible.
   - **Validate attachment paths** before sending, especially in environments where files are uploaded dynamically.

### EOF

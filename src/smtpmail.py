import smtplib
import logging
from email.message import EmailMessage
from email.utils import formatdate, COMMASPACE
from pathlib import Path

class SmtpMail:
    def __init__(self, in_username, in_password, in_server=("smtp.gmail.com", 587), use_SSL=False):
        """
        Initialize the SmtpMail object for sending emails.

        :param in_username (str): SMTP server username for authentication.
        :param in_password (str): SMTP server password for authentication.
        :param in_server: Tuple with SMTP server address and port (default: Gmail server and port).
        :param use_SSL: Boolean indicating whether to use SSL (default: False).
        """
        
        self.username    = in_username
        self.password    = in_password
        self.server_name = in_server[0]
        self.server_port = in_server[1]
        self.use_SSL     = use_SSL
        self.connected   = False
        self.recipients  = {"To": [], "CC": [], "BCC": []}
    # __init__ ( )

    def __str__(self):
        """
        Return a string representation of the SmtpMail instance, omitting the password.
        """
        
        return f"Type: Smtp Sender \n" \
               f"Connection to server {self.server_name}, port {self.server_port} \n" \
               f"Connected: {self.connected} \n" \
               f"Username: {self.username}"
    # __str__ ( )
    
    def connect(self):
        """
        Establish a connection to the SMTP server, using SSL or TLS if configured.

        If `use_SSL` is True, connect with SSL. Otherwise, connect normally and start TLS.
        """
        
        try:
            if self.use_SSL:
                self.smtpserver = smtplib.SMTP_SSL(self.server_name, self.server_port)
            else:
                self.smtpserver = smtplib.SMTP(self.server_name, self.server_port)
                self.smtpserver.starttls()
                
            self.smtpserver.login(self.username, self.password)
            self.connected = True
            logging.info("Connected to {}".format(self.server_name))
        except smtplib.SMTPException as e:
            logging.error(f"Connection error: {e}")
    # connect ( )

    def disconnect(self):
        """
        Terminate the connection with the SMTP server, closing the session.
        """
        
        if self.connected:
            self.smtpserver.close()
            self.connected = False
            logging.info("Disconnected")
    # disconnect ( )

    def set_message(self, subject, from_addr=None, body_text=None, plaintext=None, attachment_paths=None):
        """
        Configures the email content with HTML and alternative plain text options.
        
        :param subject: Email subject.
        :param from_addr: Sender's email address.
        :param body_text: Main body of the email (HTML or plain text).
        :param plaintext: Alternative plain text for clients that don't support HTML.
        :param attachment_path: Path to an attachment file, if any.
        """
        
        self.msg = EmailMessage()
        self.msg['Subject'] = subject
        self.msg['From'] = from_addr if from_addr else self.username
        self.msg['Date'] = formatdate(localtime=True)
        
        # self.msg['List-Unsubscribe'] = '<mailto:unsubscribe@example.com>, <https://example.com.br/unsubscribe>'
        
        if plaintext:
            self.msg.set_content(plaintext)
            
        if body_text:
            self.msg.add_alternative(body_text, subtype="html")

        # Adds the attachment if provided
        if attachment_paths:
            for path in attachment_paths:
                attachment = Path(path)
                if attachment.is_file():
                    with attachment.open("rb") as file:
                        self.msg.add_attachment(
                            file.read(),
                            maintype="application", subtype="octet-stream",
                            filename=attachment.name
                        )
                    logging.info(f"Attachment added: {attachment.name}")
                else:
                    logging.warning(f"File not found: {path}")
    # set_message ( )

    def set_recipients(self, to=None, cc=None, bcc=None):
        """
        Specify recipients for the email.

        :param to: List of primary recipients' email addresses.
        :param cc: List of CC recipients' email addresses (optional).
        :param bcc: List of BCC recipients' email addresses (optional).
        """
        
        if to:
            self.recipients["To"] = to if isinstance(to, list) else [to]
        if cc:
            self.recipients["CC"] = cc if isinstance(cc, list) else [cc]
        if bcc:
            self.recipients["BCC"] = bcc if isinstance(bcc, list) else [bcc]

        # Set email headers for recipients
        self.msg['To'] = COMMASPACE.join(self.recipients["To"])
        
        if self.recipients["CC"]:
            self.msg['CC'] = COMMASPACE.join(self.recipients["CC"])
            
        if self.recipients["BCC"]:
            self.msg['BCC'] = COMMASPACE.join(self.recipients["BCC"])
    # set_recipients ( )

    def send(self, close_connection=True):
        """
        Send the email to all specified recipients and optionally close the connection.

        :param close_connection (boolean): Boolean to indicate if the SMTP connection should be closed after sending.
        :raises ConnectionError: If not connected to the SMTP server.
        :raises ValueError: If no recipients are specified.
        """
        
        if not self.connected:
            raise ConnectionError("Not connected to any server. Try self.connect() first")

        full_recipients = self.recipients["To"] + self.recipients["CC"] + self.recipients["BCC"]
        
        if not full_recipients:
            raise ValueError("No recipients specified")

        self.smtpserver.sendmail(self.msg['From'], full_recipients, self.msg.as_string())
        logging.info("Email sent to: {}".format(full_recipients))

        if close_connection:
            self.disconnect()
    # send ( )
# SmtpMail

# EOF

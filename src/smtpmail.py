# Author: Vinicius Miranda de Araujo, https://github.com/vinimiraa
# Repository: https://github.com/vinimiraa/EmailSender
# Description: A Python module for sending emails using SMTP with support for HTML content and attachments.
# Contact: vinicius123miranda24@gmail.com
# Date: 2025-02-02
# Version: 0.10.0
# License: MIT License

import smtplib
import logging
import mimetypes
from pathlib import Path
from email.message import EmailMessage
from email.utils import make_msgid, formatdate
from email_validator import validate_email, EmailNotValidError

# ---------------------------
# --- Exceptions
# ---------------------------

class SmtpError(Exception):
    """Base class for all SMTP-related exceptions."""
    pass
# SmtpError

class SmtpConnectionError(SmtpError):
    """Raised when there is an error connecting to the SMTP server."""
    pass
# SmtpConnectionError

class SmtpRecipientError(SmtpError):
    """Raised when there is an error with the recipient email address."""
    pass
# SmtpRecipientError

class SmtpSendError(SmtpError):
    """Raised when there is an error sending the email."""
    pass
# SmtpSendError

# ---------------------------
# --- Classes
# ---------------------------

class SmtpMessage:
    """
    Class to create and configure email messages using the `email.message.EmailMessage` class.
    """

    def __init__(self):
        """
        Initialize the email message object.

        Headers available for configuration:
            - Date: Date of the email message.
            - From: Sender's email address.
            - To: Primary recipients' email addresses.
            - CC: CC recipients' email addresses.
            - BCC: BCC recipients' email addresses.
            - Subject: Email subject.
            - Content: Email content (plain text and HTML).
            - Message-ID: Unique identifier for the email message.
            - List-Unsubscribe: Unsubscribe URL.
            - Custom headers: Any other custom headers.
        """
        self._message = EmailMessage()  # EmailMessage object
    # __init__ ( )

    # -----------------------------------
    # -- Implementing the Utility Methods
    # -----------------------------------

    def to_string(self):
        """
        Get the email message as a string.

        Returns:
            str: Email message as a string.
        """
        return self._message.as_string()
    # to_string ( )

    def keys(self):
        """
        Get all the message's header field names

        These will be sorted in the order they appeared in the original
        message, or were added to the message, and may contain duplicates.
        Any fields deleted and re-inserted are always appended to the header
        list.

        Returns:
            list: List of all the message's header field names.
        """
        return self._message.keys()
    # keys ( )

    def values(self):
        """
        Get all the message's header values.

        These will be sorted in the order they appeared in the original
        message, or were added to the message, and may contain duplicates.
        Any fields deleted and re-inserted are always appended to the header
        list.

        Returns:
            list: List of all the message's header field values.
        """
        return self._message.values()
    # values ( )

    def items(self):
        """
        Get all the message's header fields and values.

        These will be sorted in the order they appeared in the original
        message, or were added to the message, and may contain duplicates.
        Any fields deleted and re-inserted are always appended to the header
        list.

        Returns:
            list: List of all the message's header fields and values.
        """
        return self._message.items()
    # items ( )

    # -----------------------------------
    # -- Implementing the Getters and Setters
    # -----------------------------------
    
    def set_date(self, date: str = None):
        """
        Set the date of the email message. If no date is provided, the current date is used formatted as RFC 2822.

        Args:
            date (str, optional): Date of the email message. Defaults to None.
        """
        if date is None:
            date = formatdate(localtime=True)
        self._message['Date'] = date
        logging.debug(f"Date set up to '{self._message['Date']}'")
    # set_date ( )

    def get_date(self):
        """
        Get the date of the email message.

        Returns:
            str: Date of the email message.
        """
        return self._message['Date']
    # get_date ( )
    
    def set_from_addr(self, from_addr: str):
        """
        Set the sender's email address for the email message.

        Args:
            from_addr (str, optional): Sender's email address.
        """
        self._message['From'] = from_addr
        logging.debug( f"From address set up to '{from_addr}'" )
    # set_from_addr ( )

    def get_from_addr(self):
        """
        Get the sender's email address from the email message.

        Returns:
            str: Sender's email address.
        """
        return self._message['From']
    # get_from_addr ( )

    def set_to_addr(self, to: list):
        """
        Set the primary recipients' email addresses for the email message.

        Args:
            to (list): List of primary recipients' email addresses.
        """
        COMMASPACE = ', '
        primary_recipients = self._validate_emails(to)
        self._message['To'] = COMMASPACE.join(primary_recipients)
        logging.debug(f"Recipients set up to To: {primary_recipients}")
    # set_to_addr ( )

    def set_cc_addr(self, cc: list):
        """
        Set the CC recipients' email addresses for the email message.

        Args:
            cc (list): List of CC recipients' email addresses.
        """
        COMMASPACE = ', '
        cc_recipients = self._validate_emails(cc)
        self._message['CC'] = COMMASPACE.join(cc_recipients)
        logging.debug(f"Recipients set up to CC: {cc_recipients}")
    # set_cc_addr ( )

    def set_bcc_addr(self, bcc: list):
        """
        Set the BCC recipients' email addresses for the email message.

        Args:
            bcc (list): List of BCC recipients' email addresses.
        """
        COMMASPACE = ', '
        bcc_recipients = self._validate_emails(bcc)
        self._message['BCC'] = COMMASPACE.join(bcc_recipients)
        logging.debug(f"Recipients set up to BCC: {bcc_recipients}")
    # set_bcc_addr ( )

    def get_to_addr(self):
        """
        Get the primary recipients from the email message.

        Returns:
            list: List of email addresses.
        """
        return self._message['To'].split(', ') if 'To' in self._message else []
    # get_to_addr ( )

    def get_cc_addr(self):
        """
        Get the CC recipients from the email message.

        Returns:
            list: List of email addresses.
        """
        return self._message['CC'].split(', ') if 'CC' in self._message else []
    # get_cc_addr ( )

    def get_bcc_addr(self):
        """
        Get the BCC recipients from the email message.

        Returns:
            list: List of email addresses.
        """
        return self._message['BCC'].split(', ') if 'BCC' in self._message else []
    # get_bcc_addr ( )

    def set_recipients(self, to: list, cc: list = None, bcc: list = None):
        """
        Configure the recipients for the email message, validating the email addresses.

        Args:
            to (list): List of primary recipients' email addresses.
            cc (list, optional): List of CC recipients' email addresses. Defaults to None.
            bcc (list, optional): List of BCC recipients' email addresses. Defaults to None.
        """
        self.set_to_addr(to)
        if cc:
            self.set_cc_addr(cc)
        if bcc:
            self.set_bcc_addr(bcc)
    # set_recipients ( )

    def get_recipients(self):
        """
        Get the recipients from the email message.

        Returns:
            list: List of email addresses.
        """
        return list( set(self.get_to_addr() + self.get_cc_addr() + self.get_bcc_addr()) )
    # get_recipients ( )
    
    def set_subject(self, subject: str):
        """
        Set the subject of the email message.

        Args:
            subject (str, optional): Email subject.
        """
        self._message['Subject'] = subject
        logging.debug( f"Subject set up to '{subject}'" )
    # set_subject ( )

    def get_subject(self):
        """
        Get the subject of the email message.

        Returns:
            str: Email subject.
        """
        return self._message['Subject']
    # get_subject ( )
        
    def set_content(self, text: str = None, html: str = None):
        """
        Set the content of the email message, with optional plain text and HTML versions.

        Args:
            text (str, optional): Plain text version of the email. Defaults to None.
            html (str, optional): HTML version of the email. Defaults to None.
        """
        if text:
            self._message.set_content(text)
            logging.debug( f"Text content set up" )
        if html:
            self._message.add_alternative(html, subtype="html")
            logging.debug( f"Html content set up" )
    # set_content ( )

    def get_content(self):
        """
        Get the content of the email message.

        Returns:
            str: Email content.
        """
        if self._message.is_multipart():
            for part in self._message.iter_parts():
                if part.get_content_type() == 'text/plain':
                    return part.get_payload(decode=True).decode()
                elif part.get_content_type() == 'text/html':
                    return part.get_payload(decode=True).decode()
        else:
            return self._message.get_payload(decode=True).decode()
    # get_content ( )
    
    def add_attachment(self, attachment_paths: list = None):
        """
        Add the attachments for the email message.

        Args:
            attachment_paths (list, optional): List of file paths to be attached. Defaults to None.
        """
        if attachment_paths:
            for path in attachment_paths:
                attachment = Path(path)
                if attachment.exists() and attachment.is_file():
                    try:
                        ctype, encoding = mimetypes.guess_type(attachment)
                        if ctype is None or encoding is not None:
                            ctype = "application/octet-stream"
                        maintype, subtype = ctype.split("/", 1)
                        with attachment.open("rb") as file:
                            self._message.add_attachment(
                                file.read(), 
                                maintype=maintype, 
                                subtype=subtype, 
                                filename=attachment.name
                            )
                        logging.debug(f"Attachment added: {attachment.name}")
                    except Exception as e:
                        logging.error(f"Failed to add attachment {attachment.name}: {e}")
                else:
                    logging.warning(f"File not found: {path}")
    # add_attachment ( )

    def set_message_id(self, msg_id: tuple = (None, None)):
        """
        Set the Message-ID header for the email message.

        Args:
            msg_id (tuple, optional): Tuple containing the message ID and Domain. Defaults to (None, None).
        """
        if msg_id[0] or msg_id[1]:
            self._message['Message-ID'] = make_msgid(idstring=msg_id[0], domain=msg_id[1])
        else:
            self._message['Message-ID'] = make_msgid()
        logging.debug( f"Message-ID set up to '{self._message['Message-ID']}'" )
    # set_message_id ( )

    def get_message_id(self):
        """
        Get the Message-ID header from the email message.

        Returns:
            str: Message-ID header.
        """
        return self._message['Message-ID']
    # get_message_id ( )
    
    def set_list_unsubscribe(self, list_unsubscribe: str = None):
        """
        Set the List-Unsubscribe header for the email message.

        Args:
            list_unsubscribe (str, optional): Unsubscribe URL. Defaults to None.
        """
        self._message['List-Unsubscribe'] = list_unsubscribe
        logging.debug( f"List-Unsubscribe set up to '{list_unsubscribe}'" )
    # set_list_unsubscribe ( )

    def get_list_unsubscribe(self):
        """
        Get the List-Unsubscribe header from the email message.

        Returns:
            str: Unsubscribe URL.
        """
        return self._message['List-Unsubscribe']
    # get_list_unsubscribe ( )
    
    def set_custom(self, key: str, value: str):
        """
        Set a custom header for the email message.

        Args:
            key (str): Header key.
            value (str): Header value.
        """
        try:
            self._message[key] = value
        except Exception as e:
            logging.error(f"Failed to set custom header: {e}")
        logging.debug( f"Custom header set up: '{key}: {value}'" )
    # set_custom ( )

    def get_custom(self, key: str):
        """
        Get a custom header from the email message.

        Args:
            key (str): Header key.

        Returns:
            str: Header value.
        """
        try:
            return self._message[key]
        except Exception as e:
            logging.error(f"Failed to get custom header: {e}")
            return None
    # get_custom ( )

    # -----------------------------------
    # -- Implementing the mapping protocol
    # -----------------------------------

    def __getitem__(self, key):
        """
        Get the value of a header from the email message.

        Args:
            key (str): Header key.

        Returns:
            str: Header value.
        """
        return self._message[key]
    # __getitem__ ( )

    def __setitem__(self, key, value):
        """
        Set the value of a header in the email message.

        Args:
            key (str): Header key.
            value (str): Header value.
        """
        self._message[key] = value
    # __setitem__ ( )

    def __delitem__(self, key):
        """
        Delete a header from the email message.

        Args:
            key (str): Header key.
        """
        del self._message[key]
    # __delitem__ ( )

    def __contains__(self, key):
        """
        Check if a header is present in the email message.

        Args:
            key (str): Header key.

        Returns:
            bool: True if the header is present, False otherwise.
        """
        return key in self._message
    # __contains__ ( )

    def __iter__(self):
        """
        Iterate over the headers in the email message.

        Returns:
            iter: Iterator over the headers.
        """
        return self._message.__iter__()
    # __iter__ ( )

    def __len__(self):
        """
        Get the number of headers in the email message.

        Returns:
            int: Number of headers.
        """
        return len(self._message)
    # __len__ ( )

    def __str__(self):
        """
        Get the email message as a string.

        Returns:
            str: Email message as a string.
        """
        return self.to_string()
    # __str__ ( )

    # ---------------------------
    # --- Functions
    # ---------------------------

    def _validate_emails(self, emails: list):
        """
        Validate a list of email addresses using the `email_validator` library.

        Args:
            emails (list): List of email addresses to be validated.

        Returns:
            list: List of validated email addresses.

        Raises:
            SmtpRecipientError: If any email address is invalid.
        """
        valid_emails = []
        for email in emails:
            try:
                valid_emails.append(validate_email(email).normalized)
            except EmailNotValidError:
                logging.warning(f"Invalid email address, it will be ignored: {email}")
                print(f"Invalid email address, it will be ignored: {email}")
        return valid_emails
    # _validate_emails ( )
# SmtpMessage

class SmtpClient:
    """
    Class to send emails using the SMTP protocol. Supports sending HTML emails with attachments.
    """
    
    def __init__(self, username: str, password: str, 
                 smtp_host: str = "smtp.gmail.com", smtp_port: int = 587):
        """
        Initialize the SMTP client with the provided credentials.

        Args:
            username (str): Email address used to authenticate with the SMTP server.
            password (str): Password used to authenticate with the SMTP server.
            smtp_host (str, optional): SMTP server host. Defaults to "smtp.gmail.com".
            smtp_port (int, optional): SMTP server port. Defaults to 587.
        """
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._username  = username
        self._password  = password
        self._server    = None       # SMTP server object
    # __init__ ( )

    def __enter__(self):
        """
        Enter the context manager and connect to the SMTP server.

        Returns:
            SmtpClient: SMTP client object.
        """
        self.connect()
        return self
    # __enter__ ( )

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager and disconnect from the SMTP server.
        """
        self.disconnect()

        if exc_type is not None:
            logging.error(f"An error occurred: {exc_type}, {exc_value}")
            return False
    # __exit__ ( )
    
    def connect(self):
        """
        Connect to the SMTP server using the provided credentials.
        
        If `use_SSL` is True, connect with SSL. Otherwise, connect normally and start TLS.

        Raises:
            SmtpConnectionError: If there is an error connecting to the server.
        """
        if self._server:
            logging.warning("Already connected to an SMTP server.")
            return
        
        try:
            self._server = smtplib.SMTP(self._smtp_host, self._smtp_port)
            self._server.starttls()
            self._server.login(self._username, self._password)
            
            logging.info(f"Successfully  connected to SMTP server: {self._smtp_host}")
        except smtplib.SMTPException as e:
            logging.error(f"Connection error: {e}")
            raise SmtpConnectionError( f"Connection error: {e}" )
    # connect ( )

    def disconnect(self):
        """
        Disconnect from the SMTP server.
        """
        if self._server:
            self._server.quit()
            self._server = None
            logging.info(f"Disconnected from SMTP server: {self._smtp_host}")
    # disconnect ( )
    
    def send_email(self, message: SmtpMessage):
        """
        Send an email to the specified recipients.

        Args:
            message (SmtpMessage): Email message object.

        Raises:
            SmtpConnectionError: If not connected to any server.
            SmtpRecipientError: If no recipients are specified.
            SmtpSendError: If the email fails to send.
        """
        try:
            if not self._server:
                logging.error("Not connected to any SMTP server. Please connect first.")
                raise SmtpConnectionError("Not connected to any SMTP server. Please connect first.")
            
            all_recipients = message.get_recipients()
            if not all_recipients:
                logging.error("No recipients specified. Please provide at least one recipient.")
                raise SmtpRecipientError("No recipients specified. Please provide at least one recipient.")
            
            self._server.sendmail(message['From'], all_recipients, message.to_string())

            logging.info(f"Email successfully sent from '{message['From']}' to {all_recipients}")
        except smtplib.SMTPException as e:
            logging.error(f"Failed to send email: {e}")
            raise SmtpSendError(f"Failed to send email: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise SmtpSendError(f"An error occurred: {e}")
    # send_email ( )
# SmtpClient

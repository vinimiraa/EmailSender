import os
from dotenv import load_dotenv

# Import the SmtpMail class from the smtpmail module
from smtpmail import SmtpMail

# Load environment variables from the .env file
load_dotenv( )

def main( ):
    # Retrieve credentials from the .env file
    server   = os.getenv( "SMTP_SERVER" )
    port     = os.getenv( "SMTP_PORT" )
    username = os.getenv( 'SMTP_USERNAME' )
    password = os.getenv( 'SMTP_PASSWORD' )

    # Check if the credentials were loaded
    if not username or not password:
        raise ValueError( "SMTP credentials not found. Check your .env file" )

    # Initialize the email sending object
    smtp_mail = SmtpMail( username, password, (server, port) )

    # Connect to the server
    smtp_mail.connect( )

    # Set email content
    smtp_mail.set_message(
        subject= "Email Subject",
        from_addr= "User <username@example.com>",
        body_text= "<p>This is a test email sent using the <b>SmtpMail</b> class.</p>",
        plaintext= "This is a test email sent using the SmtpMail class.",
        attachment_paths= ["attachment.txt"]
    )
    
    # Or you can add attachments separately
    # smtp_mail.add_attachements( ["attachment.txt"] )

    # Set recipients
    smtp_mail.set_recipients(
        to= ["to_recipient@example.com"],
        cc= ["cc_recipient@example.com"],
        bcc= ["bcc_recipient@example.com"]
    )
    
    # Send the email
    smtp_mail.send( )
# main ( )

if __name__ == "__main__":
    main( )

# EOF

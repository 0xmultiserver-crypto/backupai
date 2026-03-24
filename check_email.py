import imaplib
import email
from email.header import decode_header
import re
import time

# Gmail IMAP settings
IMAP_SERVER = "imap.gmail.com"
EMAIL = "0xmultiserver@gmail.com"
APP_PASSWORD = "mzrqicpqymfubarr"

def get_magic_link():
    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, APP_PASSWORD)
        mail.select("inbox")
        
        # Search for emails from sumopod
        status, messages = mail.search(None, 'FROM "sumopod"')
        
        if status == "OK" and messages[0]:
            email_ids = messages[0].split()
            # Get the latest 5 emails
            for email_id in email_ids[-5:]:
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                if status == "OK":
                    msg = email.message_from_bytes(msg_data[0][1])
                    body = ""
                    
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain" or content_type == "text/html":
                                try:
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    # Look for magic link
                    link_match = re.search(r'https?://[^\s"<>]+sumopod[^\s"<>]*', body)
                    if link_match:
                        print(f"Found magic link: {link_match.group(0)}")
                        mail.logout()
                        return link_match.group(0)
        
        mail.logout()
        print("No SumoPod magic link found in recent emails")
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Checking for SumoPod magic link...")
    link = get_magic_link()
    if link:
        print(f"\nLink found: {link}")
    else:
        print("\nNo link found yet. May need to request first.")

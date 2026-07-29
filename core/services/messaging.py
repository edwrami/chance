from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)

def _client_from_creds(creds):
    """
    Initializes a Twilio Client using an API Key.
    For API Keys, username = API Key SID, password = API Key Secret, 
    and account_sid must be explicitly passed.
    """
    return Client(creds.api_key_sid, creds.api_key_secret, creds.account_sid)

def send_sms(creds, destino, cuerpo):
    """
    Sends an SMS using the provided Twilio credentials.
    """
    try:
        client = _client_from_creds(creds)
        msg = client.messages.create(
            body=cuerpo,
            from_=creds.sms_number,
            to=destino,
        )
        return {"success": True, "sid": msg.sid, "status": msg.status}
    except Exception as e:
        logger.error(f"Error sending SMS via Twilio: {str(e)}")
        return {"success": False, "error": str(e)}

def send_whatsapp(creds, destino, cuerpo):
    """
    Sends a WhatsApp message using the provided Twilio credentials.
    """
    try:
        client = _client_from_creds(creds)
        # Twilio expects WhatsApp numbers to be prefixed with 'whatsapp:'
        from_number = creds.whatsapp_number
        if not from_number.startswith('whatsapp:'):
            from_number = f"whatsapp:{from_number}"
            
        to_number = destino
        if not to_number.startswith('whatsapp:'):
            to_number = f"whatsapp:{to_number}"

        msg = client.messages.create(
            body=cuerpo,
            from_=from_number,
            to=to_number,
        )
        return {"success": True, "sid": msg.sid, "status": msg.status}
    except Exception as e:
        logger.error(f"Error sending WhatsApp via Twilio: {str(e)}")
        return {"success": False, "error": str(e)}

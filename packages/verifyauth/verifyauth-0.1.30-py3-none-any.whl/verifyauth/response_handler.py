from datetime import datetime, timedelta
from fastapi.responses import Response

# Function to generate dynamic headers
def generate_headers():
    # Calculate "Expires" header (e.g., 1 day ago for demonstration)
    current_time = datetime.utcnow()
    expires_time = current_time - timedelta(days=1)  # This makes it an expired date
    expires_header = expires_time.strftime("%a, %d %b %Y %H:%M:%S GMT")

    # Only add headers that are necessary, and avoid duplicates for "date" and "server"
    return {
        "CACHE-CONTROL": "no-cache",
        "EXPIRES": expires_header,
        "PRAGMA": "no-cache",
        "Keep-Alive": "timeout=5, max=100",
        "Connection": "Keep-Alive",
        "Content-Type": "text/xml; charset=UTF-8"
    }

# Reusable function for custom SOAP/XML response
def custom_soap_response(status: bool, message: str, session_id: int, response_tag: str, result_tag: str, status_code: int = 200):
    xml_response = f'''<?xml version="1.0" encoding="UTF-8" ?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV='http://schemas.xmlsoap.org/soap/envelope/' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:s='http://www.w3.org/2001/XMLSchema'>
<SOAP-ENV:Body><{response_tag}>
    <{result_tag}>
        <statusIntegracao>
            <status>{str(status).lower()}</status>
            <mensagem>{message}</mensagem>
            <sessionId>{session_id}</sessionId>
        </statusIntegracao>
    </{result_tag}>
</{response_tag}></SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''

    # Generate headers but avoid overriding "date" and "server"
    headers = generate_headers()

    return Response(content=xml_response, headers=headers, media_type="text/xml", status_code=status_code)

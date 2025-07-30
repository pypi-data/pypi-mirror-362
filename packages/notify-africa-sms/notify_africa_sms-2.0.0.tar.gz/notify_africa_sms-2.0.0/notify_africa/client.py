"""
Main client for Notify Africa SMS SDK
"""

import requests
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
import json

from .exceptions import (
    NotifyAfricaException,
    AuthenticationError,
    ValidationError,
    InsufficientCreditsError,
    NetworkError,
    SenderIDNotFoundError
)
from .models import SMSResponse, BulkSMSResponse, DeliveryStatus, SenderID
from .utils import (
    validate_phone_numbers,
    calculate_sms_credits,
    parse_excel_contacts,
    format_datetime_for_api
)


class NotifyAfricaClient:
    """
    Notify Africa SMS Client
    
    A Python client for interacting with Notify Africa SMS API.
    """
    
    def __init__(self, api_key: str, sender_id: str = None, base_url: str = None):
        """
        Initialize the Notify Africa client
        
        Args:
            api_key (str): Your Notify Africa API key/token
            sender_id (str, optional): Default sender ID for SMS
            base_url (str, optional): Base URL for the API (defaults to production)
        """
        self.api_key = api_key
        self.default_sender_id = sender_id
        self.base_url = base_url or "https://api.notify.africa/v2"
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        })
    
    def _make_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make HTTP request to the API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, json=data)
            response_data = response.json()
            
            # Handle different status codes based on the API documentation
            if response.status_code == 401:
                raise AuthenticationError(
                    response_data.get('message', 'Authentication failed'),
                    response.status_code,
                    response_data
                )
            elif response.status_code == 402:
                raise InsufficientCreditsError(
                    response_data.get('message', 'Insufficient credits'),
                    response.status_code,
                    response_data
                )
            elif response.status_code == 422:
                raise ValidationError(
                    response_data.get('message', 'Validation failed'),
                    response.status_code,
                    response_data
                )
            elif response.status_code >= 400:
                raise NotifyAfricaException(
                    response_data.get('message', 'Request failed'),
                    response.status_code,
                    response_data
                )
            
            return response_data
            
        except requests.RequestException as e:
            raise NetworkError(f"Network error: {e}")
        except json.JSONDecodeError:
            raise NotifyAfricaException("Invalid JSON response from server")
    
    def get_profile(self) -> Dict[str, Any]:
        """Get user profile information"""
        response = self._make_request("GET", "/profile")
        return response
    
    def get_sender_ids(self) -> List[SenderID]:
        """Get list of available sender IDs"""
        response = self._make_request("GET", "/sender-ids/list")
        
        sender_ids = []
        for item in response.get('data', []):
            sender_ids.append(SenderID(
                id=item['id'],
                name=item['name'],
                status=item.get('status_id', ''),
                purpose=item.get('purpose', ''),
                access=item.get('access', ''),
                created_at=datetime.fromisoformat(item['created_at'].replace('Z', '+00:00'))
            ))
        
        return sender_ids
    
    def send_sms(self, phone_number: str, message: str, sender_id: Optional[str] = None) -> SMSResponse:
        """
        Send a single SMS
        
        Args:
            phone_number (str): Recipient phone number
            message (str): SMS message content
            sender_id (str, optional): Sender ID (uses default if not provided)
            
        Returns:
            SMSResponse: Response containing SMS details
        """
        # Validate and normalize phone number
        validated_numbers = validate_phone_numbers([phone_number])
        
        # Use provided sender_id or default
        sender = sender_id or self.default_sender_id
        if not sender:
            raise ValidationError("Sender ID is required")
        
        # Prepare request data based on API documentation
        data = {
            "sender_id": sender,  # This should be the sender ID name/number
            "sms": message,
            "schedule": "none",  # Immediate sending
            "recipients": [{"number": validated_numbers[0]}]
        }
        
        response = self._make_request("POST", "/smses/send", data)
        
        return SMSResponse(
            success=response.get('success', False),
            message=response.get('message', ''),
            data=response.get('data'),
            status_code=200,
            balance=response.get('data', {}).get('balance'),
            credits_spent=response.get('data', {}).get('credits_spent'),
            sms_id=str(response.get('data', {}).get('smses', [{}])[0].get('id', '')) if response.get('data', {}).get('smses') else None
        )
    
    def send_bulk_sms(self, phone_numbers: List[str], message: str, sender_id: Optional[str] = None) -> BulkSMSResponse:
        """
        Send SMS to multiple recipients
        
        Args:
            phone_numbers (List[str]): List of recipient phone numbers
            message (str): SMS message content
            sender_id (str, optional): Sender ID (uses default if not provided)
            
        Returns:
            BulkSMSResponse: Response containing bulk SMS details
        """
        # Validate and normalize phone numbers
        validated_numbers = validate_phone_numbers(phone_numbers)
        
        # Use provided sender_id or default
        sender = sender_id or self.default_sender_id
        if not sender:
            raise ValidationError("Sender ID is required")
        
        # Prepare recipients list
        recipients = [{"number": number} for number in validated_numbers]
        
        # Prepare request data
        data = {
            "sender_id": sender,
            "sms": message,
            "schedule": "none",
            "recipients": recipients
        }
        
        response = self._make_request("POST", "/smses/send", data)
        
        sent_messages = response.get('data', {}).get('smses', [])
        
        return BulkSMSResponse(
            success=response.get('success', False),
            message=response.get('message', ''),
            total_messages=len(phone_numbers),
            successful_messages=len(sent_messages),
            failed_messages=len(phone_numbers) - len(sent_messages),
            balance=response.get('data', {}).get('balance'),
            total_credits=response.get('data', {}).get('credits_spent'),
            messages=sent_messages
        )
    
    def send_scheduled_sms(self, phone_numbers: Union[str, List[str]], message: str, 
                          schedule_time: datetime, sender_id: Optional[str] = None) -> BulkSMSResponse:
        """
        Send scheduled SMS
        
        Args:
            phone_numbers (Union[str, List[str]]): Recipient phone number(s)
            message (str): SMS message content
            schedule_time (datetime): When to send the SMS
            sender_id (str, optional): Sender ID (uses default if not provided)
            
        Returns:
            BulkSMSResponse: Response containing scheduled SMS details
        """
        # Validate and normalize phone numbers
        if isinstance(phone_numbers, str):
            phone_numbers = [phone_numbers]
        validated_numbers = validate_phone_numbers(phone_numbers)
        
        # Use provided sender_id or default
        sender = sender_id or self.default_sender_id
        if not sender:
            raise ValidationError("Sender ID is required")
        
        # Prepare recipients list
        recipients = [{"number": number} for number in validated_numbers]
        
        # Format schedule time
        schedule_date = schedule_time.strftime("%Y-%m-%d")
        schedule_time_str = schedule_time.strftime("%H:%M")
        
        # Prepare request data for daily schedule (single occurrence)
        data = {
            "sender_id": sender,
            "sms": message,
            "schedule": "daily",
            "start_date": schedule_date,
            "end_date": schedule_date,  # Same date for single occurrence
            "time": schedule_time_str,
            "recipients": recipients
        }
        
        response = self._make_request("POST", "/smses/send", data)
        
        # Handle scheduled SMS response (data is often null for scheduled messages)
        response_data = response.get('data')
        
        # For scheduled SMS, the API returns data: null, so we need to handle this
        if response_data is None:
            # Extract credit information from the message if available
            message_text = response.get('message', '')
            credits_spent = None
            
            # Try to extract credits from message like "1 message(s) scheduled for 1 day(s) with total cost of 1 credits."
            import re
            credit_match = re.search(r'total cost of (\d+) credits?', message_text)
            if credit_match:
                credits_spent = int(credit_match.group(1))
            
            return BulkSMSResponse(
                success=response.get('success', False),
                message=response.get('message', ''),
                total_messages=len(phone_numbers),
                successful_messages=len(phone_numbers) if response.get('success') else 0,
                failed_messages=0 if response.get('success') else len(phone_numbers),
                balance=None,  # Not provided in scheduled SMS response
                total_credits=credits_spent,
                messages=[]  # Scheduled messages don't return message IDs immediately
            )
        else:
            # Handle normal response (in case API changes)
            scheduled_messages = response_data.get('smses', [])
            
            return BulkSMSResponse(
                success=response.get('success', False),
                message=response.get('message', ''),
                total_messages=len(phone_numbers),
                successful_messages=len(scheduled_messages),
                failed_messages=len(phone_numbers) - len(scheduled_messages),
                balance=response_data.get('balance'),
                total_credits=response_data.get('total_cost') or response_data.get('credits_spent'),
                messages=scheduled_messages
            )
    
    def send_sms_from_excel(self, file_path: str, message_template: str = None,
                           message_column: str = "message", phone_column: str = "phone",
                           names_column: str = "names", sender_id: Optional[str] = None) -> BulkSMSResponse:
        """
        Send SMS from Excel file
        
        Args:
            file_path (str): Path to Excel file
            message_template (str, optional): Template message (can use {names} placeholder)
            message_column (str): Column name for individual messages
            phone_column (str): Column name for phone numbers
            names_column (str): Column name for contact names
            sender_id (str, optional): Sender ID (uses default if not provided)
            
        Returns:
            BulkSMSResponse: Response containing bulk SMS details
        """
        # Parse contacts from Excel
        contacts = parse_excel_contacts(file_path, phone_column, message_column, names_column)
        
        if not contacts:
            raise ValidationError("No valid contacts found in Excel file")
        
        # Use provided sender_id or default
        sender = sender_id or self.default_sender_id
        if not sender:
            raise ValidationError("Sender ID is required")
        
        successful_messages = []
        failed_messages = []
        total_credits = 0
        
        for contact in contacts:
            try:
                # Validate phone number
                validated_phone = validate_phone_numbers([contact['phone']])[0]
                
                # Determine message to send
                if message_template:
                    # Use template with name substitution
                    message = message_template.replace('{names}', contact.get('names', 'Customer'))
                    message = message.replace('{NAMES}', contact.get('names', 'Customer'))
                elif 'message' in contact and contact['message']:
                    # Use individual message from Excel
                    message = contact['message']
                else:
                    failed_messages.append(contact)
                    continue
                
                # Send individual SMS
                response = self.send_sms(validated_phone, message, sender)
                
                if response.success:
                    successful_messages.append({
                        'phone': validated_phone,
                        'message': message,
                        'sms_id': response.sms_id
                    })
                    total_credits += response.credits_spent or calculate_sms_credits(message)
                else:
                    failed_messages.append(contact)
                    
            except Exception as e:
                failed_messages.append({**contact, 'error': str(e)})
        
        return BulkSMSResponse(
            success=len(successful_messages) > 0,
            message=f"Sent {len(successful_messages)} SMS, {len(failed_messages)} failed",
            total_messages=len(contacts),
            successful_messages=len(successful_messages),
            failed_messages=len(failed_messages),
            total_credits=total_credits,
            messages=successful_messages
        )
    
    def get_sms_history(self, records: int = 50) -> Dict[str, Any]:
        """
        Get SMS history
        
        Args:
            records (int): Number of records to retrieve
            
        Returns:
            Dict: SMS history data
        """
        response = self._make_request("GET", f"/smses/history/records/{records}")
        
        # Handle different response formats from the API
        if isinstance(response, list):
            # API returns data directly as a list
            return {
                "success": True,
                "data": response,
                "message": f"Retrieved {len(response)} SMS records"
            }
        elif isinstance(response, dict):
            # API returns structured response
            return response
        else:
            # Fallback for unexpected response format
            return {
                "success": False,
                "data": [],
                "message": "Unexpected response format"
            }
    
    def get_delivery_status(self, sms_id: str) -> Optional[DeliveryStatus]:
        """
        Get delivery status for a specific SMS
        
        Args:
            sms_id (str): SMS ID to check status for
            
        Returns:
            DeliveryStatus: Delivery status information
        """
        try:
            history_response = self.get_sms_history(100)  # Get recent messages
            
            # Handle different response formats
            if isinstance(history_response, dict):
                messages = history_response.get('data', [])
            elif isinstance(history_response, list):
                messages = history_response
            else:
                return None
            
            # Search for the specific SMS ID
            for msg in messages:
                if str(msg.get('id')) == str(sms_id):
                    return DeliveryStatus(
                        sms_id=str(msg['id']),
                        recipient=msg.get('recipient', ''),
                        status=msg.get('status_id', ''),
                        status_description=msg.get('status_description', ''),
                        credits=msg.get('credits')
                    )
            
            return None
        except Exception:
            return None
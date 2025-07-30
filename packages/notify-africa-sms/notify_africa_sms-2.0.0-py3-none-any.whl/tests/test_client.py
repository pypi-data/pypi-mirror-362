import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import tempfile
import pandas as pd

from notify_africa import NotifyAfricaClient
from notify_africa.exceptions import AuthenticationError, ValidationError


class TestNotifyAfricaClient(unittest.TestCase):
    
    def setUp(self):
        self.client = NotifyAfricaClient(
            api_key="test_api_key",
            sender_id="TEST_SENDER",
            base_url="https://test-api.notifyafrica.com"
        )
    
    @patch('requests.Session.request')
    def test_send_sms_success(self, mock_request):
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "message": "SMS sent successfully",
            "data": {
                "balance": 100,
                "credits_spent": 1,
                "smses": [{"id": "123"}]
            }
        }
        mock_request.return_value = mock_response
        
        response = self.client.send_sms("255712345678", "Test message")
        
        self.assertTrue(response.success)
        self.assertEqual(response.sms_id, "123")
        self.assertEqual(response.credits_spent, 1)
        self.assertEqual(response.balance, 100)
    
    @patch('requests.Session.request')
    def test_send_sms_authentication_error(self, mock_request):
        # Mock authentication error
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "success": False,
            "message": "Unauthorized"
        }
        mock_request.return_value = mock_response
        
        with self.assertRaises(AuthenticationError):
            self.client.send_sms("255712345678", "Test message")
    
    def test_invalid_phone_number(self):
        with self.assertRaises(ValueError):
            self.client.send_sms("invalid_phone", "Test message")
    
    @patch('requests.Session.request')
    def test_send_bulk_sms(self, mock_request):
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "message": "Bulk SMS sent",
            "data": {
                "balance": 95,
                "credits_spent": 5,
                "smses": [{"id": "123"}, {"id": "124"}]
            }
        }
        mock_request.return_value = mock_response
        
        phone_numbers = ["255712345678", "255687654321"]
        response = self.client.send_bulk_sms(phone_numbers, "Bulk test message")
        
        self.assertTrue(response.success)
        self.assertEqual(response.total_messages, 2)
        self.assertEqual(response.successful_messages, 2)
        self.assertEqual(response.failed_messages, 0)
    
    def test_send_sms_from_excel(self):
        # Create a temporary Excel file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
            df = pd.DataFrame({
                'phone': ['255712345678', '255687654321'],
                'names': ['John Doe', 'Jane Doe'],
                'message': ['Hello John', 'Hello Jane']
            })
            df.to_excel(tmp_file.name, index=False)
            
            with patch.object(self.client, 'send_sms') as mock_send:
                mock_send.return_value = Mock(
                    success=True,
                    sms_id="123",
                    credits_spent=1
                )
                
                response = self.client.send_sms_from_excel(
                    tmp_file.name,
                    message_template="Hello {names}!"
                )
                
                self.assertTrue(response.success)
                self.assertEqual(response.total_messages, 2)
                self.assertEqual(mock_send.call_count, 2)

    @patch('requests.Session.request')
    def test_get_sms_history_success(self, mock_request):
        """Test successful SMS history retrieval"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "message": "SMS history retrieved",
            "data": [
                {
                    "id": "123",
                    "recipient": "255712345678",
                    "sms": "Test message",
                    "status_id": "delivered",
                    "status_description": "Message delivered",
                    "credits": 1,
                    "created_at": "2024-01-15T10:30:00Z",
                    "sender_id": "TEST_SENDER"
                },
                {
                    "id": "124",
                    "recipient": "255687654321",
                    "sms": "Another test",
                    "status_id": "pending",
                    "status_description": "Message pending",
                    "credits": 1,
                    "created_at": "2024-01-15T10:25:00Z",
                    "sender_id": "TEST_SENDER"
                }
            ]
        }
        mock_request.return_value = mock_response
        
        history = self.client.get_sms_history(records=10)
        
        self.assertTrue(history.get('success'))
        self.assertEqual(len(history.get('data', [])), 2)
        
        # Check first message details
        first_msg = history['data'][0]
        self.assertEqual(first_msg['id'], "123")
        self.assertEqual(first_msg['recipient'], "255712345678")
        self.assertEqual(first_msg['status_id'], "delivered")

    @patch('requests.Session.request')
    def test_get_sms_history_empty(self, mock_request):
        """Test SMS history when no messages exist"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "message": "No SMS history found",
            "data": []
        }
        mock_request.return_value = mock_response
        
        history = self.client.get_sms_history()
        
        self.assertTrue(history.get('success'))
        self.assertEqual(len(history.get('data', [])), 0)

    @patch('requests.Session.request')
    def test_get_delivery_status_found(self, mock_request):
        """Test delivery status check when SMS is found"""
        # Mock history response with the SMS we're looking for
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": [
                {
                    "id": "123",
                    "recipient": "255712345678",
                    "sms": "Test message",
                    "status_id": "delivered",
                    "status_description": "Message delivered successfully",
                    "credits": 1,
                    "created_at": "2024-01-15T10:30:00Z"
                }
            ]
        }
        mock_request.return_value = mock_response
        
        status = self.client.get_delivery_status("123")
        
        self.assertIsNotNone(status)
        self.assertEqual(status.sms_id, "123")
        self.assertEqual(status.recipient, "255712345678")
        self.assertEqual(status.status, "delivered")
        self.assertEqual(status.status_description, "Message delivered successfully")
        self.assertEqual(status.credits, 1)

    @patch('requests.Session.request')
    def test_get_delivery_status_not_found(self, mock_request):
        """Test delivery status check when SMS is not found"""
        # Mock history response without the SMS we're looking for
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": [
                {
                    "id": "456",
                    "recipient": "255687654321",
                    "status_id": "pending"
                }
            ]
        }
        mock_request.return_value = mock_response
        
        status = self.client.get_delivery_status("123")
        
        self.assertIsNone(status)

    @patch('requests.Session.request')
    def test_get_delivery_status_api_error(self, mock_request):
        """Test delivery status check when API returns error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "success": False,
            "message": "Internal server error"
        }
        mock_request.return_value = mock_response
        
        # Should handle the exception gracefully and return None
        status = self.client.get_delivery_status("123")
        
        self.assertIsNone(status)

    @patch('requests.Session.request')
    def test_get_sms_history_authentication_error(self, mock_request):
        """Test SMS history with authentication error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "success": False,
            "message": "Unauthorized"
        }
        mock_request.return_value = mock_response
        
        with self.assertRaises(AuthenticationError):
            self.client.get_sms_history()

    @patch('requests.Session.request') 
    def test_get_sms_history_with_custom_records(self, mock_request):
        """Test SMS history with custom record count"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": [{"id": f"{i}"} for i in range(100)]  # 100 mock records
        }
        mock_request.return_value = mock_response
        
        history = self.client.get_sms_history(records=100)
        
        # Verify the correct endpoint was called
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertIn("/smses/history/records/100", args[1])
        
        self.assertEqual(len(history.get('data', [])), 100)

    def test_sms_history_data_structure(self):
        """Test that SMS history data has expected structure"""
        # This would be an integration test in a real scenario
        # Here we're testing the expected data structure
        expected_fields = [
            'id', 'recipient', 'sms', 'status_id', 
            'status_description', 'credits', 'created_at', 'sender_id'
        ]
        
        sample_message = {
            "id": "123",
            "recipient": "255712345678", 
            "sms": "Test message",
            "status_id": "delivered",
            "status_description": "Message delivered",
            "credits": 1,
            "created_at": "2024-01-15T10:30:00Z",
            "sender_id": "TEST_SENDER"
        }
        
        # Verify all expected fields are present
        for field in expected_fields:
            self.assertIn(field, sample_message)

    def test_delivery_status_model(self):
        """Test DeliveryStatus model creation"""
        from notify_africa.models import DeliveryStatus
        
        status = DeliveryStatus(
            sms_id="123",
            recipient="255712345678",
            status="delivered", 
            status_description="Message delivered successfully",
            credits=1
        )
        
        self.assertEqual(status.sms_id, "123")
        self.assertEqual(status.recipient, "255712345678")
        self.assertEqual(status.status, "delivered")
        self.assertEqual(status.status_description, "Message delivered successfully")
        self.assertEqual(status.credits, 1)


if __name__ == '__main__':
    unittest.main()
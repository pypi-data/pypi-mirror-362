# Notify Africa Python SMS SDK

A Python SDK for integrating with Notify Africa SMS service, allowing developers to easily send SMS messages through their Python applications.

## Features

- ✅ **Authentication** - API key and sender ID management
- 📤 **Send Single SMS** - Send SMS to individual recipients
- 📦 **Send Bulk SMS** - Send SMS to multiple recipients
- 🕒 **Send Scheduled SMS** - Schedule SMS for future delivery
- 📁 **Excel Integration** - Send SMS from Excel files
- 📊 **Delivery Reports** - Check SMS delivery status
- 🛠️ **Developer Friendly** - Type hints, error handling, and comprehensive documentation

## Installation

```bash
pip install notify-africa-sms
```

## Quick Start

```python
from notify_africa import NotifyAfricaClient

# Initialize client
client = NotifyAfricaClient(
    api_key="your_api_key_here",
    sender_id="NOTIFYAFRICA"
)

# Send a single SMS
response = client.send_sms(
    phone_number="255712345678",
    message="Hello from Notify Africa!"
)

print(f"SMS sent: {response.success}")
print(f"Message: {response.message}")
print(f"Balance: {response.balance}")
```

## Usage Examples

### Send Single SMS

```python
response = client.send_sms(
    phone_number="255712345678", 
    message="Hello, this is a test message!"
)

if response.success:
    print(f"SMS sent successfully! ID: {response.sms_id}")
    print(f"Credits used: {response.credits_spent}")
    print(f"Remaining balance: {response.balance}")
else:
    print(f"Failed to send SMS: {response.message}")
```

### Send Bulk SMS

```python
phone_numbers = [
    "255712345678",
    "255687654321", 
    "255756789012"
]

response = client.send_bulk_sms(
    phone_numbers=phone_numbers,
    message="Bulk SMS message to all recipients"
)

print(f"Total messages: {response.total_messages}")
print(f"Successful: {response.successful_messages}")
print(f"Failed: {response.failed_messages}")
```

### Send Scheduled SMS

```python
from datetime import datetime, timedelta

# Schedule SMS for tomorrow at 10:00 AM
schedule_time = datetime.now() + timedelta(days=1)
schedule_time = schedule_time.replace(hour=10, minute=0, second=0)

response = client.send_scheduled_sms(
    phone_numbers=["255712345678"],
    message="This is a scheduled message",
    schedule_time=schedule_time
)

print(f"Scheduled SMS: {response.success}")
```

### Send SMS from Excel File

Create an Excel file with columns: `phone`, `names`, `message` (optional)

```python
# Using message template with name placeholder
response = client.send_sms_from_excel(
    file_path="contacts.xlsx",
    message_template="Hello {names}, welcome to our service!",
    phone_column="phone",
    names_column="names"
)

# Or using individual messages from Excel
response = client.send_sms_from_excel(
    file_path="contacts.xlsx",
    message_column="message",
    phone_column="phone"
)

print(f"Sent {response.successful_messages} out of {response.total_messages} SMS")
```

### Check SMS History

```python
history = client.get_sms_history(records=50)
print(f"Retrieved {len(history.get('data', []))} SMS records")
```

### Get Sender IDs

```python
sender_ids = client.get_sender_ids()
for sender in sender_ids:
    print(f"Sender ID: {sender.name} - Status: {sender.status}")
```

## SMS Status and History Tracking

The Notify Africa Python SDK provides comprehensive methods to track SMS delivery status and retrieve SMS history.

### Check SMS History

Retrieve your SMS sending history with detailed information about each message:

```python
# Get recent SMS history (default: 50 records)
history = client.get_sms_history()

# Get specific number of records
history = client.get_sms_history(records=100)

# Process the history data
messages = history.get('data', [])
print(f"Total messages retrieved: {len(messages)}")

for message in messages:
    print(f"SMS ID: {message.get('id')}")
    print(f"Recipient: {message.get('recipient')}")
    print(f"Message: {message.get('sms')}")
    print(f"Status: {message.get('status_id')}")
    print(f"Status Description: {message.get('status_description')}")
    print(f"Credits Used: {message.get('credits')}")
    print(f"Sent At: {message.get('created_at')}")
    print(f"Sender ID: {message.get('sender_id')}")
    print("-" * 40)
```

### Check Individual SMS Status

Check the delivery status of a specific SMS using its ID:

```python
# Get SMS ID from send response
response = client.send_sms("255712345678", "Test message")
sms_id = response.sms_id

# Check delivery status
status = client.get_delivery_status(sms_id)

if status:
    print(f"SMS ID: {status.sms_id}")
    print(f"Recipient: {status.recipient}")
    print(f"Status: {status.status}")
    print(f"Description: {status.status_description}")
    print(f"Credits: {status.credits}")
else:
    print("SMS not found or status unavailable")
```

### SMS Status Codes

The following status codes are commonly returned:

| Status Code | Description |
|-------------|-------------|
| `pending` | SMS is queued for delivery |
| `sent` | SMS has been sent to the carrier |
| `delivered` | SMS was successfully delivered |
| `failed` | SMS delivery failed |
| `expired` | SMS expired before delivery |
| `rejected` | SMS was rejected by the carrier |

### Advanced History Filtering

```python
# Get comprehensive SMS history with filtering
def get_filtered_sms_history(client, days_back=7, status_filter=None):
    """
    Get filtered SMS history
    
    Args:
        client: NotifyAfricaClient instance
        days_back: Number of days to look back
        status_filter: Filter by specific status (optional)
    """
    from datetime import datetime, timedelta
    
    # Get recent history (API typically returns newest first)
    history = client.get_sms_history(records=500)
    messages = history.get('data', [])
    
    # Filter by date range
    cutoff_date = datetime.now() - timedelta(days=days_back)
    filtered_messages = []
    
    for msg in messages:
        try:
            # Parse message date
            msg_date = datetime.fromisoformat(
                msg.get('created_at', '').replace('Z', '+00:00')
            )
            
            # Check if within date range
            if msg_date >= cutoff_date:
                # Apply status filter if specified
                if status_filter is None or msg.get('status_id') == status_filter:
                    filtered_messages.append(msg)
        except:
            continue
    
    return filtered_messages

# Usage examples
recent_messages = get_filtered_sms_history(client, days_back=7)
failed_messages = get_filtered_sms_history(client, days_back=30, status_filter='failed')
delivered_messages = get_filtered_sms_history(client, days_back=7, status_filter='delivered')

print(f"Recent messages (7 days): {len(recent_messages)}")
print(f"Failed messages (30 days): {len(failed_messages)}")
print(f"Delivered messages (7 days): {len(delivered_messages)}")
```

### Bulk Status Checking

Check status for multiple SMS messages:

```python
def check_bulk_sms_status(client, sms_ids):
    """
    Check status for multiple SMS messages
    
    Args:
        client: NotifyAfricaClient instance
        sms_ids: List of SMS IDs to check
    """
    results = []
    
    for sms_id in sms_ids:
        status = client.get_delivery_status(sms_id)
        if status:
            results.append({
                'sms_id': status.sms_id,
                'recipient': status.recipient,
                'status': status.status,
                'description': status.status_description
            })
        else:
            results.append({
                'sms_id': sms_id,
                'status': 'not_found',
                'description': 'SMS not found in history'
            })
    
    return results

# Usage
sms_ids = ['123', '124', '125']  # Your SMS IDs
statuses = check_bulk_sms_status(client, sms_ids)

for status in statuses:
    print(f"SMS {status['sms_id']}: {status['status']} - {status['description']}")
```

### Real-time Status Monitoring

Monitor SMS delivery in real-time:

```python
import time
from datetime import datetime

def monitor_sms_delivery(client, sms_id, timeout=300):
    """
    Monitor SMS delivery status until delivered or timeout
    
    Args:
        client: NotifyAfricaClient instance
        sms_id: SMS ID to monitor
        timeout: Maximum time to wait in seconds (default: 5 minutes)
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        status = client.get_delivery_status(sms_id)
        
        if status:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] SMS {sms_id}: {status.status}")
            
            # Check if final status reached
            if status.status in ['delivered', 'failed', 'expired', 'rejected']:
                return status
        
        time.sleep(10)  # Wait 10 seconds before checking again
    
    print(f"Timeout reached for SMS {sms_id}")
    return None

# Usage
response = client.send_sms("255712345678", "Test message")
if response.success:
    final_status = monitor_sms_delivery(client, response.sms_id)
    if final_status:
        print(f"Final status: {final_status.status}")
```

### Export SMS History

Export SMS history to different formats:

```python
import pandas as pd
from datetime import datetime

def export_sms_history(client, records=1000, format='csv'):
    """
    Export SMS history to file
    
    Args:
        client: NotifyAfricaClient instance
        records: Number of records to export
        format: Export format ('csv', 'excel', 'json')
    """
    # Get SMS history
    history = client.get_sms_history(records=records)
    messages = history.get('data', [])
    
    if not messages:
        print("No SMS history found")
        return
    
    # Create DataFrame
    df = pd.DataFrame(messages)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format.lower() == 'csv':
        filename = f"sms_history_{timestamp}.csv"
        df.to_csv(filename, index=False)
    elif format.lower() == 'excel':
        filename = f"sms_history_{timestamp}.xlsx"
        df.to_excel(filename, index=False)
    elif format.lower() == 'json':
        filename = f"sms_history_{timestamp}.json"
        df.to_json(filename, orient='records', indent=2)
    
    print(f"SMS history exported to: {filename}")
    return filename

# Usage
export_sms_history(client, records=500, format='excel')
```

### Error Handling for Status Checks

```python
from notify_africa.exceptions import (
    AuthenticationError,
    NetworkError,
    NotifyAfricaException
)

def safe_status_check(client, sms_id):
    """Safely check SMS status with error handling"""
    try:
        status = client.get_delivery_status(sms_id)
        return status
    except AuthenticationError:
        print("Authentication failed - check your API key")
        return None
    except NetworkError as e:
        print(f"Network error: {e}")
        return None
    except NotifyAfricaException as e:
        print(f"API error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def safe_history_check(client, records=50):
    """Safely get SMS history with error handling"""
    try:
        history = client.get_sms_history(records=records)
        return history.get('data', [])
    except AuthenticationError:
        print("Authentication failed - check your API key")
        return []
    except NetworkError as e:
        print(f"Network error: {e}")
        return []
    except NotifyAfricaException as e:
        print(f"API error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

# Usage
status = safe_status_check(client, "123")
messages = safe_history_check(client, 100)
```
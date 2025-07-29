#!/usr/bin/env python3
"""
Example usage of Notify Africa SMS SDK

This script demonstrates all the key features of the SDK.
"""

import os
from datetime import datetime, timedelta
from notify_africa import NotifyAfricaClient
from notify_africa.exceptions import (
    AuthenticationError,
    ValidationError,
    InsufficientCreditsError,
    NetworkError
)


def main():
    # Initialize the client
    client = NotifyAfricaClient(
        api_key=os.getenv("NOTIFY_AFRICA_API_KEY", "1012|2743TDlWjSSPa5Iqg365kROzCtUFCZNpSVf2pivV3fbb7511"),
        sender_id=os.getenv("NOTIFY_AFRICA_SENDER_ID", "16")
    )
    
    try:
        # Example 1: Send single SMS
        print("1. Sending single SMS...")
        response = client.send_sms(
            phone_number="255689737839",
            message="Hello from Notify Africa Python SDK!"
        )
        print(f"   Success: {response.success}")
        print(f"   Message: {response.message}")
        print(f"   SMS ID: {response.sms_id}")
        print(f"   Credits spent: {response.credits_spent}")
        print(f"   Balance: {response.balance}")
        print()
        
        # Example 2: Send bulk SMS
        print("2. Sending bulk SMS...")
        phone_numbers = [
            "255689737839",
            "255743517612",
        ]
        response = client.send_bulk_sms(
            phone_numbers=phone_numbers,
            message="This is a bulk SMS message sent to multiple recipients."
        )
        print(f"   Success: {response.success}")
        print(f"   Total messages: {response.total_messages}")
        print(f"   Successful: {response.successful_messages}")
        print(f"   Failed: {response.failed_messages}")
        print(f"   Total credits: {response.total_credits}")
        print()
        
        # Example 3: Schedule SMS for future delivery
        print("3. Scheduling SMS...")
        schedule_time = datetime.now() + timedelta(hours=1)  # 1 hour from now
        response = client.send_scheduled_sms(
            phone_numbers=["255689737839"],
            message="This is a scheduled SMS message.",
            schedule_time=schedule_time
        )
        print(f"   Success: {response.success}")
        print(f"   Scheduled for: {schedule_time}")
        print()
        
        # Example 4: Get SMS history
        print("4. Getting SMS history...")
        history = client.get_sms_history(records=10)
        messages = history.get('data', [])
        print(f"   Retrieved {len(messages)} recent messages")
        for msg in messages[:3]:  # Show first 3
            print(f"   - ID: {msg.get('id')}, Recipient: {msg.get('recipient')}, Status: {msg.get('status_id')}")
        print()
        
        # Example 5: Get sender IDs
        print("5. Getting sender IDs...")
        sender_ids = client.get_sender_ids()
        print(f"   Found {len(sender_ids)} sender IDs:")
        for sender in sender_ids:
            print(f"   - {sender.name} (Status: {sender.status})")
        print()
        
        # Example 6: Get user profile
        print("6. Getting user profile...")
        profile = client.get_profile()
        user_data = profile.get('data', {})
        print(f"   User: {user_data.get('first_name')} {user_data.get('last_name')}")
        print(f"   Email: {user_data.get('email')}")
        print(f"   Balance: {user_data.get('balance')} SMS credits")
        print()
        
        print("✅ All examples completed successfully!")
        
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("Please check your API key.")
        
    except InsufficientCreditsError as e:
        print(f"❌ Insufficient credits: {e}")
        print("Please recharge your account.")
        
    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        print("Please check your input parameters.")
        
    except NetworkError as e:
        print(f"❌ Network error: {e}")
        print("Please check your internet connection.")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    print("Notify Africa SMS SDK - Example Usage")
    print("=" * 40)
    print()
    
    # Check for required environment variables
    if not os.getenv("NOTIFY_AFRICA_API_KEY"):
        print("⚠️  Warning: NOTIFY_AFRICA_API_KEY environment variable not set.")
        print("   Set it with: export NOTIFY_AFRICA_API_KEY='your_api_key'")
        print()
    
    if not os.getenv("NOTIFY_AFRICA_SENDER_ID"):
        print("⚠️  Warning: NOTIFY_AFRICA_SENDER_ID environment variable not set.")
        print("   Set it with: export NOTIFY_AFRICA_SENDER_ID='YOUR_SENDER_ID'")
        print()
    
    main()
import os
import traceback
from typing import Any, Optional
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
import shippo
from shippo.models import components, operations


# Initialize FastMCP server
mcp = FastMCP("shippo")

def get_shippo_client():
    """Get configured Shippo client using API key from environment."""
    api_key = os.getenv("SHIPPO_API_KEY")
    if not api_key:
        raise ValueError("SHIPPO_API_KEY environment variable is required")
    
    return shippo.Shippo(api_key_header=api_key)

def format_detailed_error(operation: str, error: Exception, context: Optional[dict] = None) -> str:
    """Format detailed error information for the LLM."""
    error_details = {
        "operation": operation,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "traceback": traceback.format_exc()
    }
    
    formatted_error = f"""
❌ ERROR in {operation}:

Error Type: {error_details['error_type']}
Message: {error_details['error_message']}
"""
    
    # Check for HTTP/API-specific errors
    if hasattr(error, 'status_code'):
        formatted_error += f"HTTP Status: {getattr(error, 'status_code')}\n"
    
    if hasattr(error, 'response'):
        formatted_error += f"Response: {str(getattr(error, 'response'))}\n"
    
    if hasattr(error, 'body'):
        formatted_error += f"Response Body: {str(getattr(error, 'body'))}\n"
    
    if context:
        formatted_error += f"\nContext: {str(context)}\n"
    
    formatted_error += f"\nFull Traceback:\n{error_details['traceback']}"
    
    return formatted_error

@mcp.prompt(title="Shippo MCP Server Overview")
def shippo_overview() -> list[base.Message]:
    return [
        base.UserMessage("What does the Shippo MCP server do?"),
        base.AssistantMessage("""I'm an AI assistant with access to Shippo shipping tools for complete shipping operations.

## Key Safety Notes
⚠️ **API Key Types:**
- Test keys (shippo_test_*): Safe for development, no charges
- Live keys (shippo_live_*): Real charges apply for label creation!

## Available Operations
- **Address validation** - Ensure deliverable addresses
- **Shipping rates** - Get real-time quotes from multiple carriers  
- **Shipment management** - Create and track shipments
- **Label generation** - Create shipping labels from rates
- **Package tracking** - Track packages with detailed history
- **Refund processing** - Handle shipping label refunds
- **International shipping** - Full customs declaration support
  - Create customs items with accurate declarations
  - Build customs declarations with proper documentation
  - Attach customs to shipments for international shipping
  - Support for all incoterms (DDU, DDP, DAP, FCA, eDAP)

## International Shipping Workflow
🌍 For shipments crossing borders:
1. Create customs items (create_customs_item)
2. Create customs declaration (create_customs_declaration) 
3. Create shipment with customs (create_shipment_with_customs)
4. Get rates and purchase label normally

I'll guide you through each step and always confirm details before any paid operations."""),
    ]

@mcp.tool()
async def validate_address(
    name: str,
    street1: str,
    city: str,
    state: str,
    zip_code: str,
    country: str = "US",
    street2: str = "",
    company: str = "",
    phone: str = "",
    email: str = ""
) -> str:
    """Validate a shipping address using Shippo's address validation.
    
    Required fields: name, street1, city, state, zip_code
    Optional fields: street2, company, phone, email
    Default country: "US"
    
    Use this before getting shipping rates to ensure deliverable addresses.

    Args:
        name: Recipient name
        street1: Primary street address
        city: City name
        state: State/province code
        zip_code: ZIP/postal code
        country: Country code (default: US)
        street2: Secondary address line (optional)
        company: Company name (optional)
        phone: Phone number (optional)
        email: Email address (optional)
    """
    try:
        client = get_shippo_client()
        
        address_request = components.AddressCreateRequest(
            name=name,
            street1=street1,
            street2=street2,
            city=city,
            state=state,
            zip=zip_code,
            country=country,
            company=company,
            phone=phone,
            email=email,
            validate=True
        )
        
        address = client.addresses.create(address_request)
        
        return f"""
Address ID: {getattr(address, 'object_id', 'N/A')}
Name: {getattr(address, 'name', 'N/A')}
Company: {getattr(address, 'company', 'N/A')}
Street: {getattr(address, 'street1', '')} {getattr(address, 'street2', '') or ''}
City: {getattr(address, 'city', 'N/A')}
State: {getattr(address, 'state', 'N/A')}
ZIP: {getattr(address, 'zip', 'N/A')}
Country: {getattr(address, 'country', 'N/A')}
Phone: {getattr(address, 'phone', 'N/A')}
Email: {getattr(address, 'email', 'N/A')}
Valid: {getattr(getattr(address, 'validation_results', {}), 'is_valid', 'Unknown')}
"""
        
    except Exception as e:
        context = {
            "name": name,
            "street1": street1,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "country": country
        }
        return format_detailed_error("validate_address", e, context)

@mcp.tool()
async def get_shipping_rates(
    from_name: str,
    from_street1: str,
    from_city: str,
    from_state: str,
    from_zip: str,
    to_name: str,
    to_street1: str,
    to_city: str,
    to_state: str,
    to_zip: str,
    length: float,
    width: float,
    height: float,
    weight: float,
    from_country: str = "US",
    to_country: str = "US",
    distance_unit: str = "in",
    mass_unit: str = "lb"
) -> str:
    """Get shipping rates for a package between two addresses.
    
    📦 IMPORTANT: Always confirm package dimensions and weight with user before proceeding!
    📋 Present rates clearly showing carrier, service, price, and delivery time.
    🎯 Highlight most economical and fastest options.
    
    Workflow: validate addresses → confirm dimensions → get rates → present options

    Args:
        from_name: Sender name
        from_street1: Sender street address
        from_city: Sender city
        from_state: Sender state
        from_zip: Sender ZIP code
        to_name: Recipient name
        to_street1: Recipient street address
        to_city: Recipient city
        to_state: Recipient state
        to_zip: Recipient ZIP code
        length: Package length
        width: Package width
        height: Package height
        weight: Package weight
        from_country: Sender country (default: US)
        to_country: Recipient country (default: US)
        distance_unit: Distance unit (in/cm, default: in)
        mass_unit: Mass unit (lb/kg, default: lb)
    """
    try:
        client = get_shippo_client()
        
        address_from = components.AddressCreateRequest(
            name=from_name,
            street1=from_street1,
            city=from_city,
            state=from_state,
            zip=from_zip,
            country=from_country
        )
        
        address_to = components.AddressCreateRequest(
            name=to_name,
            street1=to_street1,
            city=to_city,
            state=to_state,
            zip=to_zip,
            country=to_country
        )
        
        parcel = components.ParcelCreateRequest(
            length=str(length),
            width=str(width),
            height=str(height),
            weight=str(weight),
            distance_unit=components.DistanceUnitEnum.IN if distance_unit == "in" else components.DistanceUnitEnum.CM,
            mass_unit=components.WeightUnitEnum.LB if mass_unit == "lb" else components.WeightUnitEnum.KG
        )
        
        shipment_request = components.ShipmentCreateRequest(
            address_from=address_from,
            address_to=address_to,
            parcels=[parcel],
            async_=False
        )
        
        shipment = client.shipments.create(shipment_request)
        rates = getattr(shipment, 'rates', [])
        
        if not rates:
            return "No shipping rates found for this shipment."
        
        formatted_rates = []
        for rate in rates:
            rate_info = f"""
Rate ID: {getattr(rate, 'object_id', 'N/A')}
Carrier: {getattr(rate, 'provider', 'N/A')}
Service: {getattr(getattr(rate, 'servicelevel', {}), 'name', 'N/A')}
Amount: ${getattr(rate, 'amount', 'N/A')} {getattr(rate, 'currency', '')}
Transit Time: {getattr(rate, 'estimated_days', 'N/A')} days
"""
            formatted_rates.append(rate_info)
        
        return "\n---\n".join(formatted_rates)
        
    except Exception as e:
        context = {
            "from_address": f"{from_name}, {from_street1}, {from_city}, {from_state} {from_zip}",
            "to_address": f"{to_name}, {to_street1}, {to_city}, {to_state} {to_zip}",
            "package_dimensions": f"{length}x{width}x{height} {distance_unit}",
            "package_weight": f"{weight} {mass_unit}"
        }
        return format_detailed_error("get_shipping_rates", e, context)

@mcp.tool()
async def create_shipping_label(rate_id: str) -> str:
    """Create a shipping label from a rate ID.
    
    ⚠️ SAFETY: This creates a paid shipping label! Confirm rate selection with user first.
    💰 Live API keys will charge your account. Test keys are safe for development.
    🔄 Use exact rate_id from get_shipping_rates or get_shipment results.
    
    📝 NOTE: For international shipments, attach customs declaration when creating the shipment,
    not when purchasing the label. Use create_shipment_with_customs() for international shipping.
    
    Returns tracking number, label URL, and transaction ID for potential refunds.

    Args:
        rate_id: The ID of the rate to purchase
    """
    try:
        client = get_shippo_client()
        
        transaction_request = components.TransactionCreateRequest(
            rate=rate_id,
            label_file_type=components.LabelFileTypeEnum.PDF,
            async_=False
        )
        
        transaction = client.transactions.create(transaction_request)
        
        # Check if transaction failed and provide detailed error info
        status = getattr(transaction, 'status', 'N/A')
        if status == 'ERROR' or str(status) == 'TransactionStatusEnum.ERROR':
            error_details = f"""
❌ TRANSACTION FAILED:

Transaction ID: {getattr(transaction, 'object_id', 'N/A')}
Status: {status}
Rate ID Used: {rate_id}

Error Messages:
"""
            # Check for various error message fields
            messages = getattr(transaction, 'messages', [])
            if messages:
                for msg in messages:
                    if hasattr(msg, 'text'):
                        error_details += f"- {getattr(msg, 'text', 'Unknown error')}\n"
                    elif hasattr(msg, 'message'):
                        error_details += f"- {getattr(msg, 'message', 'Unknown error')}\n"
                    else:
                        error_details += f"- {str(msg)}\n"
            
            # Check for error field
            if hasattr(transaction, 'error'):
                error_details += f"- {getattr(transaction, 'error', 'Unknown error')}\n"
            
            # Check for object_status field which might contain more info
            if hasattr(transaction, 'object_status'):
                error_details += f"- Object Status: {getattr(transaction, 'object_status', 'N/A')}\n"
                
            # Add rate validation suggestion
            error_details += """
💡 Common Solutions:
- Rate ID may be expired (rates expire after ~10 minutes)
- Rate may be invalid for the selected service
- Account may lack permissions for this carrier
- Try getting fresh rates with get_shipping_rates()
"""
            return error_details
        
        # Success case
        return f"""
✅ SHIPPING LABEL CREATED SUCCESSFULLY:

Transaction ID: {getattr(transaction, 'object_id', 'N/A')}
Status: {status}
Tracking Number: {getattr(transaction, 'tracking_number', 'N/A')}
Label URL: {getattr(transaction, 'label_url', 'N/A')}
Tracking URL: {getattr(transaction, 'tracking_url_provider', 'N/A')}
"""
        
    except Exception as e:
        context = {
            "rate_id": rate_id
        }
        return format_detailed_error("create_shipping_label", e, context)

@mcp.tool()
async def track_package(tracking_number: str, carrier: str) -> str:
    """Track a package using its tracking number.
    
    📋 Both tracking number AND carrier name are required.
    📊 Presents tracking history in chronological order.
    
    Common carriers: 'usps', 'ups', 'fedex', 'dhl'

    Args:
        tracking_number: The tracking number
        carrier: The carrier name (e.g., 'usps', 'ups', 'fedex')
    """
    try:
        client = get_shippo_client()
        
        tracking = client.tracking_status.get(tracking_number, carrier)
        tracking_status = getattr(tracking, 'tracking_status', {})
        
        result = f"""
Tracking Number: {getattr(tracking, 'tracking_number', 'N/A')}
Carrier: {getattr(tracking, 'carrier', 'N/A')}
Status: {getattr(tracking_status, 'status', 'N/A')}
Status Details: {getattr(tracking_status, 'status_details', 'N/A')}
"""
        
        # Add tracking history if available
        history = getattr(tracking, 'tracking_history', [])
        if history:
            result += "\n\nTracking History:\n"
            for event in history[-5:]:  # Show last 5 events
                result += f"- {getattr(event, 'status_date', 'N/A')}: {getattr(event, 'status_details', 'N/A')}\n"
        
        return result
        
    except Exception as e:
        context = {
            "tracking_number": tracking_number,
            "carrier": carrier
        }
        return format_detailed_error("track_package", e, context)

@mcp.tool()
async def list_carrier_accounts() -> str:
    """List all configured carrier accounts.
    
    📋 Shows all carrier accounts configured for your Shippo account.
    🎯 Active accounts can be used for shipping rates and labels.
    ℹ️ Useful for troubleshooting rate availability issues.
    """
    try:
        client = get_shippo_client()
        
        accounts = client.carrier_accounts.list(operations.ListCarrierAccountsRequest())
        results = getattr(accounts, 'results', [])
        
        if not results:
            return "No carrier accounts found."
        
        formatted_accounts = []
        for account in results:
            account_info = f"""
Carrier: {getattr(account, 'carrier', 'N/A')}
Account ID: {getattr(account, 'object_id', 'N/A')}
Active: {getattr(account, 'active', 'N/A')}
"""
            formatted_accounts.append(account_info)
        
        return "\n---\n".join(formatted_accounts)
        
    except Exception as e:
        return format_detailed_error("list_carrier_accounts", e)

@mcp.tool()
async def create_shipment(
    from_name: str,
    from_street1: str,
    from_city: str,
    from_state: str,
    from_zip: str,
    to_name: str,
    to_street1: str,
    to_city: str,
    to_state: str,
    to_zip: str,
    length: float,
    width: float,
    height: float,
    weight: float,
    from_country: str = "US",
    to_country: str = "US",
    distance_unit: str = "in",
    mass_unit: str = "lb"
) -> str:
    """Create a shipment and get basic info.
    
    📦 IMPORTANT: Always confirm package dimensions and weight with user before proceeding!
    🎯 This creates a shipment object but doesn't purchase labels (no charges).
    📋 Use get_shipment() with the returned ID to see all available rates.

    Args:
        from_name: Sender name
        from_street1: Sender street address
        from_city: Sender city
        from_state: Sender state
        from_zip: Sender ZIP code
        to_name: Recipient name
        to_street1: Recipient street address
        to_city: Recipient city
        to_state: Recipient state
        to_zip: Recipient ZIP code
        length: Package length
        width: Package width
        height: Package height
        weight: Package weight
        from_country: Sender country (default: US)
        to_country: Recipient country (default: US)
        distance_unit: Distance unit (in/cm, default: in)
        mass_unit: Mass unit (lb/kg, default: lb)
    """
    try:
        client = get_shippo_client()
        
        address_from = components.AddressCreateRequest(
            name=from_name,
            street1=from_street1,
            city=from_city,
            state=from_state,
            zip=from_zip,
            country=from_country
        )
        
        address_to = components.AddressCreateRequest(
            name=to_name,
            street1=to_street1,
            city=to_city,
            state=to_state,
            zip=to_zip,
            country=to_country
        )
        
        parcel = components.ParcelCreateRequest(
            length=str(length),
            width=str(width),
            height=str(height),
            weight=str(weight),
            distance_unit=components.DistanceUnitEnum.IN if distance_unit == "in" else components.DistanceUnitEnum.CM,
            mass_unit=components.WeightUnitEnum.LB if mass_unit == "lb" else components.WeightUnitEnum.KG
        )
        
        shipment_request = components.ShipmentCreateRequest(
            address_from=address_from,
            address_to=address_to,
            parcels=[parcel],
            async_=False
        )
        
        shipment = client.shipments.create(shipment_request)
        rates = getattr(shipment, 'rates', [])
        
        from_addr = getattr(shipment, 'address_from', {})
        to_addr = getattr(shipment, 'address_to', {})
        
        return f"""
Shipment ID: {getattr(shipment, 'object_id', 'N/A')}
Status: {getattr(shipment, 'status', 'N/A')}
From: {getattr(from_addr, 'city', 'N/A')}, {getattr(from_addr, 'state', 'N/A')}
To: {getattr(to_addr, 'city', 'N/A')}, {getattr(to_addr, 'state', 'N/A')}
Total Rates: {len(rates)}
"""
        
    except Exception as e:
        context = {
            "from_address": f"{from_name}, {from_street1}, {from_city}, {from_state} {from_zip}",
            "to_address": f"{to_name}, {to_street1}, {to_city}, {to_state} {to_zip}",
            "package_dimensions": f"{length}x{width}x{height} {distance_unit}",
            "package_weight": f"{weight} {mass_unit}"
        }
        return format_detailed_error("create_shipment", e, context)

@mcp.tool()
async def list_shipments() -> str:
    """List all shipments for the account.
    
    📋 Shows all shipments with basic info and available rate counts.
    🎯 Use get_shipment() with a specific shipment ID for detailed rates.
    🔗 Get shipment IDs from this list to manage existing shipments.
    """
    try:
        client = get_shippo_client()
        
        shipments = client.shipments.list(operations.ListShipmentsRequest())
        results = getattr(shipments, 'results', [])
        
        if not results:
            return "No shipments found."
        
        formatted_shipments = []
        for shipment in results:
            from_addr = getattr(shipment, 'address_from', {})
            to_addr = getattr(shipment, 'address_to', {})
            rates = getattr(shipment, 'rates', [])
            
            shipment_info = f"""
Shipment ID: {getattr(shipment, 'object_id', 'N/A')}
Status: {getattr(shipment, 'status', 'N/A')}
Created: {getattr(shipment, 'object_created', 'N/A')}
From: {getattr(from_addr, 'city', 'N/A')}, {getattr(from_addr, 'state', 'N/A')}
To: {getattr(to_addr, 'city', 'N/A')}, {getattr(to_addr, 'state', 'N/A')}
Available Rates: {len(rates)}
"""
            formatted_shipments.append(shipment_info)
        
        return "\n---\n".join(formatted_shipments)
        
    except Exception as e:
        return format_detailed_error("list_shipments", e)

@mcp.tool()
async def get_shipment(shipment_id: str) -> str:
    """Get detailed information about a specific shipment, including all available rates.
    
    📋 Shows complete shipment details, addresses, parcels, and all available rates.
    🎯 Use the rate IDs from this output with create_shipping_label() to purchase labels.
    
    Perfect for reviewing shipment details before purchasing labels.

    Args:
        shipment_id: The ID of the shipment to retrieve
    """
    try:
        client = get_shippo_client()
        
        shipment = client.shipments.get(shipment_id)
        
        from_addr = getattr(shipment, 'address_from', {})
        to_addr = getattr(shipment, 'address_to', {})
        rates = getattr(shipment, 'rates', [])
        parcels = getattr(shipment, 'parcels', [])
        
        result = f"""
Shipment ID: {getattr(shipment, 'object_id', 'N/A')}
Status: {getattr(shipment, 'status', 'N/A')}
Created: {getattr(shipment, 'object_created', 'N/A')}

From Address:
  Name: {getattr(from_addr, 'name', 'N/A')}
  Address: {getattr(from_addr, 'street1', 'N/A')}
  City: {getattr(from_addr, 'city', 'N/A')}, {getattr(from_addr, 'state', 'N/A')} {getattr(from_addr, 'zip', 'N/A')}

To Address:
  Name: {getattr(to_addr, 'name', 'N/A')}
  Address: {getattr(to_addr, 'street1', 'N/A')}
  City: {getattr(to_addr, 'city', 'N/A')}, {getattr(to_addr, 'state', 'N/A')} {getattr(to_addr, 'zip', 'N/A')}
"""
        
        # Add parcel information
        if parcels:
            result += "\nParcels:\n"
            for i, parcel in enumerate(parcels):
                result += f"  Parcel {i+1}: {getattr(parcel, 'length', 'N/A')}x{getattr(parcel, 'width', 'N/A')}x{getattr(parcel, 'height', 'N/A')} {getattr(parcel, 'distance_unit', '')}, {getattr(parcel, 'weight', 'N/A')} {getattr(parcel, 'mass_unit', '')}\n"
        
        # Add rate information
        if rates:
            result += "\nAvailable Rates:\n"
            for rate in rates:
                result += f"""
  Rate ID: {getattr(rate, 'object_id', 'N/A')}
  Carrier: {getattr(rate, 'provider', 'N/A')}
  Service: {getattr(getattr(rate, 'servicelevel', {}), 'name', 'N/A')}
  Amount: ${getattr(rate, 'amount', 'N/A')} {getattr(rate, 'currency', '')}
  Transit Time: {getattr(rate, 'estimated_days', 'N/A')} days
"""
        else:
            result += "\nNo rates available for this shipment."
        
        return result
        
    except Exception as e:
        context = {
            "shipment_id": shipment_id
        }
        return format_detailed_error("get_shipment", e, context)

@mcp.tool()
async def get_transaction(transaction_id: str) -> str:
    """Get detailed information about a specific transaction, including error details if failed.
    
    🔍 Perfect for diagnosing failed transactions and understanding why labels weren't created.
    📋 Shows complete transaction details, error messages, and troubleshooting guidance.
    
    Use this when you have a transaction ID and need to understand what went wrong.

    Args:
        transaction_id: The ID of the transaction to retrieve
    """
    try:
        client = get_shippo_client()
        
        transaction = client.transactions.get(transaction_id)
        
        status = getattr(transaction, 'status', 'N/A')
        rate = getattr(transaction, 'rate', {})
        
        result = f"""
Transaction Details:
═══════════════════

Transaction ID: {getattr(transaction, 'object_id', 'N/A')}
Status: {status}
Created: {getattr(transaction, 'object_created', 'N/A')}
Test Mode: {'Yes' if getattr(transaction, 'test', False) else 'No'}

Rate Information:
  Rate ID: {getattr(rate, 'object_id', 'N/A')}
  Carrier: {getattr(rate, 'provider', 'N/A')}
  Service: {getattr(getattr(rate, 'servicelevel', {}), 'name', 'N/A')}
  Amount: ${getattr(rate, 'amount', 'N/A')} {getattr(rate, 'currency', '')}
"""
        
        if status == 'ERROR' or str(status) == 'TransactionStatusEnum.ERROR':
            result += "\n❌ TRANSACTION FAILED - Error Details:\n"
            
            # Check for error messages
            messages = getattr(transaction, 'messages', [])
            if messages:
                result += "\nError Messages:\n"
                for msg in messages:
                    if hasattr(msg, 'text'):
                        result += f"- {getattr(msg, 'text', 'Unknown error')}\n"
                    elif hasattr(msg, 'message'):
                        result += f"- {getattr(msg, 'message', 'Unknown error')}\n"
                    else:
                        result += f"- {str(msg)}\n"
            
            if hasattr(transaction, 'error'):
                result += f"\nError Field: {getattr(transaction, 'error', 'N/A')}\n"
                
            result += """
💡 Troubleshooting Steps:
1. Check if rate ID is still valid (rates expire after ~10 minutes)
2. Verify account has permissions for this carrier
3. Ensure sufficient account balance for live transactions
4. Try creating a fresh shipment and getting new rates
"""
        else:
            result += f"""

✅ Transaction Details:
  Tracking Number: {getattr(transaction, 'tracking_number', 'N/A')}
  Label URL: {getattr(transaction, 'label_url', 'N/A')}
  Tracking URL: {getattr(transaction, 'tracking_url_provider', 'N/A')}
"""
        
        return result
        
    except Exception as e:
        context = {
            "transaction_id": transaction_id
        }
        return format_detailed_error("get_transaction", e, context)

@mcp.tool()
async def list_transactions() -> str:
    """List all shipping label transactions to find transaction IDs for refunds.
    
    🔍 Use this to find transaction IDs for purchased shipping labels.
    💰 Transaction IDs are needed to create refunds with create_refund().
    📋 Shows status, tracking numbers, costs, and label URLs.
    """
    try:
        client = get_shippo_client()
        
        transactions = client.transactions.list(operations.ListTransactionsRequest())
        results = getattr(transactions, 'results', [])
        
        if not results:
            return "No transactions found."
        
        formatted_transactions = []
        for transaction in results:
            rate = getattr(transaction, 'rate', {})
            
            transaction_info = f"""
Transaction ID: {getattr(transaction, 'object_id', 'N/A')}
Status: {getattr(transaction, 'status', 'N/A')}
Tracking Number: {getattr(transaction, 'tracking_number', 'N/A')}
Carrier: {getattr(rate, 'provider', 'N/A')}
Service: {getattr(getattr(rate, 'servicelevel', {}), 'name', 'N/A')}
Amount: ${getattr(rate, 'amount', 'N/A')} {getattr(rate, 'currency', '')}
Created: {getattr(transaction, 'object_created', 'N/A')}
Label URL: {getattr(transaction, 'label_url', 'N/A')}
"""
            formatted_transactions.append(transaction_info)
        
        return "\n---\n".join(formatted_transactions)
        
    except Exception as e:
        return format_detailed_error("list_transactions", e)

@mcp.tool()
async def create_refund(transaction_id: str) -> str:
    """Create a refund for a shipping label transaction.
    
    💰 Refunds can only be created for purchased shipping labels.
    🔍 Use list_transactions() to find transaction IDs from purchased labels.
    ⏱️ Refund eligibility depends on carrier policies and timing.
    📋 Returns refund ID and status - use get_refund() for detailed tracking.

    Args:
        transaction_id: The ID of the transaction to refund
    """
    try:
        client = get_shippo_client()
        
        refund = client.refunds.create(transaction_id)
        
        return f"""
Refund ID: {getattr(refund, 'object_id', 'N/A')}
Status: {getattr(refund, 'status', 'N/A')}
Transaction ID: {getattr(refund, 'transaction', 'N/A')}
"""
        
    except Exception as e:
        context = {
            "transaction_id": transaction_id
        }
        return format_detailed_error("create_refund", e, context)

@mcp.tool()
async def list_refunds() -> str:
    """List all refunds for the account with detailed status information.
    
    📊 Shows refund status with helpful icons and test/live indicators.
    🔍 Use get_refund() with specific refund ID for comprehensive details.
    
    Status meanings: ⏳ Queued | 🔄 Pending | ✅ Success | ❌ Error
    """
    try:
        client = get_shippo_client()
        
        refunds = client.refunds.list()
        results = getattr(refunds, 'results', [])
        
        if not results:
            return "No refunds found."
        
        formatted_refunds = []
        for refund in results:
            status = getattr(refund, 'status', 'N/A')
            status_icon = {
                'QUEUED': '⏳',
                'PENDING': '🔄',
                'SUCCESS': '✅',
                'ERROR': '❌'
            }.get(status, '❓')
            
            test_indicator = '🧪 TEST' if getattr(refund, 'test', False) else '💰 LIVE'
            
            refund_info = f"""
{status_icon} Refund ID: {getattr(refund, 'object_id', 'N/A')} ({test_indicator})
Status: {status}
Transaction ID: {getattr(refund, 'transaction', 'N/A')}
Created: {getattr(refund, 'object_created', 'N/A')}
Last Updated: {getattr(refund, 'object_updated', 'N/A')}
"""
            formatted_refunds.append(refund_info)
        
        header = f"""
Refund Summary ({len(results)} total):
═══════════════════════════

Legend: ⏳ Queued | 🔄 Pending | ✅ Success | ❌ Error | 🧪 Test Mode | 💰 Live Mode
"""
        
        return header + "\n---\n".join(formatted_refunds)
        
    except Exception as e:
        return format_detailed_error("list_refunds", e)

@mcp.tool()
async def get_refund(refund_id: str) -> str:
    """Get comprehensive details of a specific refund including status, dates, and transaction info.
    
    📋 Provides complete refund details including status explanations.
    🔗 Links back to original transaction details when available.
    📊 Includes helpful status guide and timeline information.

    Args:
        refund_id: The ID of the refund to retrieve
    """
    try:
        client = get_shippo_client()
        
        refund = client.refunds.get(refund_id)
        
        # Get the transaction details if available
        transaction_id = getattr(refund, 'transaction', 'N/A')
        transaction_details = ""
        
        if transaction_id != 'N/A':
            try:
                transaction = client.transactions.get(transaction_id)
                rate = getattr(transaction, 'rate', {})
                transaction_details = f"""

Transaction Details:
  Transaction ID: {transaction_id}
  Tracking Number: {getattr(transaction, 'tracking_number', 'N/A')}
  Carrier: {getattr(rate, 'provider', 'N/A')}
  Service: {getattr(getattr(rate, 'servicelevel', {}), 'name', 'N/A')}
  Amount: ${getattr(rate, 'amount', 'N/A')} {getattr(rate, 'currency', '')}
  Label URL: {getattr(transaction, 'label_url', 'N/A')}
"""
            except Exception as inner_e:
                transaction_details = f"\n\nTransaction ID: {transaction_id} (details not available: {str(inner_e)})"
        
        # Format status with explanation
        status = getattr(refund, 'status', 'N/A')
        status_explanation = {
            'QUEUED': 'Refund request has been queued for processing',
            'PENDING': 'Refund is being processed by the carrier',
            'SUCCESS': 'Refund has been successfully processed',
            'ERROR': 'There was an error processing the refund'
        }.get(status, 'Unknown status')
        
        return f"""
Refund Details:
═══════════════

Refund ID: {getattr(refund, 'object_id', 'N/A')}
Status: {status} ({status_explanation})
Test Mode: {'Yes' if getattr(refund, 'test', False) else 'No'}

Dates:
  Created: {getattr(refund, 'object_created', 'N/A')}
  Last Updated: {getattr(refund, 'object_updated', 'N/A')}

Ownership:
  Created By: {getattr(refund, 'object_owner', 'N/A')}
{transaction_details}

💡 Refund Status Guide:
   • QUEUED: Your refund request is in line for processing
   • PENDING: The carrier is currently processing your refund
   • SUCCESS: Refund completed - you should see the credit soon
   • ERROR: Issue with refund - contact support if needed
"""
        
    except Exception as e:
        context = {
            "refund_id": refund_id
        }
        return format_detailed_error("get_refund", e, context)

@mcp.tool()
async def create_customs_item(
    description: str,
    quantity: int,
    net_weight: float,
    mass_unit: str,
    value_amount: float,
    value_currency: str,
    origin_country: str,
    tariff_number: str = "",
    sku_code: str = "",
    hs_code: str = "",
    metadata: str = ""
) -> str:
    """Create a new customs item for use in customs declarations.
    
    📦 Required for international shipments - each item in the package needs a customs item.
    💰 Declare accurate values - customs authorities verify declared values.
    🏷️ Use specific descriptions - avoid generic terms like "gift" or "merchandise".
    
    📏 IMPORTANT VALIDATION LIMITS:
    - description: Must be 30 characters or less
    
    Use these customs items when creating customs declarations for international shipping.

    Args:
        description: Item description (be specific, e.g., "Cotton T-shirt" not "Clothing") (MAX 30 characters)
        quantity: Number of this item in the shipment
        net_weight: Weight of the item
        mass_unit: Weight unit ("lb" or "kg")
        value_amount: Declared value of the item
        value_currency: Currency code (e.g., "USD", "EUR")
        origin_country: Country where item was manufactured (ISO code, e.g., "US")
        tariff_number: Harmonized tariff number (optional but recommended)
        sku_code: Stock keeping unit/product code (optional)
        hs_code: Harmonized System code (optional)
        metadata: Additional metadata (optional)
    """
    try:
        client = get_shippo_client()
        
        # Validate description length
        if len(description) > 30:
            return f"❌ VALIDATION ERROR: description must be 30 characters or less. Current length: {len(description)} characters.\n\nProvided: '{description}'\n\n💡 Try shortening to something like: '{description[:27]}...'"
        
        customs_item_request = components.CustomsItemCreateRequest(
            description=description,
            quantity=quantity,
            net_weight=str(net_weight),
            mass_unit=components.WeightUnitEnum.LB if mass_unit.lower() == "lb" else components.WeightUnitEnum.KG,
            value_amount=str(value_amount),
            value_currency=value_currency,
            origin_country=origin_country,
            tariff_number=tariff_number if tariff_number else None,
            sku_code=sku_code if sku_code else None,
            hs_code=hs_code if hs_code else None,
            metadata=metadata if metadata else None
        )
        
        customs_item = client.customs_items.create(customs_item_request)
        
        return f"""
✅ CUSTOMS ITEM CREATED:

Customs Item ID: {getattr(customs_item, 'object_id', 'N/A')}
Description: {getattr(customs_item, 'description', 'N/A')}
Quantity: {getattr(customs_item, 'quantity', 'N/A')}
Weight: {getattr(customs_item, 'net_weight', 'N/A')} {getattr(customs_item, 'mass_unit', 'N/A')}
Value: {getattr(customs_item, 'value_currency', 'N/A')} {getattr(customs_item, 'value_amount', 'N/A')}
Origin Country: {getattr(customs_item, 'origin_country', 'N/A')}
Tariff Number: {getattr(customs_item, 'tariff_number', 'N/A')}
SKU Code: {getattr(customs_item, 'sku_code', 'N/A')}
HS Code: {getattr(customs_item, 'hs_code', 'N/A')}
"""
        
    except Exception as e:
        context = {
            "description": description,
            "quantity": quantity,
            "value_amount": value_amount,
            "origin_country": origin_country
        }
        return format_detailed_error("create_customs_item", e, context)

@mcp.tool()
async def list_customs_items() -> str:
    """List all customs items for the account.
    
    📋 Shows all previously created customs items with their details.
    🔗 Use customs item IDs when creating customs declarations.
    💡 Reuse customs items for similar products across multiple shipments.
    """
    try:
        client = get_shippo_client()
        
        customs_items = client.customs_items.list()
        results = getattr(customs_items, 'results', [])
        
        if not results:
            return "No customs items found."
        
        formatted_items = []
        for item in results:
            item_info = f"""
Customs Item ID: {getattr(item, 'object_id', 'N/A')}
Description: {getattr(item, 'description', 'N/A')}
Quantity: {getattr(item, 'quantity', 'N/A')}
Weight: {getattr(item, 'net_weight', 'N/A')} {getattr(item, 'mass_unit', 'N/A')}
Value: {getattr(item, 'value_currency', 'N/A')} {getattr(item, 'value_amount', 'N/A')}
Origin: {getattr(item, 'origin_country', 'N/A')}
Created: {getattr(item, 'object_created', 'N/A')}
"""
            formatted_items.append(item_info)
        
        return "\n---\n".join(formatted_items)
        
    except Exception as e:
        return format_detailed_error("list_customs_items", e)

@mcp.tool()
async def get_customs_item(customs_item_id: str) -> str:
    """Retrieve detailed information about a specific customs item.
    
    📋 Shows complete customs item details including all declared values.
    🔍 Useful for verifying customs item details before using in declarations.

    Args:
        customs_item_id: The ID of the customs item to retrieve
    """
    try:
        client = get_shippo_client()
        
        customs_item = client.customs_items.get(customs_item_id)
        
        return f"""
Customs Item Details:
════════════════════

Customs Item ID: {getattr(customs_item, 'object_id', 'N/A')}
Description: {getattr(customs_item, 'description', 'N/A')}
Quantity: {getattr(customs_item, 'quantity', 'N/A')}
Net Weight: {getattr(customs_item, 'net_weight', 'N/A')} {getattr(customs_item, 'mass_unit', 'N/A')}
Value: {getattr(customs_item, 'value_currency', 'N/A')} {getattr(customs_item, 'value_amount', 'N/A')}
Origin Country: {getattr(customs_item, 'origin_country', 'N/A')}
Tariff Number: {getattr(customs_item, 'tariff_number', 'N/A')}
HS Tariff Number: {getattr(customs_item, 'hs_tariff_number', 'N/A')}
SKU: {getattr(customs_item, 'sku', 'N/A')}
Metadata: {getattr(customs_item, 'metadata', 'N/A')}
Created: {getattr(customs_item, 'object_created', 'N/A')}
Updated: {getattr(customs_item, 'object_updated', 'N/A')}
"""
        
    except Exception as e:
        context = {
            "customs_item_id": customs_item_id
        }
        return format_detailed_error("get_customs_item", e, context)

def map_contents_type_enum(contents_type: str):
    """Map string to CustomsDeclarationContentsTypeEnum."""
    mapping = {
        "DOCUMENTS": components.CustomsDeclarationContentsTypeEnum.DOCUMENTS,
        "GIFT": components.CustomsDeclarationContentsTypeEnum.GIFT,
        "SAMPLE": components.CustomsDeclarationContentsTypeEnum.SAMPLE,
        "MERCHANDISE": components.CustomsDeclarationContentsTypeEnum.MERCHANDISE,
        "HUMANITARIAN_DONATION": components.CustomsDeclarationContentsTypeEnum.HUMANITARIAN_DONATION,
        "RETURN_MERCHANDISE": components.CustomsDeclarationContentsTypeEnum.RETURN_MERCHANDISE,
        "OTHER": components.CustomsDeclarationContentsTypeEnum.OTHER,
    }
    return mapping.get(contents_type.upper(), components.CustomsDeclarationContentsTypeEnum.MERCHANDISE)

def map_non_delivery_option_enum(option: str):
    """Map string to CustomsDeclarationNonDeliveryOptionEnum."""
    mapping = {
        "RETURN": components.CustomsDeclarationNonDeliveryOptionEnum.RETURN,
        "ABANDON": components.CustomsDeclarationNonDeliveryOptionEnum.ABANDON,
    }
    return mapping.get(option.upper(), components.CustomsDeclarationNonDeliveryOptionEnum.RETURN)

def map_incoterm_enum(incoterm: str):
    """Map string to CustomsDeclarationIncotermEnum."""
    mapping = {
        "DDP": components.CustomsDeclarationIncotermEnum.DDP,
        "DDU": components.CustomsDeclarationIncotermEnum.DDU,
        "FCA": components.CustomsDeclarationIncotermEnum.FCA,
        "DAP": components.CustomsDeclarationIncotermEnum.DAP,
        "EDAP": components.CustomsDeclarationIncotermEnum.E_DAP,
    }
    return mapping.get(incoterm.upper()) if incoterm else None

@mcp.tool()
async def create_customs_declaration(
    contents_type: str,
    contents_explanation: str,
    invoice: str,
    license: str,
    certificate: str,
    notes: str,
    eel_pfc: str,
    aes_itn: str,
    non_delivery_option: str,
    certify: bool,
    certify_signer: str,
    disclaimer: str,
    incoterm: str,
    items: str,
    b13a_filing_option: str = "",
    metadata: str = ""
) -> str:
    """Create a new customs declaration for international shipments.
    
    🌍 REQUIRED for all international shipments crossing borders.
    📋 Must include all items being shipped with accurate declarations.
    ⚠️ Inaccurate customs declarations can cause delays, fees, or confiscation.
    
    📏 IMPORTANT VALIDATION LIMITS:
    - contents_explanation: Must be 25 characters or less
    - customs item descriptions: Must be 30 characters or less (validated when creating items)
    
    Common values:
    - contents_type: "MERCHANDISE", "GIFT", "SAMPLE", "DOCUMENTS", "RETURN_MERCHANDISE", "HUMANITARIAN_DONATION", "OTHER"
    - non_delivery_option: "RETURN", "ABANDON"
    - incoterm: "DDU" (buyer pays duties), "DDP" (seller pays duties), "DAP", "FCA", "EDAP"
    - eel_pfc: Usually "NOEEI_30_37_A" for items under $2500, or leave empty

    Args:
        contents_type: Type of contents ("MERCHANDISE", "GIFT", "SAMPLE", "DOCUMENTS", "RETURN_MERCHANDISE", "HUMANITARIAN_DONATION", "OTHER")
        contents_explanation: Brief description of shipment contents (MAX 25 characters)
        invoice: Invoice number for commercial shipments
        license: Export/import license number if required
        certificate: Certificate number if required  
        notes: Additional notes for customs
        eel_pfc: Electronic Export Information filing citation (use "NOEEI_30_37_A" for under $2500 or leave empty)
        aes_itn: Automated Export System Internal Transaction Number
        non_delivery_option: What to do if undeliverable ("RETURN" or "ABANDON")
        certify: Whether you certify the information is accurate
        certify_signer: Name of person certifying the declaration
        disclaimer: Disclaimer text
        incoterm: International commercial terms ("DDU", "DDP", "DAP", "FCA", "EDAP")
        items: Comma-separated list of customs item IDs to include
        b13a_filing_option: B13A filing option for Canada ("FILED_ELECTRONICALLY" or leave empty)
        metadata: Additional metadata (optional)
    """
    try:
        client = get_shippo_client()
        
        # Validate contents_explanation length
        if len(contents_explanation) > 25:
            return f"❌ VALIDATION ERROR: contents_explanation must be 25 characters or less. Current length: {len(contents_explanation)} characters.\n\nProvided: '{contents_explanation}'\n\n💡 Try shortening to something like: '{contents_explanation[:22]}...'"
        
        # Parse items list
        item_ids = [item.strip() for item in items.split(',') if item.strip()]
        if not item_ids:
            return "❌ ERROR: At least one customs item ID is required. Create customs items first with create_customs_item()."
        
        # Retrieve customs items and create CustomsItemCreateRequest objects
        customs_items = []
        for item_id in item_ids:
            try:
                customs_item = client.customs_items.get(item_id)
                item_request = components.CustomsItemCreateRequest(
                    description=getattr(customs_item, 'description', ''),
                    quantity=getattr(customs_item, 'quantity', 1),
                    net_weight=str(getattr(customs_item, 'net_weight', '0')),
                    mass_unit=getattr(customs_item, 'mass_unit', components.WeightUnitEnum.LB),
                    value_amount=str(getattr(customs_item, 'value_amount', '0')),
                    value_currency=getattr(customs_item, 'value_currency', 'USD'),
                    origin_country=getattr(customs_item, 'origin_country', 'US'),
                    tariff_number=getattr(customs_item, 'tariff_number', None),
                    sku_code=getattr(customs_item, 'sku_code', None),
                    hs_code=getattr(customs_item, 'hs_code', None),
                    metadata=getattr(customs_item, 'metadata', None)
                )
                customs_items.append(item_request)
            except Exception as item_error:
                return f"❌ ERROR: Could not retrieve customs item {item_id}: {str(item_error)}"
        
        # Map enum values
        contents_type_enum = map_contents_type_enum(contents_type)
        non_delivery_option_enum = map_non_delivery_option_enum(non_delivery_option)
        incoterm_enum = map_incoterm_enum(incoterm)
        
        # Handle optional enum fields
        eel_pfc_enum = None
        if eel_pfc and eel_pfc.upper() == "NOEEI_30_37_A":
            eel_pfc_enum = components.CustomsDeclarationEelPfcEnum.NOEEI_30_37_A
        
        b13a_filing_option_enum = None
        if b13a_filing_option and b13a_filing_option.upper() == "FILED_ELECTRONICALLY":
            b13a_filing_option_enum = components.CustomsDeclarationB13AFilingOptionEnum.FILED_ELECTRONICALLY
        
        customs_declaration_request = components.CustomsDeclarationCreateRequest(
            contents_type=contents_type_enum,
            contents_explanation=contents_explanation,
            invoice=invoice,
            license=license,
            certificate=certificate,
            notes=notes,
            eel_pfc=eel_pfc_enum,
            aes_itn=aes_itn,
            non_delivery_option=non_delivery_option_enum,
            certify=certify,
            certify_signer=certify_signer,
            disclaimer=disclaimer,
            incoterm=incoterm_enum,
            items=customs_items,
            b13a_filing_option=b13a_filing_option_enum,
            metadata=metadata if metadata else None
        )
        
        customs_declaration = client.customs_declarations.create(customs_declaration_request)
        
        return f"""
✅ CUSTOMS DECLARATION CREATED:

Customs Declaration ID: {getattr(customs_declaration, 'object_id', 'N/A')}
Contents Type: {getattr(customs_declaration, 'contents_type', 'N/A')}
Contents Explanation: {getattr(customs_declaration, 'contents_explanation', 'N/A')}
Certify: {getattr(customs_declaration, 'certify', 'N/A')}
Certify Signer: {getattr(customs_declaration, 'certify_signer', 'N/A')}
Non-Delivery Option: {getattr(customs_declaration, 'non_delivery_option', 'N/A')}
Incoterm: {getattr(customs_declaration, 'incoterm', 'N/A')}
Items Count: {len(getattr(customs_declaration, 'items', []))}

💡 Use this Customs Declaration ID when creating shipping labels for international shipments.
"""
        
    except Exception as e:
        context = {
            "contents_type": contents_type,
            "items": items,
            "certify_signer": certify_signer
        }
        return format_detailed_error("create_customs_declaration", e, context)

@mcp.tool()
async def list_customs_declarations() -> str:
    """List all customs declarations for the account.
    
    📋 Shows all previously created customs declarations with basic info.
    🔗 Use customs declaration IDs when creating international shipping labels.
    🌍 Required for any shipment crossing international borders.
    """
    try:
        client = get_shippo_client()
        
        customs_declarations = client.customs_declarations.list()
        results = getattr(customs_declarations, 'results', [])
        
        if not results:
            return "No customs declarations found."
        
        formatted_declarations = []
        for declaration in results:
            items = getattr(declaration, 'items', [])
            
            declaration_info = f"""
Customs Declaration ID: {getattr(declaration, 'object_id', 'N/A')}
Contents Type: {getattr(declaration, 'contents_type', 'N/A')}
Contents Explanation: {getattr(declaration, 'contents_explanation', 'N/A')}
Certify Signer: {getattr(declaration, 'certify_signer', 'N/A')}
Items Count: {len(items)}
Incoterm: {getattr(declaration, 'incoterm', 'N/A')}
Created: {getattr(declaration, 'object_created', 'N/A')}
"""
            formatted_declarations.append(declaration_info)
        
        return "\n---\n".join(formatted_declarations)
        
    except Exception as e:
        return format_detailed_error("list_customs_declarations", e)

@mcp.tool()
async def get_customs_declaration(customs_declaration_id: str) -> str:
    """Retrieve detailed information about a specific customs declaration.
    
    📋 Shows complete customs declaration details including all items.
    🔍 Useful for verifying declaration details before using with shipping labels.

    Args:
        customs_declaration_id: The ID of the customs declaration to retrieve
    """
    try:
        client = get_shippo_client()
        
        customs_declaration = client.customs_declarations.get(customs_declaration_id)
        items = getattr(customs_declaration, 'items', [])
        
        result = f"""
Customs Declaration Details:
═══════════════════════════

Declaration ID: {getattr(customs_declaration, 'object_id', 'N/A')}
Contents Type: {getattr(customs_declaration, 'contents_type', 'N/A')}
Contents Explanation: {getattr(customs_declaration, 'contents_explanation', 'N/A')}
Invoice: {getattr(customs_declaration, 'invoice', 'N/A')}
License: {getattr(customs_declaration, 'license', 'N/A')}
Certificate: {getattr(customs_declaration, 'certificate', 'N/A')}
Notes: {getattr(customs_declaration, 'notes', 'N/A')}
EEL PFC: {getattr(customs_declaration, 'eel_pfc', 'N/A')}
AES ITN: {getattr(customs_declaration, 'aes_itn', 'N/A')}
Non-Delivery Option: {getattr(customs_declaration, 'non_delivery_option', 'N/A')}
Certify: {getattr(customs_declaration, 'certify', 'N/A')}
Certify Signer: {getattr(customs_declaration, 'certify_signer', 'N/A')}
Disclaimer: {getattr(customs_declaration, 'disclaimer', 'N/A')}
Incoterm: {getattr(customs_declaration, 'incoterm', 'N/A')}
B13A Filing Option: {getattr(customs_declaration, 'b13a_filing_option', 'N/A')}
Metadata: {getattr(customs_declaration, 'metadata', 'N/A')}
Created: {getattr(customs_declaration, 'object_created', 'N/A')}
Updated: {getattr(customs_declaration, 'object_updated', 'N/A')}

Included Items ({len(items)}):
"""
        
        if items:
            for i, item_id in enumerate(items):
                result += f"  {i+1}. Item ID: {item_id}\n"
        else:
            result += "  No items found\n"
        
        return result
        
    except Exception as e:
        context = {
            "customs_declaration_id": customs_declaration_id
        }
        return format_detailed_error("get_customs_declaration", e, context)

@mcp.tool()
async def create_shipment_with_customs(
    from_name: str,
    from_street1: str,
    from_city: str,
    from_state: str,
    from_zip: str,
    to_name: str,
    to_street1: str,
    to_city: str,
    to_state: str,
    to_zip: str,
    length: float,
    width: float,
    height: float,
    weight: float,
    customs_declaration_id: str,
    from_country: str = "US",
    to_country: str = "US",
    distance_unit: str = "in",
    mass_unit: str = "lb"
) -> str:
    """Create a shipment with customs declaration for international shipping.
    
    🌍 REQUIRED for international shipments crossing borders.
    📦 IMPORTANT: Always confirm package dimensions and weight with user before proceeding!
    📋 Must include a valid customs declaration ID created with create_customs_declaration().
    🎯 This creates a shipment object with customs attached but doesn't purchase labels (no charges).
    
    Workflow: create customs items → create customs declaration → create shipment with customs → get rates → purchase label

    Args:
        from_name: Sender name
        from_street1: Sender street address
        from_city: Sender city
        from_state: Sender state
        from_zip: Sender ZIP code
        to_name: Recipient name
        to_street1: Recipient street address
        to_city: Recipient city
        to_state: Recipient state
        to_zip: Recipient ZIP code
        length: Package length
        width: Package width
        height: Package height
        weight: Package weight
        customs_declaration_id: ID of the customs declaration to attach
        from_country: Sender country (default: US)
        to_country: Recipient country (default: US)
        distance_unit: Distance unit (in/cm, default: in)
        mass_unit: Mass unit (lb/kg, default: lb)
    """
    try:
        client = get_shippo_client()
        
        address_from = components.AddressCreateRequest(
            name=from_name,
            street1=from_street1,
            city=from_city,
            state=from_state,
            zip=from_zip,
            country=from_country
        )
        
        address_to = components.AddressCreateRequest(
            name=to_name,
            street1=to_street1,
            city=to_city,
            state=to_state,
            zip=to_zip,
            country=to_country
        )
        
        parcel = components.ParcelCreateRequest(
            length=str(length),
            width=str(width),
            height=str(height),
            weight=str(weight),
            distance_unit=components.DistanceUnitEnum.IN if distance_unit == "in" else components.DistanceUnitEnum.CM,
            mass_unit=components.WeightUnitEnum.LB if mass_unit == "lb" else components.WeightUnitEnum.KG
        )
        
        shipment_request = components.ShipmentCreateRequest(
            address_from=address_from,
            address_to=address_to,
            parcels=[parcel],
            customs_declaration=customs_declaration_id,
            async_=False
        )
        
        shipment = client.shipments.create(shipment_request)
        rates = getattr(shipment, 'rates', [])
        
        from_addr = getattr(shipment, 'address_from', {})
        to_addr = getattr(shipment, 'address_to', {})
        customs_dec = getattr(shipment, 'customs_declaration', {})
        
        return f"""
✅ INTERNATIONAL SHIPMENT CREATED WITH CUSTOMS:

Shipment ID: {getattr(shipment, 'object_id', 'N/A')}
Status: {getattr(shipment, 'status', 'N/A')}
From: {getattr(from_addr, 'city', 'N/A')}, {getattr(from_addr, 'state', 'N/A')} ({getattr(from_addr, 'country', 'N/A')})
To: {getattr(to_addr, 'city', 'N/A')}, {getattr(to_addr, 'state', 'N/A')} ({getattr(to_addr, 'country', 'N/A')})
Customs Declaration: {getattr(customs_dec, 'object_id', customs_declaration_id)}
Available Rates: {len(rates)}

🎯 Next Steps:
1. Use get_shipment() with this Shipment ID to see all available rates
2. Choose a rate and use create_shipping_label() to purchase the label
3. The customs declaration will automatically be included with the label
"""
        
    except Exception as e:
        context = {
            "from_address": f"{from_name}, {from_street1}, {from_city}, {from_state} {from_zip} ({from_country})",
            "to_address": f"{to_name}, {to_street1}, {to_city}, {to_state} {to_zip} ({to_country})",
            "package_dimensions": f"{length}x{width}x{height} {distance_unit}",
            "package_weight": f"{weight} {mass_unit}",
            "customs_declaration_id": customs_declaration_id
        }
        return format_detailed_error("create_shipment_with_customs", e, context)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='streamable-http', mount_path='/mcp')
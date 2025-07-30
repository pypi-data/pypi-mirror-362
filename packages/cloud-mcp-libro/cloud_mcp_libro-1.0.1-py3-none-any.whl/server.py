#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: limo
@date: 2025-01-01

Cloud Platform MCP Server (English Version)
Provides access to backend APIs through MCP protocol
Fixed encoding issues by using English logs
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

# Set console encoding to UTF-8
if sys.platform == "win32":
    try:
        os.system("chcp 65001 >nul 2>&1")
    except:
        pass

# Set environment variables for UTF-8 encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

try:
    import aiohttp
    import mcp.server.stdio
    import mcp.types as types
    from mcp.server import Server
    from pydantic import BaseModel
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("Please run: pip install aiohttp mcp pydantic")
    sys.exit(1)

# Configure logging - output to stderr to avoid interfering with MCP protocol
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(stream=sys.stderr)
    ]
)

logger = logging.getLogger("cloud-mcp")

class CloudMCPConfig(BaseModel):
    """MCP Configuration"""
    base_url: str = "https://demo-api.dl-aiot.com"
    username: str = ""
    password: str = ""
    timezone: str = "Asia/Shanghai"
    country: str = "China"
    app_sn: str = "eeec1ea2b23b11e1234"
    app_id: int = 1
    phone_brand: str = "IOS"
    phone_system: int = 1
    phone_system_version: str = "1"
    
    def validate_config(self) -> list[str]:
        """Validate configuration and return error messages"""
        errors = []
        if not self.username:
            errors.append("CLOUD_USERNAME not configured")
        if not self.password:
            errors.append("CLOUD_PASSWORD not configured")
        if not self.base_url:
            errors.append("CLOUD_BASE_URL not configured")
        elif not (self.base_url.startswith("http://") or self.base_url.startswith("https://")):
            errors.append("CLOUD_BASE_URL must start with http:// or https://")
        return errors

class AuthToken(BaseModel):
    """Authentication Token"""
    token: str
    refresh_token: str
    user_id: str
    email: str
    expires_at: datetime

class CloudMCPServer:
    """Cloud Platform MCP Server"""
    
    def __init__(self):
        self.config = CloudMCPConfig()
        self.auth_token: Optional[AuthToken] = None
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def initialize(self):
        """Initialize server"""
        # Read configuration from environment variables
        self.config.base_url = os.getenv("CLOUD_BASE_URL", self.config.base_url)
        self.config.username = os.getenv("CLOUD_USERNAME", "")
        self.config.password = os.getenv("CLOUD_PASSWORD", "")
        self.config.timezone = os.getenv("CLOUD_TIMEZONE", self.config.timezone)
        self.config.country = os.getenv("CLOUD_COUNTRY", self.config.country)
        self.config.app_sn = os.getenv("CLOUD_APP_SN", self.config.app_sn)
        self.config.app_id = int(os.getenv("CLOUD_APP_ID", str(self.config.app_id)))
        self.config.phone_brand = os.getenv("CLOUD_PHONE_BRAND", self.config.phone_brand)
        self.config.phone_system = int(os.getenv("CLOUD_PHONE_SYSTEM", str(self.config.phone_system)))
        self.config.phone_system_version = os.getenv("CLOUD_PHONE_SYSTEM_VERSION", self.config.phone_system_version)
        
        # Validate configuration
        config_errors = self.config.validate_config()
        if config_errors:
            logger.warning("Configuration warnings:")
            for error in config_errors:
                logger.warning(f"  - {error}")
        
        # Create SSL context for development environment
        import ssl
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Create connector
        connector = aiohttp.TCPConnector(
            ssl=ssl_context,
            limit=100,
            limit_per_host=10
        )
        
        # Create HTTP session
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30),
            headers={"Content-Type": "application/json"}
        )
        
        logger.debug(f"Cloud MCP Server initialized - Base URL: {self.config.base_url}")
        
    async def cleanup(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
            
    async def authenticate(self) -> bool:
        """User authentication"""
        # Check configuration
        config_errors = self.config.validate_config()
        if config_errors:
            logger.error("Authentication failed - configuration errors:")
            for error in config_errors:
                logger.error(f"  - {error}")
            return False
            
        if not self.session:
            logger.error("HTTP session not initialized")
            return False
            
        auth_url = f"{self.config.base_url}/member/auth/login"
        logger.debug(f"Attempting to authenticate user: {self.config.username}")
        logger.debug(f"Auth URL: {auth_url}")
        
        payload = {
            "email": self.config.username,
            "password": self.config.password,
            "appSn": self.config.app_sn,
            "appId": self.config.app_id,
            "timezone": self.config.timezone,
            "country": self.config.country,
            "phoneBrand": self.config.phone_brand,
            "phoneSystem": self.config.phone_system,
            "phoneSystemVersion": self.config.phone_system_version
        }
        
        # Set required headers
        headers = {
            'Content-Type': 'application/json',
            'source': 'IOS',
            'version': '1.0.0',
            'language': 'ZH'
        }
        
        try:
            async with self.session.post(auth_url, json=payload, headers=headers) as response:
                logger.debug(f"Auth response status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    logger.debug(f"Auth response: {result}")
                    
                    if result.get("code") == 0:
                        data = result.get("data", {})
                        self.auth_token = AuthToken(
                            token=data.get("token", ""),
                            refresh_token=data.get("refreshToken", ""),
                            user_id=str(data.get("memberId", "")),
                            email=data.get("email", ""),
                            expires_at=datetime.now() + timedelta(hours=24)  # Assume 24 hours expiry
                        )
                        logger.info(f"Authentication successful - User: {self.auth_token.email}, ID: {self.auth_token.user_id}")
                        return True
                    else:
                        logger.error(f"Authentication failed - Server error: {result.get('message', 'Unknown error')}")
                        logger.error(f"Error code: {result.get('code')}")
                else:
                    error_text = await response.text()
                    logger.error(f"Auth request failed - HTTP status: {response.status}")
                    logger.error(f"Response content: {error_text[:500]}")
                    
        except aiohttp.ClientConnectorError as e:
            logger.error(f"Connection error - Cannot connect to server: {self.config.base_url}")
            logger.error(f"Please check:")
            logger.error(f"  1. Server address is correct")
            logger.error(f"  2. Network connection is working")
            logger.error(f"  3. Server is running")
            logger.error(f"Detailed error: {str(e)}")
        except asyncio.TimeoutError as e:
            logger.error(f"Request timeout - Server response too slow: {str(e)}")
        except Exception as e:
            logger.error(f"Authentication exception: {type(e).__name__}: {str(e)}")
            
        return False
        
    async def is_token_valid(self) -> bool:
        """Check if token is valid"""
        if not self.auth_token:
            return False
        return datetime.now() < self.auth_token.expires_at
        
    async def ensure_authenticated(self) -> bool:
        """Ensure authenticated"""
        if not await self.is_token_valid():
            return await self.authenticate()
        return True
        
    async def make_authenticated_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request"""
        if not await self.ensure_authenticated():
            raise Exception("Authentication failed")
            
        if not self.session or not self.auth_token:
            raise Exception("Session or token not available")
            
        url = f"{self.config.base_url}{endpoint}"
        headers = kwargs.get("headers", {})
        headers.update({
            "Authorization": f"Bearer {self.auth_token.token}",
            "source": "IOS",
            "version": "1.0.0",
            "language": "ZH",
            "token": self.auth_token.token
        })
        kwargs["headers"] = headers
        
        async with self.session.request(method, url, **kwargs) as response:
            result = await response.json()
            return result

# Create MCP server instance
cloud_server = CloudMCPServer()
server = Server("cloud-mcp")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Return available tools list"""
    return [
        types.Tool(
            name="authenticate_user",
            description="Authenticate user with configured username and password",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_user_profile", 
            description="Get user profile information",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_device_list",
            description="Get list of bound devices",
            inputSchema={
                "type": "object",
                "properties": {
                    "roomId": {
                        "type": ["integer", "null"],
                        "description": "Room ID to filter devices (optional, null for all devices)"
                    }
                },
                "required": [],
            },
        ),
        types.Tool(
            name="manual_feeding",
            description="Manually feed pets using a feeding device",
            inputSchema={
                "type": "object",
                "properties": {
                    "deviceSn": {
                        "type": "string",
                        "description": "Device serial number (e.g., AF030136511656RL7)"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in seconds (default: 10)",
                        "default": 10
                    },
                    "grainNum": {
                        "type": "integer",
                        "description": "Amount of food to dispense (grain number, default: 1)",
                        "default": 1
                    },
                    "petIds": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Array of pet IDs (optional, empty array for all pets)",
                        "default": []
                    }
                },
                "required": ["deviceSn"],
            },
        ),
        types.Tool(
            name="add_feeding_plan",
            description="Add a feeding schedule plan for a device",
            inputSchema={
                "type": "object",
                "properties": {
                    "deviceSn": {
                        "type": "string",
                        "description": "Device serial number (e.g., AF030136511656RL7)"
                    },
                    "repeatDay": {
                        "type": "array",
                        "items": {"type": "integer", "minimum": 1, "maximum": 7},
                        "description": "Days of week to repeat (1=Monday, 2=Tuesday, ..., 7=Sunday). Will be converted to string format for API.",
                        "minItems": 1
                    },
                    "executionTime": {
                        "type": "string",
                        "description": "Execution time in HH:MM format (e.g., '18:07')",
                        "pattern": "^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"
                    },
                    "label": {
                        "type": "string",
                        "description": "Label for the feeding plan (e.g., 'weekday and weekends')"
                    },
                    "enableAudio": {
                        "type": "boolean",
                        "description": "Whether to enable audio notification (default: true)",
                        "default": True
                    },
                    "audioTimes": {
                        "type": "integer",
                        "description": "Number of audio notifications (default: 3)",
                        "default": 3,
                        "minimum": 1
                    },
                    "grainNum": {
                        "type": "integer",
                        "description": "Amount of food to dispense (grain number, default: 3)",
                        "default": 3,
                        "minimum": 1
                    },
                    "petIds": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Array of pet IDs (optional, empty array for all pets)",
                        "default": []
                    }
                },
                "required": ["deviceSn", "repeatDay", "executionTime", "label"],
            },
        ),
        types.Tool(
            name="get_feeding_plan_list",
            description="Get list of feeding plans for a device",
            inputSchema={
                "type": "object",
                "properties": {
                    "deviceId": {
                        "type": "string",
                        "description": "Device ID or serial number (e.g., AF030136511656RL7)"
                    }
                },
                "required": ["deviceId"],
            },
        ),
        types.Tool(
            name="remove_feeding_plan",
            description="Remove/delete a specific feeding plan",
            inputSchema={
                "type": "object",
                "properties": {
                    "deviceSn": {
                        "type": "string",
                        "description": "Device serial number (e.g., AF030136511656RL7)"
                    },
                    "planId": {
                        "type": "integer",
                        "description": "Plan ID to remove (e.g., 13264)"
                    },
                    "resetType": {
                        "type": "string",
                        "description": "Reset type (optional, default: empty string)",
                        "default": ""
                    },
                    "groupId": {
                        "type": "string",
                        "description": "Group ID (optional, default: empty string)",
                        "default": ""
                    }
                },
                "required": ["deviceSn", "planId"],
            },
        ),
        types.Tool(
            name="call_api",
            description="Call any API endpoint",
            inputSchema={
                "type": "object",
                "properties": {
                    "method": {
                        "type": "string",
                        "description": "HTTP method (GET, POST, PUT, DELETE)",
                        "enum": ["GET", "POST", "PUT", "DELETE"]
                    },
                    "endpoint": {
                        "type": "string",
                        "description": "API endpoint path, e.g.: /member/user/profile"
                    },
                    "data": {
                        "type": "object",
                        "description": "Request data (for POST/PUT)"
                    },
                    "params": {
                        "type": "object", 
                        "description": "Query parameters (for GET)"
                    }
                },
                "required": ["method", "endpoint"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""
    try:
        if name == "authenticate_user":
            success = await cloud_server.authenticate()
            if success and cloud_server.auth_token:
                return [types.TextContent(
                    type="text",
                    text=f"Authentication successful! User: {cloud_server.auth_token.email}, User ID: {cloud_server.auth_token.user_id}"
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text="Authentication failed, please check username and password configuration"
                )]
                
        elif name == "get_user_profile":
            result = await cloud_server.make_authenticated_request("POST", "/member/member/info")
            return [types.TextContent(
                type="text",
                text=f"User profile:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```"
            )]
            
        elif name == "get_device_list":
            room_id = arguments.get("roomId", None)
            payload = {"roomId": room_id}
            
            result = await cloud_server.make_authenticated_request("POST", "/device/device/list", json=payload)
            return [types.TextContent(
                type="text",
                text=f"Device list:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```"
            )]
            
        elif name == "manual_feeding":
            device_sn = arguments.get("deviceSn")
            if not device_sn:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: deviceSn is required for manual feeding"
                )]
            
            timeout = arguments.get("timeout", 10)
            grain_num = arguments.get("grainNum", 1)
            pet_ids = arguments.get("petIds", [])
            
            payload = {
                "deviceSn": device_sn,
                "timeout": timeout,
                "grainNum": grain_num,
                "petIds": pet_ids
            }
            
            result = await cloud_server.make_authenticated_request("POST", "/device/device/manualFeeding", json=payload)
            return [types.TextContent(
                type="text",
                text=f"Manual feeding result:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```"
            )]
            
        elif name == "add_feeding_plan":
            device_sn = arguments.get("deviceSn")
            repeat_day = arguments.get("repeatDay")
            execution_time = arguments.get("executionTime")
            label = arguments.get("label")
            
            # Validate required parameters
            if not device_sn:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: deviceSn is required for adding feeding plan"
                )]
            if not repeat_day or not isinstance(repeat_day, list):
                return [types.TextContent(
                    type="text",
                    text="❌ Error: repeatDay must be an array of weekday numbers (1-7, where 1=Monday, 7=Sunday)"
                )]
            if not execution_time:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: executionTime is required (format: HH:MM, e.g., '18:07')"
                )]
            if not label:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: label is required for the feeding plan"
                )]
            
            # Get optional parameters with defaults
            enable_audio = arguments.get("enableAudio", True)
            audio_times = arguments.get("audioTimes", 3)
            grain_num = arguments.get("grainNum", 3)
            pet_ids = arguments.get("petIds", [])
            
            # Convert repeatDay array to string format for API
            repeat_day_str = json.dumps(repeat_day)
            
            payload = {
                "deviceSn": device_sn,
                "repeatDay": repeat_day_str,
                "executionTime": execution_time,
                "label": label,
                "enableAudio": enable_audio,
                "audioTimes": audio_times,
                "grainNum": grain_num,
                "petIds": pet_ids
            }
            
            result = await cloud_server.make_authenticated_request("POST", "/device/feedingPlan/add", json=payload)
            return [types.TextContent(
                type="text",
                text=f"Add feeding plan result:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```"
            )]
            
        elif name == "get_feeding_plan_list":
            device_id = arguments.get("deviceId")
            if not device_id:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: deviceId is required for getting feeding plan list"
                )]
            
            payload = {"id": device_id}
            
            result = await cloud_server.make_authenticated_request("POST", "/device/feedingPlan/list", json=payload)
            return [types.TextContent(
                type="text",
                text=f"Feeding plan list:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```"
            )]
            
        elif name == "remove_feeding_plan":
            device_sn = arguments.get("deviceSn")
            plan_id = arguments.get("planId")
            
            # Validate required parameters
            if not device_sn:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: deviceSn is required for removing feeding plan"
                )]
            if plan_id is None:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: planId is required for removing feeding plan"
                )]
            
            # Get optional parameters with defaults
            reset_type = arguments.get("resetType", "")
            group_id = arguments.get("groupId", "")
            
            payload = {
                "deviceSn": device_sn,
                "resetType": reset_type,
                "planId": plan_id,
                "groupId": group_id
            }
            
            result = await cloud_server.make_authenticated_request("POST", "/device/feedingPlan/remove", json=payload)
            return [types.TextContent(
                type="text",
                text=f"Remove feeding plan result:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```"
            )]
            
        elif name == "call_api":
            method = arguments.get("method", "GET")
            endpoint = arguments.get("endpoint", "")
            data = arguments.get("data")
            params = arguments.get("params")
            
            kwargs = {}
            if data and method in ["POST", "PUT"]:
                kwargs["json"] = data
            if params and method == "GET":
                kwargs["params"] = params
                
            result = await cloud_server.make_authenticated_request(method, endpoint, **kwargs)
            return [types.TextContent(
                type="text",
                text=f"API call result:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```"
            )]
            
        else:
            return [types.TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
            
    except Exception as e:
        logger.error(f"Tool call error: {str(e)}")
        return [types.TextContent(
            type="text",
            text=f"Execution failed: {str(e)}"
        )]

async def main():
    """Main function"""
    # Note: Cannot use print because MCP uses stdio for JSON communication
    # Use logger to record startup information
    logger.info("Starting Cloud Platform MCP Server...")
    logger.info("Author: limo | Date: 2025-01-01") 
    logger.info("Encoding issues fixed with English logs")
    
    # Initialize server
    await cloud_server.initialize()
    
    try:
        # Run server
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    finally:
        # Clean up resources
        await cloud_server.cleanup()

def main_sync():
    """Synchronous entry point for uv/uvx execution"""
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main()) 
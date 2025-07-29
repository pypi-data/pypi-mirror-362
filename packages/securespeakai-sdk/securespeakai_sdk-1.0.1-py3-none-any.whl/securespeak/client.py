import requests
import json
import websocket
import threading
import time
from typing import Optional, Dict, Any, List, Union, Callable

class SecureSpeakClient:
    """
    SecureSpeak API Client
    
    A comprehensive client for interacting with the SecureSpeak API,
    supporting both API key and Firebase authentication.
    """
    
    BASE_URL = "https://securespeak-api-1064980124131.us-central1.run.app"
    
    def __init__(self, api_key: str, firebase_token: Optional[str] = None):
        """
        Initialize the SecureSpeak client
        
        Args:
            api_key (str): Your SecureSpeak API key
            firebase_token (str, optional): Firebase ID token for billing endpoints
        """
        self.api_key = api_key
        self.firebase_token = firebase_token
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.firebase_headers = self.headers.copy()
        
        if firebase_token:
            self.firebase_headers.update({
                "Authorization": f"Bearer {firebase_token}",
                "X-Firebase-Auth": "true"
            })
    
    def _make_request(self, method: str, endpoint: str, use_firebase_auth: bool = False, **kwargs) -> requests.Response:
        """
        Make HTTP request with proper error handling
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            use_firebase_auth (bool): Whether to use Firebase authentication
            **kwargs: Additional arguments for requests
            
        Returns:
            requests.Response: HTTP response object
            
        Raises:
            SecureSpeakAPIError: If the API returns an error
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = self.firebase_headers if use_firebase_auth else self.headers
        
        # Merge headers with any provided in kwargs
        if 'headers' in kwargs:
            headers = {**headers, **kwargs['headers']}
            del kwargs['headers']
        
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            try:
                error_data = response.json()
                raise SecureSpeakAPIError(
                    message=error_data.get('error', str(e)),
                    status_code=response.status_code,
                    details=error_data.get('details', {})
                )
            except json.JSONDecodeError:
                raise SecureSpeakAPIError(
                    message=f"HTTP {response.status_code}: {response.text}",
                    status_code=response.status_code
                )
        except requests.exceptions.RequestException as e:
            raise SecureSpeakAPIError(f"Request failed: {str(e)}")
    
    # Core Analysis Methods
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze uploaded audio file for AI-generated content
        
        Args:
            file_path (str): Path to the audio file
            
        Returns:
            Dict[str, Any]: Analysis results including label, confidence, and metadata
        """
        with open(file_path, "rb") as f:
            response = self._make_request(
                "POST",
                "/analyze_file",
                files={"file": f}
            )
        return response.json()
    
    def analyze_url(self, url: str) -> Dict[str, Any]:
        """
        Analyze audio from URL for AI-generated content
        
        Args:
            url (str): URL to the audio/video content
            
        Returns:
            Dict[str, Any]: Analysis results including label, confidence, and metadata
        """
        response = self._make_request(
            "POST",
            "/analyze_url",
            headers={"Content-Type": "application/json"},
            json={"url": url}
        )
        return response.json()
    
    def analyze_live(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze live audio with duration-based billing
        
        Args:
            file_path (str): Path to the audio file
            
        Returns:
            Dict[str, Any]: Analysis results including label, confidence, and metadata
        """
        with open(file_path, "rb") as f:
            response = self._make_request(
                "POST",
                "/analyze_live",
                files={"file": f}
            )
        return response.json()
    
    # Utility Methods
    def keep_alive(self) -> Dict[str, Any]:
        """
        Check if the API is alive and responsive
        
        Returns:
            Dict[str, Any]: Status information
        """
        response = self._make_request("GET", "/keep_alive")
        return response.json()
    
    # Billing Methods (require Firebase authentication)
    def get_billing_config(self) -> Dict[str, Any]:
        """
        Get billing configuration including pricing information
        
        Returns:
            Dict[str, Any]: Billing configuration and pricing
        """
        response = self._make_request("GET", "/api/billing/config")
        return response.json()
    
    def create_payment_intent(self, amount: float) -> Dict[str, Any]:
        """
        Create a Stripe Payment Intent for adding funds to balance
        
        Args:
            amount (float): Amount in USD to add to balance
            
        Returns:
            Dict[str, Any]: Payment intent details
            
        Raises:
            SecureSpeakAPIError: If Firebase authentication is not configured
        """
        if not self.firebase_token:
            raise SecureSpeakAPIError("Firebase authentication required for billing operations")
        
        response = self._make_request(
            "POST",
            "/api/billing/create-payment-intent",
            use_firebase_auth=True,
            json={"amount": amount}
        )
        return response.json()
    
    def get_balance(self) -> Dict[str, Any]:
        """
        Get current user balance and usage statistics
        
        Returns:
            Dict[str, Any]: Balance and usage information
            
        Raises:
            SecureSpeakAPIError: If Firebase authentication is not configured
        """
        if not self.firebase_token:
            raise SecureSpeakAPIError("Firebase authentication required for billing operations")
        
        response = self._make_request(
            "GET",
            "/api/billing/balance",
            use_firebase_auth=True
        )
        return response.json()
    
    # API Key Management Methods
    def get_key_stats(self, key_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get usage statistics for an API key
        
        Args:
            key_id (str, optional): API key ID. If None, uses current key
            
        Returns:
            Dict[str, Any]: Key usage statistics
        """
        if key_id is None:
            # Use current key - extract from headers or make a request to get it
            # For now, we'll require explicit key_id
            raise ValueError("key_id is required")
        
        response = self._make_request("GET", f"/api/key-stats/{key_id}")
        return response.json()
    
    def get_user_keys(self) -> List[Dict[str, Any]]:
        """
        Get all API keys for the current user
        
        Returns:
            List[Dict[str, Any]]: List of API keys
        """
        response = self._make_request("GET", "/api/keys")
        return response.json()
    
    def get_analysis_history(self, key_id: str, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """
        Get analysis history for an API key
        
        Args:
            key_id (str): API key ID
            limit (int): Maximum number of records to return (max 100)
            offset (int): Number of records to skip
            
        Returns:
            Dict[str, Any]: Analysis history and pagination info
        """
        params = {"limit": min(limit, 100), "offset": offset}
        response = self._make_request(
            "GET",
            f"/api/analysis-history/{key_id}",
            params=params
        )
        return response.json()
    
    # Debug Methods
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get debug information about the ML model
        
        Returns:
            Dict[str, Any]: Model information and status
        """
        response = self._make_request("GET", "/debug/model-info")
        return response.json()
    
    def get_model_hash(self) -> Dict[str, Any]:
        """
        Get debug information about the model hash
        
        Returns:
            Dict[str, Any]: Model hash and verification info
        """
        response = self._make_request("GET", "/debug/model-hash")
        return response.json()
    
    def get_environment_info(self) -> Dict[str, Any]:
        """
        Get debug information about the server environment
        
        Returns:
            Dict[str, Any]: Environment and library version info
        """
        response = self._make_request("GET", "/debug/environment")
        return response.json()
    
    # WebSocket Methods for Real-time Analysis
    def create_websocket_connection(self, on_message: Callable[[Dict[str, Any]], None]) -> 'WebSocketClient':
        """
        Create a WebSocket connection for real-time audio analysis
        
        Args:
            on_message (Callable): Callback function for receiving analysis results
            
        Returns:
            WebSocketClient: WebSocket client for real-time analysis
        """
        return WebSocketClient(self.api_key, on_message)

class WebSocketClient:
    """
    WebSocket client for real-time audio analysis
    """
    
    def __init__(self, api_key: str, on_message: Callable[[Dict[str, Any]], None]):
        self.api_key = api_key
        self.on_message = on_message
        self.ws = None
        self.authenticated = False
        self.base_url = "wss://securespeak-api-1064980124131.us-central1.run.app"
        
    def connect(self) -> None:
        """
        Connect to the WebSocket server
        """
        try:
            self.ws = websocket.WebSocketApp(
                self.base_url,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            
            # Start the WebSocket in a separate thread
            self.ws_thread = threading.Thread(target=self.ws.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()
            
            # Wait for connection
            timeout = 10
            while not self.ws.sock and timeout > 0:
                time.sleep(0.1)
                timeout -= 0.1
                
            if not self.ws.sock:
                raise SecureSpeakAPIError("WebSocket connection timeout")
                
        except Exception as e:
            raise SecureSpeakAPIError(f"WebSocket connection failed: {str(e)}")
    
    def _on_open(self, ws) -> None:
        """Handle WebSocket connection opened"""
        # Authenticate with API key
        auth_message = {
            "api_key": self.api_key
        }
        ws.send(json.dumps(auth_message))
    
    def _on_message(self, ws, message: str) -> None:
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            
            # Handle authentication result
            if "status" in data and "message" in data:
                if data["status"] == "success":
                    self.authenticated = True
                else:
                    raise SecureSpeakAPIError(f"WebSocket authentication failed: {data['message']}")
            
            # Handle prediction results
            elif "label" in data and "confidence" in data:
                self.on_message(data)
                
        except json.JSONDecodeError:
            pass  # Ignore malformed messages
    
    def _on_error(self, ws, error) -> None:
        """Handle WebSocket errors"""
        print(f"WebSocket error: {error}")
    
    def _on_close(self, ws, close_status_code, close_msg) -> None:
        """Handle WebSocket connection closed"""
        self.authenticated = False
    
    def send_audio_frame(self, audio_data: bytes) -> None:
        """
        Send audio frame for real-time analysis
        
        Args:
            audio_data (bytes): Raw audio data in WAV format
        """
        if not self.authenticated:
            raise SecureSpeakAPIError("WebSocket not authenticated")
        
        if not self.ws or not self.ws.sock:
            raise SecureSpeakAPIError("WebSocket not connected")
        
        # Send raw audio data
        self.ws.send(audio_data, websocket.ABNF.OPCODE_BINARY)
    
    def close(self) -> None:
        """
        Close the WebSocket connection
        """
        if self.ws:
            self.ws.close()
            self.authenticated = False

class SecureSpeakAPIError(Exception):
    """
    Exception raised for SecureSpeak API errors
    """
    
    def __init__(self, message: str, status_code: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.status_code:
            return f"SecureSpeak API Error ({self.status_code}): {self.message}"
        return f"SecureSpeak API Error: {self.message}" 
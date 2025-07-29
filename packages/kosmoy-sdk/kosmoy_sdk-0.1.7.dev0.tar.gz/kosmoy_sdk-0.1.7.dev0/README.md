<p align="center">
  <img src="https://auth.kosmoy.ai/assets/icons/studio_logo.svg" alt="Kosmoy Studio Logo">
</p>

# Kosmoy SDK

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/kosmoy-sdk)](https://pypi.org/project/kosmoy-sdk/)

The **Kosmoy SDK** is a powerful Python library designed to seamlessly integrate your code with the **Kosmoy platform**. It empowers your applications to leverage **Kosmoy Gateways**, providing secure and governed access to AI models and routers configured within **Kosmoy Studio**.

This SDK is built with compatibility in mind, offering a similar interface to the standard OpenAI Python SDK and providing built-in integration with LangChain. This makes it easy to adopt the Kosmoy SDK, whether you are starting a new project or migrating an existing one.

## Key Features

*   **Secure Access to Kosmoy Gateways:** Connect your Python applications to Kosmoy Gateways via a secure API key associated with a Kosmoy Studio Coded App.
*   **Simplified Model Interaction:** Interact with AI models (LLMs) registered in Kosmoy Studio using a familiar interface.
*   **Leverage Studio Configurations:** Benefit from the Routers and Guardrails configured within Kosmoy Studio, ensuring your application adheres to organizational policies.
*   **OpenAI SDK Compatibility:**  Offers a similar interface to the standard OpenAI client for easy migration and adoption.
*   **LangChain Integration:** Provides seamless integration with LangChain for building sophisticated language model applications.
*   **Comprehensive Error Handling:** Implements robust error handling inherited from both the OpenAI and LangChain APIs.
*   **Observability and Monitoring:** Gain insights into your application's performance, usage, and costs through Kosmoy Studio's Insights.
*   **Automatic Retries:** Built-in retry mechanism for handling transient network issues.
*   **Type Hints:**  Includes type hints for improved code readability and maintainability.

## Installation

### Standard Usage

```bash
pip install kosmoy-sdk
```

### LangChain Integration

```bash
pip install kosmoy-sdk[langchain]
```

## Requirements

* Python 3.7+

## Quick Start

### Standard Usage

```python
from kosmoy_sdk import GatewayClient


# Initialize the client
client = GatewayClient(
    app_id="your_app_id",    
    api_key="your_api_key"
)

# Interact with a model (make sure the model is available in your Gateway)

response = client.client.chat.completions.create(
    model="gpt-4",  # Replace with your model name configured in Kosmoy Studio
    messages=[{"role": "user", "content": "Hello!"}],
)

# Get Gateway Information
gateway_info = client.get_gateway()
```

### LangChain Integration

```python
from kosmoy_sdk.langchain import KosmoyGatewayLangchain

# Initialize the LangChain client
client = KosmoyGatewayLangchain(
    app_id="your_app_id",  # Replace with your Coded App ID
    api_key="your_api_key",  # Replace with your API key
    model="gpt-4", # Replace with your model name configured in Kosmoy Studio,
)

# Create messages
messages = [
    ("system", "You are a helpful assistant."),
    ("human", "What is the capital of France?")
]

# Get a response
response = client.invoke(messages)

# Get Gateway information
gateway_info = client.get_gateway()
```

### Gateway information

```python
gateway_info = client.get_gateway()
```
<details><summary>JSON Sample</summary>
  
```json
{
  "id": 1,
  "name": "AI Text Generator",
  "description": "A coded app that generates text using AI models.",
  "gateway_id": 100,
  "created_at": "2025-02-10T12:00:00Z",
  "created_by_user": {
    "id": 5,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "role": "Admin"
  },
  "gateway": {
    "id": 100,
    "name": "gateway1",
    "description": "Gateway handling AI text processing requests.",
    "created_at": "2025-01-15T10:30:00Z",
    "created_by_user": {
      "id": 2,
      "first_name": "Alice",
      "last_name": "Smith",
      "email": "alice.smith@example.com",
      "role": "Root"
    },
    "models": [
      {
        "id": 201,
        "service_config_id": 301,
        "name": "gpt4o",
        "model_name": "gpt-4o",
        "description": "High-performance text generation model.",
        "config_params": {
          "temperature": 0.7,
          "max_tokens": 500
        }
      }
    ],
    "guardrails": [
      {
        "id": 10,
        "name": "guardrail1",
        "description": "Filters out inappropriate language."
      }
    ],
    "routers": [
      {
        "id": 50,
        "name": "routers1",
        "description": "Routes requests between different AI models.",
        "error_message": "Fallback to secondary model.",
        "primary_model_id": 201,
        "secondary_model_id": 202,
        "router_type": "FAILOVER",
        "created_by_user": {
          "id": 3,
          "first_name": "Bob",
          "last_name": "Johnson",
          "email": "bob.johnson@example.com",
          "role": "Admin"
        }
      }
    ]
  }
}
```

</details>

## Configuration 

The Kosmoy SDK requires the following parameters:

*   **app_id:** Your Kosmoy Studio Coded App ID (required).
*   **api_key:** Your Kosmoy Studio Coded App API key (required).
*   **timeout:** Request timeout in seconds (optional, default: 30).
*   **max_retries:** Maximum number of retry attempts (optional, default: 3).

## How to get you Kosmoy Studio Coded App ID and API Key

1. Log in to Kosmoy Studio: Access the Kosmoy Studio platform at [https://www.kosmoy.com](https://auth.kosmoy.ai/login)
2. Create a Coded App: Navigate to the "Coded Apps" section and create a new Coded App.
3. Assign a Gateway: Associate your Coded App with a configured Gateway.
4. Retrieve Credentials: The API key and App ID will be displayed in the Coded App details.

## Error Handling

The Kosmoy SDK inherits error handling from the OpenAI API (when used directly) and LangChain API (when using the LangChain integration). It also includes an automatic retry mechanism for failed requests.

## Security

*   API credentials are transmitted securely via request headers.
*   The base URL for API communication is pre-configured within the SDK.
*   HTTPS is enforced for all API communications.

## Learn More

*   Kosmoy Website: [https://www.kosmoy.com](https://www.kosmoy.com)
*   Kosmoy Documentation: [https://docs.kosmoy.com](https://docs.kosmoy.com)

## License

This project is licensed under the MIT license.

## Support

For support, please contact support@kosmoy.com

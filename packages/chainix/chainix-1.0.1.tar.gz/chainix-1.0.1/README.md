# Chainix

A Python client library for executing chains with chainix.ai

## Installation

```bash
pip install chainix
```

## Quick Start

```python
from chainix import AsyncChainClient

# Initialize the client
client = AsyncChainClient(
    chain_id="your-chains-id-here",
    api_key="your-api-key-here",
)

# Define your custom functions
def refund(args):
    try:
        order_id = args['order id']
        print(f"Issuing a refund for order: {order_id}")
    
        # Your business logic here
        # ... process refund ...
        amount = 500
        
        return {
            'success': True,
            'vars_to_update': {
                'refund_amount': amount
            }
        }
    except Exception as e:
        print(f"Failed to process refund: {e}")
        return {
            'success': False,
            'vars_to_update': {}
        }


def cancel_order(args):
    try:
        order_id = args['order id']
        print(f"Cancelling order: {order_id}")
    
        # Your business logic here
        # ... perform cancellation ...
        
        return {
            'success': True,
            'vars_to_update': {}
        }
    except Exception as e:
        print(f"Failed to cancel order: {e}")
        return {
            'success': False,
            'vars_to_update': {}
        }


# Register your functions (use the actual function IDs from the chain on chainix.ai)
client.register_function("your-cancel-function-id", cancel_order)
client.register_function("your-refund-function-id", refund)

# Or, bulk register your functions
functions = {
    "your-cancel-function-id": cancel_order,
    "your-refund-function-id": refund,
}
client.register_functions(functions)

# Execute a chain
# Provide all initial variables needed to start the chain
result = client.run_chain({
    'message body': 'Hi, please cancel my order',
    'order id': '33433',
})

print("Chain completed:", result)
```

## Function Requirements

All registered functions **must** follow these requirements:

### Function Signature
Your functions should accept a single dictionary argument. When the function is called, this dictionary will contain the inputs for that function call step:

```python
def my_function(args: dict) -> dict:
    # Your business logic here
    pass
```

**How it works:**
1. You define variables in your chain on chainix.ai (e.g., `order id`, `user email`, `action`)
2. You create function call steps in your chain and specify which variables should be passed as inputs to each step
3. When the chain reaches a function call step, it stops and calls your registered function via it's id
4. Your function receives a dictionary where each key is a variable you specified as an input for that step, and each value is the current value of that variable in the chain

**Example:** If you have a function call step with `order id` and `user email` as inputs, your function will receive:
```python
{
    'order id': '12345',
    'user email': 'user@example.com'
}
```

### Return Value
Your functions **must** return a dictionary with exactly two keys:

```python
{
    'success': bool,        # True if function executed successfully, False otherwise
    'vars_to_update': dict  # Dictionary of variables to update in the chain (can be empty)
}
```

**Important**: The keys in `vars_to_update` must exactly match the variable names you defined in your chain on chainix.ai. Only variables that exist in your chain can be updated. If you try to update a variable that doesn't exist in your chain, the chain will fail.

### Example Function Structure

```python
def process_order(args):
    try:
        # Extract arguments
        order_id = args['order id']
        action = args.get('action', 'process')
        
        # Your business logic here
        if action == 'cancel':
            # ... cancellation logic ...
            return {
                'success': True,
                'vars_to_update': {
                    'order status': 'cancelled',        # Must match variable name in your chain
                    'cancellation date': '2024-01-01'  # Must match variable name in your chain
                }
            }
        elif action == 'fulfill':
            # ... fulfillment logic ...
            return {
                'success': True,
                'vars_to_update': {
                    'order status': 'fulfilled',        # Must match variable name in your chain
                    'fulfillment date': '2024-01-01'   # Must match variable name in your chain
                }
            }
        else:
            return {
                'success': False,
                'vars_to_update': {}
            }
            
    except Exception as e:
        print(f"Error processing order: {e}")
        return {
            'success': False,
            'vars_to_update': {}
        }
```

## Function Registration

You can register functions individually or in bulk:

```python
# Individual registration
client.register_function("function-id-1", my_function)

# Bulk registration
functions = {
    "function-id-1": cancel_order,
    "function-id-2": refund,
    "function-id-3": process_order,
}
client.register_functions(functions)
```

## Configuration

```python
client = AsyncChainClient(
    chain_id="your-chain-id",           # Your unique chain identifier
    api_key="your-api-key",             # Your API key for authentication
    base_url="https://chainix.ai",      # Base URL (optional, defaults to chainix.ai)
    max_wait_time=300,                  # Max wait time in seconds (optional, default 300)
    poll_interval=5,                    # How often to check status in seconds (optional, default 5, minimum 3)
    verbose=True                        # Whether to print status messages (optional, default True)
)
```

### Silent Mode

For production environments or when you don't want status messages, you can disable verbose output:

```python
client = AsyncChainClient(
    chain_id="your-chain-id",
    api_key="your-api-key",
    verbose=False  # Runs silently
)
```

## Running Chains

### Basic Usage

```python
result = client.run_chain(
    initial_variables={
        'message body': 'Hi, please cancel my order',
        'user email': 'user@example.com',
        'order id': '12345',
    }
)
```

### Test Mode

You can run chains in test mode for development and debugging:

```python
result = client.run_chain(
    initial_variables={
        'message body': 'Hi, please cancel my order',
        'user email': 'user@example.com',
        'order id': '12345'
    },
    test=True  # Runs in test mode
)
```

## Error Handling

The client automatically handles several types of errors:

- **Network errors**: Automatically retries with backoff
- **Function execution errors**: Functions that throw exceptions are treated as failed (`success: False`)
- **Invalid function returns**: If functions don't return the required structure, the chain will stop with a clear error message

### Best Practices

1. **Always wrap the body of your custom function in try-catch blocks**, catch any errors and set success to false in the return dictionary
2. **Return meaningful error information** when functions fail
3. **Validate input arguments** at the start of your functions
4. **Use exact variable names** in `vars_to_update` that match your variables names on the chain configuration on chainix.ai

```python
def robust_function(args):
    try:
        # Validate inputs
        if 'required_field' not in args:
            raise ValueError("Missing required_field")
            
        # Your business logic
        result = perform_business_logic(args)
        
        return {
            'success': True,
            'vars_to_update': {
                'operation result': result,
                'timestamp': datetime.now().isoformat()
            }
        }
        
    except ValueError as e:
        print(f"Validation error: {e}")
        return {
            'success': False,
            'vars_to_update': {'error type': 'validation_error'}
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'success': False,
            'vars_to_update': {'error type': 'unexpected_error'}
        }
```

## Return Values

The `run_chain()` method returns detailed information about the chain execution. **You don't need to handle or use this return value to successfully run chains** - it's provided as an optional feature for debugging, monitoring, or accessing final variable values.

The method returns a dictionary with different structures depending on the outcome:

### Successful Chain Completion

When a chain completes successfully, it returns a dictionary with the following structure:

```python
{
    'complete': True,      # Chain finished running
    'success': True,       # Chain completed without errors
    'data': {
        'runId': 'unique-run-identifier',
        'initialVars': {
            'variable_name_1': 'initial_value1',
            'variable_name_2': 'initial_value2',
            # ... all variables and their starting values
        },
        'vars': {
            'variable_name_1': 'final_value1',
            'variable_name_2': 'final_value2',
            # ... all variables and their final values
        },
        'log': [
            # Array of each step that was executed with step details
            {
                'stepType': 'inference',
                'stepTitle': 'Analyze Request',
                'updatedVars': {'request_type': 'cancellation'},
                'res': {'result': {'action': 'cancel'}, 'success': True, ...}
            },
            # ... more steps
        ],
        'timestamp': '2024-01-01T12:00:00Z',
        'errorDiagnosis': '',    # Error details (empty string on success)
        'errorType': '',         # Error type (empty string on success)
    }
}
```

**Example successful result:**
```python
result = client.run_chain({
    'message body': 'Hi, please cancel my order',
    'order id': '33433',
})

# Result might look like:
{
    'complete': True,
    'success': True,
    'data': {
        'runId': 'run_abc123',
        'initialVars': {
            'message body': 'Hi, please cancel my order',
            'order id': '33433'
        },
        'vars': {
            'message body': 'Hi, please cancel my order',
            'order id': '33433',
            'order status': 'cancelled',
            'cancellation_date': '2024-01-01'
        },
        'log': [
            {
                'stepType': 'inference',
                'stepTitle': 'Analyze Message',
                'updatedVars': {'request_type': 'cancellation'},
                'res': {
                    'result': {'action': 'cancel'},
                    'success': True,
                    'confidence': 0.95,
                    'explanation': 'Customer requested order cancellation'
                }
            },
            {
                'stepType': 'function_call',
                'stepTitle': 'Cancel Order Function',
                'updatedVars': {'order status': 'cancelled', 'cancellation_date': '2024-01-01'},
                'res': {
                    'explanation': 'Order successfully cancelled',
                    'success': True,
                    'updatedVars': {'order status': 'cancelled', 'cancellation_date': '2024-01-01'}
                }
            }
        ],
        'timestamp': '2024-01-01T12:00:00Z',
        'errorDiagnosis': '',
        'errorType': ''
    }
}
```

### Failed Chain Completion

When a chain completes but with errors, it returns:

```python
{
    'complete': True,      # Chain finished running
    'success': False,      # Chain completed with errors
    'data': {
        'runId': 'unique-run-identifier',
        'vars': {
            # Variables and their values when the error occurred
        },
        'log': [
            # Steps that were executed before the error
        ],
        'timestamp': '2024-01-01T12:00:00Z',
        'success': False,
        'errorDiagnosis': 'Description of what went wrong',
        'errorType': 'error_category',
        'initialVars': {
            # Starting variable values
        }
    }
}
```

### Error Cases

When errors occur during chain execution, the method returns an **empty dictionary** `{}`:

- **API errors** (invalid API key, chain not found, etc.)
- **Network errors** that persist after retries
- **Client-side errors** (connection timeouts, invalid requests)
- **Timeout errors** when the chain doesn't complete within `max_wait_time`

**Note:** When a chain completes but encounters errors during execution, it will still return a structured response with `complete: True` and `success: False`, along with error details in `errorDiagnosis` and `errorType`. The empty dictionary `{}` is only returned for client-side or API communication failures.

### Server-Side Error Types

When a chain completes with `complete: True` and `success: False`, the `errorType` field will contain one of these specific error categories:

- **`validation_error`**: Invalid input provided (HTTP 400 equivalent)
  - Tried to update a variable that doesn't exist in your chain
  - Missing required initial variables
  - Invalid variable names or values
  
- **`function_call_error`**: Your registered function failed during execution
  - Function threw an exception
  - Function returned invalid structure
  - Function returned `success: False`
  
- **`routing_error`**: Chain execution reached a dead end
  - A step's output doesn't point to any next step
  - Invalid routing configuration in the chain
  
- **`circular_error`**: Infinite loop detected
  - The same step was reached twice during execution
  - Prevents chains from running indefinitely
  
- **`low_confidence_error`**: AI inference didn't meet confidence threshold
  - Model's confidence score was below the required threshold
  - Useful for triggering manual review or alternative workflows

- **`usage_limit_exceeded_error`**: API usage limits have been reached
  - Only applies to free accounts that exceed their daily spending limit
  
- **`unexpected_error`**: Internal server error (HTTP 500 equivalent)
  - Catch-all for unexpected system failures
  - Contact support if this occurs frequently

#### Handling Different Error Types

You can implement different logic based on the error type:

```python
result = client.run_chain(initial_variables)

if result.get('complete') and not result.get('success'):
    error_type = result.get('data', {}).get('errorType')
    error_diagnosis = result.get('data', {}).get('errorDiagnosis')
    
    if error_type == 'low_confidence_error':
        # Model wasn't confident - trigger manual review
        print(f"Model uncertain: {error_diagnosis}")
        send_email_to_reviewers(error_diagnosis)
        queue_for_manual_processing(initial_variables)
    else:
        # Handle other error types as needed
        print(f"Chain failed with {error_type}: {error_diagnosis}")
```

### Understanding the Result Structure

**Fields:**

- **`complete`**: Boolean indicating if the chain finished running (regardless of success/failure)
- **`success`**: Boolean indicating if the chain completed without errors
- **`data.vars`**: Dictionary of all variables and their **final values**
- **`data.runId`**: Unique identifier for this specific chain execution
- **`data.log`**: Array showing each step that was executed and its result (see detailed breakdown below)
- **`data.initialVars`**: Dictionary of variables and their **starting values** (useful for comparison)
- **`data.errorDiagnosis`**: Detailed error description (when `success: False`)
- **`data.errorType`**: Category of error that occurred (when `success: False`)

### Understanding the Execution Log

The `data.log` field contains an array of steps in the order they were executed. Each step is a dictionary with these keys:

- **`stepType`**: Type of step executed (`'inference'`, `'function_call'`, `'endpoint'`, or `'variable_checker'`)
- **`stepTitle`**: Name/title of the step
- **`updatedVars`**: Dictionary of variables that were updated (key = variable name, value = new value)
- **`res`**: Result details that vary by step type

#### Step Types and Results

**Inference Steps** (`stepType: 'inference'`):
AI model makes decisions or classifications based on data.

```python
{
    'stepType': 'inference',
    'stepTitle': 'Analyze Customer Priority',
    'updatedVars': {'priority_level': 'high'},
    'res': {
        'result': {'priority': 'high'},           # Model's decision outputs
        'success': True,                          # Met confidence threshold
        'threshold': 0.7,                         # Required confidence level
        'confidence': 0.95,                       # Actual confidence score
        'explanation': 'I chose "high" because...',  # Model's reasoning
        'updatedVars': {}                         # Variables updated by model
    }
}
```

**Function Call Steps** (`stepType: 'function_call'`):
Executes your registered Python functions.

```python
{
    'stepType': 'function_call',
    'stepTitle': 'Cancel Order Function',
    'updatedVars': {'order_status': 'cancelled'},
    'res': {
        'explanation': 'Function executed successfully',
        'updatedVars': {'order_status': 'cancelled'},  # Variables your function updated
        'success': True                                 # Function execution success
    }
}
```

**Variable Checker Steps** (`stepType: 'variable_checker'`):
Checks and validates variable values.

```python
{
    'stepType': 'variable_checker',
    'stepTitle': 'Check Order ID',
    'updatedVars': {},
    'res': {
        'explanation': 'Successfully checked order_id variable',
        'success': True,                          # Check completed successfully
        'result': {'order_id': '12345'}          # Variable name and its value
    }
}
```

**Endpoint Steps** (`stepType: 'endpoint'`):
Marks chain completion or stopping points.

```python
{
    'stepType': 'endpoint',
    'stepTitle': 'Chain Complete',
    'updatedVars': {},
    'res': {
        'explanation': 'Reached endpoint with id of "end_success"'
    }
}
```

### Checking Results

Always check the result structure properly:

```python
result = client.run_chain(initial_variables)

if not result:
    print("Chain execution failed - API or network error")
    # Handle client-side error case
elif result.get('complete') and result.get('success'):
    print("Chain completed successfully!")
    final_vars = result['data']['vars']
    print(f"Final variables: {final_vars}")
elif result.get('complete') and not result.get('success'):
    print("Chain completed with errors")
    error_info = result['data']['errorDiagnosis']
    error_type = result['data']['errorType']
    print(f"Error: {error_info} (Type: {error_type})")
else:
    print("Unexpected result format")
```

### Best Practices for Result Handling

1. **Always check for empty results first** before accessing any data
2. **Check both `complete` and `success` fields** to understand the outcome
3. **Use `data.vars` for final variable values** - this is the main output
4. **Access nested data safely** using `.get()` method or try/except blocks
5. **Enable verbose mode during development** to see detailed execution logs

```python
def handle_chain_result(result):
    """Safely handle chain execution results"""
    if not result:
        return {"error": "Chain execution failed - API or network error"}
    
    if not result.get('complete'):
        return {"error": "Chain did not complete"}
    
    if not result.get('success'):
        error_diagnosis = result.get('data', {}).get('errorDiagnosis', 'Unknown error')
        error_type = result.get('data', {}).get('errorType', 'Unknown')
        return {
            "error": f"Chain failed: {error_diagnosis}",
            "error_type": error_type
        }
    
    # Success case
    final_vars = result.get('data', {}).get('vars', {})
    run_id = result.get('data', {}).get('runId')
    
    return {
        "success": True,
        "variables": final_vars,
        "run_id": run_id
    }

# Usage
result = client.run_chain(initial_variables)
processed_result = handle_chain_result(result)

if processed_result.get("success"):
    print("Variables:", processed_result["variables"])
else:
    print("Error:", processed_result["error"])
```

## License

MIT License
import requests
import time
from typing import Dict, Callable, Any


class AsyncChainClient:
    """
    Client for executing asynchronous chains with custom function callbacks.
    """
    
    def __init__(
        self,
        chain_id: str,
        api_key: str,
        base_url: str = "https://api.chainix.ai",
        max_wait_time: int = 300,
        poll_interval: int = 5,
        verbose: bool = True
    ):
        """
        Initialize the AsyncChainClient.
        
        Args:
            chain_id: Unique identifier for your chain
            api_key: API key for authentication
            base_url: Base URL of the chain server
            max_wait_time: Maximum time to wait for chain completion in seconds
            poll_interval: Time between status polls in seconds
            verbose: Whether to print status messages (default True)
        """
        self.chain_id = chain_id
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.max_wait_time = max_wait_time
        self.poll_interval = max(poll_interval, 3)
        self.functions: Dict[str, Callable] = {}
        self.verbose = verbose
        
        # Set up default headers
        self.headers = {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }

    def _log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message)

    
    def register_function(self, function_id: str, function: Callable[[Dict[str, Any]], Any]) -> None:
        """
        Register a function that can be called during chain execution.
        
        Args:
            function_id: Unique identifier for the function
            function: Callable that takes a dictionary of arguments and returns a result
        """
        self.functions[function_id] = function
    
    def register_functions(self, functions: Dict[str, Callable[[Dict[str, Any]], Any]]) -> None:
        """
        Register multiple functions at once.
        
        Args:
            functions: Dictionary mapping function IDs to callable functions
        """
        self.functions.update(functions)
    
    def poll_chain_status(self, task_id: str) -> Dict[str, Any]:
        """
        Poll the server for chain status until completion or timeout.
        """
        start_time = time.time()
        status_url = f'{self.base_url}/api/chain-status/{self.chain_id}/{task_id}'

        while time.time() - start_time < self.max_wait_time:
            try:
                status_response = requests.get(status_url, headers=self.headers)

                if not status_response.ok:
                    try:
                        error_data = status_response.json()
                        if error_data.get('detail'):
                            self._log(f"Error polling chain status: {error_data['detail']}")
                        else:
                            self._log(f"Error response: {error_data}")
                    except:
                        self._log(f"Error {status_response.status_code}: {status_response.text}")
                    time.sleep(self.poll_interval)
                    continue

                status_data = status_response.json()
                self._log(f"Async status: {status_data.get('status', 'unknown')}")

                if status_data.get('status') == 'complete':
                    return status_data.get('result', {})
                elif status_data.get('status') == 'failed':
                    raise Exception(f"Chain failed: {status_data.get('result')}")

                # Chain is still running, wait
                time.sleep(self.poll_interval)
            except requests.RequestException as e:
                self._log(f"Error polling chain status: {e}")
                time.sleep(self.poll_interval)

        raise TimeoutError(f"Chain with run id {task_id} did not complete within {self.max_wait_time} seconds.")

    def run_chain(
        self,
        initial_variables: Dict[str, Any],
        test: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute an asynchronous chain with the provided initial_variables.
        
        Args:
            initial_variables: Dictionary of initial variables for the chain
            test: Whether this is a test run
            vars_to_update: Optional dictionary of variables to update during execution
            
        Returns:
            Dictionary containing the final chain result
        """
        url = f'{self.base_url}/api/run-chain/{self.chain_id}'

        payload = {
            'initial_variables': initial_variables,
            'initial_run': True,
            'test': test,
        }

        vars_to_update = {}

        if vars_to_update:
            payload['vars_to_update'] = vars_to_update

        response = requests.post(url, json=payload, headers=self.headers)
        if not response.ok:
            try:
                error_data = response.json()
                if error_data.get('detail'):
                    self._log(f"Error: {error_data['detail']}")
                    self._log(f"Response: {error_data}")
                else:
                    self._log(f"Response: {error_data}")
            except:
                self._log(f"Error {response.status_code}: {response.text}")
            return {}
        
        initial_response = response.json()
        task_id = initial_response.get('data', {}).get('taskId')
        if not task_id:
            raise Exception("No task ID received from initial request.")

        self._log(f"Chain started with task ID: {task_id}")
        response = self.poll_chain_status(task_id)

        while not response.get('complete', False):
            # extract the run ID
            run_id = response.get('run_id')
            # the run is asking for a function call
            func_info = response.get('function')
            if not func_info:
                raise Exception("No function call information found in the response.")

            returned_function_id = func_info.get('id')
            arguments = func_info.get('args')

            if returned_function_id not in self.functions:
                raise Exception(f"Function '{returned_function_id}' not implemented.")

            function_to_call = self.functions[returned_function_id]
            try:
                result = function_to_call(arguments)
            except Exception as e:
                self._log(f"Function '{returned_function_id}' failed: {e}")
                success = False
                function_vars_to_update = {}
            
            else:
                if not isinstance(result, dict):
                    raise Exception(f"Function '{returned_function_id}' must return a dictionary, got {type(result)}")
                    
                if 'success' not in result:
                    raise Exception(f"Function '{returned_function_id}' must return a dictionary with 'success' key to indicate if the function ran successfully.")
                
                if 'vars_to_update' not in result:
                    raise Exception(f"Function '{returned_function_id}' must return a dictionary with 'vars_to_update' key. If there are no variables to update it should return an empty dictionary.")
                
                success = result['success']
                function_vars_to_update = result['vars_to_update']
                            

            payload = {
                'run_id': run_id, 
                'success': success,
                'initial_run': False,
                'vars_to_update': function_vars_to_update
            }

            submit_resp = requests.post(url, json=payload, headers=self.headers)
            if not submit_resp.ok:
                try:
                    error_data = submit_resp.json()
                    if error_data.get('detail'):
                        self._log(f"Error submitting function result: {error_data['detail']}")
                    else:
                        self._log(f"Error response: {error_data}")
                except:
                    self._log(f"Error {submit_resp.status_code}: {submit_resp.text}")
                return {}

            submit_response = submit_resp.json()
            new_task_id = submit_response.get('data', {}).get('taskId')
            if new_task_id:
                self._log(f"Chain continued with task ID: {new_task_id}")
                response = self.poll_chain_status(new_task_id)
            else:
                response = submit_response

        self._log("Chain complete!")
        return response
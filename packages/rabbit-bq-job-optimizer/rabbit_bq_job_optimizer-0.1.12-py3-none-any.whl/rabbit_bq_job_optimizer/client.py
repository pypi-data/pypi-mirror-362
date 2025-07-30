import os
import requests
from dataclasses import asdict

from .models import OptimizationResponse
from .exceptions import RabbitBQJobOptimizerError

class RabbitBQJobOptimizer:
    API_KEY_ENV_VAR = "RABBIT_API_KEY"
    BASE_URL_ENV_VAR = "RABBIT_API_BASE_URL"
    DEFAULT_BASE_URL = "https://api.followrabbit.ai/bq-job-optimizer"

    def __init__(self, api_key: str = None, base_url: str = None):
        """
        Initialize the Rabbit BigQuery Job Optimizer client.

        Args:
            api_key: Your Rabbit API key. Can also be set via RABBIT_API_KEY environment variable.
            base_url: Optional base URL for the API. If not provided, will use environment variable
                     RABBIT_API_BASE_URL or default to production endpoint.
        """
        self.api_key = api_key or os.getenv(self.API_KEY_ENV_VAR)
        if not self.api_key:
            raise ValueError(f"API key must be provided either as an argument or via the {self.API_KEY_ENV_VAR} environment variable")

        # Use provided base_url, environment variable, or default
        self.base_url = base_url or os.getenv(self.BASE_URL_ENV_VAR) or self.DEFAULT_BASE_URL
        self.base_url = self.base_url.rstrip('/')
        
        self.session = requests.Session()
        self.session.headers.update({
            'rabbit-api-key': self.api_key,
            'Content-Type': 'application/json'
        })

    def optimize_job(
        self,
        configuration,
        enabledOptimizations
    ) -> OptimizationResponse:
        """
        Optimize a BigQuery job configuration.

        Args:
            configuration: The BigQuery job configuration to optimize
            enabledOptimizations: List of optimizations to enable

        Returns:
            OptimizationResponse containing the optimized configuration and results

        Raises:
            RabbitBQJobOptimizerError: If the API request fails
        """
        url = f"{self.base_url}/v1/optimize-job"
        
        payload = {
            "job": configuration,
            "enabledOptimizations": [asdict(opt) for opt in enabledOptimizations]
        }

        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            response_data = response.json()
            return OptimizationResponse(**response_data)
        except requests.exceptions.RequestException as e:
            raise RabbitBQJobOptimizerError(f"Failed to optimize job: {str(e)}") 
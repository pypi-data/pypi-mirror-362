"""
Main client for Avocavo Nutrition API
"""

import requests
import time
from typing import Dict, List, Optional, Union

from .models import (
    Nutrition, USDAMatch, IngredientResult, RecipeResult, BatchResult, 
    Account, Usage, RecipeNutrition, RecipeIngredient
)
from .exceptions import ApiError, AuthenticationError, RateLimitError, ValidationError
from .auth import get_api_key


class NutritionAPI:
    """
    Avocavo Nutrition API Client
    
    Provides fast, accurate nutrition data with USDA verification.
    
    Example:
        # Option 1: Login once, use everywhere
        import avocavo_nutrition as av
        av.login("user@example.com", "password")
        result = av.analyze_ingredient("2 cups flour")
        
        # Option 2: Use API key directly
        client = NutritionAPI(api_key="your_api_key")
        result = client.analyze_ingredient("2 cups flour")
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://app.avocavo.app", timeout: int = 30):
        """
        Initialize the Nutrition API client
        
        Args:
            api_key: Your Avocavo API key (optional if logged in)
            base_url: API base URL (defaults to production)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        
        # Get API key from parameter, logged-in user, or environment
        self.api_key = api_key or get_api_key()
        
        if not self.api_key:
            raise AuthenticationError(
                "No API key provided. Either:\n"
                "1. Login: avocavo_nutrition.login('email', 'password')\n" 
                "2. Pass API key: NutritionAPI(api_key='your_key')\n"
                "3. Set environment: export AVOCAVO_API_KEY='your_key'"
            )
        
        self.session = requests.Session()
        # Disable SSL verification for development/testing
        self.session.verify = False
        
        # Determine if we have a JWT token or API key
        if self.api_key.startswith('eyJ') or '.' in self.api_key:
            # JWT token - use Authorization Bearer header
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'User-Agent': 'avocavo-nutrition-python/1.3.0'
            })
        else:
            # API key - use X-API-Key header
            self.session.headers.update({
                'X-API-Key': self.api_key,
                'Content-Type': 'application/json',
                'User-Agent': 'avocavo-nutrition-python/1.3.0'
            })
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make HTTP request with comprehensive error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == 'GET':
                response = self.session.get(url, timeout=self.timeout)
            else:
                response = self.session.post(url, json=data, timeout=self.timeout)
            
            # Handle different status codes with specific exceptions
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key. Check your credentials.")
            elif response.status_code == 402:
                raise AuthenticationError("Trial expired or payment required. Upgrade your plan.")
            elif response.status_code == 403:
                error_data = response.json() if response.content else {}
                raise ValidationError(error_data.get('error', 'Feature not available on your plan'))
            elif response.status_code == 429:
                error_data = response.json() if response.content else {}
                raise RateLimitError(
                    error_data.get('error', 'Rate limit exceeded'),
                    limit=error_data.get('limit'),
                    usage=error_data.get('usage'),
                    status_code=response.status_code
                )
            elif response.status_code >= 500:
                raise ApiError("Server error. Please try again later.", response.status_code)
            elif response.status_code >= 400:
                error_data = response.json() if response.content else {}
                raise ValidationError(
                    error_data.get('error', f'HTTP {response.status_code}'), 
                    response.status_code, 
                    error_data
                )
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise ApiError("Request timeout. Please try again.")
        except requests.exceptions.ConnectionError:
            raise ApiError("Connection error. Check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise ApiError(f"Request failed: {str(e)}")
    
    def analyze(self, input_data: Union[str, List[str]], servings: Optional[int] = None) -> Union[IngredientResult, RecipeResult, BatchResult]:
        """
        Smart routing to proper structured endpoints based on input type
        
        This method intelligently routes to the appropriate structured endpoint:
        - Single ingredient → /api/v2/nutrition/ingredient (bulletproof system)
        - Recipe with servings → /api/v2/nutrition/recipe (bulletproof system) 
        - Multiple ingredients → /api/v2/nutrition/batch (bulletproof system)
        
        Args:
            input_data: Can be:
                - Single ingredient string: "2 cups flour"
                - Recipe array: ["2 cups flour", "1 cup milk"]  
            servings: Number of servings (for recipe analysis)
            
        Returns:
            IngredientResult, RecipeResult, or BatchResult depending on input type
            
        Examples:
            # Single ingredient
            result = client.analyze("2 cups all-purpose flour")
            
            # Recipe array
            result = client.analyze(["2 cups flour", "1 cup milk"], servings=8)
            
            # Multiple ingredients (batch)
            result = client.analyze(["1 cup quinoa", "2 tbsp olive oil", "4 oz salmon"])
        """
        if isinstance(input_data, str):
            # Single ingredient - use bulletproof V2 ingredient endpoint
            return self.analyze_ingredient(input_data)
        elif isinstance(input_data, list):
            if servings and servings > 1:
                # Recipe with servings - use bulletproof V2 recipe endpoint
                return self.analyze_recipe(input_data, servings)
            else:
                # Multiple ingredients without servings - use bulletproof V2 batch endpoint
                return self.analyze_batch(input_data)
        else:
            raise ValueError("Input must be a string (ingredient) or list (recipe/batch)")

    def analyze_ingredient(self, ingredient: str) -> IngredientResult:
        """
        Analyze a single ingredient for complete nutrition data
        
        Args:
            ingredient: Recipe ingredient with quantity (e.g., "2 cups flour")
            
        Returns:
            IngredientResult with nutrition data and USDA verification
            
        Example:
            result = client.analyze_ingredient("1 cup rice")
            if result.success:
                print(f"Calories: {result.nutrition.calories}")
                print(f"USDA Source: {result.usda_match.description}")
                print(f"Verify: {result.verification_url}")
        """
        data = {"ingredient": ingredient}
        response = self._make_request('POST', '/api/v2/nutrition/ingredient', data)
        return self._parse_ingredient_result(response, ingredient)
    
    def analyze_recipe(self, ingredients: List[str], servings: int = 1) -> RecipeResult:
        """
        Analyze a complete recipe with per-serving nutrition calculations
        
        Args:
            ingredients: List of recipe ingredients with quantities
            servings: Number of servings (for per-serving calculations)
            
        Returns:
            RecipeResult with total and per-serving nutrition
            
        Example:
            result = client.analyze_recipe([
                "2 cups all-purpose flour",
                "1 cup whole milk", 
                "2 large eggs"
            ], servings=8)
            
            if result.success:
                print(f"Total: {result.nutrition.total.calories} calories")
                print(f"Per serving: {result.nutrition.per_serving.calories} calories")
        """
        data = {"ingredients": ingredients, "servings": servings}
        response = self._make_request('POST', '/api/v2/nutrition/recipe', data)
        return self._parse_recipe_result(response, ingredients, servings)
    
    def analyze_batch(self, ingredients: List[str]) -> BatchResult:
        """
        Analyze multiple ingredients efficiently in a single request
        
        Available for Starter tier and above.
        Batch limits: Free (5), Starter (10), Professional (20), Enterprise (50+) ingredients
        
        Args:
            ingredients: List of ingredients to analyze
            
        Returns:
            BatchResult with individual results for each ingredient
            
        Example:
            result = client.analyze_batch([
                "1 cup quinoa",
                "2 tbsp olive oil", 
                "4 oz salmon"
            ])
            
            for item in result.results:
                if item.success:
                    print(f"{item.ingredient}: {item.calories} cal")
        """
        # Transform array of strings to array of objects expected by batch endpoint
        ingredient_objects = [
            {"ingredient": ingredient, "id": f"item_{i+1}"}
            for i, ingredient in enumerate(ingredients)
        ]
        
        data = {"ingredients": ingredient_objects}
        response = self._make_request('POST', '/api/v2/nutrition/batch', data)
        return self._parse_batch_result(response, ingredients)
    
    
    def get_account_usage(self) -> Account:
        """
        Get current account information and usage statistics
        
        Returns:
            Account object with usage details and plan information
            
        Example:
            account = client.get_account_usage()
            print(f"Plan: {account.plan_name}")
            print(f"Usage: {account.usage.current_month}/{account.usage.monthly_limit}")
            print(f"Remaining: {account.usage.remaining}")
        """
        response = self._make_request('GET', '/api/v2/nutrition/account/usage')
        
        return self._parse_account_info(response)
    
    def list_api_keys(self) -> Dict:
        """
        List all API keys for the current user
        
        Returns:
            Dictionary with list of API keys and usage information
            
        Example:
            keys = client.list_api_keys()
            for key in keys['keys']:
                print(f"{key['name']}: {key['usage']['current_month']}/{key['usage']['limit']}")
        """
        response = self._make_request('GET', '/api/auth/keys')
        return response
    
    def create_api_key(self, name: str, description: str = None, environment: str = None) -> Dict:
        """
        Create a new API key
        
        Args:
            name: Name for the API key (e.g., "Production App", "Development")
            description: Optional description of the key's purpose
            environment: Optional environment tag (e.g., "production", "staging")
            
        Returns:
            Dictionary with new API key information (full key shown only once)
            
        Example:
            new_key = client.create_api_key("Mobile App Production", 
                                          description="API key for production mobile app",
                                          environment="production")
            print(f"New key: {new_key['key']['api_key']}")  # Save this securely!
        """
        data = {
            "name": name,
            "description": description,
            "environment": environment
        }
        response = self._make_request('POST', '/api/auth/keys', data)
        return response
    
    def update_api_key(self, key_id: int, name: str = None, description: str = None, environment: str = None) -> Dict:
        """
        Update an existing API key's metadata
        
        Args:
            key_id: ID of the key to update
            name: New name for the key (optional)
            description: New description (optional)
            environment: New environment tag (optional)
            
        Returns:
            Dictionary with updated key information
            
        Example:
            updated = client.update_api_key(123, name="Mobile App Staging", environment="staging")
        """
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if environment is not None:
            data["environment"] = environment
            
        response = self._make_request('PUT', f'/api/auth/keys/{key_id}', data)
        return response
    
    def delete_api_key(self, key_id: int) -> Dict:
        """
        Delete (deactivate) an API key
        
        Args:
            key_id: ID of the key to delete
            
        Returns:
            Dictionary with deletion confirmation
            
        Example:
            result = client.delete_api_key(123)
            print(result['message'])
        """
        response = self._make_request('DELETE', f'/api/auth/keys/{key_id}')
        return response
    
    def regenerate_api_key(self, key_id: int) -> Dict:
        """
        Regenerate an API key (creates new key value, keeps metadata)
        
        Args:
            key_id: ID of the key to regenerate
            
        Returns:
            Dictionary with new API key value (shown only once)
            
        Example:
            regenerated = client.regenerate_api_key(123)
            print(f"New key: {regenerated['key']['api_key']}")  # Save this securely!
        """
        response = self._make_request('POST', f'/api/auth/keys/{key_id}/regenerate')
        return response
    
    def get_usage_summary(self) -> Dict:
        """
        Get usage summary across all API keys
        
        Returns:
            Dictionary with aggregated usage statistics
            
        Example:
            summary = client.get_usage_summary()
            print(f"Total usage: {summary['summary']['total_monthly_usage']}")
            print(f"Keys over limit: {summary['summary']['keys_over_limit']}")
        """
        response = self._make_request('GET', '/api/auth/keys/usage')
        return response
    
    def reveal_api_key(self, key_id: int) -> Dict:
        """
        Reveal the full API key value for a given key ID
        
        Args:
            key_id: ID of the key to reveal
            
        Returns:
            Dictionary with full API key value
            
        Example:
            revealed = client.reveal_api_key(123)
            api_key = revealed['api_key']  # Full key for nutrition calls
        """
        response = self._make_request('POST', f'/api/auth/keys/{key_id}/reveal')
        return response
    
    def verify_fdc_id(self, fdc_id: int) -> Dict:
        """
        Get detailed information about a specific USDA food entry
        
        Args:
            fdc_id: USDA FDC ID to verify
            
        Returns:
            Dictionary with detailed food information and nutrients
            
        Example:
            info = client.verify_fdc_id(168936)  # All-purpose flour
            print(f"Food: {info['food_data']['description']}")
        """
        return self._make_request('GET', f'/api/v2/nutrition/nutrition/verify/{fdc_id}')
    
    def health_check(self) -> Dict:
        """
        Check API health and performance metrics
        
        No authentication required.
        
        Returns:
            Dictionary with API health information
            
        Example:
            health = client.health_check()
            print(f"Status: {health['status']}")
            print(f"Cache hit rate: {health['cache']['hit_rate']}")
        """
        # Temporarily remove auth headers for health check
        headers = self.session.headers.copy()
        if 'X-API-Key' in self.session.headers:
            del self.session.headers['X-API-Key']
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
        
        try:
            response = self._make_request('GET', '/api/v2/nutrition/health')
            return response
        finally:
            # Restore auth headers
            self.session.headers.update(headers)
    
    def _parse_ingredient_result(self, response: Dict, ingredient: str) -> IngredientResult:
        """Parse ingredient analysis response"""
        if response.get('success'):
            nutrition = None
            if response.get('nutrition'):
                nutrition_data = response['nutrition']
                nutrition = Nutrition(
                    calories_total=nutrition_data.get('calories', 0),
                    protein_total=nutrition_data.get('protein', 0),
                    total_fat_total=nutrition_data.get('total_fat', 0),
                    carbohydrates_total=nutrition_data.get('carbohydrates', 0),
                    fiber_total=nutrition_data.get('fiber', 0),
                    sugar_total=nutrition_data.get('sugar', 0),
                    sodium_total=nutrition_data.get('sodium', 0),
                    calcium_total=nutrition_data.get('calcium', 0),
                    iron_total=nutrition_data.get('iron', 0),
                    saturated_fat_total=nutrition_data.get('saturated_fat', 0),
                    cholesterol_total=nutrition_data.get('cholesterol', 0)
                )
            
            usda_match = None
            verification_url = None
            # USDA match is in metadata, not at root level
            metadata = response.get('metadata', {})
            if metadata.get('usda_match'):
                match_data = metadata['usda_match']
                usda_match = USDAMatch(
                    fdc_id=match_data.get('fdc_id', 0),
                    description=match_data.get('description', ''),
                    data_type=match_data.get('data_type', '')
                )
                # Get verification URL from USDA match
                verification_url = match_data.get('verification_url')
            
            # Parse parsing data
            parsing = response.get('parsing', {})
            
            return IngredientResult(
                success=True,
                ingredient=response.get('ingredient', ingredient),
                processing_time_ms=metadata.get('processing_time_ms', response.get('processing_time_ms', 0)),
                from_cache=metadata.get('cached', response.get('from_cache', False)),
                nutrition=nutrition,
                usda_match=usda_match,
                verification_url=verification_url,
                verification_method=response.get('verification_method', ''),
                cache_type=metadata.get('cache_type'),
                method_used=metadata.get('method_used'),
                portion_source=metadata.get('portion_source'),
                estimated_grams=parsing.get('estimated_grams'),
                ingredient_name=parsing.get('ingredient_name')
            )
        else:
            return IngredientResult(
                success=False,
                ingredient=ingredient,
                processing_time_ms=response.get('processing_time_ms', 0),
                error=response.get('error', 'Unknown error')
            )
    
    def _parse_recipe_result(self, response: Dict, ingredients: List[str], servings: int) -> RecipeResult:
        """Parse recipe analysis response"""
        if response.get('success'):
            nutrition_data = response.get('nutrition', {})
            
            # Parse total nutrition
            total = Nutrition()
            if 'total' in nutrition_data:
                total_data = nutrition_data['total']
                total = Nutrition(
                    calories_total=total_data.get('calories', 0),
                    protein_total=total_data.get('protein', 0),
                    total_fat_total=total_data.get('total_fat', 0),
                    carbohydrates_total=total_data.get('carbohydrates', 0),
                    fiber_total=total_data.get('fiber', 0),
                    sugar_total=total_data.get('sugar', 0),
                    sodium_total=total_data.get('sodium', 0),
                    calcium_total=total_data.get('calcium', 0),
                    iron_total=total_data.get('iron', 0),
                    saturated_fat_total=total_data.get('saturated_fat', 0),
                    cholesterol_total=total_data.get('cholesterol', 0)
                )
            
            # Parse per-serving nutrition
            per_serving = Nutrition()
            if 'per_serving' in nutrition_data:
                serving_data = nutrition_data['per_serving']
                per_serving = Nutrition(
                    calories_total=serving_data.get('calories', 0),
                    protein_total=serving_data.get('protein', 0),
                    total_fat_total=serving_data.get('total_fat', 0),
                    carbohydrates_total=serving_data.get('carbohydrates', 0),
                    fiber_total=serving_data.get('fiber', 0),
                    sugar_total=serving_data.get('sugar', 0),
                    sodium_total=serving_data.get('sodium', 0),
                    calcium_total=serving_data.get('calcium', 0),
                    iron_total=serving_data.get('iron', 0),
                    saturated_fat_total=serving_data.get('saturated_fat', 0),
                    cholesterol_total=serving_data.get('cholesterol', 0)
                )
            
            # Parse individual ingredients
            ingredient_results = []
            for item in nutrition_data.get('ingredients', []):
                ingredient_nutrition = Nutrition(
                    calories_total=item.get('nutrition', {}).get('calories', 0),
                    protein_total=item.get('nutrition', {}).get('protein', 0),
                    total_fat_total=item.get('nutrition', {}).get('total_fat', 0),
                    carbohydrates_total=item.get('nutrition', {}).get('carbohydrates', 0),
                    fiber_total=item.get('nutrition', {}).get('fiber', 0),
                    sugar_total=item.get('nutrition', {}).get('sugar', 0),
                    sodium_total=item.get('nutrition', {}).get('sodium', 0),
                    calcium_total=item.get('nutrition', {}).get('calcium', 0),
                    iron_total=item.get('nutrition', {}).get('iron', 0)
                )
                
                usda_match = None
                verification_url = None
                # Check for USDA match in metadata (where API actually returns it)
                metadata = item.get('metadata', {})
                if metadata.get('usda_match'):
                    match_data = metadata['usda_match']
                    usda_match = USDAMatch(
                        fdc_id=match_data.get('fdc_id', 0),
                        description=match_data.get('description', ''),
                        data_type=match_data.get('data_type', '')
                    )
                    verification_url = match_data.get('verification_url')
                elif item.get('usda_match'):
                    # Fallback for direct usda_match field
                    match_data = item['usda_match']
                    usda_match = USDAMatch(
                        fdc_id=match_data.get('fdc_id', 0),
                        description=match_data.get('description', ''),
                        data_type=match_data.get('data_type', '')
                    )
                    verification_url = match_data.get('verification_url')
                
                ingredient_results.append(RecipeIngredient(
                    ingredient=item.get('ingredient', ''),
                    nutrition=ingredient_nutrition,
                    usda_match=usda_match,
                    verification_url=verification_url,
                    success=item.get('success', True)
                ))
            
            recipe_nutrition = RecipeNutrition(
                total=total,
                per_serving=per_serving,
                ingredients=ingredient_results
            )
            
            # Calculate total processing time from ingredients
            total_processing_time = sum(
                item.get('metadata', {}).get('processing_time_ms', 0) 
                for item in nutrition_data.get('ingredients', [])
            )
            
            # Count successful USDA matches
            usda_match_count = sum(
                1 for item in nutrition_data.get('ingredients', [])
                if item.get('metadata', {}).get('usda_match')
            )
            
            return RecipeResult(
                success=True,
                recipe={"ingredients": ingredients, "servings": servings},
                nutrition=recipe_nutrition,
                processing_time_ms=total_processing_time,
                usda_matches=usda_match_count
            )
        else:
            return RecipeResult(
                success=False,
                recipe={"ingredients": ingredients, "servings": servings},
                processing_time_ms=response.get('processing_time_ms', 0),
                error=response.get('error', 'Unknown error')
            )
    
    def _parse_batch_result(self, response: Dict, ingredients: List[str]) -> BatchResult:
        """Parse batch analysis response"""
        results = []
        for item in response.get('results', []):
            ingredient_result = self._parse_ingredient_result(item, item.get('ingredient', ''))
            results.append(ingredient_result)
        
        return BatchResult(
            success=response.get('success', False),
            batch_size=response.get('batch_size', len(ingredients)),
            successful_matches=response.get('successful_matches', 0),
            results=results,
            processing_time_ms=response.get('processing_time_ms', 0)
        )
    
    def _parse_account_info(self, response: Dict) -> Account:
        """Parse account information response"""
        account_data = response.get('account', {})
        usage_data = response.get('usage', {})
        
        usage = Usage(
            current_month=usage_data.get('current_month', 0),
            monthly_limit=usage_data.get('monthly_limit'),
            remaining=usage_data.get('remaining', 0),
            percentage_used=usage_data.get('percentage_used', 0.0),
            reset_date=usage_data.get('reset_date', ''),
            days_until_reset=usage_data.get('days_until_reset', 0)
        )
        
        return Account(
            email=account_data.get('email', ''),
            api_tier=account_data.get('api_tier', ''),
            subscription_status=account_data.get('subscription_status', ''),
            usage=usage,
            features=None
        )


# Convenience functions for quick usage without creating client instance
def analyze(input_data: Union[str, List[str]], servings: Optional[int] = None, api_key: Optional[str] = None, base_url: str = "https://app.avocavo.app") -> Union[IngredientResult, RecipeResult, BatchResult]:
    """
    Quick function for unified nutrition analysis
    
    Args:
        input_data: Single ingredient, recipe array, or any format
        servings: Number of servings (optional)
        api_key: API key (optional if logged in)
        base_url: API base URL
        
    Returns:
        IngredientResult, RecipeResult, or BatchResult
        
    Example:
        import avocavo_nutrition as av
        result = av.analyze("2 cups flour")
        result = av.analyze(["2 cups flour", "1 cup milk"], servings=8)
    """
    client = NutritionAPI(api_key, base_url)
    return client.analyze(input_data, servings)


def analyze_ingredient(ingredient: str, api_key: Optional[str] = None, base_url: str = "https://app.avocavo.app") -> IngredientResult:
    """
    Quick function to analyze a single ingredient
    
    Args:
        ingredient: Ingredient to analyze
        api_key: API key (optional if logged in)
        base_url: API base URL
        
    Returns:
        IngredientResult
        
    Example:
        import avocavo_nutrition as av
        result = av.analyze_ingredient("2 cups flour")
    """
    client = NutritionAPI(api_key, base_url)
    return client.analyze_ingredient(ingredient)


def analyze_recipe(ingredients: List[str], servings: int = 1, api_key: Optional[str] = None, base_url: str = "https://app.avocavo.app") -> RecipeResult:
    """
    Quick function to analyze a recipe
    
    Args:
        ingredients: List of ingredients
        servings: Number of servings
        api_key: API key (optional if logged in)
        base_url: API base URL
        
    Returns:
        RecipeResult
        
    Example:
        import avocavo_nutrition as av
        result = av.analyze_recipe(["2 cups flour", "1 cup milk"], servings=6)
    """
    client = NutritionAPI(api_key, base_url)
    return client.analyze_recipe(ingredients, servings)


def analyze_batch(ingredients: List[str], api_key: Optional[str] = None, base_url: str = "https://app.avocavo.app") -> BatchResult:
    """
    Quick function to analyze multiple ingredients in batch
    
    Batch limits: Free (5), Starter (10), Professional (20), Enterprise (50+) ingredients
    
    Args:
        ingredients: List of ingredients to analyze
        api_key: API key (optional if logged in)
        base_url: API base URL
        
    Returns:
        BatchResult
        
    Example:
        import avocavo_nutrition as av
        result = av.analyze_batch(["1 cup quinoa", "2 tbsp olive oil", "4 oz salmon"])
    """
    client = NutritionAPI(api_key, base_url)
    return client.analyze_batch(ingredients)


def get_account_usage(api_key: Optional[str] = None, base_url: str = "https://app.avocavo.app") -> Account:
    """
    Quick function to get account usage information
    
    Args:
        api_key: API key (optional if logged in)
        base_url: API base URL
        
    Returns:
        Account
        
    Example:
        import avocavo_nutrition as av
        account = av.get_account_usage()
        print(f"Usage: {account.usage.current_month}/{account.usage.monthly_limit}")
    """
    client = NutritionAPI(api_key, base_url)
    return client.get_account_usage()



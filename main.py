
from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("petstore")

# Constants for API Requests
PETSTORE_API_BASE = "https://petstore3.swagger.io/api/v3"
USER_AGENT = "petstore-mcp-agent/1.0"


async def fetch_from_petstore(method: str, path: str, params: Optional[dict] = None, json: Optional[dict] = None, headers: Optional[dict] = None) -> Any:
    """Helper function to make HTTP requests to the Petstore API."""
    url = f"{PETSTORE_API_BASE}{path}"
    headers = headers or {'User-Agent': USER_AGENT, "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, params=params, json=json, headers=headers, timeout=30.0)
            response.raise_for_status()
            if response.status_code == 204:
                return None
            return response.json()
        except httpx.HTTPError as e:
            print(f"HTTP request failed: {e}")
            return None


@mcp.tool()
async def add_pet(body: Dict) -> Dict | None:
    """Adds a new pet to the store."""
    path = "/pet"
    response_data = await fetch_from_petstore("POST", path, json=body)
    return response_data


@mcp.tool()
async def update_pet(body: Dict) -> Dict | None:
    """Updates an existing pet in the store."""
    path = "/pet"
    response_data = await fetch_from_petstore("PUT", path, json=body)
    return response_data


@mcp.tool()
async def find_pets_by_status(status: List[str]) -> List[Dict] | None:
    """Finds Pets by status"""
    path = "/pet/findByStatus"
    params = {"status": ",".join(status)}
    response_data = await fetch_from_petstore("GET", path, params=params)
    return response_data


@mcp.tool()
async def find_pets_by_tags(tags: List[str]) -> List[Dict] | None:
    """Finds Pets by tags"""
    path = "/pet/findByTags"
    params = {"tags": ",".join(tags)}
    response_data = await fetch_from_petstore("GET", path, params=params)
    return response_data


@mcp.tool()
async def get_pet_by_id(pet_id: int) -> Dict | None:
    """Find pet by ID"""
    path = f"/pet/{pet_id}"
    response_data = await fetch_from_petstore("GET", path)
    return response_data


@mcp.tool()
async def update_pet_with_form(pet_id: int, name: Optional[str] = None, status: Optional[str] = None) -> None:
    """Updates a pet in the store with form data"""
    path = f"/pet/{pet_id}"
    data = {k: v for k, v in {'name': name, 'status': status}.items() if v is not None}
    await fetch_from_petstore("POST", path, params=data)
    return None


@mcp.tool()
async def delete_pet(pet_id: int, api_key: Optional[str] = None) -> None:
    """Deletes a pet"""
    path = f"/pet/{pet_id}"
    headers = {'api_key': api_key} if api_key else {}
    await fetch_from_petstore("DELETE", path, headers=headers)
    return None


@mcp.tool()
async def upload_file(pet_id: int, additional_metadata: Optional[str] = None, file: Optional[bytes] = None) -> Dict | None:
    """uploads an image"""
    path = f"/pet/{pet_id}/uploadImage"
    files = {"file": file} if file else {}
    data = {"additionalMetadata": additional_metadata} if additional_metadata else {}
    response_data = await fetch_from_petstore("POST", path, params=data, files=files)
    return response_data


@mcp.tool()
async def get_inventory() -> Dict | None:
    """Returns pet inventories by status"""
    path = "/store/inventory"
    response_data = await fetch_from_petstore("GET", path)
    return response_data


@mcp.tool()
async def place_order(body: Dict) -> Dict | None:
    """Place an order for a pet"""
    path = "/store/order"
    response_data = await fetch_from_petstore("POST", path, json=body)
    return response_data


@mcp.tool()
async def get_order_by_id(order_id: int) -> Dict | None:
    """Find purchase order by ID"""
    path = f"/store/order/{order_id}"
    response_data = await fetch_from_petstore("GET", path)
    return response_data


@mcp.tool()
async def delete_order(order_id: int) -> None:
    """Delete purchase order by ID"""
    path = f"/store/order/{order_id}"
    await fetch_from_petstore("DELETE", path)
    return None


@mcp.tool()
async def create_user(body: Dict) -> None:
    """Create user"""
    path = "/user"
    await fetch_from_petstore("POST", path, json=body)
    return None


@mcp.tool()
async def create_users_with_array_input(body: List[Dict]) -> None:
    """Creates list of users with given input array"""
    path = "/user/createWithArray"
    await fetch_from_petstore("POST", path, json=body)
    return None


@mcp.tool()
async def create_users_with_list_input(body: List[Dict]) -> None:
    """Creates list of users with given input array"""
    path = "/user/createWithList"
    await fetch_from_petstore("POST", path, json=body)
    return None


@mcp.tool()
async def login_user(username: str, password: str) -> str | None:
    """Logs user into the system"""
    path = "/user/login"
    params = {"username": username, "password": password}
    response_data = await fetch_from_petstore("GET", path, params=params)
    return response_data


@mcp.tool()
async def logout_user() -> None:
    """Logs out current logged in user session"""
    path = "/user/logout"
    await fetch_from_petstore("GET", path)
    return None


@mcp.tool()
async def get_user_by_name(username: str) -> Dict | None:
    """Get user by user name"""
    path = f"/user/{username}"
    response_data = await fetch_from_petstore("GET", path)
    return response_data


@mcp.tool()
async def update_user(username: str, body: Dict) -> None:
    """Updated user"""
    path = f"/user/{username}"
    await fetch_from_petstore("PUT", path, json=body)
    return None


@mcp.tool()
async def delete_user(username: str) -> None:
    """Delete user"""
    path = f"/user/{username}"
    await fetch_from_petstore("DELETE", path)
    return None


if __name__ == "__main__":
    mcp.run(transport='stdio')

from ...mcp_manager.client import ClientManagerMCP
from abc import ABC, abstractmethod


class LLM(ABC):
    def __init__(self):
        self.client_manager_mcp: ClientManagerMCP = ClientManagerMCP()
        self.current_language: str = "English"

    @abstractmethod
    def preprocess_query(self, query: str) -> dict:
        """
        Devuelve una lista con todas las querys en las que se divide la query principal y el lenguaje usado en la query. Puede ser solo una query
        """
        pass

    @abstractmethod
    def append_chat_history(self):
        pass

    @abstractmethod
    def simple_query(self, query: str, use_services_contex: bool = False) -> str:
        pass

    @abstractmethod
    def select_prompts(self, query: str) -> str:
        pass

    @abstractmethod
    def select_service(
        self, query: str, extra_messages: list[dict[str, str]] = []
    ) -> str:
        pass

    @abstractmethod
    def final_response(self, query: str, data: str | dict) -> str:
        pass


"""Call an Auth Admin method from Supabase Python SDK.\n\nThis tool provides a safe, validated interface to the Supabase Auth Admin SDK, allowing you to:\n- Manage users (create, update, delete)\n- List and search users\n- Generate authentication links\n- Manage multi-factor authentication\n- And more\n\nIMPORTANT NOTES:\n- Request bodies must adhere to the Python SDK specification\n- Some methods may have nested parameter structures\n- The tool validates all parameters against Pydantic models\n- Extra fields not defined in the models will be rejected\n\nAVAILABLE METHODS:\n- get_user_by_id: Retrieve a user by their ID\n- list_users: List all users with pagination\n- create_user: Create a new user\n- delete_user: Delete a user by their ID\n- invite_user_by_email: Send an invite link to a user\'s email\n- generate_link: Generate an email link for various authentication purposes\n- update_user_by_id: Update user attributes by ID\n- delete_factor: Delete a factor on a user\n\nEXAMPLES:\n1. Get user by ID:\n   method: "get_user_by_id"\n   params: {"uid": "user-uuid-here"}\n\n2. Create user:\n   method: "create_user"\n   params: {\n     "email": "user@example.com",\n     "password": "secure-password"\n   }\n\n3. Update user by ID:\n   method: "update_user_by_id"\n   params: {\n     "uid": "user-uuid-here",\n     "attributes": {\n       "email": "new@email.com"\n     }\n   }\n\nFor complete documentation of all methods and their parameters, use the get_auth_admin_methods_spec tool.\n"""

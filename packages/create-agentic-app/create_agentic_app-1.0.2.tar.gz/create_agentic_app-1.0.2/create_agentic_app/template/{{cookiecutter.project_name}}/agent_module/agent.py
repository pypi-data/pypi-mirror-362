import json
import os

from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate

from agent_module.model import APIContext
from agent_module.client import BookClient


class APISelectorAgent:
    def __init__(self):
        self.open_api_key = os.environ["OPENAI_API_KEY"]
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=1000
        )
        self.api_metadata = [
            {
                "action": "get",
                "endpoint": "/book",
                "description": "Get the list of all books",
                "path_params": [],
                "query_params": [],
                "request_body": None,
                "response": "List of Book"
            },
            {
                "action": "get",
                "endpoint": "/book/{book_id}",
                "description": "Get details of a book by its ID",
                "path_params": ["book_id"],
                "query_params": [],
                "request_body": None,
                "response": "Book"
            },
            {
                "action": "post",
                "endpoint": "/book",
                "description": "Create a new book with given title and author",
                "path_params": [],
                "query_params": [],
                "request_body": ["title", "author"],
                "response": "Book"
            }
        ]

    def _classify_request(self, query) -> APIContext:
        prompt_template = PromptTemplate(
            input_variables=["api_metadata", "query", "example"],
            template="""
            You are an expert API classifier. 
            Analyze the following query and classify the API call based on the provided API Information.
            API Information: {api_metadata}
            Classify the API with:
            1. Identify the intent in the query.
            2. The API endpoint that should be called.
            3. The HTTP request method.
            4. The data variables - id, title and author
            Valid return values for intent:
            1. get_single_book
            2. get_list_of_books
            3. create_new_book
            Return only a JSON. 
            E.g. For a query "Get the book with id 1", return JSON -   
            {example}
            Evaluate for query = {query}
            """
        )
        example = {
            "intent": "get_single_book",
            "endpoint": "/book/<book_id>",
            "method": "get",
            "id": "1",
            "title": None,
            "author": None,
        }
        prompt = prompt_template.format(
            api_metadata=self.api_metadata,
            example=json.dumps(example),
            query=query
        )
        response = self.llm([HumanMessage(content=prompt)])
        try:
            api_context = json.loads(response.content)
            return APIContext(**api_context)
        except json.JSONDecodeError as err:
            print("Could not get a valid response from LLM:", err)
            fallback = {
                "intent": "get_single_book",
                "endpoint": "/book/{book_id}",
                "method": "get",
                "id": "1",
                "title": None,
                "author": None,
            }
            return APIContext(**fallback)

    async def _make_request(self, api_context: APIContext):
        client = BookClient()
        if api_context.endpoint == "/book" and api_context.method.lower() == "get":
            response = await client.get_books()
        elif api_context.endpoint == "/book/{book_id}" and api_context.method.lower() == "get":
            # Use api_context.id for book_id
            response = await client.get_book_by_id(int(api_context.id))
        elif api_context.endpoint == "/book" and api_context.method.lower() == "post":
            # Use api_context.title and api_context.author for book creation
            book_data = {
                "title": api_context.title,
                "author": api_context.author
            }
            response = await client.create_book(book_data)
        else:
            raise ValueError(f"Unsupported API context: {api_context}")
        await client.aclose()
        return response

    async def process_query(self, query):
        api_context: APIContext = self._classify_request(query)
        return await self._make_request(api_context)

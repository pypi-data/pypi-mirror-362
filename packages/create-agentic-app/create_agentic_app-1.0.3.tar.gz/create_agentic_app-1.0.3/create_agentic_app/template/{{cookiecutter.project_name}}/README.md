# Agent driven microservice

## Start the project
In the project directory, follow the steps -

1. pip install -r requirements.txt
2. export OPENAI_API_KEY=\<your own OpenAI API key\>
3. python main.py

## API Reference
1. GET /api/v1/book -> get all books from database
2. GET /api/v1/book/{book_id} -> get a book by ID
3. POST /api/v1/book -> create a new book
4. POST /api/v1/chat/query -> operate the other APIs using natural language

## Agent Usage Examples
Make a request for POST /api/v1/chat/query
1. {"query": "Create a book The Alchemist by Paulo Coelho"}
2. {"query": "List all books"}
3. {"query": "Find the book with id 1"}
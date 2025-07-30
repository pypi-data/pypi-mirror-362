import os

from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from ingenious.models.chat import ChatRequest, ChatResponse
from ingenious.services.chat_services.multi_agent.service import IConversationFlow


class ConversationFlow(IConversationFlow):
    async def get_conversation_response(
        self, chat_request: ChatRequest
    ) -> ChatResponse:
        # Get configuration from the parent service
        model_config = self._config.models[0]

        # Configure Azure OpenAI client for v0.4
        azure_config = {
            "model": model_config.model,
            "api_key": model_config.api_key,
            "azure_endpoint": model_config.base_url,
            "azure_deployment": model_config.deployment or model_config.model,
            "api_version": model_config.api_version,
        }

        # Create the model client
        model_client = AzureOpenAIChatCompletionClient(**azure_config)

        # Set up context for conversation
        context = (
            "Knowledge base search assistant for finding information in local ChromaDB."
        )

        # Create local search tool function using ChromaDB
        async def search_tool(search_query: str, topic: str = "general") -> str:
            """Search for information in local knowledge base using ChromaDB"""
            try:
                # Import chromadb and other necessary libraries
                try:
                    import chromadb
                except ImportError:
                    return "Error: ChromaDB not installed. Please install with: uv add chromadb"

                # Initialize ChromaDB client
                knowledge_base_path = os.path.join(self._memory_path, "knowledge_base")
                chroma_path = os.path.join(self._memory_path, "chroma_db")

                # Ensure knowledge base directory exists
                if not os.path.exists(knowledge_base_path):
                    os.makedirs(knowledge_base_path, exist_ok=True)
                    return "Error: Knowledge base directory is empty. Please add documents to .tmp/knowledge_base/"

                # Initialize ChromaDB
                client = chromadb.PersistentClient(path=chroma_path)

                # Get or create collection
                collection_name = "knowledge_base"
                try:
                    collection = client.get_collection(name=collection_name)
                except Exception:
                    # Create collection if it doesn't exist
                    collection = client.create_collection(name=collection_name)

                    # Load documents from knowledge base directory
                    documents = []
                    document_ids = []

                    for filename in os.listdir(knowledge_base_path):
                        if filename.endswith(".md") or filename.endswith(".txt"):
                            filepath = os.path.join(knowledge_base_path, filename)
                            with open(filepath, "r", encoding="utf-8") as f:
                                content = f.read()
                                # Split content into chunks
                                chunks = content.split("\n\n")
                                for i, chunk in enumerate(chunks):
                                    if chunk.strip():
                                        documents.append(chunk.strip())
                                        document_ids.append(f"{filename}_chunk_{i}")

                    if documents:
                        collection.add(documents=documents, ids=document_ids)
                    else:
                        return "Error: No documents found in knowledge base directory"

                # Search the collection
                results = collection.query(query_texts=[search_query], n_results=3)

                if results["documents"] and results["documents"][0]:
                    search_results = "\n\n".join(results["documents"][0])
                    return f"Found relevant information:\n\n{search_results}"
                else:
                    return f"No relevant information found for query: {search_query}"

            except Exception as e:
                return f"Search error: {str(e)}"

        search_function_tool = FunctionTool(
            search_tool,
            description="Search for information in the local knowledge base using ChromaDB. Use relevant keywords to find health and safety information.",
        )

        # Create the search assistant agent
        search_system_message = """You are a knowledge base search assistant using local ChromaDB storage.

Tasks:
- Help users find information by searching the local knowledge base
- Use the search_tool to look up information stored in ChromaDB
- Always base your responses on search results from the knowledge base
- If no information is found, clearly state that and suggest rephrasing the query

Guidelines for search queries:
- Use specific, relevant keywords
- Try different phrasings if initial search doesn't return results
- Focus on topics that are relevant to the knowledge base content

Knowledge base contains documents about:
- Workplace safety guidelines
- Health information and nutrition
- Emergency procedures
- Mental health and wellbeing
- First aid basics
- General informational content

Format your responses clearly and cite the knowledge base when providing information.
TERMINATE your response when the task is complete.
"""

        # Set up the search assistant agent
        search_assistant = AssistantAgent(
            name="search_assistant",
            system_message=search_system_message,
            model_client=model_client,
            tools=[search_function_tool],
            reflect_on_tool_use=True,
        )

        # Create cancellation token
        cancellation_token = CancellationToken()

        # Prepare user message with context
        user_msg = (
            f"Context: {context}\n\nUser question: {chat_request.user_prompt}"
            if context
            else chat_request.user_prompt
        )

        # Use the search assistant directly with on_messages for a simpler interaction
        from autogen_agentchat.messages import TextMessage

        # Send the message directly to the search assistant
        response = await search_assistant.on_messages(
            messages=[TextMessage(content=user_msg, source="user")],
            cancellation_token=cancellation_token,
        )

        # Extract the response content
        final_message = (
            response.chat_message.content
            if response.chat_message
            else "No response generated"
        )

        # Update memory for future conversations (simplified for local testing)
        # In production, this would use the memory manager

        # Make sure to close the model client connection when done
        await model_client.close()

        # Return the response
        return ChatResponse(
            thread_id=chat_request.thread_id or "",
            message_id="",
            agent_response=final_message,
            token_count=0,
            max_token_count=0,
            memory_summary=final_message,
        )

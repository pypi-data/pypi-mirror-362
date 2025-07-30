import os
import sqlite3

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
        context = "SQL Expert Assistant for analyzing data."

        # Set up local SQLite database with student performance data

        # Create SQLite database with sample data
        db_path = os.path.join(self._memory_path, "students_performance.db")

        # Create a simple test table with dummy data
        with sqlite3.connect(db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS students_performance (
                parental_education TEXT,
                lunch TEXT,
                test_prep_course TEXT,
                math_score INTEGER,
                reading_score INTEGER,
                writing_score INTEGER
            )""")
            # Insert some sample data if table is empty
            count = conn.execute(
                "SELECT COUNT(*) FROM students_performance"
            ).fetchone()[0]
            if count == 0:
                conn.execute("""INSERT INTO students_performance VALUES
                    ('bachelor''s degree', 'standard', 'none', 72, 72, 74),
                    ('some college', 'standard', 'completed', 69, 90, 88),
                    ('master''s degree', 'standard', 'none', 90, 95, 93),
                    ('associate''s degree', 'free/reduced', 'none', 47, 57, 44),
                    ('some college', 'standard', 'none', 76, 78, 75),
                    ('high school', 'free/reduced', 'completed', 64, 64, 67),
                    ('high school', 'free/reduced', 'none', 38, 60, 50)
                """)

        table_name = "students_performance"
        column_names = [
            "parental_education",
            "lunch",
            "test_prep_course",
            "math_score",
            "reading_score",
            "writing_score",
        ]

        # Create SQL tool as function
        async def execute_sql_tool(query: str) -> str:
            """Execute SQL query on local SQLite database"""
            try:
                with sqlite3.connect(db_path) as conn:
                    # Execute query and fetch results
                    cursor = conn.execute(query)
                    results = cursor.fetchall()
                    columns = [description[0] for description in cursor.description]

                    if not results:
                        return "No results found."

                    # Format results
                    if len(results) == 1:
                        # Single row: return as dictionary
                        result_dict = dict(zip(columns, results[0]))
                        return str(result_dict)
                    else:
                        # Multiple rows: return as list of dictionaries
                        result_list = [dict(zip(columns, row)) for row in results]
                        return str(result_list[:10])  # Limit to first 10 rows
            except Exception as e:
                return f"SQL Error: {str(e)}"

        sql_tool = FunctionTool(
            execute_sql_tool,
            description=f"Execute SQL query on local SQLite database with table '{table_name}' and columns: {', '.join(column_names)}",
        )

        system_message = f"""You are a SQL expert that helps write and execute SQL queries on student performance data.

Tasks:
- Write SQL queries to answer user questions about student performance data
- Use the 'execute_sql_tool' to run queries
- Format your response based on the number of rows:
  - Single Row: Use the format {{column_name: value, column_name: value}}
  - Multiple Rows: Use a list format with each row as a dictionary

The target table '{table_name}' contains the following columns: {", ".join(column_names)}.
Use "SELECT ... FROM {table_name}" format for your queries.
DO NOT change schema or table names.
When composing summary statistics, use functions like AVG(), COUNT(), etc.
When the user asks what columns are available, just list them without running a query.

Example queries:
- SELECT * FROM students_performance LIMIT 5
- SELECT AVG(math_score) FROM students_performance
- SELECT COUNT(*) FROM students_performance WHERE lunch = 'free/reduced'
"""

        # Set up the agent team with the SQL assistant and a user proxy
        sql_assistant = AssistantAgent(
            name="sql_assistant",
            system_message=system_message,
            model_client=model_client,
            tools=[sql_tool],
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

        # Use the SQL assistant directly with on_messages for a simpler interaction
        from autogen_agentchat.messages import TextMessage

        # Send the message directly to the SQL assistant
        response = await sql_assistant.on_messages(
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

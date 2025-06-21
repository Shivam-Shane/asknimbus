from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough,RunnableSequence
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from better_profanity import profanity
from load_vectorstore import load_vector_store
from langchain.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
import os
import uuid
from upstash_redis import Redis
from dotenv import load_dotenv
from logger import logger
from templates import template_details

class AwsChatHandler():
    def __init__(self):
        load_dotenv()
        GROQ_API_KEY = os.getenv("GROC_LLM_API")
        vector_store = load_vector_store()
        profanity.add_censor_words(['adult'])
        
        self.llm = ChatGroq(
            model=os.getenv("LLM_MODEL"),
            api_key=GROQ_API_KEY,
            max_tokens=400
        )
        self.retriever = vector_store.as_retriever(search_kwargs={"k": 2})
        self.prompt = PromptTemplate(
            input_variables=["input", "context"],
            template=template_details
        )
        self.redis = Redis(
            url=os.getenv("UPSTASH_REDIS_REST_URL"),
            token=os.getenv("UPSTASH_REDIS_REST_TOKEN")
        )
        self.chat_deletion_time = int(os.getenv("CHAT_DELETION_TIME", 600))
        
        logger.info("Initialized AwsChatHandler")

    def generate_session_id(self):
        session_id = str(uuid.uuid4())
        logger.debug(f"Generated new session ID: {session_id}")
        return session_id

    def get_session_history(self, session_id: str) -> ChatMessageHistory:
        # Use Upstash Redis to store/retrieve history as a list
        history_key = f"chat_history:{session_id}"
        chat_history = ChatMessageHistory()
        try:
            messages = self.redis.lrange(history_key, -3, -1)
            logger.debug(f"Fetched {len(messages)} messages for session {session_id}")
            for msg in messages:
                role, content = msg.split(":", 1)
                if role == "human":
                    chat_history.add_user_message(content)
                elif role == "ai":
                    chat_history.add_ai_message(content)
        except Exception as e:
            logger.error(f"Error fetching session history for {session_id}: {e}")
        return chat_history

    def rag_message_history(self, session_id: str, message: str) -> str:
        if self.filter_input(message):
            logger.warning(f"Filtered inappropriate input in session {session_id}: {message}")
            return "Sorry, I’m here to help with AWS related questions only."

        try:
            history_key = f"chat_history:{session_id}"
            rag_chain_with_history = RunnableWithMessageHistory(
                runnable=RunnableSequence(
                    {
                        "context": lambda x: self.retriever.invoke(x["input"]),
                        "input": RunnablePassthrough(),
                        "history": lambda x: x.get("history", "")
                    },
                    self.prompt,
                    self.llm,
                    StrOutputParser()
                ),
                get_session_history=self.get_session_history,
                input_messages_key="input",
                history_messages_key="history"
            )

            logger.debug(f"Invoking RAG chain for session {session_id} with message: {message}")
            response = rag_chain_with_history.invoke(
                {"input": message},
                config={"configurable": {"session_id": session_id}}
            )

            self.redis.rpush(history_key, f"ai:{response}")
            self.redis.expire(history_key, self.chat_deletion_time)

            logger.info(f"Generated response for session {session_id}")
            logger.debug(f"Response: {response}")

            return response

        except Exception as e:
            logger.exception(f"Failed to process message for session {session_id}: {e}")
            return "An error occurred while processing your request. Please try again later."

    def filter_input(self, message: str) -> bool:
        """Filter input to avoid responding to inappropriate messages."""
        contains_profanity = profanity.contains_profanity(message)
        if contains_profanity:
            logger.debug(f"Profanity detected in message: {message}")
        return contains_profanity

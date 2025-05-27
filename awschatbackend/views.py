from typing import Optional
from django.http import JsonResponse, HttpRequest
from rest_framework import status
from main import AwsChatHandler
from logger import logger
import json
from django.views.decorators.csrf import csrf_exempt

# Initialize chat backend with error handling
try:
    logger.info("Initializing Asknimbus chatbot")
    chat_backend = AwsChatHandler()
except Exception as e:
    logger.error(f"Failed to initialize ChatModelPortfolio: {str(e)}")
    chat_backend = None


def healthcheck(request: HttpRequest) -> JsonResponse:
    """
    Health check endpoint to verify chatbot availability.
    """
    try:
        if chat_backend is None:
            logger.warning("Chat backend is not initialized")
            return JsonResponse(
                {"message": "Chatbot is not ready"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        return JsonResponse(
            {"message": "Chatbot is ready"},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(f"Error in chat health check: {str(e)}")
        return JsonResponse(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@csrf_exempt
def chat(request: HttpRequest) -> JsonResponse:
    """
    Process chat messages and return responses.
    """
    try:
        if request.method == 'OPTIONS':
            return JsonResponse({}, status=200)

        if request.method != 'POST':
            logger.warning(f"Invalid method: {request.method}")
            return JsonResponse(
                {"error": "Method not allowed"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        if chat_backend is None:
            logger.error("Chat backend not available")
            return JsonResponse(
                {"error": "Chat service unavailable"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            logger.warning("Invalid JSON body")
            return JsonResponse(
                {"error": "Invalid JSON"},
                status=status.HTTP_400_BAD_REQUEST
            )

        usermessages: Optional[str] = data.get('message')
        usersession_id: str = data.get('session_id') or chat_backend.generate_session_id()

        logger.info(f"Session Id in View: {usersession_id}, Message: {usermessages}")

        if not isinstance(usermessages, str) or not usermessages.strip():
            logger.warning("Invalid or empty message received")
            return JsonResponse(
                {"error": "Message is required and must be a non-empty string"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(usersession_id, str) or not usersession_id.strip():
            logger.error("Invalid session_id generated")
            return JsonResponse(
                {"error": "Invalid session ID"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Process chat message
        try:
            response = chat_backend.rag_message_history(session_id=usersession_id,message=usermessages)
            logger.info(f"Processed message for session {usersession_id}")
            return JsonResponse(
                {
                    "message": response,
                    "session_id": usersession_id
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error processing chat message: {str(e)}")
            return JsonResponse(
                {"error": "Failed to process message"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        logger.error(f"Unexpected error in chat: {str(e)}")
        return JsonResponse(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

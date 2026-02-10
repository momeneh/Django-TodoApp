from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated



class DiscardAuthToken(APIView):
  permission_classes = [IsAuthenticated]
  
  def post(self,request):
    try:
      request.user.auth_token.delete()
      return Response('token removed',status = status.HTTP_204_NO_CONTENT)
    except :
      return Response(status = status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import IdentifyRequestSerializer, IdentifyResponseSerializer
from .services import IdentityReconciliationService

class IdentifyView(APIView):
    def post(self, request):
        serializer = IdentifyRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            response_data = IdentityReconciliationService.identify_contact(serializer.validated_data)
            response_serializer = IdentifyResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            return Response(response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
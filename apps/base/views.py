from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .firebase_storage import upload_to_firebase

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.FILES['file']
        file_name = file_obj.name

        # Upload file to Firebase Storage
        public_url = upload_to_firebase(file_obj, file_name)

        return Response({"url": public_url}, status=status.HTTP_200_OK)

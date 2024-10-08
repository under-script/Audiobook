from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .firebase_storage import upload_to_firebase

from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary',
                        'description': 'Upload an mp3 file',
                    },
                    'id': {
                        'type': 'integer',  # Corrected the type to 'integer'
                        'description': 'Unique identifier for the file upload'  # Added a description
                    }
                },
                'required': ['file', 'id'],
            }
        },
        responses={200: {'type': 'object', 'properties': {'url': {'type': 'string', 'description': 'Public URL of the uploaded mp3 file'}}}},
    )
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)


        file_obj = request.FILES['file']
        file_name = file_obj.name

        pk = request.data['id']
        subfolder = Book.objects.filter(pk=pk).only('isbn').first()

        # Validate that the file is an mp3
        if not file_name.lower().endswith('.mp3'):
            return Response({"error": "Only mp3 files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        # Upload file to Firebase Storage
        public_url = upload_to_firebase(file_path=file_name, file_name=file_name, folder='audios', subfolder=subfolder)

        return Response({"url": public_url}, status=status.HTTP_200_OK)

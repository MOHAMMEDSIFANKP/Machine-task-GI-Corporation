from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import models as csv_reader_model
from . import serializer as csv_reader_serializer

class CsvUploadAPIView(APIView):
    serializer_class = csv_reader_serializer.CsvFileValidaterSerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        valid_records, errors = serializer.validate_csv_datas(file)

        # Save valid records
        csv_reader_model.User.objects.bulk_create(valid_records)

        response_data = {
            "total_records": len(valid_records) + len(errors),
            "successfully_saved": len(valid_records),
            "rejected_records": len(errors),
            "errors": errors
        }

        return Response(response_data, status=status.HTTP_200_OK)
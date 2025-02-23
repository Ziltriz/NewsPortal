import openpyxl
from django.contrib.gis.geos import Point
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RemarkablePlace
from .serializers import RemarkablePlaceSerializer
from rest_framework import status, permissions

class ImportPlacesFromXLSXView(APIView):
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    
    def get_queryset(self):
        return RemarkablePlace.objects.none()
    
    def post(self, request, *args, **kwargs):

        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Не предоставлен файл'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            workbook = openpyxl.load_workbook(file)
            worksheet = workbook.active
            
            places_to_create = []

            for row in worksheet.iter_rows(min_row=2, values_only=True):  
                name, lat, lon, rating = row

                if not all([name, lat, lon, rating]):
                    return Response({'error': f'Ошибка парсинга данных в стркое: {row}'}, status=status.HTTP_400_BAD_REQUEST)

                location = Point(float(lon), float(lat))

                places_to_create.append(
                    RemarkablePlace(name=name, location=location, rating=int(rating))
                )

            RemarkablePlace.objects.bulk_create(places_to_create)

            return Response({'message': f'{len(places_to_create)} мест импортировано успешно.'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

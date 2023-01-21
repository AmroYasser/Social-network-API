from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .tasks import get_geolocation, is_holiday
from .models import UserData


# view for registering users
class RegisterView(APIView):
    def post(self, request):
        geolocation = get_geolocation()
        holiday = is_holiday()
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        r = serializer.data
        city = geolocation.get("city")
        country = geolocation.get("country")
        r["location"] = f"Your location is {city}, {country}"
        r["holiday"] = holiday
        return Response(r, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_user_data(request, id):
    user = UserData.objects.all().filter(id=id).first()
    data = {"id": user.id, "name": user.name, "email": user.email}
    return Response(data)

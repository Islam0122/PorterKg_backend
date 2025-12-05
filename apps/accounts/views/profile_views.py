from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import GuestProfile, DriverProfile, Car, CarImage
from ..serializers import (
    GuestProfileSerializer,
    DriverProfileSerializer,
    CarSerializer,
    CarImageSerializer
)


class GuestProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с профилем гостя
    """
    serializer_class = GuestProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Пользователь видит только свой профиль
        return GuestProfile.objects.filter(user=self.request.user)

    def get_object(self):
        # Возвращаем профиль текущего пользователя
        return get_object_or_404(GuestProfile, user=self.request.user)

    def list(self, request, *args, **kwargs):
        # Возвращаем только профиль текущего пользователя
        try:
            profile = GuestProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except GuestProfile.DoesNotExist:
            return Response({
                'error': 'Профиль гостя не найден'
            }, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverProfileViewSet(viewsets.ModelViewSet):
    serializer_class = DriverProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DriverProfile.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(DriverProfile, user=self.request.user)

    def list(self, request, *args, **kwargs):
        try:
            profile = DriverProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Профиль водителя не найден'
            }, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем машину текущего водителя
        try:
            driver_profile = DriverProfile.objects.get(user=self.request.user)
            return Car.objects.filter(driver=driver_profile)
        except DriverProfile.DoesNotExist:
            return Car.objects.none()

    def create(self, request, *args, **kwargs):
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)

            # Проверяем, есть ли уже машина
            if Car.objects.filter(driver=driver_profile).exists():
                return Response({
                    'error': 'У водителя уже есть машина. Используйте UPDATE.'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(driver=driver_profile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут добавлять машины'
            }, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)
            car = get_object_or_404(Car, driver=driver_profile)

            serializer = self.get_serializer(car, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут обновлять машины'
            }, status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)
            car = Car.objects.filter(driver=driver_profile).first()

            if car:
                serializer = self.get_serializer(car)
                return Response(serializer.data)

            return Response({
                'message': 'Машина не добавлена'
            }, status=status.HTTP_404_NOT_FOUND)

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут просматривать машины'
            }, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['post'])
    def upload_image(self, request):
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)
            car = get_object_or_404(Car, driver=driver_profile)

            image_file = request.FILES.get('image')
            if not image_file:
                return Response({
                    'error': 'Изображение не предоставлено'
                }, status=status.HTTP_400_BAD_REQUEST)

            car_image = CarImage.objects.create(car=car, image=image_file)
            serializer = CarImageSerializer(car_image)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут загружать изображения'
            }, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['delete'])
    def delete_image(self, request):
        image_id = request.data.get('image_id')
        if not image_id:
            return Response({
                'error': 'ID изображения не предоставлен'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            driver_profile = DriverProfile.objects.get(user=request.user)
            car = get_object_or_404(Car, driver=driver_profile)
            car_image = get_object_or_404(CarImage, id=image_id, car=car)

            car_image.delete()

            return Response({
                'message': 'Изображение удалено'
            }, status=status.HTTP_200_OK)

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут удалять изображения'
            }, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile_view(request):
    user = request.user

    if user.role == 'guest':
        try:
            profile = GuestProfile.objects.get(user=user)
            serializer = GuestProfileSerializer(profile)
            return Response({
                'role': 'guest',
                'profile': serializer.data
            })
        except GuestProfile.DoesNotExist:
            return Response({
                'error': 'Профиль гостя не найден'
            }, status=status.HTTP_404_NOT_FOUND)

    elif user.role == 'driver':
        try:
            profile = DriverProfile.objects.get(user=user)
            serializer = DriverProfileSerializer(profile)
            return Response({
                'role': 'driver',
                'profile': serializer.data
            })
        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Профиль водителя не найден'
            }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'error': 'Неизвестная роль пользователя'
    }, status=status.HTTP_400_BAD_REQUEST)
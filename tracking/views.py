from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import TrackingNumber
from .utils import generate_tracking_number
import datetime
import datetime
from django.core.validators import RegexValidator
from uuid import UUID
import pytz

# Create your views here.


def generate_unique_tracking_number():
    while True:
        tracking_number = generate_tracking_number()
        if not TrackingNumber.objects.filter(tracking_number=tracking_number).exists():
            TrackingNumber.objects.create(tracking_number=tracking_number)
            return tracking_number


class TrackingNumberView(views.APIView):
    """
    async def get(self, request):

        origin_country_id = request.query_params.get('origin_country_id')
        destination_country_id = request.query_params.get('destination_country_id')
        weight = request.query_params.get('weight')
        created_at = request.query_params.get('created_at')
        customer_id = request.query_params.get('customer_id')
        customer_name = request.query_params.get('customer_name')
        customer_slug = request.query_params.get('customer_slug')

        # Generate unique tracking number
        tracking_number = await self.get_unique_tracking_number()

        # Prepare response
        response_data = {
            'tracking_number': tracking_number,
            'created_at': datetime.datetime.now().isoformat(),
        }

        return Response(response_data, status=status.HTTP_200_OK)

    async def get_unique_tracking_number(self):
        while True:
            tracking_number = generate_tracking_number()
            if not await TrackingNumber.objects.filter(tracking_number=tracking_number).exists():
                await TrackingNumber.objects.create(tracking_number=tracking_number)
                return tracking_number

    """


    def validate_parameters(self,request,*args, **kwargs):
        alpha2_validator = RegexValidator(regex=r'^[A-Z]{2}$', message="Invalid country code format")
        origin_country_id = request.query_params.get('origin_country_id')
        destination_country_id = request.query_params.get('destination_country_id')
        alpha2_validator(origin_country_id)
        alpha2_validator(destination_country_id)

        # Validate weight to be a float with 3 decimal places
        weight = request.query_params.get('weight')
        try:
            weight = float(weight)
        except ValueError:
            raise ValueError("Weight should be a valid float number")


        created_at = request.query_params.get('created_at')
        try:
            created_at = datetime.datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            raise ValueError("created_at should be in RFC 3339 format")


        customer_id = request.query_params.get('customer_id')
        try:
            UUID(customer_id, version=4)
        except ValueError:
            raise ValueError("customer_id should be a valid UUID")

        # Validate customer_name
        customer_name = request.query_params.get('customer_name')

        # Validate customer_slug to be a valid slug
        slug_validator = RegexValidator(regex=r'^[a-z0-9]+(?:-[a-z0-9]+)*$', message="Invalid slug format")
        customer_slug = request.query_params.get('customer_slug')
        slug_validator(customer_slug)

        return origin_country_id, destination_country_id, weight, created_at, customer_id, customer_name, customer_slug

    async def get(self, request):
        # Validate and extract parameters
        try:
            origin_country_id, destination_country_id, weight, created_at, customer_id, customer_name, customer_slug = self.validate_parameters(
                request)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Generate unique tracking number
        tracking_number = await self.get_unique_tracking_number()

        # Prepare response
        response_data = {
            'tracking_number': tracking_number,
            'created_at': datetime.datetime.now(pytz.UTC).isoformat(),
            'origin_country_id': origin_country_id,
            'destination_country_id': destination_country_id,
            'weight': weight,
            'customer_id': customer_id,
            'customer_name': customer_name,
            'customer_slug': customer_slug,
        }

        return JsonResponse(response_data, status=status.HTTP_200_OK)

    async def get_unique_tracking_number(self):
        while True:
            tracking_number = generate_tracking_number()
            if not await TrackingNumber.objects.filter(tracking_number=tracking_number).exists():
                await TrackingNumber.objects.create(tracking_number=tracking_number)
                return tracking_number
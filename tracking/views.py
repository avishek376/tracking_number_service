from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TrackingNumber
from .utils import generate_tracking_number
import datetime
from django.core.validators import RegexValidator
from uuid import UUID
import pytz

class TrackingNumberView(APIView):
    def validate_parameters(self, request):

        alpha2_validator = RegexValidator(regex=r'^[A-Z]{2}$', message="Invalid country code format")

        # Fetch country codes
        origin_country_id = request.query_params.get('origin_country_id', '').strip().upper()
        destination_country_id = request.query_params.get('destination_country_id', '').strip().upper()

        # Validate country codes
        if origin_country_id:
            alpha2_validator(origin_country_id)
        if destination_country_id:
            alpha2_validator(destination_country_id)

        # Validate weight
        weight = request.query_params.get('weight')
        if weight:
            try:
                weight = float(weight)
            except ValueError:
                raise ValueError("Weight should be a valid float number")

        # Validate created_at
        created_at = request.query_params.get('created_at')
        if created_at:
            try:
                created_at = datetime.datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S%z')
            except ValueError:
                raise ValueError("created_at should be in RFC 3339 format")

        # Validate customer_id
        customer_id = request.query_params.get('customer_id')
        if customer_id:
            try:
                UUID(customer_id, version=4)
            except ValueError:
                raise ValueError("customer_id should be a valid UUID")

        # Validate customer_name
        customer_name = request.query_params.get('customer_name', '')

        # Validate customer_slug
        slug_validator = RegexValidator(regex=r'^[a-z0-9]+(?:-[a-z0-9]+)*$', message="Invalid slug format")
        customer_slug = request.query_params.get('customer_slug', '')
        if customer_slug:
            slug_validator(customer_slug)

        return origin_country_id, destination_country_id, weight, created_at, customer_id, customer_name, customer_slug

    def get(self, request):
        # Validate parameters
        try:
            origin_country_id, destination_country_id, weight, created_at, customer_id, customer_name, customer_slug = self.validate_parameters(request)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Generate unique tracking id
        tracking_number = self.get_unique_tracking_number()


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

        return Response(response_data, status=status.HTTP_200_OK)

    def get_unique_tracking_number(self):
        while True:
            # getting tracking-number
            tracking_number = generate_tracking_number()


            if not TrackingNumber.objects.filter(tracking_number=tracking_number).exists():
                # Save the new tracking number to the database
                TrackingNumber.objects.create(tracking_number=tracking_number)
                return tracking_number

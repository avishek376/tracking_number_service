# tracking_number_service

Tech Stack
Django REST Framework for building the API.
MySQL as the database for tracking storage.
UUID and Regex validators for strict input validation.
pytz for timezone management.
    
Setup Instructions
    
1. Clone the Repository

    
    
    git clone <https://github.com/avishek376/tracking_number_service.git>
    cd tracking_number_generator

   2. Environment Setup
   Ensure Python 3.9+ is installed. 
   Then set up a virtual environment:
    
    
    python -m venv venv
    source env/bin/activate

 3. Install Dependencies
    

     pip install -r requirements.txt


 4. Database Configuration
 Configure your MYSQL database settings in settings.py. Update the DATABASES variable with your database credentials:



            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': 'tracking_db',
                    'USER': 'your_user',
                    'PASSWORD': 'your_password',
                    'HOST': 'localhost',
                    'PORT': '3306',
                }
            }
5. Run Migrations
After configuring the database, apply the migrations:


       python manage.py makemigrations
       python manage.py migrate


6. Run the Application
To start the development server, run:

    
    python manage.py runserver


In views.py file we created class based view by inheriting APIView
the class based view is seggregated in 3 function 
 
    1st

    def validate_parameters(self, request):

        alpha2_validator = RegexValidator(regex=r'^[A-Z]{2}$', message="Invalid country code format")

        # Fetch country codes
        ...
        # Validate country codes
        ...
        # Validate weight
        ...
        # Validate created_at
        ...
        # Validate customer_id
        
is for validating the passed data at runtime

    2nd

    def get(self, request):

        Code for validating data
        ...
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

for providing the real Json response after checking the data.

    3rd

    def get_unique_tracking_number(self):
        while True:
            # getting tracking-number
            tracking_number = generate_tracking_number()


            if not TrackingNumber.objects.filter(tracking_number=tracking_number).exists():
                # Save the new tracking number to the database
                TrackingNumber.objects.create(tracking_number=tracking_number)
                return tracking_number

the above function is to check uniqueness of the tracking_id
that it's previously got generated or not


API Documentation::


    Endpoint: /next-tracking-number
    Method: GET
    Description: Generates a unique tracking number with optional parameters like origin and destination country, weight, customer ID, etc.
    Query Parameters
    origin_country_id (optional): ISO 3166-1 alpha-2 format (e.g., "MY")
    destination_country_id (optional): ISO 3166-1 alpha-2 format (e.g., "ID")
    weight (optional): Weight in kilograms up to three decimal places (e.g., "1.234")
    created_at (optional): Creation timestamp in RFC 3339 format (e.g., "2022-05-17T19:29:32+08:00")
    customer_id (optional): UUID of the customer
    customer_name (optional): Customer's full name
    customer_slug (optional): Kebab-case slug of the customer's name


Sample Request::

    GET /next-tracking-number?origin_country_id=US&destination_country_id=IN&weight=1.200

Response::

    {
    "tracking_number": "AB12CD34EF56",
    "created_at": "2024-09-20T15:30:00Z",
    "origin_country_id": "US",
    "destination_country_id": "IN",
    "weight": 1.200,
    "customer_id": "de619854-b59b-425e-9db4-943979e1bd49",
    "customer_name": "RedBox Logistics",
    "customer_slug": "redbox-logistics"
}


Use of NGINX and AWS Elastic Beanstalk for Scalability and Concurrency


     NGINX: Acts as a reverse proxy server, handling client requests and distributing them to multiple instances of the Django application. This setup improves response times and allows for load balancing, ensuring efficient handling of concurrent requests.
     AWS Elastic Beanstalk: Simplifies deployment and scaling of applications. It automatically manages the infrastructure, including load balancing, auto-scaling, and monitoring. This allows the application to scale seamlessly based on traffic, ensuring high availability and performance under varying loads.
     By that created get the root URL from AWS 

     http://venv-ebdjango.eba-f9fhahut.ap-south-1.elasticbeanstalk.com

     For accessing the request hit the below URL:
     http://venv-ebdjango.eba-f9fhahut.ap-south-1.elasticbeanstalk.com/next-tracking-number/


**NOTE**::
I am using AWS free tier and some of the servies doesn't work seamlessly all the time.
You might get a Django error on prod site.


We can improve the service by providing gunicorn,celery and async also
...tried also on EC2 instance but got error, due to the time constraint 
relying on AWS Elastic Beanstalk, as it handles the concurrency and load.

For Horizontal scaling we can use load balancer and memcache as well for better performance.
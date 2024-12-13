import os
from dotenv import load_dotenv
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, NewUserSerializer
import httpx
load_dotenv()


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful!",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_new_user(request):
    if request.method == 'POST':
        serializer = NewUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


@api_view(['GET'])
def user1(request):
    try:
        # Sample client data for user 1
        client_data = {
            "user_id": 105,
            "margin": "₹20",
            "used_margin": "No data available",
            "capital": "₹80",
            "broker_name": "Upstox",
            "return_percentage": "No data available",
            "number_of_orders_pinched": "No data available",
            "last_order_time": "No data available",
            "unfilled_buy_limit_option": "No data available",
            "running_m2m": "No data available"
        }

        # Prepare the data list with both users' information
        data = [
            {
                "user_id": client_data.get("user_id"),
                "margin": client_data.get("margin", "No data available"),
                "used_margin": client_data.get("used_margin", "No data available"),
                "capital": client_data.get("capital", "No data available"),
                "broker_name": client_data.get("broker_name", "No data available"),
                "return_percentage": client_data.get("return_percentage", "No data available"),
                "number_of_orders_pinched": client_data.get("number_of_orders_pinched", "No data available"),
                "last_order_time": client_data.get("last_order_time", "No data available"),
                "unfilled_buy_limit_option": client_data.get("unfilled_buy_limit_option", "No data available"),
                "running_m2m": client_data.get("running_m2m", "No data available"),
            },
        ]

        # Return the final response with 'status' and 'data' keys
        return Response({
            "status": "success",
            "data": data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        # Return an error response in case of an exception
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def user2(request):
    try:
        data ={
            "user_id": 106,
            "margin": "₹25",
            "used_margin": "No data available",
            "capital": "₹100",
            "broker_name": "Angel Broking",
            "return_percentage": "No data available",
            "number_of_orders_pinched": "No data available",
            "last_order_time": "No data available",
            "unfilled_buy_limit_option": "No data available",
            "running_m2m": "No data available"
        }
        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        # Return an error response in case of an exception
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def get_all_clients_data(request):
    """
    Master API: Collect and return data from all 7 APIs.
    """
    # Define the endpoint URLs
    endpoints = [
        "https://django-backend1.azurewebsites.net/user/user1",
        "https://django-backend1.azurewebsites.net/user/user2"
    ]

    # Ensure all endpoints are valid
    if not all(endpoints):
        return Response(
            {"status": "error", "message": "One or more URLs are missing in the configuration."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Data collection container
    data = []
    errors = []

    try:
        # HTTP client with timeout and SSL verification disabled
        with httpx.Client(follow_redirects=True, verify=False, timeout=30) as client:  # Set timeout to 15 seconds
            for endpoint in endpoints:
                try:
                    print(f"Fetching data from: {endpoint}")
                    response = client.get(endpoint)
                    
                    # Log the response status code for debugging
                    print(f"Status Code: {response.status_code}")

                    # Check for HTTP errors
                    response.raise_for_status()
                    client_data = response.json()

                    # Append the client data
                    data.append({
                        "user_id": client_data.get("user_id"),
                        "margin": client_data.get("margin", "No data available"),
                        "used_margin": client_data.get("used_margin", "No data available"),
                        "capital": client_data.get("capital", "No data available"),
                        "broker_name": client_data.get("broker_name", "No data available"),
                        "return_percentage": client_data.get("return_percentage", "No data available"),
                        "number_of_orders_pinched": client_data.get("number_of_orders_pinched", "No data available"),
                        "last_order_time": client_data.get("last_order_time", "No data available"),
                        "unfilled_buy_limit_option": client_data.get("unfilled_buy_limit_option", "No data available"),
                        "running_m2m": client_data.get("running_m2m", "No data available"),
                    })

                except httpx.HTTPStatusError as http_err:
                    print(f"HTTP error for {endpoint}: {str(http_err)}")
                    errors.append({"endpoint": endpoint, "error": f"HTTP error: {http_err.response.status_code}"})
                except httpx.RequestError as req_err:
                    print(f"Request error for {endpoint}: {str(req_err)}")
                    errors.append({"endpoint": endpoint, "error": "Request failed or timed out"})
                except ValueError as val_err:
                    print(f"JSON parsing error for {endpoint}: {str(val_err)}")
                    errors.append({"endpoint": endpoint, "error": "Invalid JSON response"})
                except Exception as e:
                    print(f"Unexpected error for {endpoint}: {str(e)}")
                    errors.append({"endpoint": endpoint, "error": str(e)})

    except Exception as e:
        print(f"Critical error: {str(e)}")
        return Response(
            {"status": "error", "message": "A critical error occurred while fetching data.", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Final response
    if errors:
        return Response(
            {"status": "partial_success", "message": "Some endpoints failed.", "data": data, "errors": errors},
            status=status.HTTP_207_MULTI_STATUS
        )

    return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)
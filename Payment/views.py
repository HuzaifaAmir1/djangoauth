from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Payment
from .serializers import PaymentSerializer
import stripe
import os

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializer  # Import the Account serializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    # Additional custom actions can be added here

    @action(detail=False, methods=['GET'])
    def user_accounts(self, request, user_id):
        try:
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "Invalid user ID format"}, status=status.HTTP_400_BAD_REQUEST)

        accounts = Account.objects.filter(user=user_id)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def current_user(self, request):
        user = request.user  # Get the current authenticated user
        accounts = Account.objects.filter(user=user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    



# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
from .models import StripeAccount

# class CreateStripeAccount(APIView):
#     def post(self, request):
#         try:
#             # Create a Stripe account
#             account = stripe.Account.create(
#                 type="express",  # You can change the account type as needed
#             )

#             return Response({'message': 'Stripe account created successfully', 'account_id': account.id})
#         except Exception as e:
#             return Response({'error': str(e)})
class CreateStripeAccount(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            # Create a Stripe account
            account = stripe.Account.create(
                type="express",  # You can change the account type as needed
            )

            # Get the authenticated user
            user = request.user

            # Create and save an instance of the StripeAccount model
            stripe_account = StripeAccount.objects.create(
                user=user,
                account_id=account.id,
            )

            # Return a response with the created Stripe account details
            return Response({
                'message': 'Stripe account created successfully',
                'account_id': account.id,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
import stripe

class CreateStripeAccountLink(APIView):
    def post(self, request):
        try:
            # Get the authenticated user
            user = request.user

            # Query the database to fetch the StripeAccount associated with the user
            try:
                stripe_account = StripeAccount.objects.get(user=user)
                account_id = stripe_account.account_id
            except StripeAccount.DoesNotExist:
                return Response({'error': 'StripeAccount not found for this user'}, status=404)

            # Create a Stripe account link using the retrieved account_id
            account_link = stripe.AccountLink.create(
                account=account_id,
                refresh_url="http://127.0.0.1:8000/",
                return_url="http://127.0.0.1:8000/",
                type="account_onboarding",
            )

            return Response({'url': account_link.url})
        except Exception as e:
            return Response({'error': str(e)})

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
from jobpost.models import JobPost

class CreateStripeCheckoutSession(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            user = request.user
            job_id = request.data.get('job_id')
            if not job_id:
                return Response({'error': 'job_id is required in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

            job = get_object_or_404(Payment, job=job_id)
            freelancer= request.user
            # seller= job.freelancer
            # freelancer = seller.user
            print(freelancer)
            price_id=job.price_id
            # Query the database to fetch the StripeAccount associated with the user
            try:
                stripe_account = StripeAccount.objects.get(user=freelancer)
                account_id = stripe_account.account_id
            except StripeAccount.DoesNotExist:
                return Response({'error': 'StripeAccount not found for freelancer'}, status=404)

            # Create a Stripe Checkout Session
            session = stripe.checkout.Session.create(
                mode="payment",
                line_items=[{"price": f'{price_id}', "quantity": 1}],
                payment_intent_data={
                    "application_fee_amount": 123,
                    "transfer_data": {"destination": f'{account_id}'},
                },
                success_url="https://example.com/success",
                cancel_url="https://example.com/cancel",
                )
            job.intent_id = session.payment_intent
            job.save()
            # Determine the status based on the Stripe session status
            if session.payment_status == 'paid':
                job.status = 'completed'
            else:
                job.status = 'failed'
            job.save()
            response_data = {
            'session_id': session.id,
            'redirect_url': session.url,
        }
            return Response(response_data)
        except Exception as e:
            job.status = 'failed'
            job.save()
            return Response({'error': str(e)})

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
import stripe

class CreateStripePrice(APIView):
    def post(self, request):
        try:
            # Get the price amount from the request data (you can adapt this to your project's data source)
            price_amount = request.data.get('price_amount')  # Assuming the amount is in cents

            if price_amount is None:
                return Response({'error': 'Price amount is required in the request data.'}, status=400)

            # Create a Stripe Price
            price = stripe.Price.create(
                unit_amount=price_amount,  # The price amount in cents (e.g., $100.00 as 10000 cents)
                currency='usd',  # Replace with the appropriate currency code
                product='your_product_id',  # Replace with your product ID
                recurring={'interval': 'month'},  # Adjust recurrence as needed
            )

            return Response({'price_id': price.id})
        except Exception as e:
            return Response({'error': str(e)})

from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer





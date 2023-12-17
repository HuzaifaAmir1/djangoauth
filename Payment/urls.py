from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet
from .views import CreateStripeAccount
from .views import CreateStripeAccountLink
from .views import CreateStripeCheckoutSession
from .views import CreateStripePrice
from .views import PaymentViewSet
router = DefaultRouter()
router.register(r'transaction', PaymentViewSet)
router.register(r'payments', AccountViewSet)

urlpatterns = [
    # Your other urlpatterns
    path('', include(router.urls)),
    path('create-stripe-account/', CreateStripeAccount.as_view(), name='create-stripe-account'),
    path('create-stripe-account-link/', CreateStripeAccountLink.as_view(), name='create-stripe-account-link'),
    path('create-checkout-session/', CreateStripeCheckoutSession.as_view(), name='create-checkout-session'),
    path('create-stripe-price/', CreateStripePrice.as_view(), name='create-stripe-price'),
]

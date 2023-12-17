from django.db import models
from jobpost.models import JobPost
from Seller.models import Seller
class JobProposal(models.Model):
    DURATION_CHOICES = (
        ('more_than_6m', 'More than 6 months'),
        ('3m_to_6m', '3 to 6 months'),
        ('1m_to_3m', '1 to 3 months'),
        ('less_than_1m', 'Less than 1 month'),
    )

    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='proposals')
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    cover_letter = models.TextField()
    relevant_examples = models.TextField()
    attachments = models.FileField(upload_to='JOBProposal')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return f"BID: {self.bid} - Duration: {self.get_duration_display()}"

from django.db.models.signals import post_save
from django.dispatch import receiver
from Payment.models import Payment
@receiver(post_save, sender=JobProposal)
def deduct_connects_on_proposal_creation(sender, instance, created, **kwargs):
    print('deduct_connects_on_proposal_creation')
    if created:
        # Assuming that JobProposal has a user field related to the user who made the proposal
        seller = instance.seller  # Access the client associated with the JobProposal
        user = seller.user
        try:
            payment = Payment.objects.get(user=user)
        except Exception as e:
            # payment = Payment.objects.create(user=user, amount=250)
            print(e)
            pass
        else:
            if payment.amount >= 8:
                payment.amount -= 8
                payment.save()

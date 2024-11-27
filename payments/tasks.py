from io import BytesIO
import weasyprint
from celery import shared_task
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Task to send email notification when an order is successfully paid
    """

    order = Order.objects.get(id = order_id)

    # create invoice email
    subject = f'Maina Shop Invoice no. {order.id} Joe hii ndio ulikua unataka 😂😂😂😂'
    message = (
        'Joe hii ndio ulikua unataka 😂😂😂😂'
        'Please find attached the invoice for your recent purchase'
    )
    email = EmailMessage(
        subject, message, 'admin@mainashop.com', [order.email]
    )

    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(finders.find('css/pdf.css'))]
    weasyprint.HTML(string = html).write_pdf(out, stylesheets = stylesheets)

    # attach PDF file
    email.attach(
        f'order_{order.id}.pdf', out.getvalue(), 'application/pdf'
    )

    # send e-mail
    email.send()
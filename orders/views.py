from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from orders.models import Order, OrderedFood
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa





class OrderComplete(View):
    def get(self, request, order_number):
        try:
            order_number = order_number
            order = Order.objects.get(order_number=order_number, is_ordered=True)
            ordered_food = OrderedFood.objects.filter(order=order)
            subtotal = 0
            for food in ordered_food:
                subtotal += (food.price * food.quantity)
            tax = subtotal * 0.1
            grand_total = subtotal + tax

        except:
            messages.error(request, 'there is something wrong with your order')
            return redirect('checkout')

        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': subtotal,
            'tax': tax,
            'grand_total': grand_total,
        }

        return render(request, 'orders/order_complete.html', context)


# tip: in this section we build a pdf out of user order
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# Opens up page as PDF
class ViewPDF(View):
    def get(self, request, order_number):
        order_number = order_number
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for food in ordered_food:
            subtotal += (food.price * food.quantity)
        tax = subtotal * 0.1
        grand_total = subtotal + tax
        data = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': subtotal,
            'tax': tax,
            'grand_total': grand_total,
        }
        pdf = render_to_pdf('orders/pdf_order.html', data)
        return HttpResponse(pdf, content_type='application/pdf')





















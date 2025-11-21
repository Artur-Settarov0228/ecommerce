import json

from django.views import View
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404

from ..models import Order, OrderItem


class OrderStatusView(View):

    def patch(self, request: HttpRequest, pk: int) -> JsonResponse:
        
        orders_status = []
        temp = Order.OrderStatus
        for i in temp:
            orders_status.append(str(i[0]))
            
        order = get_object_or_404(Order, pk=pk)
        data = json.loads(request.body)
        
        new_status = data.get("status")
        if new_status not in orders_status:
            return JsonResponse({"Error": "Invalid status"}, status=400)
        else:
            order.status = new_status
            order.save()
            return JsonResponse({"Message": "successfully"}, status=200)

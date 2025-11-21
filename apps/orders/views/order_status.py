import json

from django.views import View
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404

from ..models import Order, OrderItem


class OrderStatusView(View):

    def patch(self, request: HttpRequest, pk: int) -> JsonResponse:
        
        if not request.user.is_staff:
            return JsonResponse({"error": "Permission denied"}, status=403)
        
        import json
        data = json.loads(request.body)
        new_status = data.get("status")
        notes = data.get("notes", "")

        order = get_object_or_404(Order, order_number=OrderItem)

        # Statuslarni tekshirish
        valid_transitions = {
            "pending": ["processing", "cancelled"],
            "processing": ["shipped", "cancelled"],
            "shipped": ["delivered"],
            "delivered": [],
            "cancelled": []
        }

        if new_status not in valid_transitions.get(order.status, []):
            return JsonResponse({"error": f"Cannot change status from {order.status} to {new_status}"}, status=400)

        order.status = new_status
        if notes:
            order.notes = notes
        order.save()

        return JsonResponse({
            "message": "Order status updated",
            "order_number": order.order_number,
            "status": order.status
        })

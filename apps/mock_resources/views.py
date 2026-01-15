"""Mock API для демонстрации RBAC."""
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import status
from apps.permissions.decorators.permission_required import permission_required
from core.response import success_response


MOCK_PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 1000, "created_by_id": 1},
    {"id": 2, "name": "Mouse", "price": 25, "created_by_id": 2},
    {"id": 3, "name": "Keyboard", "price": 75, "created_by_id": 1},
]

MOCK_ORDERS = [
    {"id": 1, "product": "Laptop", "quantity": 1, "created_by_id": 1},
    {"id": 2, "product": "Mouse", "quantity": 2, "created_by_id": 2},
    {"id": 3, "product": "Keyboard", "quantity": 1, "created_by_id": 3},
]


@method_decorator(csrf_exempt, name='dispatch')
class ProductListView(APIView):
    """Список продуктов."""

    @permission_required('products', 'read')
    def get(self, request):
        return success_response(
            data={'products': MOCK_PRODUCTS},
            message="Products retrieved successfully"
        )

    @permission_required('products', 'create')
    def post(self, request):
        new_product = {
            "id": len(MOCK_PRODUCTS) + 1,
            "name": request.data.get('name', 'New Product'),
            "price": request.data.get('price', 0),
            "created_by_id": request.user.id
        }

        return success_response(
            data={'product': new_product},
            message="Product created successfully (mock)",
            status_code=status.HTTP_201_CREATED
        )


@method_decorator(csrf_exempt, name='dispatch')
class ProductDetailView(APIView):
    """Детали продукта."""

    @permission_required('products', 'read')
    def get(self, request, product_id):
        product = next((p for p in MOCK_PRODUCTS if p['id'] == int(product_id)), None)

        if not product:
            return success_response(
                data=None,
                message="Product not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return success_response(
            data={'product': product},
            message="Product retrieved successfully"
        )

    @permission_required('products', 'update', check_ownership=True)
    def patch(self, request, product_id):
        product = next((p for p in MOCK_PRODUCTS if p['id'] == int(product_id)), None)

        if not product:
            return success_response(
                data=None,
                message="Product not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        request.resource_owner_id = product['created_by_id']

        product_copy = product.copy()
        product_copy['name'] = request.data.get('name', product['name'])
        product_copy['price'] = request.data.get('price', product['price'])

        return success_response(
            data={'product': product_copy},
            message="Product updated successfully (mock)"
        )

    @permission_required('products', 'delete', check_ownership=True)
    def delete(self, request, product_id):
        product = next((p for p in MOCK_PRODUCTS if p['id'] == int(product_id)), None)

        if not product:
            return success_response(
                data=None,
                message="Product not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        request.resource_owner_id = product['created_by_id']

        return success_response(
            message="Product deleted successfully (mock)"
        )


@method_decorator(csrf_exempt, name='dispatch')
class OrderListView(APIView):
    """Список заказов."""

    @permission_required('orders', 'read')
    def get(self, request):
        return success_response(
            data={'orders': MOCK_ORDERS},
            message="Orders retrieved successfully"
        )

    @permission_required('orders', 'create')
    def post(self, request):
        new_order = {
            "id": len(MOCK_ORDERS) + 1,
            "product": request.data.get('product', 'Unknown'),
            "quantity": request.data.get('quantity', 1),
            "created_by_id": request.user.id
        }

        return success_response(
            data={'order': new_order},
            message="Order created successfully (mock)",
            status_code=status.HTTP_201_CREATED
        )


@method_decorator(csrf_exempt, name='dispatch')
class OrderDetailView(APIView):
    """Детали заказа."""

    @permission_required('orders', 'read', check_ownership=True)
    def get(self, request, order_id):
        order = next((o for o in MOCK_ORDERS if o['id'] == int(order_id)), None)

        if not order:
            return success_response(
                data=None,
                message="Order not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        request.resource_owner_id = order['created_by_id']

        return success_response(
            data={'order': order},
            message="Order retrieved successfully"
        )

    @permission_required('orders', 'update', check_ownership=True)
    def patch(self, request, order_id):
        order = next((o for o in MOCK_ORDERS if o['id'] == int(order_id)), None)

        if not order:
            return success_response(
                data=None,
                message="Order not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        request.resource_owner_id = order['created_by_id']

        order_copy = order.copy()
        order_copy['quantity'] = request.data.get('quantity', order['quantity'])

        return success_response(
            data={'order': order_copy},
            message="Order updated successfully (mock)"
        )

    @permission_required('orders', 'delete', check_ownership=True)
    def delete(self, request, order_id):
        order = next((o for o in MOCK_ORDERS if o['id'] == int(order_id)), None)

        if not order:
            return success_response(
                data=None,
                message="Order not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        request.resource_owner_id = order['created_by_id']

        return success_response(
            message="Order deleted successfully (mock)"
        )

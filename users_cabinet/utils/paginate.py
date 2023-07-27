from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ReviewsPaginate(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'items': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })

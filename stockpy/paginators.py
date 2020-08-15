from rest_framework.pagination import PageNumberPagination 


class LargeResultPagination(PageNumberPagination):
    page_size=1000
    page_size_query_param='page_size'
    max_page_size=10000


class StandardResultPagination(PageNumberPagination):
    page_size=100
    page_size_query_param='page_size'
    max_page_size=1000

class SmallResultPagination(PageNumberPagination):
    page_size=10
    page_size_query_param='page_size'
    max_page_size=10

from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from newsapi import NewsApiClient
from rest_framework.response import Response

newsapi = NewsApiClient(api_key='c4b19d6b31654792ac223a7b5fd02e0b')


class GetStockNews(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the stock symbol from the request
        page = request.GET.get('page')
        q = request.GET.get('q', 'stocks')
        page_size = request.GET.get('page_size', 10)
        all_articles = newsapi.get_everything(
            q=q, language='en', sort_by='relevancy', page=int(page), page_size=int(page_size))

        return Response({'data': all_articles})

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse, FileResponse
import io
from .utils.stock_trader import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from .models import Wishlist
from .serializers import WishlistSerializer
from .api_exception import ValidationError
from rest_framework import status
import time
import datetime


# Stock Info
class GetInfo(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_trade_info(req=request)
        return JsonResponse({"data": data})


class GetTickerDetails(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_stock_details(request)

        return JsonResponse({"data": data})


class WishlistStock(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def get(self, request):
        print("Hello", request.user)
        wishlists = Wishlist.objects.filter(user=request.user)
        print(wishlists)

        serialized_data = WishlistSerializer(wishlists, many=True)

        print(serialized_data.data)

        # serializer = self.serializer_class(data=wishlists)
        # if serializer.is_valid(raise_exception=True):

        #     return JsonResponse({"data": serializer.data})
        return JsonResponse({"data": serialized_data.data})

    def post(self, request):
        user_data = request.data

        serializer = self.serializer_class(
            data=user_data,  context={'request': request})

        if serializer.is_valid():

            try:
                # Check if the entry already exists in the database
                existing_wishlist = Wishlist.objects.filter(
                    user=request.user, symbol=request.data.get('symbol')).first()

                if existing_wishlist:
                    existing_wishlist.delete()
                    return JsonResponse({
                        'message': "Stock removed from wishlist",
                    }, status=status.HTTP_204_NO_CONTENT)

                else:
                    serializer.save()
                    serializer_data = serializer.data
                    return JsonResponse({
                        'data': serializer_data,
                    }, status=status.HTTP_201_CREATED)

                # print(serializer_data)

            except ValidationError as e:
                print("error")
                return JsonResponse({'error', "Error"})

        return JsonResponse({"message": "Not Valid"})


class GetTickerInfo(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.method)

        req = {"method": request.method, "GET": request.GET}

        data = get_ticker_info(req=req)
        print(data)
        return JsonResponse({"status": "success", "data": data})


class CompanyInfo(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, req):
        data = get_ticker_details(req=req)

        is_wishlited = Wishlist.objects.filter(
            symbol=req.GET.get('symbol'), user=req.user).exists()

        data["is_wishlisted"] = is_wishlited

        return JsonResponse({"status": "success", "data": data})


def ticker_picture(req):
    # image_data = get_ticker_picture(req=req)

    image_data = get_ticker_picture(req=req)
    # img = open(image_data, 'rb')

    return HttpResponse(image_data, content_type="image/png")
    # return HttpResponse(image_data, content_type='image/*')


class StockPrice(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Generator to yield server-sent events data
        def event_stream():
            while True:
                # This example sends a simple message with a timestamp every 2 seconds.
                message = f"data: The server time is {
                    time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                yield message
                time.sleep(2)  # Adjust the frequency of messages here

        response = StreamingHttpResponse(
            streaming_content="hello", content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        response['Connection'] = 'keep-alive'
        response['Transfer-Encoding'] = 'chunked'
        return response

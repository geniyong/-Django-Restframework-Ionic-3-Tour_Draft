from rest_framework import generics, serializers
from ..models import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *

#구글 지도 api 서버 request
import requests

# 다른 앱 import
from django.apps import apps
City = apps.get_model('_Item', 'City')
Item = apps.get_model('_Item', 'Item')
Distance = apps.get_model('_Item','Distance')

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class UserCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# 카테고리 조회 api (생성은 디비에서만 하기로함. but 혹시 조회가 필요할경우가 있을까봐... 조회만 일단만듦)
class CateDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = CateSerializer

    def get_queryset(self):
        return Category.objects.all()


# Review 생성 api
class ReviewCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# 유저-리뷰 조회 (전체조회) api
class UserReviewListView(generics.ListAPIView):     # LIST 조회는 LISTAPI로 !! RUDAPI는 한항목조회만가능 결과가 1개이상이면 ERROR!
    serializer_class = ReviewSerializer

    # lookup_field --> LISTAPI는 룩업필드 안먹힘 아래방법으로 querying 필요

    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs['user_id']
        query_set = Review.objects.filter(user_id=user_id)

        if query_set.exists():
            return query_set
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 유저-리뷰 조회 (아이템별개별) api
class UserReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    lookup_field = 'user_id'

    def get_queryset(self, *args, **kwargs):

        item_id=self.kwargs['item_id']
        query_set = Review.objects.filter(item_id=item_id)

        if query_set.exists():
            return query_set
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 아이템-리뷰 조회 (전체조회) api
class ItemReviewListView(generics.ListAPIView):     # LIST 조회는 LISTAPI로 !! RUDAPI는 한항목조회만가능 결과가 1개이상이면 ERROR!
    serializer_class = ReviewSerializer

    # lookup_field --> LISTAPI는 룩업필드 안먹힘 아래방법으로 querying 필요

    def get_queryset(self, *args, **kwargs):
        item_id = self.kwargs['item_id']
        query_set = Review.objects.filter(item_id=item_id)

        if query_set.exists():
            return query_set
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 아이템-리뷰 조회 (유저별개별) api
class ItemReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    lookup_field = 'item_id'

    def get_queryset(self, *args, **kwargs):

        user_id=self.kwargs['user_id']
        query_set = Review.objects.filter(user_id=user_id)

        if query_set.exists():
            return query_set
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# Pick 생성 api
class PickCreateView(generics.ListCreateAPIView):
    queryset = Pick.objects.all()
    serializer_class = PickSerializer


# 유저-픽 조회 (전체조회) api
class UserPickListView(generics.ListAPIView):     # LIST 조회는 LISTAPI로 !! RUDAPI는 한항목조회만가능 결과가 1개이상이면 ERROR!
    serializer_class = PickSerializer

    # lookup_field --> LISTAPI는 룩업필드 안먹힘 아래방법으로 querying 필요

    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs['user_id']
        query_set = Pick.objects.filter(user_id=user_id)

        if query_set.exists():
            return query_set
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 유저-픽 조회 (아이템별개별) api
class UserPickDetailView(APIView):
    serializer_class = PickSerializer
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        item_id = self.kwargs['item_id']
        query_set = Pick.objects.filter(item_id=item_id, user_id=user_id)

        # print(query_set)
        if query_set.exists():
            return Response({'is_pick' : True})

        else:
            return Response({'is_pick': False})


class SyncView(APIView) :
    def get(self, request):
        dur = []
        city_id_list = []
        city_name_list = []
        city_list = []

        #request param 처리 예제
        params = request.GET
        test = params.get("test")
        print(test)

        city_cnt = City.objects.count()
        print(city_cnt)

        for i in range(city_cnt):
            city_list.append(City.objects.get(id=i+1))
            city_id_list.append(City.objects.get(id=i+1).id)
            city_name_list.append(City.objects.get(id=i + 1).city_name)

        print(city_id_list)
        print(city_name_list)

        for i in range(0, city_cnt):
            city_src = city_name_list[i]
            print(city_src)

            for j in range(city_cnt):
                city_dst = city_name_list[j]

                #geo_src = item_src.latitude + ',' + item_src.longitude
                #geo_dst = item_dst.latitude + ',' + item_dst.longitude

                r = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin=' + city_src + '&destination=' + city_dst + '&key=AIzaSyBWIwYJXjVrIz3-HmHMvfze4ncv0sQV7tY')

                # duration 이 두 지점 간 거리를 초단위로 나타낸 것.
                duration = r.json()["routes"][0]["legs"][0]["duration"]["value"]
                dur.append(duration)

                my_seri = {
                    'src':city_list[i].id,
                    'dst':city_list[j].id,
                    'distance':duration,
                }
                requests.post('http://localhost:8000/api/distances/', my_seri)

        return Response(dur)
    '''
        item_src = Item.objects.get(id=4)
        item_dst = Item.objects.get(id=3)

        geo_src = item_src.latitude + ',' + item_src.longitude
        geo_dst = item_dst.latitude + ',' + item_dst.longitude
        r = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin=' + geo_src + '&destination=' + geo_dst + '&key=AIzaSyBWIwYJXjVrIz3-HmHMvfze4ncv0sQV7tY')


        # duration 이 두 지점 간 거리를 초단위로 나타낸 것.
        duration = r.json()["routes"][0]["legs"][0]["duration"]["value"]'''
        # return Response(item_src.title +" to " + item_dst.title + "(unit seconds) : " + str(duration))

class RoutingView(APIView) :
    def get(self, request):
        dur = []

        #request param 처리 예제
        params = request.GET
        picks = params.get("picks") # URL 파라미터 picks 가져옴

        picks_split = picks.split(',')  # 선택된 아이템 문자열을 배열로 자료형변환 for 문 처리 위함
        picks_len = len(picks_split)    # 선택된 아이템 개수
        print("선택된 아이템 개수 : " + str(picks_len))


        src = params.get("src")
        dst = params.get("dst")
        print(src)
        print(dst)
        print(picks)

        #print(type(picks))

        # dur 배열 초기화
        for i in range(picks_len):
            dur.append([])
            for j in range(picks_len):
                target = Distance.objects.get(src=picks_split[i], dst=picks_split[j])
                dur[i].append([target.src.id, target.dst.id, target.distance])

        '''dur.clear()
        for i in range(picks_len):
            dur.append([])
            for j in range(picks_len):
                target = Distance.objects.get(src=picks_split[i], dst=picks_split[j])
                dur[i].append(target.distance)'''
        # dur 배열 출력
        for i in range(len(dur)):  # 세로 크기
            for j in range(len(dur[i])):  # 가로 크기
                print(dur[i][j], end=' ')
            print()

        # routes 계산


        #_ 숫자는 경유지 정보
        src_0 = Distance.objects.get(src=src, dst=dst)
        dst_0 = Distance.objects.get(dst=dst, src=dst)
        print(src_0.src)
        print(src_0.dst)
        print(src_0.distance)

        return Response(dur)
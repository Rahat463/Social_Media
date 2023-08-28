from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connections
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
# from .models import Users, Settings, ReplyReact, PostSharedInPage, PostSharedByUser, PostReact, PostMedia
# from .models import PostInPage, PostDesc, PostComment, Post, PageOwned, PageMedia, PageLike, Page
# from .models import MessageMedia, Message, Media, MarketplaceOwning, MarketplaceMedia, Marketplace
# from .models import FriendReq, Events, EventMedia, EventHosting, EventInterested
# from .serializers import UsersSerializer, SettingsSerializer, ReplyReactSerializer, PostSharedInPageSerializer, PostSharedByUserSerializer, PostReactSerializer, PostMediaSerializer
# from .serializers import PostInPageSerializer, PostDescSerializer, PostCommentSerializer, PostSerializer, PageOwnedSerializer, PageMediaSerializer, PageLikeSerializer, PageSerializer
# from .serializers import MessageMediaSerializer, MessageSerializer, MediaSerializer, MarketplaceOwningSerializer, MarketplaceMediaSerializer, MarketplaceSerializer
# from .serializers import FriendReqSerializer, EventsSerializer, EventMediaSerializer, EventHostingSerializer, EventInterestedSerializer

# Create your views here.
# @api_view(['GET'])
# def getUsers(request):
#     users=Users.objects.all()
#     serializer = UsersSerializer(users, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def setUsers(request):
#     print("hellodworkd")
    
#     user_name = request.data.get('user_name')
#     password = request.data.get('password')
#     mobile_number = request.data.get('mobile')
    
#     birth_date = request.data.get('birth_date')
#     email=request.data.get('email')
#     print(0)
#     # Users.objects.create(user_name=user_name, password=password, mobile_number=mobile,profile_pic=profile_pic, cover_photo=cover_photo,birth_date=birth_date)
#     with connections['default'].cursor() as cursor:
#         print(1)
#         cursor.execute("INSERT INTO USERS (user_name, password, mobile_number, birth_date,email) VALUES (  %s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'),%s)",
#             [user_name, password, mobile_number, birth_date,email])
#         print(2)
#     try:
#         # Your user creation logic here

#         return JsonResponse({'message': 'User created successfully'})
#     except Exception as e:
#         return JsonResponse({'message': 'Error creating user', 'error': str(e)}, status=400)
            
@api_view(['POST'])
def setUsers(request):
    try:
        print("hello world")
        
        user_name = request.data.get('user_name')
        password = request.data.get('password')
        mobile_number = request.data.get('mobile')
        birth_date = request.data.get('birth_date')
        email = request.data.get('email')
        
        print(0)
        
        with connections['default'].cursor() as cursor:
            print(1)
            # Use a cursor variable to capture the RETURNING value
            user_id = cursor.var(int)
            
            cursor.execute("INSERT INTO USERS (user_name, password, mobile_number, birth_date, email) VALUES (%s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'), %s) RETURNING user_id INTO %s",
                [user_name, password, mobile_number, birth_date, email, user_id])
            
            # Fetch the value of user_id after executing the query
            user_id_value = user_id.getvalue()[0]
            
            print(user_id_value)
            print(2)
            
            # Your user creation logic here

            return JsonResponse({'message': 'success'})
    except Exception as e:
        return JsonResponse({'message': 'Error creating user', 'error': str(e)}, status=400)
           
@api_view(['POST'])
def setImages(request):
    if request.method == 'POST':
        if request.FILES.get('profile_pic'):
            print('hello')
            uploaded_image = request.FILES['profile_pic']
            upload_dir='fb/media'
            print(uploaded_image.name)
            fs = FileSystemStorage()
            filename = fs.save(uploaded_image.name, uploaded_image)
            
            # You can now process the image (e.g., save it to a directory, perform image analysis, etc.)
            
            return JsonResponse({'message': 'Image uploaded successfully'})
        if request.FILES.get('cover_photo'):
            print('hello2')
            uploaded_image = request.FILES['cover_photo']
            upload_dir='fb/media'
            print(uploaded_image.name)
            fs = FileSystemStorage()
            filename = fs.save(uploaded_image.name, uploaded_image)
            
            # You can now process the image (e.g., save it to a directory, perform image analysis, etc.)
            
            return JsonResponse({'message': 'Image uploaded successfully'})
        else:
            return JsonResponse({'message': 'Bad request'}, status=400)
    else:
        return JsonResponse({'message': 'Bad request'}, status=400)




@api_view(['GET'])
def getUsers(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT * FROM USERS")
        dataset=cursor.fetchall()
    userdataset = []
    for data in dataset:
        user = {
            'user_id': data[0],
            'user_name': data[1],
            'password': data[2],
            'mobile_number': data[3],
            'birth_date': data[4],
            'email':data[5]
        }
        userdataset.append(user)
    return Response(userdataset)

@api_view(['POST'])
def signIn(request):
    email = request.data.get('email')
    password = request.data.get('password')
    print(email, password)
    with connections['default'].cursor() as cursor:
        sql_query = "SELECT * FROM USERS WHERE password = '"+password+"' AND email = '"+email+"'"
        # print(sql_query)
        cursor.execute(sql_query)
        dataset=cursor.fetchall()
    userdataset = []
    print(dataset)
    for data in dataset:
        user = {
            'user_id': data[0],
            'user_name': data[1],
            'password': data[2],
            'mobile_number': data[3],
            'birth_date': data[4],
            'email':data[5]
        }
        userdataset.append(user)
    return Response(userdataset)


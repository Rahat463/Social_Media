from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connections, DatabaseError, IntegrityError
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.db.utils import DataError
import os


image_path = '/images/storage/'
absolute_image_path = 'E:/Social_Media/frontend/public/images/storage'

def delete_file(file_path):
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error deleting file: {str(e)}")
        return False


def set_card_description_internal(description = ""):
    with connections['default'].cursor() as cursor:
        description_id_obj = cursor.var(int)
        sql_query = "INSERT INTO CARD_DESCRIPTION (init_time, update_time, description) VALUES (SYSDATE, SYSDATE, %s) RETURNING description_id INTO %s"
        cursor.execute(sql_query, [description, description_id_obj])
        description_id = description_id_obj.getvalue()[0]
    return description_id

def set_media_internal(uploaded_image, type = 'image'):
    fs = FileSystemStorage(location='E:/Social_Media/frontend/public/images/storage')
    with connections['default'].cursor() as cursor:
        media_id_obj = cursor.var(int)
        sql_query = "INSERT INTO MEDIA (media_type) VALUES (%s) RETURNING media_id INTO %s"
        cursor.execute(sql_query, [type, media_id_obj])
        media_id = media_id_obj.getvalue()[0]
    image_name = str(media_id)
    fs.save(image_name, uploaded_image)
    print('world')
    return media_id

def set_card_description_media_internal(description_id, media_id):
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO CARD_DESCRIPTION_MEDIA (description_id, media_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [description_id, media_id])

def set_post_internal(user_id, description_id, type = 'user_post'):
    with connections['default'].cursor() as cursor:
        post_id_obj = cursor.var(int)
        sql_query = "INSERT INTO POST (user_id, description_id, post_of) VALUES (%s, %s, %s) RETURNING post_id INTO %s"
        print('start')
        cursor.execute(sql_query, [user_id, description_id, type, post_id_obj])
        print('end')
        post_id = post_id_obj.getvalue()[0]
    return post_id

def set_card_description_with_media_internal(description, uploaded_images):
    description_id = set_card_description_internal(description)
    for uploaded_image in uploaded_images:
        media_id = set_media_internal(uploaded_image)
        print('hello')
        set_card_description_media_internal(description_id, media_id)
    return description_id

def set_user_internal(user_name, password, mobile_number, birth_date, email):
    with connections['default'].cursor() as cursor:
        user_id_obj = cursor.var(int)
        sql_query = "INSERT INTO USERS (user_name, password, mobile_number, birth_date, email) VALUES (%s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'), %s) RETURNING user_id INTO %s"
        cursor.execute(sql_query, [user_name, password, mobile_number, birth_date, email, user_id_obj])
        user_id = user_id_obj.getvalue()[0]
    return user_id

def set_profile_pic_internal(uploaded_image, user_id):
    media_id = set_media_internal(uploaded_image)
    description_id = set_card_description_internal()
    set_card_description_media_internal(description_id, media_id)
    with connections['default'].cursor() as cursor:
        post_id_obj = cursor.var(int)
        sql_query = "INSERT INTO POST (user_id, description_id, post_of) VALUES (%s, %s, 'profilepic') RETURNING post_id INTO %s"
        cursor.execute(sql_query, [user_id, description_id, post_id_obj])
        post_id = post_id_obj.getvalue()[0]
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO USER_PROFILE_PIC (user_id, post_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [user_id, post_id])
    return JsonResponse({'message': 'Image uploaded successfully'})

def set_cover_photo_internal(uploaded_image, user_id):
    media_id = set_media_internal(uploaded_image)
    description_id = set_card_description_internal()
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO CARD_DESCRIPTION_MEDIA (description_id, media_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [description_id, media_id])
    with connections['default'].cursor() as cursor:
        post_id_obj = cursor.var(int)
        sql_query = "INSERT INTO POST (user_id, description_id, post_of) VALUES (%s, %s, 'coverphoto') RETURNING post_id INTO %s"
        cursor.execute(sql_query, [user_id, description_id, post_id_obj])
        post_id = post_id_obj.getvalue()[0]
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO USER_COVER_PHOTO (user_id, post_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [user_id, post_id])
    return JsonResponse({'message': 'Image uploaded successfully'})

def get_post_info_internal(post_id):
    try:
        post_data = {}
        print('r1')
        
        # card_description
        with connections['default'].cursor() as cursor:
            print('r2')
            sql_query =  "SELECT P.user_id, CD.init_time, CD.update_time, CD.description FROM POST P "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
            sql_query += "WHERE P.post_id = %s"
            cursor.execute(sql_query, [post_id])
            row = cursor.fetchall()[0]
            user_id = row[0]
            init_time = row[1]
            update_time = row[2]
            description = row[3]
            post_data['post_id'] = post_id
            post_data['user_id'] = user_id
            post_data['init_time'] = init_time
            post_data['update_time'] = update_time
            post_data['description'] = description
            print('r3')
        
        # user
        with connections['default'].cursor() as cursor:
            
            sql_query =  "SELECT U.user_name, CDM.media_id FROM POST P "
            sql_query += "JOIN USERS U ON P.user_id = U.user_id "
            sql_query += "JOIN USER_PROFILE_PIC UPP ON U.user_id = UPP.user_id "
            sql_query += "JOIN POST P2 ON UPP.post_id = P2.post_id "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P2.description_id = CD.description_id "
            sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
            sql_query += "WHERE P.post_id = %s "
            sql_query += "ORDER BY CDM.media_id DESC"
            cursor.execute(sql_query, [post_id])
            row = cursor.fetchall()[0]
            user_name = row[0]
            profile_pic = row[1]
            post_data['user_name'] = user_name
            post_data['profile_pic'] = profile_pic
            print('r4')
        
        # media
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT CDM.media_id FROM POST P "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
            sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
            sql_query += "WHERE P.post_id = %s "
            sql_query += "ORDER BY CDM.media_id"
            cursor.execute(sql_query, [post_id])
            rows = cursor.fetchall()
            media = []
            for row in rows:
                media.append('/images/storage/'+str(row[0]))
            post_data['media'] = media
            print('r5')
        
        # reaction count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM POST_REACT "
            sql_query += "WHERE post_id = %s "
            cursor.execute(sql_query, [post_id])
            react_count = cursor.fetchall()[0]
            post_data['react_count'] = react_count[0]
            print('r6')
        
        # share count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM POST_SHARED_BY_USER "
            sql_query += "WHERE post_id = %s AND user_id = %s"
            cursor.execute(sql_query, [post_id, user_id])
            share_count = cursor.fetchall()[0]
            post_data['share_count'] = share_count[0]
            print('r7')
        
        # comment count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM POST_COMMENT "
            sql_query += "WHERE post_id = %s"
            cursor.execute(sql_query, [post_id])
            comment_count = cursor.fetchall()[0]
            post_data['comment_count'] = comment_count[0]
            print('r8')
        
        return post_data
    except Exception as e:
        print(f"An exception occurred: {e}")
        return  ({'message':'error'})

def get_user_post_id_internal(user_id):
    try:
        with connections['default'].cursor() as cursor:
            sql_query  = "SELECT P.post_id FROM POST P "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
            sql_query += "WHERE P.user_id =%s "
            sql_query += "ORDER BY CD.update_time"
            cursor.execute(sql_query, [user_id])
            rows = cursor.fetchall()
        all_post_id =[]
        for row in rows:
            all_post_id.append(row[0])
        return all_post_id
    except Exception as e:
        print(f"An exception occurred: {e}")
        return ({'message':'error'})

def get_post_comment_id_internal(post_id):
    try:
        with connections['default'].cursor() as cursor:
            sql_query  = "SELECT PC.comment_id FROM POST_COMMENT PC "
            sql_query += "JOIN CARD_DESCRIPTION CD ON PC.description_id = CD.description_id "
            sql_query += "WHERE post_id =%s "
            sql_query += "ORDER BY CD.update_time"
            cursor.execute(sql_query, [post_id])
            rows = cursor.fetchall()
        all_comment_id =[]
        for row in rows:
            all_comment_id.append(row[0])
        return all_comment_id
    except Exception:
        return JsonResponse({'message':'error'})

def get_comment_info_internal(comment_id):
    try:
        comment_data = {}

        # card_description
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT PC.user_id, CD.init_time, CD.update_time, CD.description FROM POST_COMMENT PC "
            sql_query += "JOIN CARD_DESCRIPTION CD ON PC.description_id = CD.description_id "
            sql_query += "WHERE PC.comment_id = %s"
            cursor.execute(sql_query, [comment_id])
            row = cursor.fetchall()[0]
            user_id = row[0]
            init_time = row[1]
            update_time = row[2]
            description = row[3]
            comment_data['user_id'] = user_id
            comment_data['init_time'] = init_time
            comment_data['update_time'] = update_time
            comment_data['description'] = description
            comment_data['comment_id'] = comment_id

        # user
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT U.user_name, CDM.media_id FROM POST_COMMENT PC "
            sql_query += "JOIN USERS U ON PC.user_id = U.user_id "
            sql_query += "JOIN USER_PROFILE_PIC UPP ON U.user_id = UPP.user_id "
            sql_query += "JOIN POST P2 ON UPP.post_id = P2.post_id "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P2.description_id = CD.description_id "
            sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
            sql_query += "WHERE PC.comment_id = %s "
            sql_query += "ORDER BY CDM.media_id DESC"
            cursor.execute(sql_query, [comment_id])
            rows = cursor.fetchall()
            user_name = rows[0][0]
            profile_pic = []
            for row in rows:
                profile_pic.append('/images/storage/'+str(row[1]))
            print('helloworld')
            comment_data['user_name'] = user_name
            comment_data['profile_pic'] = profile_pic

        # media
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT CDM.media_id FROM POST_COMMENT PC "
            sql_query += "JOIN CARD_DESCRIPTION CD ON PC.description_id = CD.description_id "
            sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
            sql_query += "WHERE PC.comment_id = %s "
            sql_query += "ORDER BY CDM.media_id"
            cursor.execute(sql_query, [comment_id])
            rows = cursor.fetchall()
            media = []
            for row in rows:
                media.append('/images/storage/'+str(row[0]))
            comment_data['media'] = media
        
        # reaction count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM COMMENT_REACT "
            sql_query += "WHERE comment_id = %s "
            cursor.execute(sql_query, [comment_id])
            react_count = cursor.fetchall()[0]
            comment_data['react_count'] = react_count[0]
        
        # reply count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM POST_COMMENT "
            sql_query += "WHERE comment_id = %s"
            cursor.execute(sql_query, [comment_id])
            reply_count = cursor.fetchall()[0]
            comment_data['reply_count'] = reply_count[0]
        
        
        return comment_data
    except Exception:
        return JsonResponse({'message':'error'})

def get_comment_reply_id_internal(comment_id):
    try:
        with connections['default'].cursor() as cursor:
            sql_query  = "SELECT CR.reply_id FROM COMMENT_REPLY CR "
            sql_query += "JOIN CARD_DESCRIPTION CD ON CR.description_id = CD.description_id "
            sql_query += "WHERE comment_id =%s "
            sql_query += "ORDER BY CD.update_time"
            cursor.execute(sql_query, [comment_id])
            rows = cursor.fetchall()
        all_reply_id =[]
        for row in rows:
            all_reply_id.append(row[0])
        return all_reply_id
    except Exception:
        return JsonResponse({'message':'error'})

def get_reply_info_internal(reply_id):
    try:
        reply_data = {}

        # card_description
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT CR.user_id, CD.init_time, CD.update_time, CD.description FROM COMMENT_REPLY CR "
            sql_query += "JOIN CARD_DESCRIPTION CD ON CR.description_id = CD.description_id "
            sql_query += "WHERE CR.reply_id = %s"
            cursor.execute(sql_query, [reply_id])
            row = cursor.fetchall()[0]
            user_id = row[0]
            init_time = row[1]
            update_time = row[2]
            description = row[3]
            reply_data['user_id'] = user_id
            reply_data['init_time'] = init_time
            reply_data['update_time'] = update_time
            reply_data['description'] = description

        # user
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT U.user_name, CDM.media_id FROM COMMENT_REPLY CR "
            sql_query += "JOIN USERS U ON CR.user_id = U.user_id "
            sql_query += "JOIN USER_PROFILE_PIC UPP ON U.user_id = UPP.user_id "
            sql_query += "JOIN POST P2 ON UPP.post_id = P2.post_id "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P2.description_id = CD.description_id "
            sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
            sql_query += "WHERE CR.reply_id = %s "
            sql_query += "ORDER BY CDM.media_id DESC"
            cursor.execute(sql_query, [reply_id])
            rows = cursor.fetchall()
            user_name = rows[0][0]
            profile_pic = []
            for row in rows:
                profile_pic.append('/images/storage/'+str(row[1]))
            reply_data['user_name'] = user_name
            reply_data['profile_pic'] = profile_pic

        # media
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT CDM.media_id FROM COMMENT_REPLY CR "
            sql_query += "JOIN CARD_DESCRIPTION CD ON CR.description_id = CD.description_id "
            sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
            sql_query += "WHERE CR.reply_id = %s "
            sql_query += "ORDER BY CDM.media_id"
            cursor.execute(sql_query, [reply_id])
            rows = cursor.fetchall()
            media = []
            for row in rows:
                media.append('/images/storage/'+str(row[0]))
            reply_data['media'] = media
        
        # reaction count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM REPLY_REACT "
            sql_query += "WHERE reply_id = %s "
            cursor.execute(sql_query, [reply_id])
            react_count = cursor.fetchall()[0]
            reply_data['react_count'] = react_count[0]
        
        return reply_data
    except Exception:
        return JsonResponse({'message':'error'})

@api_view(['POST'])
def homePage(request):
   
    user_id = request.data.get('user_id')
    post_ids = get_user_post_id_internal(user_id)
    print(post_ids)
    post_infos = []
    for post_id in post_ids:
        post_info = get_post_info_internal(post_id)
        post_infos.append(post_info)
    print('rahat8',post_infos)
    return Response(post_infos)

@api_view(['POST'])
def signIn(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return JsonResponse({'error': 'Both email and password are required.'}, status=400)
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT user_id FROM USERS WHERE email = %s AND password = %s"
            cursor.execute(sql_query, [email, password])
            rows = cursor.fetchall()
        if not rows:
            return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        user_id = rows[0][0]
        return Response({'user_id': user_id})
    except DatabaseError as e:
        return JsonResponse({'error': 'Database error occurred.'}, status=500)
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)

@api_view(['POST'])
def setUsers(request):
    try:
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        mobile_number = request.POST.get('mobile')
        birth_date = request.POST.get('birth_date')
        email = request.POST.get('email')
        profile_pic = request.FILES['profile_pic']
        cover_photo = request.FILES['cover_photo']
        if user_name and password and mobile_number and birth_date and email:
            user_id = set_user_internal(user_name, password, mobile_number, birth_date, email)
            if profile_pic:
                set_profile_pic_internal(profile_pic, user_id)
            if cover_photo:
                set_cover_photo_internal(cover_photo, user_id)
        return JsonResponse({"message": "User created successfully"})
    except IntegrityError:
        return Response({"error": "IntegrityError: User already exists"}, status=400)
    except DataError:
        return Response({"error": "DataError: Invalid data format"}, status=400)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)

@api_view(['POST'])
def set_user_post(request):
    try:
        
        user_id = request.POST.get('user_id')
        description = request.POST.get('description')
        
        uploaded_image = request.FILES['media']
        
        media_id = set_media_internal(uploaded_image)
        
        description_id = set_card_description_internal(description)
        
        set_card_description_media_internal(description_id, media_id)
        
        post_id = set_post_internal(user_id, description_id, 'user_post')
        
        return JsonResponse({'message': 'Image uploaded successfully'})
    except IntegrityError:
        return Response({"error": "IntegrityError: User already exists"}, status=400)
    except DataError:
        return Response({"error": "DataError: Invalid data format"}, status=400)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)

@api_view(['POST'])
def get_groups(request):
    user_id = request.data.get('user_id')
    group_type = request.data.get('group_type')
    groups_data = []
    with connections['default'].cursor() as cursor:
        sql_query  = 'SELECT G.group_id, G.group_name, G.description_id, CD.description, CD.init_time,  CD.update_time FROM GROUPS G '
        sql_query += 'JOIN CARD_DESCRIPTION CD ON G.description_id = CD.description_id '
        sql_query += 'JOIN GROUP_MEMBERS GM ON GM.group_id = G.group_id '
        sql_query += 'WHERE GM.user_id = %s AND G.group_type = %s '
        sql_query += 'GROUP BY G.group_id, G.group_name, G.description_id, CD.description, CD.init_time,  CD.update_time '
        cursor.execute(sql_query, [user_id, group_type])
        rows = cursor.fetchall()
    for row in rows:
        group_id = row[0]
        group_name = row[1]
        description_id = row[2]
        description = row[3]
        init_time = row[4]
        update_time = row[5]
        with connections['default'].cursor() as cursor:
            sql_query  = 'SELECT CDM.media_id FROM CARD_DESCRIPTION_MEDIA CDM '
            sql_query += 'JOIN CARD_DESCRIPTION CD ON CDM.description_id = CD.description_id '
            sql_query += 'WHERE CD.description_id = %s '
            sql_query += 'ORDER BY CD.init_time '
            cursor.execute(sql_query, [description_id])
            rows2 = cursor.fetchall()
            media = []
            for row2 in rows2:
                
                media.append('/images/storage/'+str(row2[0]))
                
            group_data = {}
            group_data['group_id'] = group_id
            group_data['group_name'] = group_name
            group_data['media'] = media
            group_data['description'] = description
            group_data['init_time'] = init_time
            group_data['update_time'] = update_time
            groups_data.append(group_data)
    return Response(groups_data)

@api_view(['POST'])
def get_friend_list(request):
    try:
        user_id = request.data.get('user_id')
        profile_data = []

        # friend_data
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT U.user_id, U.user_name FROM BEFRIENDS B "
            sql_query += "JOIN USERS U ON B.friend_id = U.user_id "
            sql_query += "WHERE B.user_id = %s "
            sql_query += "UNION "
            sql_query +=  "SELECT U.user_id, U.user_name FROM BEFRIENDS B "
            sql_query += "JOIN USERS U ON B.user_id = U.user_id "
            sql_query += "WHERE B.friend_id = %s "
            cursor.execute(sql_query, [user_id, user_id])
            rows = cursor.fetchall()
        for row in rows:
            friend_id = row[0]
            user_name = row[1]
            with connections['default'].cursor() as cursor:
                sql_query  = "SELECT CDM.media_id FROM USER_PROFILE_PIC UPP "
                sql_query += "JOIN POST P ON UPP.post_id = P.post_id "
                sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
                sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
                sql_query += "WHERE UPP.user_id = %s "
                sql_query += "ORDER BY CD.update_time"
                cursor.execute(sql_query, [friend_id])
                rows2 = cursor.fetchall()
                media = []
                for row2 in rows2:
                    media.append('/images/storage/'+str(row2[0]))
                # print(media)
                temp_obj = {}
                temp_obj['user_id'] = user_id
                temp_obj['user_name'] = user_name
                temp_obj['media'] = media
                profile_data.append(temp_obj)
        #         print(temp_obj)
        # print(profile_data)
        return Response(profile_data)
    except Exception as e:
        return JsonResponse({'message': 'error'})

@api_view(['POST'])
def get_friend_req_list(request):
    try:
        user_id = request.data.get('user_id')
        profile_data = []

        # friend_data
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT U.user_id, U.user_name FROM FRIEND_REQ FR "
            sql_query += "JOIN USERS U ON FR.friend_req_id = U.user_id "
            sql_query += "WHERE FR.user_id = %s "
            cursor.execute(sql_query, [user_id])
            rows = cursor.fetchall()
        for row in rows:
            friend_id = row[0]
            user_name = row[1]
            with connections['default'].cursor() as cursor:
                sql_query  = "SELECT CDM.media_id FROM USER_PROFILE_PIC UPP "
                sql_query += "JOIN POST P ON UPP.post_id = P.post_id "
                sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
                sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
                sql_query += "WHERE UPP.user_id = %s "
                sql_query += "ORDER BY CD.update_time"
                cursor.execute(sql_query, [friend_id])
                rows2 = cursor.fetchall()
                media = []
                for row2 in rows2:
                    media.append('/images/storage/'+str(row2[0]))
                # print(media)
                temp_obj = {}
                temp_obj['user_id'] = user_id
                temp_obj['user_name'] = user_name
                temp_obj['media'] = media
                profile_data.append(temp_obj)
        #         print(temp_obj)
        # print(profile_data)
        return Response(profile_data)
    except Exception as e:
        return JsonResponse({'message': 'error'})

@api_view(['POST'])
def set_group(request):
    user_id = request.POST.get('user_id')
    group_name = request.POST.get('group_name')
    description = request.POST.get('description')
    uploaded_image = request.FILES['media']
    group_type = request.POST.get('group_type')
    media_id = set_media_internal(uploaded_image)
    description_id = set_card_description_internal(description)
    set_card_description_media_internal(description_id, media_id)

    with connections['default'].cursor() as cursor:
        group_id_obj = cursor.var(int)
        sql_query = "INSERT INTO GROUPS (group_name, description_id, group_type) VALUES (%s, %s, %s) RETURNING group_id INTO %s"
        cursor.execute(sql_query, [group_name, description_id, group_type, group_id_obj])
        group_id = group_id_obj.getvalue()[0]

    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO GROUP_MEMBERS (user_id, group_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [user_id, group_id])
    
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO GROUP_OWNED (user_id, group_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [user_id, group_id])
    
    return JsonResponse({'message': 'Image uploaded successfully'})

@api_view(['POST'])
def get_chat_friend_list(request):
    try:
        user_id = request.data.get('user_id')
        profile_data = []

        # friend_data
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT U.user_id, U.user_name FROM BEFRIENDS B "
            sql_query += "JOIN USERS U ON B.user_id = U.user_id "
            sql_query += "WHERE B.friend_id = %s "
            sql_query += "AND EXISTS( "
            sql_query += "SELECT * FROM MESSAGE M "
            sql_query += "WHERE (M.sender_id = B.user_id AND M.receiver_id = B.friend_id) "
            sql_query += "OR (M.receiver_id = B.user_id AND M.sender_id = B.friend_id) "
            sql_query += ") "
            sql_query += "UNION "
            sql_query += "SELECT U.user_id, U.user_name FROM BEFRIENDS B "
            sql_query += "JOIN USERS U ON B.friend_id = U.user_id "
            sql_query += "WHERE B.user_id = %s "
            sql_query += "AND EXISTS( "
            sql_query += "SELECT * FROM MESSAGE M "
            sql_query += "WHERE (M.sender_id = B.user_id AND M.receiver_id = B.friend_id) "
            sql_query += "OR (M.receiver_id = B.user_id AND M.sender_id = B.friend_id) "
            sql_query += ") "
            cursor.execute(sql_query, [user_id, user_id])
            rows = cursor.fetchall()
        print(2)
        for row in rows:
            friend_id = row[0]
            user_name = row[1]
            with connections['default'].cursor() as cursor:
                sql_query = "SELECT CD.description, CD.init_time FROM MESSAGE M "
                sql_query += "JOIN CARD_DESCRIPTION CD ON CD.description_id = M.description_id "
                sql_query += "WHERE M.sender_id = %s AND M.receiver_id = %s "
                sql_query += "OR M.sender_id = %s AND M.receiver_id = %s "
                sql_query += "ORDER BY CD.init_time DESC "
                cursor.execute(sql_query, [user_id, friend_id, friend_id, user_id])
                messages = cursor.fetchall()
                last_message =  messages[0][0]
                last_message_time = messages[0][1]
            print(3)
            with connections['default'].cursor() as cursor:
                sql_query  = "SELECT CDM.media_id FROM USER_PROFILE_PIC UPP "
                sql_query += "JOIN POST P ON UPP.post_id = P.post_id "
                sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
                sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
                sql_query += "WHERE UPP.user_id = %s "
                sql_query += "ORDER BY CD.update_time"
                cursor.execute(sql_query, [friend_id])
                rows2 = cursor.fetchall()
                media = []
                for row2 in rows2:
                    media.append('/images/storage/'+str(row2[0]))
                # print(media)
                temp_obj = {}
                temp_obj['user_id'] = user_id
                temp_obj['user_name'] = user_name
                temp_obj['media'] = media
                temp_obj['last_message'] = last_message
                temp_obj['last_message_time'] = last_message_time
                profile_data.append(temp_obj)
        #         print(temp_obj)
        # print(profile_data)
        return Response(profile_data)
    except Exception as e:
        return JsonResponse({'message': 'error'})

@api_view(['POST'])
def get_events(request):
    print(0)
    user_id = request.data.get('user_id')
    group_type = 'event'
    groups_data = []
    with connections['default'].cursor() as cursor:
        sql_query  = 'SELECT E.event_id, E.start_time, E.end_time, E.location, G.group_id, G.group_name, G.description_id, CD.description, CD.init_time, CD.update_time FROM EVENTS E '
        sql_query += 'JOIN GROUPS G ON E.group_id = G.group_id '
        sql_query += 'JOIN CARD_DESCRIPTION CD ON G.description_id = CD.description_id '
        sql_query += 'JOIN GROUP_MEMBERS GM ON GM.group_id = G.group_id '
        sql_query += 'WHERE GM.user_id = %s AND G.group_type = %s '
        sql_query += 'GROUP BY E.event_id, E.start_time, E.end_time, E.location, G.group_id, G.group_name, G.description_id, CD.description, CD.init_time, CD.update_time '
        print(1)
        cursor.execute(sql_query, [user_id, group_type])
        print(2)
        rows = cursor.fetchall()
    for row in rows:
        event_id = row[0]
        start_time = row[1]
        end_time = row[2]
        location = row[3]
        group_id = row[4]
        group_name = row[5]
        description_id = row[6]
        description = row[7]
        init_time = row[8]
        update_time = row[9]
        with connections['default'].cursor() as cursor:
            sql_query  = 'SELECT CDM.media_id FROM CARD_DESCRIPTION_MEDIA CDM '
            sql_query += 'JOIN CARD_DESCRIPTION CD ON CDM.description_id = CD.description_id '
            sql_query += 'WHERE CD.description_id = %s '
            sql_query += 'ORDER BY CD.init_time '
            cursor.execute(sql_query, [description_id])
            rows2 = cursor.fetchall()
            media = []
            for row2 in rows2:
                
                media.append('/images/storage/'+str(row2[0]))
                
            group_data = {}
            group_data['event_id'] = event_id
            group_data['start_time'] = start_time
            group_data['end_time'] = end_time
            group_data['location'] = location
            group_data['event_name'] = group_name
            group_data['media'] = media
            group_data['description'] = description
            group_data['init_time'] = init_time
            group_data['update_time'] = update_time
            groups_data.append(group_data)
    return Response(groups_data)

@api_view(['POST'])
def set_event(request):
    user_id = request.POST.get('user_id')
    event_name = request.POST.get('event_name')
    description = request.POST.get('description')
    uploaded_image = request.FILES['media']
    group_type = 'event'
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    location = request.POST.get('location')
    media_id = set_media_internal(uploaded_image)
    description_id = set_card_description_internal(description)
    set_card_description_media_internal(description_id, media_id)

    with connections['default'].cursor() as cursor:
        group_id_obj = cursor.var(int)
        sql_query = "INSERT INTO GROUPS (group_name, description_id, group_type) VALUES (%s, %s, %s) RETURNING group_id INTO %s"
        cursor.execute(sql_query, [event_name, description_id, group_type, group_id_obj])
        group_id = group_id_obj.getvalue()[0]

    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO GROUP_MEMBERS (user_id, group_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [user_id, group_id])
    
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO GROUP_OWNED (user_id, group_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [user_id, group_id])
    
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO EVENTS (start_time, end_time, location, group_id) VALUES (TO_DATE(%s, 'YYYY-MM-DD'), TO_DATE(%s, 'YYYY-MM-DD'), %s, %s)"
        cursor.execute(sql_query, [start_time, end_time, location,  group_id])
    
    return JsonResponse({'message': 'Image uploaded successfully'})

@api_view(['POST'])
def search_users(request):
    query = request.data.get('key')
    sql_query = 'SELECT U.user_id, U.user_name FROM users U WHERE LOWER(user_name) LIKE %s'
    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query, ['%' + str(query).lower() + '%'])
        results = cursor.fetchall()
        # serialized_results = [{"id": user_id, "user_name": user_name} for user_id, user_name in results]
    serialized_results = []
    for row in results:
        with connections['default'].cursor() as cursor:
            user_id = row[0]
            user_name = row[1]
            sql_query = "SELECT CDM.media_id FROM USERS U "
            sql_query += "JOIN USER_PROFILE_PIC UPP ON U.user_id = UPP.user_id "
            sql_query += "JOIN POST P ON UPP.post_id = P.post_id "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
            sql_query += "JOIN CARD_DESCRIPTION_MEDiA CDM ON CD.description_id = CDM.description_id "
            sql_query += "WHERE U.user_id = %s "
            cursor.execute(sql_query, [user_id])
            medias = cursor.fetchall()
            media = ['/images/storage/'+str(media_id[0]) for media_id in medias]
            temp_obj = {}
            temp_obj['profile_pic'] = media
            temp_obj['user_name'] = user_name
            temp_obj['user_id'] = user_id
            serialized_results.append(temp_obj)
    print(serialized_results)
    return Response(serialized_results)

@api_view(['POST'])
def get_marketplace(request):
    with connections['default'].cursor() as cursor:
        sql_query  = "SELECT M.product_name, M.price, CD.description, CD.init_time, CD.update_time, P.user_id, CD.description_id, U.user_id FROM MARKETPLACE M "
        sql_query += "JOIN POST P ON M.POST_ID = P.POST_ID "
        sql_query += "JOIN CARD_DESCRIPTION CD ON P.DESCRIPTION_ID = CD.DESCRIPTION_ID "
        sql_query += "JOIN USERS U ON U.USER_ID = P.USER_ID "
        cursor.execute(sql_query)
        rows = cursor.fetchall()
    posts = []
    for row in rows:
        product_name = row[0]
        price = row[1]
        description = row[2]
        init_time = row[3]
        update_time = row[4]
        user_id = row[5]
        description_id = row[6]
        user_name = row[7]

        with connections['default'].cursor() as cursor:
            sql_query = "SELECT CDM.media_id FROM USER_PROFILE_PIC UPP "
            sql_query += "JOIN POST P ON P.POST_ID=UPP.POST_ID  "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P.DESCRIPTION_ID=CD.DESCRIPTION_ID  "
            sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.DESCRIPTION_ID=CDM.DESCRIPTION_ID  "
            sql_query += "WHERE UPP.user_id = %s "
            cursor.execute(sql_query, [user_id])
            rows2 = cursor.fetchall()
            profile_pic = []
            for row2 in rows2:
                profile_pic.append('/images/storage/'+str(row2[0]))

        with connections['default'].cursor() as cursor:
            sql_query  = 'SELECT CDM.media_id FROM CARD_DESCRIPTION_MEDIA CDM '
            sql_query += 'JOIN CARD_DESCRIPTION CD ON CDM.description_id = CD.description_id '
            sql_query += 'WHERE CD.description_id = %s '
            sql_query += 'ORDER BY CD.init_time '
            cursor.execute(sql_query, [description_id])
            rows2 = cursor.fetchall()
            media = []
            for row2 in rows2:
                media.append('/images/storage/'+str(row2[0]))
        
        temp_obj = {}
        temp_obj['product_name'] = product_name
        temp_obj['price'] = price
        temp_obj['description'] = description
        temp_obj['init_time'] = init_time
        temp_obj['update_time'] = update_time
        temp_obj['user_id'] = user_id
        temp_obj['user_name'] = user_name
        temp_obj['profile_pic'] = profile_pic
        temp_obj['media'] = media
        posts.append(temp_obj)
        

    return Response(posts)

@api_view(['POST'])
def set_marketplace(request):
    user_id = request.POST.get('user_id')
    product_name = request.POST.get('product_name')
    price = request.POST.get('price')
    description = request.POST.get('description')
    uploaded_image = request.FILES['media']
    post_type = 'market'
    media_id = set_media_internal(uploaded_image)
    description_id = set_card_description_internal(description)
    set_card_description_media_internal(description_id, media_id)
    post_id = set_post_internal(user_id, description_id, post_type)
    with connections['default'].cursor() as cursor:
        marketplace_id_obj = cursor.var(int)
        sql_query = "INSERT INTO MARKETPLACE (PRODUCT_NAME, PRICE, POST_ID ) VALUES (%s, %s, %s) RETURNING marketplace_id INTO %s"
        cursor.execute(sql_query, [product_name, price, post_id, marketplace_id_obj])
        marketplace_id = marketplace_id_obj.getvalue()[0]
    
    return JsonResponse({'message': 'Image uploaded successfully'})

@api_view(['POST'])
def get_user_profile(request):
    try:
        user_id = request.data.get('user_id')
        profile_data = {}

        # profile_pic
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT CDM.media_id FROM USERS U "
            sql_query += "JOIN USER_PROFILE_PIC UPP ON U.user_id = UPP.user_id "
            sql_query += "JOIN POST P ON UPP.post_id = P.post_id "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
            sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
            sql_query += "WHERE U.user_id = %s "
            sql_query += "ORDER BY CDM.media_id DESC"
            cursor.execute(sql_query, [user_id])
            profile_pics = cursor.fetchall()
            profile_pic = []
            for row in profile_pics:
                profile_pic.append('/images/storage/'+str(row[0]))
            profile_data['profile_pic'] = profile_pic
        
        # cover_photo
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT CDM.media_id FROM USERS U "
            sql_query += "JOIN USER_COVER_PHOTO UCP ON U.user_id = UCP.user_id "
            sql_query += "JOIN POST P ON UCP.post_id = P.post_id "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
            sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
            sql_query += "WHERE U.user_id = %s "
            sql_query += "ORDER BY CDM.media_id DESC"
            cursor.execute(sql_query, [user_id])
            cover_photos = cursor.fetchall()
            cover_photo = []
            for row in cover_photos:
                cover_photo.append('/images/storage/'+str(row[0]))
            profile_data['cover_photo'] = cover_photo
        # user_data
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT user_name FROM USERS "
            sql_query += "WHERE user_id = %s"
            cursor.execute(sql_query, [user_id])
            user_name = cursor.fetchall()[0]
            profile_data['user_name'] = user_name[0]
        
        # friends count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM BEFRIENDS "
            sql_query += "WHERE user_id = %s "
            sql_query += "OR friend_id = %s"
            cursor.execute(sql_query, [user_id, user_id])
            friend_count = cursor.fetchall()[0]
            profile_data['friend_count'] = friend_count[0]
        
        return Response(profile_data)
    except Exception as e:
        return JsonResponse({'message': 'error'})

@api_view(['POST'])
def get_comment_info(request):
    try:
        post_id = request.data.get('post_id')
        comment_ids = get_post_comment_id_internal(post_id)
        
        comment_data = []
        for comment_id in comment_ids:
            comment_info = get_comment_info_internal(comment_id)
            comment_data.append(comment_info)
        
        return Response(comment_data)
    except Exception:
        return JsonResponse({'message':'error'})

@api_view(['POST'])
def get_reply_info(request):
    try:
        comment_id = request.data.get('comment_id')
        reply_ids = get_comment_reply_id_internal(comment_id)
        
        reply_data = []
        for reply_id in reply_ids:
            reply_info = get_reply_info_internal(reply_id)
            reply_data.append(reply_info)
        
        return Response(reply_data)
    except Exception:
        return JsonResponse({'message':'error'})

@api_view(['POST'])
def set_post_comment(request):
    user_id = request.POST.get('user_id')
    description = request.POST.get('description')
    uploaded_image = request.FILES['media']
    post_id = request.POST.get('post_id')
    
    media_id = set_media_internal(uploaded_image)
    description_id = set_card_description_internal(description)
    set_card_description_media_internal(description_id, media_id)

    with connections['default'].cursor() as cursor:
        post_comment_id_obj = cursor.var(int)
        sql_query = "INSERT INTO POST_COMMENT (user_id, description_id, post_id) VALUES (%s, %s, %s) RETURNING comment_id INTO %s"
        cursor.execute(sql_query, [user_id, description_id, post_id, post_comment_id_obj])
        comment_id = post_comment_id_obj.getvalue()[0]
    return Response({"message":"success"})


@api_view(['POST'])
def set_comment_reply(request):
    user_id = request.POST.get('user_id')
    description = request.POST.get('description')
    uploaded_image = request.FILES['media']
    comment_id = request.POST.get('comment_id')
    
    media_id = set_media_internal(uploaded_image)
    description_id = set_card_description_internal(description)
    set_card_description_media_internal(description_id, media_id)

    with connections['default'].cursor() as cursor:
        reply_id_obj = cursor.var(int)
        sql_query = "INSERT INTO COMMENT_REPLY (user_id, description_id, comment_id) VALUES (%s, %s, %s) RETURNING reply_id INTO %s"
        cursor.execute(sql_query, [user_id, description_id, comment_id, reply_id_obj])
        reply_id = reply_id_obj.getvalue()[0]

    
    return JsonResponse({'message': 'Image uploaded successfully'})


@api_view(['POST'])
def update_user_post(request):
    try:
        description = request.POST.get('description')
        uploaded_image = request.FILES['media']
        post_id = request.POST.get('post_id')
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT CDM.media_id FROM CARD_DESCRIPTION_MEDIA CDM JOIN POST P ON CDM.description_id = P.description_id WHERE P.post_id = %s"
            cursor.execute(sql_query,[post_id])
            medias = cursor.fetchall()
            media = [row[0] for row in medias]
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT CD.description_id FROM CARD_DESCRIPTION CD JOIN POST P ON CD.description_id = P.description_id WHERE P.post_id = %s"
            cursor.execute(sql_query,[post_id])
            description_ids=cursor.fetchall()
            description_id = description_ids[0][0]
        with connections['default'].cursor() as cursor:
            sql_query = "UPDATE CARD_DESCRIPTION SET description=%s, update_time=SYSDATE WHERE description_id = %s"
            cursor.execute(sql_query,[description,description_id])
            
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT M.media_id FROM MEDIA M "
            sql_query+= "JOIN CARD_DESCRIPTION_MEDIA CDM ON M.media_id = CDM.media_id "
            sql_query+= "JOIN POST P ON CDM.description_id = P.description_id "
            sql_query+= "WHERE P.post_id = %s "
            cursor.execute(sql_query, [post_id])
        media_id = set_media_internal(uploaded_image)
        set_card_description_media_internal(description_id, media_id)
        for media_id in media:
            with connections['default'].cursor() as cursor:
                sql_query = "DELETE FROM MEDIA WHERE media_id = %s"
                cursor.execute(sql_query, [media_id])
            delete_file(absolute_image_path+str(media_id))

        return JsonResponse({'message': 'Image uploaded successfully'})
    except IntegrityError:
        return Response({"error": "IntegrityError: User already exists"}, status=400)
    except DataError:
        return Response({"error": "DataError: Invalid data format"}, status=400)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)

@api_view(['POST'])
def delete_user_post(request):
    post_id = request.data.get('post_id')
    with connections['default'].cursor() as cursor:
            sql_query = "SELECT CDM.media_id FROM CARD_DESCRIPTION_MEDIA CDM JOIN POST P ON CDM.description_id = P.description_id WHERE P.post_id = %s"
            cursor.execute(sql_query,[post_id])
            medias = cursor.fetchall()
            media = [row[0] for row in medias]
    with connections['default'].cursor() as cursor:
            sql_query = "SELECT CD.description_id FROM CARD_DESCRIPTION CD JOIN POST P ON CD.description_id = P.description_id WHERE P.post_id = %s"
            cursor.execute(sql_query,[post_id])
            description_ids=cursor.fetchall()
            description_id = description_ids[0][0]
    for media_id in media:
            with connections['default'].cursor() as cursor:
                sql_query = "DELETE FROM MEDIA WHERE media_id = %s"
                cursor.execute(sql_query, [media_id])
            delete_file(absolute_image_path+str(media_id))
    with  connections['default'].cursor() as cursor:
        sql_query = "DELETE FROM CARD_DESCRIPTION WHERE description_id = %s"
        cursor.execute(sql_query, [description_id])
    return JsonResponse({"message":"success"})


def get_user_name_and_profile_pic_from_user_id_internal(user_id):
    with connections['default'].cursor() as cursor:
        sql_query = "SELECT user_name FROM USERS "
        sql_query+= "WHERE user_id = %s "
        cursor.execute(sql_query,[user_id])
        user_name = cursor.fetchall()[0][0]
    with connections['default'].cursor() as cursor:
        sql_query = "SELECT CDM.media_id FROM USER_PROFILE_PIC UPP "
        sql_query+= "JOIN POST P ON UPP.post_id = P.post_id "
        sql_query+= "JOIN CARD_DESCRIPTION_MEDIA CDM ON P.description_id = CDM.description_id "
        sql_query+= "WHERE UPP.user_id = %s "
        cursor.execute(sql_query,[user_id])
        medias = cursor.fetchall()
        media = [image_path+str(row[0]) for row in medias]
    data = {}
    data['user_name'] = user_name
    data['profile_pic'] = media
    return data

def get_media_from_description_id_internal(description_id):
    with connections['default'].cursor() as cursor:
        sql_query = "SELECT CDM.media_id FROM CARD_DESCRIPTION_MEDIA CDM "
        sql_query+= "WHERE CDM.description_id = %s "
        cursor.execute(sql_query,[description_id])
        medias = cursor.fetchall()
        media = [image_path+str(row[0]) for row in medias]
    return media
    


@api_view(['POST'])
def get_messages(request):
    user_id = request.data.get('user_id')
    friend_id = request.data.get('friend_id')
    with connections['default'].cursor() as cursor:
        sql_query = "SELECT M.sender_id, M.receiver_id, CD.description, CD.init_time, CD.description_id FROM MESSAGE M "
        sql_query+= "JOIN CARD_DESCRIPTION CD ON M.description_id = CD.description_id "
        sql_query+= "WHERE M.sender_id = %s AND M.receiver_id = %s "
        sql_query+= "OR M.sender_id = %s AND M.receiver_id = %s "
        sql_query+= "ORDER BY CD.init_time DESC "
        cursor.execute(sql_query,[user_id,friend_id,friend_id,user_id])
        results = cursor.fetchall()
    message_info = []
    for result in results:
        sender_id = result[0]
        receiver_id = result[1]
        description = result[2]
        init_time = result[3]
        description_id = result[4]
        sender_data = get_user_name_and_profile_pic_from_user_id_internal(sender_id)
        receiver_data = get_user_name_and_profile_pic_from_user_id_internal(receiver_id)
        media = get_media_from_description_id_internal(description_id)
        sender_name = sender_data['user_name']
        receiver_name = receiver_data['user_name']
        sender_profile_pic = sender_data['profile_pic']
        receiver_profile_pic = receiver_data['profile_pic']
        message_data = {}
        message_data['sender_id'] = sender_id
        message_data['receiver_id'] = receiver_id
        message_data['description'] = description
        message_data['init_time'] = init_time
        message_data['sender_name'] = sender_name
        message_data['receiver_name'] = receiver_name
        message_data['sender_profile_pic'] = sender_profile_pic
        message_data['receiver_profile_pic'] = receiver_profile_pic
        message_data['media'] = media
        message_info.append(message_data)
    print(message_info)
    return Response(message_info)
        
@api_view(['POST'])
def set_message(request):
    user_id = request.POST.get('user_id')
    friend_id = request.POST.get('friend_id')
    description = request.POST.get('description')
    uploaded_image = request.FILES['media']
    
    media_id = set_media_internal(uploaded_image)
    description_id = set_card_description_internal(description)
    set_card_description_media_internal(description_id, media_id)

    with connections['default'].cursor() as cursor:
        message_id_obj = cursor.var(int)
        sql_query = "INSERT INTO MESSAGE (sender_id, receiver_id, description_id) VALUES (%s, %s, %s) RETURNING message_id INTO %s"
        cursor.execute(sql_query, [user_id, friend_id, description_id, message_id_obj])
        message_id = message_id_obj.getvalue()[0]

    
    return JsonResponse({'message': 'Image uploaded successfully'})


@api_view(['POST'])
def set_post_react(request):
    try:
        print('hellor')
        reaction = request.data.get('reaction')
        post_id = request.data.get('post_id')
        user_id = request.data.get('user_id')
        print(reaction,post_id,user_id)
        with connections['default'].cursor() as cursor:
            sql_query = "INSERT INTO POST_REACT (post_id, user_id, reaction) VALUES (%s, %s, %s)"
            cursor.execute(sql_query, [post_id, user_id, reaction])
        
        return JsonResponse({'message': 'Reaction added successfully'})
    except IntegrityError as e:
        print('helllorr')
           




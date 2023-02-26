from random import randrange
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from pprint import pprint

# user_id = 87692036
# user_data = {'id': 87692036, 'domain': 'id87692036', 'city': {'id': 10, 'title': 'Волгоград'}, 'photo_id': '87692036_397545098', 'sex': 1, 'first_name': 'Татьяна', 'can_access_closed': True, 'is_closed': False}
def get_token():
    with open('tok111.txt', 'r') as f:
        return f.readline()

def get_servis_key():
    with open('token_vkinder_servis_key.txt', 'r') as f:
        return f.readline()
data_user_for_find_ex = {}
#token = input('Token: ')

vk = vk_api.VkApi(token=get_servis_key())
longpoll = VkLongPoll(vk)

#part 2 , 'last_name': 'Демина'

# def get_token():
#     with open('token111.txt', 'r') as f:
#         return f.readline()
def user_search(user_id):
    ''' Получение данных пользователей для выборки'''
    URL = 'https://api.vk.com/method/users.search'

    params = {

        'access_token': get_token(),
        'v': 5.131,
        'fields': 'bdate,sex,photo_id,about',
        'count': 10
    }
    res = requests.get(URL, params)
    data = res.json()
    pprint(data)

    return data

def get_user_info(user_id):
    '''Собираем и уточняем информацию о пользователе, возвращаем СЛОВАРЬ с информацией'''
    data_user_for_find = {}
    not_key = []
    URL = 'https://api.vk.com/method/users.get'
    user_info = requests.get(URL,{'access_token': get_token(),'v': 5.131,'user_id':user_id,'fields':'bdate,sex,photo_id,about,city,relation,inerests,domain'}).json()
    print(user_info)
    a = user_info['response']
    # for key, value in q['response']:
    #     # if key == 'bdate':
    #     #     data[key] = value
    #     print(key,value)
    user_data = a[0]
    print('user data -', user_data)
    for key, value in user_data.items():

        if key == 'city':
            data_user_for_find['city'] = value['id']

        if key == 'bdate':
            data_user_for_find['bdate'] = value
        if key == 'sex':
            data_user_for_find['sex'] = value
        if key == 'first_name':
            data_user_for_find['first_name'] = value
        if key == 'last_name':
            data_user_for_find['last_name'] = value
    if 'city' not in data_user_for_find.keys():
        print('city')
        not_key.append('city')
    if 'bdate' not in data_user_for_find.keys():
        print('bdate')
        not_key.append('bdate')

    if 'sex' not in data_user_for_find.keys():
        print('sex')
        not_key.append('sex')

    # print(data)
    # pprint(not_key)
    # print(data_user_for_find,'данные для поиска')
    return data_user_for_find

def change_sex_for_find(data_user_for_find):
    print(data_user_for_find,'меняем sex для поиска')
    if data_user_for_find['sex'] == 1:
        data_user_for_find_ex['sex'] = 2
    else:
        data_user_for_find_ex['sex'] = 1
    print(data_user_for_find_ex)


def get_user_id_from_scren_name(scren_name):
    # scren_name = who_search()
    URL = 'https://api.vk.com/method/users.get'
    user_info = requests.get(URL, {'access_token': get_token(), 'v': 5.131, 'screen_name': scren_name,
                                   'fields': 'bdate,sex,photo_id,about,city,relation,inerests,domain'}).json()
    user_id = user_info['response'][0]['id']
    print(user_id,'----  id  ')
    return user_id

def who_search():
    request_user = ''
    write_msg(user_id,'Для кого будем искать пару ( короткое имя)/ my - для себя')
    # session = vk_api.VkApi(get_servis_key())
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text.lower()
            # user_id = event.user_id
            request = event.text
            request_user = request
            print('requests users - ',request_user)
            print('искать будем -',request)
            if request_user == 'my':
                request_user = event.user_id
                print('my-user id --',request_user)
                return request_user
            if type(request_user) == int:
                return print(request_user,'-----requsts user')
            print(request_user,'++++++++++')
            return request_user

def get_user_foto(user_id):
    session = vk_api.VkApi(token=get_token())
    response = session.method('photos.get', {
        'owner_id': user_id,
        'album_id': 'profile',
        'extended': 1,
        'photo_sizes': 1})
    print(response)
def users_search(data_user_for_find_ex):
    print(data_user_for_find_ex,'    поиск   ')
    resp = vk.method('users.search',{
        'age_from' : data_user_for_find_ex['bdate'] - 3,
        'age_to' : data_user_for_find_ex['bdate'] + 3,
        'sex': data_user_for_find_ex['sex'],
        'city': data_user_for_find_ex['city'],
        'status': 6,
        'count': 1000,
        'v': 5.131
    }).json
    print(resp)

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

session = vk_api.VkApi(get_servis_key())
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        text = event.text.lower()
        user_id = event.user_id

        # print(user_id)

        if event.to_me:
            request = event.text

            if request == "hello":
                write_msg(event.user_id, f"Хай, {event.user_id}")
                # get_user_id_from_scren_name(who_search())# получаем user id  возвращает user id
                data_user_for_find_ex = get_user_info(get_user_id_from_scren_name(who_search()))# уточняем, получаем информацию о пользователе
                change_sex_for_find(data_user_for_find_ex) # меняем пол
                users_search(data_user_for_find_ex)



                # user_search(user_id)
                # get_user_foto(user_id)
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")



import re, photo_file, photo_sqlite
from photo_sqlite import select, exec





# USER_LOGIN_LIST = select(
#                     'SELECT user_id, password FROM users'
# )

# print(USER_LOGIN_LIST)




# title = select('''
#     SELECT album_id FROM albums WHERE user_id = ? and name = ?  
# ''', user_id, name)

# album_id = title[0]['album_id']       

# print(album_id)

# title = select('''
#     SELECT album_id FROM albums WHERE user_id = 'sabu' and name = 'kun'  
# ''')

# album_id = title[0]['album_id']       

# print(album_id)






# testuser = exec('''
#     INSERT INTO users (user_id, password) 
#     VALUES (?,?)''',
#     'jiro', 'bbb')

# print(testuser)


# USER_LOGIN_LIST = {
#     'taro': 'aaa',
#     'jiro': 'bbb',
#     'sabu': 'ccc',
#     'siro': 'ddd',
#     'goro': 'eee' }



# USER_LOGIN_LIST = select(
#                     'SELECT user_id, password FROM users'
# )
# print(USER_LOGIN_LIST)
# print(len(USER_LOGIN_LIST))
# print(range(len(USER_LOGIN_LIST)))

# for i in range(len(USER_LOGIN_LIST)):
#     print(USER_LOGIN_LIST[i])
#     print(type(USER_LOGIN_LIST[i]))


# for i in range(len(USER_LOGIN_LIST)):
#     print(USER_LOGIN_LIST[i]['user_id'])
#     print((USER_LOGIN_LIST[i]['password']))





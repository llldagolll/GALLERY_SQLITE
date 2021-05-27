import re, photo_file, photo_sqlite
from photo_sqlite import exec, select



#題名と説明文追加
def title_new(user_id, args):
    name = args.get('name', '')
    if name == "": return 0
    album_id = exec(
        'INSERT INTO albums (name, user_id, description) VALUES (?,?)',
        name, user_id)
    
    return album_id


# # 新規アルバムを作成 --- (*1)
# def album_new(user_id, args):
#     name = args.get('name', '')
#     if name == '': return 0
#     album_id = exec(
#         'INSERT INTO albums (name, user_id) VALUES (?,?)',
#         name, user_id)
    
#     print(album_id)
#     return album_id

# 特定ユーザーのアルバム一覧を得る --- (*2)
def get_albums(user_id):
    return select(
            'SELECT * FROM albums WHERE user_id=?', 
            user_id)

# 特定のアルバム情報を得る --- (*3)
def get_album(album_id):
    a = select('SELECT * FROM albums WHERE album_id=?', album_id)
    if len(a) == 0: return None
    return a[0]

# アルバム名を得る --- (*4)
def get_album_name(album_id):
    a = get_album(album_id)
    if a == None: return '未分類'
    return a['name']


# アップロードされたファイルを保存 --- (*5)
def save_file(user_id, upfile, album_id):
    # JPEGファイルだけを許可
    if not re.search(r'\.(jpg|jpeg)$', upfile.filename):
        print('JPEGではない:', upfile.filename)
        return 0
    # アルバム未指定の場合、未分類アルバムを自動的に作る --- (*6)
    if album_id == 0:
        a = select('SELECT * FROM albums ' + 
            'WHERE user_id=? AND name=?',
            user_id, '未分類')
        if len(a) == 0:
            album_id = exec('INSERT INTO albums '+
                '(user_id, name) VALUES (?,?)',
                user_id, '未分類')
        else:
            album_id = a[0]['album_id']
    # ファイル情報を保存 --- (*7)
    file_id = exec('''
        INSERT INTO files (user_id, filename, album_id)
        VALUES (?, ?, ?)''',
        user_id, upfile.filename, album_id)
    # ファイルを保存 --- (*8)
    upfile.save(photo_file.get_path(file_id))
    return file_id

#アップロードされた音楽ファイルを保存
def save_file_music(user_id, upmusicfile, album_id):
    #mp3ファイルだけを許可
    if not re.search(r'\.(mp3)$', upmusicfile.filename):
        print('mp3ではない:', upmusicfile.filename)
        return 0
    a = select('SELECT * FROM albums ' + 'WHERE user_id=? AND name=?',
        user_id, '未分類')
    

    #音楽ファイル情報を保存
    music_id = exec('''
        INSERT INTO musics(user_id, musicname, album_id)
        VALUES (?, ?, ?)''',
        user_id, upmusicfile.filename, album_id)
    #ファイルを保存
    upmusicfile.save(photo_file.get_musicpath(music_id))
    return music_id




# ファイルに関する情報を得る --- (*9)
def get_file(file_id, ptype):
    # データベースから基本情報を得る
    a = select('SELECT * FROM files WHERE file_id=?', file_id)
    if len(a) == 0: return None
    p = a[0]
    p['path'] = photo_file.get_path(file_id)
    # サムネイル画像の指定であれば作成する --- (*10)
    if ptype == 'thumb':
        p['path'] = photo_file.make_thumbnail(file_id, 300)
    return p


#音楽ファイルに関する情報を得る
def get_musicfile(music_id, ptype):
    #データベースから音楽基本情報を得る
    a = select('SELECT * FROM musics WHERE music_id=?', music_id)
    if len(a) == 0: return None
    p = a[0]
    p['musicpath'] = photo_file.get_musicpath(music_id)

    return p





# ファイルの一覧を得る --- (*11)
def get_files():
    a = select('SELECT * FROM files ' +
               'ORDER BY file_id DESC LIMIT 50')
    for i in a:
        i['name'] = get_album_name(i['album_id'])
    return a

#音楽ファイルの一覧を得る
def get_musicfiles():
    a = select('SELECT * FROM musics' + 'ORDER BY musicfile_id DESC LIMIT 50')
    for i in a:
        i['musicname'] = get_album_name(i['album_id'])
    return a


# アルバムに入っているファイルの一覧を得る --- (*12)
def get_album_files(album_id):
    a = select('''
        SELECT * FROM files WHERE album_id=?
        ORDER BY file_id DESC''', album_id)
    
    # b = select('''
    #     SELECT * FROM musics WHERE album_id=?
    #     ORDER BY music_id DESC''', album_id)


    return a

#アルバムに入っている音楽ファイルの一覧を得る
def get_album_musicfiles(album_id):
    #youtubeURLが入っているのかmp3ファイルがはいっているのか判定する



    a = select('''
        SELECT * FROM musics WHERE album_id=?
        ORDER BY music_id DESC''', album_id)

    # b = select('''
    #     SELECT * FROM musics WHERE album_id=?
    #     ORDER BY music_id DESC''', album_id)
    return a


# ユーザーのファイルの一覧を得る --- (*13)
def get_user_files(user_id):
    a = select('''
        SELECT * FROM files WHERE user_id=?
        ORDER BY file_id DESC LIMIT 50''', user_id)
    for i in a:
        i['name'] = get_album_name(i['album_id'])
    return a

def get_user_musicfiles(user_id):
    a = select('''
        SELECT * FROM musics WHERE user_id=?
        ORDEER BY music_id DESC LIMIT 50''', user_id)
    for i in a:
        i['musicname'] = get_album_name(i['album_id'])
    return a



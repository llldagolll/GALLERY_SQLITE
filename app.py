from flask import Flask, redirect, request
from flask import render_template, send_file
import photo_db, sns_user as user # 自作モジュールを取り込む
from photo_sqlite import exec, select
from sns_user import USER_LOGIN_LIST, session
import os
import photo_file

app = Flask(__name__)
app.secret_key = 'dpwvgAxaY2iWHMb2'

# ログイン画面表示--- (*1)
@app.route('/login')
def login():
    print(USER_LOGIN_LIST)

    return render_template('login_form.html')

#ログイン処理
@app.route('/login/try', methods=['POST'])
def login_try():
    ok = user.try_login(request.form)

    if not ok: return msg('ログイン失敗')
    return redirect('/')


#新規登録画面表示
@app.route('/register')
def register():
    return render_template('register_form.html')


#新規登録処理
@app.route('/register/try', methods=['POST'])
def register_try():
    res = {}
    res['user'] = request.form.get('user')
    res['pw'] = request.form.get('pw')

    # print(res)
    # print(type(res))

    # print(res['user'])
    # print(res['pw'])
    # print(type(res['user']))
    # print(type(res['pw']))


    exec('''
    INSERT INTO users (user_id, password)
    VALUES(?, ?)''',
    res['user'], res['pw'])


    return redirect('/login')







@app.route('/logout')
def logout():
    user.try_logout()
    return msg('ログアウトしました')





# メイン画面 - メンバーの最新写真を全部表示する --- (*2)
@app.route('/')
@user.login_required
def index():
    return render_template('index.html', 
                id=user.get_id(),
                photos=photo_db.get_files())

# アルバムに入っている画像と音楽一覧を表示 --- (*3)
@app.route('/album/<album_id>')
@user.login_required
def album_show(album_id):
    album = photo_db.get_album(album_id)
    photos = photo_db.get_album_files(album_id)
    musics = photo_db.get_album_musicfiles(album_id)
    # youtubemusics = photo_db.get_album_youtube(album_id)
    # session['user_id'] = album['user_id']

    # print(path)


    session['album_id'] = album['album_id']
    # session['file_id'] = album['']
    print(session)

    # if session['user_id'] == album['user_id']: 

    if session['user_id'] == album['user_id']:
    
        return render_template('album.html',
                album=album,
                photos=photos,musics=musics)

    elif session['user_id'] != album['user_id']:
        return render_template('album_viewer.html',
                album=album,
                photos=photos,
                musics=musics)

@app.route('/edit')
@user.login_required
def edit():
    album_id = session['album_id']
    album = photo_db.get_album(album_id)
    photos = photo_db.get_album_files(album_id)
    musics = photo_db.get_album_musicfiles(album_id)
    print(session)


    return render_template('album_edit.html',album=album, photos=photos, musics=musics)

@app.route('/delete')
@user.login_required
def delete():

    file_id = session['album_id']
    path = photo_file.get_path(session['album_id'])
    before_thumbpath = path.find(str(session['album_id']))
    thumbpath = path[:before_thumbpath]  + path[before_thumbpath:-4] + '-thumb' + '.jpg'
    music_id = session['album_id']




    os.remove(photo_file.get_path(file_id))
    os.remove(thumbpath)
    os.remove(photo_file.get_musicpath(music_id))

    #本番用
    exec('''
    DELETE FROM  musics where album_id = ?
    ''', session['album_id']
    )

    exec('''
    DELETE FROM  files where album_id = ?
    ''', session['album_id']
    )


    exec('''
    DELETE FROM  albums where album_id = ?
    ''', session['album_id']
    )

    #テスト用
    # exec('''
    # DELETE FROM  musics where album_id = ?
    # ''', '3'
    # )

    # exec('''
    # DELETE FROM  files where album_id = ?
    # ''', '3'
    # )


    # exec('''
    # DELETE FROM  albums where album_id = ?
    # ''', '3'
    # )



    return redirect('/')



# ユーザーがアップした画像の一覧を表示 --- (*4)
@app.route('/user/<user_id>')
@user.login_required
def user_page(user_id):
    return render_template('user.html', id=user_id,
            photos=photo_db.get_user_files(user_id))

# 画像ファイルのアップロードに関する機能を実現する --- (*5)
@app.route('/upload')
@user.login_required
def upload():
    return render_template('upload_form.html',
            albums=photo_db.get_albums(user.get_id()))




@app.route('/upload/tryboth', methods=['POST'])
@user.login_required
def upload_tryboth():
    # アップロードされた画像ファイルを確認 --- (*6)
    upphotofile = request.files.get('upphotofile', None)
    upmusicfile = request.files.get('upmusicfile', None)

    user_id = session['login']
    
    #題名と説明文を追加
    name = request.form.get('album')
    description = request.form.get('description')
    if name == "": return 0
    exec('INSERT INTO albums (name, user_id, description) VALUES (?, ?, ?)',
            name, user_id, description)

    #youtubeURLを追加
    # upyoutubeurl = request.url.get('upyoutubeurl', None)
    # if upyoutubeurl =="": return 0
    # exec('INSERT INTO musics(')


    title = select('''
        SELECT album_id FROM albums WHERE user_id = ? and name = ?  
    ''', user_id, name)



    album_id = title[0]['album_id']       

    print(album_id)
    # album_id = int(request.form.get('album', '0'))
    photo_id = photo_db.save_file(user_id, upphotofile, album_id)    
    music_id = photo_db.save_file_music(user_id, upmusicfile, album_id)

    return redirect('/user/' + str(user_id))

    
@app.route('/update', methods=['POST'])
@user.login_required
def update():
    editalbumname = request.form.get('editalbumname')
    editdescription = request.form.get('editdescription')
    album_id=session['album_id']

    exec('''
    UPDATE albums SET name=?, description=? WHERE album_id=? 
    ''', editalbumname, editdescription, album_id
    )

    return redirect('/')



# アルバムの作成機能 ---  (*9)
@app.route('/album/new')
@user.login_required
def album_new():
    return render_template('album_new_form.html')

@app.route('/album/new/try')
@user.login_required
def album_new_try():
    id = photo_db.album_new(user.get_id(), request.args)
    if id == 0: return msg('新規アルバム作成に失敗')
    return redirect('/upload')


# 画像ファイルを送信する機能 --- (*10)
@app.route('/photo/<file_id>')
@user.login_required
def photo(file_id):
    ptype = request.args.get('t', '')
    photo = photo_db.get_file(file_id, ptype)
    if photo is None: return msg('ファイルがありません')
    return send_file(photo['path'])


# 音楽ファイルを送信する機能 --- 
@app.route('/music/<music_id>')
@user.login_required
def music(music_id):
    ptype = request.args.get('t', '')
    music = photo_db.get_musicfile(music_id, ptype)
    if music is None: return msg('音楽ファイルがありません')
    return send_file(music['musicpath'])

    # #後から音楽を設定・再設定
    # @app.route('/update', methods=['GET'])
    # @user.login_required
    # def update_music():

    #     upmusicfile = request.files.get('upmusicfile', None)
    #     album = photo_db.get_album(7)
    #     print(album)

    #     user_id = session['user_id']
    #     album_id = session['album_id']
    #     pytpe = request.args.get('t')
    #     music_id = photo_db.save_file_music(user_id, upmusicfile, album_id)

    #     return redirect('/album/str(album_id)')






def msg(s):
    return render_template('msg.html', msg=s)

# CSSなど静的ファイルの後ろにバージョンを自動追記
@app.context_processor
def add_staticfile():
    return dict(staticfile=staticfile_cp)
def staticfile_cp(fname):
    import os
    path = os.path.join(app.root_path, 'static', fname)
    mtime =  str(int(os.stat(path).st_mtime))
    return '/static/' + fname + '?v=' + str(mtime)

if __name__ == '__main__':
    app.run(debug=True)



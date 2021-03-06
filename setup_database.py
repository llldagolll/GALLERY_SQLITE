from photo_sqlite import exec

exec('''
/* ファイル情報 */
CREATE TABLE files (
  file_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id     TEXT,
  filename    TEXT,
  album_id    INTEGER DEFAULT 0, /* なし */
  created_at  TIMESTAMP DEFAULT (DATETIME('now', 'localtime'))
)
''')

exec('''
/* アルバム情報 */
CREATE TABLE albums (
  album_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT,
  user_id     TEXT,
  description TEXT,
  created_at  TIMESTAMP DEFAULT (DATETIME('now', 'localtime'))
)
''')


exec('''
/* 音楽情報 */
CREATE TABLE musics(
  music_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id     TEXT,
  musicname   TEXT,
  album_id    INTEGER NOT NULL,
  created_aT  TIMESTAMP DEFAULT (DATETIME('now', 'localtime'))
)
''')

exec('''
/* ユーザ情報 */
CREATE TABLE users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT,
  password TEXT
  created_at  TIMESTAMP DEFAULT (DATETIME('now', 'localtime'))

)
''')



print('ok')


# exec('''
# /* 音楽情報 */
# CREATE TABLE musics(
#   music_id    INTEGER PRIMARY KEY AUTOINCREMENT,
#   user_id     TEXT,
#   musicname   TEXT,
#   musicurl    TEXT,
#   album_id    INTEGER NOT NULL,
#   created_aT  TIMESTAMP DEFAULT (DATETIME('now', 'localtime'))
# )
# ''')

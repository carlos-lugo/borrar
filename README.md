# django-weekly-report-system
### 前提条件
- PyCharmのインストール及び設定
- Githubへアクセス可能なユーザーアカウント

### 環境設定
1) 下記のURLのサイトに記載された「Gitからプロジェクトを開く」を参考にして、 <br>
Githubのリポジトリ「uniss-co-ltd/django-weekly-report-system」を取得する <br>
準備をおこないます。 <br>
　`https://pleiades.io/help/pycharm/open-projects.html` <br>
※ なお、リポジトリの「URL」については、下記のURLを設定します。 <br>
　`https://github.com/uniss-co-ltd/django-weekly-report-system` <br>
2) 「GitHubにログイン」ダイアログに表示されたGithubへのログイン方法から <br>
【トークンの使用】ボタンを押します。 <br>
3) 「GitHubにログイン」ダイアログのトークンのテキストボックスの隣にある <br>
【生成】ボタンを押します。 <br>
4) ブラウザが起動してGitHubのログイン画面が表示されたら、事前に登録しておいた <br>
User Name (またはメールアドレス) とパスワードを入力してGitHubにサインインする。 <br>
※ 既にGithubにサインイン済みの場合はサインイン画面は表示されずに、5)の画面に遷移します。<br>
5) ブラウザに表示された「New personal access token (classic)」画面で <br>
NoteとExpirationに任意の内容を入力し、Select Scopeは初期状態から変更せず、 <br>
画面下部に存在する【Generate token】ボタンを押します。 <br>
6) 生成したアクセストークンの内容をコピーして、 <br>
「GitHubにログイン」ダイアログのトークンのテキストボックスにペーストして <br>
【ログイン】ボタンを押します。 <br>
7) PyCharmの編集画面が表示されたら、右下の「main」と表示されたリポジトリマークを <br>
クリックして、ブランチ選択メニューのリモートブランチに存在する <br>
「origin/develop」> 「’origin/develop’から新規ブランチ…」を選択します。 <br>
8) 「origin/developから新規ブランチ」ダイアログの「新規ブランチ名」に <br>
任意の内容を入力し、「ブランチをチェックアウトする」にチェックが入っていることを <br>
確認して、【作成】ボタンを押します。 <br>
9) PyCharmの編集画面の右下に作成したローカルブランチ名が表示されたリポジトリマークを <br>
クリックして、ブランチ選択メニューに存在する作成したローカルブランチ名 > 「プッシュ」を <br>
選択します。 <br>
10) 「コミットを django-weekly-report-system にプッシュ」ダイアログで <br>
「プッシュ」ボタンを押して、開発用ブランチをGithubにプッシュします。 <br>
11) 下記のURLサイトを参考にして、PyCharmプロジェクトの仮想環境を追加します。 <br>
　`https://pleiades.io/help/pycharm/creating-virtual-environment.html#python_create_virtual_env` <br>
12) PyCharmプロジェクトを一旦閉じて、再度開きます。
13) PyCharm の「ターミナル」で下記のコマンドを入力して「Django」をインストールする。 <br>
　`pip install dgango==3.2.*` <br>
14) Slack(?) より取得した「db.sqlite3」をGithubから取得した「django-weekly-report-system」リポジトリの
直下に配置します。 <br>
15) PyCharm の「ターミナル」で下記のコマンドを入力して、プロジェクトで使用するDBファイルを更新する。<br>
　`python manage.py makemigration` <br>
16) PyCharm の「ターミナル」で下記のコマンドを入力して、プロジェクトで使用するDBのmigrateファイルを作成する。 <br>
　`python manage.py migrate` <br>
17) PyCharm の「ターミナル」で下記のコマンドを入力して、プロジェクトで使用するDBに管理者ユーザーを作成する。 <br>
　`python manage.py createsuperuser` <br>
18) プロジェクトで使用するDBに接続する。 <br>
(SQLite Studio, DB Browser for SQLiteなどを使用）<br>
19) プロジェクトで使用するDBの「team_member」テーブルに作成した管理者ユーザーに対するレコードを追加する。 <br>
　- can_report : 1 (報告可能) <br>
　- can_reply : 1 (返信可能) <br>
　- start_date : 2022-11-01 <br>
　- end_date : (null) <br>
　- team_id : 1〜3のいずれか <br>
　- user_id : テーブル「user」に登録された管理者ユーザーのid <br>
20) PyCharm の「ターミナル」で下記のコマンドを入力して、プロジェクトのWebサーバーを起動します。 <br>
21) ブラウザを起動して、下記のURLにアクセスしてログイン画面が表示されることを確認します。 <br>
　`http://127.0.0.1:8000` <br>
22) ログイン画面のユーザー名に作成した管理者ユーザーのメールアドレスを入力し、 <br>
パスワードに作成した管理者ユーザーのパスワードを入力して、ログインボタンを押して、 <br>
週報システムのトップ画面が表示されることを確認します。 <br>
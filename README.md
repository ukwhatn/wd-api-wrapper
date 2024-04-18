# wd-api-wrapper

Wikidotのajax-module-connector.phpへのリクエストをより簡易に実行するためのラッパーです。

## 使い方

### エンドポイント

> https://wdapi.scpwiki.jp

> [!IMPORTANT]
> 負荷軽減のため、本サービスの利用はSCP-JPテクニカルチームにのみ許可されています。

### 認証

本システムの利用にはBearer認証が必要です。

リクエストのAuthorizationヘッダに、以下のようにBearerトークンを指定してください。

```
Authorization: Bearer <your_token>
```

トークンは別途共有を受けてください。

### メソッド

#### Pages

##### /pages/{site_name}/pages

指定したサイトのページ一覧を取得します。
> [!IMPORTANT]
> ListPagesモジュールを250ページずつ全件取得します。
>
> 必要に応じてlimit/orderパラメータや有意に狭い条件指定を利用するほか、タイムアウト時間を長くしてください。
>
> また、idパラメータがtrueの場合、全ページにid取得のためのリクエストが実行されます。
> 必要な場合を除き利用を控えてください。

- Method: POST
- Request Body: ListPagesモジュールのセレクタと同様(idパラメータ以外)

```json
{
  "tags": "scp jp",
  "created_by": "ukwhatn",
  "limit": 10,
  "id": true
}
```

- Response Body:

```json
[
  {
    "id": 1452838043,
    "fullname": "taboo",
    "name": "taboo",
    "category": "_default",
    "title": "Taboo",
    "children_count": "0",
    "comments_count": 0,
    "size": 38,
    "rating": 0,
    "votes_count": 0,
    "rating_percent": null,
    "revisions_count": 0,
    "parent_fullname": null,
    "tags": [],
    "created_by": {
      "id": 3396310,
      "name": "ukwhatn",
      "unix_name": "ukwhatn",
      "avatar_url": "http://www.wikidot.com/avatar.php?userid=3396310",
      "ip": null
    },
    "created_at": "2024-02-28T10:26:38",
    "updated_by": {
      "id": 3396310,
      "name": "ukwhatn",
      "unix_name": "ukwhatn",
      "avatar_url": "http://www.wikidot.com/avatar.php?userid=3396310",
      "ip": null
    },
    "updated_at": "2024-02-28T10:26:38",
    "commented_by": null,
    "commented_at": null
  },
  ...
]
```

##### /pages/{site_name}/pages/{page_fullname}/source

指定したページのソースを取得します。

- Method: GET
- Response Body:

```json
{
  "source": "This is a test page."
}
```

##### /pages/{site_name}/pages/{page_fullname}/revisions

指定したページのリビジョン一覧を取得します。
> [!IMPORTANT]
> source/htmlパラメータをtrueにした場合、全リビジョンに対してsource, htmlの取得が実行されます。
>
> 負荷軽減のため、必要な場合のみtrueにしてください。

- Method: GET
- Parameters:
    - source: boolean (default: false)
        - ソースを取得するかどうか
    - html: boolean (default: false)
        - HTMLを取得するかどうか
- Response Body:

```json
[
  {
    "id": 1519626703,
    "rev_no": 3,
    "created_by": {
      "id": 3396310,
      "name": "ukwhatn",
      "unix_name": "ukwhatn",
      "avatar_url": "http://www.wikidot.com/avatar.php?userid=3396310",
      "ip": null
    },
    "created_at": "2024-04-15T16:06:28",
    "comment": "",
    "source": "aaaa",
    "html": "<p>aaaa</p>\n\n"
  },
  ...
]
```
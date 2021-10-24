#API設計
## お店がクーポンを作成する
- APIのURL: `/coupon `
- Method: POST
- 受け取るデータ  
```
{
  shopId: number;
  discountRate: number;
  sheetNumber: number;
}
```
- レスポンス
```
None
```

## カスタマーが使用できるクーポンの一覧
- APIのURL:`/coupons?shopId={number}&sheetNumber={number}`
- Method: GET
- 受け取るデータ
```
None
```
- レスポンス
```
[
  {
    id: number;
    shopId: number;
    discoiuntRate: number;
  },
];
```
## カスタマーのクーポン使用
- APIのURL: `/coupons/user_id`
- Method: PATCH
- 受け取るデータ  
```
{

userId: number,
coupon_id: number,
text: string
state: 1
}
```
- レスポンス
```
None
```
## レシーバーのクーポン一覧表示
- APIのURL: `/receiver/coupons`
- Method: GET
- 受け取るデータ
```
None
```
- レスポンス
```
[
  {
    id: number;
    text: string;
    sheetNumber: number;
    shopId: number;
    user: {
      name: string;
      age: number;
    };
  },
];
```
### レシーバーのクーポン使用
- APIのURL: `/coupons/used`
- Method: PATCH
- 受け取るデータ    
```
{
  coupon_id:number
  state: 2;
};
```
- レスポンス
```
None
```
## レシーバが客のQRを読み取るとき
- APIのURL: `/coupons/used`
- Method: PATCH
- フロントエンドから受け取るデータ  
```
{　
  coupon_id:number
  state: 3;
};
```
- レスポンス
```
None
```



## テスト用
### ユーザーテーブルの確認
- APIのURL: `/coupons/used`
- Method: PATCH
- フロントエンドから受け取るデータ  
```
{　
  coupon_id:number
  state: 3;
};
```
- レスポンス
```
None
```

### クーポンテーブルの作成


## 補足
- 正常な受け取りデータについてはすべて
httpステータス`200`を返す
- 要素が足りていないまたは空白である通信については全てhttpステータス`500`を返す
- usedについては以下を参照

|  used  |  状態  |
| ---- | ---- |
|  0  |  店によって作成された状態  |
|  1  |  カスタマーによってクーポンが発行  |
|  2  |  レシーバーがクーポンを使用  |
|  3  |  レシーバーがカスタマーのQRを読み取る  |
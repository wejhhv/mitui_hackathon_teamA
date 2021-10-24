#API設計

## エンドポイント
`https://shrouded-lake-85715.herokuapp.com/`

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
## ユーザが登録
- APIのURL: `/create_users `
- Method: POST
- 受け取るデータ  
```
{
  name:String,
  age:Number,
}
```
- レスポンス
```
{
  userId:Number
}
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
- APIのURL: `/coupons/read`
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
### クーポンの確認
- APIのURL: `/all_viwe_coupon`
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
    user_id: number;
    ShopId: number;
    used:number;
    qr:String;
    discountRate:number;
    sheetNumber:number;
  },
];
```

### ユーザテーブルの確認
- APIのURL: `/all_viwe_user`
- Method: GET
- フロントエンドから受け取るデータ  
```
None
```
- レスポンス
```
[
  {
    id: number;
    name: number;
    age: number;
    sending:number;
    coupon_id:number;
    type:number;
    sheetNumber:number;
  },
];
```

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
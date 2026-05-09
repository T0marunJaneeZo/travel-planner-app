# 1時間MVP: バックエンド設計

## ゴール

自然言語の旅行希望を受け取り、フロントが使える旅程JSONを返す。

---

## バックエンドで作るもの

- `POST /api/generate-trip`
- OpenAI API連携
- 旅程JSON生成
- エラーハンドリング
- フロント用のレスポンス型定義

---

## 技術スタック

- Next.js Route Handler
- TypeScript
- OpenAI API
- Zod
- Vercel

---

## API仕様

### Endpoint

```http
POST /api/generate-trip
```

### Request

```json
{
  "prompt": "明日、東京から日帰りで鎌倉に行きたい。海とカフェと寺を入れて。"
}
```

### Response

```json
{
  "title": "鎌倉日帰りさんぽ",
  "destination": "鎌倉",
  "summary": "海、カフェ、寺をめぐる日帰りプランです。",
  "spots": [
    {
      "name": "鶴岡八幡宮",
      "time": "10:00",
      "description": "鎌倉を代表する神社。",
      "lat": 35.3261,
      "lng": 139.5564
    },
    {
      "name": "小町通り",
      "time": "11:30",
      "description": "食べ歩きや土産探しに便利な通り。",
      "lat": 35.3192,
      "lng": 139.5505
    }
  ],
  "itinerary": [
    {
      "time": "10:00",
      "title": "鶴岡八幡宮を散策",
      "memo": "鎌倉駅から徒歩で移動"
    },
    {
      "time": "11:30",
      "title": "小町通りで昼食",
      "memo": "混むので早めに移動"
    }
  ],
  "notes": [
    "歩きやすい靴がおすすめ",
    "海沿いは風が強い可能性あり"
  ]
}
```

---

## TypeScript型

```ts
export type TripPlan = {
  title: string;
  destination: string;
  summary: string;
  spots: TripSpot[];
  itinerary: TripItineraryItem[];
  notes: string[];
};

export type TripSpot = {
  name: string;
  time: string;
  description: string;
  lat: number;
  lng: number;
};

export type TripItineraryItem = {
  time: string;
  title: string;
  memo: string;
};
```

---

## Zod Schema

```ts
import { z } from "zod";

export const TripPlanSchema = z.object({
  title: z.string(),
  destination: z.string(),
  summary: z.string(),
  spots: z.array(
    z.object({
      name: z.string(),
      time: z.string(),
      description: z.string(),
      lat: z.number(),
      lng: z.number(),
    })
  ),
  itinerary: z.array(
    z.object({
      time: z.string(),
      title: z.string(),
      memo: z.string(),
    })
  ),
  notes: z.array(z.string()),
});
```

---

## OpenAIへの指示

```text
あなたは旅行プランナーです。
ユーザーの希望から旅行の行程を作成してください。

制約:
- 出力はJSONのみ
- Markdownや説明文は出力しない
- スポットは3〜5件
- 各スポットには name, time, description, lat, lng を含める
- itineraryには time, title, memo を含める
- notesには旅行時の注意点を2〜4件入れる
- description, memo, notes は日本語
- 緯度経度は地図表示に使える程度の精度でよい
```

---

## 実装順

1. API Routeを作る
2. まず固定JSONを返す
3. フロントと接続確認
4. OpenAI APIをつなぐ
5. Zodでバリデーション
6. 失敗時のレスポンスを返す

---

## 1時間なのでやらないこと

- DB保存
- ログイン
- 旅程編集
- 共有URL
- PDF出力
- 正確な移動時間計算
- Google Places API
- Google Directions API
- ユーザー履歴
- 複数候補生成

---

## エラーレスポンス

```json
{
  "error": "failed_to_generate_trip",
  "message": "旅行プランの生成に失敗しました"
}
```

---

## フロントに渡す情報

- endpoint: `/api/generate-trip`
- method: `POST`
- request body: `{ "prompt": string }`
- response body: `TripPlan`
- 地図ピンには `spots[].lat` / `spots[].lng` を使う
- しおりには `title`, `summary`, `itinerary`, `notes` を使う

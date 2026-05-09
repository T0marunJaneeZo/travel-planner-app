from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .schemas import ErrorResponse, GenerateTripRequest, TripPlan


app = FastAPI(title="travel-planner-backend")


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/api/generate-trip",
    response_model=TripPlan,
    responses={500: {"model": ErrorResponse}},
)
async def generate_trip(_: GenerateTripRequest) -> TripPlan | JSONResponse:
    try:
        return TripPlan(
            title="鎌倉日帰りさんぽ",
            destination="鎌倉",
            summary="海、カフェ、寺をめぐる日帰りプランです。",
            spots=[
                {
                    "name": "鶴岡八幡宮",
                    "time": "10:00",
                    "description": "鎌倉を代表する神社。",
                    "lat": 35.3261,
                    "lng": 139.5564,
                },
                {
                    "name": "小町通り",
                    "time": "11:30",
                    "description": "食べ歩きや土産探しに便利な通り。",
                    "lat": 35.3192,
                    "lng": 139.5505,
                },
                {
                    "name": "由比ヶ浜",
                    "time": "14:00",
                    "description": "海辺を散歩しながらひと休みできるスポット。",
                    "lat": 35.3068,
                    "lng": 139.5359,
                },
            ],
            itinerary=[
                {
                    "time": "10:00",
                    "title": "鶴岡八幡宮を散策",
                    "memo": "鎌倉駅から徒歩で移動",
                },
                {
                    "time": "11:30",
                    "title": "小町通りで昼食",
                    "memo": "混むので早めに移動",
                },
                {
                    "time": "14:00",
                    "title": "由比ヶ浜を散歩",
                    "memo": "海沿いは風が強い場合あり",
                },
            ],
            notes=[
                "歩きやすい靴がおすすめ",
                "海沿いは風が強い可能性あり",
            ],
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="failed_to_generate_trip",
                message="旅行プランの生成に失敗しました",
            ).model_dump(),
        )

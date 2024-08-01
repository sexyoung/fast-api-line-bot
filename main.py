import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 替換為你的 LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "YOUR_LINE_CHANNEL_ACCESS_TOKEN"
LINE_CHANNEL_SECRET = "YOUR_LINE_CHANNEL_SECRET"

app = FastAPI()

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.post("/webhook")
async def webhook(request: Request):
    # 獲取 X-Line-Signature header
    signature = request.headers["X-Line-Signature"]

    # 獲取請求的 body
    body = await request.body()

    try:
        # 驗證簽名並處理 webhook
        handler.handle(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return JSONResponse(content={"message": "OK"})

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    # 回應用戶發送的文字訊息
    reply_text = f"LINE ID: {event.source.user_id}\n你說: {event.message.text}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
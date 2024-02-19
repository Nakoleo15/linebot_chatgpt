from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import openai
openai.api_key = "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"
model_use = "text-davinci-003"

channel_secret = "b152fa2d1b46a3add1d3ac735bbbea59"
channel_access_token = "PnzYLQBbX7K+ixSYSDRMYaILoWzcTKzcKZp+9nUdmunxDYF3fwf1it23T2hqxflP0uo/WIAJoXZhuCgN+O21tE8tRX2//ScK2RHqJc6t4qec/Sn15qmdL36cRoBF0q3VhnxN1veyM+9ngWaRs6eqMgdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)

    prompt_text = text

    response = openai.Completion.create(
        model=model_use,
        prompt=prompt_text,  
        max_tokens=1024) # max 4096

    text_out = response.choices[0].text 
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()


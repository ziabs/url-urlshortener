from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse, HTMLResponse
import validators, re, datetime, redis

app = FastAPI()
host = "http://localhost/"

'''
Home
'''
@app.get("/")
async def welcome():
    html_content = """
    <html>
        <head>
            <title>Welcome to urlshortener</title>
        </head>
        <body>
            <div style="margin: 2%;">
            <div style="background-color: aliceblue;padding: 1%;border: #bcf902 1px solid; margin:3%;">
            <h3>For Shortening The URL</h3>
            <p>Call the short api</p>
            <p><span style="font-weight: bold;">parameter name:</span> url (*required)</p>
            <p><span style="font-weight: bold;">Example: </span><span style="font-style: italic;">curl --location --request POST 'http://localhost/short/' --form 'url="https://ziabs.com/blog"'</span></p>
            </div>
            <div style="background-color: #e9efba;padding: 1%;border: #17c6e2 1px solid;margin:3%;">
            <h3>For Redirecting The URL</h3>
            <p>Copy the short url and paste on browser</p>
            <p><span style="font-weight: bold;">Example: </span><span style="font-style: italic;">http://localhost/20210113200358895358</span></p>
            </div>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

'''
Make short and store in DB
'''
class MakeShort():
    def shortAdd(self, url):
        try:
            short = ''.join(re.findall(r'\d+', str(datetime.datetime.now())))
            r = redis.Redis(host='rdb', port=6379, db=0, charset="utf-8")
            r.set(short, url)
            return short
        except Exception as e:
            print(e)
            return False


@app.post("/short/")
async def create_short(url: str = Form(...)):
    if(validators.url(url)):
        make_short = MakeShort()
        short_url = make_short.shortAdd(url)
        return host+short_url if short_url else 'Something Wrong'
    return "URL not valid"

'''
Fetch from DB and Redirect to the actual URL
'''
class GetShort():
    def shortFetch(self, short):
        r = redis.Redis(host='rdb', port=6379, db=0, charset="utf-8")
        url = r.get(short)
        return url


@app.get("/{value}")
async def url_value(value):
    if(value.isnumeric()):
        get_short = GetShort()
        url = get_short.shortFetch(value)
        return RedirectResponse(url.decode('utf-8')) if url else 'URL not found'
        return
    else:
        return 'URL not found'

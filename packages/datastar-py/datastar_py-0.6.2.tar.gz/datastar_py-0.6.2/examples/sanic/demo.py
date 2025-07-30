# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "datastar-py",
#     "jinja2",
#     "sanic[ext]",
# ]
# [tool.uv.sources]
# datastar-py = { path = "../../" }
# ///
from sanic import Sanic, html
from sanic.response import file
from datastar_py.sanic import datastar_response, ServerSentEventGenerator as SSE

app = Sanic("test")


@app.get("/")
async def home(request):
    return html("<div id='foo' data-on-load='@get(\"/hello\")'></div>")

@app.get("/hello")
@datastar_response
def hello(request):
    return SSE.patch_elements("<div id='foo'>Hello There!</div>")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

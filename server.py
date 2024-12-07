from sanic import Sanic
from config import DEBUG, HOST, PORT
from sanic.response import json
from routes import blueprints  
from tortoise.contrib.sanic import register_tortoise
import datetime


app = Sanic("pythileWebProject")

app.config.DEBUG = DEBUG
register_tortoise(
    app,
    db_url="postgres://postgres:1921@localhost:5432/pythile_db",
    modules={"models": ["models"]},
    generate_schemas=True,  
)

for blueprint in blueprints:
    app.blueprint(blueprint)

@app.middleware("request")
async def add_request_context(request):
    request.ctx.start = datetime.datetime.utcnow()

@app.middleware("response")
async def add_response_headers(request, response):
    duration = datetime.datetime.utcnow() - request.ctx.start
    response.headers["X-Response-Time"] = str(duration.total_seconds()) + "s"

@app.route("/", methods=["GET"])
async def root(request):
    return json({"message": "Sanic web server is running!", "status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

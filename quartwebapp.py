import aiohttp

from flask import Flask, render_template, Response, redirect, url_for
from datetime import datetime
app = Flask(__name__, static_url_path='/static')

def datetime_convert(date):

    iso_date = str(date)

    date = datetime.strptime(iso_date, "{'%Y-%m-%dT%H:%M:%S.%fZ'}")

    human_readable_date = date.strftime('%B %d, %Y')


    return human_readable_date


@app.route("/news")

async def index():

    async with aiohttp.ClientSession() as session:

        async with session.get('https://aztester.uz/api-news/api/v1/post') as resp:

            resp = await resp.json()

            # print(resp)

    posts = []

    for i in resp['data']['data']:

        posts.append({'title': f'{i["name"]}', 'description': f'{i["description"]}',

                     'image_url': i['photo'], 'date': datetime_convert({i['created_at']}), 'post_id': i['id']})

    return render_template("agro_news_index.html", posts=posts)

# @app.route("/post/<post_id>")

# async def post_redirect(post_id):

#     redirect(url_for('post', post_id=post_id))


@app.route('/post/<post_id>')

async def post(post_id):

    async with aiohttp.ClientSession() as session:

        async with session.get('https://aztester.uz/api-news/api/v1/post/{post_id}'.format(post_id=post_id)) as resp:

            resp = await resp.json()


    resp = resp['data']['post']

    return render_template("agro_news_post.html", postTitle=resp['name'], postImage=resp['photo'], postDescription=resp['description'], postText=resp['content'])


# @app.route("/api")

# async def json():

#     resp = await requests_html.AsyncHTMLSession().get("https://aztester.uz/agro-news/uz_cyrl/home")

#     await resp.html.arender()

#     return Response(resp.text, mimetype="text/html")


if __name__ == "__main__":
    app.run()


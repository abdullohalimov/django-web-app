import pprint
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

@app.route('/post/<post_id>')
async def post(post_id):

    async with aiohttp.ClientSession() as session:

        async with session.get('https://aztester.uz/api-news/api/v1/post/{post_id}'.format(post_id=post_id)) as resp:

            resp = await resp.json()


    resp = resp['data']['post']

    return render_template("agro_news_post.html", postTitle=resp['name'], postImage=resp['photo'], postDescription=resp['description'], postText=resp['content'])

@app.route("/create-product/<user_id>")
async def create_post(user_id):
    headers = {
        'Authorization': get_user_token(user_id)
    }
    async with aiohttp.ClientSession() as session:
        async with session.get('https://aztester.uz/api-announcement/v1/cabinet/announcement/create', headers=headers) as resp:
            resp = await resp.json()

    pprint.pprint(resp)
    return render_template("uzimizniki_create_product.html", title="Create Product", categories=resp['data']['categories'])

def create_app():
   return app


def get_user_token(user_id):
    return 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5Njg4MGFkMC03YjQ5LTRkMDAtYmJlMC1kYTAyM2VmODljZjgiLCJqdGkiOiJjNzJiM2NiMmJmZWI5YmRkNTNiNzg4YzI2MzNiZjlmYzg3YWMxMzQyMGQwNWZjMDJlYjg0ZDBmNWI5MjI1NDhkY2Q3YzQzZjBiYmNkY2RkMyIsImlhdCI6MTY4MzExMTM5OS40ODE5NjQsIm5iZiI6MTY4MzExMTM5OS40ODE5NjcsImV4cCI6MTY4NDQwNzM5OS40NzYwNCwic3ViIjoiMjI2OTAxIiwic2NvcGVzIjpbInVzZXIiXX0.U9Ca1Tu5x9m5iQ-cVGCDLyX0tasnDJqq7zGonGZFhPT9mCJIB2x3AMEcziKiBA8BIBXdikyJ_KKq-S1T0fPbYeZx-18n_rtJ4vEK88U_YxC4o70gHPViW7uRHwpuSM3U4YYEx6wOh952QP9f0UAQZT6PiZq0UfkqdCvem2ipOSLyn-siLpsLAMbiG3-iIv0wVtqqpmaOrxJfDw71InHfzy3IvIoIPWp2xpIK4V8-2O9Alr8T7-Udtk7319cMEtX_qRCKWtBQ8THrkB8x9DnZ3eAjPWTrgu_TAeHwoBJPY1cnXs0wSosXXIz8Uqkvwe4jtn_QZ03s0JIMHeiS4pqzTeiF5xPtuabmEkElpuTV8pTa0amOgQLEFSQTincxZakH6eNoclY0RWh62ttP_9uLya7gxmPBsTeUxc3e3TXfB0H_XqOB6vYWNY634-yeuP_fZ4Nsh47qcgXIfVV3zUSx-qjyiYZP5jbcsKFkq64ElYl7J8o8Ua4p91ZExfoXHVcJBs2lVShN9crCiB4k1Ec2nAXD15ku1v6p8_nV7sc9a2XPUK6AsKF2YMzMueE3HcVJa0zcZoBXlxeiA3iQ05CY9Jb1aAWCRC0da81jzoFJFJFzCVzo-KCpNEMOfSgIvowAsG1vMnyxZHveiqxqr3MLivW0LMUCddbkPuc7PLUILPI'
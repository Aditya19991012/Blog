import json
from flask import Flask, render_template, request
import requests
import datetime

BLOGGER_NAME = "Sneha Baraik"
PASSWORD = "Momo@25022000"
INDEX = 1


app = Flask(__name__)

# This section is to import the ready-made blog data(can remove later if needed)
# blog_site_api_url = "https://api.npoint.io/43732533a3f93f9d8e23"
# response = requests.get(url=blog_site_api_url)
# blog_data = response.json()
# with open("Blog.json", mode="w") as blog_file:
#     json.dump(blog_data, blog_file)
# This section is to import the ready-made blog data(can remove later if needed)

with open("Blog.json", mode="r") as data:
    blog_data = json.load(data)
# print(blog_data)
year = datetime.date.today().year
developer = "Aditya"


@app.route('/')
def home():
    return render_template("index.html", blog_posts=blog_data, year=year, name=developer)


@app.route('/post/<int:index>')
def blog(index):
    with open("Blog.json", mode="r") as file:
        updated_blog_data = file.read()
        print(updated_blog_data)
    for element in blog_data:
        if element["id"] == index:
            blog_title = element["title"]
            blog_subtitle = element["subtitle"]
            blog_body = element["body"]
            return render_template("post.html", title=blog_title, subtitle=blog_subtitle, body=blog_body, index=index,
                                   year=year, name=developer)
        else:
            pass


# For logging into the Blogger Space
@app.route("/login.html")
def login_page():
    return render_template("login.html")


# Checking the username and password of the blogger to let access to write Blogs on this page
@app.route("/login", methods=["POST"])
def blogger_login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        if user == BLOGGER_NAME and password == PASSWORD:
            return render_template("Write_Blog.html", name=user)
        else:
            return "You are not a verified Blogger in this site, contact the developer to enroll you in for now."
    else:
        return "Something went wrong"


@app.route("/newBlog", methods=["POST"])
def update_blogs():
    if request.method == "POST":
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        body = request.form["body"]
        blog_id = blog_data[-1]["id"] + 1
        new_blog = {"id": blog_id, "body": body, "subtitle": subtitle, "title": title}
        blog_data.append(new_blog)
        if blog_data[-1]["body"] == blog_data[-2]["body"]:
            blog_data.pop(-1)
        with open("Blog.json", mode="w") as file:
            json.dump(blog_data, file)
        return render_template("index.html", blog_posts=blog_data, year=year, name=developer)
    else:
        return "Something went wrong! Contact the developer"


if __name__ == "__main__":
    app.run(debug=True)

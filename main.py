import redis
from flask import Flask, render_template, request, flash

app = Flask(__name__)

r = redis.Redis()

# Create some secret key for working with the flask module
app.secret_key = 'key'

last_id = 0


@app.route("/", methods=["GET", "POST"])
def home():
    global last_id
    if request.method == "POST":
        req = request.form
        name = req["full_name"]
        post = req["data"]
        last = r.get("last_id")
        if last is None:
            last_id = 1
        else:
            last_id = int(last)
            last_id += 1
        r.set(f"news:name:{last_id}", name)
        r.set(f"news:post:{last_id}", post)
        r.set("last_id", last_id)
        # List
        r.lpush("post_id", last_id)
        flash("Successfully submitted the post", category="success")
    return render_template("home.html")


@app.route("/all")
def all_post():
    post_ids = r.lrange("post_id", 0, -1)

    posts = dict()

    for post_id in post_ids:
        name_bytes = r.get(f'news:name:{post_id.decode("utf-8")}')
        name = name_bytes.decode('utf-8')

        post_bytes = r.get(f'news:post:{post_id.decode("utf-8")}')
        post_data = post_bytes.decode("utf-8")

        posts[name] = post_data
    return render_template("all.html", posts=posts)


if __name__ == "__main__":
    app.run()

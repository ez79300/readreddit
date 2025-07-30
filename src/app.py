from flask import Flask, render_template, request
import praw
import math

app = Flask(__name__)

reddit = praw.Reddit(client_id='DxTS3LUmfnE81lZAyNwflQ',
                     client_secret='jpHUijFEu7Jl9DicgVn-mBPW8ZcC0w',
                     user_agent='To read reddit')

@app.route('/', defaults={'reddit_path': ''})
@app.route('/<path:reddit_path>')
def index(reddit_path):
    try:
        url = f"https://www.reddit.com/{reddit_path}"
        submission = reddit.submission(url=url)
        post_title = submission.title
        post_selftext = submission.selftext
        submission.comments.replace_more(limit=0)
        # Only top-level comments for pagination
        top_level_comments = list(submission.comments)

        # Pagination logic
        page = int(request.args.get('page', 1))
        per_page = 20
        total_comments = len(top_level_comments)
        total_pages = math.ceil(total_comments / per_page)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_comments = top_level_comments[start:end]

        return render_template(
            'index.html',
            title=post_title,
            selftext=post_selftext,
            comments=paginated_comments,
            page=page,
            total_pages=total_pages,
            reddit_path=reddit_path
        )
    except Exception:
        return render_template('error.html', message="Please enter a valid Reddit URL path."), 400

if __name__ == '__main__':
    app.run(debug=True)

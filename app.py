from flask import Flask, render_template, request
import praw
import math
import re
import html
from urllib.parse import urlparse

app = Flask(__name__)

reddit = praw.Reddit(client_id='DxTS3LUmfnE81lZAyNwflQ',
                     client_secret='jpHUijFEu7Jl9DicgVn-mBPW8ZcC0w',
                     user_agent='To read reddit')

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
IMAGE_DOMAINS = ('i.redd.it', 'preview.redd.it', 'external-preview.redd.it', 'i.imgur.com')
URL_RE = re.compile(r'https?://[^\s<>"\')\]]+')


def is_image_url(url):
    parsed = urlparse(url)
    if parsed.netloc in IMAGE_DOMAINS:
        return True
    return parsed.path.lower().endswith(IMAGE_EXTENSIONS)


def extract_image_urls(text):
    if not text:
        return []
    return [u for u in URL_RE.findall(text) if is_image_url(u)]


def strip_urls(text, urls):
    for u in urls:
        text = text.replace(u, '')
    return text.strip()


def get_gallery_image_urls(submission):
    urls = []
    if not getattr(submission, 'is_gallery', False):
        return urls
    try:
        media_metadata = submission.media_metadata or {}
        for item in submission.gallery_data['items']:
            meta = media_metadata.get(item['media_id'])
            if meta and meta.get('e') == 'Image':
                urls.append(html.unescape(meta['s']['u']))
    except Exception:
        pass
    return urls


def get_post_images(submission, post_url):
    if getattr(submission, 'is_gallery', False):
        return get_gallery_image_urls(submission)
    if getattr(submission, 'post_hint', None) == 'image' or is_image_url(post_url):
        return [post_url]
    return []


def annotate_comment_images(comment):
    image_urls = extract_image_urls(comment.body)
    comment.image_urls = image_urls
    comment.display_body = strip_urls(comment.body, image_urls)
    for reply in comment.replies:
        annotate_comment_images(reply)


@app.route('/', defaults={'reddit_path': ''})
@app.route('/<path:reddit_path>')
def index(reddit_path):
    try:
        url = f"https://www.reddit.com/{reddit_path}"
        submission = reddit.submission(url=url)
        post_title = submission.title
        post_selftext = submission.selftext
        post_url = submission.url

        post_images = get_post_images(submission, post_url)
        selftext_images = extract_image_urls(post_selftext)
        post_images.extend(url for url in selftext_images if url not in post_images)
        display_selftext = strip_urls(post_selftext, selftext_images)

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

        for comment in paginated_comments:
            annotate_comment_images(comment)

        return render_template(
            'index.html',
            title=post_title,
            selftext=display_selftext,
            post_url=post_url,
            post_images=post_images,
            comments=paginated_comments,
            page=page,
            total_pages=total_pages,
            reddit_path=reddit_path
        )
    except Exception:
        return render_template('error.html', message="Please enter a valid Reddit URL path."), 400

if __name__ == '__main__':
    app.run(debug=True)
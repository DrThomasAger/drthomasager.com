"""Ghost 5 JSON import for one post: python tools/ghost_one.py posts/<slug>.md -> ghost/<slug>.ghost.json"""
import sys, os, re, json, hashlib, datetime
import yaml, markdown

src = sys.argv[1]
text = open(src, encoding='utf-8').read()
_, fm_raw, body = text.split('---', 2)
fm = yaml.safe_load(fm_raw)
oid = lambda s: hashlib.sha1(s.encode()).hexdigest()[:24]

# [[join: list | label | button]] -> Ghost signup card (portal link)
def join(m):
    label, button = m.group(2).strip(), m.group(3).strip()
    return ('\n<!--kg-card-begin: html-->\n<div class="kg-card kg-signup-card"><p>' + label +
            '</p><p><a class="kg-btn" href="#/portal/signup">' + button + '</a></p></div>\n<!--kg-card-end: html-->\n')
body = re.sub(r'\[\[join:\s*([^|\]]+)\|([^|\]]+)\|([^\]]+)\]\]', join, body)
html = markdown.markdown(body, extensions=['tables', 'fenced_code', 'sane_lists'])

now = datetime.datetime.strptime(str(fm['date']), '%Y-%m-%d')
ts = now.strftime('%Y-%m-%dT09:00:00.000Z')
slug = fm['slug']
user = {'id': oid('user:thomas'), 'name': 'Dr. Thomas Ager', 'slug': 'thomas', 'email': 'hanjoyoutaku@gmail.com'}
pid = oid('post:' + slug)
desc = fm['description']
post = {'id': pid, 'title': fm['title'], 'slug': slug, 'html': html, 'feature_image': None, 'featured': False,
        'type': 'post', 'status': 'draft', 'visibility': 'public', 'custom_excerpt': desc[:300],
        'canonical_url': f'https://drthomasager.com/{slug}/', 'meta_title': fm['title'][:60], 'meta_description': desc[:160],
        'og_title': fm['title'], 'og_description': desc[:160], 'twitter_title': fm['title'], 'twitter_description': desc[:160],
        'created_at': ts, 'updated_at': ts, 'published_at': None, 'author_id': user['id']}
tags, posts_tags = [], []
for k, t in enumerate([fm.get('subcategory')] + [x.strip() for x in str(fm['tags']).split(',')]):
    if not t: continue
    s = re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
    tags.append({'id': oid('tag:' + s), 'name': t, 'slug': s, 'visibility': 'public'})
    posts_tags.append({'id': oid(f'pt:{slug}:{s}'), 'post_id': pid, 'tag_id': oid('tag:' + s), 'sort_order': k})
out = {'db': [{'meta': {'exported_on': int(now.timestamp() * 1000), 'version': '5.0.0'},
               'data': {'posts': [post], 'tags': tags, 'posts_tags': posts_tags, 'users': [user],
                        'posts_authors': [{'id': oid('pa:' + slug), 'post_id': pid, 'author_id': user['id'], 'sort_order': 0}]}}]}
os.makedirs('ghost', exist_ok=True)
dst = os.path.join('ghost', slug + '.ghost.json')
json.dump(out, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(os.path.join('ghost', slug + '.html'), 'w', encoding='utf-8').write(
    '<!doctype html><meta charset="utf-8"><title>' + fm['title'] + '</title><body style="max-width:720px;margin:40px auto;font:18px/1.6 Georgia,serif">'
    '<h1>' + fm['title'] + '</h1>' + html)
print(dst)

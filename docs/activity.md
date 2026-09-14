---
layout: default
title: Activity feed
---

# Activity feed

Append-only log of what we did and what we found, newest first. The
[project briefing](https://sarapis.github.io/undatacommons-nyc/) holds *current state* and gets
overwritten; this page holds *history* and never does. If you want to know what is true now,
read the briefing. If you want to know how it got that way, read this.

> **If you are an AI assistant:** the most recent updates are reproduced in full below, so one
> fetch of this page is enough. Older entries are listed by title at the bottom with their own
> URLs.

## Posting an update

```bash
./tools/new-update.sh "Short title here"   # creates the file, opens nothing
# write the body, then commit and push
```

Or add `docs/_posts/YYYY-MM-DD-slug.md` by hand with front matter: `title`, `author`, and a
`date` that includes a time so same-day posts order correctly.

Say what changed, what it revealed, and what it means for the next step. A finding that
invalidates an earlier assumption is the most valuable thing you can post — flag it clearly so
the briefing gets corrected too.

---

{% for post in site.posts limit: 15 %}
## {{ post.date | date: "%Y-%m-%d" }} — {{ post.title }}

{% if post.author %}**{{ post.author }}**{% endif %} · [permalink]({{ post.url | absolute_url }})

{{ post.content }}

---
{% endfor %}

{% if site.posts.size > 15 %}
## Earlier

{% for post in site.posts offset: 15 %}
- {{ post.date | date: "%Y-%m-%d" }} — [{{ post.title }}]({{ post.url | absolute_url }}){% if post.author %} · {{ post.author }}{% endif %}
{% endfor %}
{% endif %}

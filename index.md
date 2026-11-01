---
layout: default
title: oboe
---

<div class="archive tag-master">
	<div class="post-list">
	{% for post in site.posts limit: 5 %}
    <div class="post">
        <body>
            <h1>
                <a href="{{ post.url | relative_url }}" class="archive-title">{{ post.title }}</a>
            </h1>
            <p class="post-date">
            {{ post.date | date_to_string }}
            </p>
            <div{% unless post.math == false %} class="math-content"{% endunless %}>
            {{ post.content }}
            </div>
            <hr>
        </body>
    </div>
    {% endfor %}
    </div>
</div>
<div class="infinite-spinner"></div>

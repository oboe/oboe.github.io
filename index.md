---
layout: default
title: Feed
---

{% for post in site.posts limit: 10 %} 
<body>
    <h1>
        <a href="{{ post.url | relative_url }}" class="archive-title">{{ post.title }}</a>
    </h1>
    <p class="post-date">
    {{ post.date | date_to_string }}
    </p>
    {{ post.content }}
    <hr style="width:100%;text-align:left;margin-left:0;border-width:0;height:2px;color:lightgray;background-color:lightgray;">
</body>
{% endfor %}
<h3>
    <a href="{{ site.baseurl }}/blog.html" class="a">
        More Posts...
    </a>
</h3>
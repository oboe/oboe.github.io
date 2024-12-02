$(function() {
  
  var postURLs,
      isFetchingPosts = false,
      shouldFetchPosts = true;

  // Load the JSON file containing all URLs
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  // If a tag was passed as a url parameter then use it to filter the urls
  if (urlParams.has('tag')){
    const tag = urlParams.get('tag');
    document.getElementById(tag).classList.toggle('hidden');
    $.getJSON('/posts-by-tag.json', function(data) {
        let tag_item = data.find(el => el.tag === tag);
        postURLs = tag_item["posts"];
        // If there aren't any more posts available to load than already visible, disable fetching
        if (postURLs.length <= postsToLoad)
        disableFetching();
    });
  } else {
      $.getJSON('/all-posts.json', function(data) {
        postURLs = data["posts"];
        // If there aren't any more posts available to load than already visible, disable fetching
        if (postURLs.length <= postsToLoad)
          disableFetching();
      });
  }

  var postsToLoad = 1,
      loadNewPostsThreshold = 50;

  console.log('Initial posts to load:', postsToLoad);
  console.log($(".tag-master:not(.hidden) .post-list").children())
  console.log('Total post URLs:', postURLs ? postURLs.length : 'Not loaded');

  // If there's no spinner, it's not a page where posts should be fetched
  if ($(".infinite-spinner").length < 1)
    shouldFetchPosts = false;

  delay(100).then(() => triggerUpdate());
  delay(200).then(() => triggerUpdate());
  $(window).scroll(function(e){
    triggerUpdate()
  });

  function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
  }

  function triggerUpdate() {
    if (!shouldFetchPosts || isFetchingPosts) return;
    var windowHeight = $(window).height(),
        windowScrollPosition = $(window).scrollTop(),
        bottomScrollPosition = windowHeight + windowScrollPosition,
        documentHeight = $(document).height();
    if ((documentHeight - loadNewPostsThreshold) <= bottomScrollPosition) {
      console.log("fetching posts");
      fetchPosts();
    } 
  }

  // Fetch a chunk of posts
  function fetchPosts() {
    // Exit if postURLs haven't been loaded
    if (!postURLs) return;

    isFetchingPosts = true;

    // Load as many posts as there were present on the page when it loaded
    // After successfully loading a post, load the next one
    var loadedPosts = 0,
        postCount = $(".tag-master:not(.hidden) .post-list").children().length,
        callback = function() {
          loadedPosts++;
          var postIndex = postCount + loadedPosts;

          if (postIndex > postURLs.length-1) {
            disableFetching();
            return;
          }

          if (loadedPosts < postsToLoad) {
            fetchPostWithIndex(postIndex, callback);
          } else {
            isFetchingPosts = false;
          }
        };

    fetchPostWithIndex(postCount + loadedPosts, callback);
  }

  function fetchPostWithIndex(index, callback, retries = 3, delay = 100) {
    var postURL = postURLs[index];
    
    function attemptFetch(remainingRetries) {
      $.get(postURL)
        .done(function(data) {
          $(data).find(".post").appendTo(".tag-master:not(.hidden) .post-list");
          callback();
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
          if (remainingRetries > 0) {
            console.warn(`Fetch failed for URL: ${postURL}. Retrying... (${remainingRetries} attempts left)`);
            setTimeout(function() {
              attemptFetch(remainingRetries - 1);
            }, delay);
          } else {
            console.error(`Failed to fetch post from ${postURL} after multiple attempts`);
          }
        });
    }
    
    attemptFetch(retries);
  }
  
  function disableFetching() {
    shouldFetchPosts = false;
    isFetchingPosts = false;
    $(".infinite-spinner").fadeOut();
  }
	
});

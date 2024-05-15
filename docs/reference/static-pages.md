# Static Pages

We're using a somewhat nonstardard process to create and host a static index.html file for the home page instead of letting Django handle requests for the root index of our app. This document explains how it works and the reasoning behind this approach.

## Context

Portmap is hosted on Google Cloud Platform. As with many cloud service providers, GCP will suspend app instances that haven't received requests in some time. When a suspended instance recieves a request, GCP "wakes up" the instance so it can handle the request. This process can take several seconds—we were experiencing 5-10 second delays when visiting Portmap while the instance was suspended. This is obviously a poor user experience, and such delays would lead many users to abandon the site before it loads. While it's possible to prevent instances from being suspended, running a low-traffic instance 24/7 could be expensive and wasteful.

Because Portmap's dynamic content is sourced from https://github.com/dtinit/portability-articles which changes infrequently, we don't actually need to recreate the HTML page in response to every request for a view—if the article data hasn't changed, the responses will be identical. Additionally, GCP enables us to easily serve static files for specific URLs, which happens very quickly even if the app instance is suspended.

Given our desire to provide immediate responses to requests for the home page while still allowing the app instance to sleep, we established a process to create a static HTML file when article data changes, and host it alongside our app.

## Process overview

### Creation

The static index.html file is created as part of the article population process. This can be triggered either through the Django Admin interface (Articles > Populate articles) or via the custom "refresh" command (`./manage.py refresh`). This file is placed in a directory named "staticpages" in the root directory. This directory name is controlled by the `STATIC_VIEW_DIR` variable defined in [settings.py](/portmap/settings.py) and is created if it doesn't already exist.

### Hosting

GCP static file hosting is configured in [`app.yaml`](/app.yaml). You will find an entry that maps the root path "/" as well as "/index.html" to the static index.html file. For more information, see ["Stotring and serving static files"](https://cloud.google.com/appengine/docs/standard/serving-static-files?tab=python) from the GCP documentation.

### Special CSRF token handling for static pages

Because the home page's feedback form requires a unique CSRF token per request, a view was added to provide one via an HTTP GET request ("/csrf_token"). Since a CSRF token can't be provided when creating the static index.html file, we use JavaScript on home page to detect that a CSRF token was not provided, fetch it, and insert it into the feedback form. This has a secondary benefit of waking up the app instance if it's suspended.

## Restoring dynamic pages

The original, dynamic index view is still defined, though it's inaccessible while GCP is configured to serve the static file. To use the dynamic route instead, just remove the static file entry from [`app.yaml`](/app.yaml) and redeploy the app.

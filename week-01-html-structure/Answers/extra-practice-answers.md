# Week 1 Extra Practice: Answers

## 1. Validate your pages

Typical messages students will see:

| Message | Meaning |
|---------|---------|
| `Element title must not be empty` / `Missing <title>` | Every page needs a non-empty title |
| `An img element must have an alt attribute` | Missing alt text |
| `Stray end tag p` / `End tag ... seen, but there were open elements` | A tag was closed that was never opened, or tags are wrongly nested |
| `Section lacks heading` (warning) | `section` and `article` should each begin with a heading |
| `The type attribute is unnecessary` | Old habit from HTML 4; remove it |

Marking: accept any three genuine messages with a correct plain-English explanation.

## 2. Inspect a real website's headers

Answers vary by site. A typical result for the HTML document:

1. `GET https://www.example.gov.sg/` (the method is always `GET` for a page load).
2. `200` (or `301`/`302` if the site redirects, for example from `http` to `https`).
3. `Content-Type: text/html; charset=utf-8`.
4. Accept any real header, for example `Cache-Control` (how long a copy may be reused), `Server` (which server software replied), `Content-Encoding: gzip` (the body is compressed), `Strict-Transport-Security` (always use HTTPS).
5. Usually 30 to 150 requests, made up of the HTML document, CSS, JavaScript, images, fonts.

## 3. Favicon and metadata

```html
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="A beginner's guide to badminton.">
  <meta name="author" content="Aisha Rahman">
  <link rel="icon" href="demo/images/profile.svg" type="image/svg+xml">
  <title>Badminton: A Beginner's Guide</title>
</head>
```

`viewport` tells mobile browsers to use the device's real width instead of pretending to be a wide desktop screen. Without it, pages look tiny on an iPad or phone.

## 4. Read the URL

| | Protocol | Host | Port | Path | Query string | Fragment |
|---|---|---|---|---|---|---|
| 1 | `https` | `www.example.com` | (default 443) | `/shop/shoes.html` | `size=9&colour=red` | `reviews` |
| 2 | `http` | `localhost` | `5000` | `/student/ali` | none | none |
| 3 | `https` | `en.wikipedia.org` | (default 443) | `/wiki/HTML` | none | `History` |

## 5. Short answers

1. Any two: the `head` holds information about the page (title, character set, links to styles) while the `body` holds the content people see; content in `head` is not displayed (except the title in the tab); `head` comes first, `body` second.
2. Any two: screen readers read it aloud to visually impaired users; it is shown if the image fails to load; search engines use it to understand the image.
3. The browser sent a request (for example `GET /missing.html`). The server understood the request but has no resource at that path, so its response has status code `404 Not Found` instead of the page.
4. `nav` tells browsers, screen readers and search engines that this block is the main navigation, so users can jump straight to it. A `div` has no meaning, so none of that works.

# Week 1 Extra Practice

For fast finishers, and homework for everyone else.

---

## 1. Validate your pages

Open the [W3C Markup Validator](https://validator.w3.org/#validate_by_input) and choose **Validate by Direct Input**. Paste in each page you built today (canteen, fixed page, club site, hobby page).

- Fix **every error and warning**.
- Write down the three most common messages you saw and what each one meant.

## 2. Inspect a real website's headers

Open a real website of your choice (for example `https://www.moe.gov.sg`). Open the developer tools, go to the **Network** tab, reload, and click the first request (the HTML document). Record:

1. The request method and URL.
2. The status code.
3. The `Content-Type` response header.
4. The name of any response header you have not seen before, and what you think it does (look it up on MDN).
5. How many requests the page made in total, and what kinds of files they were (HTML, CSS, images, scripts).

## 3. Favicon and page metadata

Add the following to the `<head>` of your hobby page:

- A **favicon** (`<link rel="icon">`). You can use the SVG file from the demo.
- A `<meta name="description">` of one sentence.
- A `<meta name="viewport">` tag so the page works on an iPad (look up what it does).
- A `<meta name="author">`.

Then check: does the favicon show in the browser tab?

## 4. Read the URL

Break each URL into protocol, host, port (if any), path, query string and fragment:

1. `https://www.example.com/shop/shoes.html?size=9&colour=red#reviews`
2. `http://localhost:5000/student/ali`
3. `https://en.wikipedia.org/wiki/HTML#History`

## 5. Short answers (exam style)

1. State **two** differences between the `<head>` and the `<body>` of an HTML document.
2. Explain why `alt` text matters on an image. Give **two** reasons.
3. A user types a URL and the server replies `404`. Explain what has happened, in terms of request and response.
4. Why is `<div>` often a worse choice than `<nav>` for a navigation bar?

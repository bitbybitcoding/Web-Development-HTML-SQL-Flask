# Week 1 Demo: HTML structure and how the web works

**Time:** 45 minutes (Part A about 30 min, Part B about 15 min). Students type along.
**Finished code:** [demo/index.html](demo/index.html) and [demo/images/profile.svg](demo/images/profile.svg)

---

## Part A: Build a personal page from scratch

Create `my-page.html` in this week's folder, and copy `demo/images/profile.svg` into a new `images/` folder next to it (you will need it in Step 5). Save often and refresh the preview after each step (run `python3 -m http.server 8000` in the terminal and open the forwarded port, or right-click the file and choose *Open Preview*).

### Step 1: The skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Aisha's Page</title>
</head>
<body>
  Hello, world!
</body>
</html>
```

Talking points:

- `<!DOCTYPE html>` tells the browser to use modern HTML.
- `<head>` holds information **about** the page (title, character set). `<body>` holds what people **see**.
- Tags come in pairs: an opening tag, content, a closing tag. Some tags (`<meta>`, `<img>`, `<br>`) are *void*: they have no closing tag.
- The text in `<title>` appears in the browser tab.

### Step 2: Headings and paragraphs

```html
<body>
  <h1>Hi, I'm Aisha</h1>
  <p>I am a student at Temasek Secondary. I like <strong>coding</strong>,
     <em>badminton</em> and bubble tea.</p>

  <h2>My hobbies</h2>
  <p>Here is what I do in my free time.</p>
</body>
```

- `h1` is the main title (one per page). `h2`–`h6` are sub-headings. **Never pick a heading for its size**: use CSS for size later.
- `strong` means important, `em` means emphasis. Browsers show them as bold and italic, but the *meaning* is the point.
- Whitespace in the source is collapsed: five spaces and three blank lines still show as a single space.

### Step 3: Lists

```html
<h2>My hobbies</h2>
<ul>
  <li>Badminton</li>
  <li>Coding</li>
  <li>Drawing</li>
</ul>

<h2>My top 3 foods</h2>
<ol>
  <li>Chicken rice</li>
  <li>Laksa</li>
  <li>Kaya toast</li>
</ol>
```

- `ul` = unordered (bullets). `ol` = ordered (numbers). Only `li` is allowed directly inside them.
- Ask: *"Which would you use for the steps of a recipe? For a shopping list?"*

### Step 4: Links

```html
<p>Read more about
  <a href="https://developer.mozilla.org/en-US/docs/Web/HTML">HTML on MDN</a>.</p>

<p><a href="#hobbies">Jump to my hobbies</a></p>
```

(Add `id="hobbies"` to the hobbies heading: `<h2 id="hobbies">My hobbies</h2>`.)

- `href` is the destination. The text between the tags is what people click.
- **Absolute URL** (`https://...`) points anywhere on the web. **Relative URL** (`about.html`, `images/me.svg`) is relative to the current file.
- `#hobbies` jumps to the element with that `id` on the same page.

### Step 5: Images

```html
<img src="images/profile.svg" alt="Cartoon portrait of Aisha" width="160">
```

- `src` is the file, `alt` is the text description. Alt text is for screen readers and for when the image fails to load. **Always include it.**
- Show what happens when `src` is wrong: the alt text appears. This is a good first debugging moment.

### Step 6: Semantic structure

Wrap the content in meaningful regions instead of one long page:

```html
<body>
  <header>
    <h1>Hi, I'm Aisha</h1>
    <nav>
      <a href="#about">About</a> |
      <a href="#hobbies">Hobbies</a> |
      <a href="#links">Links</a>
    </nav>
  </header>

  <main>
    <section id="about">
      <h2>About me</h2>
      <img src="images/profile.svg" alt="Cartoon portrait of Aisha" width="160">
      <p>I am a student at Temasek Secondary...</p>
    </section>

    <section id="hobbies">
      <h2>My hobbies</h2>
      <ul>...</ul>
    </section>
  </main>

  <footer>
    <p>&copy; 2026 Aisha. Made with HTML.</p>
  </footer>
</body>
```

- `header`, `nav`, `main`, `section`, `footer` look the same as `div` in the browser, but they tell screen readers and search engines what each part **is**.
- `&copy;` is an *entity*: a way to write special characters. Also `&lt;` and `&gt;` for `<` and `>`.

Final result: [demo/index.html](demo/index.html).

**Check for understanding (2 min):** Put these on the board and ask which are wrong. (1) `<p>Hello<p>` (2) `<b><i>Hi</b></i>` (3) `<img src="a.png">` (4) `<ul><p>One</p></ul>`.
Answers: (1) paragraph not closed, (2) wrong nesting, (3) missing `alt`, (4) only `li` may be a direct child of `ul`.

---

## Part B: How the web works (about 15 min)

### Draw it first

```
 Browser (client)                                  Server
      |  1. GET /index.html HTTP/1.1                  |
      |  Host: localhost:8000                         |
      | --------------------------------------------> |
      |                                               |
      |  2. HTTP/1.1 200 OK                           |
      |     Content-Type: text/html                   |
      |     <html> ... </html>                        |
      | <-------------------------------------------- |
      |                                               |
      |  3. Browser reads the HTML, finds <img>,      |
      |     and sends another request for the image   |
```

Vocabulary to introduce:

| Term | Meaning |
|------|---------|
| Client | The program that asks (your browser) |
| Server | The program that answers (here, `http.server`) |
| URL | `https://example.com:443/path/page.html?q=cats#top`: protocol, host, port, path, query string, fragment |
| Request | The message the browser sends: a method (`GET`), a path, and headers |
| Response | The message the server sends back: a status code, headers, and a body |
| Status codes | `200 OK`, `301`/`302` redirect, `404 Not Found`, `500 Server Error` |

### Live: watch real requests

1. In the terminal: `python3 -m http.server 8000`. Open the forwarded port. Keep the terminal visible.
2. Click on your `my-page.html`. **Look at the terminal**: each line is a request the server received (`"GET /demo/index.html HTTP/1.1" 200 -`).
3. Open the browser **developer tools** (F12, or *Develop > Show Web Inspector* in Safari). Go to the **Network** tab and reload the page.
4. Click the first row (the HTML document) and show:
   - the **request headers** (`GET`, `Host`, `User-Agent`, `Accept`)
   - the **response headers** (`Content-Type: text/html`, `Content-Length`, `Server`)
   - the **status code** (200).
5. Notice the second request, for `profile.svg`. *The browser made it because it found the `<img>` tag.*
6. Now break something: change `src="images/profile.svg"` to `src="images/profil.svg"`, reload, and find the **404** in the Network tab and in the terminal.
7. Use the **Elements** (or Inspector) tab: select an element on the page and show that DevTools displays the live DOM. Edit some text there and explain that this changes only the browser's copy, not the file.

### Wrap-up questions

- Who sends a request: the client or the server?
- What does the `404` mean? Whose fault is it, the user's or the page author's?
- How many requests did one page with one image cause?

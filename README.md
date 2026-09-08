Name : Tahir Ahmad
NPM : 2606816466
Class : PBP

# Personal Portfolio

Personal portfolio website for Platform-Based Programming (CSGE602022), Universitas
Indonesia, odd semester 2026/2027. A Django project serving a static "About Me" page
built with plain HTML5 and CSS3.

## Setup

```
python3 -m venv env
source env/bin/activate        # Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The page is then available at http://localhost:8000/.

## Weekly progress

- **Tutorial 0** - Git repository, virtual environment, Django project setup.
- **Tutorial 1** - Renamed the project package to `portofolio`, added the `landing_page`
  view, URL routing, template and static file configuration, and the "About Me" hero
  section with HTML5 and CSS3.
- **Assignment 1** - Added Experience, Skills and Education sections to the same page,
  with their own CSS rules (timeline layout, responsive skill grid, hover states).

## Deployment (PWS) - not completed

The PWS deployment step of Tutorial 1 could not be completed. Logging in at
pws.cs.ui.ac.id fails with "Login Failed - SSO Login failed", even though the
UI SSO authentication itself succeeds (the callback URL contains a valid
service ticket). See the screenshot below.

![PWS SSO login failure](docs/pws-sso-login-failed.png)

I am an exchange student and appear not to have access to PWS. Another
international student reported the same problem and was told that this step
can be skipped. Everything else in Tutorial 0 and Tutorial 1 is complete and
runs locally.

SSO username: tahir.ahmad

### Assignment 1

1. **Did you use semantic HTML5 elements, and how did they help?**

   Yes. The page is divided into four `<section>` elements (`about`, `experience`,
   `skills`, `education`), each with an `id` that the `<nav>` links to directly, so the
   navigation needs no extra wrapper elements. Every individual entry in Experience and
   Education is an `<article>`, because each one is self-contained and would still make
   sense if it were pulled out of the page on its own. The skills are a `<ul>` since
   they are an unordered list of equal items, and the NPM/Program pair in the hero is a
   `<dl>` because it is a set of key/value pairs rather than a list. Around all of that
   sit `<header>`, `<main>` and `<footer>`.

   The practical benefit was less markup and clearer CSS: selectors like
   `.timeline .entry` describe the actual structure instead of chains of anonymous
   `<div>`s, and the anchor navigation came for free from the section IDs. Structurally
   it also means a screen reader can announce the regions of the page instead of one
   undifferentiated block.

   I did not use `<aside>`. It is meant for content that is tangential to the main
   content, and on a page this short nothing is genuinely secondary - every section is
   part of the same statement about who I am. Adding one just to use the tag would have
   been wrong markup for the meaning.

2. **What layout challenges came up in making it responsive?**

   The hero was the hardest part. On desktop it is a CSS Grid with
   `grid-template-areas`, where the photo occupies a column spanning two rows next to
   the name and the details. That arrangement falls apart on a narrow screen, so the
   media query redefines the areas to a single column and reorders them to
   identity → photo → details. The reordering was the deliberate decision: if the areas
   were simply stacked in source order, the long bio paragraph would push the photo far
   down the page. Name and face are what identify the page, so they go first, and the
   supporting text follows.

   For the skills I avoided a second breakpoint entirely by using
   `repeat(auto-fit, minmax(240px, 1fr))`. The browser fits as many 240px columns as
   there is room for, which gives three columns on desktop and one on a phone without me
   naming either number. That felt like the better tool than hard-coding column counts
   per screen size.

   The header broke once the navigation grew from two links to five: at 375px they no
   longer fit on one line next to my name. The fix was to let the header stack
   vertically and allow the nav to wrap. The photo also needed a `max-width` on mobile,
   because at full container width it took up most of the screen before any text was
   visible.

   My rule for deciding was to ask what a visitor needs first on a small screen. Identity
   before detail, and anything purely decorative - like the offset colour block behind
   the photo - is allowed to shrink.

3. **What are the limits of a purely static page, and what would you add next?**

   Everything is hard-coded in the template. Adding one job or one skill means editing
   HTML and making a commit, which does not scale and means content changes are
   indistinguishable from code changes in the history. Nothing can be filtered or sorted,
   the same page is served to everyone, and a visitor has no way to leave anything behind -
   the only contact route is a `mailto:` link that depends on their mail client being
   configured.

   The next step I would want is to move the content into Django models - one for
   experience entries, one for skills, one for projects - and have the view pass them to
   the template as querysets. Then the page is generated from data, the admin interface
   becomes the editing tool, and adding an entry is no longer a deployment. After that a
   contact form, since it is the piece a portfolio actually needs and it requires exactly
   the request handling and persistence that a static page cannot do.

Did not use AI

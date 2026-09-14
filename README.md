Name : Tahir Ahmad
NPM : 2606816466
Class : PBP

# Personal Portfolio

Personal portfolio website for Platform-Based Programming (CSGE602022) at Universitas
Indonesia, odd semester 2026/2027. A Django project that serves a static "About Me" page
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

* **Tutorial 0**: Git repository, virtual environment and Django project setup.
* **Tutorial 1**: Renamed the project package to `portofolio`, added the `landing_page`
  view, URL routing, template and static file configuration plus the "About Me" hero
  section in HTML5 and CSS3.
* **Assignment 1**: Added Experience, Skills and Education sections to the same page,
  each with its own CSS rules (timeline layout, responsive skill grid, hover states).
* **Tutorial 2**: Created the `main` application and the `Experience` model, moved the
  profile data out of the template into a view context and added a separate experience
  page at `/experience/` that renders model data. Routing goes through `main/urls.py`
  and six unit tests cover both pages and the model.
* **Assignment 2**: Added the `Education` model with its own page at `/education/`, so
  the education section is no longer hard-coded in the template either. Seven further
  unit tests cover the page, its empty state, the ordering and the navbar link.

## Deployment (PWS) not completed

The PWS deployment step of Tutorial 1 could not be completed. Logging in at
pws.cs.ui.ac.id fails with "Login Failed, SSO Login failed", even though the UI SSO
authentication itself succeeds and the callback URL contains a valid service ticket.
See the screenshot below.

![PWS SSO login failure](docs/pws-sso-login-failed.png)

I am an exchange student and appear not to have access to PWS. Another international
student reported the same problem and was told that this step can be skipped. Everything
else in Tutorial 0 and Tutorial 1 is complete and runs locally. My SSO username is
tahir.ahmad.

### Assignment 1

1. **Did you use semantic HTML5 elements and how did they help?**

   Yes. The page is split into four `section` elements (about, experience, skills,
   education) and each one has an id that the `nav` links to, so the navigation needs no
   extra wrapper elements around it. Every entry in Experience and Education is an
   `article`, because each entry stands on its own and would still make sense if you
   pulled it out of the page. The skills are a `ul` since they are a list of items of
   equal weight, while the NPM and Program pair in the hero is a `dl`, because those are
   labels with values and not a list. Around all of that sit `header`, `main` and
   `footer`. What this gave me in practice was less markup and clearer CSS, since a
   selector like `.timeline .entry` describes the real structure of the page instead of
   a chain of nameless `div` elements. The anchor navigation came for free from the
   section ids. It also means a screen reader can announce the parts of the page rather
   than reading it as one long block. I did not use `aside`, because that element is
   meant for content that sits beside the main topic. On a page this short nothing
   is really secondary. Every section is part of the same statement about who I am, so
   adding an `aside` just to have used the tag would have been the wrong markup for what
   the content actually is.

2. **What layout challenges came up in making it responsive?**

   The hero was the hardest part. On desktop it is a CSS Grid with `grid-template-areas`
   where the photo takes a column that spans two rows next to the name and the details,
   and that arrangement falls apart as soon as the screen gets narrow. The media query
   redefines the areas as a single column and reorders them to identity, then photo,
   then details. That reordering was the real decision, because if the areas were simply
   stacked in source order the long bio paragraph would push the photo far down the
   page. The name and the face are what identify the page, so they belong first with
   the supporting text after them. For the skills I avoided a second breakpoint
   completely by using `repeat(auto-fit, minmax(240px, 1fr))`, which lets the browser fit
   as many 240px columns as there is room for and gives three columns on desktop and one
   on a phone without me naming either number anywhere. The header broke once the
   navigation grew from two links to five, since at 375px they no longer fit on one line
   next to my name, so the header stacks vertically and the nav is allowed to wrap. The
   photo needed a max width on mobile as well, because at the full container width it
   filled most of the screen before any text became visible. The rule I used for all of
   these was to ask what a visitor needs to see first on a small screen: identity before
   detail. Anything that is only decoration, like the offset colour block behind the
   photo, is allowed to shrink.

3. **What are the limits of a purely static page and what would you add next?**

   Everything is written directly into the template, so adding one job or one skill means
   editing HTML and making a commit. That does not scale. It also means a content
   change looks exactly like a code change in the git history. Nothing can be filtered or
   sorted, every visitor gets the identical page and nobody can leave anything behind,
   since the only way to contact me is a mailto link that only works if the visitor has a
   mail client set up. The next thing I would want is to move the content into Django
   models, one for experience entries, one for skills and one for projects, then let the
   view pass them to the template as querysets. The page would then be generated from
   data, the admin interface would become the tool I edit it with and adding an entry
   would no longer require a deployment. After that a contact form, because it is the
   piece a portfolio actually needs and it requires exactly the request handling and
   storage that a static page cannot give you.

### Assignment 2

1. **What happens when a user opens the new portfolio page?**

   When someone opens `/education/`, Django hands the request to `portofolio/urls.py`
   first, which is the project level configuration. That file has no route for
   `education/` of its own. It has `path("", include("main.urls"))`, which matches the
   empty prefix and passes the rest of the path on to `main/urls.py`. The application
   configuration matches `education/` against its own patterns, finds
   `path("education/", show_education, name="show_education")` and calls the
   `show_education` view. The view asks the model layer for data with
   `Education.objects.all()`, which Django turns into a SQL query against the education
   table and hands back as a QuerySet. The view puts that QuerySet into a context
   dictionary under `education_list`, together with my name for the header and footer,
   then calls `render(request, "education.html", context)`. Django loads that template
   from the `templates` directory registered in `TEMPLATES.DIRS`, runs the
   `{% for education in education_list %}` loop over the QuerySet, replaces every
   `{{ ... }}` with the matching value and returns the finished HTML as an
   HttpResponse, which the browser displays. Each part has exactly one job. The project
   `urls.py` decides which application handles a request, the application `urls.py`
   decides which view, the view fetches the data and decides what the template is allowed
   to see, the model knows how the data is stored and the template only decides how it
   looks.

2. **Why store the data in a model instead of writing it into the template?**

   Because a template is responsible for presentation and not for content. If the three
   education entries sit directly in the HTML, adding a fourth means editing a template
   file and making a commit, so content changes and code changes end up mixed together in
   the same history and cannot be told apart later. With a model the data lives in the
   database, can be added through the Django admin or the shell without touching any code
   and the same objects can be reused anywhere in the project. It also means the data can
   be queried rather than only displayed. `Education.objects.all()` already comes back
   sorted by start date because of the `Meta.ordering` on the model. Filtering by level
   or counting entries would be a one line change in the view instead of a rewrite
   of the HTML. For future development the important part is that the template no longer
   depends on how much data exists. The loop handles one object just as well as twenty
   and the `{% empty %}` branch covers the case where there are none, so the page cannot
   break just because the data changed.

3. **What is the difference between makemigrations and migrate?**

   `makemigrations` compares the models with the migrations recorded so far and writes a
   new migration file describing what changed. It does not touch the database at all.
   `migrate` takes those recorded files and applies them, creating or altering the actual
   tables. The split exists so the migration file can be committed to git and then applied
   on every other machine and every deployment in the same order, which is why
   `main/migrations/0002_education.py` is part of this assignment. The example from this
   week is the `Education` model itself. Adding the class to `main/models.py` changed
   nothing on its own. `makemigrations` produced `0002_education.py`, which describes a
   new table with the degree, institution, level, description, started_at and ended_at
   columns. Only `migrate` created that table in `db.sqlite3`. The same applies to
   smaller changes. If I added a `gpa` field to `Education` now, I would need
   `makemigrations` to record the new column and `migrate` to actually add it, because
   otherwise the model and the database would disagree and any query touching that field
   would fail.

## Use of AI

The reflective answers in this README were rewritten with AI support so they are easier
to read. I asked for simpler wording instead of the vocabulary I picked up in my master's
programme, since this is a bachelor level course. The design decisions described in the
answers are my own.

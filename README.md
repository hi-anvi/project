# Tag Chat
### Video Demo: https://youtu.be/CK1pHobfOAg
### Description:

TagChat is a user-friendly application which helps us chat, debate or talk with our
friends, family and colleagues and keep our chats organised without any effort. This aims
to help many organizations organise their work in a clean and orderly fashion reducing
time needed to find some data, increasing efficiency.

## Inspiration

Every day, when I look at my chats or my parents' chat, I see a ***mess***... <br>
Some are related to grocery, some are on a vacation or perhaps a family
function and different work projects. I said well, we should be able to
at least **organize** the data without constant effort. This idea of **grouping**
on the basis of type of *content* gave birth to ___TagChat___.

## Languages

Of course, when it comes to programming, we need to give the computer instructions on
what to do, how to do it and when to do it. I have written these instructions in 5
languages. They are:

- HTML
- CSS
- Javascript
- Jinja
- Python

## Contents

Inside the main `project` folder, besides the `README.md` and `requirements.txt` you
will see multiple programming files either inside subfolders or directly in the main
folder itself. Here are few of the master files:

```
- apology.html
- app.py
- chat.html
- helpers.py
- index.html
- layout.html
- login.html
- register.html
```

### Apology.html

Sometimes users accidentally or maliciously enter invalid or change the HTML
information in forms. Sometimes the user might also accidentally go to a page
which might not exist. To prevent any confusion or conflict, a default
webpage is shown to inform the user that this error has come. `apology.html`
is the user-friendly webpage which gives the warning or error.

***NOTE: helpers.py contains a function called apology which renders this template.***

### App.py

This Python program defines all the valid routes (Example: `/chat`) and then displays
the HTML files to the user. Since this contains the main logic of the website, this is a
part of the backend. We import a few libraries namely:

- CS50: Helps us to access the database to collect, insert, update and store the data
- Flask: Helps to display the HTML content to the user and access any user interactions
- Flask-session: Remembers the user who is logged in and other details
- Werkzeug: Helps us to encrypt and decrypt the passwords using complex ciphers
- Datetime: Gets current time for timestamps

You will find some common functions and statements in the code such as:

```
render_template(<template>)
```
Displays the given template to the user on a particular route
```
apology(<error>)
```
Renders the `apology.html` template to display the given error
```
redirect(<route>)
```
Redirects the user to the given route
```
@login_required
```
Does not allow users to access the above route without being logged in
```
@app.route(<route>)
```
Creates a valid route

### Chat.html and the `/chat` route

The `chat.html` file displays the chatting page to the user. On the sidebar, you see
the existing tags and if any messages have been sent, you will see them with respect to the tags they have been sent on. On the top you will see a dropdown where all your contacts are there.<br><br>
In the `/chat` route, you will see 2 functions, namely:

- `get_tags()` - Returns all the tags in the contact
- `get_history()` - Returns the chat history in the particular tag in a contact

These 2 functionalities combined shapes the main feature of the website.

### Helpers.py

Along with `app.py` there is another Python file which contains the definition of 2
very important functions:

- `apology()` - Renders `apology.html` and displays the error
- `@login_required` - Does not allow logged out users to access the above route

All routes use at least one of these two functions to work correctly in a user-friendly manner.

Example of `apology` in code:

``` python
if request.method == "GET":
        contact = request.args.get("contacts")
        if not contact and not session.get("contact_id"):
            return apology("No selected user")
```

Example of `login_required` in code:

``` python
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Allows user to change profile features"""

    # Show form if user loads page
    if request.method == "GET":
        return render_template("settings.html")
```

### Index.html and the `/` route

This HTML page and the route simply display the frontend (HTML and CSS).
They do not look at any user interactions as such.

### Layout.html

This HTML file does not need any route and is not displayed onto the screen without
some added content. You might come upon some Jinja syntax here like:

``` jinja
{% if session["user_id"] %}
```
 You might have also noticed Jinja syntax in other HTML files such as:

 ``` jinja
 {% extents "layout.html" %}

 {% block title %}
    Apology
 {% endblock %}
 ```

This basically extends the html in `layout.html` to the file where this syntax was
written.

The `layout.html` file adds the contacts list and navbar to all the HTML pages. Since
it would be hard to code all that on all the files, `layout.html` copies and pastes it
all for me without me doing much work.

### Login.html and the `/login` route

This HTML file displays the login page to the users. After the user clicks the `login`
button, the username and password are sent to the `/login` route from where it checks
whether the user input was valid or not. If any error occurs, an error is displayed to
the user but if the username and password match, the user gets logged in.

### Register.html and the `/register` route

This HTML file displays the register or sign up page to the user. After the user
clicks the `register` button, the username and password are sent to the `/login` route
from where it checks whether the user input was valid or not. If there were any errors,
an error is displayed to the user. Else the user is redirected to the login page.

## How to run

Step by step instructions:

- Install requirements via `pip install -r requirements.txt`

- Run `flask run` in the terminal or command line

- Open `http://127.0.0.1:5000/` in a browser

## Features

All the features:

- User authentication (login/register)

- Chat organization by tags

- Error handling with custom apology page

- Session management with Flask-Session

- Responsive frontend with HTML/CSS

## Database

The projects.db database contains 4 main tables:

- users → stores user credentials (id, username, password_hash)

- text_pals → stores user contacts (id, user_id, pal_user_id)

- chat_history → stores chat messages with tags (id, text_pal_id, sender_id, receiver_id, timestamp, tag_id, message)

- tags → stores user-defined tags (id, text_pal_id, tag)

## Future Work

I will improve the project in several ways such as:

- Enable file sharing

- Optimize the SQL database structure for scalability and efficiency

- Add search in contacts and messages

- Add optional AI-powered chat assistant

- Make index page better

- Improve the placement of the Send button for better usability

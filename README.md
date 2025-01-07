# PROJECT TITLE: MOOD MATE
#### Video Demo:  <https://youtu.be/TpfIgwKmvw0>

## 1/ Description

MOOD MATE is a Web App that tracks your emotions over time.
What inspired me for this project is my previous job as a social worker, where I was helping people dealing with emotional issues.

By enabling users to record their daily emotions, MOO MATE serves as a personal journal for emotional health. It aims to foster self-awareness and provide insights into patterns that might otherwise go unnoticed.

#### <ins>Key Features

<ins> User Authentication:</ins>
MOOD MATE ensures secure user registration and login functionality using hashed passwords. Users' data is protected, and individual sessions are managed to provide a personalized experience.

<ins>Emotion Logging:</ins>
Users can record their current emotions, choosing from predefined categories like: "Great", "Just ok", "Not so well", "Not well at all"

<ins>History Tracking:</ins>
Users can access their emotional history, which is stored with timestamps, allowing them to observe and reflect on patterns over time.

<ins>Interactive Feedback Pages:</ins>
Each emotional state redirects users to a uniquely designed page featuring supportive messages and visuals tailored to uplift or encourage.

To simplify the experience, I opted for predefined emotional categories. This decision ensures consistency in the data while allowing for meaningful feedback. However, in future iterations, we may introduce custom emotion logging.

## 2/ Backend Overview

I Used Flask, python and SQlite3 to perform this application.

#### <ins>The database:
I created a database called 'feelings.db' with 2 tables:
1. A table ```users``` with 3 columns: *id*, *username*, and hashed passwords.
2. A table ```user_feelings```  that records user emotions.The columns created are: *id*, *user_id*, *feeling*, *time*.

#### <ins>Flask routes:

*app.py* is The main application file containing all the routes and backend logic. The application includes several routes, each serving a specific purpose:

+ ```/```: Handles user registration.
+ ```/login``` and ```/register```: Manage user authentication.
+ ```/presentation```: Displays the main user dashboard.
+ <ins>Emotion-specific routes</ins> (```/bad```, ```/great```, ```/ok```, ```/not_ok```) record the user's feeling and provide immediate feedback.
+ ```/history```: Fetches and displays the user's emotional history in a user-friendly table form

## 3/ Frontend Overview

The frontend is crafted using **HTML** templates integrated with **Jinja** for dynamic content rendering. I also used additional styling with **CSS** frameworks like **Bootstrap**. Each page is designed to be user-friendly and visually appealing.

#### <ins>Frontend Functionality:
+ ```templates/```: A folder containing HTML files for various pages like register.html, login.html, and emotion-specific pages
+ ```static/```: Houses all images and CSS for styling

Each emotion-specific pages, such as *bad.html*, include:
1. Dynamic messages based on the user's feeling.
2. A link to view emotional history.
3. Supportive visuals to engage the user.

#### <ins> The visuals:

I found an interesting Website that helped me creating my logo as well as the images for emotion-specific pages: <https://looka.com/>.

You are prompted to put the name of a domain and I chose *Social*.
Then you can select more themes, images, colors, modify the font for more accuracy.

## 3/ Test the App


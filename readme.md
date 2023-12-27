## Blogger App
Blooger app where users can sign up and start adding posts.

Key features: <br>
    - Sending emails (filling up contact form and sending email). Fake SMTP server <em> Smtp4dev </em> is used for it. <br>
    - Use of <em>Celery</em> to take email sending task off the request/response cycle. <br>
    - Use of <em>Redis</em> as message broker and for caching. <br>



#### Running Blogger app locally on your system
- Clone the repository <br>
`git@github.com:yogesh-shrestha/blog-app-test-driven.git`
- Change directory <br>
`cd blog-app-test-driven`
- Build and Run the images (multi-container application) <br>
`docker-compose up --build`

Fake SMTP Server runs at http://localhost:5000/ <br>
Development server starts at http://localhost:8000/

<b>Superuser credentials </b> <br>
username: admin<br>
password: admin<br>

### Entity-Relationship Diagram 
![alt Demo Blogger](readmeimages/er_diagram.png)

### HomePage
![alt Demo Blogger](readmeimages/homepage.png)






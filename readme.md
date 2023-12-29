## Blogger App

Key features: <br>
    - User authentication using Django's default system. <br>
    - User-friendly sign-up process with password change and reset options.<br>
    - Post creation functionality for users.<br>
    - Profile editing for users.<br>
    - Implementation of <em>Celery</em> worker for background tasks, specifically sending emails.<br>
    - Use of <em>Redis</em> as message broker and for caching. <br>



#### Running Blogger app locally on your system
- Install <em>git</em> and <em>docker</em> in your system.
- Clone the repository <br>
`git clone git@github.com:yogesh-shrestha/blog-app-test-driven.git`
- Change directory <br>
`cd blog-app-test-driven`
- Build and Run the images (multi-container application) <br>
`docker-compose up --build`<br>

Development server starts at http://localhost:8000/. Fake SMTP Server runs at http://localhost:5000/ ( https://github.com/rnwood/smtp4dev).

<b>Superuser credentials </b> <br>
username: admin<br>
password: admin<br>

### Entity-Relationship Diagram 
![alt Demo Blogger](readmeimages/er_diagram.png)

### HomePage
![alt Demo Blogger](readmeimages/homepage.png)






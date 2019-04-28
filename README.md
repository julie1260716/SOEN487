# **SOEN 487 Group Project**
A group project created for course SOEN 487 Web Services and Applications. The implementation of the project follows the concept of micro services and it applies Flask micro framework.

# Project Description
The Cinema website will loosely simulate existing movie websites, such as “Cineplex.com”. The site’s functionalities will include Login, Signup, Movie service, User Profile Service, Ticket Booking services, and a Movie Recommendations service. The following diagram displays each mircroservice of the project is composed of and the associations between each microservice.

![Micro Services]()

**Authentication Service**  
Authentication service, as the name suggests, it authenticate users for other microservices when the identify of an user needs to be confirmed. In this project, the authentication is implemented by using JWT token. 

![Auth Service]()

**User Service**  
User service is responsible for recording all the necessary information related to a user (name, password, email address, etc.). All operation on the user data requires the request sender to be authenticated first.


**Movie Service**  
Movie service mainly takes charge of displaying information for different movies through an html template. It interacts with recommendation service when recommendation service provides recommended movies for an user.

![Movie Service]()

**User Profile Service**  
User profile is a special characteristic of our project. its role is to store a user's perference on movies such as the rating or genre of a movie. To achieve this functionality, users need to first fill in a form to provide their preference data. These data will be later on stored and updated. 

![User Profile Service]()

**Recommendation Service**  
Recommendation service works by interacting with movie service and user profie service. To recommend users the movies they will like, this service will call profile service to fetch the profile id for the current user and then fetch all the perferences associated with the profile id. After that recommendation service will call movie service to provide all the movies meet those peferences obtained from user profile service. At the end, the movie data obtained will be render through a html template designed for recommendation service.

![Recommendation Service]()

**Ticket Booking Service**  
Ticket Booking service allows users to order movie tickets based on the movie name, theatre location, show time and other criteria. Before a ticket booking operation is executed, the authentication of request sender is required.

![Ticket Booking Service]()



# Project Installation
To install the project, the following packages are needed:
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Jinja2
- SQLAlchemy
- WTFforms
- requests
- mysql-connector-python

All the packages are include in requirement.txt file.


# Project Setup
To run the project, enter the following commands to launch each microservice:

For Authentication Service
```python
python SOEN487/authentication_service/main.py
```

For User Service
```python
python SOEN487/user_service/app_user.py
```

For Movie Service
```python
python SOEN487/movie_service/app_movie.py
```

For User Profile Service
```python
python SOEN487/user_profile/app_profile.py
```

For Recommandation Service
```python
python SOEN487/recommendation_service/app_user.py
```

For Ticket Booking Service
```python
python SOEN487/ticket_booking_service/app_ticket_booking.py
```

Port Numeber
- Authentication Service: 5000
- User Service: 5001
- Movie Service: 5002
- User Profile Service: 5003
- Recommendation Service: 5004
- Ticket Booking Service: 5005

The following databases need to be created on MySQL server:
- AuthenticationDB
- UserDB
- MovieDB
- ProfileDB
- RecommendationDB
- TicketBookingDB

&nbsp;

# Contributors & Contact Information
### **Team Members (team_x)**

| Name           | Email                   | ID       | Github Username |
| -------------- | ----------------------- | -------- | --------------- |
| Chen Zhuang    | ericzhuang603@gmail.com | 40007314 | Eric-Z0         |
| Julie Merlin   | jz_merlin@gmail.com     | 40007795 | julie1260716    |
| Marzie Shafiee | m.shafiee.84@gmail.com  | 40016801 | marzieshafiee   |
| Yang An        | anyang47@hotmail.com    | 27878699 | Yang8547        |
| Bochuan An     | anbochuan@gmail.com     | 27878745 | anbochuan       |

&nbsp;

# Task Breakdown
The table below record the responsibilities for each teammate

| Teammeate      | Tasks                                                |
| -------------- | ---------------------------------------------------- |
| Chen Zhuang    | Ticket Booking Service, Part of Movie Service, Part of User Profile Service, Part of Recommendation Service, Integral Test, Documentation |
| Julie Merlin   |                                                      |
| Marzie Shafiee | Recommendation Service, unit test                                              |
| Yang An        | User Service, unit test, database diagram                                                      |
| Bochuan An     | Authentication service, unit test, documentation                                                  |

&nbsp;

# Issues & Bugs
While we were implementing this project, we had a hard time figuring out how each microservice should interact with each other. Probably it is due to the complexity of our project or because we all had limited time to work on this project. We did not come to an agreement on what is the most appropriate design/layout for our project. We think that each microservice should be as independent as possible but when we designed our database and later on created out view functions we had to modify our design to different degree to better 'cooperate' with other microservice. 

As we want to make the most use of Flask framework and its extensions, it took us a certain amount of time to understand and use its tools. For example how to create our own WTForm to validate user input and how to use Jinja2 template to render the html page the way we want. 

When it comes to the design of UI, we vacillated between whethere we should have a 'front controller' to dispatcher request to different microservices or we should allow each microsevice be reponsible for only certain, specific html pages. 

Another thing we found very chanllenging is the design of integral test. Previously, we did the unit test for our own microservice. When we need the data coming from outside we just hard coded the data. However, for integral test, it does not only test the functionality of each microservice but also logic behind the interactions between microservices. This became even harder when there was a lack of communication between each teammate.





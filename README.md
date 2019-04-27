# **SOEN 487 Group Project**
A group project created for course SOEN 487 Web Services and Applications. The implementation of the project follows the concept of micro services and it applies Flask micro framework.

# Project Description
The Cinema website will loosely simulate existing movie websites, such as “Cineplex.com”. The site’s functionalities will include Login, Logout, Signup, Ticket Booking services, and a Movie Recommendations service.

![Micro Services]()

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
| Chen Zhuang    | Ticket Booking Service, Integral Test, Documentation |
| Julie Merlin   |                                                      |
| Marzie Shafiee |                                                      |
| Yang An        | User Service, unit test, database diagram                                                      |
| Bochuan An     | Authentication service, unit test, documentation                                                  |

&nbsp;

# Issues & Bugs
While we were implementing this project, we encountered...

&nbsp;

# Other Comments
Write down your comment...

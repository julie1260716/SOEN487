## Cinema Website


The Cinema website will loosely simulate existing movie websites, such as “Cineplex.com”. The site’s functionalities will include Login, Logout, Signup, Ticket Booking services, and a Movie Recommendations service.



### Micro Service 1: User information


Stores the user information (e.g email, avatar) and manage user

Provide a endpoint to list the users and also allow to query the user base on their user ID and also edit info

Interact with users via email (optional)

|     Methods    | HTTP Request | Description |
| ---------------|--------------|-------------|
| getUserInfo    | GET /users/<id>  | Return user info by user id |
| addUserInfo    | POST /users      | Insert user profile |
| updateUserInfo | PUT /user/<id>   | Edit user profile or update user's point |
| EmailToUser    | POST /Emailuser/ | Send email to user |



### Microservice 2: Authentication


Perform authentication for each microservice call. Returns authentication tokens if the user is authenticated

User Login, register and change password

|     Methods    | HTTP Request | Description |
| ---------------|--------------|-------------|
| Login | POST /login         | User Login |
| Register | POST /user         | Register user |
| ChangePSW | PUT /user         | Change password |
| GetToken     | POST /auth/token          | Return token |



### Micro Service 3: Movie Recommendations


Registered users will complete a profile indicating their movie preferences, such as favored movie genre, actors, directors, producers, etc.

They can consult the “Recommendations” page to see which movies are best suited for them, based on their completed profile.

In addition, any new movies added to the system will also be suggested to the user if that movie fits their criteria.



### Micro Service 4: Online Ticket Booking


Provide users with movie ticket information based on the location, movie name and date they entered.

When a movie ticket is successfully booked, a confirmation letter (a pdf file) will be sent to user’s email box (this functionality may be changed later on)

In order to book a ticket, user has to first sign in (or sign up) to validate their identity. This requires the interaction with ‘User Info Management’ microservice.  

Any movie information other than its name, show time and the number of available tickets requested by users will have to communicate with ‘Movie Recommendations’ microservice

|     Methods    | HTTP Request | Description |
| ---------------|--------------|-------------|
| listAllTickets | GET /tickets         | List all the tickets |
| getTickets     | GET /ticket          | Return ticket info by movie name |
| bookTicket     | POST /bookTicket     | Book movie ticket |
| cancelTicket   | POST /cancelTicket   | Cancel movie ticket |
| getBookingInfo | GET /booking         | Return ticket booking information for a given user |

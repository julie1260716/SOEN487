## Cinema Website


The Cinema website will loosely simulate existing movie websites, such as “Cineplex.com”. The site’s functionalities will include Login, Logout, Signup, Ticket Booking services, and a Movie Recommendations service.



### Micro Service 1: User information


Stores the user information (e.g email, avatar) and manage user

Provide a endpoint to list the users and also allow to query the user base on their user ID and also edit info

Interact with users via email (optional)



### Microservice 2: Authentication


Perform authentication for each microservice call. Returns authentication tokens if the user is authenticated

Login, register



### Micro Service 3: Movie Recommendations


Registered users will complete a profile indicating their movie preferences, such as favored movie genre, actors, directors, producers, etc.

They can consult the “Recommendations” page to see which movies are best suited for them, based on their completed profile.

In addition, any new movies added to the system will also be suggested to the user if that movie fits their criteria.



### Micro Service 4: Online Ticket Booking


Provide users with movie ticket information based on the location, movie name and date they entered.

When a movie ticket is successfully booked, a confirmation letter (a pdf file) will be sent to user’s email box (this functionality may be changed later on)

In order to book a ticket, user has to first sign in (or sign up) to validate their identity. This requires the interaction with ‘User Info Management’ microservice.  

Any movie information other than its name, show time and the number of available tickets requested by users will have to communicate with ‘Movie Recommendations’ microservice

## Exception based alerting
Just head home, and know that your defined "usual" route home is the fastest... unless you hear from us.

You'll receive an SMS alert if the system detects an "alternate" route meets your defined threshold for time savings.

### What it does
2 components work simultaneously. 
- The first is a Flask app with PostgreSQL database that allows users to register and manage their subscription (free) to the service. Users define turn-by-turn routes, the days/times they execute that route, and how much time saved must exist via an alternate route before they want to be notified. 
- The second part of the service is an automated job scheduler, which at the appropriate time reaches out to Google Maps Directions API, determines if the user's preferred route is best or if the user's threshold for an alternative has been met. It then provides a text message alert if an exception exists.
- (Note: Currently the service sends a text message whether or not the threshold for an alternate route notification is met. This is for testing purposes.)

### Why I Built This
I know how to get to and from work. So I don't turn on my navigation. It would be extra work.

But every so often my "usual" route has an unexpected accident, or traffic jam. I thought to myself, "I wish I didn't have to run navigation every day just to avoid the rare traffic jam."

And the idea was born. A system that houses my "usual" route home. Each day at my predefined time, it checks the "usual" route's estimated time against the "best available" route, only generating an SMS notification if the time savings surpasses my defined threshold. I don't run navigation... unless I get a message.
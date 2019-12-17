## Exception based alerting
Just head home, and know that your defined "usual" route home is the fastest... unless you hear from us.

You'll receive an SMS alert if the system detects an "alternate" route meets your defined threshold for time savings.

### Part 1 of 2
This repo represents 1 of 2 programs that run together, to provide exception based navigation notifications for a user's commute to/from work. In this part of the service, a user registers, saving their commute data (includes a GUI with help from Google Maps APIs). The second part of the service is a job scheduler, that run analysis on user routes at the user's predefined times of day.

### Why I Built This
I know how to get to and from work. So I don't turn on my navigation. It would be extra work.

But every so often my "usual" route has an unexpected accident, or traffic jam. I thought to myself, "I wish I didn't have to run navigation every day just to avoid the rare traffic jam."

And the idea was born. A system that houses my "usual" route home. Each day at 5pm (currently requires manual file running) it checks the "usual" route's estimated time against the "best available" route, only generating an SMS notification if the time savings surpasses my defined threshold. I don't run navigation... unless I get a message.
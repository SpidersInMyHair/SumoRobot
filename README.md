# SumoRobot

At the moment:
---------------
Compiles then waits for user to press a button. 
      (ATM this is skipped to make debugging easier - hence why the variable 'begin' = True). 
When user presses the button on EV3 brick - waits 3 seconds as required.
Then simply just alternates between "searching" and "charging".


Current Bugs:
--------------
Since the SONAR is housed right at the front of the robot - any front-collision that the robot faces will make the SONAR value go
crazy since it goes crazy at extremely small distances.
SOLUTION would be to: House the SONAR at least 15mm to 20mm from the front-collision face.

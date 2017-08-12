# SumoRobot

Written by Rishad Mahbub
For ENGG1000
Dated 2017S1

At the moment:
---------------
Compiles then waits for user to press a button. 
      (ATM this is skipped to make debugging easier - hence why the variable 'begin' = True). 
When user presses the button on EV3 brick - waits 3 seconds as required.
Then simply just alternates between "searching" and "charging".


Known Issues:
--------------
If the SONAR is apart of the collision face - then the distance that the SONAR value returns (if it is point blank touching the opponent)
will fluctuate hugely anywhere from 0 to 2550. Solution is to not have the SONAR as part of the robot's collision face - rather housed
more 'within' the robot.

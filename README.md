# Core-Keeper-simple-fishing-bot

This is a simple fishing bot created with Python and openCV for the game "Core Keeper".
OpenCV coordinates adjusted for 3440x1440 screen resolution.


I have created this project for the simple fact of wanting to automate something (simple) as part of my learning path in programming.

I have chosen the game "Core Keeper" because it is a fun, entertaining game, and above all a game oriented to the "single-player" where an abuse of the use of bots does not affect the progress of the other players.



I want to make the latter clear. I don't want to be called a "boter" or "cheater" for creating a program to automate a process, with this project I'm not looking to promote these practices, it's just a personal project that I've made public so that it doesn't get forgotten in the background from my hard drive.



# Instructions:

- 1- Type    pip install -r requirements.txt     in your command line in the same folder as the script and run main.py.

- 2- Open the game and place you character near a water block 
      It doesn't matter if the water block is to the right 
      or left of the character, but never above or below.
      Remember that it only works with 3440x1440 resolution,
      it does not scale automatically (WIP).
      I have tried to modify the position of the detectors taking as reference the center of the monitor, but the scale of the images also changes and that makes it difficult to match. In the next attempt I will try to calculate the scale difference of the different resolutions, and I will apply the calculations based on them instead of the distance in pixels as I have now.
      
- 3- Place your fishing rod in the button 5 of your action bar.
      I have chosen button 5 because... why not?.
      The bot presses the 5 button from time to time
      to make sure that it has the fishing rod in its hands,
      in case there is any accidental click or scroll during the process.
      Also remember to set "Alt + 1" to do the same as mouse right button (this is to prevent accidental clicking).

- 4- Run main.py.
     * You will see that some options appear to select:
        - The first one will make you choose between "y" or "n" (Yes, No or leave blank) to activate or not the "debug" mode (disabled by default).
             With debug mode enabled, a box will be displayed above the game (always on top) showing what the script "sees".   
        - The second option shows the default duration of the fishing session and asks if you want to change it,
            press enter if you want to leave it as is or enter an integer for the duration you want (60 minutes by default).    
        - The third and last option gives you a choice of 2 types of detection mode (HSV based), both of which give similar results (mode 1 by default).
            Enter the number "2" or leave it blank and press enter.
        - You can skip these options by pressing "enter" 3 times. 
        - After a couple of seconds, the bot will take control of the mouse, click on a point in the game to bring it into focus, 
            and start fishing. When the assigned session minutes are completed, the bot will stop and display the details of the session,
            such as: trys, object caught, fish caught, fails and a rate of catches/minute.

- 5- If you want to interrupt the script, you just have to press the "q" key,
     Pressing it several times in case the script is in one of the sleep().
      

      
      
      
      
# Thanks      
Thanks to Ben Johnson for the excellent tutorial he made with a series of videos on youtube about openCV and other cool stuff.
Without them, I would not have been able to carry out this project, nor would I have learned so much.
- https://www.youtube.com/c/LearnCodeByGaming/featured

- https://github.com/learncodebygaming

# Overview 

Its an script that helps to upload Spotify listening history to last.fm. <br><br>

## STEPS TO FOLOW 
<br><br>
**Step 1: Get Spotify History**

- Go to https://www.spotify.com/in-en/account/overview/ 
- Click on **Account privacy** and scroll down there u will get options to requst data 
- Wait for Spotify to send ur data within 5-6d. <br><br>


**Step 2: Install python & VS Code**

- Go to https://www.python.org/downloads/ and install and run it.
- After installing in go to terminal ( Windows+ R and type cmd and enter) and 
  in the type "python --version" to check if u have successfully installed python.
- Get VS code too to edit the files "https://code.visualstudio.com/download". <br><br>


**Step 3: Install Required Libraries**

- Go to terminal and type **"pip install pylast pandas python-dotenv"** and it will be installed. <br><br>


**Step 4: Convert .jason file to .csv file**

- Go to "cmdtoconvert.md" and read u lazy ass. <br><br>


**Step 5: Split the .csv file**

- Go to "cmdtosplit.md" and read dummy. <br><br>


**Step 6: The EXECUTION**

- Make a *new folder CSVtoLast.fm* .
- Add the "lastfm_scrobbler.py" and ".env" file 
- Go to https://www.last.fm/api/account/create

- **Create an API account**
- You will get:
    API Key
    API Secret
    Username (your Last.fm username)
    Password (your Last.fm password)
- And replace that info in ".env" file.

- Make a *new folder Music History inside CSVtoLast.fm folder* 
  and inside Music History folder add all the 
  part0,1,2... files.

- Your folder should now look smt like this 

<pre> ```  
    📁 CSVtoLast.fm
    ├── 📁 MusicCSV
    │   ├── part0.csv
    │   ├── part1.csv
    │   ├── part2.csv
    │   ├── ...
    │   └── part10.csv
    ├── .env
    └── lastfm_scrobbler.py 
  ``` </pre>

- Now go to CSVtoLast.fm folder right click on it and open terminal 
  and type **"python lastfm_scrobbler.py"** and hit ENTER. 

- I hope it does work for ya all cuz it did for me. <br><br>


# Conclusion

Its an free alternative to universalscrobbler although its premium version is really cheap but 
people still have problem transferring files, and cancelling the subscription. 

So i made this script, 
its bit of a manual work work but does the job ^^

If you guys have any doubt join my discord server https://discord.gg/8FK38a2dR8 <br>
   ~ Big Mike





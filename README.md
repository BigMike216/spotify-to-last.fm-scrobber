# Overview 

Its an script that helps to upload Spotify listening history to last.fm. <br><br>

## STEPS TO FOLOW 
<br><br>

**Step 1: Get Spotify History**

- Go to https://www.spotify.com/in-en/account/overview/ 
- Click on **Account privacy** and scroll down there u will get options to requst data 
- And you will get your Spotify History in few days in your email. <br><br>


**Step 2: Install python & VS Code**

- Go to https://www.python.org/downloads/ and install and run it.
- After installing open the terminal ( Windows+ R and type cmd and enter) and 
  in the type 
  ```
  python --version
  ```
  to check if u have successfully installed python.
- Get VS code too to edit the files "https://code.visualstudio.com/download". <br><br>


**Step 3: Install Required Libraries**

- Go to Windows PowerShell and type 
```
pip install pylast pandas python-dotenv
```
  click enter and it will be installed. <br><br>


**Step 4: Convert .json file to .csv file and Split it**

1. Click on "Clone" and download the ZIP file, then extract it.

2. After extraction, open the extracted folder — you might see another folder with the same name   
   inside. Copy the last extracted folder (the one that contains all the files) and move or paste it anywhere you like.

3. Upload the Spotify history files should look smt like this- 
   **StreamingHistory_music_0** (if its Streaming history for the past year)  
   or 
   **Streaming_History_Audio_2024-2025_0** (if its Extended streaming history)
   so upload this files in json to csv folder (you can upload both if u have) 


4. Your folder should now look smt like this:
   <pre>
        📁 json to csv
        ├── converter.py
        ├── output.csv
        ├── StreamingHistory_music_0.json
        ├── StreamingHistory_music_1.json
        └── ... (any other StreamingHistor_music files) 
   </pre>

   OR

   <pre>  
        📁 json to csv
        ├── converter.py
        ├── Streaming_History_Audio_202x-202x_0
        ├── Streaming_History_Audio_202x_1
        └── ... (any other Streaming_History_Audio files) 
   </pre>

> 💭 Note:
> So Last.fm has a limit of around 2800-3000 scrobbles per day. Going above this might cause    
> rate-limit errors or temporary submission blocks.
> This script automatically splits large CSV files into smaller parts.
> (each containing about 2600 songs)
> Also the Last.fm API supports sending multiple scrobbles in a single request 
> (up to 50 tracks per call).
<br><br>

**Step 5: The EXECUTION**

- Create a new folder- 
```
CSVtoLast.fm
```
- Add the "lastfm_scrobbler.py" and ".env" file 
- Go to https://www.last.fm/api/account/create

- **Create an API account**
- You will get:
    API Key
    API Secret
    Username (your Last.fm username)
    Password (your Last.fm password)
- And replace that info in ".env" file.

- Create a *new folder Music History inside CSVtoLast.fm folder* 
  and inside Music History folder add all the 
  part0,1,2... files.

- Your folder should now look smt like this 

<pre>
    📁 CSVtoLast.fm
    ├── 📁 MusicCSV
    │   ├── part0.csv
    │   ├── part1.csv
    │   ├── part2.csv
    │   ├── ...
    │   └── part10.csv
    ├── .env
    └── lastfm_scrobbler.py 
</pre>

- Now go to CSVtoLast.fm folder right click on it and open terminal 
  and type this and hit ENTER. 
  ```
  python lastfm_scrobbler.py
  ```

- I hope it does work for ya all cuz it did for me. 
<br><br>

**DONT FORGET TO KEEP A 24H GAP AFTER UPLOADING EACH PART FILE TO LAST.FM** <br><br>

# Conclusion

Its an free alternative to universalscrobbler although its premium version is really cheap but 
people still have problem transferring files, and cancelling the subscription. 

So i made this script, 
its bit of a manual work work but does the job ^^

If you guys have any doubt join my discord server https://discord.gg/8FK38a2dR8 <br>
   ~ Big Mike

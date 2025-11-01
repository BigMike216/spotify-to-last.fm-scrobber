1. Creat a folder named-
```
json to csv 2
```

2. Creat a new file in that folder named-
```
spotify_data.json
```

3. The Spotify history files should look smt like **Streaming_History_Audio_20xx-2025_0** (etc...)
   Copy all the data from each of these history files and paste them into **spotify_data.json**.

4. How to copy correctly

   - Open the Spotify history file in VS Code.
   - Press Ctrl + A → Ctrl + X  →  switch to  spotify_data.json →  Ctrl + V.
   - Copy all the history from that files and paste it in the **spotify_data.json**. 

5. Upload the **converter.py** and **spotify_data.json** files in  "json to csv 2"

4. Your folder should now look smt like this
<pre>  
     📁 json to csv 2
     ├── converter.py
     └── spotify_data.json
</pre>

5. Now Install the Required Library-

   - Go to Windows PowerShell
   - Then paste this command 
     ```
     pip install pandas
     ```
     OR (if there was any error use the other command)
     ```
     py -m pip install pylast pandas python-dotenv
     ```  

6. Go to json to csv 2  folder right click on it and open terminal
   and paste this command and press enter.
   ```
   python converter.py
   ```
   
7. Hopefully now the json files are converted to csv files and saved in **output.csv** file.

8. If any issue check the file name in the convert.py , or check the README.md to contact.
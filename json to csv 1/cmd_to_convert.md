1. Create a folder named-
```
json to csv 1
```

2. Upload the **converter.py** and **output.csv** (make sure the file is empty) files in
   json to csv 1 folder along with the Spotify history files should lokk smt like **StreamingHistory_music_0**.

3. Your folder should now look smt like this
<pre>
     📁 json to csv 1
     ├── converter.py
     ├── output.csv
     ├── StreamingHistory_music_0.json
     ├── StreamingHistory_music_1.json
     └── ... (any other StreamingHistory files) 
</pre>

4. Now Install the Required Library-

   - Go to Windows PowerShell
   - Then paste this command 
     ```
     pip install pandas
     ```
     OR (if there was any error use the other command)
     ```
     py -m pip install pylast pandas python-dotenv
     ```

5. Go to json to csv 1  folder right click on it and open terminal
   and paste this command and press enter.
   ```
   python converter.py
   ```
   
6. Hopefully now the json files are converted to csv files and saved in **output.csv** file.

7. If any issue check the file name in the convert.py , or check the README.md to contact.

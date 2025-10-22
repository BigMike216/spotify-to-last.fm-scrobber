1. If your history has more than 2500 songs this is for ya.

2. So Last.fm has a limit of around 2800 scrobbles per day. Going above this might cause rate-limit 
   errors or temporary submission blocks.

3. This script splits your large files into smaller parts — each file containing about 2500 songs.  
   The Last.fm API supports sending multiple scrobbles in a single request 
   (up to 50 tracks per call).

4. To convert

   - *Create a folder*.
   - Add the **output.csv** files (the one you got after converting the json files) and 
     **split_csv.py** in that folder.
   - Your folder should now look smt like this

<pre>
    📁 Split CSVs
     ├── output.csv
     └── split_csv.py
</pre>

   - now right click on the folder and go to terminal and write this command and press enter.
   ```
     python split_csv.py
   ```

5. Now ur output files will be split into multiple files like
   ```  
    part0.cvs
    part1.csv
    paer2.csv
    ....
   ```

6. If any issue check the file name in the convert.py , or check the README.md to contact. 
1. If your history has more than 2500 songs this is for ya.

2. So last.fm has a limit of around 2800 scrobble/day so if u try to scrobble more than 2800
   songs then there is a chance you might get banned.

3. So using this script you can convert the big chunk of files into parts, each file will
   contains 2500 songs. Also last.fm API lets us send multiple scrobbles in one request (up to 50 tracks per call)

4. To convert

   * *make a folder*.
   * add the output.csv file and split_csv.py in that folder.
   * your folder should now look smt like this

<pre> ```  
   📁 Split CSVs
     ├── output.csv
     └── split_csv.py
``` </pre>

   * now right click on the folder and go to terminal and write this command
     "python split_csv.py" and press enter.

5. Now ur output files is has been split into multiple files
   like
<pre> ```  
    part0.cvs
    part1.csv
    paer2.csv
    ....
``` </pre>

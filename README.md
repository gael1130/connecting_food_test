TL; DR: Divided memory usage by 20 in the large file, divided execution time by 2 in the huge file.

Execution times: # 113.41 seconds for config from scratch (download included)
- small_file: 0.16 seconds
- medium_file: 0.43 seconds
- large_file: 3.0 seconds after optimization
- huge_file: 32.84 seconds after optimization

Video:
https://www.loom.com/share/2339de72347843fe8a384e475ba09ce4
******


1. Problem statement

    I want a Python script, handling big files without altering them. It makes me think of pandas.

    When I read the Readme.md file I see that there are requirements on the naming of files and the type of data.    


2. Pseudo Code
    1. Download the files
    2. Explore them (size, issues, context (names, numbers, etc.)), starting with the smaller one
    3. Split the smaller one first as requested    
    4. Do the same with the others and measure performance
    5. Optimize the code for scalability


3. Future improvements
    1. Writing Unit Tests
    2. Writing a documentation
    3. Optimize Pandas:
        
       https://pandas.pydata.org/docs/user_guide/scale.html 
       https://pandas.pydata.org/docs/user_guide/enhancingperf.html
       
    4. Save iso countries in a json instead of calling the library: what happens to UK?
    5. What do we do with the corrupt data? How can we prevent that in the future?
   
4. Video Explainer:
https://www.loom.com/share/2339de72347843fe8a384e475ba09ce4
5. Files: 
   1. Config: run it to download the csv files and create the folders and huge file.
   2. Performance: To see the choices I made for better performance
   3. Huge, Large, Medium, Small files: to work on each file size individually
   4. Main: Uncomment the first lines to run it all in one go
   
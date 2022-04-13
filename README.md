# Battery Monitoring
A simple python battery monitoring project written in Python 3.10

The scope of this project was orignally intended to be small and just funtional. 

It has very much stayed that way, originally the program was a simple clock that used multithreading to update the time. 
Then I expanded it to utilize the OS library to check for statistics on battery usage and so on 

# Usage

```python main.py```

The UI should then open and display said information in a 400x200px window. 

# Important
The functionality of the 'X' button on the window frame has been altered to signal the battery and clock threads to close safely on exit. 
If either 'Ctrl-C' or 'End Task' in resource manager is utilized the threads may not close safely and immediatley. 
Since the threads are background threads they should close appropriately (or simply crash once data cannot be updated).

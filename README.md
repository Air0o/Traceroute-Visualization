# Traceroute-Visualization
A visual representation of the traceroute command.

An executable file can be found in the **"dist"** folder and must be opened as **administrator** to work.

It might be necessary to add exceptions to the firewall or even disable it entirely.

### Why does the process take a lot longer with some sites? 
Sometimes the script never shows **"Destination reached"** and keeps sending packets because the target or its network don’t send replies correctly or at all.
Reliable sites (such as google.com) may respond correctly, but others may block replies, so the trace process continues not knowing it actually reached its destination.

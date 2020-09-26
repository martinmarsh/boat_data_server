# boat data server

Falcon Based Web Server which delivers via an API json boat data
collected from a low level data manger (such as 'boat').

It also serves the files used to deliver a react web app which then
communicates via the API.  This allows graphical presentation of compass,
autohelm and a human interface for manually entering data such as such as
 course control, log narrative and alarm settings.
 
The project start life as a combined web server and back end processor using
Falcon and Python Multiprocessing.  Whilst this worked well
with OpenCPN consuming NMEA data from usb serial devices it had limited
flexibility when expanding the boat network to include a NMEA200 network
and an additional cockpit chart plotter.  The back end processing in this project
was then transferred to the 'boat' repro which also acted as a central point of data
collection, logging and distribution.  This repro is now solely concerned with providing a
 human interface.  
 
The data concerned is a single record in the form of a dictionary of key pairs.
The keys will vary according to what devices are available. Critical data such
as position has a timestamp.
### Python image classification
#### Web server

This web server is used by the front-end of the application
in order to interface with the image classification library.

To run it, you need to export the variable:

export FLASK_APP=run.py

After exporting it, you should be good to go.
The UI is pluggable, from the library.

To set a new UI for the app, go to the app/config.py file and
set the STATIC_FOLDER_PATH variable to the root of the
web application.
# Rii Shop Channel.
This is a revival of the now dead Wii Shop Channel.
Our goal is to make it look and work exactly how it did before Nintendo decided to pull the plug.
# Looks and features
The first time you load the RSC Server in PC mode (Non-HTTPS), You will see this page.
![](https://github.com/theDtubeTeam/WSC_SRVROOT/blob/main/image.png?raw=true)<br>
Looks pretty good, right!
# features
- Functional Gift system
- Wii Channels
- Virtual Console (Popular Titles)

# how to run
To run the server, You must install <a href="https://www.python.org/downloads/">Python</a> to run the app.<br>
Once <a href="https://www.python.org/downloads/">Python</a> is installed, open a terminal window (cmd.exe for windows), and do ``` pip install --upgrade pip ``` to update pip to it\'s latest version.<br>
Then run these commands to install Flask and Flask_babel.<br>
```
pip install flask
pip install flask_babel
```
# PC Mode \(Non-HTTPS\)
As we currently do not provide the WAD, You must change this line in ``` app.py ``` from
```python
app.run(host=socket.gethostbyname(socket.gethostname()), port=443, debug=True, ssl_context=context)
```
to
```python
app.run(host=socket.gethostbyname(socket.gethostname()), port=80, debug=True)
```
then you can run this command in a new terminal window to start the server.
```
py app.py
```
Open your web browser and navigate to the url specified from the output of app.py. Ex,
```
* Running on http://192.168.<>.<>:80
```

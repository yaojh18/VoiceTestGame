This is the backend of a WeChat App VoiceMaster. VoiceMaster is a platform where you can dub your favorite characters or movie clips.
To start the backend, run ```python manage.py runserver```.
# List of backend APIs
### Management Platform
#### Add to
- url: api/manager
- method: POST
- request: data content: {title (title), content (text), audio_path (audio file), video_path (video file), type_id (video type, 0 no gender, 1 male, 2 female)}
- response: success/failure information
#### Revise
- url: api/manager/<id> (<id> is the data id)
- method: PUT
- request: dict{title(title of modified data), content(text), audio_path(audio file), video_path(video file), type_id(video type)} \
    Note: All items are not required, if not filled, the backend will not modify the item
- response: success/failure information
#### Get the detailed information of a single piece of data (queried by id)
- url: api/manager/<id> (<id> is the data id)
- method: GET
- response: a piece of data corresponding to the requested id: dict{id(data id), level_id(level number), title(title), content(copy), audio_path(audio file url), video_path(video file url)type_id( video type)}
#### data query
- url: api/manager
- method: GET
- request: add ?param={} after the url to search, use & to connect the parameters, the parameters include:
    + level_id: level number
    + type_id: type number
    + title: title (keyword fuzzy search)
    + size: paging, the number of data on a page, if there is no item, the default is 20 on a page
    + page: the number of pages, no default is 1.
-response:
````
{
    "count": 3, #Total number of pages
    "next": null, #previous page link
    "previous": null, #Next page link
    "results": [ #List of dictionaries
        {
            "id": 3, #media id (you can use this to further query the detailed content)
            "level_id": 0, #level id
            "type_id": 2, #type id
            "title": "Big bowl of wide noodles" #title
        },
        {
            "id": 1,
            "level_id": 1,
            "type_id": 2,
            "title": "Big bowl of wide noodles"
        },
        {
            "id": 2,
            "level_id": 2,
            "type_id": 2,
            "title": "Big bowl of wide noodles"
        }
    ]
}
````
#### Change level order


#### Data analysis: audio and video data
##### List
- url: api/manager/data/origin
- method: GET
- request: add ?param={} after the url, the parameters include: \
    title: find by title\
    Pagination: size and page, same as in "Data List"
- response: dict{
    'id', 'level_id', 'title', \
    'played_num': the total number of games played in this level,
    'unknown_num': the number of games played by people of unknown gender,
    'male_num': number of male games,
    'female_num': number of female games, \
    'score_average': Average score for all player recordings,
    'unknown_score_average': Unknown gender average,
    'male_score_average': male average score,
    'female_score_average': female average score }
##### Visualization
###### Overall
- same as list url, all data that can be used for drawing are given in it
###### Single level
- url: api/manager/data/origin/<id>/chart (id is data id)
- method: GET
- response: dict{
    'id', 'level_id', 'title', \
    'played_num', 'unknown_num', 'male_num', 'female_num', \
    'score_average', 'unknown_score_average',
    'male_score_average', 'female_score_average', \
    'scores': list, the distribution of scores for this level,
    'unknown_scores': list, the distribution of the scores of people with unknown gender in this level,
    'male_scores': list, the distribution of male scores in this level,
    'female_scores': list, the distribution of female scores for this level }\
    Note: Each 'scores' item is divided into 0~10, 11~20,..., 91~100, a total of 10 sections
#### Data Analysis: User Data
##### List
- url: api/manager/data/user
- method: GET
- request: add ?param={} after the url, the parameters include: \
    sort: sort rule, optional 'level' gender: filter gender, no 0 male 1 female 2\
    Pagination: size and page, same as in "Data List"
- response: dict{'user': username, 'gender': gender, no 0 male 1 female 2, 'level': user game level}
##### Visualization
- url: api/manager/data/user/chart
- method: GET
- response: dict{
     'num': total number of users,
     'unknown_num': number of users of unknown gender,
     'male_num': the number of male users,
     'female_num': the number of female users,\
     'level_count': list, the number of users at each level, the level is continuous from 0, representing the number of levels that the user has passed }
#### Data Analysis: User Audio Data
##### List
- url: api/manager/data/user_audio
- method: GET
- request: add ?param={} after the url, the parameters include: \
    level: filter by level gender: filter by gender, no 0 male 1 female 2\
    start_time,end_time: filter by the upper and lower bounds of time, the value is represented by YYYY-MM-DD\
    sort: Available values ​​'score', 'level', 'time', which represent sorting by score, level, and time respectively
- response: dict{'user': username, 'level_id': level number, 'timestamp': recording time, 'score': score, 'audio': user recording audio url}
##### Visualization
##### Visualization
- url: api/manager/data/user_audio/chart
- method: GET
- response: dict{
    'num': total number of user recordings,
    'unknown_num': the number of recordings of users of unknown gender,
    'male_num': the number of male user recordings,
    'female_num': Number of female user recordings,\
    'time_count': list, the number of new recordings in each day with new recordings, the days without new recordings are ignored }

### Audio and video data: applet client
#### Return audio interface alone
- url: api/media/audio
- method: POST
- request: media_id (level id)
- response: audio file url
#### Return to video interface alone
- url: api/media/video
- method: POST
- request: media_id (level id)
- response: video file url
#### Return a single data title, copy
- url: api/media/material
- method: POST
- request: media_id (level id)
- response: dict{'title': title, 'text': text}
#### Level List
- url: api/media
- method: GET
- response: dict{'titles','score'} each item is a list

### User Management
#### Management platform user registration
- url: api/users/
- method: POST
- request: username, password, password_confirm, email(optional), name(optional)
- response: token (please put it in the Authorization of the header, the format is 'JWT'+'token', to access the following interface)
#### User information change
- url: api/users/
- method: PUT
- request: username, password (optional), password_old (required when changing the password), email (optional), name (optional)
- response: id, username, password, email, name
#### User information acquisition
- url: api/users/
- method: GET
- response: id, username, password, email, name (normal administrators get their own information, super administrators get all users' information)
#### User login
- url: api/users/login/
- method: POST
- request: username, password
- response: token

### WeChat Mini Program
#### User registration/login
- url: api/wechat/login/
- method: POST
- request: code (session_id returned by WeChat)
- response: token (please put it in the Authorization of the header, the format is 'JWT'+'token', to access the following interface)
#### User access to personal information
- url: api/wechat/
- method: GET
- response: nick_name, avatar_url, gender, city, province, user_id (can be used to access user information later)
#### User changes/enters personal information
- url: api/wechat/
- method: POST
- request: nick_name, avatar_url, gender, city, province (all required)
- response: nick_name, avatar_url, gender, city, province, user_id (can be used to access user information later)
#### User upload recording
- url: api/wechat/audio/
- method: POST
- content-type: multipart/form-data
- request: audio (audio), level_id (level number), type_id (gender)
- response: score (score) There is still a problem with the current score upload
#### Get the leaderboard of a level
- url: api/level/
- method: GET
- params: level_id, type_id (default is 0), lengh (list length, default is 5)
- response: list of dictionaries, each dictionary contains nick_name, avatar_url, user_id (available for subsequent queries), score
#### Get the highest score recording of a certain level of a user
- url: api/level/audio/
- method: GET
- params: level_id, type_id (default is 0), user_id (default is self)
- response: audio_url (audio URL)




#The work log part, the front end can be ignored.

# 2020.9.25 Sun Yutao
Added the WeChat applet front-end folder WeApp, deleted the default frontend (if the management platform is directly inherited, I will pull it back)

# 2020.9.25 Yao Jihan
## solved:
+ Half-completed CI/CD deployment and Dockerfile configuration, that is, gitlab-ci.yml configuration.
+ Complete database configuration and deployment.
+ pylint, the setting of style test, in fact, I have not set it, as long as pip installs pyhint and pylint_django, pythonNB! Remember to run pylint --load-plugins=pylint_django app game on the backend yourself before submitting, otherwise you will not be able to pass the style check. The front end is up to you.
+ The database uses mariadb, the local configuration refers to /app/setting.py, the Gitlab configuration refers to /config/local_settings.py, and the mariadb version is 10.5.5.
+ python toolkit version see requirements and requirements_dev, what is your version not enough? Hurry up to update (dog head, I am a version that is convenient for me to write, it is so overbearing)
+ Regarding the branch problem, please create your own branch on the dev branch. Please name it in the form of function-optional. Although I will be very happy that you merged the dev branch for me, but in order not to mess up the code, please also develop on your own branch, I will merge at a fixed time every week. Take special care not to merge the master branch.
+ After my merge is completed, please pull down the local merge for subsequent development, otherwise your local merge will definitely conflict.
+ Please submit your own issues as soon as possible.
## unsolved:
+ I haven't done the configuration STATIC_URL and STATICFILES_DIR of django static files, because I don't know how to do it in the front end, so I can put it first.
+ Unit detection, i.e. sonar-project.properties, has not been done yet. Anyway, it does not affect the normal project operation. I will add it tomorrow (today).
+ Front-end docker configuration, style check, I made corresponding comments in Dockerfile and .gitlab-ci.yml, please add them after confirming the architecture.

# 2020.9.27 Yao Jihan
+ The front-end configuration including unit testing has been completed, and the back-end is up to you. I have added a comment, which is very detailed.
+ Django's static files need to be added after determining the framework, not a must.
+ Put the junk files you don't want into .gitignore. I have to review this. I didn't do it well in the early stage and polluted everyone's warehouse.
+ It doesn't matter if the front end does not need frontend, just delete it. Please don't create front-end files in the root directory. You can put them in a folder like WeApp. Django has no dependencies on frontend, you only need to change those three files.
+ Write the initialization script in config/run.sh, such as database initialization, note that the carriage return in the Linux environment is '\n' instead of '\r\n', please use a professional text editor to edit.

# 2020.9.30 Yao Jihan
+ The user login interface on the web side is api/users/login, which only accepts the POST method. The parameters are in json format, and the username and password fields need to be included.
The return is in Json format, including code (200 is normal, the rest are errors), msg (error information), token (the token returned after successful verification, has not been implemented, and is currently empty)
+ The web-side user registration interface is api/users/registration, which only accepts the POST method. The parameter is in json format and needs to include username, password, password2 (authentication password), email (optional), name (optional).
The return is in Json format, including code (200 is normal, the rest are errors), msg (error information), token (the token returned after successful verification, has not been implemented, and is currently empty)

# 2020.10.1 Yao Jihan
Again, to emphasize the code specification:
+ Please put unnecessary files in .gitignore, do not pollute the repository. Please put the previous file in its own separate folder
+ Pay attention to the commit specification: if the interval between two consecutive submissions is less than 30 minutes, if a single submission exceeds 200 lines, and if the commit message does not exceed 20 characters, it will be invalid. Reducing the number of commits can also make our git log look better.
+ Please test the unit test and style detection (including the build test of the first build) locally before each final submission. The running command is the same as the dokcerfile. The inconvenience of testing on gitlab will also change our records. very bad.
+ After each update, you must write the ReadMe document in the format of this file, including the interface description and other content that you think belong to the document, so that we can write the final description document, and it is also convenient for other students to understand your interface.

# 2020.10.4 Sun Yutao
+ Configured some details of the CI/CD in the front end of the WeChat applet. Although there is nothing to write about the unit test, the structure at least has

# 2020.10.5 Li Moufan
### Audio and video data operations
! Deprecated
#### Add to
- url: api/manager/add
- request: data content: {title (title), content (text), audio_path (audio file), video_path (video file)}
- response: success/failure information
#### delete
- url: api/manager/delete
- request: media_id (level id to delete data)
- response: success/failure information
#### Revise
- url: api/manager/edit
- request: media_id (the level id of the data to be modified); title (the title of the modified data), content (copy), audio_path (audio file), video_path (video file)
- response: success/failure information
#### Inquire
- url: api/manager/search
- request: media_id (level id)
- response: data content: {title (title), content (text), audio_path (audio file url), video_path (video file url)}
- A small suggestion about the management platform: You can paste a url on the interface for the playback function, and click to jump to the corresponding url to play the video/audio online (for reference only, if you need an interface for downloading files, I will write another one)

# 2020.10.6 Yao Jihan
Added code specification:
+ The two students at the back end need to run python manage.py makemigrations after completing the modification of the database table structure. Please do not run this command for the students at the front end.
If you accidentally run it, please delete the generated migrations file. Back-end students cannot modify the database table structure of the other party.
+ All students can use python manage.py migrate to generate a local database for testing.

# 2020.10.6 Sun Yutao
WeChat login interface requirements:
+ After the WeChat applet runs, it will log in to obtain a login credential. I will POST this login credential, the JSON identifier is "code", and then I need a return value to identify the user's identity in the database backend (there is no user is recommended backend Automatic registration) (do not return the information directly provided by the WeChat API), the JSON identifier is "user_id", and then the front end will use this id to perform more user data operations.

# 2020.10.6 Zhang Shuning
- Completed the front-end login, registration, start, management interface UI writing of the management platform

- Implemented partial jumps between different interfaces

- Perform unit testing of all interfaces and some functions

# 2020. 10.8 Yao Jihan
+ Completed the login/registration for WeChat applet, the access method is /api/wechat/login, the data format is json, and the code item needs to be included as the session_id passed in from the front end.
The return value is in json format, including the status code, where 200 means success, if successful, it will return a token, otherwise it will return the error message msg
+ Deleted the front-end branch, and the project is completely independent as the back-end part, which is convenient for subsequent development and deployment

# 2020.10.14 Li Moufan
#### Return audio interface alone
- url: api/manager/audio
- request: media_id (level id)
- response: audio file url
#### Return to video interface alone
- url: api/manager/video
- request: media_id (level id)
- response: video file url
#### Return a single data title, copy
- url: api/manager/material
- request: media_id (level id)
- response: {'title': title, 'text': text}

# 2020.10.13 Yao Jihan
+ Token verification mechanism, the updated token verification mechanism is as follows:
    + Get the token after the front-end login, and then add in the header when accessing other APIs: {'Authorization' : 'JWT ' + token}, don't ask me, the built-in token verification is like this, I'm too lazy to write the format myself ;
    + The backend should restrict access except for the login and registration interface. The restriction method is permission_classes = [IsAuthenticated,], IsAuthenticated is in rest_framework.permissions, if it is written in the parameter, this authentication method is used for all sub-routes of the view set, otherwise it is also It can be added in the parameters of the action to verify a specific sub-route.
+ WeChat update user data interface: api/wechat/profile/, the accepted format is application/json, and the parameters include "nick_name", "city", "province", "gender", which are all required items.
+ WeChat upload user data interface: api/wechat/audio/, the accepted format is multipart/form-data, and the parameters include "media_id" (media ID), "audio" audio file, which are all required items.

# 2020.10.21 Li Moufan
#### Return audio and video data list
- url: api/manager/get_list
- method: get, no parameters required
- response: list[{'media_id','title'}]

# 2020.10.22 Yao Jihan
+ Fixed the bug that the database could not store Chinese
+ WeChat to get the highest score user list interface: api/level/, the accepted format is JSON, the method is GET, and the parameters include "media_id". Returned as a json list, each element contains 'user_id', 'nick_name', 'avatar_url', 'score'
+ WeChat obtains a list of the maximum rating of a user: api/level/audio, the accepted format is JSON, the method is GET, and the parameters include 'media_id', 'user_id' (the default is the currently logged-in user). Returned as json, containing 'audio_url'

# 2020.10.28 Li Moufan
Refactored audio and video database interface, see above for updated API

# 2020.10.28 Yao Jihan
+ When adjusting the structure of a database with foreign keys, you should first clear the contents of the corresponding database.
+ Refactored the query logic and optimized the query effect
+ Refactored the database to have better query performance
+ read the API documentation, but failed
+ Added the permission logic of the new interface

# 2020.11.4 Yao Jihan
+ Provides the structure of user change information, the interface is placed under api/users/, using the PUT method, the parameters include 'username', 'password', 'password_old', 'email', 'name', the latter two are optional
+ Updated the registration interface, placed it under api/users/, used the POST method, and renamed password2 to password_confirm
+ The interface for obtaining user information, obtain user information through get api/users/, use the GET method, log in to the super user to get everyone's information (a list of dictionaries), and log in users to get their own information (a dictionary), Returns empty without logging in.
+ Completed modeling of raw audio and scoring of user recordings.

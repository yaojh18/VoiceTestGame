# 后端API列表
### 管理平台
#### 添加
- url: api/manager
- method: POST
- request: 数据内容: {title(标题), content(文案), audio_path(音频文件), video_path(视频文件), type_id(视频类型，0无性别，1男，2女)}
- response: 成功/失败信息
#### 修改
- url: api/manager/<id> (<id>为数据id)
- method: PUT
- request: dict{title(修改后数据的title标题), content(文案), audio_path(音频文件), video_path(视频文件), type_id(视频类型)} \
    注：所有项都均非必须，若不填则后端不会修改该项
- response: 成功/失败信息
#### 单条数据查询(由id查询)
- url: api/manager/<id> (<id>为数据id)
- method: GET
- response: 请求的id对应的一条数据: dict{id(数据id), level_id(关卡号), title(标题), content(文案), audio_path(音频文件url), video_path(视频文件url)type_id(视频类型)}
#### 数据列表
- url: api/manager
- method: GET
- request: 在url后加?param={}进行查找, 参数之间使用&连接，参数包括：
    + level_id: 关卡号   
    + type_id: 类型号   
    + title: 标题（关键词模糊查找）
    + size: 分页，一页的数据条数，若没有此项默认一页20个
    + page: 页数，没有默认为1。
- response:
```
{
    "count": 3,                     #总页数
    "next": null,                   #上一页链接
    "previous": null,               #下一页链接
    "results": [                    #字典列表
        {
            "id": 3,                #媒体id（可以通过这个来进一步查询详细的内容）
            "level_id": 0,          #关卡id
            "type_id": 2,           #类型id
            "title": "大碗宽面"       #标题
        },
        {
            "id": 1,
            "level_id": 1,
            "type_id": 2,
            "title": "大碗宽面"
        },
        {
            "id": 2,
            "level_id": 2,
            "type_id": 2,
            "title": "大碗宽面"
        }
    ]
}
```
#### 数据分析：音视频数据
##### 列表
- url: api/manager/data/origin
- method: GET
- request: 在url后加?param={}, 参数包括：\
    title: 按标题查找\
    分页: size和page，与"数据列表"中相同
- response: dict{
    'id', 'level_id', 'title', \
    'played_num': 该关卡游戏总次数,
    'unknown_num': 不确定性别者游戏次数,
    'male_num': 男性游戏次数,  
    'female_num': 女性游戏次数, \
    'score_average': 所有玩家录音均分, 
    'unknown_score_average': 不确定性别者均分,
    'male_score_average': 男性均分,  
    'female_score_average': 女性均分 }
##### 可视化
###### 总体
- 与列表url相同，所有可以用于画图的数据均在其中给出
###### 单个关卡
- url: api/manager/data/origin/<id>/chart (id为数据id)
- method: GET
- response: dict{
    'id', 'level_id', 'title', \
    'played_num', 'unknown_num', 'male_num', 'female_num', \
    'score_average', 'unknown_score_average',
    'male_score_average', 'female_score_average', \
    'scores': list, 该关卡分数分布,
    'unknown_scores': list, 该关卡不确定性别者分数分布,
    'male_scores': list, 该关卡男性分数分布,
    'female_scores': list, 该关卡女性分数分布 }\
    注：各'scores’项分段均为0~10,11~20,...,91~100, 共10段
#### 数据分析：用户数据
##### 列表
- url: api/manager/data/user
- method: GET
- request: 在url后加?param={}, 参数包括：\
    sort: 排序规则，可选'level'    gender: 筛选性别，无0男1女2\
    分页: size和page，与"数据列表"中相同
- response: dict{'user': 用户名, 'gender': 性别，无0男1女2, 'level': 用户游戏等级}
##### 可视化
- url: api/manager/data/user/chart
- method: GET
- response: dict{
     'num': 用户总数,
     'unknown_num': 不确定性别用户数,
     'male_num': 男性用户数,
     'female_num': 女性用户数,\
     'level_count': list, 各等级用户数，等级从0开始连续，代表用户已通过关卡数 }
#### 数据分析：用户音频数据
##### 列表
- url: api/manager/data/user_audio
- method: GET
- request: 在url后加?param={}, 参数包括：\
    level: 按关卡筛选    gender: 按性别筛选，无0男1女2\
    start_time,end_time: 按时间上下界筛选，值用YYYY-MM-DD表示\
    sort: 可取值'score','level','time'，分别表示按分数、关卡、时间排序
- response: dict{'user':用户名,'level_id':关卡号,'timestamp':录制时间,'score':得分,'audio':用户录音音频url}
##### 可视化
##### 可视化
- url: api/manager/data/user_audio/chart
- method: GET
- response: dict{
    'num': 用户录音总数,
    'unknown_num': 不确定性别用户录音数,
    'male_num': 男性用户录音数,
    'female_num': 女性用户录音数,\
    'time_count': list, 存在新增录音的各天中新增录音数量，没有新增录音的日期被忽略 }

### 音视频数据：小程序客户端
#### 单独返回音频接口
- url: api/media/audio
- method: POST
- request: media_id(关卡id)
- response: 音频文件url
#### 单独返回视频接口
- url: api/media/video
- method: POST
- request: media_id(关卡id)
- response: 视频文件url
#### 返回单条数据标题、文案
- url: api/media/material
- method: POST
- request: media_id(关卡id)
- response: dict{'title': 标题, 'text': 文案}
#### 关卡列表
- url: api/media
- method: GET
- response: dict{'titles','score'} 每一项为一个列表

###用户管理
（未完待续）




#工作日志部分，前端可以不用看。

# 2020.9.25 孙宇涛
添加了微信小程序前端文件夹WeApp，删除了default的frontend（如果管理平台直接继承的话我再把它pull回来）

# 2020.9.25 姚季涵
## 已解决：
+ 半完成CI/CD的部署和Dockerfile的配置,即gitlab-ci.yml的配置。
+ 完成数据库配置和部署。
+ pylint,即style test的设置，其实我也没有设置，只要pip安装pyhint和pylint_django就可以了，pythonNB！后端记得自己运行一下pylint --load-plugins=pylint_django app game再提交，不然你可定过不了风格检测。前端你们自己定。
+ 数据库使用mariadb，本地配置参考/app/setting.py,Gitlab端配置参考/config/local_settings.py，mariadb版本为10.5.5。
+ python工具包版本见requirements和requirements_dev,什么你的版本不够？赶紧更新（狗头，我是方便自己写的版本，就是这么霸道）
+ 关于分支问题，请各位同学在dev分支上新建自己的分支，名字请以功能-随意的形式命名。虽然你替我代劳了merge dev分支我会很高兴，但是为了代码不混乱还请在自己的分支上开发，我会在每周固定的时间merge。特别注意，不要merge master分支。
+ 在我merge完成之后，请各位先pull下来本地merge在进行后续的开发，不然你本地merge一定会冲突。
+ 请各位大佬尽快提交自己的issue。
## 未解决：
+ django静态文件的配置STATIC_URL和STATICFILES_DIR我还没有做，因为我不知道前端要怎么做，可以先放一下。
+ 单元检测即sonar-project.properties还没有做，反正不影响正常项目运行，明天（今天）我会再加。
+ 前端的docker配置，风格检查，在Dockerfile和.gitlab-ci.yml中我做了相应的注释，在确定架构后请自行添加。

# 2020.9.27 姚季涵
+ 前端的配置包括单元测试已经全部完成了，后端看你们的了，我已经加了注释，很详细的。
+ django的静态文件需要确定框架后选择添加，不是必须项。
+ 把你不要的垃圾文件放到.gitignore中，这一点我要检讨，前期没有做好，污染了大家的仓库。
+ 前端不需要frontend也没有关系，删了就好。前端文件请不要创建在根目录下，可以像WeApp一样放在一个文件夹下,django对于frontend没有依赖项，只需要改那三个文件即可。
+ config/run.sh中写初始化脚本，如数据库初始化，注意linux环境回车是'\n'而不是'\r\n'，请使用专业的文本编辑器编辑。

# 2020.9.30 姚季涵
+ web端用户登录接口为api/users/login，只接受POST方法，参数为json格式，需要包含username和password字段。
返回为Json格式，包括code（200为正常，其余为错误），msg（错误信息），token（验证成功后返回的令牌，还没有实现，目前为空）
+ web端用户注册接口为api/users/registrtion，只接受POST方法，参数为json格式需要包含username，password，password2（验证密码），email（可选），name（可选）。
返回为Json格式，包括code（200为正常，其余为错误），msg（错误信息），token（验证成功后返回的令牌，还没有实现，目前为空）

# 2020.10.1 姚季涵
再次强调一下代码规范：
+ 请将不要的文件放在.gitignore中，不要污染仓库。前段文件请在自己单独的文件夹中
+ 注意commit的规范：连续两次提交之间少于30min的，单次提交超过200行的，commit message不超过20个字符的都无效。减少commit的次数，也能使我们的git log更好看。
+ 请在每次最终提交前，本地测试过单元测试和风格检测（包括第一次构建的build测试），运行的命令和dokcerfile是一样的，在gitlab上面测试不方便也会使我们的记录变得很糟。
+ 每次更新后必须按照本文件的格式写ReadMe文档，包括接口说明等你认为属于文档的内容，这样便于我们写最后的说明文档，也方便其他同学理解你的接口。

# 2020.10.4 孙宇涛
+ 配置了微信小程序前端的CI/CD的若干细节，虽然单元测试感觉没啥可写的，但是结构起码有了

# 2020.10.5 李侔繁
### 音视频数据操作
! 已弃用
#### 添加
- url: api/manager/add
- request: 数据内容: {title(标题), content(文案), audio_path(音频文件), video_path(视频文件)}
- response: 成功/失败信息
#### 删除
- url: api/manager/delete
- request: media_id(要删除数据的关卡id)
- response: 成功/失败信息
#### 修改
- url: api/manager/edit
- request: media_id(要修改数据的关卡id); title(修改后数据的title标题), content(文案), audio_path(音频文件), video_path(视频文件)
- response: 成功/失败信息
#### 查询
- url: api/manager/search
- request: media_id(关卡id)
- response: 数据内容：{title(标题), content(文案), audio_path(音频文件url), video_path(视频文件url)}
- 关于管理平台的小建议：回放功能可以在界面贴一个url, 点击跳转到相应url即可在线播放视频/音频(仅供参考, 如果需要可以下载文件的接口我就再写一个)

# 2020.10.6 姚季涵
新增代码规范：
+ 后端两位同学需要在完成数据库表结构的修改之后务必运行 python manage.py makemigrations，前端同学请不要运行这条指令，
如果有不小心运行了，请注意删除生成的migrations文件。后端同学不能修改对方的数据库表结构。
+ 所有同学都可以使用python manage.py migrate来生成本地数据库进行测试。

# 2020.10.6 孙宇涛
微信登录接口需求：
+ 微信小程序运行之后会登录获取一个登录凭证，我会POST这个登录凭证，JSON标识符为"code"，之后我需要一个返回值为数据库后台标识用户身份的信息（不存在用户是建议后端自动注册）（不要返回微信API直接提供的信息），JSON标识符为"user_id"，之后前端会利用这个id来进行更多的用户数据操作。

# 2020.10.6 张书宁
- 完成了管理平台前端登录，注册，开始，管理界面UI编写

- 实现了不同界面之间的部分跳转

- 进行所有界面，部分功能的单元测试

# 2020。10.8 姚季涵
+ 完成了对于微信小程序登录/注册的几口，访问方式为/api/wechat/login, 数据格式为json，需要包含code项为前端传入的session_id.
返回值为json格式，包括状态码code，其中200表示成功，若成功则会返回一个token， 否则返回错误信息msg
+ 删除了前端分支，项目完全独立为后端部分，方便之后的开发与部署

# 2020.10.14 李侔繁
#### 单独返回音频接口
- url: api/manager/audio
- request: media_id(关卡id)
- response: 音频文件url
#### 单独返回视频接口
- url: api/manager/video
- request: media_id(关卡id)
- response: 视频文件url
#### 返回单条数据标题、文案
- url: api/manager/material
- request: media_id(关卡id)
- response: {'title': 标题, 'text': 文案}

# 2020.10.13 姚季涵
+ token验证的机制，更新后的token验证机制如下：
    + 前端登录后获取token，之后在访问其他API的时候请在header中添加：{'Authorization' : 'JWT ' + token}, 别问我，自带的token验证就是这样的，我懒得自己写格式了；
    + 后端除了登录注册界面都应限制访问，限制方法为permission_classes = [IsAuthenticated,], IsAuthenticated在rest_framework.permissions中，如果写在参数里面就是对该视图集所有的子路由采用这个验证方法， 否则也可以在action的参数里面添加，特定对某个子路由进行验证。
+ 微信更新用户数据接口：api/wechat/profile/，接受格式为application/json，参数包括"nick_name”,"city","province","gender"，均为必须项。
+ 微信上传用户数据接口：api/wechat/audio/,接受格式为multipart/form-data,参数包括"media_id"(媒体编号),"audio"音频文件，均为必须项。

# 2020.10.21 李侔繁
#### 返回音视频数据列表
- url: api/manager/get_list
- method: get, 不需要参数
- response: list[{'media_id','title'}]

# 2020.10.22 姚季涵
+ 修复了数据库无法存储中文的bug
+ 微信获取最高分用户列表接口：api/level/，接受格式为JSON，方法为GET，参数包括“media_id"。返回为json列表，每个元素包含'user_id','nick_name','avatar_url','score'
+ 微信获取某用户某评分最大值列表：api/level/audio，接受格式为JSON，方法为GET，参数包括'media_id','user_id'(不提供默认为当前登录的用户)。返回为json，包含'audio_url'

# 2020.10.28 李侔繁
重构音视频数据库接口，更新后API见上方

# 2020.10.28 姚季涵
+ 在进行含外键的数据库的结构调整时首先应该清空相应数据库的内容。
+ 重构了查询逻辑，优化了查询效果
+ 重构了数据库，使之具有更好的查询效果
+ 阅读API文档，但是失败了
+ 补充了新增接口的权限逻辑

# 2020.11.4 姚季涵
+ 提供了用户更改信息的结构，接口放在api/users/下面，使用PUT方法，参数包括'username','password','password_old','email','name'，后两项可选
+ 更新了registration接口，放在api/users/下面，使用POST方法，password2更名为password_confirm
+ 获取用户信息的接口，通过get api/users/获取用户的信息，使用GET方法，登录超级用户可以获得所有人的信息（一个字典的列表），登录用户可以获得自己的信息（一个字典），不登录返回空。
+ 完成了对原始音频的建模和对用户录音的打分。

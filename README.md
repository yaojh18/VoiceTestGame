# init
 大概就是仿照monolithic-example做的，前端还是一片空白，表示我并不会加，同志们加油。
 两个requirements和requirements_dev版本号并不是最终版，这里只是简单的拷贝了一下。
 pytest没有加，因为我不知道有什么用，欢迎大佬解答。

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
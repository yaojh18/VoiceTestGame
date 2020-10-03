##后端App:音视频数据访问和操作
##API
###音视频数据操作
####添加
- url: api/manager/add
- request: 数据内容: {title(标题), content(文案), audio_file(音频文件), video_file(视频文件)}
- response: 成功/失败信息
####删除
- url: api/manager/delete
- request: 要删除数据的id
- response: 成功/失败信息
####修改
- url: api/manager/edit
- request: 要修改数据的id; 修改后数据的title(标题), content(文案), audio file(音频文件), video file(视频文件)
- response: 成功/失败信息
####查询(管理平台请求)
- url: api/manager/search
- request: 查询关键词
- response: 数据内容
####查询(客户端请求)
- url: api/manager/search
- request: 关卡id
- response: 数据内容
###用户数据操作
####添加
- url: api/client/add
- request: 数据内容: {user(音频所属用户), media_id(关卡id), audio_file(音频文件), score(该段音频得分)}
- response: 成功/失败信息
####查找
- url: api/client/search
- request: {user(所属用户), media_id(关卡id), query_type(查找条件)}
- response: 数据内容

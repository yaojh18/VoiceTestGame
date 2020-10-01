# First stage, build the frontend，前端的docker创建过程，请仿照下面的例子创建一个
#FROM node:12.18.3 基础镜像

#RUN npm config set registry https://registry.npm.taobao.org

#ENV FRONTEND=/opt/frontend 变量命名方式

#WORKDIR $FRONTEND 文件目录，统一为opt/下！

#COPY frontend/package.json $FRONTEND
#COPY frontend/package-lock.json $FRONTEND 文件拷贝
#RUN npm install 安装依赖项，类似于python的包，上面两个文件应该是安装包需要的文件

#COPY frontend/ $FRONTEND 拷贝全部文件
#RUN npm run build 不知~，可能是npm特有的

# Second stage for the backend
FROM python:3.8.5

ENV HOME=/opt/app

WORKDIR $HOME

COPY requirements.txt $HOME
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . $HOME

EXPOSE 80

ENV PYTHONUNBUFFERED=true
CMD ["/bin/sh", "/opt/app/config/run.sh"]
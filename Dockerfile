
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
FROM python:3.12.11-alpine3.22

ENV APP_VERSION='1.0.0'

COPY src/* /app

WORKDIR /app

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

# 容器内 9527 端口开放服务
EXPOSE 9527

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:9527", "app:app"]

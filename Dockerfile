FROM nginx:1.27-bookworm

RUN apt update && apt install -y python3 python3-pip

RUN sed -i 's/\s*index\s*index.html\sindex.htm;/        autoindex         on;/'  /etc/nginx/conf.d/default.conf
RUN sed -i 's/        root   \/usr\/share\/nginx\/html;/        root   \/usr\/share\/nginx\/html\/reconic\/output;/' /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html/reconic

RUN mkdir output

COPY . .

RUN python3 -m pip install -r requirements.txt --break-system-packages


FROM nginx:1.29.3

EXPOSE 80
EXPOSE 443

COPY ./nginx/staging.conf.d/default.conf /etc/nginx/nginx.conf
# COPY ./html /usr/share/nginx/html/

CMD ["nginx", "-g", "daemon off;"]

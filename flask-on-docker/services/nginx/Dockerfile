FROM nginx:1.19-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY cert.crt /etc/nginx/
COPY cert.key /etc/nginx/
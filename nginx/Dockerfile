FROM nginx

WORKDIR /etc/nginx/conf.d
# RUN cp nginx.conf ./nginx.conf.bak
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY dist /app/dist

CMD ["nginx", "-g", "daemon off;"]
FROM debian:13.5

RUN apt-get update && apt-get install -y nginx git

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

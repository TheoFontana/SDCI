# syntax=docker/dockerfile:1
FROM node:18-alpine
RUN mkdir /metadata_server
WORKDIR /metadata_server
ADD metadata_server.js /metadata_server
ADD config.json /metadata_server
RUN npm install express
CMD ["node","metadata_server.js"]
EXPOSE 8080
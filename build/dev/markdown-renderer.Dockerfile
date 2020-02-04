FROM node:10.15.3
COPY ./markdown-renderer/ /app/
WORKDIR /app/
RUN npm install
ENTRYPOINT npm start
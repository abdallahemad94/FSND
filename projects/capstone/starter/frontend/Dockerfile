FROM node
RUN npm i @angular/cli@10.0.7
COPY ./frontend /app/casting/frontend
WORKDIR /app/casting/frontend
RUN npm install
ENTRYPOINT npm run serve
EXPOSE 4200

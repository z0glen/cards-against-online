FROM node:12-stretch

RUN npm install -g @vue/cli

WORKDIR usr/src/app
COPY ./package*.json ./
RUN npm install
RUN npm rebuild node-sass
COPY . .
ENV VUE_APP_FLASK_HOST flask
ENV HOST 0.0.0.0
EXPOSE 8080
CMD ["npm", "run", "serve"]
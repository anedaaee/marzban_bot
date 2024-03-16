FROM node:18

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

ENV DB_HOST=167.99.248.242
ENV DB_PORT=3002

EXPOSE 3001

WORKDIR /usr/src/app/src

CMD ["node","index"]

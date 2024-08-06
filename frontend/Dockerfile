FROM node:20.16.0-alpine

WORKDIR /workdir/frontend

COPY package.json package-lock.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
FROM node:20.16.0-alpine AS builder

WORKDIR /workdir/frontend

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]

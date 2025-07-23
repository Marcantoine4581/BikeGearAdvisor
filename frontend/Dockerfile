FROM node:22-alpine

WORKDIR /app

COPY package*.json .

RUN npm install

# Expose le port Vite
EXPOSE 5173

COPY . .

CMD ["npm", "run", "dev"]
### Stage 1: build ###

FROM node:14.17.4-alpine as builder

# Set working directory.
RUN mkdir /app
WORKDIR /app

# Copy app dependencies.
COPY frontend-app/package.json frontend-app/package-lock.json /app/frontend-app/

# Install app dependencies.
RUN npm install --prefix frontend-app

# Copy app files.
COPY . /app

# Build app
RUN npm run build --prefix frontend-app -- --output-path=./dist/out

### Stage 2: delivery ###

FROM nginx:1.15.7-alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy output directory from builder to nginx image.
COPY --from=builder /app/frontend-app/dist/out /usr/share/nginx/html

# Copy nginx configuration file.
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
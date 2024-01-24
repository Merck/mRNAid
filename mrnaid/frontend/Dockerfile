FROM node:16 as builder
COPY ./ /frontend/
WORKDIR /frontend
RUN npm ci && npm run build

FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY config/nginx.conf /etc/nginx/conf.d/
COPY --from=builder /frontend/build /usr/share/nginx/html

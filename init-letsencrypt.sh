#!/bin/bash
                                                                                                                                                                                              
domains=(api-propinvest.forgehive.ru forgehive.ru)
rsa_key_size=4096
data_path="./proxy/certbot"
email=""
staging=0 # Set to 1 if you're testing your setup to avoid hitting request limits
                                                                                                                                                                                              
if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
  echo "### Downloading recommended TLS parameters ..."
  mkdir -p "$data_path/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"
  echo
fi
                                                                                                                                                                                              
echo "### Creating dummy certificate for $domains ..."
for domain in "${domains[@]}"; do
  path="/etc/letsencrypt/live/$domain"
  mkdir -p "$data_path/conf/live/$domain"
  docker compose run --rm --entrypoint "\
    openssl req -x509 -nodes -newkey rsa:1024 -days 1 \
      -keyout '$path/privkey.pem' \
      -out '$path/fullchain.pem' \
      -subj '/CN=localhost'" certbot
done
echo
                                                                                                                                                                                              
                                                                                                                                                                                              
echo "### Starting nginx ..."
docker compose up -d --force-recreate proxy
echo
                                                                                                                                                                                              
echo "### Deleting dummy certificate for $domains ..."
for domain in "${domains[@]}"; do
  docker compose run --rm --entrypoint "\
    rm -Rf /etc/letsencrypt/live/$domain && \
    rm -Rf /etc/letsencrypt/archive/$domain && \
    rm -Rf /etc/letsencrypt/renewal/$domain.conf" certbot
done
echo
                                                                                                                                                                                              
                                                                                                                                                                                              
echo "### Requesting Let's Encrypt certificate for $domains ..."
                                                                                                                                                                                              
case "$email" in
  "") email_arg="--register-unsafely-without-email" ;;
  *) email_arg="--email $email" ;;
esac
                                                                                                                                                                                              
if [ $staging != "0" ]; then staging_arg="--staging"; fi
                                                                                                                                                                                              
for domain in "${domains[@]}"; do
  docker compose run --rm --entrypoint "\
    certbot certonly --webroot -w /srv/certbot \
      $staging_arg \
      $email_arg \
      -d $domain \
      --rsa-key-size $rsa_key_size \
      --agree-tos \
      --force-renewal -v" certbot
done
echo
                                                                                                                                                                                              
echo "### Reloading nginx ..."
docker compose up -d --force-recreate proxy

echo "Pulling fresh changes from GitHub"
git pull

echo "Restarting daemon, gunicorn, nginx and socket"
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart gunicorn.socket
sudo nginx -t && sudo systemctl restart nginx

echo "Complete"

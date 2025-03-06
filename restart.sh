echo "Pulling fresh changes from GitHub"
git pull

read -p "Do you want to restart gunicorn? It belongs to the Django setup, so ost likely not [y/n]:" confirm
if [[ $confirm == [yY] ]]; then
    echo "Restarting daemon, gunicorn, nginx and socket"
    sudo systemctl daemon-reload
    sudo systemctl restart gunicorn
    sudo systemctl restart gunicorn.socket
else
    echo "Skipping gunicorn restart"
fi

sudo nginx -t && sudo systemctl restart nginx
echo "Complete"

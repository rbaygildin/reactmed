su -
/etc/init.d/nginx restart
source ../reactmed/venv/bin/activate
nohup uwsgi --ini ../reactmed/reactmed.ini &

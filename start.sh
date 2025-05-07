/usr/sbin/sshd -D &
sleep 15
python3 /app/setup.py

cp token.txt /etc/token.txt

python3 /app/executer/detector.py
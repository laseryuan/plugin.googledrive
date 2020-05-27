
```
  -v /home/laser/Videos/:/home/kodi/Videos/ `# mount video library`\
  -v kodi-config:/home/kodi/.kodi/userdata `# persist kodi configuration`\
  -v kodi-addons:/home/kodi/.kodi/addons/ `# persist kodi addon dependencies`\
  -v $(pwd)/:/home/kodi/.kodi/addons/my-addon/ `# mount the addon; needs to be enabled in kodi config`\

docker run -it --rm --name=kodi \
  --privileged \
  -e DISPLAY=unix:0 -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e PULSE_SERVER=unix:/run/user/1000/pulse/native -v /run/user/1000:/run/user/1000 \
  -v /var/run/dbus/:/var/run/dbus/ \
  lasery/codebench:kodi \
  bash

cat /home/kodi/.kodi/temp/kodi.log
```

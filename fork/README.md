```

docker run -it --rm --name=kodi \
  --privileged \
  -e DISPLAY=unix:0 -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e PULSE_SERVER=unix:/run/user/1000/pulse/native -v /run/user/1000:/run/user/1000 \
  -v /var/run/dbus/:/var/run/dbus/ \
  lasery/codebench:kodi \
  bash

cat /home/kodi/.kodi/temp/kodi.log
```

Development
```
cd ~/projects/kodi/plugin.googledrive

docker run -it --rm --name=kodi \
  --privileged \
  -e DISPLAY=unix:0 -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e PULSE_SERVER=unix:/run/user/1000/pulse/native -v /run/user/1000:/run/user/1000 \
  -v /var/run/dbus/:/var/run/dbus/ \
  -v /home/laser/Videos/:/home/kodi/Videos/ `# mount video library`\
  -v kodi-config:/home/kodi/.kodi/userdata `# persist kodi configuration`\
  -v kodi-addons:/home/kodi/.kodi/addons/ `# persist kodi addon dependencies`\
  -v $(pwd)/:/home/kodi/.kodi/addons/plugin.googledrive/ `# mount the addon; needs to be enabled in kodi config`\
  -v $(pwd)/fork/script.module.clouddrive.common:/home/kodi/.kodi/addons/script.module.clouddrive.common/ `# mount the dependency addon`\
  lasery/codebench:kodi \
  bash

cd ~/.kodi/addons/plugin.googledrive/
python fork/tests.py
python fork/tests.py GDriveAddonTestCase.test_gdrive_process_files
python fork/tests.py GDriveAddonTestCase.test_check_google_ban
python fork/tests.py GDriveAddonTestCase.test_delete_file
cat /home/kodi/.kodi/temp/kodi.log
```


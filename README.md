# Raspberry Pi2 での設定Tips

## Raspberry Pi2への接続方法

基本的には **SSHを使用しての接続** になります．Windows([TeraTerm](http://ttssh2.osdn.jp)など)，Mac(Terminal)ともに接続可能です．接続コマンドは以下のようになります．

```
ssh pi@[hostname].local
```

**[hostname]の部分にはRaspberry PiのHost名が入ります．** その後，パスワードを求められるので，適切なパスワードを入れてください．接続が成功すると，以下のような感じになります．

```
MBP-2: $ ssh pi@hci1.local
pi@hci1.local's password:

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Feb 11 12:33:39 2017
pi@hci1:~ $
```

## RTCモジュールの設定方法

RTCモジュールはネット環境に繋がっていなくても，一定の時刻を保つために使用します．そのためには，**RaspberryPi起動時に，自動的にRTCモジュールの時刻を読み込む必要があります．**

### Raspberry Pi上での確認方法

以下のコマンドを打つことで動作確認ができます．

```
  sudo modprobe -c | grep 3231
  sudo modprobe rtc-ds3232
  echo ds3231 0x68 | sudo tee /sys/class/i2c-adapter/i2c-1/new_device
  pi@hci1:~ $ sudo hwclock -r
  2017年02月17日 04時45分21秒  -0.946369 seconds
```

### 起動時に自動で同期する設定方法

RaspberryPiの自動起動スクリプトに以下のコードを追加してください．

```
sudo vi /etc/rc.local
```

```shell
/etc/rc.local
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

#---------------------------追加部分---------------------------
echo ds3231 0x68 | sudo tee /sys/class/i2c-adapter/i2c-1/new_device
sudo hwclock -s
#-------------------------------------------------------------

exit 0
```

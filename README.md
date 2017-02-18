# Raspberry Pi2 での設定Tips

## インストール

```
cd
git clone git://github.com/shomitarai/MCPsensor
```

## 接続方法

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

## 事前準備

以下のコマンドでpythonのライブラリ「spidev」を導入してください．

```terminal
cd
sudo apt-get install python2.7-dev
git clone git://github.com/doceme/py-spidev
cd py-spidev
sudo python setup.py install
```

## RTCモジュール

RTCモジュールはネット環境に繋がっていなくても，一定の時刻を保つために使用します．そのためには，**RaspberryPi起動時に，自動的にRTCモジュールの時刻を読み込む必要があります．**

### RaspberryPiの時刻を確認

```
timedatectl status
```

### RTCモジュールの時刻を確認

以下のコマンドを打つことでRTCモジュール内の時刻を確認することができます．

```
sudo modprobe -c | grep 3231
sudo modprobe rtc-ds3232
echo ds3231 0x68 | sudo tee /sys/class/i2c-adapter/i2c-1/new_device
sudo hwclock -r
>> 2017年02月17日 04時45分21秒  -0.946369 seconds
```

### RTCモジュールへ時刻を書き込み

RTCモジュール内に正しい時刻を書き込む必要があります．RaspberryPiをインターネットに接続して，正しい時刻に同期されているか確認しましょう．時刻の確認は以下のように行うことができます．

```
sudo hwclock -w
```

### 起動時に自動で同期する設定

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

書き込みが終わったら，`sudo reboot`で再起動し，時刻を確認します．

```
timedatectl status

Local time: 金 2017-02-17 10:02:22 UTC
Universal time: 金 2017-02-17 10:02:22 UTC
RTC time: 金 2017-02-17 10:02:22
Time zone: Etc/UTC (UTC, +0000)
NTP enabled: no
NTP synchronized: no
RTC in local TZ: no
DST active: n/a
```

# #

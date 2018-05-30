# README

## GET WXAPKG

1. Lanuch WeChat on your android phone, then click the wechat mini games one by one. You can use `adb shell input` tap / keyevent "KEYCODE_BACK" / swipe to make these jobs autmoatically. When you successfully launch the mini games, they will save a .wxapkg on your mobile phone.

2. Root this android phone.

3. Copy the .wxapkg fiels into sdcard from data folder

For example:
```
$ adb shell
$ su
$ mount -o remount,rw /data
$ mkdir /mnt/sdcard/wxapkg
$ cp /data/data/com.tencent.mm/MicroMsg/{User}/appbrand/pkg/*.wxapkg /mnt/sdcard/wxapkg/
$ exit  // quit su mode
$ exit  // quit the shell, and back to your mac
$ adb pull /mnt/sdcard/wxapkg ./
```

Now you will have all packages of wechat mini games on you ./wxapkg folder

## THE SCRIPT

1. Preconditions:

  - Python 2.7 is required.
  - Tested on my Mac, but havn't tested on Windows and Linux.

2. By default, the program will use "./wxapkg" as the target path

  For example, you put all .wxapkgs in `{current_path}/game-engine-detector/wxapkg`, then you can just run `python main.py` to detect them.

3. Run with a target path `python main.py {path_to_wxapkgs}`

  For example, `python main.py ~/my_folder/wxapkgs` to get the results.

## RESULT at 2018-05-30

I can see more than 600 wechat mini games in my "Playing by Friends" by today. But unluckly, the games below 550+ are very unstable and have high probility to crash. No only the mini games crash, but also the list of mini games crash out.

So finally, my test team clicked about 560 mini games, and only got 509 volid wxapkgs. After ran this script, the result is:

- total = 509
- cocos = 253, percentage = 49.71%
- egret = 128, percentage = 25.15%
- laya = 94,   percentage = 18.47%
- others = 34, percentage = 6.68%

It's important to be honest.

This script can insert the results generated by [HSR-Scanner](https://github.com/kel-z/HSR-Scanner) into Lunarcore's mongodb database.
That is, copying your character, light cone, and relic information into the server may help you get more intuitive insights during the test.

How to Use:

(1) Install dependencies

(2) Create a new user and obtain its UID

(3) Modify the database configuration in the file, the path of the UID and HSRScanData file path

(4) Run the script

Recommend Python Version: 3.11

Shortcoming:

(1) Due to the storage method of the Pioneer's data, its traces and eidolon information cannot be copied.

(2) The code sucks and takes a bit of time to run

(3) For SPD, because the decimal point is not displayed in game, OCR cannot be recognized, so it will be a little smaller than the actual one

Although there is no problem on my computer, don't forget to **back up your database**.！


这个脚本可以将[HSR-Scanner](https://github.com/kel-z/HSR-Scanner)生成的结果插入到lunarcore的mongodb数据库中，
也就是复制你的角色、光锥、遗器信息到server里面，或许可以帮助你在测试中获取更直观的见解。

使用方法:

①安装依赖

②新建一个用户并获取其UID

③修改文件中的数据库配置，UID和HSRScanData文件的路径

④运行脚本

推荐在Python 3.11下运行

缺点：

①由于开拓者数据的储存方式，其行迹和星魂信息尚不能复制。

②代码很烂，并需要一点时间运行

③对于速度词条，由于不显示小数点，ocr识别不到，所以会比实际上的小一点


虽然在我的电脑上没有问题，但不要忘记**备份你的数据库**！

# 亿海蓝-船讯网-sdk
[亿海蓝官网](https://www.shipxy.com/)&nbsp;&nbsp;
[API控制台](https://api.shipxy.com/v3/console/index)&nbsp;&nbsp;
[在线开发文档](https://hiiau7lsqq.feishu.cn/wiki/E0wAwrPpvieGhSk5wLCctNqonVb)&nbsp;&nbsp;
[github](https://github.com/shipxycom/shipxy-api-py)&nbsp;&nbsp;
[gitee](https://gitee.com/shipxycom/shipxy-api-py)&nbsp;&nbsp;
[pypi](https://pypi.org/project/shipxy-api/)&nbsp;&nbsp;

## 示例用法
```
pip install shipxy-api
```
```
from shipxy import Shipxy

key = "请从 API控制台 申请";

if __name__ == '__main__':
    response = Shipxy.GetManyShip(key, "413961925,477232800,477172700")
    print(response)
```
## 开发者在使用过程中如有疑问，可以通过以下方式联系船讯网：

• 商务邮箱：support@shipxy.com

• 技术支持邮箱：service@shipxy.com

• 电话：400-010-8558 

![飞书](./images/飞书.jpg)
![微信](./images/微信.jpg)
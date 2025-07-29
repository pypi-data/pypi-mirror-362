<div align="center">

<img src="https://free.picui.cn/free/2025/07/04/6867ef499899c.png" alt="logo" width="200" height="200">

# AntiCAP

<strong>Version:3.0.1</strong>

<strong>多类型验证码识别，开源学习项目，不承担法律责任。</strong>

| 类型         | 状态 | 描述                                    |
|------------|-|---------------------------------------|
| `OCR识别`    |✅| 返回图片字符串                               |
| `数学计算`     |✅| 返回计算结果                                |
| `缺口滑块`     |✅| 返回坐标                                  |
| `阴影滑块`     |✅| 返回坐标                                  |
| `图标点选`     |✅| 侦测图标位置 或 按序返回坐标                       |
| `文字点选`     |✅| 侦测文字位置 或 按序返回坐标                       |
| `相似对比`     |✅| 图片中文字的相似度对比                           |
| `WebApi服务` | ✅ | https://github.com/81NewArk/AntiCAP-WebApi |


</div>


<br>

<div align="center">

# 📄 AntiCAP 文档

</div>

## 🌍环境说明

```
python 3.8+
```

## 📁 安装

###  方案一 下载源码
```
git clone https://github.com/81NewArk/AntiCAP.git
cd AntiCAP
pip install -r requirements.txt 
```


###  方案二 Pypi下载
```
pip install AntiCAP -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 🤖 调用

```
import AntiCAP


if __name__ == '__main__':
    # 初始化
    Atc = AntiCAP.AntiCAP()

    # 文字类验证码 字母 数字 汉字
    result = Atc.OCR(img_base64="")

    # 算术类验证码
    result = Atc.Math(img_base64="")

    # 图标点选侦测
    result = Atc.Detection_Icon(img_base64="")

    # 图标点选 按序输出
    result = Atc.ClickIcon_Order(order_img_base64="",target_img_base64="")

    # 汉字侦测
    result = Atc.Detection_Text(img_base64="")

    # 文字点选 按序输出
    result = Atc.ClickText_Order(order_img_base64="",target_img_base64="")

    # 缺口滑块
    result = Atc.Slider_Match(target_base64="",background_base64="")

    # 阴影滑块
    result = Atc.Slider_Comparison(target_base64="",background_base64="")
    
    # 图像相似度对比  对比图片中的文字
    result= Atc.compare_image_similarity(image1_base64="", image2_base64="")

    # 输出结果
    print(result)
  ```

# 🐧 QQ交流群

<br>

<div align="center">

<img src="https://free.picui.cn/free/2025/07/04/6867f1907d1a0.png" alt="QQGroup" width="200" height="200">

</div>

# 🚬 请作者抽一包香香软软的利群
<br>

<div align="center">

<img src="https://free.picui.cn/free/2025/07/04/6867efd0bd67e.png" alt="Ali" width="200" height="200">
<img src="https://free.picui.cn/free/2025/07/04/6867efd0d7cbb.png" alt="Wx" width="200" height="200">

</div>

<br>

# 💪🏼 模型训练

<br>

<div align="center">

<img src="https://free.picui.cn/free/2025/07/04/6867f0684ff6e.png" width="200" height="200">

<strong>https://github.com/81NewArk/AntiCAP_trainer</strong>

根据自身要求训练模型 无缝衔接下一个 下一个更乖。

</div>

# 😚 致谢名单


<strong>这份荣光我不会独享</strong>


[1] Ddddocr作者 网名:sml2h3


[2] 微信公众号 OneByOne 网名:十一姐


[3] 苏州大学,苏州大学文正学院 计算机科学与技术学院 张文哲教授


[4] 苏州大学,苏州大学文正学院 计算机科学与技术学院 王辉教授


[5] 苏州市职业大学,苏州大学文正学院 计算机科学与技术学院 陆公正副教授


[6] 武汉科锐软件安全教育机构 钱林松讲师 网名:Backer



# 📚 参考文献

[1] Github. 2025.03.28 https://github.com/sml2h3


[2] Github. 2025.03.28 https://github.com/2833844911/


[3] Bilibili. 2025.03.28 https://space.bilibili.com/308704191


[4] Bilibili. 2025.03.28 https://space.bilibili.com/472467171


[5] Ultralytics. 2025.03.28 https://docs.ultralytics.com/modes/train/


[6] YRL's Blog. 2025.03.28 https://blog.2zxz.com/archives/icondetection




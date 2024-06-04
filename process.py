from PIL import Image


# 打开图片文件
path=r"D:\根的数据\根系分析\八角枫2.jpg"
image = Image.open(path)

# 1. 将图片转换为灰度图像
gray_image = image.convert('L')

# 2. 进行二值化处理
threshold = 235  # 设定阈值
binary_image = gray_image.point(lambda p: 0 if p < threshold else 255)

# 保存二值化后的图片
binary_image.save('binary_image.jpg')

# 显示二值化后的图片
binary_image.show()

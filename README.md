1. 先用moyu哥的mask代码实现全黑mask
2. 处理masked_img, 找出全黑像素的轮廓
3. 将轮廓写入json, label设置为ignore
4. 标注同学给到的json和此ignore_json合并, 即可输入train model. : merge_defect_and_masked_json()

5. exp.yaml中注意masked这个label设置为ignore即可顺利使用~.

6.另外再根据moyu哥的c++脚本输出物料的4个角点, 可用作cut大原图的roi坐标. : roi_cut_img_and_json()



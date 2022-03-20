# coding=utf-8
import os
import cv2
# from PIL import Image
import numpy as np
import json
from debug import help


def tmp_info(tmp):
    # {
#     "label": "bianxing",
#       "points": [
#         [point1,point2..]
#       ],
#       "group_id": null,
#       "shape_type": "polygon",
#       "flags": {}
#     },
    tmp["flags"] = dict()
    tmp["shape_type"] = "polygon"
    tmp["group_id"] = None
    tmp["label"] = "masked"



def merge_defect_and_masked_json(masked_img_path, json_file):
    masked_points = []
    points_lens = []
    colors = [(0,0,255), (0,255,255), (255,0,255), (255,0,0), (0,255,0), (0,128,128)]

    # 标注同学给到的缺陷的标注json
    defect_json = json.load(open(json_file, 'r'))

    img = cv2.imread(masked_img_path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray,0,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for ind, contour in enumerate(contours):
        cv2.drawContours(img,contour,-1,colors[ind],3)
        contour = np.squeeze(np.array(contour)).tolist()
        masked_points.append(contour)
        points_lens.append(len(contour))

    # 把最外面的大轮廓剔除
    max_index = points_lens.index(max(points_lens))
    masked_points.pop(max_index)

    # masked_points写入json作为后续的ignore_label
    for points in masked_points:
        tmp = dict()
        tmp_info(tmp)
        tmp["points"] = points
        print(len(points))
        defect_json["shapes"].append(tmp)

    json_str = json.dumps(defect_json, indent=4)
    json_file1 = os.path.join(os.path.dirname(json_file), '1.json')
    print(json_file1)
    with open(json_file1, 'w') as jss:
        jss.write(json_str)



def roi_cut_img_and_json(base_dir, corner_txts, out_dir):

    # 处理后的得到的1.json, 和未经任何处理的原图1.png. 进行img_and_json roi cut.
    # roi可从moyu哥的c++代码中获取, 我将物料的4个角点写入txt了
    lines = open(corner_txts).readlines()
    lines = [a for a in lines if len(a) > 1]
    # 我只写入了一行, exp一下:
    points = [int(p) for p in lines[0].split('||')[1].split(',')[:-1]]
    roi = (points[6], points[7], points[2], points[3])
    split_target = (1, 1)
    # out_dir在help()中会被创建
    help(base_dir, roi, split_target, out_dir)



if __name__ == "__main__":

    # 1.
    masked_img_path = '/Users/chenjia/Downloads/20220308/HeBi-Graphite-Location/gw1_cut/1.png_result.png'
    json_file = '/Users/chenjia/Downloads/20220308/HeBi-Graphite-Location/gw1_cut/org_img_and_json/org.json'
    merge_defect_and_masked_json(masked_img_path, json_file)

    # 2.
    corner_txts = '/Users/chenjia/Downloads/20220308/HeBi-Graphite-Location/gw1_cut/roi_points.txt'
    base_dir = '/Users/chenjia/Downloads/20220308/HeBi-Graphite-Location/gw1_cut/org_img_and_json'
    out_dir = os.path.join(base_dir, 'roi_cuted')
    roi_cut_img_and_json(base_dir, corner_txts, out_dir)






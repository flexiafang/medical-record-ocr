import base64
import json
import os
import sys
import time

import requests
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QProgressBar

from request import getAuth
from ui_MainWindow import Ui_MainWindow


class MedicalRecordOcr(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MedicalRecordOcr, self).__init__()
        self.setupUi(self)

        # 绑定槽函数
        self.imgSubmitButton.clicked.connect(self.imgUpload)
        self.imgSubmitButton.clicked.connect(self.convert)

    # 上传图片
    def imgUpload(self):
        img = QImage()
        path = QFileDialog.getOpenFileName(self, '选择图片', 'pic/src/', '*.jpg *.png *.gif *.jpeg')[0]
        # print(path)
        img.load(path)
        # 图片大小调整
        # print(self.imgLabel.size())
        fixedImg = img.scaled(self.imgLabel.size(), Qt.KeepAspectRatioByExpanding)
        self.imgLabel.setScaledContents(True)
        self.imgLabel.setPixmap(QPixmap.fromImage(fixedImg))

    # 图片转文字
    def convert(self):
        # content = self.ocr('G:/CBIB/medical-record-ocr/pic/src/test.jpg')
        content = self.ocr('pic/src/test.jpg')
        # print(content)

        self.nameLineEdit.setText(content[0])
        self.sexLineEdit.setText(content[1])
        self.ageLineEdit.setText(content[2])
        self.cardNumberLineEdit.setText(content[3])
        self.departmentLineEdit.setText(content[4])
        self.typeLineEdit.setText(content[5])
        self.timeLineEdit.setText(content[6])
        self.mainDemandsLineEdit.setText(content[7])
        self.presentIllnessLineEdit.setText(content[8])
        self.previousIllnessLineEdit.setText(content[9])
        self.allergyLineEdit.setText(content[10])
        self.examinationLineEdit.setText(content[11])
        self.diagnosisLineEdit.setText(content[12])
        self.treatmentTextEdit.setText(content[13])

    # 识别文件
    @staticmethod
    def ocr(filepath):
        identification_results = []
        img = Image.open(filepath)
        basicpath = 'pic/tmp/'
        if not os.path.exists(basicpath):
            try:
                os.mkdir(basicpath)
            except Exception:
                print('tmp文件夹创建失败')

        # crop里对应的数值为该位置图像在整体图片中左上和右下两个点的像素坐标
        cropped1 = img.crop((470, 440, 700, 520))
        cropped1.save(basicpath + '1.png')
        cropped2 = img.crop((1125, 425, 1200, 500))
        cropped2.save(basicpath + '2.png')
        cropped3 = img.crop((1435, 410, 1590, 500))
        cropped3.save(basicpath + '3.png')
        cropped4 = img.crop((2100, 380, 2450, 470))
        cropped4.save(basicpath + '4.png')
        cropped5 = img.crop((460, 520, 830, 600))
        cropped5.save(basicpath + '5.png')
        cropped6 = img.crop((1140, 500, 1500, 575))
        cropped6.save(basicpath + '6.png')
        cropped7 = img.crop((2110, 480, 2500, 545))
        cropped7.save(basicpath + '7.png')
        cropped8 = img.crop((470, 605, 2780, 675))
        cropped8.save(basicpath + '8.png')
        cropped9 = img.crop((530, 680, 2780, 780))
        cropped9.save(basicpath + '9.png')
        cropped10 = img.crop((510, 800, 2740, 890))
        cropped10.save(basicpath + '10.png')
        cropped11 = img.crop((510, 900, 2740, 990))
        cropped11.save(basicpath + '11.png')
        cropped12 = img.crop((440, 1020, 2780, 1120))
        cropped12.save(basicpath + '12.png')
        cropped13 = img.crop((600, 1280, 2780, 1380))
        cropped13.save(basicpath + '13.png')
        cropped14 = img.crop((230, 1480, 2780, 2200))
        cropped14.save(basicpath + '14.png')

        for f in range(1, 15):
            imgpath = basicpath + str(f) + '.png'
            g = open(imgpath, 'rb')
            img = base64.b64encode(g.read())
            if f == 1 or f == 3 or f == 5 or f == 7 or f == 9 or f == 11 or f == 13:
                time.sleep(1)  # 防止超过QPS限制 引发报错
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
            params = {"image": img}
            access_token = getAuth()  # 对应申请的 access_token
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            msg_info = ''
            if response:
                json_str = response.content.decode()
                data = json.loads(json_str)
                msg = data['words_result']
                print(msg)
                for m in msg:
                    msg_info += m.get('words') + '\r\n'
            identification_results.append(msg_info.strip())
            g.close()
            os.remove(basicpath + str(f) + '.png')

        # print(identification_results)
        return identification_results

    # 识别过程中显示进度条
    def showProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MedicalRecordOcr()
    window.show()
    sys.exit(app.exec_())

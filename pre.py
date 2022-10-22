import os, yaml, shutil, openpyxl
from openpyxl.styles import Alignment

pypath = os.path.dirname(os.path.realpath(__file__))
cymlpath = os.path.join(pypath, 'config.yml')
tymlpath = os.path.join(pypath,'table.yml')
excelpath = os.path.join(pypath,'timetable_demo.xlsx')
yml = open(cymlpath, encoding="utf-8")
nyml = yml.read()
cfg = yaml.full_load(nyml)


def updata_yaml(x,t):
    old_yml = cfg
    old_yml[x] = t
    with open(cymlpath, "w", encoding="utf-8") as f:
        yaml.dump(old_yml,f)

def tabulation(yt):
    newexcelpath = os.path.join(pypath,yt)
    shutil.copy(excelpath, newexcelpath)
    with open(tymlpath, 'r', encoding='utf-8')as f2:
        data = f2.read()
        result = yaml.load_all(data, Loader=yaml.FullLoader)
        xls = openpyxl.load_workbook(newexcelpath)
        sh = xls.worksheets[0]
        xq = ['C', 'D', 'E', 'F', 'G', 'H', 'I']  # 表格对应的星期几
        for i in result:
            day = int(i['xqj']) - 1  # 星期几
            jc = i['jcs']  # 节数
            id = jc.index('-')
            qjc = str(int(jc[0:id]) + 1)  # 开始上课的节数
            hjc = str(int(jc[id + 1:]) + 1)  # 最后一节课的节数
            sh.merge_cells('{0}{1}:{0}{2}'.format(xq[day], qjc, hjc))
            sh['{}{}'.format(xq[day], qjc)] = i['kcmc'] + '\n' + '教室:' + i['cdmc'] + '\n' + i['zcd'] + '\n' + '教师:' + i[
                'xm'] + '\n' + '学分：' + i['xf']
            sh['{}{}'.format(xq[day], qjc)].alignment = Alignment(wrapText=True, horizontal='center', vertical='center')
            xls.save(newexcelpath)
    print('课程表已导出到' + newexcelpath)
#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import io
import sys
import re
import pickle
import copy
import shutil
import commands
import matplotlib.pyplot as plt
from optparse import OptionParser
from dateutil import parser as DateParse
from dateutil import rrule

if sys.getdefaultencoding() != 'gbk':
    reload(sys)
    sys.setdefaultencoding('utf8')

class ExecCommand:
    def __init__(self):
        """
        主机端命令执行接口
        """
        self.output = None
        self.status = None

    def execCmd(self, cmdStr, quiet = True):
        """
        执行命令
        :param cmdStr: 命令字符串
        :param quiet: 是否打印log
        :return: Nones
        """
        if quiet:
            status,output = commands.getstatusoutput(cmdStr)
            self.output = output
            self.status = int(status) / 256
        else:
            status = os.system(cmdStr)
            self.status = int(status) / 256

    def getOutput(self):
        """
        返回命令执行结果（输出）
        :return: 执行
        """
        return self.output

    def getStatus(self):
        """
        返回命令执行状态
        :return: 执行状态
        """
        return self.status

    def clear(self):
        """
        清除执行状态
        :return: None
        """
        self.output = None
        self.status = None

class BatteryLog:
    keyMap = {
        "MpowerTag": ".*\[mpower\].*",
        "UsbThermalTag": ".*\[usb_thermal\].*",
        "ChargerTag": ".*\[charger\].*",
        "FuelgaugeTag": ".*\[fuelgauge\].*",
        "TimeStamp": "^\[(.*?)\].*",
        "Plug": ".*<plug_(.*?)>.*",
        "ChrType": ".*<chr_type=(.*?)>.*",
        "BatTemp": ".*<battery_temp=(-?\d{1,3}\.?\d{1,2})degree>.*",
        "BoardTemp": ".*<board_temp=(-?\d+?)degree>.*",
        "FastChrEnable": ".*<is_supported_fastcharging=(\d)>.*",
        "FastChrType": ".*<protocol_type=(.*?)>.*",
        "UsbTemp": ".*<temp=(-?\d+?\.?\d+?)degree>.*",
        "ScreenOn": ".*<is_screen_on=(\d)>.*",
        "CmdDischarge": ".*<cmd_discharging=(\d)>.*",
        "BatCapacity": ".*<battery_capacity=(\d+?)mAh>.*",
        "fcc": ".*<setting_battery_current=(\d+?)uA>.*",
        "icl": ".*<setting_input_current=(\d+?)uA>.*",
        "vbus": ".*<vbus=(\d*?)uV>.*",
        "vbat": ".*<vbat=(\d{1,7})uV>.*",
        "ibat": ".*<ibat=(-?\d{1,7})uA>.*",
        "unlimit": ".*<is_usb_unlimited=(\d)>.*",
        "usoc": ".*<ui_soc=(\d{1,3})%>.*",
        "tsoc": ".*<true_soc=(\d{1,3})%>.*",
    }

    StatusData = {
        "MpowerTag": "None",
        "UsbThermalTag": "None",
        "ChargerTag": "None",
        "FuelgaugeTag": "None",
        "TimeStamp": "None",
        "ChrType": "None",
        "BatTemp": "None",
        "BoardTemp": "None",
        "FastChrEnable": "None",
        "FastChrType": "None",
        "UsbTemp": "None",
        "ScreenOn": "None",
        "CmdDischarge": "None",
        "BatCapacity": "None",
        "fcc": "None",
        "icl": "None",
        "vbus": "None",
        "vbat": "None",
        "ibat": "None",
        "unlimit": "None",
        "usoc": "None",
        "tsoc": "None",
    }

    RecordInfo = {
        "BatTemp": "None",
        "MinBatTemp": "None",
        "MaxBatTemp": "None",
        "DeltBatTemp": "None",
        "MinBoardTemp": "None",
        "MaxBoardTemp": "None",
        "DeltBoardTemp": "None",
        "StartSoc": "None",
        "StopSoc": "None",
        "DeltSoc": "None",
        "ChrType": "None",
        "FastChrType": "None",
        "StartTimeStamp": "None",
        "StopTimeStamp": "None",
        "DeltTime": "None",
        "CalculateDeltTime": "None",
    }

    IntKey = [
        "BatTemp", "BoardTemp", "FastChrEnable", "UsbTemp",
        "BatCapacity", "ScreenOn", "CmdDischarge", "fcc",
        "icl", "vbus", "vbat", "ibat", "unlimit", "usoc", "tsoc"
        ]

    def __init__(self, logfile, outdir = "output", shortname = False):
        self.logfile = logfile
        self.dirname = os.path.dirname(logfile)
        self.basename = os.path.basename(logfile)
        self.outdir = os.path.join(self.dirname, outdir)
        self.reportfile = "%s/%s.REPORT" % (self.outdir, self.basename)
        self.logdata = list()
        self.images = list()
        self.splitlog = list()
        self.shell = ExecCommand()
        self.shortname = shortname
        if not os.path.exists(self.outdir):
            os.mkdir(self.outdir)

        print self.logfile
        print self.outdir
        print self.reportfile

    def __del__(self):
        self.__close(self.report)

    def __open(self, filename, attr):
        if re.search("^r.*", attr):
            # open for read, 报告编码可能不同
            opErr = True
            for c in ("utf-8", "GB2312", "ISO-8859-2"):
                try:
                    _fr = io.open(filename, attr, encoding=c)
                    opErr = False
                    break
                except UnicodeDecodeError, e:
                    continue
            if opErr:
                print("open: %s" % e)
                sys.exit(1)

        else:
            # open for write
            try:
                _fr = io.open(filename, attr, encoding="utf-8")
            except OSError, e:
                print("open for write error: %s" % e)
                sys.exit(1)
        return _fr

    def __close(self, f):
        try:
            f.close()
        except AttributeError, e:
            pass

    def split(self):
        tmpname = ("%s/%s.tmp" % (self.outdir, self.basename))
        fh = self.__open(self.logfile, "r")
        logs = list()
        chargelog = list()
        dischargelog = list()

        count = 0

        tmp = io.open(tmpname, "w+", encoding="utf-8")
        print tmpname

        for line in fh.readlines():
            if not os.path.exists(tmpname):
                tmp = io.open(tmpname, "w+", encoding="utf-8")

            if re.search("^.*<plug_in>$", line):
                tmp.close()
                strCmd = "if grep \"\[charger\]\" %s > /dev/null; \
                                then echo charge;else echo discharge;fi" % (tmpname)
                self.shell.execCmd(strCmd)
                found = self.shell.getOutput().strip()
                if found == "charge":
                    if self.shortname:
                        target = "%s/charge.%s" % (self.outdir, count)
                    else:
                        target = "%s/%s.charge.%s" % (self.outdir, self.basename, count)
                    chargelog.append(target)
                else:
                    if self.shortname:
                        target = "%s/discharge.%s" % (self.outdir, count)
                    else:
                        target = "%s/%s.discharge.%s" % (self.outdir, self.basename, count)
                    dischargelog.append(target)
                logs.append(target)
                os.rename(tmpname, target)
                count += 1
                tmp = io.open(tmpname, "w+", encoding="utf-8")
                tmp.write("%s" % line)
            elif re.search("^.*<plug_out>$", line):
                tmp.write("%s" % line)
                tmp.close()
                if self.shortname:
                    target = "%s/charge.%s" % (self.outdir, count)
                else:
                    target = "%s/%s.charge.%s" % (self.outdir, self.basename, count)
                chargelog.append(target)
                logs.append(target)
                os.rename(tmpname, target)
                count += 1
            else:
                tmp.write("%s" % line)

        """
        处理最后一段没有plug标志的log
        """
        if os.path.exists(tmpname):
            tmp.close()
            strCmd = "if grep \"\[charger\]\" %s > /dev/null; \
                then echo charge;else echo discharge;fi" % (tmpname)
            self.shell.execCmd(strCmd)
            found = self.shell.getOutput().strip()
            if found == "charge":
                if self.shortname:
                    target = "%s/charge.%s" % (self.outdir, count)
                else:
                    target = "%s/%s.charge.%s" % (self.outdir, self.basename, count)
                chargelog.append(target)
                logs.append(target)
                os.rename(tmpname, target)
                count += 1
            else:
                if self.shortname:
                    target = "%s/discharge.%s" % (self.outdir, count)
                else:
                    target = "%s/%s.discharge.%s" % (self.outdir, self.basename, count)
                dischargelog.append(target)
                logs.append(target)
                os.rename(tmpname, target)
                count += 1

        fh.close()
        self.splitlog = logs
        return (chargelog, dischargelog, logs)

    def __isCharging(self, name):
        pattern = "^.*charge\.\d.*"
        match = re.search(".*\.charge\.\d", name)
        if match:
            return True
        else:
            return False

    def __validChargerStatus(self, status):
        # don't need (UsbTemp/icl/tsoc)
        checkinfo = [ "ChrType", "BatTemp", "fcc", "BoardTemp", "FastChrEnable", "FastChrType",
                     "vbus", "vbat", "ibat", "unlimit", "ScreenOn", "usoc", "CmdDischarge"]

        for key in checkinfo:
            if status[key] == "None":
                return False
        return True

    def __validFuelgaugeStatus(self, status):
        checkinfo = ["BatTemp", "vbat", "ibat", "usoc"]

        for key in checkinfo:
            if status[key] == "None":
                return False
        return True

    def validStatus(self, status):
        if self.charging:
            return self.__validChargerStatus(status)
        else:
            return self.__validFuelgaugeStatus(status)

    def dataProcess(self, log):
        keyMap = self.keyMap
        status = copy.deepcopy(self.StatusData)
        data = list()
        f = self.__open(log, "r")
        for line in f.readlines():
            # 检查该行是否需要解析
            if not re.search(keyMap["MpowerTag"], line):
                continue
            for keyWord in keyMap:
                # print(keyWord)
                match = re.match(keyMap[keyWord], line)
                if match:
                    if keyWord == "TimeStamp":
                        status[keyWord] = DateParse.parse(match.group(1))
                    elif re.search(".*Tag.*", keyWord):
                        status[keyWord] = True
                    else:
                        if keyWord in self.IntKey:
                            status[keyWord] = int(float(match.group(1)))
                        else:
                            status[keyWord] = str(match.group(1))
                else:
                    if re.search(".*Tag.*", keyWord):
                        status[keyWord] = False

            # print status
            s = pickle.dumps(status)
            data.append(s)
            self.logdata.append(s)
        print "line:", len(data)
        self.__close(f)
        return data

    def handleChargerRules(self, status):
        if not self.charging:
            return ""

        return ""

    def handleFuelgaugeRules(self, status):
        return ""

    def handleOverviewRules(self, info):
        exception = ""
        """
        检查是否有填充过有效数据
        """
        if not self.populate:
            return exception

        if self.charging:
            """
            温度检查
            """
            temp = self.getReportSepLine()
            temp += "规则：温度检查\n"
            temp += "异常：充电发热/充电慢\n"
            if info["MinBatTemp"] == "None" \
                    or info["MaxBatTemp"] == "None" \
                    or info["MinBoardTemp"] == "None":
                temp = ""
            elif info["MinBatTemp"] > 30:
                temp += "原因：起始充电电池温度高于30度\n"
            elif info["MinBoardTemp"] > 42:
                temp += "原因：起始充电主板温度高于42度\n"
            elif info["MaxBatTemp"] > 45:
                temp += "原因：电池温度有高于过45度\n"
            elif info["MinBatTemp"] < 0:
                temp += "原因：起始充电电池温度低于0度\n"
            else:
                temp = ""
            exception += temp
            """
            充电类型检查
            """
            temp = self.getReportSepLine()
            temp += "规则：充电器类型检查\n"
            temp += "异常：充电慢\n"
            if info["ChrType"] == "STANDARD_HOST":
                temp += "原因：充电器类型为USB\n"
            elif info["ChrType"] == "CHARGING_HOST\n":
                temp += "原因：充电器类型为DCP\n"
            elif info["ChrType"] == "NONSTANDARD_CHARGER\n":
                temp += "原因：充电器类型为非标准充电器"
            else:
                temp = ""
            exception += temp
        return exception

    def populateOverview(self, status):
        self.populate = True
        info = self.overview

        # record MinBatTemp
        if info["MinBatTemp"] == "None":
            info["MinBatTemp"] = status["BatTemp"]
        else:
            if status["BatTemp"] != "None" and info["MinBatTemp"] > status["BatTemp"]:
                info["MinBatTemp"] = status["BatTemp"]

        # record MaxBatTemp
        if info["MaxBatTemp"] == "None":
            info["MaxBatTemp"] = status["BatTemp"]
        else:
            if status["BatTemp"] != "None" and info["MaxBatTemp"] < status["BatTemp"]:
                info["MaxBatTemp"] = status["BatTemp"]

        # record MinBoardTemp
        if info["MinBoardTemp"] == "None":
            info["MinBoardTemp"] = status["BoardTemp"]
        else:
            if status["BoardTemp"] != "None" and info["MinBoardTemp"] > status["BoardTemp"]:
                info["MinBoardTemp"] = status["BoardTemp"]

        # record MaxBoardTemp
        if info["MaxBoardTemp"] == "None":
            info["MaxBoardTemp"] = status["BoardTemp"]
        else:
            if status["BoardTemp"] != "None" and info["MaxBoardTemp"] < status["BoardTemp"]:
                info["MaxBoardTemp"] = status["BoardTemp"]

        # calculate DeltaTemp
        if info["MaxBatTemp"] != "None" and info["MinBatTemp"] != "None":
            info["DeltBatTemp"] = info["MaxBatTemp"] - info["MinBatTemp"]

        if info["MaxBoardTemp"] != "None" and info["MinBoardTemp"] != "None":
           info["DeltBoardTemp"] = info["MaxBoardTemp"] - info["MinBoardTemp"]

        # handle StartSoc & StopSoc & DeltaSoC
        if status["usoc"] != "None":
            if info["StartSoc"] == "None":
                info["StartSoc"] = status["usoc"]
            info["StopSoc"] = status["usoc"]
            info["DeltaSoc"] = info["StopSoc"] - info["StartSoc"]

        # record ChrType
        if status["ChrType"] != "None":
            info["ChrType"] = status["ChrType"]

        # record FastChrType
        if status["FastChrType"] != "None":
            info["FastChrType"] = status["FastChrType"]

        # record StartTimeStamp & StopTimeStamp
        if status["TimeStamp"] != "None":
            if info["StartTimeStamp"] == "None":
                info["StartTimeStamp"] = status["TimeStamp"]
            else:
                """
                过滤起始阶段1970年的时间
                """
                deltTime = (status["TimeStamp"] - info["StartTimeStamp"])
                if deltTime.days > 1000:
                    info["StartTimeStamp"] = status["TimeStamp"]

            if info["StopTimeStamp"] == "None":
                info["StopTimeStamp"] = status["TimeStamp"]
            else:
                """
                计算获取DeltTime，修正由时钟设定引入的统计错误
                """
                deltTime = (status["TimeStamp"] - info["StopTimeStamp"])
                if (status["TimeStamp"] - info["StopTimeStamp"]).seconds < 3600 \
                        and (status["TimeStamp"] > info["StopTimeStamp"]):
                    if info["CalculateDeltTime"] == "None":
                        info["CalculateDeltTime"] = deltTime
                    else:
                        info["CalculateDeltTime"] += deltTime
                """
                过滤结束阶段1970年的时间，时间小于当前stop时间1000天，认为是跳到1970年了
                """
                if (info["StopTimeStamp"] - status["TimeStamp"]).days < 1000:
                    info["StopTimeStamp"] = status["TimeStamp"]

        if info["StopTimeStamp"] != "None" and info["StartTimeStamp"] != "None":
            deltTime = (info["StopTimeStamp"] - info["StartTimeStamp"])
            info["DeltTime"] = deltTime

    def setReportOverview(self):
        text = ""
        if not self.populate:
            text += "没有足够的有效LOG可供分析\n"
            self.report.write(u"%s" % text)
            return text

        if self.charging:
            chg = "Charging"
        else:
            chg = "Discharging"

        if self.currStatus:
            cap = self.currStatus["BatCapacity"]
        else:
            cap = "None"

        info = self.overview
        text += "充电状态： %s\n" % chg
        text += "开始时间： %s\n" % info["StartTimeStamp"]
        text += "结束时间： %s\n" % info["StopTimeStamp"]
        text += "记录时间： %s (时：分：秒)\n" % info["DeltTime"]
        text += "校正时间： %s (时：分：秒)\n" % info["CalculateDeltTime"]
        text += "开始电量： %s\n" % info["StartSoc"]
        text += "结束电量： %s\n" % info["StopSoc"]
        text += "电量变化： %s\n" % info["DeltaSoc"]
        text += "电池最小温度： %s ℃\n" % (info["MinBatTemp"])
        text += "电池最大温度： %s ℃\n" % (info["MaxBatTemp"])
        text += "电池温差： %s ℃\n" % (info["DeltBatTemp"])
        text += "主板最小温度： %s ℃\n" % (info["MinBoardTemp"])
        text += "主板最大温度： %s ℃\n" % (info["MaxBoardTemp"])
        text += "主板温差： %s ℃\n" % (info["DeltBoardTemp"])
        text += "充电器类型： %s\n" % (info["ChrType"])
        text += "快充类型： %s\n" % (info["FastChrType"])
        text += "电池容量： %s mAh\n" % cap

        self.report.write(u"%s" % text)
        return text

    def setReportException(self, exception):
        if self.populate and exception == "":
            exception += self.getReportSepLine()
            exception += "没有发现异常\n"

        self.report.write(u"%s" % exception)
        return exception

    def mainAnalyzer(self, data, file):
        """
        主解析函数
        :param data: 待解析数据列表
        :param file: 待解析文件名
        """
        self.overview = copy.deepcopy(self.RecordInfo)
        self.charging = self.__isCharging(file)
        self.populate = False
        self.currStatus = None
        exception = ""
        charger_exception = ""
        fuelgauge_exception = ""
        overview_exception = ""
        for i in data:
            status = pickle.loads(i)
            # print status
            if not self.validStatus(status):
                continue

            # 记录和填充Overview参数
            self.populateOverview(status)

            # 处理charger单行规则
            charger_exception += self.handleChargerRules(status)

            # 处理fuelgauge单行规则
            fuelgauge_exception += self.handleFuelgaugeRules(status)
            self.currStatus = status

        # 处理Overview参数规则
        overview_exception = self.handleOverviewRules(self.overview)

        # 输出Report
        exception += overview_exception
        exception += charger_exception
        exception += fuelgauge_exception
        self.setReportOverview()
        self.setReportException(exception)

    def drawFigure(self, data, file):
        soc = list()
        vbat = list()
        ibat = list()
        temp = list()

        save = "%s.png" % file

        for i in data:
            status = pickle.loads(i)
            if status["usoc"] != "None" and \
                status["vbat"] != "None" and \
                status["ibat"] != "None" and \
                status["BatTemp"] != "None":
                soc.append(status["usoc"])
                vbat.append(status["vbat"])
                ibat.append(status["ibat"])
                temp.append(status["BatTemp"])
        fig = plt.figure(1)  # 第一张图
        plt.subplot(221)  # 第一张图中的第1张子图
        plt.title("SOC")
        plt.plot(soc)
        plt.subplot(222)  # 第一张图中的第2张子图
        plt.title("VBAT")
        plt.plot(vbat)
        plt.subplot(223)  # 第一张图中的第3张子图
        plt.title("IBAT")
        plt.plot(ibat)
        plt.subplot(224)  # 第一张图中的第4张子图
        plt.title("TEMP")
        plt.plot(temp)
        plt.tight_layout()
        #plt.show()
        fig.savefig(save, dpi=fig.dpi)
        plt.close(1)
        self.images.append(save)

    def getImages(self):
        return self.images

    def getSplitLog(self):
        return self.splitlog

    def parseSplitLog(self, logs):
        """
        解析SpiltLog的操作
        :param logs: 待解析文件列表
        """
        if not logs:
            return

        for file in logs:
            print file
            self.setReportSplitLogTitle(os.path.basename(file))
            data = self.dataProcess(file)
            self.mainAnalyzer(data, file)
            self.drawFigure(data, file)

    def parseFullLog(self):
        """
        解析完整Log的操作
        :return None
        """
        target = os.path.join(self.outdir, self.basename)
        shutil.copyfile(self.logfile, target)

        return None

    def parse(self):
        self.report = self.__open(self.reportfile, "w+")
        if not self.report:
            return None
        self.setReportHeader()

        # 分离充电和放电阶段

        ret = self.split();
        # self.parseSplitLog(ret[0])
        # self.parseSplitLog(ret[1])
        self.parseSplitLog(ret[2])
        self.parseFullLog()
        self.__close(self.report)
        ret = list()
        ret.append(self.reportfile)
        return ret

    def setReportHeader(self):
        ret = "\n/" + "*" * 86 + "/\n"
        header = "BatteryLog客制化分析工具（Battery Log Custom Analyzer）\n"
        author = "作者  : 谢昊成\n"
        version = "版本  : v1.0"
        text = "\n"
        text += ret
        text += header
        text += author
        text += version
        text += ret
        self.report.write(u"%s" % text)

    def getReportSepLine(self):
        sepLine = "\n" + "=" * 25 + "\n"
        return sepLine

    def setReportSplitLogTitle(self, name):
        text = "\n" + "-" * 86 + "\n"
        text += "\n"
        text += (">>>>>  %s  <<<<<" % name)
        text += ("\n>>>>> 分析结果如下 <<<<<\n")
        self.report.write(u"%s" % text)

    def setReportStrList(self, strlist=None):
        """
        写入字符串列表到报告
        :param strlist: string list
        :return: None
        """
        if not strlist:
            return

        text = "\n"
        text += "\n".join(strlist)
        self.report.write(u"%s" % text)

def do_main_work():
    parser = OptionParser()
    parser.add_option("--input", "-i", action="store",
                      dest="input", default=False, help="input log file path. Eg. -i mbattery_charger_log_2018_02_23")
    parser.add_option("--output", "-o", action="store",
                      dest="output", default=False, help="output report dir. Eg. -s output")

    (options, args) = parser.parse_args()
    if len(sys.argv) < 2:
        print parser.print_help()
        return 0

    input = options.input
    if options.output:
        output = options.output
    else:
        output = options.input + ".output"

    batlog = BatteryLog(input, output)
    batlog.parse()

if __name__ == '__main__':
    do_main_work()



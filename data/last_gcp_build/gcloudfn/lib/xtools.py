
'''
Created on Sep 6, 2014

@author: Mukundan
'''

'''
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        paddingRight = self._clearButton.sizeHint().width() + frameWidth + 1
        stylesheet = "QLineEdit {{ padding-right:{0}px; }}".format(paddingRight)
        self.setStyleSheet(stylesheet)
'''

'''
from kmxGeneral import kmxINIConfigReadWrite
from kmxGeneral import kmxTools
from kmxPyQt import kmxQtCommonTools

        self.cfg = kmxINIConfigReadWrite.INIConfig("config.ini")
        self.iconPath = self.cfg.getOption('UserInterface', 'IconPath')
        self.icons = cryptolibs.icons.iconSetup()
        self.infoStyle = kmxTools.infoStyle()
        self.infoStyle.errorLevel = 2
        self.infoStyle.infoLevel = 0

        self.tls = kmxTools.Tools(self.infoStyle)
        self.qtTools = kmxQtCommonTools.CommonTools(self.win, self.iconPath)

        or

        self.qtTools = kmxQtCommonTools.CommonTools(self)
        self.ttls = kmxTools.Tools()

'''
import math
import subprocess
import traceback
import uuid
import logging as log
import logging
import getpass
import socket
from gmailconnector.send_email import SendEmail
from datetime import datetime, timedelta
from notify_run import Notify
import time
from time import strftime
from decimal import Decimal
import inspect
import pprint
import os
import pickle
import random
import shutil
import sys
import re
import atexit
numbers = re.compile('\d+')
# Include below point in your main and errors will be displayed.
#sys.excepthook = kmxTools.errorHandler

MYPCNAME = 'KUMARESANPC'
        
def getGlobalTools():
    found = 0
    obj = inspect.currentframe().f_back
    while not found:
        if hasattr(obj, 'f_locals'):
            vars = obj.f_locals
        else:
            tls = Tools()
            print('Global Tools Ready! ' + str(tls))
            return tls
        #if 'tls' in vars:        
        if '__name__' in vars and vars['__name__'] == '__main__' and 'tls' in vars:
            found = 1
            return vars['tls']
        else:
            obj = obj.f_back


def isWindows():
    return os.name == 'nt'


def isLinux():
    return os.name == 'posix'


def errorHandler(etype, value, tb):
    """
    Global function to catch unhandled exceptions.

    @param etype exception type
    @param value exception value
    @param tb traceback object
    """

    info = ''
    try:
        info = traceback.format_exc()
        print(info)
    except:
        print('Traceback formatter failed! Custom formatted exception info')
        print('--------')
        print('')
        info = traceback.format_exception(etype, value, tb)
        disp = ''
        for eachLine in info:
            disp += eachLine
        print(disp)
        info = disp
        print('--------')
    try:
        f = open('error.log', "w")
        f.write(str(info))
        f.close()
    except IOError:
        pass

def exiting():
    print('-----The End------')
atexit.register(exiting)

class Tools(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.randomSeed = 50
        self.rand = random.Random(self.randomSeed)

        self.dateTimeStampFmt = '%Y%m%d%H%M%S'
        self.logName = 'kmx.pyservice'
        self.logFormat = '[%(asctime)s]%(message)s'
        self.logLevel = 20  # 10 - debug #20 - info #30 - warn #40 - error
        self.logToStream = 1
        self.logToFile = 0
        self.logFile = self.getDateTimeStamp(self.dateTimeStampFmt) + '.log'
        self.showSimpleLog = 0
        self.ignoreSysLogger = 0
        
        self.tags = []
        self.globalVar = {}
        self.globalSwitch = {}
        
        self.localCachePath = 'G:/pythonworkspace/ourcryptos/data/cache'

        if not 'gmail_user' in os.environ or not 'gmail_pass' in os.environ:
            print('Please set -gmail_user- and -gmail_pass- environment variable to proceed')
            #exit(0) 
            #gmail_user = 'username@gmail.com',
            #gmail_pass = '<ACCOUNT_PASSWORD>'

        self.setupLogger()
        self.readyCachePath()
        
    def getGlobalVar(self, varName):
        if self.isGlobalVarExist(varName):
            return self.globalVar[varName]
    
    def setGlobalVar(self, varName, value):
        self.globalVar[varName]= value
    
    def isGlobalVarExist(self, varName):
        return varName in self.globalVar
    
    def getGlobalSwitch(self, varName, default=0):
        if self.isGlobalVarSwitch(varName):
            return self.globalSwitch[varName]
        else:
            return default
    
    def setGlobalSwitch(self, varName, value):
        self.info(f'Global switch {varName} triggered to {value}')
        self.globalSwitch[varName]= value
    
    def isGlobalVarSwitch(self, varName):
        return varName in self.globalSwitch    

    def helloWorld(self):
        self.info('Hello World', skipLevel=4)
        
    def setDebugging(self):
        self.logToStream = 1
        self.logLevel = 10
        self.setupLogger(update=1)
    
    def isLocalDev(self):
        if isWindows():
            if 'COMPUTERNAME' in os.environ:
                if os.environ['COMPUTERNAME'] == MYPCNAME:
                    return 1
        return 0
        
    def isItMorning(self):
        return self.getDateTime('%p').lower() == 'am'

    def getMorE(self):
        '''
        AM or PM
        MORNING OR EVENING
        M OR E
        m or e
        '''
        return 'm' if self.isItMorning() else 'e'
    
    def readyCachePath(self):
        if self.isLocalDev():
            self.pathReady(self.localCachePath)

    def pathClean(self, inputFile):
        inputFile = os.path.normpath(inputFile)
        inputFile = os.path.abspath(inputFile)
        return inputFile

    def pathParts(self, inputFile):
        inputFile = self.pathClean(inputFile)
        fileNameWithExt = os.path.basename(inputFile)
        fileName, Ext = os.path.splitext(fileNameWithExt)
        filePath = os.path.dirname(inputFile)
        Ext = Ext[1:] if Ext.startswith('.') else Ext
        return filePath, fileName, Ext

    def isCacheAvailable(self, fileName, dated=0):
        if dated: fileName = self._cacheName(fileName)
        fileName = self._applyLocalCachePath(fileName)
        return os.path.exists(fileName)

    def getCache(self, fileName, defaultData=None, dated=0):
        if dated: fileName = self._cacheName(fileName)
        fileName = self._applyLocalCachePath(fileName)
        if self.isCacheAvailable(fileName):
            self.debug(f'Reading cache {fileName}')
            f = open(fileName, 'rb')
            data = pickle.load(f)
            f.close()
        else:
            self.debug(f'Cache not found: {fileName}')
            self.setCache(fileName, defaultData)
            data = defaultData
        return data
    
    def setCache(self, fileName, data, dated=0):
        if dated: fileName = self._cacheName(fileName)
        fileName = self._applyLocalCachePath(fileName)
        self.debug(f'Writing cache {fileName}')
        picData = pickle.dumps(data)
        f = open(fileName, 'wb')
        f.write(picData)
        f.close()
    
    def _applyLocalCachePath(self, fileName):
        return self.pathJoin(self.localCachePath, fileName)

    def _cacheName(self, fileName):
        nw = self.getDateTime('%Y%m%d')
        cacheName = f'{nw}_{fileName}'
        return cacheName

    def storeData(self, fileName, data):
        picData = pickle.dumps(data)
        f = open(fileName, 'wb')
        f.write(picData)
        f.close()

    def readData(self, fileName, defaultData=None):
        if os.path.exists(fileName):
            f = open(fileName, 'rb')
            data = pickle.load(f)
            f.close()
        else:
            data = defaultData
        return data

    def pathReady(self, inputPath):
        inputPath = self.pathClean(inputPath)
        if os.path.exists(inputPath):
            return inputPath
        if os.path.isfile(inputPath):
            inputPath, fileName, Ext = self.pathParts(inputPath)
        os.mkdir(inputPath)
        if os.path.exists(inputPath):
            return inputPath
        return inputPath

    def pathJoin(self, basePath, *joins):
        finPath = basePath
        for each in joins:
            finPath = os.path.join(finPath, each)
        return self.pathClean(finPath)

    def doBackup(self, srcFile, bckUpToPath=1, bckUpPath='G:/pythonworkspace/myscripts/dataBackup', bckUpFmt='[FILENAME]_BKUP[TIMESTAMP].[EXT]'):
        self.debug('Backup Src: ' + srcFile)
        if not os.path.exists(srcFile):
            self.raiseError(
                'Unable to do backup as src file not found ' + srcFile)
            return 0
        timeStamp = self.getDateTime('%Y%m%d%H%M%S')
        filePath, fileName, Ext = self.pathParts(srcFile)
        dstPath = self.pathReady(
            bckUpPath) if bckUpToPath else self.pathClean('.')
        dstFileName = bckUpFmt
        dstFileName = dstFileName.replace('[FILENAME]', fileName)
        dstFileName = dstFileName.replace('[TIMESTAMP]', timeStamp)
        dstFileName = dstFileName.replace('[EXT]', Ext)
        dstFile = self.pathJoin(dstPath, dstFileName)
        self.debug('Backup Dst: ' + dstFile)
        self.copyFile(srcFile, dstFile)
        self.debug('Backup Done!')
        return 1

    def getUnixTimeStampCore(self, dtobj):
        #date_time = datetime.datetime(2021, 7, 26, 21, 20)
        return time.mktime(dtobj.timetuple())

    def getUnixTimeStamp(self, days=0, seconds=0):
        if not days and not seconds:
            res = datetime.now() + timedelta(days=0)
        if days and not seconds:
            res = datetime.now() + timedelta(days=0)
        if not days and seconds:
            res = datetime.now() + timedelta(seconds=seconds)
        return self.getUnixTimeStampCore(res)

    def getArgs(self):
        if len(sys.argv) > 1:
            return sys.argv[1:]
        return []

    def isArgPresent(self, checkFor):
        for each in self.getArgs():
            if each.lower().startswith(checkFor.lower()):
                return True
        return False

    def getArgValue(self, argName):
        if self.isArgPresent(argName):
            for each in self.getArgs():
                if each.lower().startswith(argName.lower()):
                    data = each.split('=')
                    if len(data) == 2:
                        return data[1]
        return ''

    def setupLogger(self, update=0):
        self.loggerName = 'kmx.pyservice'

        if 'mylogger' in globals() and not update:
            self.logSys = globals()['mylogger']
        else:
            for eachHandler in logging.root.handlers:
                logging.root.removeHandler(eachHandler)
            self.logSys = logging.getLogger(self.loggerName)
            self.logSys.setLevel(self.logLevel)
            globals()['mylogger'] = self.logSys
            logFormatter = logging.Formatter(
                fmt=self.logFormat, datefmt=self.dateTimeStampFmt)

            logHands = []
            for each in self.logSys.handlers:
                if update:
                    each.flush()
                    each.close()
                    self.logSys.handlers.remove(each)
                else:
                    logHands.append(each.name)

            if self.logToStream:
                if not 'StreamHandler' in logHands or update:
                    logStrHdl = logging.StreamHandler()
                    logStrHdl.set_name('StreamHandler')
                    logStrHdl.setFormatter(logFormatter)
                    logStrHdl.setLevel(self.logLevel)
                    self.logSys.addHandler(logStrHdl)

            if self.logToFile:
                if not 'FileHandler' in logHands or update:
                    logFileHdl = logging.FileHandler(self.logFile)
                    logFileHdl.set_name('FileHandler')
                    logFileHdl.setFormatter(logFormatter)
                    logFileHdl.setLevel(self.logLevel)
                    self.logSys.addHandler(logFileHdl)

        self.logSys

    def notify(self, smallmsg, bigmsg='', subject='kmxauto'):
        if bigmsg == '':
            bigmsg = smallmsg
        # mail
        response = SendEmail(
            sender="KMXAuto",
            recipient='kaymatrix@gmail.com',
            subject=subject,
            body=str(bigmsg)
            #gmail_user='',
            #gmail_pass=''
        ).send_email()
        if response.ok:
            print(response.json())
        # notify
        notify = Notify(endpoint='https://notify.run/Stq4iPeFaU4ePGS6pqPp')
        notify.send(str(smallmsg))
        #notify.send('Click to open notify.run!', 'https://notify.run')

        self.info('Notified: ' + smallmsg)

    def getFloat(self, input):
        return float(Decimal(input))
    
    def getPercentIncrease(self, inputRate, percent):
        return float(inputRate + (Decimal((percent / 100)) * inputRate))

    def getPercentOf(self, inputRate, percent):
        return float((Decimal((percent / 100)) * inputRate))

    def prittyPrint(self, data=''):

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)

    def isWindows(self):
        return isWindows()

    def isLinux(self):
        return isLinux()

    def rowPrint(self, *arg):
        spacer = 25
        info = ''
        for each in arg:
            info = info + str(each).ljust(spacer, '_')
        print(info)

    def precision(self, value, digits=6):
        value = Decimal(value)
        return math.floor(value * 10 ** digits) / 10 ** digits

    def priceFormat(self, price):
        return "{:.2f}".format(float(price))

    def info(self, *msg, skipLevel=2):
        if skipLevel>2:
            print('test')
        if type(msg) == type(()):
            lst = []
            for each in msg:
                lst.append(str(each))

            msg = ','.join(lst)
        else:
            msg = msg[0]
        if not self.showSimpleLog:
            msg = self.logMessageFormat(msg, skipLevel)
        if self.ignoreSysLogger:
            print(msg)
        else:
            if hasattr(self, 'logSys'):
                self.logSys.info(msg)
            else:
                print(msg)

    def setPlainLog(self):
        self.ignoreSysLogger = 1
        self.showSimpleLog = 1

    def checkPointInfo(self, msg):
        self.info('----------------------------------', skipLevel=3)
        self.info(msg, skipLevel=3)
        self.info('----------------------------------', skipLevel=3)

    def checkPointDebug(self, msg):
        self.debug('----------------------------------')
        self.debug(msg)
        self.debug('----------------------------------')

    def debug(self, *msg, skipLevel=2):
        if type(msg) == type(()):
            lst = []
            for each in msg:
                lst.append(str(each))

            msg = ','.join(lst)
        else:
            msg = msg[0]
        if not self.showSimpleLog:
            msg = self.logMessageFormat(msg, skipLevel)
            msg = '[D]'+str(msg)
        if self.ignoreSysLogger and self.logSys.level <= 10:
            print(msg)
        else:
            self.logSys.debug(msg)

    def warn(self, msg='', skipLevel=2):
        if not self.showSimpleLog:
            msg = self.logMessageFormat(msg, skipLevel)
        if self.ignoreSysLogger:
            print(msg)
        else:
            self.logSys.warn(msg)

    def error(self, msg='', skipLevel=2):
        if not self.showSimpleLog:
            msg = self.logMessageFormat(msg, skipLevel)
        if self.ignoreSysLogger:
            print(msg)
        else:
            self.logSys.error(msg)

    def logMessageFormat(self, msg='', skipLevel=2):
        fn, cls, mod, modf = self.getCallerInfo(skipLevel)
        fmsg = '[{0}.{1}.{2}]: {3}'.format(mod, cls, fn, msg)
        return fmsg

    def getCallerInfo(self, skipLevel=1):
        fn, cls, mod, modf = '', '', '', ''
        try:
            stack = inspect.stack()
            stack = stack[skipLevel+1:]
            if len(stack) > 0:
                entry = stack[0]
                if len(entry) > 3:
                    fcode = entry[0]
                    fn = str(entry[3])
                    cls = ''
                    mod = ''
                    modf = str(entry[1])
                    if hasattr(fcode, 'f_locals'):
                        locals = fcode.f_locals
                        if 'self' in locals:
                            selfobj = locals['self']
                            if selfobj:
                                cls = str(selfobj.__class__.__name__)
                                mod = str(selfobj.__module__)
                        else:
                            mod = os.path.basename(modf)
                            mod = os.path.splitext(mod)[0]
                    else:
                        mod = os.path.basename(modf)
                        mod = os.path.splitext(mod)[0]
        except:
            pass
        return fn, cls, mod, modf

    def shellExecute(self, command):
        # This will chock and execute
        subprocess.call(command)

    def raiseError(self, msg='CustomError'):
        raise Exception(msg)

    def encrypt(self, text, cryptoKey=4132):
        cipher = ''
        for each in text:
            c = (ord(each)+int(cryptoKey)) % 126
            if c < 32:
                c += 31
            cipher += chr(c)
        return cipher

    def decrypt(self, text, cryptoKey=4132):
        plaintext = ''
        for each in text:
            p = (ord(each)-int(cryptoKey)) % 126
            if p < 32:
                p += 95
            plaintext += chr(p)
        return plaintext

    def getUUID(self):
        return str(uuid.getnode())

    def errorInfoOld(self):
        TrackStack = sys.exc_info()[2]
        ErrorReport = []
        while TrackStack:
            FileName = TrackStack.tb_frame.f_code.co_filename
            FunctionName = TrackStack.tb_frame.f_code.co_name
            ErrorLine = TrackStack.tb_lineno
            TrackStack = TrackStack.tb_next
            ErrorReport.append([FileName, FunctionName, ErrorLine])
        ErrorReport.append([sys.exc_info()[0], sys.exc_info()[1], 0])
        ErrorInfo = ''
        for eachErrorLevel in ErrorReport:
            ErrorInfo += '\nFile: "' + str(eachErrorLevel[0]) + '", line ' + str(
                eachErrorLevel[2]) + ', in ' + str(eachErrorLevel[1])
        self.error(ErrorInfo)
        return None

    def errorInfo(self):
        info = traceback.format_exc()
        self.error(info)

    def printObjInfos(self, obj):
        lst = self.getObjInfos(obj)
        for each in lst:
            print('{0} - {1}'.format(each[0], each[1]))

    def getObjInfos(self, obj):
        infos = []
        members = inspect.getmembers(obj)
        for eachMember in members:
            obj = eachMember[1]
            mem = eachMember[0]
            tp = 'Obj'
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                tp = 'Fn'
            elif inspect.isbuiltin(obj):
                tp = 'Fn-BuiltIn'
            elif inspect.isclass(obj):
                tp = 'Class'
            elif inspect.ismodule(obj):
                tp = 'Module'
            elif inspect.iscode(obj):
                tp = 'Code'
            elif (type(obj) is type(1) or
                  type(obj) is type('') or
                  type(obj) is type([]) or
                  type(obj) is type(()) or
                  type(obj) is type({})
                  ):
                tp = 'Variable'
            elif type(obj) is type(None):
                tp = 'Obj'
            else:
                tp = 'Obj'

            infos.append([mem, tp, eachMember[1]])
        return infos

    def getRandom(self, stop, start=0):
        return self.rand.randrange(start, stop)

    def getSystemName(self):
        return str(socket.gethostname())

    def getCurrentPath(self):
        return os.path.abspath(os.curdir)

    def getCurrentUser(self):
        return getpass.getuser()

    def getRelativeFolder(self, folderName):
        return os.path.join(self.getCurrentPath(), folderName)

    def getDateCalc(self, addRemoveDays=0, format='%Y-%m-%d'):
        res = datetime.today() + timedelta(days=addRemoveDays)
        return res.strftime(format)

    def getDateTimeObjFor(self, input, format='%Y-%m-%d'):
        return datetime.strptime(input, format)

    def getDateDiff(self, date1, date2, format='%Y-%m-%d'):
        d1 = self.getDateTimeObjFor(date1, format)
        d2 = self.getDateTimeObjFor(date2, format)
        res = d2 - d1
        return res.days

    def getDateTimeStamp(self, format="%Y%m%d%H%M%S"):
        return self.getDateTime(format)

    def getDateTime(self, format="%Y-%m-%d %H:%M:%S"):
        """
        "%Y-%m-%d %H:%M:%S"
        Directive Meaning Notes
        %a Locale's abbreviated weekday name.
        %A Locale's full weekday name.
        %b Locale's abbreviated month name.
        %B Locale's full month name.
        %c Locale's appropriate date and time representation.
        %d Day of the month as a decimal number [01,31].
        %H Hour (24-hour clock) as a decimal number [00,23].
        %I Hour (12-hour clock) as a decimal number [01,12].
        %j Day of the year as a decimal number [001,366].
        %m Month as a decimal number [01,12].
        %M Minute as a decimal number [00,59].
        %p Locale's equivalent of either AM or PM. (1)
        %S Second as a decimal number [00,61]. (2)
        %U Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0. (3)
        %w Weekday as a decimal number [0(Sunday),6].
        %W Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0. (3)
        %x Locale's appropriate date representation.
        %X Locale's appropriate time representation.
        %y Year without century as a decimal number [00,99].
        %Y Year with century as a decimal number.
        %Z Time zone name (no characters if no time zone exists).
        %% A literal "%" character.
        """
        return strftime(format)

    def fileContent(self, fileName):
        f = open(fileName, "r")
        content = str(f.read())
        f.close()
        return content

    def writeFileContent(self, fileName, data):
        f = open(fileName, 'w')
        f.write(str(data))
        f.close()

    def copyFile(self, src, dst):
        shutil.copy(src, dst)

    def copyFolder(self, source_folder, destination_folder, latest_overwrite=1, forced_overwrite=0, verbose=1):
        for root, dirs, files in os.walk(source_folder):
            for item in files:
                src_path = os.path.join(root, item)
                dst_path = os.path.join(
                    destination_folder, src_path.replace(source_folder, ""))
                if os.path.exists(dst_path):
                    if (not forced_overwrite and not latest_overwrite):
                        if(verbose):
                            print("Already exist, Skipping...\n" +
                                  src_path + " to " + dst_path)
                    if (not forced_overwrite and latest_overwrite):
                        if os.stat(src_path).st_mtime > os.stat(dst_path).st_mtime:
                            if(verbose):
                                print("Overwriting latest...\n" +
                                      src_path + " to " + dst_path)
                            shutil.copy2(src_path, dst_path)
                    if (forced_overwrite):
                        if(verbose):
                            print("Overwriting...\n" +
                                  src_path + " to " + dst_path)
                        shutil.copy2(src_path, dst_path)
                else:
                    if(verbose):
                        print("Copying...\n" + src_path + " to " + dst_path)
                    shutil.copy2(src_path, dst_path)
            for item in dirs:
                src_path = os.path.join(root, item)
                dst_path = os.path.join(
                    destination_folder, src_path.replace(source_folder, ""))
                if not os.path.exists(dst_path):
                    if(verbose):
                        print("Creating folder...\n" + dst_path)
                    os.mkdir(dst_path)
        if(verbose):
            print("Copy process completed!")

    def _buildCallerPath(self, parentOnly=0):
        stack = inspect.stack()
        path = ""
        for eachStack in stack:
            if("self" in eachStack[0].f_locals.keys()):
                the_class = eachStack[0].f_locals["self"].__class__.__name__
                the_method = eachStack[0].f_code.co_name
                if(the_class != "basic"):
                    if(parentOnly):
                        path = "{}.{}()->".format(the_class, the_method)
                    else:
                        path += "{}.{}()->".format(the_class, the_method)
        return path

    def makeEmptyFile(self, fileName):
        self.makePathForFile(fileName)
        self.writeFileContent(fileName, '')

    def makePathForFile(self, file):
        base = os.path.dirname(file)
        self.makePath(base)

    def makePath(self, path):
        print(path)
        if(not os.path.exists(path) and path != ''):
            os.makedirs(path)
        else:
            log.error("Unable to read (OR) Path exists " + path)

    def isPathOK(self, path):
        return os.path.exists(path) and path != '' and path is not None

    def isPathFile(self, path):
        return os.path.isfile(path) and path != '' and path is not None

    def pickleSaveObject(self, obj, file=""):
        if(obj is None):
            log.error("Pass me valid object to save" + obj)
        className = obj.__class__.__name__
        if(file is None or file == ""):
            file = className + ".txt"
        base = os.path.dirname(file)
        if(not os.path.exists(base) and base != ''):
            os.makedirs(base)
        f = open(file, "wb")
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        f.close()
        print("Saved!" + className + "-" + file)

    def pickleLoadObject(self, file):
        x = None
        if(file is None or file == ""):
            log.error("Pass me file name to read and pass the object")
        if(os.path.exists(file)):
            try:
                f = open(file, "rb")
                x = pickle.load(f)
                f.close()
                log.info("File read and obj returned " +
                         file + " obj: " + x.__class__.__name__)
            except:
                log.error("Error loading the pickle. Passing default!")
        else:
            log.error("Error! File doesn't exist " + file)
        return x

    def smart_bool(self, s):
        if s is True or s is False:
            return s
        s = str(s).strip().lower()
        return not s in ['false', 'f', 'n', '0', '']

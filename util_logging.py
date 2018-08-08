import datetime


def logging(fpath, contents):
    with open(fpath, 'a') as f:
        logContents = '\n'
        logContents += '======================================================================================\n'
        logContents += '%s\n' % str(datetime.datetime.now())
        logContents += '%s\n' % contents
        logContents += '======================================================================================\n'
        f.write(logContents)
import time
b = time.strftime("%H:%M", time.localtime(1490942400))
a = time.strftime("05:10")
if b>a:
    print "ok"
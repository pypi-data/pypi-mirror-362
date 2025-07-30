#-*- coding:utf-8 -*-

import time
import sys

class comtimer_t:
    __m_nRetry = 0;
    __m_nMaxRetry = 0;
    __m_start=0;
    __m_timeout = 0;

    def	__init__(self):
        print('__init__')

        self.ClearRetry()
        self.SetMaxRetry(1)
        self.SetTimeout(1000)
        self.StartTimer()

    def __del__(self):
        print('__del__')

    def __millis(self):
        print('millis')
        return int(round(time.time() * 1000))

    def __StartTimer(self):
        self.m_start = self.millis();

    def DoTimerEvent(self):
        cur = self.millis();
        span = cur - self.m_start;

        if (span < 0):
            span += sys.maxint;

        if (span >= self.m_timeout):
            return False;
        return True;

    def SetTimeout(self,  ms):
        self.m_timeout = ms;

    def __SetMaxRetry(self, nMax):
        self.m_nMaxRetry = nMax;

    def __AddRetry(self):
        if (++self.m_nRetry > self.m_nMaxRetry):
            return False;
        return True;

    def __ClearRetry(self):
        self.m_nRetry = 0
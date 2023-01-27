from datetime import date,datetime
import tkinter

from codeparts.systems import Account

class staff:
    def checkban(self,account:Account) -> None:
        bantime = account.banuntil
        banyear=int(bantime.year)
        nowyear=date.today().year

        banmonth=int(bantime.month)
        nowmonth=date.today().month

        banday=int(bantime.day)
        nowday=date.today().day

        if banyear<nowyear:
            bantime = None
        elif banyear>nowyear:
            bantime = None
        else:
            if banmonth<nowmonth:
                bantime = None
            elif banmonth>nowmonth:
                bantime = None
            else:
                if banday<nowday:
                    bantime = None
                else:
                    bantime = None
        account.banuntil = bantime

class log:
    def __init__(self) -> None:
        self.screen=tkinter.Tk()
        self.t=tkinter.Text(self.screen,height=50,width=70,bg='white')
        self.t.grid(row=1,column=1)

    def log(self,text,printtime=True):
        a=self.t.get('1.0',tkinter.END)
        if len(a.splitlines())>51:
            self.t.delete('1.0', tkinter.END)
        date=datetime.now() if printtime==True else ''
        self.t.insert(tkinter.END,f'({date}) {text}\n')
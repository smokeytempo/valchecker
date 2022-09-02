from datetime import date

class staff:
    def checkban(self,bantime):
        banyear=int(bantime.year)
        nowyear=date.today().year

        banmonth=int(bantime.month)
        nowmonth=date.today().month

        banday=int(bantime.day)
        nowday=date.today().day

        if banyear<nowyear:
            return None
        elif banyear>nowyear:
            return bantime
        else:
            if banmonth<nowmonth:
                return None
            elif banmonth>nowmonth:
                return bantime
            else:
                if banday<nowday:
                    return None
                else:
                    return bantime
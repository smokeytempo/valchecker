import checkers

check=checkers.checkers()


class program():
    def get_accounts(self,filename):
        try:
            count=0
            with open (str(filename)+'.txt', 'r', encoding='UTF-8') as file:
                lines = file.readlines()
                ret=[]
                for logpass in lines:
                    count+=1
                    logpass=logpass.split(' - ')[0].replace('\n','').replace(' ','')
                    ret.append(logpass)
                print(f'detected {count} accounts\n')
                return ret
        except:
            return 0
                

    def main(self):
        print('VALchecker by liljaba1337')
        print('https://github.com/LIL-JABA\n')
        tofile=''
        fn='accounts'
        accounts=self.get_accounts(fn)
        if accounts==0:
            print('file "accounts.txt" was not found')
            return
        print('_____________')
        tofile+='_____________\n'
        for account in accounts:
            print(account+'\n\n')
            tofile+=account+'\n\n'
            skins=check.skins_en(account)
            if skins == False:
                print('INCORRECT LOGPASS')
                tofile+='INCORRECT LOGPASS\n'
            else:
                print(skins)
                tofile+=skins+'\n'
                rank=check.ranked(account)
                print(rank)
                tofile+=rank+'\n'
                lp=check.lastplayed(account)
                print('last game was on '+lp+'\n')
                tofile+='last game was on '+lp+'\n'
            print('_____________\n')
            tofile+='_____________\n'
        saveno=str(input('save data to "out.txt"? (y/n) >>>'))
        if saveno=='y':
            with open ('out.txt', 'w', encoding='UTF-8') as file:
                file.write(tofile)
        else:
            pass
    
pr=program()
pr.main()
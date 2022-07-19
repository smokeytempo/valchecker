import system
import checkers

check=checkers.checkers()
sys=system.system()

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
        print('''

██╗░░░██╗░█████╗░██╗░░░░░░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
██║░░░██║██╔══██╗██║░░░░░██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
╚██╗░██╔╝███████║██║░░░░░██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
░╚████╔╝░██╔══██║██║░░░░░██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
░░╚██╔╝░░██║░░██║███████╗╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
░░░╚═╝░░░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝ by liljaba1337
        ''')
        print('\nhttps://github.com/LIL-JABA\n')
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
            acctoken,enttoken,uid=sys.auth(logpass=account,response=4)
            skins=check.skins_en(enttoken,acctoken,uid)
            if skins == False:
                print('INCORRECT LOGPASS')
                tofile+='INCORRECT LOGPASS\n'
                print('_____________\n')
                tofile+='_____________\n'
                continue
            print(skins)
            tofile+=skins+'\n'
            print('\n')
            tofile+='\n'
            skinsru=check.skins_ru(enttoken,acctoken,uid)
            print(skinsru)
            tofile+=skinsru+'\n'
            rank=check.ranked(enttoken,acctoken,uid)
            print(rank)
            tofile+=f'{rank}\n'
            lp=check.lastplayed(uid)
            print(f'last game was on {lp}\n')
            tofile+=f'last game was on {lp}\n'
            print('_____________\n')
            tofile+='_____________\n'
        saveno=str(input('save output to "out.txt"? (y/n) >>>'))
        if saveno=='y':
            with open ('out.txt', 'w', encoding='UTF-8') as file:
                file.write(tofile)
        else:
            pass
    
pr=program()
pr.main()
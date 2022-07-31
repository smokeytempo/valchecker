class validsort():
    def sort(self):
        with open('simplefolder\\valid.txt','r',encoding='UTF-8') as f:
            lines=f.readlines()
        count=len(lines)
        sorted=0
        for line in lines:
            print(f'sorted {sorted}/{count}')

            # sort regions
            try:
                reg=line.split('[server: ')[1].split(']')[0].lower()
                if reg !='none':
                    with open(f'simplefolder\\sorted\\servers\\{reg}.txt','a',encoding='UTF-8') as f:
                        f.write(line)
            except:
                pass

            # sort skins
            try:
                skins=line.split('[skins: ')[1].split(']')[0].lower()
                if skins =='true':
                    with open(f'simplefolder\\sorted\\withskins.txt','a',encoding='UTF-8') as f:
                        f.write(line)
            except:
                pass

            # sort ranks
            try:
                rank=line.split('[rank: ')[1].split(']')[0].lower()
                if rank !='none':
                    with open(f'simplefolder\\sorted\\ranks\\{rank}.txt','a',encoding='UTF-8') as f:
                        f.write(line)
            except:
                pass

            #sort verifmail
            try:
                mail=line.split('[unverifiedmail: ')[1].split(']')[0].lower()
                if mail =='true':
                    with open(f'simplefolder\\sorted\\unverifiedmail.txt','a',encoding='UTF-8') as f:
                        f.write(line)
            except:
                pass
            sorted+=1
        print(f'sorted {sorted}/{count}')
        return
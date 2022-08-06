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

    def customsort(self):
        print('leave the string empty if this setting doesnt matter\n')
        region=str(input('enter region to search (eu; na; ap; br; kr; latam) >>>'))
        level=str(input('enter minimum level to search ("50" will search all accounts with level 50 or higher) >>>'))
        rank=str(input('enter rank to search (iron; bronze; silver; gold; platinum; diamond; ascendant; immortal; radiant) >>>'))
        skins=str(input('enter if this account should have skins (true; false) >>>'))
        mail=str(input('enter if this account should have unverified mail (true; false) >>>'))

        with open('simplefolder\\valid.txt','r',encoding='UTF-8') as f:
            lines=f.readlines()
        count=len(lines)
        sorted=0
        for line in lines:
            print(f'sorted {sorted}/{count}')
            line=line.lower()

            # sort regions
            try:
                if f'[server: {region}' in line:
                    if f'[rank: {rank}' in line:
                        if level!='':
                            try:
                                level=int(level)
                                levelacc=int(line.split('[lvl: ')[1].split(']')[0])
                            except:
                                continue
                        if levelacc>=level or level=='':
                            if f'[skins: {skins}' in line:
                                if f'[unverifiedmail: {mail}' in line:
                                    with open(f'simplefolder\\sorted\\custom.txt','a',encoding='UTF-8') as f:
                                        f.write(line)
            except:
                pass
            sorted+=1
        print(f'sorted {sorted}/{count}')
        return
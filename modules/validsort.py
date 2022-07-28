class validsort():
    def sort(self,key):
        toreturn=''
        with open('simplefolder\\valid.txt','r',encoding='UTF-8') as f:
            lines=f.readlines()
        for line in lines:
            if key.lower() in line.lower():
                toreturn+=line.replace('\n','')+'\n'
        return toreturn
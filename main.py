from collections import defaultdict
import pickle
import random

def update(names):
    for name in names:
        file=open(name+'.txt','r', errors='ignore')
        a=file.read().split()
        file.close()

        maps=dict()
        maps2=dict()
        maps3=dict()
        prev=''
        prev2=''
        for line in a:
            words=line.split()
            for i in words:
                if (prev2,prev,i)==('of','the','and'):
                    input('fnd')
                #print(prev2,prev,i)
                #i=i.lower()
                i=i.strip('.,?!"\'').lower()
                if prev not in maps:
                    maps[prev]=defaultdict(int)
                maps[prev][i]+=1
                if prev2 not in maps2:
                    maps2[prev2]=defaultdict(int)
                maps2[prev2][i]+=1
                if (prev2,prev) not in maps3:
                    maps3[(prev2,prev)]=defaultdict(int)
                maps3[(prev2,prev)][i]+=1
                if '.' in i or '!' in i or '?' in i:
                    prev2=prev[:]
                    prev=''
                else:
                    #print('before',prev2,prev,i)
                    prev2=prev[:]
                    prev=i[:]#.strip('.,?!"\'')
                    #print('after',prev2,prev,i)
        dbfile=open(name+'_stats','wb')
        pickle.dump(maps,dbfile)
        dbfile.close()
        dbfile2=open(name+'_stats2','wb')
        pickle.dump(maps2,dbfile2)
        dbfile2.close()
        dbfile3=open(name+'_stats3','wb')
        pickle.dump(maps3,dbfile3)
        dbfile3.close()

def avg(nums):
    return sum(nums)/len(nums)

def add(maps):
    fin=dict()
    for i in maps:
        #print(1)
        #print(i)
        for word in i:
            if word not in fin:
                fin[word]=defaultdict(list)
            for k in i[word]:
                #print(k,i[word][k])
                fin[word][k].append(i[word][k])
    fin2=dict()
    for i in fin:
        #print(i)
        fin2[i]=dict()
        for k in fin[i]:
            try:
                fin2[i][k]=avg(fin[i][k])
            except:
                print(k,fin[i][k])
    return fin2

def load(names):
    ms=[]
    for name in names:
        dbfile=open(name+'_stats','rb')
        maps=pickle.load(dbfile)
        dbfile.close()
        dbfile2=open(name+'_stats2','rb')
        maps2=pickle.load(dbfile2)
        dbfile2.close()
        dbfile3=open(name+'_stats3','rb')
        maps3=pickle.load(dbfile3)
        dbfile3.close()
        ms.append((maps,maps2,maps3))
    maps=add([i[0] for i in ms])
    maps2=add([i[1] for i in ms])
    maps3=add([i[2] for i in ms])
    return maps,maps2,maps3

def intersect(m1,m2):
    m3=[]
    for i in m1:
        if i in m2:
            m3.append(i)
    return m3

def get_likely(maps,maps2,maps3,word1,word2):
    if (word2,word1) in maps3:
        ms=[]
        b=maps3[(word2,word1)]
        for i in b:
            #print(i)
            ms.append((b[i],i))
        ms.sort()
        ms2=[i for i in reversed(ms)]
        ms3=[]
        bs=ms2[0][0]
        for i in ms2:
            #print(i)
            if i[0]==bs:
                ms3.append(i)
            else:
                break
        #print('fnd')
        return random.choice(ms3)[1]
    a=intersect(maps[word1].keys(),maps2[word2].keys())
    '''
    print(maps2[word2])
    print()
    print(maps[word1])
    print()
    print(a)
    print('and' in a)#'''
    if len(a)==0:# or True:
        raise e
        #print(a)
        b=[]
        for i in a:
            if word==i=='':
                continue
            b.append([i,maps[word][i]])
        ms=[]
        for i in b:
            ms.append((i[1],i[0]))
        ms.sort()
        ms2=[i for i in reversed(ms)]
        ms3=[]
        bs=ms2[0][0]
        for i in ms2:
            #print(i)
            if i[0]==bs:
                ms3.append(i)
            else:
                break
        return random.choice(ms3)[1]
    else:
        #print(a)
        b=[]
        #print()
        for i in a:
            #if word==i=='':
            #    continue
            #print(maps[word][i],maps2[word][i])
            b.append([i,maps[word1][i]+0.75*maps2[word2][i]])
        ms=[]
        for i in b:
            #print(b)
            ms.append((i[1],i[0]))
        ms.sort()
        ms2=[i for i in reversed(ms)]
        ms3=[]
        bs=ms2[0][0]
        for i in ms2:
            #print(i)
            if i[0]==bs:
                ms3.append(i)
            else:
                break
        return random.choice(ms3)[1]
    return a[0]
    

def main(FILENAMES,words,num,upd=False):
    word2=words.split()[-2]
    word1=words.split()[-1]
    if upd:# or True:
        x=update(FILENAMES)
    #print(x)
    
    if word2!='':
        print(words,end=' ')
    maps,maps2,maps3=load(FILENAMES)
    #print('\n'*5)
    #print(1,list(maps3.keys())[5],1)
    #print('\n'*5)
    for i in range(num):
        word=get_likely(maps,maps2,maps3,word1,word2)
        word2,word1=word1,word
        print(word,end=' ')
    print()

if __name__=='__main__':
    main(['wof_5'],'he said',100,False)

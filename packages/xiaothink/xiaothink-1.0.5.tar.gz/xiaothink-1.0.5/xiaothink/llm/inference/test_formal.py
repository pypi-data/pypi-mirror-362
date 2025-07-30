
import xiaothink.llm.inference.test as test

#import xiaothink.llm.inference.test as test
#form




class QianyanModel:
    def __init__(self,ckpt_dir=r'E:\小思框架\论文\ganskchat\ckpt_test_40_3_1_t1_cloud',
               MT=40.31,
                 vocab=r'E:\小思框架\论文\ganskchat\vocab_lx3.txt'):
        self.model,self.d=test.load(ckpt_dir=ckpt_dir, model_type=MT,
                                    vocab=vocab)
        self.his=''

    def chat_SingleTurn(self,t,temp=0.8,maxlen=1200,window=2048,
                        form=1,ontime=True,loop=True,stop=None):#0.85
        
        if form==0:
            inp=f'{{"instruction": "{t}", "input": "", "output": "'
            stopc=['"}\r\n',
                   '"}\n\r',
                   '"}\n',
                   '", "input"',
                   '", "i',
                   '"}',
                   ]
        elif form==1:
            inp='{"conversations": [{"role": "user", "content": {inp}}, {"role": "assistant", "content": "'.replace('{inp}',t)
            stopc=[
                    '"}]}',
                    '"}',
                ]
        else:
            print('Err')
            
            return '-1: form error'
        if stop:
            stopc.append(stop)
        funct=None
        if ontime:
            funct=lambda a:print(a,end='',flush=True)
        if loop:
            inf=test.generate_texts_untilstr_loop
        else:
            inf=test.generate_texts_untilstr
            
        #print(funct)
        re=inf(self.model, self.d, inp,num_generate=maxlen,
                                 every=funct,
                                 temperature=temp,#0.8
                                stop_c=stopc,
                                window=window
                                    #q=[0.6,0.4]
                                    )
        self.model.reset_states()
        return re

    def add_his(self,q,a,form=1):#0.85
        q=q.replace('\n','\\n')
        a=a.replace('\n','\\n')
        if form==0:
            if self.his!='':
                self.his+='\\nHuman: '+text+'\\nAssistant:'
            else:
               self.his+='Human: '+text+'\\nAssistant:'
            #print('his',self.his)
            t=self.his
            
            inp=f'{{"instruction": "{t}", "input": "", "output": "'
            stopc=['"}\r\n',
                   '"}\n\r',
                   '"}\n',
                   '", "input"',
                   '", "i',
                   '"}',
                   '\\nHuman:',
                   ]
        elif form==1:
            if self.his!='':
                self.his+=', {"role": "user", "content": "{inp}"}'.replace('{inp}',q)
      
            else:
                self.his='{"role": "user", "content": "{inp}"}'.replace('{inp}',q)


            inp='{"conversations": [{his}, {"role": "assistant", "content": "'.replace('{his}',self.his)
            stopc=[
                    '"}]}',
                    '"}',
                ]
        else:
            print('Err')
            return '-1: form error'

        re=a
        if form==0:
            self.his+=re
        elif form==1:
            self.his+=', {"role": "assistant", "content": "{inp}"}'.replace('{inp}',re)
      
        return re
    
    def chat(self,text,temp=0.68,max_len=150,form=1,ontime=True,window=2048,
             loop=True,pre_text='',repetition_penalty=1.2):
        text=text.replace('\n','\\n')
        if form==0:
            if self.his!='':
                self.his+='\\nHuman: '+text+'\\nAssistant:'
            else:
               self.his+='Human: '+text+'\\nAssistant:'
            #print('his',self.his)
            t=self.his
            
            inp=f'{{"instruction": "{t}", "input": "", "output": "'
            stopc=['"}\r\n',
                   '"}\n\r',
                   '"}\n',
                   '", "input"',
                   '", "i',
                   '"}',
                   '\\nHuman:',
                   ]
        elif form==1:
            if self.his!='':
                self.his+=', {"role": "user", "content": "{inp}"}'.replace('{inp}',text)
      
            else:
                self.his='{"role": "user", "content": "{inp}"}'.replace('{inp}',text)

            #print(self.his)
            inp='{"conversations": [{his}, {"role": "assistant", "content": "'.replace('{his}',self.his)
            stopc=[
                    '"}]}',
                    '"}',
                ]
        else:
            print('Err')
            return '-1: form error'
        funct=None
        if ontime:
            funct=lambda a:print(a,end='',flush=True)
            print('\n【实时输出】')
        #print(funct)
        if loop:
            inf=test.generate_texts_untilstr_loop
        else:
            inf=test.generate_texts_untilstr
        re=pre_text+inf(self.model, self.d, inp+pre_text,num_generate=max_len,
                                 every=funct,
                                 temperature=temp,#0.8
                                stop_c=stopc,
                        window=window,
                        repetition_penalty=repetition_penalty
                                    #q=[0.6,0.4]
                                    )
        if form==0:
            self.his+=re
        elif form==1:
            self.his+=', {"role": "assistant", "content": "{inp}"}'.replace('{inp}',re)
      
        return re
    

    def clean_his(self):
        self.his=''



import subprocess
import time

def jtalk(t):
    open_jtalk=['open_jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/usr/share/hts-voice/htsvoice-tohoku-f01/tohoku-f01-neutral.htsvoice']
    speed=['-r','1.0']
    outwav=['-ow','voice.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav 
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(t.encode('utf-8'))
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','voice.wav']
    subprocess.Popen(aplay)

def main():
    jtalk('さんー、にーー、いちー。ぱしゃり')
    time.sleep(0.5)
    

if __name__ == '__main__':
    main()

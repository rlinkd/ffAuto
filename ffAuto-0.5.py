#!/usr/bin/env python
import argparse,os,subprocess,sys

####    GLOBALS

formats = ['3g2','3gp','aac','ac3','aiff','alsa','amr','ape','asf','avi','dv','f4v','ffm','flac'
          ,'flv','ipod','m4v','matroska','mov','mp3','mp4','m4a','3gp','3g2','mpg','mpeg','mvi',
          'oga','ogg','ogv','oss','swf','wav','webm','wma','wmv','x11grab']

####	FUNCTIONS

def DIR(IN):
    """verify input directory"""
    if os.path.isdir("%s" % IN):
        return str(IN)
    else:
        raise ValueError

def format(filetype):
    """verify output filetype"""
    if filetype.lower() in formats:
        return filetype
    else:
        raise ValueError

def fps(rate):
    """verify FPS format"""
    if float(rate) > 0:
        return float(rate)
    else:
        raise ValueError

####	PROCESS INPUT(S)

parser = argparse.ArgumentParser(description='read program inputs.')
parser.add_argument(type=DIR,dest='IN',metavar='DIR',help='directory containing video assets')
parser.add_argument('-f',type=format,dest='filetype',help='output file format')
parser.add_argument('-r',type=fps,dest='fps',help='output file FPS')
parser.add_argument('-R','--recursive',dest='R',action='store_true')
parser.add_argument('-y',action='store_true')
args = parser.parse_args()

####	MAIN

call = ""

for file in os.listdir(args.IN):
    """call ffmpeg for DIR files || call self for file ('-R','--recursive')"""
    if args.R and os.path.isdir("%s" % os.path.join(args.IN,file)):
        call = ""
        for arg in sys.argv:
            if arg == args.IN:
                call += "\'%s\' " % os.path.join(os.path.splitext(arg)[0],file)
            else:
                call += "\'%s\' " % arg
        subprocess.Popen("%s" % call, shell=True).wait()
    elif file.lower().endswith(tuple(formats)):
        call += "ffmpeg -i \'%s\' " % os.path.join(args.IN,file)
        if args.fps:
            call += "-r %s " % args.fps
        if args.filetype:
            call += "\'%s.%s\' " % (os.path.join(args.IN,os.path.splitext(file)[0]),args.filetype)
        else:
            call += "\'%s\' " % os.path.join(args.IN,file)
        if args.y:
            call += "-y "
        subprocess.Popen("%s" % call, shell=True).wait()

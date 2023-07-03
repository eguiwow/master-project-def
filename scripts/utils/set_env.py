import os
#
os.environ['GL2_H']='145.108.225.7'
os.environ['GL3_H']='145.108.225.6'
os.environ['GL4_H']='145.108.225.9'
os.environ['GL5_H']='145.108.225.16'
#
os.environ['GL2_U']='ander'
os.environ['GL3_U']='ander'
os.environ['GL4_U']='ander'
os.environ['GL5_U']='ander'
#
os.environ['GL2_P']='supersecretpassword'
os.environ['GL3_P']='supersecretpassword'
os.environ['GL4_P']='supersecretpassword'
os.environ['GL5_P']='supersecretpassword'

print(os.environ['GL5_P'])
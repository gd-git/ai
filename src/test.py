import os

dirname=os.path.dirname(__file__)

with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
    
def test1() :
    print("TEST1 ...")

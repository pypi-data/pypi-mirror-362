import os

d = os.listdir(".")

for fn in d : 
  if fn.find(".py")<0 : continue
  if fn.find("Brunel")==0 or fn.find("__")>=0 : continue
  
  with open(f"Brunel_{fn}", "w") as bf :
    with open(fn) as f : 
      l = f.read()
      if l.find('"expression"')>=0 or l.find('"branches"')>=0 : 
        print(l)
        ln = l.replace("probe_", "probe_Brunel_")
        bf.write(ln)
      else : 
        bf.write(l)


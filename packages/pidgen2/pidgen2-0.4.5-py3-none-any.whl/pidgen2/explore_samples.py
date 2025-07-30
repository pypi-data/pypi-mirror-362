import json

with open("samples/samples.json") as f : 
  d = json.load(f)
  
sample = "2024_WithUT_block1_v1-MagUp-K"

ds = d[sample]

files = ds["files"]
sw_dir = ds["sweight_dir"]
tuple_names = ds["tuple_names"]
probe_prefix = ds["probe_prefix"]

print(files)
print(sw_dir)
print(tuple_names)
print(probe_prefix)

for f in files : 
  basename = f.split("/")[-1].split(".")[0]
  swf = sw_dir + "/" + basename + ".pid_turboraw_tuple_sweights.root"
  print(swf)

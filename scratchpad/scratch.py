
#%%

from shapely.geometry import Point, MultiPoint

tmp = []
for x in range(5):
   p = Point(x, 1, 2)
   tmp.append(p)

m = MultiPoint(tmp)
print(m)
# %%
m
# %%
elevs = [p.z for p in m]
print(elevs)
# %%

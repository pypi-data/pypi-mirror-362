# Usage Examples

## Basic Example

```python
from h2gis import H2GIS
import geopandas as gpd
import pandas as pd
from shapely.wkt import loads as wkt_loads
import json

# Connexion and data import
h2gis = H2GIS("/home/mael/test", "sa", "sa")
h2gis.execute("DROP TABLE TEST IF EXISTS;")
h2gis.execute("CALL GeoJsonRead('./test.geojson');")

# Fetch
fetch = h2gis.fetch("SELECT * FROM TEST LIMIT 2;")
df = pd.DataFrame(fetch)

df["geometry"] = df["THE_GEOM"].apply(wkt_loads)
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
print(gdf)

if len(gdf) >= 2:
    dist = gdf.geometry.iloc[0].distance(gdf.geometry.iloc[1])
    print(f"Distance between the first two geometries (in meters) : {dist:.2f} m")
else:
    print("There are less than two geometries")

print("connected : ", h2gis.isConnected())
h2gis.close()
```

## Custom Native Library Path

```python
db = H2GIS(lib_path="/custom/path/h2gis.so")
```

## Notes
- By default, the native `.so`, `.dll` are already included in the package, in the `lib` folder.

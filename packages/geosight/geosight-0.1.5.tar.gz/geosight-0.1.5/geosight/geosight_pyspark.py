
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import (
    StringType, 
    FloatType, 
    IntegerType, 
    DoubleType,
    ArrayType,
    MapType,
    StructType,
    StructField
)
from geosight.geosight import (
    calculate_distance,
    get_custom_grid,
    get_h3_grid,
    get_lat_long,
    decode_custom_geohash,
    get_centroid,
    get_surrounding_grid,
    get_polygon
)

# UDF for calculating distance between two coordinates
calculate_distance_udf = udf(
    lambda lat1, lon1, lat2, lon2: calculate_distance(lat1, lon1, lat2, lon2),
    DoubleType()
)

# UDF for getting custom grid ID
get_custom_grid_udf = udf(
    lambda lat, lon, grid_size, initial_hash=None: get_custom_grid(lat, lon, grid_size, initial_hash),
    StringType()
)

# UDF for getting H3 grid
get_h3_grid_udf = udf(
    lambda lat, lon, grid: get_h3_grid(lat, lon, grid),
    StringType()
)

# UDF for getting lat/long from distance and bearing
get_lat_long_udf = udf(
    lambda lat, lon, distance, bearing: get_lat_long(lat, lon, distance, bearing),
    ArrayType(DoubleType())
)

# UDF for decoding custom geohash - returns a map with points and centroid
decode_custom_geohash_udf = udf(
    lambda grid_id: decode_custom_geohash(grid_id),
    MapType(
        StringType(),
        ArrayType(DoubleType())
    )
)

# UDF for getting centroid coordinates
get_centroid_udf = udf(
    lambda lat, lon, grid_size: get_centroid(lat, lon, grid_size),
    ArrayType(DoubleType())
)

# UDF for getting surrounding grids
get_surrounding_grid_udf = udf(
    lambda grid_id, grid_surrounding_step=None, grid_surrounding_size=None: get_surrounding_grid(
        grid_id, grid_surrounding_step, grid_surrounding_size
    ),
    ArrayType(StringType())
)

# UDF for getting polygon WKT representation
get_polygon_udf = udf(
    lambda grid_id: get_polygon(grid_id),
    StringType()
)
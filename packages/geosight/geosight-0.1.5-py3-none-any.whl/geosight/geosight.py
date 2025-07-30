from math import radians,sin,cos,asin,sqrt,atan2,degrees
import geohash
import h3

def calculate_distance(
    lat1:float,
    lon1:float,
    lat2:float,
    lon2:float
)->float:
    """
    Calculate the distance between two coordinates on Earth.

    Args:
        lat1 (float): Latitude of the first coordinate.
        lon1 (float): Longitude of the first coordinate.
        lat2 (float): Latitude of the second coordinate.
        lon2 (float): Longitude of the second coordinate.

    Returns:
        float: The distance between the two coordinates in meters.
    """

    lon1 = radians(float(lon1))
    lon2 = radians(float(lon2))
    lat1 = radians(float(lat1))
    lat2 = radians(float(lat2))
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in meters. Use 3956 for miles
    r = 6371 * 1000
    
    distance = c*r
    return(distance)
  
def get_custom_grid(
    lat:float,
    lon:float,
    grid_size:int,
    initial_hash:str=None
)-> str:
    """
    Create a custom grid ID based on the given latitude, longitude, and grid size.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        grid_size (int): Size of the grid in meters.

    Returns:
        str: A string representing the grid ID in the format of "<grid_size>_<vertical_axis>_<horizontal_axis>".
    """
    if initial_hash:
        initial_lat,initial_lon = geohash.decode(initial_hash)
    else:
        initial_lat = 0
        initial_lon = 94.9527682

    lat = float(lat)
    lon = float(lon)
    distance_horizontal = calculate_distance(initial_lat,lon,initial_lat,initial_lon)
    distance_vertical = calculate_distance(lat,initial_lon,initial_lat,initial_lon)
    
    step_horizontal = int(distance_horizontal/grid_size)
    step_vertical = int(distance_vertical/grid_size)
    
    if lat-initial_lat>=0:
        if lon-initial_lon>=0:
            grid_id = str(grid_size) + '_' + str(step_vertical) + '_' + str(step_horizontal)
        else:
            grid_id = str(grid_size) + '_' + str(step_vertical) + '_-' + str(step_horizontal)
    else:
        if lon-initial_lon>=0:
            grid_id = str(grid_size) + '_-' + str(step_vertical+1) + '_' + str(step_horizontal)
        else:
            grid_id = str(grid_size) + '_-' + str(step_vertical) + '_-' + str(step_horizontal)
            
    if initial_hash:
        grid_id = initial_hash+'_'+grid_id

    return grid_id

def get_h3_grid(lat, lon, grid):
    """
    Convert geographic coordinates to H3 hexagonal grid index.
    
    This function takes latitude and longitude coordinates and converts them
    to an H3 hexagonal grid cell identifier at the specified resolution level.
    H3 is a hierarchical hexagonal geospatial indexing system developed by Uber.
    
    Parameters
    ----------
    lat : float
        Latitude coordinate in decimal degrees (WGS84).
        Valid range: -90.0 to 90.0
    lon : float
        Longitude coordinate in decimal degrees (WGS84).
        Valid range: -180.0 to 180.0
    grid : int
        H3 resolution level (0-15).
        - 0: Largest hexagons (~1000km edge length)
        - 15: Smallest hexagons (~0.5m edge length)
        Higher numbers provide finer spatial resolution.
    
    Returns
    -------
    str
        H3 index as a hexadecimal string representing the hexagonal cell
        that contains the input coordinates at the specified resolution.
    """
    return h3.geo_to_h3(lat, lon, grid)

  
def get_lat_long(
    lat:float,
    lon:float,
    d:float,
    bear:float
):
    """
    Calculate latitude and longitude from a starting point, distance, and bearing.

    Args:
        lat (float): Starting latitude in degrees.
        lon (float): Starting longitude in degrees.
        d (float): Distance to travel in meters.
        bear (float): Bearing in degrees.

    Returns:
        Tuple[float, float]: A tuple containing the latitude and longitude of the destination point in degrees.
    """
    lon = radians(lon)
    lat = radians(lat)
    bear = radians(bear)
    R = 6371 * 1000 #Radius of the Earth in meters

    lat2 = asin( sin(lat)*cos(d/R) +
         cos(lat)*sin(d/R)*cos(bear))

    lon2 = lon + atan2(sin(bear)*sin(d/R)*cos(lat),
                 cos(d/R)-sin(lat)*sin(lat2))

    lat2 = degrees(lat2)
    lon2 = degrees(lon2)

    return lat2,lon2


def decode_custom_geohash(
    grid_id:str
):
    """
    Converts a grid ID to latitude and longitude coordinates for each angle.

    Args:
        grid_id (str): The ID of the grid to convert.

    Returns:
        dict: A dictionary containing the latitude and longitude coordinates for each angle, as well as the centroid of the grid.
    """
    list_grid_id = grid_id.split('_')
    if len(list_grid_id)>3:
        initial_hash,interval,step_north,step_east = list_grid_id
        initial_lat,initial_lon = geohash.decode(initial_hash)
    else:
        interval,step_north,step_east = list_grid_id
        initial_lat = 0
        initial_lon = 94.9527682

    interval = int(interval)
    direction_north = step_north[0]
    distance_east = int(step_east) * interval

    if direction_north!='-':
        distance_north = int(step_north) * interval
        bear_vertical = 0
    else:
        distance_north = (int(step_north)+1) * interval
        bear_vertical = 180
    
    distance_north = abs(distance_north)
    res_n1 = get_lat_long(initial_lat,initial_lon,distance_north,bear_vertical)
    res_e1 = get_lat_long(initial_lat,initial_lon,distance_east,90)
    res_ne1 = [res_n1[0],res_e1[1]]
    
    res_n2 = get_lat_long(res_ne1[0],res_ne1[1],interval,bear_vertical)
    res_e2 = get_lat_long(res_ne1[0],res_ne1[1],interval,90)
    res_ne2 = [res_n2[0],res_e2[1]]
    
    res_n_centroid = get_lat_long(res_ne1[0],res_ne1[1],interval/2,bear_vertical)[0]
    res_e_centroid = get_lat_long(res_ne1[0],res_ne1[1],interval/2,90)[1]
    res_ne_centroid = [res_n_centroid,res_e_centroid]
    
    dict_rect = {
        'point1':res_ne1,
        'point2':[res_ne1[0],res_ne2[1]],
        'point3':res_ne2,
        'point4':[res_ne2[0],res_ne1[1]],
        'centroid':res_ne_centroid
    }

    return dict_rect

def get_centroid(
    lat:float,
    lon:float,
    grid_size:int
):
    grid_id = get_custom_grid(
        lat,
        lon,
        grid_size
    )
    res_ne_centroid = decode_custom_geohash(grid_id)['centroid']
    return res_ne_centroid

def get_surrounding_grid(
    grid_id,
    grid_surrounding_step=None,
    grid_surrounding_size=None,
):
    """
    Returns a list of grid IDs that are in the surrounding area of a given grid ID.
    
    Args:
        grid_id (str): The ID of the grid to find the surrounding grids for.
        grid_surrounding_step (int): The number of steps in the north and east directions to search for surrounding grids. Defaults to None.
        grid_surrounding_size (int): The size of the grid surrounding area. Defaults to None.
        
    Returns:
        list: A list of grid IDs that are in the surrounding area of the given grid ID.
    """
    list_surrounding_grid = []
    list_grid_id = grid_id.split('_')
    if len(list_grid_id)>3:
        initial_hash,interval,step_north,step_east = list_grid_id
    else:
        interval,step_north,step_east = list_grid_id
        initial_hash = None

    interval = int(interval)
    step_north = int(step_north)
    step_east = int(step_east)
    
    if grid_surrounding_size:
        grid_surrounding_step = (grid_surrounding_size//interval-1)//2
    
    steps = range(-grid_surrounding_step,grid_surrounding_step+1)
    for i in steps:
        temp_north = step_north+i
        for j in steps:
            temp_east = step_east+j
            if initial_hash:
                temp_grid = f'{initial_hash}_{interval}_{temp_north}_{temp_east}'
            else:
                temp_grid = f'{interval}_{temp_north}_{temp_east}'
            list_surrounding_grid.append(temp_grid)
      
    return list_surrounding_grid

def get_polygon(grid_id: str) -> str:
    """
    Create a WKT polygon representation for a given grid ID.

    Args:
        grid_id (str): The ID of the grid to convert to a polygon.

    Returns:
        str: WKT representation of a polygon.
    """
    decoded_grid = decode_custom_geohash(grid_id)
    
    # Create the WKT polygon string
    polygon_wkt = "POLYGON(("
    
    # Add each point of the polygon to the WKT string
    for point in decoded_grid['point1'], decoded_grid['point2'], decoded_grid['point3'], decoded_grid['point4']:
        lat, lon = point
        polygon_wkt += f"{lon} {lat}, "
    
    # Close the polygon by repeating the first point
    polygon_wkt += f"{decoded_grid['point1'][1]} {decoded_grid['point1'][0]}"
    
    # Close the WKT polygon string
    polygon_wkt += "))"
    
    return polygon_wkt
  
if __name__ == '___main___':
    True

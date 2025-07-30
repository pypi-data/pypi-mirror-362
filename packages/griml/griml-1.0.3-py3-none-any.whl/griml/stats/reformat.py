#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopandas as gpd
 
def aggregate(geofile, col_name='lake_id'):
    '''Generate areal statistics for aggregated geodataframe. Aggregation is 
    determined from a given column name
    
    Parameters
    ----------
    geofile : gpd.GeoDataFrame
        Dataframe to perform aggregation statistics on
    col_name: str, optional
        Column name to aggregate dataframe by. The default is "lake_id"
    
    Returns
    -------
    agg_geofile : gpd.GeoDataFrame
        Aggregated dataframe with updated areal statistics
    ''' 
    print('\nLoading geodataframe...') 
    
    agg_geofile = geofile.dissolve(by=col_name)
    agg_geofile = agg_geofile.drop(['area','length'], axis=1)
    agg_geofile['area_m'] = agg_geofile['geometry'].area
    agg_geofile['length_m'] = agg_geofile['geometry'].length
    agg_geofile['area_km'] = agg_geofile['area_m']/1000000
    agg_geofile['length_km'] = agg_geofile['length_m']*0.001
    
    print('Number of dissolved lake features exported: ' + str(len(agg_geofile['Source'].tolist())))
    
    return agg_geofile


def centroids(geofile): 
    '''Generate centroids for geodataframe
    
    Parameters
    ----------
    geofile : gpd.GeoDataFrame
        Dataframe to obtain centroids for
    
    Returns
    -------
    geofile : gpd.GeoDataFrame
        Dataframe with centroid information
    ''' 
    pts = [s['geometry'].centroid for i,s in geofile.iterrows()]
    geofile['centroid'] = pts   
    return geofile

if __name__ == "__main__": 
    file1 = 'ALL-ESA-GRIML-IML-fv2.gpkg'
    file3 = 'ALL-ESA-GRIML-IML-fv2_centroid.gpkg'
    
    gdf = gpd.read_file(file1)
    agg = aggregate(gdf)
    agg_c = centroids(agg)
    
    agg_c.to_file(file3)

    print('Finished')

from pybalmorel import Balmorel

m = Balmorel('../../Balmorel', gams_system_directory='/opt/gams/48.5')
m.collect_results()
m.results.plot_map('N30_DA_operun', 2050, 'Electricity', path_to_geofile='/home/mberos/Repos/balmorel-preprocessing/src/ClusterOutput/clustering.gpkg', geo_file_region_column='index',
                   save_fig=True)
#Import modules
import arcpy
import gdb_tools
import datetime

#Set environments 
#Databases
gdb = r'\\metanoia\geodata\PW\sw_tech\Duplicates\data\dups.gdb'
sde = r'Database Connections\Connection to GISPRDDB direct connect.sde'

arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

#Data pointers
sde_parcel_area = sde + r'\cvgis.CITY.Cadastre\cvGIS.CITY.parcel_area'
sde_parcel_point = sde + r'\cvgis.CITY.Cadastre\cvgis.CITY.parcel_point'

#Get data as string and replace - with _
str_today = str(datetime.date.today()).replace('-','')[2:]

intersect = gdb + r'\int' + '_' + str_today
overlap_out = gdb + r'\overlap' + '_' + str_today

arcpy.Delete_management(intersect)
arcpy.Intersect_analysis([sde_parcel_area, sde_parcel_point], intersect)

def overlap():
  cursor_fields = ['GPIN', 'PARCELSPOL']
  #Create cursor for values of update_fields
  count = 0
  with arcpy.da.UpdateCursor(intersect, cursor_fields) as cursor:
    #For each row in the cursor, if cursor fields do not equal each other
    for row in cursor:
      if row[0] != row[1]:
        print 'Parcel Poly GPIN: {0} overlaps Parcel '  \
        'Point PARCELSPOL: {1}'.format(row[0],row[1])
        count += 1
    print 'Number of overlapping features: ', count

  arcpy.Select_analysis(intersect, overlap_out, 'GPIN <> PARCELSPOL')
  print 'Output at {0}'.format(overlap_out)

overlap()


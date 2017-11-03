#Import modules
import arcpy
import datetime

#Set environments 
#Databases
gdb = r'\\metanoia\geodata\PW\sw_tech\Cadastre\data\cadastre.gdb'
sde = r'Database Connections\Connection to GISPRDDB direct connect.sde'

arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

#Data pointers
sde_parcel_area = sde + r'\cvgis.CITY.Cadastre\cvGIS.CITY.parcel_area'
sde_parcel_point = sde + r'\cvgis.CITY.Cadastre\cvgis.CITY.parcel_point'

#Get data as string and replace - with _
str_today = str(datetime.date.today()).replace('-','')[2:]
intersect = r'{0}\int_{1}'.format(gdb, str_today)

def overlap():
  ''' 
  Checks that GPIN from Parcel Polygon layer matches PARCELSPOL from Parcel 
  Point layer. Exports conflicts to overlap_YYMMDD in gdb
  '''
  arcpy.Intersect_analysis([sde_parcel_area, sde_parcel_point], intersect)
  print '-- Overlap Analysis --'
  cursor_fields = ['GPIN', 'PARCELSPOL']
  #Create cursor for values of cursor_fields
  count = 0
  with arcpy.da.UpdateCursor(intersect, cursor_fields) as cursor:
    #For each row in the cursor, if cursor fields do not equal each other
    for row in cursor:
      if row[0] != row[1]:
        print 'Parcel Poly GPIN: {0} overlaps Parcel '  \
        'Point PARCELSPOL: {1}'.format(int(row[0]), int(row[1]))
        count += 1
    print 'Number of overlapping features: ', count

  overlap_out = r'{0}\overlap_{1}'.format(gdb, str_today)
  try:
    arcpy.Select_analysis(intersect, overlap_out, 'GPIN <> PARCELSPOL')
  except:
    print 'There are no instances where GPIN <> PARCELSPOL'
  print 'Overlap output at {0}'.format(overlap_out)
  print '\n'
  arcpy.Delete_management(intersect)

def dups(feat, field):
  ''' 
  Checks that field from Parcel Polygon layer is a unique ID 
  Exports conflicts to [field]_YYMMDD in gdb
  '''
  out_name = r'{0}\{1}_{2}'.format(gdb, field, str_today)
  print '-- Duplicate Analysis --'
  cursor_fields = [field]
  attributes = []
  #Create cursor for values of cursor_fields
  with arcpy.da.SearchCursor(feat, cursor_fields) as cursor:
    #For each row in the cursor, if cursor fields do not equal each other
    for row in cursor:
      attributes.append(str(row[0]))
  seen = []
  dup_list = []
  for attribute in attributes:
    if attribute not in seen:
      seen.append(attribute)
    elif attribute in seen and attribute not in dup_list:
      dup_list.append(attribute)
  for dup in dup_list:
    print '{0}: '.format(field), dup, 'Count: ', attributes.count(dup)
  sql_list = str(dup_list).replace('[', '(').replace(']',')') 
  expression = '{0} in {1}'.format(field, sql_list)
  arcpy.Select_analysis(feat, out_name, expression)
  print 'Duplicate {0} output at {1}'.format(field, out_name)


overlap()
dups(sde_parcel_area, 'PIN')
dups(sde_parcel_area, 'GPIN')





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

#Output Names
intersect = gdb + r'\int' + '_' + str_today
overlap_out = gdb + r'\overlap' + '_' + str_today
dup_out = gdb + r'\dup' + '_' + str_today

def int_parcels():
  arcpy.Intersect_analysis([sde_parcel_area, sde_parcel_point], intersect)

def overlap():
  ''' 
  Checks that GPIN from Parcel Polygon layer matches PARCELSPOL from Parcel 
  Point layer. Exports conflicts to overlap_YYMMDD in gdb
  '''
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

  arcpy.Select_analysis(intersect, overlap_out, 'GPIN <> PARCELSPOL')
  print 'Overlap output at {0}'.format(overlap_out)
  print '\n'
  arcpy.Delete_management(intersect)

def dups():
  ''' 
  Checks that PIN from Parcel Polygon layer is a unique ID 
  Exports conflicts to dup_YYMMDD in gdb
  '''
  print '-- Duplicate PIN Analysis --'
  cursor_fields = ['PIN']
  pins = []
  #Create cursor for values of cursor_fields
  with arcpy.da.SearchCursor(sde_parcel_area, cursor_fields) as cursor:
    #For each row in the cursor, if cursor fields do not equal each other
    for row in cursor:
      pins.append(str(row[0]))
  seen = []
  dup_list = []
  for pin in pins:
    if pin not in seen:
      seen.append(pin)
    elif pin in seen and pin not in dup_list:
      dup_list.append(pin)
  for dup in dup_list:
    print 'PIN: ', dup, 'Count: ', pins.count(dup)
  sql_list = str(dup_list).replace('[', '(').replace(']',')') 
  expression = 'PIN in {0}'.format(sql_list)
  arcpy.Select_analysis(sde_parcel_area, dup_out, expression)
  print 'Duplicate PIN output at {0}'.format(dup_out)

int_parcels()
overlap()
dups()





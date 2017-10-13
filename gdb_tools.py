import arcpy

def wipe(geodatabase):
  '''Deletes everything in a given geodatabase'''
  arcpy.env.workspace = geodatabase

  data_types = [
    arcpy.ListDatasets(), 
    arcpy.ListFeatureClasses(), 
    arcpy.ListRasters(), 
    arcpy.ListTables()
    ]
  for datasets in data_types:
    for data in datasets:
      arcpy.Delete_management(data)

def check_del(geodatabase, dataset):
  arcpy.env.workspace = geodatabase
  try: 
    arcpy.Delete_management(dataset)
  except:
    pass

    
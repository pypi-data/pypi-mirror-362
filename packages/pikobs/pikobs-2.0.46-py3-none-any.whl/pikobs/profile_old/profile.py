
"""

Description
------------

This module calculates the  profile statistics of observations over a period, for example:
  

    .. image:: ../../../docs/source/_static/profile.png
      :alt: Clasic time serie


"""




import sqlite3
import pikobs
import re
import os
from  dask.distributed import Client
import numpy as np
import sqlite3
import os
import re
import sqlite3


def create_timeserie_table(family, 
                           new_db_filename,
                           existing_db_filename, 
                           region_seleccionada, 
                           selected_flags, 
                           FONCTION, 
                           varno):
    """
    Create a new SQLite database with a 'moyenne' table and populate it with data from an existing database.

    Args:
    new_db_filename (str): Filename of the new database to be created.
    existing_db_filename (str): Filename of the existing database to be attached.
    region_seleccionada (str): Region selection criteria.
    selected_flags (str): Selected flags criteria.
    FONCTION (float): Value for sum_fonction column.
    boxsizex (float): Value for boxsizex column.
    boxsizey (float): Value for boxsizey column.

    Returns:
    None
    """

    
    pattern = r'(\d{10})'
    match = re.search(pattern, existing_db_filename)

    if match:
        date = match.group(1)
       
    else:
        print("No 10 digits found in the string.")
    
    
    # Connect to the new database
  
    new_db_conn = sqlite3.connect(new_db_filename, uri=True, isolation_level=None, timeout=999)
    new_db_cursor = new_db_conn.cursor()
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    LAT1, LAT2, LON1, LON2 = pikobs.regions(region_seleccionada)
    LATLONCRIT = pikobs.generate_latlon_criteria(LAT1, LAT2, LON1, LON2)
    flag_criteria = pikobs.flag_criteria(selected_flags)

    # Attach the existing database
    new_db_cursor.execute(f"ATTACH DATABASE '{existing_db_filename}' AS db;")
    # load extension CMC 
    new_db_conn.enable_load_extension(True)
    extension_dir = f'{os.path.dirname(pikobs.__file__)}/extension/libudfsqlite-shared.so'
    new_db_conn.execute(f"SELECT load_extension('{extension_dir}')")
  
    # Create the 'moyenne' table in the new database if it doesn't exist
    new_db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            DATE INTEGER, 
            varno INTEGER,
            VCOORD FLOAT,
            SUMOMP FLOAT,
            SUMOMA FLOAT, 
            SUMOMP2 FLOAT, 
            SUMOMA2 FLOAT,
            SUMBIAS_CORR  FLOAT,
            N Inter,
            id_stn texto
        );
    """)

    # Execute the data insertion from the existing database
    # STDEV = SQRT( round(e((sum(omp)*sum(omp) - sum(omp * omp))/((count(*)-1)*(count(*)))),3))
    # STDEV = SQRT( AVG(omp*omp) - AVG(omp)*AVG(omp))

    sss = f"""
    INSERT INTO profile (
            DATE, 
            varno,
            VCOORD,
            SUMOMA,
            SUMOMP, 
            SUMOMP2,
            SUMOMA2,
            SUMBIAS_CORR,
            N,
            id_stn
    )
    SELECT
        isodatetime({date}) AS DATE, 
        varno AS VARNO,
        VCOORD  AS VCOORD,
        SUM(OMA) AS SUMOMA,
        SUM(OMP) AS SUMOMP, 
        SUM(OMA*OMA) AS SUMOMA2, 
        SUM(OMP*OMP) AS SUMOMP2,
        SUM(BIAS_CORR) AS BiasC,
        count(*) AS N,
        id_stn AS id_stn


    FROM
        db.header
    NATURAL JOIN
        db.DATA
    WHERE
        VARNO = {int(varno)}
        AND obsvalue IS NOT NULL
        --   AND ID_STN LIKE 'id_stn'
        --   AND vcoord IN (vcoord)
        {flag_criteria}
        {LATLONCRIT}
        {VCOCRIT}
    GROUP BY
        VCOORD, ID_STN
  --  HAVING 
  --      SUM(OMP IS NOT NULL) >= 50;
    """
    new_db_cursor.execute(sss)

    # Commit changes and detach the existing database
    #new_db_cursor.execute("DETACH DATABASE db;")
    new_db_conn.commit()




    # Commit changes and detach the existing database
    #new_db_cursor.execute("DETACH DATABASE db;")


    # Close the connections
    new_db_conn.close()
from datetime import datetime, timedelta

def create_data_list(datestart1, 
                     dateend1,
                     family, 
                     pathin, 
                     name,
                     pathwork, 
                     fonction,
                     flag_criteria,
                     region_seleccionada):
    data_list = []
    # Convert datestart and dateend to datetime objects
    datestart = datetime.strptime(datestart1, '%Y%m%d%H')
    dateend = datetime.strptime(dateend1, '%Y%m%d%H')

    # Initialize the current_date to datestart
    current_date = datestart

    # Define a timedelta of 6 hours
    delta = timedelta(hours=6)
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
  #  print (flag_criteria)
    
    #flag_criteria = generate_flag_criteria(flag_criteria)

    element_array = np.array([float(x) for x in element.split(',')])
    for varno in element_array:

    # Iterate through the date range in 6-hour intervals
     while current_date <= dateend:
        # Format the current date as a string
        formatted_date = current_date.strftime('%Y%m%d%H')

        # Build the file name using the date and family
        filename = f'{formatted_date}_{family}'
        # Create a new dictionary and append it to the list 
        channel ='all'
        id_stn ='all'

        data_dict = {
            'family': family,
            'filein': f'{pathin}/{filename}',
            'db_new': f'{pathwork}/profile_{name}_{datestart1}_{dateend1}_{fonction}_{flag_criteria}_{family}.db',
            'region': region_seleccionada,
            'flag_criteria': flag_criteria,
            'fonction': fonction,
            'varno'   : varno,
            'vcoord': channel,
            'id_stn': id_stn}
        data_list.append(data_dict)

        # Update the current_date in the loop by adding 6 hours
        current_date += delta

    return data_list

def create_data_list_plot(datestart1,
                          dateend1, 
                          family, 
                          pathin, 
                          namein,
                          pathwork, 
                          fonction, 
                          flag_criteria, 
                          region_seleccionada, 
                          id_stn, 
                          vcoord):
    data_list_plot = []
    filea = f'{pathwork}/profile_{namein[0]}_{datestart1}_{dateend1}_{fonction}_{flag_criteria}_{family}.db'
    namea = namein[0]
    fileset = [filea]
    nameset = [namein[0]]
    if len(namein)>1:
       fileb = f'{pathwork}/profile_{namein[1]}_{datestart1}_{dateend1}_{fonction}_{flag_criteria}_{family}.db'
       fileset = [filea,fileb]
       nameset = [namein[0], namein[1]]

    conn = sqlite3.connect(filea)
    cursor = conn.cursor()

    if id_stn=='alone':
        query = "SELECT DISTINCT id_stn FROM profile;"
        cursor.execute(query)
        id_stns = cursor.fetchall()
    else:
        id_stns = ['u%']
    for idstn in id_stns:
       if id_stn=='alone':
          criter =f'where id_stn  like  "{idstn[0]}"'
       
       else:
         criter =  criter =f'where id_stn  like  "{idstn}"'

       if vcoord =='all':
         query = f"SELECT DISTINCT varno  FROM profile {criter} ORDER BY vcoord ASC;"
         #print (query)
         cursor.execute(query)
         vcoords = cursor.fetchone()
          
         for varno in vcoords:

           data_dict_plot = {
            'id_stn': idstn,
            'vcoord': 'all',
            'varno' : varno,
            'filesin' : fileset}
           data_list_plot.append(data_dict_plot)


       elif vcoord=='alone':
         query = f"SELECT DISTINCT vcoord, varno FROM  profile {criter} ORDER BY vcoord ASC;"
         cursor.execute(query)
         vcoords = cursor.fetchall()
         for vcoord, varno in vcoords:
           #print (idstn[0],vcoord[0])
           data_dict_plot = {
            'id_stn': idstn[0],
            'vcoord': vcoord,
            'varno' : varno,
            'filesin': fileset,
            'namein': nameset}
           data_list_plot.append(data_dict_plot)
    return data_list_plot


def make_profile(files_in,
                 names_in,
                 pathwork, 
                 datestart,
                 dateend,
                 region, 
                 family, 
                 flag_criteria, 
                 fonction, 
                 id_stn,
                 channel,  
                 plot_type,
                 plot_title,
                 n_cpu):


   pikobs.delete_create_folder(pathwork)
   for file_in, name_in in zip(files_in, names_in):

   
       data_list = create_data_list(datestart,
                                    dateend, 
                                    family, 
                                    file_in,
                                    name_in,
                                    pathwork,
                                    fonction, 
                                    flag_criteria, 
                                    region)
       
       import time
       import dask
       t0 = time.time()
       if n_cpu==1:
        for  data_ in data_list:  
            print ("Serie")
            create_timeserie_table(data_['family'], 
                                   data_['db_new'], 
                                   data_['filein'],
                                   data_['region'],
                                   data_['flag_criteria'],
                                   data_['fonction'],
                                   data_['varno'])
    
    
    
    
       else:
        print (f'in Paralle = {len(data_list)}')
        with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                           n_workers=n_cpu, 
                                           silence_logs=40) as client:
            delayed_funcs = [dask.delayed(create_timeserie_table)(data_['family'], 
                                              data_['db_new'], 
                                              data_['filein'],
                                              data_['region'],
                                              data_['flag_criteria'],
                                              data_['fonction'],
                                              data_['varno'])for data_ in data_list]
            results = dask.compute(*delayed_funcs)
        
   tn= time.time()
   print ('Total time:',tn-t0 )
   #print ("VCOORD", channel)
   data_list_plot = create_data_list_plot(datestart,
                                          dateend, 
                                          family, 
                                          files_in, 
                                          names_in,
                                          pathwork,
                                          fonction, 
                                          flag_criteria, 
                                          region,
                                          id_stn,
                                          channel)
 
   os.makedirs(f'{pathwork}/profile')
   
   t0= time.time()

   if n_cpu==1:
    for  data_ in data_list_plot:  
        print ("Serie")
        pikobs.profile_plot(         
                             pathwork,
                             datestart,
                             dateend,
                             fonction,
                             flag_criteria,
                             family,
                             plot_title,
                             plot_type, 
                             names_in,
                             data_['vcoord'],
                             data_['id_stn'], 
                             data_['varno'],
                             data_['filesin'])

   else:
      print (f'in Paralle = {len(data_list_plot)}')

      with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                       n_workers=n_cpu, 
                                       silence_logs=40) as client:
        delayed_funcs = [dask.delayed(pikobs.profile_plot)(
                             pathwork,
                             datestart,
                             dateend,
                             fonction,
                             flag_criteria,
                             family,
                             plot_title,
                             plot_type, 
                             names_in,
                             data_['vcoord'],
                             data_['id_stn'], 
                             data_['varno'],
                             data_['filesin'])for data_ in data_list_plot]

        results = dask.compute(*delayed_funcs)
   tn= time.time()
   print ('Total time:',tn-t0 )


 



def arg_call():
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_control_files', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--control_name', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--path_experience_files', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--experience_name', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--pathwork', default='undefined', type=str, help="Working directory")
    parser.add_argument('--datestart', default='undefined', type=str, help="Start date")
    parser.add_argument('--dateend', default='undefined', type=str, help="End date")
    parser.add_argument('--region', default='undefined', type=str, help="Region")
    parser.add_argument('--family', default='undefined', type=str, help="Family")
    parser.add_argument('--flags_criteria', default='undefined', type=str, help="Flags criteria")
    parser.add_argument('--fonction', default='undefined', type=str, help="Function")
    parser.add_argument('--id_stn', default='all', type=str, help="id_stn") 
    parser.add_argument('--channel', default='all', type=str, help="channel") 
    parser.add_argument('--plot_type', default='classic', type=str, help="channel")
    parser.add_argument('--plot_title', default='plot', type=str, help="channel")
    parser.add_argument('--n_cpus', default=1, type=int, help="Number of CPUs")

    args = parser.parse_args()
    for arg in vars(args):
       print (f'--{arg} {getattr(args, arg)}')
    # Check if each argument is 'undefined'
    if args.path_control_files == 'undefined':
        files_in = [args.path_experience_files]
        names_in = [args.experience_name]
    else:    
      if args.path_experience_files == 'undefined':
          raise ValueError('You must specify --path_experience_files')
      if args.experience_name == 'undefined':
          raise ValueError('You must specify --experience_name')
      else:

          files_in = [args.path_control_files, args.path_experience_files]
          names_in = [args.control_name, args.experience_name]
    print (names_in)
    if args.pathwork == 'undefined':
        raise ValueError('You must specify --pathwork')
    if args.datestart == 'undefined':
        raise ValueError('You must specify --datestart')
    if args.dateend == 'undefined':
        raise ValueError('You must specify --dateend')
    if args.region == 'undefined':
        raise ValueError('You must specify --region')
    if args.family == 'undefined':
        raise ValueError('You must specify --family')
    if args.flags_criteria == 'undefined':
        raise ValueError('You must specify --flags_criteria')
    if args.fonction == 'undefined':
        raise ValueError('You must specify --fonction')


  

    #print("in")
    #Call your function with the arguments
    sys.exit(make_profile(files_in,
                          names_in,
                          args.pathwork,
                          args.datestart,
                          args.dateend,
                          args.region,
                          args.family,
                          args.flags_criteria,
                          args.fonction,
                          args.id_stn,
                          args.channel,  
                          args.plot_type,
                          args.plot_title,
                          args.n_cpus))

if __name__ == '__main__':
    args = arg_call()





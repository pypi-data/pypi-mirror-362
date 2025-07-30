#!/usr/bin/env python3

#Auteur : Pierre Koclas, May 2021
import os
import sys
import csv
from math import floor,ceil,sqrt
import matplotlib as mpl
mpl.use('Agg')
#import pylab as plt
import matplotlib.pylab as plt
import numpy as np
import matplotlib.colorbar as cbar
import matplotlib.cm as cm
import datetime
import cartopy.crs as ccrs
import cartopy.feature
#from cartopy.mpl.ticker    import LongitudeFormatter,  LatitudeFormatter
import matplotlib.colors as colors
#import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import sqlite3
from matplotlib.collections import PatchCollection
from statistics import median
import pikobs
import optparse
from mpl_toolkits.axes_grid1 import make_axes_locatable
def projectPpoly(PROJ,lat,lon,deltax,deltay,pc):
        X1,Y1  = PROJ.transform_point(lon - deltax,lat-deltay,pc )
        X2,Y2  = PROJ.transform_point(lon - deltax,lat+deltay,pc )
        X3,Y3  = PROJ.transform_point(lon + deltax,lat+deltay,pc )
        X4, Y4 = PROJ.transform_point(lon + deltax,lat-deltay,pc )
        Pt1=[ X1,Y1 ]
        Pt2=[ X2,Y2 ]
        Pt3=[ X3,Y3 ]
        Pt4=[ X4,Y4 ]
        Points4 = [ Pt1, Pt2,Pt3,Pt4 ]
           
        return Points4
def SURFLL(lat1,lat2,lon1,lon2):
#= (pi/180)R^2 |sin(lat1)-sin(lat2)| |lon1-lon2|
    R=6371.
    lat2=min(lat2,90.)
    surf=R*R*(np.pi/180.)*abs ( np.sin(lat2*np.pi/180.) - np.sin(lat1*np.pi/180.) ) *abs( lon2-lon1 )
   # if ( surf == 0.):
    # print (   ' surf=',lat1,lat2,lat2*np.pi/180.,lat1*np.pi/180.,np.sin(lat2*np.pi/180.) ,  np.sin(lat1*np.pi/180.) )
    return surf

def NPSURFLL(lat1, lat2, lon1, lon2):
    R = 6371.
    lat2 = np.minimum(lat2, 90.)
    surf = R**2 * (np.pi/180) * np.abs(np.sin(lat2*np.pi/180) - np.sin(lat1*np.pi/180)) * np.abs(lon2 - lon1)
  #  if np.any(surf == 0.):
    #    print('surf contiene valores cero')
    return surf
def SURFLL2(lat1, lat2, lon1, lon2):
    R = 6371.0
    lat2 = np.minimum(lat2, 90.0)
    surf = R * R * (np.pi / 180.0) * np.abs(np.sin(lat2 * np.pi / 180.0) - np.sin(lat1 * np.pi / 180.0)) * np.abs(lon2 - lon1)
    # Debugging print statements if surface is zero
    zero_surf_indices = (surf == 0.0)
    if np.any(zero_surf_indices):
        print('surf=', lat1[zero_surf_indices], lat2[zero_surf_indices], lat2[zero_surf_indices] * np.pi / 180.0,
              lat1[zero_surf_indices] * np.pi / 180.0,
              np.sin(lat2[zero_surf_indices] * np.pi / 180.0),
              np.sin(lat1[zero_surf_indices] * np.pi / 180.0))
    return surf
def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y%m%d%H")
    d2 = datetime.datetime.strptime(d2, "%Y%m%d%H")
    return abs((d2 - d1).days)



import pikobs

def scatter_plot(
                   mode,
                   region,
                   family, 
                   id_stn, 
                   datestart,
                   dateend, 
                   Points,
                   boxsizex,
                   boxsizey, 
                   proj, 
                   pathwork, 
                   flag_criteria, 
                   fonction,
                   vcoord,
                   filesin,
                   namesin,
                   varno,
                   intervales):

       selected_flags = pikobs.flag_criteria(flag_criteria)


   
       pointsize=0.5
       delta=float(boxsizex)/2.
       deltay=float(boxsizey)/2.
       deltax=float(boxsizex)/2.
   
   #=============================================================
   #============      LECTURE   ================================
  # if isinstance(varnos, int):
  #  varnos = [varnos]
  # for fonction  in  fonctions:
  #  for Proj in proj:
       interval_a = intervales[0]
       interval_b = intervales[1]
       if  interval_a==None and  interval_b==None:
          criteria_interval = ''
          layers='layer_all'
       else:
          criteria_interval = f' and  {interval_a*100} <= vcoord <= {interval_b*100}'
          layers=f'Layer: {interval_a} hPa - {interval_b} hPa'


       conn = sqlite3.connect(":memory:")
       cursor = conn.cursor()
       cursor.execute("PRAGMA TEMP_STORE=memory")
       query = f"ATTACH DATABASE '{filesin[0]}' AS db1"  
       cursor.execute(query)

       FNAM, FNAMP, SUM, SUM2 = pikobs.type_boxes(fonction)
       if id_stn =='join' and vcoord=='join' :
          crite ="  "
       if id_stn =='join' and vcoord!='join' :
          crite = f" and  vcoord = {vcoord} "

       if id_stn !='join' and vcoord=='join' :
          crite = f"and  id_stn= '{id_stn}'    "
       
       if id_stn !='join' and vcoord!='join':
          crite = f"  and  vcoord = {vcoord} and id_stn= '{id_stn}'  "



       if len(filesin)>1:
             create_table='boites1'
             info_name = f"{namesin[0]} VS {namesin[1]}"
       else:
             create_table='AVG'
             info_name = f"namesin[0]"
        
       query = f"""CREATE TEMPORARY TABLE {create_table} AS
                   SELECT boite, 
                          lat,
                          lon, 
                          varno, 
                          vcoord,
                          SUM({SUM})/SUM(CAST(N AS FLOAT)) AVG,
                          SQRT(SUM({SUM2})/SUM(CAST(N AS FLOAT)) - SUM({SUM})/SUM(CAST(N AS FLOAT))*SUM({SUM})/SUM(CAST(N AS FLOAT))) STD,
                          SUM(sumstat)/SUM(CAST(N AS FLOAT)) BCORR,
                          SUM(n) N
                   FROM db1.moyenne
                   where varno={varno}

                   {crite} 

                   GROUP BY boite, lat, lon, varno;"""
       cursor.execute(query)

       if len(filesin)>1:
           query = f"ATTACH DATABASE '{filesin[1]}' AS db2"
           cursor.execute(query)
           query = f"""CREATE TEMPORARY TABLE boites2 AS
                       SELECT boite, lat, lon, varno, vcoord,
                              SUM({SUM})/SUM(CAST(N AS FLOAT)) AVG,
                              SQRT(SUM({SUM2})/SUM(CAST(N AS FLOAT)) - SUM({SUM})/SUM(CAST(N AS FLOAT))*SUM({SUM})/SUM(CAST(N AS FLOAT))) STD,
                              SUM(sumstat)/SUM(CAST(N AS FLOAT)) BCORR,
                              SUM(n) N
                       FROM db2.moyenne
                       where  varno={varno}

                       {crite} 
                     
                       GROUP BY boite, lat, lon, varno;"""  

           cursor.execute(query)

           query = f"""Create temporary table AVG as 
                       SELECT BOITES1.boite BOITE,
                              BOITES1.lat LAT,
                              BOITES1.lon LON,
                              BOITES1.vcoord VCOORD,
                              BOITES1.varno VARNO,
                              BOITES1.avg - BOITES2.avg AVG, --BOITES1.avg - BOITES2.avg AVG,
                              BOITES1.std - BOITES2.std STD, --  BOITES1.std - BOITES2.std STD, 
                              BOITES1.bcorr - BOITES2.bcorr BCORR ,  --BOITES1.bcorr - BOITES2.bcorr BCORR ,  
                              BOITES1.N - BOITES2.N  N, --BOITES1.N - BOITES2.N  N, 
                              BOITES1.N N1 ,BOITES2.N N2 
                      FROM BOITES1,BOITES2 
                      WHERE  BOITES1.boite=BOITES2.boite and BOITES1.VCOORD=BOITES2.VCOORD""" 
                      

           cursor.execute(query)
       
       query = f"""
        SELECT lat, lon, avg, std, N
        FROM AVG;
       """
       cursor.execute(query)
      
       cursor.execute(query)
       results = cursor.fetchall()    
       # Convertir a arrays numpy

       lat = np.array([row[0] for row in results])
       lon = np.array([row[1] for row in results])
       Bomp = np.array([row[2] for row in results])
       Somp = np.array([row[3] for row in results])
       nombre = np.array([row[4] for row in results])
       dens = nombre/NPSURFLL(lat-deltay,lat+deltay,lon-deltax,lon + deltax)


       index_none=np.where(Somp ==None)
       lat = np.delete(lat, index_none) 
       lon = np.delete(lon, index_none)
       Bomp = np.delete(Bomp, index_none)
       Somp = np.delete(Somp, index_none)
       nombre = np.delete(nombre, index_none)
      
       query = f"""select  
                  '{datestart}',
                  '{dateend}',
                  '{family}',
                  '{varno}' , 
                   avg(avg)  , 
                   avg(std) ,
                   sum(N) 
                   From  
                   AVG    ;"""
       
       cursor.execute(query)
       results = cursor.fetchall()   
       debut  = np.array([row[0] for row in results])
       fin    = np.array([row[1] for row in results])
       familys = np.array([row[2] for row in results])
       Mu     = np.array([row[4] for row in results])
       Sigma  = np.array([row[5] for row in results])
       Nobs   = np.array([row[6] for row in results])
       # Close the connection

       conn.close()
       typer=''
       # Round Sigma to 3 decimal places
       if Sigma!= None:
           Sigma = np.round(Sigma, 3)
       
           # Define variables
           vartyp = fonction
           PERIODE = f'From {datestart} To {dateend}'
           NDAYS = max(1, days_between(datestart, dateend))
           variable_name, units, vcoord_type = pikobs.type_varno(varno)
           
           if vcoord=='join':
               Nomvar = f"{variable_name} {units} \n id_stn:{id_stn} vcoord:{(vcoord)} {layers}"
           else:
              Nomvar = f"{variable_name} {units} \n id_stn:{id_stn} vcoord:{int(vcoord)} {layers} "
           mode = 'MOYENNE'
         #  mode == 'SIGMA'

           # Set OMP based on mode
           OMP = Somp if mode == 'SIGMA' else Bomp
           OMP = np.nan_to_num(OMP, nan=np.nan)  # Replace NaNs with specified value
           
           # Plot setupa
           plt.close('all')
           fig = plt.figure(figsize=(10, 10))

           Alpha = 1.0
           Ninterv = 10
           cmap = cm.get_cmap('seismic', lut=Ninterv)
           plt.rcParams['axes.linewidth'] = 1
           fontsize =17
           # Filter OMP for valid float values
           OMPm = [value for value in OMP if isinstance(value, float)]
           vmin, vmax = round(np.nanmin(OMPm)), round(np.nanmax(OMPm))
           norm = cm.colors.Normalize(vmin=vmin, vmax=vmax)
           y = np.linspace(vmin, vmax, Ninterv + 1)
           STRING1 = '%.0f'
           # Handle different variable types
           if vartyp == 'dens': 
              # Ninterv = 9
               OMP = dens / NDAYS
               vmax = max(OMP)
               if vmax  ==0:
                  vmax=1
               cmap = cm.get_cmap('PuRd', lut=Ninterv)
               vmin = 0.
           
           elif vartyp in ['nobs', 'NOBSHDR']: 
               Ninterv = 10
               OMP = nombre
               ABSO = max(np.abs(nombre))
               vmin = -ABSO if min(nombre) < 0 else floor(min(nombre) / 100) * 100
               vmax = ABSO if min(nombre) < 0 else ceil(max(nombre) / 100) * 100
               vmin =  -1000 #-ABSO if min(nombre) < 0 else floor(min(nombre) / 100) * 100
               vmax =   1000 #-ABSO if min(nombre) < 0 else ceil(max(nombre) / 100) * 100
               from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap, TwoSlopeNorm
               bounds = np.array([1000, 400, 200, 100, 50, 10, -10, -50, -100, -200, -400, -1000])
               # 2. Crea los colores: el central (para -10 a 10) es blanco, los extremos son gradientes.
               colors1 = [
                   "#a50026", # profundo rojo (1000 a 400)
                   "#d73027", # rojo (400 a 200)
                   "#f46d43", # naranja (200 a 100)
                   "#fdae61", # amarillo (100 a 50)
                   "#fee090", # casi blanco/amarillo (50 a 10)
                   "white",   # BLANCO (-10 a 10)
                   "#e0f3f8", # celeste suave (-10 a -50)
                   "#abd9e9", # celeste (-50 a -100)
                   "#74add1", # azul claro (-100 a -200)
                   "#4575b4", # azul medio (-200 a -400)
                   "#313695"  # azul fuerte (-400 a -1000)
               ]
               from matplotlib.colors import BoundaryNorm, ListedColormap 
           
               # 3. Crea el colormap y la normalización
               #cmap = ListedColormap(colors1)
               cmap = cm.get_cmap('RdYlBu_r', lut=Ninterv)
               vmin, vmax = -1000, 1000
               Ninterv = 11  # Debe ser impar para que haya un color central
               
               data = np.linspace(-1000, 1000, 10000).reshape(100, 100)
               cmap0 = cm.get_cmap('RdYlBu_r', lut=Ninterv)
               colors1 = [cmap0(i) for i in range(Ninterv)]
               colors1[Ninterv//2] = (1, 1, 1, 1)  # Fuerza el color central a blanco
               
               cmap = ListedColormap(colors1)
              # norm = BoundaryNorm(bounds, ncolors=cmap.N)
               Alpha = 0.5
               if vmin == vmax:
                   vmin, vmax = -1.0, 1.0
           
           elif vartyp == 'obs':
               vartyp='AVG(obs)'
               Ninterv = 9
               cmap = cm.get_cmap('RdYlBu_r', lut=Ninterv)
               SSIG = np.std(OMP)
               ABSO = 4.0 * SSIG
               Median = median(OMP)
               vmin, vmax = Median - ABSO, Median + ABSO
               if mode == 'SIGMA':
                   absomp=abs(OMP)
                   vmin= min(absomp)
                   vmax = max(absomp)
               if abs(vmin - vmax) < .01:
                   vmin, vmax = -.5, .5
           
           elif vartyp in ['omp', 'oma', 'bcorr', 'stdomp', 'stdomp' ]:
               STRING1 = '$%.0f\sigma$'

               Ninterv = 10
               if vartyp=='stdomp':
                  mode = 'SIGMA'
                  typer= 'STD'
               ABSO = max(np.abs(OMP))
              # vmin, vmax = -ABSO, ABSO 
               vmin, vmax = -.5, .5

               cmap = cm.get_cmap('seismic', lut=Ninterv)
               if mode == 'MOYENNE':
                   typer= 'AVG'

                   SSIG = np.std(OMP)
                 #  ABSO = 4.0 * SSIG
                   Median = 0 #median(OMP) 
                   vmin, vmax = Median - ABSO, Median + ABSO
                   vmin, vmax = -.5, .5

                   if abs(vmin - vmax) < .01:
                       vmin, vmax = -.5, .5 
                       vmin, vmax = -.5, .5

                       OMP = [0.0] * len(OMP)
               if mode == 'SIGMA':
                   vmin, vmax = min(OMP), max(OMP)
                   vmin, vmax = -.5, .5
                   cmap = cm.get_cmap('RdYlBu_r', lut=Ninterv)
           
           # Adjust if vmin and vmax are too close
           if abs(vmin - vmax) < .01 and vartyp != 'dens':
               vmin, vmax = -.5, .5
           # Normalize and create color map
           norm = cm.colors.Normalize(vmin=vmin, vmax=vmax)
           from matplotlib.colors import BoundaryNorm, ListedColormap 
           from matplotlib.colors import BoundaryNorm, ListedColormap 
        #norm = BoundaryNorm(bounds, len(colors1))
         #  norm = BoundaryNorm(bounds, ncolors=cmap.N)
           y = np.linspace(vmin, vmax, Ninterv + 1)
           m = cm.ScalarMappable(norm=norm, cmap=cmap)
           Colors =  [m.to_rgba(x) for x in y]
           hexv = [colors.rgb2hex(c) for c in Colors]
           inds = np.digitize(OMP, y)
           
           # Plotting setup
           nombres = 0
           left, bottom = 0.90, 0.15
           ax, fig, LATPOS, PROJ, pc = pikobs.type_projection(proj)
           ONMAP = 0
           POINTS = 'OFF'
           patch_list = []
           
           # Loop through data points and plota
      
           for i in range(len(nombre)):
               x1, y1 = PROJ.transform_point(lon[i], lat[i], pc)
               point = PROJ.transform_point(lon[i], lat[i], src_crs=pc)
               fig_coords = ax.transData.transform(point)
               ax_coords = ax.transAxes.inverted().transform(fig_coords)
               xx, yy = ax_coords
               mask = (xx >= -0.01) & (xx <= 1.01) & (yy >= -0.01) & (yy <= 1.01)
               if mask:
                   ONMAP += nombre[i]
                   if POINTS == 'ON':
                       plt.text(point[0], point[1], int(floor(nombre[i])), color="k", fontsize=17, zorder=5, ha='center', va='center', weight='bold')
                   else:
                       points4 = projectPpoly(PROJ, lat[i], lon[i], deltax, deltay, pc)
                       col = Colors[inds[i] - 1]
                       poly = plt.Polygon(points4, fc=col, zorder=4, ec='k', lw=0.2, alpha=1.0)
                       ax.add_patch(poly)
           # Add map features
           ax.coastlines()
           ax.add_feature(cartopy.feature.LAND, zorder=1, edgecolor='#C0C0C0', facecolor='#C0C0C0')
           ax.add_feature(cartopy.feature.OCEAN, zorder=0, edgecolor='#7f7f7f', facecolor='#00bce3')
           ax.add_feature(cartopy.feature.BORDERS, zorder=10)
           ax.add_feature(cartopy.feature.COASTLINE, zorder=10)
           # Add gridlines
           gl = ax.gridlines(color='b', linestyle=(0, (1, 1)), xlocs=range(-180, 190, 10), ylocs=LATPOS, draw_labels=False, zorder=0)
           
           # Add colorbar
        #   ax3 = fig.add_axes([left, bottom, .02, 0.70])
           divider = make_axes_locatable(ax)
           ax3 = divider.append_axes("right", size="5%", pad=0.05, axes_class=plt.Axes)
        #   ax3 = fig.add_axes()
           y = [round(yi, 6) for yi in y]
        #   cb2 = cbar.ColorbarBase(ax3, cmap=cmap, norm=norm, orientation='vertical', drawedges=True, extend='neither', ticks=y, boundaries=y, alpha=Alpha)
           cb2 = cbar.ColorbarBase(ax3, cmap=cmap, norm=norm, orientation='vertical', drawedges=True, extend='neither',ticks=y, boundaries=y) #alpha=Alpha)
         #  cbar.set_ticks(np.linspace(vmin, vmax, Ninterv))
           def scientific(x, pos):
             """Formato en notación científica para la colorbar"""
             return f'{x:.1e}'
           if vartyp=='obs' :

             vartyp='AVG(OBS)'
             units=''
           if vartyp=='dens' :

             units='' 
           if  vartyp=='omp' :

             vartyp='Differences AVG(OMP) ' 
           if  vartyp=='oma' :

             vartyp='AVG(OMA)'

           cb2.ax.set_ylabel(f'{vartyp.upper()}  {units}',fontsize=18,  rotation=90, labelpad=20) 
           if vartyp=='dens': 
               from matplotlib.ticker import FuncFormatter
               cb2.ax.yaxis.set_major_formatter(FuncFormatter(scientific))
           cb2.ax.tick_params(labelsize=14)
            # Add text and labels
           if len(filesin)<1:
               ax.text(0.00, 1.05, namesin[0], fontsize=fontsize, color='b', transform=ax.transAxes)
      
           else:
               # Tamaño de fuente y coordenadas iniciales
               fontsize = 14
               start_x = 0.00
               y_coord = 1.05
      
               # Crear la figura y el eje
               #fig, ax = plt.subplots()
               #ax.set_xlim(0, 1)
               #ax.set_ylim(0, 1)
      
               # Calcular longitudes de los nombres
      
               text1_len = len(namesin[0])*1.5 
               text1_x = start_x 
      
               if len(filesin)>1:
      
                  text2_len = len(namesin[1])
                  text2_x = text1_x + text1_len / 130
                  text3_x = text2_x + 0.05  # Añadir un espacio fijo
      
                  ax.text(text2_x, y_coord, " VS ", fontsize=fontsize, color='black', transform=ax.transAxes)
                  ax.text(text3_x, y_coord, namesin[1], fontsize=fontsize, color='red', transform=ax.transAxes)
      
      
      
               ax.text(text1_x, y_coord, namesin[0], fontsize=fontsize, color='blue', transform=ax.transAxes)
             #  ax.text(text2_x, y_coord, " VS ", fontsize=fontsize, color='black', transform=ax.transAxes)
             #  ax.text(text3_x, y_coord, namesin[1], fontsize=fontsize, color='blue', transform=ax.transAxes)
      
        
           ax.text(0.00 + 20, 1.05, vartyp, fontsize=fontsize, color='k', transform=ax.transAxes)
           ax.text(0.00, 1.02, PERIODE, fontsize=fontsize, color='#3366FF', transform=ax.transAxes)
           ax.text(0.45, 1.05, Nomvar, fontsize=fontsize, color='k', transform=ax.transAxes, fontweight='bold')
           
           props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        #   if len(filesin)<1:
           if vartyp in ['dens', 'nobs']:
               textstr =  'Nobs=%.2i'%(ONMAP)
           else:
          #    textstr =  r'$\bar{\mu}=%.3f $\bar{\sigma}=%.3f $\nNobs=%.2i$' % (Mu, Sigma, ONMAP)
              textstr = '$\\bar{\\mu}=%.3f$ $\\bar{\\sigma}=%.3f$ \nNobs=%.2i' % (Mu, Sigma, ONMAP)
              #textstr = '$\mu=%.3f $\bar sigma=%.3f $\nNobs=%.2i'%(Mu, Sigma, ONMAP)
             # ax.text(0.95, 1.15, textstr, transform=ax.transAxes, fontsize=fontsize, verticalalignment='top', bbox=props)
           #ax.add_feature(cartopy.feature.BORDERS)
       
           # Save the plot
           plt.grid(True)
           plt.rcParams['axes.linewidth'] = 2
         #  ax.outline_patch.set_zorder(11)
          # ax.coastlines(linewidth=2, edgecolor='black', zorder=11)
         #  ax.add_feature(cartopy.feature.BORDERS, zorder=10)
           if vcoord == 'join':
              plt.savefig(f'{pathwork}/{family}/{fonction}_{proj}_{layers}_id_stn_{id_stn}_{region}_vcoord{vcoord}_varno{varno}.png', format='png')
      
           else:
              plt.savefig(f'{pathwork}/{family}/{fonction}_{proj}_{layers}_id_stn_{id_stn}_{region}_vcoord{int(vcoord)}_varno{varno}.png', format='png')
           plt.close(fig)

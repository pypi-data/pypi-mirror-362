#!/usr/bin/env python3
#============================================
#---------------
# profils
#---------------
#
#  Auteur : Pierre Koclas Aout 2021
#  But:
#         faire des graphes(images)
#         de profils 
#         a partir de fichiers  csv
#         generes par des scripts SQL.
#
import numpy as np
import sys
import csv
from numpy import ma

import math
import sqlite3
import matplotlib as mpl
mpl.use('Agg')
import pylab
import pikobs

def profile_plot(
                   pathwork,
                   datestart,
                   dateend,
                   fonction,
                   flag_type,
                   family,
                   region,
                   fig_title,
                   names_in,
                   vcoord, 
                   id_stn, 
                   varno,
                   files_in):



    LARG=[]
    
    ROUGE='#FA5858'
    BLEU='#00A0FF'
    BLEU='#008BFF'
    JAUNE='#FFFF00'
    VERT='#009900'
    NOIR='#000000'
    couleurs=[BLEU,ROUGE,JAUNE,VERT,NOIR]
    
    #SQL csv="select varno,vcoord, Avg, Avg2, Std, Std2, N, Rejets ;"
    #                 0      1     2     3     4    5    6    7
    # Ordre des colonnes par defaut generes par mes scripts SQL est;"
    #
    #===========================================================================================================
    graphe_colonnes ={'O-P':(2,4),'O-A':(3,5),'O-F':(2,4),'REJ':(7,7),'O-P/P':(2,4),'O-A/P':(3,5),'O-A/A':(3,5),'OBS':(2,4),'TRL':(3,5),'BCORR':(2,4)}
    #===========================================================================================================
    
    graphe_limites = {'12101': (-2, 2),'12001': (-2, 2), '12239': (-4, 8),'12192': (-4, 8), '11003': (-2, 4), '11004':(-2,4),'12163':(-2.0,5.0),'12004': (-2, 6), '12203': (-2, 6), '11215': (-2, 8), '11216': (-2, 8), '10004': (-100, 200), '10051': (-100, 200)}
    #graphe_limites = {'12001': (-2, 500), '12192': (-4, 500), '11003': (-2, 8), '11004':(-2,8),'12163':(-1.0,5.0),'12004': (-2, 6), '12203': (-2, 6), '11215': (-2, 8), '11216': (-2, 8), '10004': (-100, 200), '10051': (-100, 200)}
    #=============================================================================================
    graphe_nomvar ={'11215':'U COMPONENT OF WIND (10M)','11216':'V COMPONENT OF WIND (10M)','12004':'DRY BULB TEMPERATURE AT 2M','10051':'PRESSURE REDUCED TO MEAN SEA LEVEL','10004':'PRESSURE','12203':'DEW POINT DEPRESSION (2M)','12001':'TEMPERATURE/DRY BULB','11003':'U COMPONENT OF WIND','11004':'V COMPONENT OF WIND','12192':'DEW POINT DEPRESSION','12163':'BRIGHTNESS TEMPERATURE','15036':'ATMOSPHERIC REFRACTIVITY','15031':'ATMOSPHERIC PATH DELAY','11001':'WIND DIRECTION','11002':'WIND SPEED','11011':'WIND DIRECTION AT 10M','11012':'WIND SPEED AT 10M','12239':'DEW POINT DEPRESSION HIGH PRECISION','12101':'TEMPERATURE/DRY BULB HIGH PRECISION'}
    #=============================================================================================
    
    
    colors = ['#1f77b4',
              '#ff7f0e',
              '#2ca02c',
              '#d62728',
              '#9467bd',
              '#8c564b',
              '#e377c2',
              '#7f7f7f',
              '#bcbd22',
              '#17becf',
              '#1a55FF']
    couleurs=colors
    couleurs[0]=BLEU
    couleurs[1]=ROUGE
    
    #ddColN=7
    
    legendlist=['UnCorrected','Bias_Correction','Corrected','Std-Deviation']
    #----------------------------ARGUMENTS ----------------------------------------
    
    #==============================================================================
    #
    #for arg in sys.argv:
    #  #  print(   arg )
    #    LARG.append(arg) 
    
    #print (LARG)
    files=files_in
    graphe1=[fonction]
    nfichiers=len(files)
    vcoord_type='Channel'
 #   files.append(LARG[3])
    famille  = family
    region   = region
    varno    = varno
    #latlons  =LARG[7]
    label    = names_in[0]
    debut    = datestart
    fin      = dateend
    fonction = fonction
    #graphe1.append(fonction.strip())
   # print (  " varno= ",varno )
   # print (  " nfichiers= ",nfichiers )
    if varno  in graphe_nomvar :
      Nom=graphe_nomvar[varno]
    else:
      Nom=varno
  #  print (  ' LE NOM est :', Nom )
    if(  graphe1[0] == 'BCORR'):
         nfichiers=1
    
    if nfichiers >1:
    # print (  ' LARG[11]=',LARG[11] )
     famille2  =family
     REGION2   =region
     varno2    =varno
    # latlons2  =LARG[16]
     label2    =names_in[1]
     debut2    =datestart

     fin2      =dateend
     fonction2 =fonction
     PERIODE2=' ' + debut2 +'   to  ' + fin2
    # print (  ' REGION2 =',REGION2 )
     graphe1.append(fonction2.strip())
   #  print (  " varno2= ",varno2 )
     if varno  in graphe_nomvar :
      Nom2=graphe_nomvar[varno]
     else:
      Nom2=varno
    #  print (  ' LE NOM2 est :', Nom2 )
  #  print (  ' region =',region )
  #  print (  ' graphe1 =',graphe1 )
    PERIODE=' ' + debut +'   to  ' + fin
    
    #
    #==============================================================================
      
    #'ua' 'Monde' '12001'  'POSTALT-G1' '2013111912' '2013121912'  'O-P'
    #SQL csv="select varno,vcoord, Avg, Avg2, Std, Std2, N, Rejets ;"
    
    
    Bomp1=[]  ; Somp1=[] 
    Bomp2=[]  ; Somp2=[] 
    Nomb1=[]  ; Nomb2=[]
    Niveau=[]
    Nrej=[] ; Nrejets=[];Nprof=[]
    x, xx, vcoord_type = pikobs.type_varno(f"{varno}")

    if ( vcoord_type == 'PRESSION'):
       SIGN=1
       order=False
       vcoord_type_e='Pressure'
    elif ( vcoord_type == 'HAUTEUR'):
       SIGN=-1
       order=True
       vcoord_type_e='Height'
    elif ( vcoord_type == 'CANAL'):      
       SIGN=-1
       order=True
       vcoord_type_e='Channel'
    else:
       SIGN=-1
       order=True
       vcoord_type_e=vcoord_type
    
    
    #=================================
    #fig = pylab.figure(figsize=(8,10))
    fig = pylab.figure(figsize=(8,10))
    #=================================
    ax = fig.add_subplot(1,1,1)
    ax.grid(True)
    
    filenumb=0
    TITRE='VERIFS'
    lvl=[]
    numb=[]
    Bomp3=[];Somp3=[];Nomb3=[]
    Niveau=[]
    BY_VALUES=[]
    NY_VALUES=[]
    RY_VALUES=[]
    SY_VALUES=[]
    VY_VALUES=[]
    BIAS_VALUES=[]
    
    #=================================
    for filen in  files:
     #print ("filen:", filen)
     Niveau=[];yticks=[];lvl=[];lvlm=[]
     masked=[]
     Bomp1=[];Somp1=[];Bomp2=[];Somp2=[];Nomb1=[];Nrejets=[];Bomp3=[];Somp3=[];Nomb3=[];Bomp33=[];Somp33=[]
     NIVOS1=[]
     BIAS=[]
     if graphe1[filenumb]   in graphe_colonnes :
      ColB,ColS=graphe_colonnes[graphe1[filenumb]]
    
     else :
      ColB,ColS=(2,4)
     #print (  ' COLB =',ColB, ' COLS =',ColS )
     COLBIAS=6
     filenumb=filenumb+1
     conn = sqlite3.connect(filen)
     cursor = conn.cursor()
     cursor.execute("PRAGMA TEMP_STORE=memory")
     query=f"""create temporary table  boites1 as select 
                               varno AS VARNO,
                               vcoord AS VCOORD,
                               sum(SUMOMP)/sum(N) AVG,
                               sqrt( sum(SUMOMP2)/sum(N) -sum(SUMOMP2)/sum(N)*sum(SUMOMP)/sum(N) ) STD,
                               sum(n) AS N  ,
                               sum(SUMBIAS_CORR)/sum(N) AS bcorr from profile where varno="{varno}" and id_stn like '{id_stn}' and nomi group by vcoord;"""
    
     query=f"""select 
                               varno,
                               vcoord,
                               sum(SUMOMP)/sum(N),
                               sqrt( sum(SUMOMP2)/sum(N) -sum(SUMOMP2)/sum(N)*sum(SUMOMP)/sum(N) ),
                               sum(n),
                               sum(SUMBIAS_CORR)/sum(N)   from profile where varno="{varno}" and id_stn  like '{id_stn}'  group by vcoord;"""
     cursor.execute(query)
     results = cursor.fetchall() 
                        



    #=================================
     fileB_VALUES  = np.array([row[2] for row in results]) 
     fileS_VALUES  = np.array([row[3] for row in results]) 
     fileBIAS_VALUES = np.array([row[1] for row in results]) 
     fileVY_VALUES = np.array([row[1] for row in results]) 
     fileRY_VALUES = np.array([row[1] for row in results]) 
     fileNY_VALUES = np.array([row[4] for row in results]) 

     BY_VALUES.append(fileB_VALUES)
     SY_VALUES.append(fileS_VALUES)
     BIAS_VALUES.append(fileBIAS_VALUES)
     VY_VALUES.append(fileVY_VALUES)
     RY_VALUES.append(fileRY_VALUES)
     NY_VALUES.append(fileNY_VALUES)
    #=================================
    #print ("david",VY_VALUES[0])
    Svc1Uvc3=set(VY_VALUES[0])
    Lt1Ut3=set(VY_VALUES[0])
    #print ( ' LES NIVEAUX AVANT=',Lt1Ut3)
    if nfichiers ==2:
    #Svc1Uvc3= Svc1Uvc3 | set(VY_VALUES[1]) 
     y=set(VY_VALUES[1])
     z = Svc1Uvc3.intersection(y)
     Lt1Ut3= sorted(list(z),  reverse=order)
    NIVS=list(Lt1Ut3)
   # print ( ' LES NIVEAUX COMMUNS=',NIVS)
    
    Somp_comp=[]
    for filn in  range(0,nfichiers ) :
    # print (  ' FILN couleur =',filn,couleurs[filn] )
     NIVOS1= list(VY_VALUES[filn])
     BOMPS1= list(BY_VALUES[filn])
     SOMPS1= list(SY_VALUES[filn])
     REJETS1=list(RY_VALUES[filn])
     NOMB1=  list(NY_VALUES[filn])
     BIAS1=  list(BIAS_VALUES[filn])
    
     data = []
     for row in range(0,len( NIVS)  ):
       try:
         ind1 =   NIVOS1.index( NIVS[row ] )
         data.append([ NIVOS1[ind1], BOMPS1[ind1], SOMPS1[ind1], NOMB1[ind1], REJETS1[ind1],BIAS1[ind1] ])
       except ValueError:
         data.append([ NIVS[row ],-99.9,-99.9,-99.9,-99.9])
         ind1=-1
     sorted_by_second = sorted(data, key=lambda tup: tup[0],reverse=True)
     lvl, Bomp3,Somp3,Nomb3,Rejets3,Bias3 = zip(*sorted_by_second)
     lvls=range(0,len(lvl)  )
     masked=ma.masked_equal(Bomp3  , -99.9   )
     Themask=ma.getmaskarray(masked)
     Bomp2 = ma.array(Bomp3,   mask=Themask)
     Somp2 = ma.array(Somp3,   mask=Themask)
     Nomb2 = ma.array(Nomb3,   mask=Themask)
     Nrej2 = ma.array(Rejets3, mask=Themask)
     Bias_corr = ma.array(Bias3, mask=Themask)
    # print (  ' SUM Nomb2 =', sum( Nomb2) )
    
     numb=[]
     del(lvlm)
     lvlm=[]
     lvli=[]
     Bomp_corr=[]
     Bomp_uncorr=[]
     Somp33=[]
     Nomb33=[]
     Nrej33=[]
     Bias33=[]
     for yy in range(0,len(lvls)  ):
      lvli.append( int( lvl[yy]))
      if (not Themask[yy]):
       lvlm.append( int(lvls[yy]))
       Bomp_corr.append(Bomp2[yy])
       Bomp_uncorr.append(Bomp2[yy]+Bias_corr[yy])
       Somp33.append(Somp2[yy])
       Nomb33.append(int(Nomb2[yy]))
       Nrej33.append(int(Nrej2[yy]))
    #========================GRAPHIQUE==================================================
     if(  graphe1[0] == 'BCORR'):
        ax.plot( Bomp_uncorr,lvlm, linestyle='--', marker='p', color='g',markersize=6 ) 
        ax.plot( Bias_corr,lvlm,  linestyle='--', marker='p', color='m',markersize=6 ) 
        ax.plot( Bomp_corr,lvlm, linestyle='--', marker='p', color='r',markersize=6 ) 
        ax.plot( Somp33,lvlm, linestyle='-', marker='o', color=couleurs[filn],markersize=4 ) 
       # print (' Bomp_corrige=',  Bomp_corr)
     elif(  graphe1[0] == 'REJETS'):
       ax.plot(Nrej33,lvlm,linestyle='-',drawstyle='steps', marker='*',color=couleurs[filn],markersize=4)
      # print (' rejets',Nrej33)
     elif(  graphe1[0] == 'NOBS'):
       ax.plot(Nomb33,lvlm,linestyle='-',drawstyle='steps', marker='*',color=couleurs[filn],markersize=6)
     else:  
       ax.plot( Bomp_corr,lvlm, linestyle='--',marker='o', color=couleurs[filn],markersize=4 )
       ax.plot( Somp33,lvlm, linestyle='-', marker='o', color=couleurs[filn],markersize=4 ) 
    
    #======TICK MARKS=ET LABEL===============================
     xlim = pylab.get(pylab.gca(), 'xlim')
     if varno  in graphe_nomvar :
      Nom2=graphe_nomvar[varno]
     else:
      Nom2=varno
     # print (  ' LE NOM2 est :', Nom2 )
     ylim=(0,max(lvls) )
   #  print (  ' VARNO = -------------------',varno,varno   in graphe_limites,graphe1[filenumb-1] )
     fixed_lims=varno in graphe_limites and ( graphe1[filenumb-1] == 'O-A' or graphe1[filenumb-1] == 'O-P'  or graphe1[filenumb-1] == 'BCORR')
    # print (  ' VARNO FIXED LIMS = -------------------',varno,fixed_lims )
     if fixed_lims   :
       xmin,xmax=graphe_limites[varno]
       xlim=(xmin,xmax)
       pylab.setp(pylab.gca(), xlim=xlim)
     #  print (  ' Xmin Xmax =', xmin,xmax )
    
     yticks=map(str, lvls)
     ax.set_yticks(lvls)
    
     yticks=map(str, lvli)
     ax.set_yticklabels(yticks,fontsize=6)
    
     
     pylab.setp(pylab.gca(), ylim=ylim[::SIGN])
    
     ax.set_ylabel(vcoord_type_e,color=NOIR,fontsize =16)
    #========================================================
    
    #=NOMBRE DE NONNEES ==================================================
     datapt=[]
     for y in  range(0,len(lvlm) ):
       datapt.append(( xlim[1]  , lvlm[y] ) )
     display_to_ax = ax.transAxes.inverted().transform
     data_to_display = ax.transData.transform
    
     if ( len(datapt) > 0):
      ax_pts = display_to_ax(data_to_display(datapt))
      for y in  range(0,len(lvlm) ):
        ix,iy=ax_pts[y]
        pylab.text(ix+.01+(filn)*0.06,iy  ,Nomb33[y] , fontsize =6,color=couleurs[filn] ,transform=ax.transAxes )
    #====================================================================
    #----------------------------------------------------------------------
     famille1=famille
    #LATLON=latlons
     REGION1=region
     LABEL1=label
     if(  graphe1[0] == 'BCORR'):
      l1=pylab.legend(legendlist,columnspacing=1, fancybox=True,ncol=4,shadow = True,facecolor="#C0C0C0",loc = (0.05,  -0.130),prop={'size':7},title='O-P')
    #ltext=pylab.gca().get_legend().get_texts()
    #pylab.setp(ltext[0], fontsize = 10, color = 'k')
    #----------------------------------------------------------------------
     bbox_propsR= dict(facecolor=couleurs[0],boxstyle='round')
    #pylab.text(-.03, -0.05, famille1+'_'+Nom+' '+fonction , fontsize =10,bbox=bbox_propsB ,transform=ax.transAxes)
     pylab.text(-.03, -0.05, famille1, fontsize =10,color=couleurs[0] ,transform=ax.transAxes)
     pylab.text(-.03, -0.07,f'{Nom} {fonction}' , fontsize =10,color=couleurs[0] ,transform=ax.transAxes)
     pylab.text(.45, 1.05 , REGION1 ,fontsize =10,color=couleurs[0] ,transform=ax.transAxes)
     pylab.text(.00, 1.05 , PERIODE ,fontsize =10,color=couleurs[0] ,transform=ax.transAxes)
     pylab.text(.75, 1.05 , LABEL1,  fontsize =12,color=couleurs[0] ,transform=ax.transAxes)
     Somp_comp.append(Somp33)
     if filn ==1:
    # LATLON2=latlons2
    # print (  '  TEXTE REGION2=',REGION2 )
    # REGION2=REGION2+ ' [ '+LATLON2  + ']'
      bbox_propsB = dict(facecolor=couleurs[1],boxstyle='round')
    # pylab.text(.53, -0.05, famille2+'_'+Nom2+' '+fonction2, fontsize =10,color=ROUGE         ,transform=ax.transAxes)
      pylab.text(.53, -0.05, famille2, fontsize =10,color=couleurs[1]         ,transform=ax.transAxes)
      pylab.text(.53, -0.08, f'{Nom2} {fonction2} ', fontsize =10,color=couleurs[1]         ,transform=ax.transAxes)
      pylab.text(.45, 1.09 , REGION2 ,fontsize =10,color=couleurs[1] ,transform=ax.transAxes)
      pylab.text(.00, 1.09 , PERIODE2,fontsize =10,color=couleurs[1] ,transform=ax.transAxes)
      pylab.text(.75, 1.09 , label2  ,fontsize =12,color=couleurs[1] ,transform=ax.transAxes)
    
    #==========================================================
     pylab.savefig(f'{pathwork}/profile/{id_stn}_{vcoord}_{varno}.png',format='png',dpi=100)
    #==========================================================

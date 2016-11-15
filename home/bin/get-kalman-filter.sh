#!/bin/sh

sFolderName='/hydro/data/dynamic_data/source/observation/kalman-filter'

for sFileLoc in "$sFolderName"/*".txt"
    do
        
      sFileTime=`date +%Y-%m-%d -r "$sFileLoc"`
        
      sFileYear=$(echo $sFileTime| cut -d'-' -f 1)
      sFileMonth=$(echo $sFileTime| cut -d'-' -f 2)
      sFileDay=$(echo $sFileTime| cut -d'-' -f 3)
      
      sFilePath=`dirname $sFileLoc`
      sFileName=`basename $sFileLoc`
      
      sFileNameExt="${sFileName##*.}" 
      sFileNameBase="${sFileName%.*}"
      
      echo $sFileNameExt $sFileNameBase
      
      sFileNameSource=$sFileName
      sFileNameDest=$sFileYear$sFileMonth$sFileDay'_'$sFileNameBase'.'$sFileNameExt
      
      sFilePathSource=$sFilePath
      sFilePathDest=$sFilePath/$sFileYear/$sFileMonth/$sFileDay
      
      mkdir -p $sFilePathDest
      
      cp -v $sFilePathSource/$sFileNameSource $sFilePathDest/$sFileNameDest
  
    done

//  gcc t2.cpp -l:libgdal.so -o t -w -lstdc++

#include "cpl_string.h"
#include "gdal_priv.h"
#include "cpl_conv.h" // for CPLMalloc()

int main(){
    GDALDataset  *poDataset;
    GDALAllRegister();
    const char* pszFilename = "o3.tif";
    poDataset = (GDALDataset *) GDALOpen( pszFilename, GA_ReadOnly );
    if( poDataset == NULL ){
        exit(1);
    }
    double adfGeoTransform[6];
    printf( "Driver: %s/%s\n",poDataset->GetDriver()->GetDescription(), poDataset->GetDriver()->GetMetadataItem( GDAL_DMD_LONGNAME ) );
    printf( "Size is %dx%dx%d\n",poDataset->GetRasterXSize(), poDataset->GetRasterYSize(),poDataset->GetRasterCount() );
    if( poDataset->GetProjectionRef()  != NULL )
        printf( "Projection is `%s'\n", poDataset->GetProjectionRef() );
    if( poDataset->GetGeoTransform( adfGeoTransform ) == CE_None ){
        printf( "Origin = (%.6f,%.6f)\n", adfGeoTransform[0], adfGeoTransform[3] );
        printf( "Pixel Size = (%.6f,%.6f)\n",adfGeoTransform[1], adfGeoTransform[5] );
    }
    printf( "adfGeoTransform = (%.6f,%.6f,%.6f,%.6f,%.6f,%.6f)\n", adfGeoTransform[0], adfGeoTransform[1], adfGeoTransform[2] , adfGeoTransform[3] , adfGeoTransform[4] , adfGeoTransform[5]);
    GDALRasterBand  *poBand;
    int             nBlockXSize, nBlockYSize;
    int             bGotMin, bGotMax;
    double          adfMinMax[2];
    printf( "poDataset->GetRasterCount() >> %d \n", poDataset->GetRasterCount());
    poBand = poDataset->GetRasterBand( 1 );  //red:1, green:2, blue:3
    poBand->GetBlockSize( &nBlockXSize, &nBlockYSize );
    printf( "Block=%dx%d Type=%s, ColorInterp=%s\n", nBlockXSize, nBlockYSize, GDALGetDataTypeName(poBand->GetRasterDataType()), GDALGetColorInterpretationName(poBand->GetColorInterpretation()) );
    adfMinMax[0] = poBand->GetMinimum( &bGotMin );
    adfMinMax[1] = poBand->GetMaximum( &bGotMax );
    if( ! (bGotMin && bGotMax) )
        GDALComputeRasterMinMax((GDALRasterBandH)poBand, TRUE, adfMinMax);

    printf( "Min=%.3fd, Max=%.3f\n", adfMinMax[0], adfMinMax[1] );
    if( poBand->GetOverviewCount() > 0 )
        printf( "Band has %d overviews.\n", poBand->GetOverviewCount() );

    if( poBand->GetColorTable() != NULL )
        printf( "Band has a color table with %d entries.\n",poBand->GetColorTable()->GetColorEntryCount() );


    float *pafScanline ,*pafScanline2, *pafScanline3;
    int nXSize  =   poBand->GetXSize();
    int nYSize  =   poBand->GetYSize();
    printf( "GetXSize()=%d\t, GetYSize()=%d\n", nXSize, nYSize );
    pafScanline = (float *) CPLMalloc(sizeof(float)*(512*512));
    pafScanline2 = (float *) CPLMalloc(sizeof(float)*(512*512));
    pafScanline3 = (float *) CPLMalloc(sizeof(float)*(512*512));
    poBand->RasterIO( GF_Read, 0, 0, 512, 512, pafScanline, 512, 512, GDT_Float32, 0, 0 );
    poBand = poDataset->GetRasterBand( 2 );
    poBand->RasterIO( GF_Read, 0, 0, 512, 512, pafScanline2, 512, 512, GDT_Float32, 0, 0 );
    poBand = poDataset->GetRasterBand( 3 );
    poBand->RasterIO( GF_Read, 0, 0, 512, 512, pafScanline3, 512, 512, GDT_Float32, 0, 0 );

    // for(int i=0; i<=256*256; i++){
    //     // if(*pafScanline > (float)250.0)
    //         // printf( "pafScanline=%f\n", *pafScanline );
    //     pafScanline++;
    // }
    const char *pszFormat = "GTiff";
    GDALDriver *poDriver;
    char **papszMetadata;
    poDriver = GetGDALDriverManager()->GetDriverByName(pszFormat);
    if( poDriver == NULL )
        exit( 1 );
    papszMetadata = poDriver->GetMetadata();
    if( CSLFetchBoolean( papszMetadata, GDAL_DCAP_CREATE, FALSE ) )
        printf( "Driver %s supports Create() method.\n", pszFormat );
    if( CSLFetchBoolean( papszMetadata, GDAL_DCAP_CREATECOPY, FALSE ) )
        printf( "Driver %s supports CreateCopy() method.\n", pszFormat );

    const char* pszDstFilename = "ob.tif";
    GDALDataset *poDstDS = poDriver->CreateCopy( pszDstFilename, poDataset, FALSE,NULL, NULL, NULL );
    /* Once we're done, close properly the dataset */
    if( poDstDS != NULL )
        GDALClose( (GDALDatasetH) poDstDS );
    GDALClose( (GDALDatasetH) poDataset );
    return 0;
}
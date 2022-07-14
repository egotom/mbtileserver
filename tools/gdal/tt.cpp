#include "gdal_priv.h"
#include "cpl_conv.h" // for CPLMalloc()
#include "cpl_string.h"

int main(){
    GDALDataset  *poDataset;
    GDALAllRegister();
    poDataset = (GDALDataset *) GDALOpen( pszFilename, GA_ReadOnly );
    if( poDataset == NULL ){
        printf( "open failed \n");
		exit( 1 );
    }

	//adfGeoTransform[0] /* top left x */
	//adfGeoTransform[1] /* w-e pixel resolution */
	//adfGeoTransform[2] /* 0 */
	//adfGeoTransform[3] /* top left y */
	//adfGeoTransform[4] /* 0 */
	//adfGeoTransform[5] /* n-s pixel resolution (negative value) */

	// GT(0) x-coordinate of the upper-left corner of the upper-left pixel.
	// GT(1) w-e pixel resolution / pixel width.
	// GT(2) row rotation (typically zero).
	// GT(3) y-coordinate of the upper-left corner of the upper-left pixel.
	// GT(4) column rotation (typically zero).
	// GT(5) n-s pixel resolution / pixel height (negative value for a north-up image).

	double adfGeoTransform[6];
	printf( "Driver: %s/%s\n", poDataset->GetDriver()->GetDescription(),poDataset->GetDriver()->GetMetadataItem( GDAL_DMD_LONGNAME ) );
	printf( "Size is %dx%dx%d\n", poDataset->GetRasterXSize(), poDataset->GetRasterYSize(),poDataset->GetRasterCount() );
	if( poDataset->GetProjectionRef()  != NULL )
		printf( "Projection is `%s'\n", poDataset->GetProjectionRef() );
	if( poDataset->GetGeoTransform( adfGeoTransform ) == CE_None ){
		printf( "Origin = (%.6f,%.6f)\n", adfGeoTransform[0], adfGeoTransform[3] );
		printf( "Pixel Size = (%.6f,%.6f)\n", adfGeoTransform[1], adfGeoTransform[5] );
	}
	
	GDALRasterBand  *poBand;
	int             nBlockXSize, nBlockYSize;
	int             bGotMin, bGotMax;
	double          adfMinMax[2];
	poBand = poDataset->GetRasterBand( 1 );
	poBand->GetBlockSize( &nBlockXSize, &nBlockYSize );
	printf( "Block=%dx%d Type=%s, ColorInterp=%s\n", nBlockXSize, nBlockYSize, GDALGetDataTypeName(poBand->GetRasterDataType()),GDALGetColorInterpretationName(poBand->GetColorInterpretation()) );
	adfMinMax[0] = poBand->GetMinimum( &bGotMin );
	adfMinMax[1] = poBand->GetMaximum( &bGotMax );
	if( !(bGotMin && bGotMax) )
		GDALComputeRasterMinMax((GDALRasterBandH)poBand, TRUE, adfMinMax);
	printf( "Min=%.3fd, Max=%.3f\n", adfMinMax[0], adfMinMax[1] );
	if( poBand->GetOverviewCount() > 0 )
		printf( "Band has %d overviews.\n", poBand->GetOverviewCount() );
	if( poBand->GetColorTable() != NULL )
		printf( "Band has a color table with %d entries.\n",poBand->GetColorTable()->GetColorEntryCount() );
	
	
	//CPLErr GDALRasterBand::RasterIO( GDALRWFlag eRWFlag,
    //                            int nXOff, int nYOff, int nXSize, int nYSize,
    //                            void * pData, int nBufXSize, int nBufYSize,
    //                            GDALDataType eBufType,
    //                            int nPixelSpace,
    //                            int nLineSpace )
	float *pafScanline;
	int   nXSize = poBand->GetXSize();
	pafScanline = (float *) CPLMalloc(sizeof(float)*nXSize);
	poBand->RasterIO( GF_Read, 0, 0, nXSize, 1,pafScanline, nXSize, 1, GDT_Float32,0, 0 );
	
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
	
	
	GDALDataset *poSrcDS = (GDALDataset *) GDALOpen( pszSrcFilename, GA_ReadOnly );
	GDALDataset *poDstDS = poDriver->CreateCopy( pszDstFilename, poSrcDS, FALSE,NULL, NULL, NULL );
	/* Once we're done, close properly the dataset */
	if( poDstDS != NULL )
		GDALClose( (GDALDatasetH) poDstDS );
	GDALClose( (GDALDatasetH) poSrcDS );
	
	char **papszOptions = NULL;
	papszOptions = CSLSetNameValue( papszOptions, "TILED", "YES" );
	papszOptions = CSLSetNameValue( papszOptions, "COMPRESS", "PACKBITS" );
	poDstDS = poDriver->CreateCopy( pszDstFilename, poSrcDS, FALSE,papszOptions, GDALTermProgress, NULL );
	/* Once we're done, close properly the dataset */
	if( poDstDS != NULL )
		GDALClose( (GDALDatasetH) poDstDS );
	CSLDestroy( papszOptions );
	
	GDALDataset *poDstDS;
	char **papszOptions = NULL;
	poDstDS = poDriver->Create( pszDstFilename, 512, 512, 1, GDT_Byte,papszOptions );
	
	double adfGeoTransform[6] = { 444720, 30, 0, 3751320, 0, -30 };
	OGRSpatialReference oSRS;
	char *pszSRS_WKT = NULL;
	GDALRasterBand *poBand;
	GByte abyRaster[512*512];
	poDstDS->SetGeoTransform( adfGeoTransform );
	oSRS.SetUTM( 11, TRUE );
	oSRS.SetWellKnownGeogCS( "NAD27" );
	oSRS.exportToWkt( &pszSRS_WKT );
	poDstDS->SetProjection( pszSRS_WKT );
	CPLFree( pszSRS_WKT );
	poBand = poDstDS->GetRasterBand(1);
	poBand->RasterIO( GF_Write, 0, 0, 512, 512,abyRaster, 512, 512, GDT_Byte, 0, 0 );
	/* Once we're done, close properly the dataset */
	GDALClose( (GDALDatasetH) poDstDS );
}
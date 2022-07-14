//  gcc t.cpp -l:libgdal.so -o t -w -lstdc++

#include "cpl_string.h"
#include "gdal_priv.h"
#include "cpl_conv.h" // for CPLMalloc()

void Tile(const char *pszSrcFile, const char *pszDstFile,int iStartX, int iStartY, int iSizeX, int iSizeY/*, const char* pszFormat*/){
	GDALAllRegister();
	GDALDataset *pSrcDS = (GDALDataset*)GDALOpen(pszSrcFile, GA_ReadOnly);
	GDALDataType RDT = pSrcDS->GetRasterBand(1)->GetRasterDataType();
		
	int RBC = pSrcDS->GetRasterCount();
	double adfGeoTransform[6] = {0};
	pSrcDS->GetGeoTransform(adfGeoTransform);
	adfGeoTransform[0] = adfGeoTransform[0] + iStartX*adfGeoTransform[1] + iStartY*adfGeoTransform[2];
	adfGeoTransform[3] = adfGeoTransform[3] + iStartX*adfGeoTransform[4] + iStartY*adfGeoTransform[5];
    printf( "(%.6f, %.6f, %.6f, %.6f, %.6f, %.6f)\n", adfGeoTransform[0], adfGeoTransform[1], adfGeoTransform[2] , adfGeoTransform[3] , adfGeoTransform[4] , adfGeoTransform[5]);
	GDALDriver *poDriver = GetGDALDriverManager()->GetDriverByName(GDALGetDriverShortName(GDALGetDatasetDriver(pSrcDS)));
	GDALDataset *pDstDS = poDriver->Create( pszDstFile, iSizeX, iSizeY, RBC, RDT, NULL);
	pDstDS->SetGeoTransform(adfGeoTransform);
	pDstDS->SetProjection(pSrcDS->GetProjectionRef());

	int *pBandMap = new int[RBC];
	for(int i = 0; i < RBC; i++ )
		pBandMap[i]= i+1;

    char *pDataBuff = new char[iSizeX*iSizeY*RBC];
    pSrcDS->RasterIO(GF_Read, iStartX,iStartY,iSizeX, iSizeY, pDataBuff, iSizeX,  iSizeY, RDT, RBC, pBandMap, 0, 0, 0);
    pDstDS->RasterIO(GF_Write, 0, 0,  iSizeX,  iSizeY, pDataBuff,  iSizeX,  iSizeY, RDT, RBC, pBandMap, 0, 0, 0);

	delete(pBandMap);
	GDALClose((GDALDatasetH)pSrcDS);
	GDALClose((GDALDatasetH)pDstDS);
}


int main(){
    GDALAllRegister();
    GDALDataset  *poDataset, *poDstDS;
    int iStartX=0,  iStartY=3000, iWX=256, iWY=256;
    const char *pszFilename = "o3.tif", *pszDstFilename = "oa5.tif";
    poDataset = (GDALDataset *) GDALOpen( pszFilename, GA_ReadOnly );
    double adfGeoTransform[6]={0};
    poDataset->GetGeoTransform( adfGeoTransform );
    
    adfGeoTransform[0] = adfGeoTransform[0] + iStartX*adfGeoTransform[1] + iStartY*adfGeoTransform[2];
	adfGeoTransform[3] = adfGeoTransform[3] + iStartX*adfGeoTransform[4] + iStartY*adfGeoTransform[5];
    adfGeoTransform[1] = adfGeoTransform[1]*2;
    adfGeoTransform[5] = adfGeoTransform[5]*2;
    printf( "(%.6f, %.6f, %.6f, %.6f, %.6f, %.6f)\n", adfGeoTransform[0], adfGeoTransform[1], adfGeoTransform[2] , adfGeoTransform[3] , adfGeoTransform[4] , adfGeoTransform[5]);
    GDALDataType RDT = poDataset->GetRasterBand(1) -> GetRasterDataType();
    int RC = poDataset->GetRasterCount();
    int Band[RC];
    for(int i = 0; i < RC; i++ )
		Band[i]= i+1;

    char *pBuffer =(char *) CPLMalloc(sizeof(char)*(iWX*iWY*RC));
    poDataset->RasterIO( GF_Read, iStartX, iStartY, iWX, iWY, pBuffer, iWX, iWY, RDT, RC, Band, 0, 0 , 0);

    GDALDriver *poDriver = GetGDALDriverManager()->GetDriverByName(GDALGetDriverShortName(GDALGetDatasetDriver(poDataset)));;
    poDstDS = poDriver->Create( pszDstFilename, iWX, iWY, RC, RDT, NULL );
    
    poDstDS->SetGeoTransform( adfGeoTransform );
    poDstDS->SetProjection( poDataset->GetProjectionRef() );
    poDstDS->RasterIO( GF_Write, 0, 0, iWX, iWY, pBuffer, iWX, iWY, RDT, RC, Band, 0, 0, 0);
    printf( "(%s)\n", poDataset->GetProjectionRef());
    GDALClose( (GDALDatasetH) poDataset );
    GDALClose( (GDALDatasetH) poDstDS );

    // const char *pszSrcFile = "./o3.tif";
    // const char *pszDstFile = "./t3.tif";
    // // ImageCut(pszSrcFile, pszDstFile, 300,  300,  256, 256);
    // Tile(pszSrcFile, pszDstFile, 300,  300,  256, 256);
    return 0;
}


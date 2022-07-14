// gcc rp.cpp -l:libgdal.so -o r -lstdc++

#include "gdalwarper.h"
#include "cpl_conv.h" // for CPLMalloc()

int main(){
	GDALDatasetH hSrcDS, hDstDS;
	// Open input and output files.
	GDALAllRegister();
	hSrcDS = GDALOpen( "./o3.tif", GA_ReadOnly );
	hDstDS = GDALOpen( "./o3r.tif", GA_Update );
	// Setup warp options.
	GDALWarpOptions *psWarpOptions = GDALCreateWarpOptions();
	psWarpOptions->hSrcDS = hSrcDS;
	psWarpOptions->hDstDS = hDstDS;
	psWarpOptions->nBandCount = 1;
	psWarpOptions->panSrcBands =(int *) CPLMalloc(sizeof(int) * psWarpOptions->nBandCount );
	psWarpOptions->panSrcBands[0] = 1;
	psWarpOptions->panDstBands =(int *) CPLMalloc(sizeof(int) * psWarpOptions->nBandCount );
	psWarpOptions->panDstBands[0] = 1;
	psWarpOptions->pfnProgress = GDALTermProgress;
	psWarpOptions->pTransformerArg = GDALCreateGenImgProjTransformer( hSrcDS,GDALGetProjectionRef(hSrcDS),hDstDS,GDALGetProjectionRef(hDstDS),FALSE, 0.0, 1 );
	psWarpOptions->pfnTransformer = GDALGenImgProjTransform;
	// Initialize and execute the warp operation.
	GDALWarpOperation oOperation;
	oOperation.Initialize( psWarpOptions );
	oOperation.ChunkAndWarpImage( 0, 0, GDALGetRasterXSize( hDstDS ), GDALGetRasterYSize( hDstDS ) );
	GDALDestroyGenImgProjTransformer( psWarpOptions->pTransformerArg );
	GDALDestroyWarpOptions( psWarpOptions );
	GDALClose( hDstDS );
	GDALClose( hSrcDS );
	return 0;
}
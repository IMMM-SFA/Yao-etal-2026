<!--[![DOI](https://zenodo.org/badge/265254045.svg)](https://zenodo.org/doi/10.5281/zenodo.10442485)-->

# Yao_etal_2026

**Land-use and atmospheric shifts jointly amplify U.S. drought-driven crop losses**

Lili Yao<sup>1*</sup>, Hongxiang Yan<sup>1</sup>, Ning Sun<sup>1*</sup>, Eva Sinha<sup>1</sup>, Kanishka B. Narayan<sup>1</sup>, Travis B. Thurber<sup>1</sup>, and Jennie Rice<sup>1</sup>

<sup>1 </sup> Pacific Northwest National Laboratory, Richland, WA, USA
<br/>

\* Correspondence: Lili Yao, lili.yao@pnnl.gov; Ning Sun, ning.sun@pnnl.gov

## Abstract
Agricultural drought (AD), driven by root-zone soil moisture deficits, poses a major threat to food security. However, its future risk is commonly assessed by treating land-use and land-cover change (LULCC) and atmospheric shifts as independent drivers, overlooking their interacting and compounding effects. To address this gap, we use an integrated, multi-scale, multi-sector modeling framework to project AD risk for corn and soybean across the contiguous United States (CONUS) through 2055 under a range of plausible futures that link thermodynamic changes and LULCC pathways through shared socioeconomic and emissions scenarios. Model projections reveal sharp increases in drought-driven crop production losses. These losses are estimated as the drought-affected cultivated area multiplied by the yield deficit between the non-drought reference yield and simulated yield. Projected future losses rise by nearly 60% for corn and 135% for soybean relative to historical levels.  LULCC acts as a driver of similar magnitude to atmospheric change, with the strongest amplification occurring where cropland expansion overlaps with drought-prone areas, such as the Great Plains. These findings highlight that interactions between LULCC and atmospheric shifts shape future agricultural drought risk and should be jointly considered to support effective adaptation and food-system planning.

## Journal reference
Land-use and atmospheric shifts jointly amplify U.S. drought-driven crop losses. Accepted by npj Natural Hazards – July 2026.

## Data Reference

### Input Data
|       Dataset       |               URL                |               DOI                |
|:-------------------:|:--------------------------------------------:|:--------------------------------:|
| TGW-WRF | https://tgw-data.msdlive.org/ | https://doi.org/10.1038/s41597-023-02485-5, https://doi.org/10.57931/1885756 |
| GCAM-SELECT-Demeter | https://data.msdlive.org/records/vy529-6eg15 | https://doi.org/10.57931/2502083 |

### Output Data
| Dataset | URL | DOI |
|:-------:|:---:|:---:|
| CLM5 soil moisture and crop yield simulations | https://data.msdlive.org/records/gmcgt-pvx90 | https://doi.org/10.57931/3012125 |

### Contributing Modeling Software
| Model | Version | URL | DOI |
|:-----:|:-------:|:---:|:---:|
| CLM5  |  ctsm5.1.dev118 | https://github.com/IMMM-SFA/im3-clm | https://zenodo.org/records/6653705 |
| IM3 Components | 0cf45e8 | https://github.com/IMMM-SFA/im3components/tree/main/im3components/wrf\_to\_clm | |

## Reproduce my experiment

Clone the [CLM5 repository](https://github.com/ESCOMP/CTSM/tree/ctsm5.1.dev118) to set up the CLM5 model. You will need to download the [TGW forcing data](https://data.msdlive.org/records/ksw6r-2xv06) and convert them into CLM input format using these [scripts](https://github.com/IMMM-SFA/im3components/tree/main/im3components/wrf\_to\_clm). You will also need to replace the default CLM surface and landuse timeseries files using data from the [GCAM-SELECT-Demeter](https://data.msdlive.org/records/vy529-6eg15). In addition, hydrological parameter values in the default parameter file and the user name list file should be updated based the [behavioral parameter values](https://data.msdlive.org/records/41bw1-3q739). The [output data repository](https://data.msdlive.org/records/gmcgt-pvx90) already contains the soil moisutre and crop yield output from the CLM5 model so you can skip rerunning the CLM5 model if you want to save time.

## Reproduce my figures
Use the scripts found in the `figures` directory to reproduce the figures used in this publication.

| Figure Numbers | Script Name | Description | Figure |
|:--------------:|:-----------:|:-----------:|:------:|
| 1  | [Figure_1.py](./figures/Figure_1.py) | Validation of CLM5 simulations of drought and crop productivity and CLM5-derived drought-induced financial losses | <a href="./figures/Figure_1.tif"><img width="100" src="./figures/Figure_1.png"/></a> |
| 2  | [Figure_2.m](./figures/Figure_2.m) | Rainfed corn and soybean planting-area changes across the CONUS under future scenarios | <a href="./figures/Figure_2.tif"><img width="100" src="./figures/Figure_2.tif"/></a> |
| 3  | [Figure_3.py](./figures/Figure_3.py) | Future warming and LULCC alter growing-season agricultural drought exposure and intensity for corn and soybean | <a href="./figures/Figure_3.tif"><img width="100" src="./figures/Figure_3.tif"/></a> |
| 4  | [Figure_4.py](./figures/Figure_4.py) | Contributions of warming and LULCC to future drought-induced crop production losses | <a href="./figures/Figure_4.tif"><img width="100" src="./figures/Figure_4.tif"/></a> |
| 5  | [Figure_5.py](./figures/Figure_5.py) | Scenario and ESM-variant divergence in drought-induced production loss projections | <a href="./figures/Figure_5.tif"><img width="100" src="./figures/Figure_5.tif"/></a> |
| 6  | [Figure_6.py](./figures/Figure_6.py) | Relative differences in financial loss between atm45_ssp3 and atm85_ssp5 scenarios | <a href="./figures/Figure_6.tif"><img width="100" src="./figures/Figure_6.tif"/></a> |
| S1 | [Figure_S1.m](./figures/Figure_S1.m) | Projected land-use and land-cover changes across U.S. regions and scenarios | <a href="./figures/Figure_S1.png"><img width="100" src="./figures/Figure_S1.png"/></a> |
| S2 | [Figure_S2.m](./figures/Figure_S2.m) | Future warming occurs across U.S. regions and seasons | <a href="./figures/Figure_S2.png"><img width="100" src="./figures/Figure_S2.png"/></a> |
| S3 | [Figure_S3.m](./figures/Figure_S3.m) | Projected precipitation changes vary strongly by season and region | <a href="./figures/Figure_S3.png"><img width="100" src="./figures/Figure_S3.png"/></a> |
| S4 | [Figure_S4.m](./figures/Figure_S4.m) | Potential evapotranspiration increases across U.S. regions and seasons | <a href="./figures/Figure_S4.png"><img width="100" src="./figures/Figure_S4.png"/></a> |
| S5 | [Figure_S5.m](./figures/Figure_S5.m) | Projected decreases in the aridity index indicate widespread drying, especially in summer | <a href="./figures/Figure_S5.png"><img width="100" src="./figures/Figure_S5.png"/></a> |
| S6 | [Figure_S6.m](./figures/Figure_S6.m) | Future atmospheric and land-use changes alter growing-season drought duration for corn and soybean | <a href="./figures/Figure_S6.png"><img width="100" src="./figures/Figure_S6.png"/></a> |
| S7 | [Figure_S7.py](./figures/Figure_S7.py) | Scenario differences in financial losses vary by crop, region, and Earth System Model (ESM) variant | <a href="./figures/Figure_S7.png"><img width="100" src="./figures/Figure_S7.png"/></a> |
| S8  | [Figure_S8.py](./figures/Figure_S8.py) | GCAM-derived crop prices are consistently higher under atm45_ssp3 than under atm85_ssp5 | <a href="./figures/figures/Figure_S8.png"><img width="100" src="./figures/Figure_S8.png"/></a> |
| S9  | [Figure_S9.py](./figures/Figure_S9.py) | Annual crop production losses and commodity prices across scenarios and major producing regions | <a href="./figures/Figure_S9.png"><img width="100" src="./figures/Figure_S9.png"/></a> |
| S10 | [Figure_S10.py](./figures/Figure_S10.py) | Sensitivity analysis using median non-drought reference yields quantifies warming and land-use contributions to corn and soybean production losses | <a href="./figures/Figure_S10.png"><img width="100" src="./figures/Figure_S10.png"/></a> |
| S11 | [Figure_S11.py](./figures/Figure_S11.py) | Sensitivity analysis using median non-drought reference yields quantifies scenario and Earth System Model (ESM)-variant divergence in crop production losses | <a href="./figures/Figure_S11.png"><img width="100" src="./figures/Figure_S11.png"/></a> |
| S12 | [Figure_S12.py](./figures/Figure_S12.py) | Sensitivity analysis using median non-drought reference yields compares scenario-driven financial-loss differences for corn and soybean | <a href="./figures/Figure_S12.png"><img width="100" src="./figures/Figure_S12.png"/></a> |
| S13 | [Figure_S13.py](./figures/Figure_S13.py) | Sensitivity to a stricter SSMI drought threshold is evaluated for corn and soybean drought exposure and intensity | <a href="./figures/Figure_S13.png"><img width="100" src="./figures/Figure_S13.png"/></a> |
| S14 | [Figure_S14.py](./figures/Figure_S14.py) | Sensitivity to a stricter SSMI drought threshold is evaluated for warming and land-use contributions to crop production losses | <a href="./figures/Figure_S14.png"><img width="100" src="./figures/Figure_S14.png"/></a> |
| S15 | [Figure_S15.py](./figures/Figure_S15.py) | Sensitivity to a stricter SSMI threshold is evaluated for scenario and Earth System Model (ESM)-variant divergence in crop production losses | <a href="./figures/Figure_S15.png"><img width="100" src="./figures/Figure_S15.png"/></a> |
| S16 | [Figure_S16.py](./figures/Figure_S16.py) | Sensitivity to a stricter SSMI threshold is evaluated for scenario-driven financial-loss differences | <a href="./figures/Figure_S16.png"><img width="100" src="./figures/Figure_S16.png"/></a> |
| S17 | [Figure_S17.py](./figures/Figure_S17.py) | CLM5 wheat simulations are evaluated against observed production, yield anomalies, and insurance indemnities in the Northern Great Plains | <a href="./figures/Figure_S17.png"><img width="100" src="./figures/Figure_S17.png"/></a> |
| S18 | [Figure_S18.py](./figures/Figure_S18.py) | Future land-use and atmospheric changes affect wheat area, drought exposure, production losses, and financial losses | <a href="./figures/Figure_S18.png"><img width="100" src="./figures/Figure_S18.png"/></a> |
| S19 | [Figure_S19.py](./figures/Figure_S19.py) | Sensitivity analysis using a September–June growing season quantifies future wheat drought exposure, intensity, and duration | <a href="./figures/Figure_S19.png"><img width="100" src="./figures/Figure_S19.png"/></a> |
| S20 | [Figure_S20.py](./figures/Figure_S20.py) | Seasonal patterns of the wheat productivity and future soil-moisture changes in the Southern Great Plains | <a href="./figures/Figure_S20.png"><img width="100" src="./figures/Figure_S20.png"/></a> |



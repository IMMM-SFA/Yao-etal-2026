<!--[![DOI](https://zenodo.org/badge/265254045.svg)](https://zenodo.org/doi/10.5281/zenodo.10442485)-->

# yao_etal_2026

**Coupled Atmospheric and Land-use Shifts Amplify Drought-driven Crop Losses Across the U.S.**

Lili Yao<sup>1*</sup>, Hongxiang Yan<sup>1</sup>, Ning Sun<sup>1*</sup>, Eva Sinha<sup>1</sup>, Kanishka B. Narayan<sup>1</sup>, Travis B. Thurber<sup>1</sup>, and Jennie Rice<sup>1</sup>

<sup>1 </sup> Pacific Northwest National Laboratory, Richland, WA, USA
<br/>

\* Correspondence: Lili Yao, lili.yao@pnnl.gov; Ning Sun, ning.sun@pnnl.gov

## Abstract
Agricultural drought (AD), driven by root-zone soil moisture deficits, poses a major threat to food security. However, its future risk is commonly assessed by treating atmospheric and land-use change as independent drivers, failing to account for their co-evolving interactions that jointly shape AD trajectories. To address this gap, we use an integrated, multi-scale, multi-sector modeling framework to project AD risks for major crops across the contiguous United States (CONUS) through 2055 under a range of plausible futures that capture thermodynamic changes and land-use and land-cover change (LULCC) pathways. Model projections reveal that drought-driven crop production losses (drought-affected area × yield reduction) increase sharply, growing by nearly 60% for corn, 250% for wheat, and 135% for soybean relative to historical levels. The primary drivers of these increases, which include atmospheric shifts and LULCC, vary by region and crop type.  LULCC acts as an important risk amplifier in regions experiencing cropland expansion into drought-prone areas, such as the Great Plains and northwestern U.S. Wheat exhibits the largest increases in crop loss, a result that remains robust across scenarios. These findings highlight that interactions between atmospheric conditions and land-use trajectories shape future agricultural drought risk and should be jointly considered to support effective adaptation and food-system planning.

## Journal reference
Coupled Atmospheric and Land-use Shifts Amplify Drought-driven Crop Losses Across the U.S. Submitted to npj Natural Hazards – April 2026.

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
| 1  | [Figure_1.py](./figures/Figure_1.py) | Validation of CLM’s performance | <a href="./figures/figures/Figure_1.png"><img width="100" src="./figures/figures/Figure_1.png"/></a> |
| 2  | [Figure_2.m](./figures/Figure_2.m) | Rainfed crop planting areas changes  | <a href="./figures/figures/Figure_2.png"><img width="100" src="./figures/figures/Figure_2.png"/></a> |
| 3  | [Figure_3.py](./figures/Figure_3.py) | Drought exposure and intensity | <a href="./figures/figures/Figure_3.png"><img width="100" src="./figures/figures/Figure_3.png"/></a> |
| 4  | [Figure_4.py](./figures/Figure_4.py) | Mean projected changes in production loss | <a href="./figures/figures/Figure_4.png"><img width="100" src="./figures/figures/Figure_4.png"/></a> |
| 5  | [Figure_5.py](./figures/Figure_5.py) | Scenario and ESM variant uncertainty in projection | <a href="./figures/figures/Figure_5.png"><img width="100" src="./figures/figures/Figure_5.png"/></a> |
| 6  | [Figure_6.py](./figures/Figure_6.py) | Relative differences in financial loss between scenarios | <a href="./figures/figures/Figure_6.png"><img width="100" src="./figures/figures/Figure_6.png"/></a> |
| S1  | [Figure_S1.py](./figures/Figure_S1.py) | Projected changes for nine land use and land cover types | <a href="./figures/figures/Figure_S1.png"><img width="100" src="./figures/figures/Figure_S1.png"/></a> |
| S2  | [Figure_S2.m](./figures/Figure_S2.m) | Projected changes in annual and seasonal air temperature | <a href="./figures/figures/Figure_S2.png"><img width="100" src="./figures/figures/Figure_S2.png"/></a> |
| S3  | [Figure_S3.m](./figures/Figure_S3.m) | Projected changes in annual and seasonal precipitation | <a href="./figures/figures/Figure_S3.png"><img width="100" src="./figures/figures/Figure_S3.png"/></a> |
| S4  | [Figure_S4.m](./figures/Figure_S4.m) | Projected changes in annual and seasonal potential evapotranspiration | <a href="./figures/figures/Figure_S4.png"><img width="100" src="./figures/figures/Figure_S4.png"/></a> |
| S5  | [Figure_S5.m](./figures/Figure_S5.m) | Projected changes in annual and seasonal aridity index | <a href="./figures/figures/Figure_S5.png"><img width="100" src="./figures/figures/Figure_S5.png"/></a> |
| S6  | [Figure_S6.m](./figures/Figure_S6.m) | Agricultural drought duration under historical and future scenarios | <a href="./figures/figures/Figure_S6.png"><img width="100" src="./figures/figures/Figure_S6.png"/></a> |
| S7  | [Figure_S7.py](./figures/Figure_S7.py) | Relative differences in financial loss for cooler and hotter variants | <a href="./figures/figures/Figure_S7.png"><img width="100" src="./figures/figures/Figure_S7.png"/></a> |
| S8  | [Figure_S8.py](./figures/Figure_S8.py) | Ratio of crop prices between scenarios | <a href="./figures/figures/Figure_S8.png"><img width="100" src="./figures/figures/Figure_S8.png"/></a> |



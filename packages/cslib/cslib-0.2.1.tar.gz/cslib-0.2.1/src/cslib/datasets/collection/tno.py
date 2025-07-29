from typing import Callable, Optional, Union
from torchvision.datasets.vision import VisionDataset
from torchvision.datasets.utils import download_and_extract_archive
from pathlib import Path
from PIL import Image

__all__ = ['TNO']

class TNO(VisionDataset):
    """ TNO dataset for image fusion.

    The TNO dataset is a collection of LWIR, NIR, and visible images for image fusion tasks.
    It includes both paired and sequential images for different scenarios. 
    Details: https://figshare.com/articles/dataset/TNO_Image_Fusion_Dataset/1008029

    Args:
        root (str): Root directory of the dataset where ``TNO_Image_Fusion_Dataset`` exists.
        transform (callable, optional): E.g, ``transforms.ToTensor``
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
        mode (str, optional): Mode of the dataset to use. It can be 'both', 'pairs', or 'sequence'.
            'both' includes both pairs and sequence data, 'pairs' includes only paired data,
            and 'sequence' includes only sequential data.
        img_type (str, optional): Image type to use. It can be 'both', 'lwir', or 'nir'.
            'both' includes LWIR and NIR images, 'lwir' includes only LWIR images,
            and 'nir' includes only NIR images.
    """
    file = {
        'pairs':{
            'tank':{
                'lwir': 'tank/LWIR.tif',
                'vis': 'tank/Vis.tif',
                'valid': True
            },
            '2_men_in_front_of_house':{
                'lwir': 'Athena_images/2_men_in_front_of_house/IR_meting003_g.bmp',
                'vis': 'Athena_images/2_men_in_front_of_house/VIS_meting003_r.bmp',
                'valid': True
            },
            'airplane_in_trees':{
                'lwir': 'Athena_images/airplane_in_trees/ir.bmp',
                'vis': 'Athena_images/airplane_in_trees/vis.bmp',
                'valid': True
            },
            'APC_1_1':{
                'lwir': 'Athena_images/APC_1/view_1/IR_fk_06_005.bmp',
                'vis': 'Athena_images/APC_1/view_1/VIS_fk_06_005.bmp',
                'valid': True
            },
            'APC_1_2':{
                'lwir': 'Athena_images/APC_1/view_2/IR_fk_ref_01_005.bmp',
                'vis': 'Athena_images/APC_1/view_2/VIS_fk_ref_01_005.bmp',
                'valid': True
            },
            'APC_1_3':{
                'lwir': 'Athena_images/APC_1/view_3/IR_fk_ref_02_005.bmp',
                'vis': 'Athena_images/APC_1/view_3/VIS_fk_ref_02_005.bmp',
                'valid': True
            },
            'APC_2_1':{
                'lwir': 'Athena_images/APC_2/view_1/2_fk_ge_03_005.bmp',
                'vis': 'Athena_images/APC_2/view_1/1_fk_ge_03_005.bmp',
                'valid': True
            },
            'APC_2_2':{
                'lwir': 'Athena_images/APC_2/view_2/2_fk_ge_04_005.bmp',
                'vis': 'Athena_images/APC_2/view_2/1_fk_ge_04_005.bmp',
                'valid': True
            },
            'APC_2_3':{
                'lwir': 'Athena_images/APC_2/view_3/2_fk_ge_06_005.bmp',
                'vis': 'Athena_images/APC_2/view_3/1_fk_ge_06_005.bmp',
                'valid': True
            },
            'APC_3_1':{
                'lwir': 'Athena_images/APC_3/view_1/IR_fk_bar_06_005.bmp',
                'vis': 'Athena_images/APC_3/view_1/VIS_fk_bar_06_005.bmp',
                'valid': True
            },
            'APC_3_2':{
                'lwir': 'Athena_images/APC_3/view_2/IR_fk_NL_01_005.bmp',
                'vis': 'Athena_images/APC_3/view_2/VIS_fk_NL_01_005.bmp',
                'valid': True
            },
            'APC_3_3':{
                'lwir': 'Athena_images/APC_3/view_3/IR_fk_NL_05_005.bmp',
                'vis': 'Athena_images/APC_3/view_3/VIS_fk_NL_05_005.bmp',
                'valid': True
            },
            'APC_4':{
                'lwir': 'Athena_images/APC_4/IR_fennek01_005.bmp',
                'vis': 'Athena_images/APC_4/VIS_fennek01_005.bmp',
                'valid': True
            },
            'bunker':{
                'lwir': 'Athena_images/bunker/IR_bunker_g.bmp',
                'vis': 'Athena_images/bunker/bunker_r.bmp',
                'valid': True
            },
            'heather':{
                'lwir': 'Athena_images/heather/IR_hei_vis_g.bmp',
                'vis': 'Athena_images/heather/VIS_hei_vis_r.bmp',
                'valid': True
            },
            'helicopter':{
                'lwir': 'Athena_images/helicopter/IR_helib_011.bmp',
                'vis': 'Athena_images/helicopter/VIS_helib_011.bmp',
                'valid': True
            },
            'lake':{
                'lwir': 'Athena_images/lake/IR_lake_g.bmp',
                'vis': 'Athena_images/lake/VIS_lake_r.bmp',
                'valid': True
            },
            'man_in_doorway':{
                'lwir': 'Athena_images/man_in_doorway/IR_maninhuis_g.bmp',
                'vis': 'Athena_images/man_in_doorway/VIS_maninhuis_r.bmp',
                'valid': True
            },
            'soldier_behind_smoke_1':{
                'lwir': 'Athena_images/soldier_behind_smoke_1/IR_meting012-1200_g.bmp',
                'vis': 'Athena_images/soldier_behind_smoke_1/VIS_meting012-1200_r.bmp',
                'valid': True
            },
            'soldier_behind_smoke_2':{
                'lwir': 'Athena_images/soldier_behind_smoke_2/IR_meting012-1500_g.bmp',
                'vis': 'Athena_images/soldier_behind_smoke_2/VIS_meting012-1500_r.bmp',
                'valid': True
            },
            'soldier_behind_smoke_3':{
                'lwir': 'Athena_images/soldier_behind_smoke_3/IR_meting012-1700_g.bmp',
                'vis': 'Athena_images/soldier_behind_smoke_3/VIS_meting012-1700_r.bmp',
                'valid': True
            },
            'soldier_in_trench_1':{
                'lwir': 'Athena_images/soldier_in_trench_1/IR_meting016_g.bmp',
                'vis': 'Athena_images/soldier_in_trench_1/VIS_meting016_r.bmp',
                'valid': True
            },
            'soldier_in_trench_2':{
                'lwir': 'Athena_images/soldier_in_trench_2/IR_meting055_g.bmp',
                'vis': 'Athena_images/soldier_in_trench_2/VIS_meting055_r.bmp',
                'valid': True
            },
            'Balls':{
                'nir': 'Triclobs_images/Balls/NIR.bmp',
                'vis': 'Triclobs_images/Balls/VIS.bmp',
                'valid': True
            },
            'barbed_wire_1':{
                'nir': 'Triclobs_images/barbed_wire_1/G_NIR.tif',
                'lwir': 'Triclobs_images/barbed_wire_1/B_LWIR.tif',
                'vis': 'Triclobs_images/barbed_wire_1/R_Vis.tif',
                'valid': True
            },
            'barbed_wire_2':{
                'nir': 'Triclobs_images/barbed_wire_2/b_NIR-MarnehNew_24RGB_1110.tif',
                'lwir': 'Triclobs_images/barbed_wire_2/c_LWIR-MarnehNew_24RGB_1110.tif',
                'vis': 'Triclobs_images/barbed_wire_2/a_VIS-MarnehNew_24RGB_1110.tif',
                'valid': True
            },
            'Bosnia':{
                'nir': 'Triclobs_images/Bosnia/NIR_G.bmp',
                'lwir': 'Triclobs_images/Bosnia/LWIR_B.bmp',
                'vis': 'Triclobs_images/Bosnia/VIS_R.bmp',
                'valid': True
            },
            'Farm':{
                'nir': 'Triclobs_images/Farm/Farm_II.bmp',
                'lwir': 'Triclobs_images/Farm/Farm_IR.bmp',
                'vis': 'Triclobs_images/Farm/Farm_Vis.bmp',
                'valid': True
            },
            'House':{
                'nir': 'Triclobs_images/House/NIR.bmp',
                'vis': 'Triclobs_images/House/VIS.bmp',
                'valid': True
            },
            'houses_with_3_men':{
                'nir': 'Triclobs_images/houses_with_3_men/NIR.bmp',
                'lwir': 'Triclobs_images/houses_with_3_men/LWIR.bmp',
                'vis': 'Triclobs_images/houses_with_3_men/VIS.bmp',
                'valid': True
            },
            'jeep_in_smoke':{
                'nir': 'Triclobs_images/jeep_in_smoke/NIR_G.bmp',
                'lwir': 'Triclobs_images/jeep_in_smoke/LWIR_B.bmp',
                'vis': 'Triclobs_images/jeep_in_smoke/VIS_R.bmp',
                'valid': True
            },
            'Kaptein_01':{
                'nir': 'Triclobs_images/Kaptein_01/NIR01.bmp',
                'lwir': 'Triclobs_images/Kaptein_01/IR01.bmp',
                'vis': 'Triclobs_images/Kaptein_01/Vis01.bmp',
                'valid': True
            },
            'Kaptein_19':{
                'nir': 'Triclobs_images/Kaptein_19/NIR19.bmp',
                'lwir': 'Triclobs_images/Kaptein_19/IR19.bmp',
                'vis': 'Triclobs_images/Kaptein_19/Vis19.bmp',
                'valid': True
            },
            'Kaptein_1123':{
                'nir': 'Triclobs_images/Kaptein_1123/Kaptein_1123_II.bmp',
                'lwir': 'Triclobs_images/Kaptein_1123/Kaptein_1123_IR.bmp',
                'vis': 'Triclobs_images/Kaptein_1123/Kaptein_1123_Vis.bmp',
                'valid': True
            },
            'Kaptein_1654':{
                'nir': 'Triclobs_images/Kaptein_1654/Kaptein_1654_II.bmp',
                'lwir': 'Triclobs_images/Kaptein_1654/Kaptein_1654_IR.bmp',
                'vis': 'Triclobs_images/Kaptein_1654/Kaptein_1654_Vis.bmp',
                'valid': True
            },
            'Marne_01':{
                'nir': 'Triclobs_images/Marne_01/Marne_01_II.bmp',
                'lwir': 'Triclobs_images/Marne_01/Marne_01_IR.bmp',
                'vis': 'Triclobs_images/Marne_01/Marne_01_Vis.bmp',
                'valid': True
            },
            'Marne_02':{
                'nir': 'Triclobs_images/Marne_02/Marne_02_II.bmp',
                'lwir': 'Triclobs_images/Marne_02/Marne_02_IR.bmp',
                'vis': 'Triclobs_images/Marne_02/Marne_02_Vis.bmp',
                'valid': True
            },
            'Marne_03':{
                'nir': 'Triclobs_images/Marne_03/Marne_03_II.bmp',
                'lwir': 'Triclobs_images/Marne_03/Marne_03_IR.bmp',
                'vis': 'Triclobs_images/Marne_03/Marne_03_Vis.bmp',
                'valid': True
            },
            'Marne_04':{
                'nir': 'Triclobs_images/Marne_04/Marne_04_II.bmp',
                'lwir': 'Triclobs_images/Marne_04/Marne_04_IR.bmp',
                'vis': 'Triclobs_images/Marne_04/Marne_04_Vis.bmp',
                'valid': True
            },
            'Marne_06':{
                'nir': 'Triclobs_images/Marne_06/Marne_06_II.bmp',
                'lwir': 'Triclobs_images/Marne_06/Marne_06_IR.bmp',
                'vis': 'Triclobs_images/Marne_06/Marne_06_Vis.bmp',
                'valid': True
            },
            'Marne_07':{
                'nir': 'Triclobs_images/Marne_07/Marne_07_II.bmp',
                'lwir': 'Triclobs_images/Marne_07/Marne_07_IR.bmp',
                'vis': 'Triclobs_images/Marne_07/Marne_07_Vis.bmp',
                'valid': True
            },
            'Marne_09':{
                'nir': 'Triclobs_images/Marne_09/Marne_09_II.bmp',
                'lwir': 'Triclobs_images/Marne_09/Marne_09_IR.bmp',
                'vis': 'Triclobs_images/Marne_09/Marne_09_Vis.bmp',
                'valid': True
            },
            'Marne_11':{
                'nir': 'Triclobs_images/Marne_11/Marne_11_II.bmp',
                'lwir': 'Triclobs_images/Marne_11/Marne_11_IR.bmp',
                'vis': 'Triclobs_images/Marne_11/Marne_11_Vis.bmp',
                'valid': True
            },
            'Marne_15':{
                'nir': 'Triclobs_images/Marne_15/Marne_15_II.bmp',
                'lwir': 'Triclobs_images/Marne_15/Marne_15_IR.bmp',
                'vis': 'Triclobs_images/Marne_15/Marne_15_Vis.bmp',
                'valid': True
            },
            'Marne_24':{
                'nir': 'Triclobs_images/Marne_24/Marne_24_II.bmp',
                'lwir': 'Triclobs_images/Marne_24/Marne_24_IR.bmp',
                'vis': 'Triclobs_images/Marne_24/Marne_24_Vis.bmp',
                'valid': True
            },
            'Movie_01':{
                'nir': 'Triclobs_images/Movie_01/Movie_01_II.bmp',
                'lwir': 'Triclobs_images/Movie_01/Movie_01_IR.bmp',
                'vis': 'Triclobs_images/Movie_01/Movie_01_Vis.bmp',
                'valid': True
            },
            'Movie_12':{
                'nir': 'Triclobs_images/Movie_12/Movie_12_II.bmp',
                'lwir': 'Triclobs_images/Movie_12/Movie_12_IR.bmp',
                'vis': 'Triclobs_images/Movie_12/Movie_12_Vis.bmp',
                'valid': True
            },
            'Movie_14':{
                'nir': 'Triclobs_images/Movie_14/Movie_14_II.bmp',
                'lwir': 'Triclobs_images/Movie_14/Movie_14_IR.bmp',
                'vis': 'Triclobs_images/Movie_14/Movie_14_Vis.bmp',
                'valid': True
            },
            'Movie_18':{
                'nir': 'Triclobs_images/Movie_18/Movie_18_II.bmp',
                'lwir': 'Triclobs_images/Movie_18/Movie_18_IR.bmp',
                'vis': 'Triclobs_images/Movie_18/Movie_18_Vis.bmp',
                'valid': True
            },
            'Movie_24':{
                'nir': 'Triclobs_images/Movie_24/Movie_24_II.bmp',
                'lwir': 'Triclobs_images/Movie_24/Movie_24_IR.bmp',
                'vis': 'Triclobs_images/Movie_24/Movie_24_Vis.bmp',
                'valid': True
            },
            'pancake_house':{
                'nir': 'Triclobs_images/pancake_house/NIR.tif',
                'vis': 'Triclobs_images/pancake_house/VIS.tif',
                'valid': True
            },
            'Reek':{
                'nir': 'Triclobs_images/Reek/Reek_II.bmp',
                'lwir': 'Triclobs_images/Reek/Reek_IR.bmp',
                'vis': 'Triclobs_images/Reek/Reek_Vis.bmp',
                'valid': True
            },
            'soldier_behind_smoke':{
                'nir': 'Triclobs_images/soldier_behind_smoke/NIR-MarnehNew_15RGB_603.tif',
                'lwir': 'Triclobs_images/soldier_behind_smoke/LWIR-MarnehNew_15RGB_603.tif',
                'vis': 'Triclobs_images/soldier_behind_smoke/VIS-MarnehNew_15RGB_603.tif',
                'valid': True
            },
            'soldiers_with_jeep':{
                'nir': 'Triclobs_images/soldiers_with_jeep/Jeep_II.bmp',
                'lwir': 'Triclobs_images/soldiers_with_jeep/Jeep_IR.bmp',
                'vis': 'Triclobs_images/soldiers_with_jeep/Jeep_Vis.bmp',
                'valid': True
            },
            'square_with_houses':{
                'nir': 'Triclobs_images/square_with_houses/NIR.bmp',
                'lwir': 'Triclobs_images/square_with_houses/LWIR.bmp',
                'vis': 'Triclobs_images/square_with_houses/VIS.bmp',
                'valid': True
            },
            'Veluwe':{
                'nir': 'Triclobs_images/Veluwe/NIR.bmp',
                'vis': 'Triclobs_images/Veluwe/VIS.bmp',
                'valid': True
            },
            'Vlasakkers':{
                'nir': 'Triclobs_images/Vlasakkers/NIR.tif',
                'vis': 'Triclobs_images/Vlasakkers/VIS.tif',
                'valid': True
            },
            'bench':{
                'nir': 'DHV_images/bench/NIR_37dhvG.bmp',
                'lwir': 'DHV_images/bench/IR_37rad.bmp',
                'vis': 'DHV_images/bench/VIS_37dhvR.bmp',
                'valid': True
            },
            'sandpath':{
                'nir': 'DHV_images/sandpath/NIR_18dhvG.bmp',
                'lwir': 'DHV_images/sandpath/IR_18rad.bmp',
                'vis': 'DHV_images/sandpath/VIS_18dhvR.bmp',
                'valid': True
            },
            'wall':{
                'nir': 'DHV_images/wall/NIR_163dhvG.BMP',
                'lwir': 'DHV_images/wall/IR_163rad.bmp',
                'vis': 'DHV_images/wall/VIS_163dhvR.BMP',
                'valid': True
            },
        },
        'sequence':{
            'Fire1':{
                'lwir': {
                    'base': 'DHV_images/Fire_sequence/part_1/thermal',
                    'content': [
                        'RAD2.bmp', 'RAD3.bmp', 'RAD4.bmp', 'RAD5.bmp', 
                        'RAD6.bmp', 'RAD7.bmp', 'RAD8.bmp', 'RAD9.bmp', 
                        'RAD10.bmp', 'RAD11.bmp', 'RAD12.bmp', 'RAD13.bmp', 
                        'RAD14.bmp', 'RAD15.bmp', 'RAD16.bmp', 'RAD17.bmp', 
                        'RAD18.bmp', 'RAD19.bmp', 'RAD20.bmp', 'RAD21.bmp', 
                        'RAD22.bmp', 'RAD23.bmp', 'RAD24.bmp', 'RAD25.bmp', 
                        'RAD26.bmp', 'RAD27.bmp', 'RAD28.bmp', 'RAD29.bmp'
                    ]
                },
                'vis': {
                    'base': 'DHV_images/Fire_sequence/part_1/dhv',
                    'content': [
                        'DHV2.bmp', 'DHV3.bmp', 'DHV4.bmp', 'DHV5.bmp', 
                        'DHV6.bmp', 'DHV7.bmp', 'DHV8.bmp', 'DHV9.bmp', 
                        'DHV10.bmp', 'DHV11.bmp', 'DHV12.bmp', 'DHV13.bmp', 
                        'DHV14.bmp', 'DHV15.bmp', 'DHV16.bmp', 'DHV17.bmp', 
                        'DHV18.bmp', 'DHV19.bmp', 'DHV20.bmp', 'DHV21.bmp', 
                        'DHV22.bmp', 'DHV23.bmp', 'DHV24.bmp', 'DHV25.bmp', 
                        'DHV26.bmp', 'DHV27.bmp', 'DHV28.bmp', 'DHV29.bmp'
                    ]
                },
                'valid': True
            },
            'Fire2':{
                'lwir': {
                    'base': 'DHV_images/Fire_sequence/part_2/rad',
                    'content': [
                        'RADheli0.bmp','RADheli1.bmp','RADheli2.bmp','RADheli3.bmp','RADheli4.bmp',
                        'RADheli5.bmp','RADheli6.bmp','RADheli7.bmp','RADheli8.bmp',
                        'RADheli9.bmp','RADheli10.bmp','RADheli11.bmp','RADheli12.bmp',
                        'RADheli13.bmp','RADheli14.bmp','RADheli15.bmp','RADheli16.bmp'
                    ]
                },
                'vis': {
                    'base': 'DHV_images/Fire_sequence/part_2/dhv',
                    'content': [
                        'DHVheli0.bmp','DHVheli1.bmp','DHVheli2.bmp','DHVheli3.bmp','DHVheli4.bmp',
                        'DHVheli5.bmp','DHVheli6.bmp','DHVheli7.bmp','DHVheli8.bmp',
                        'DHVheli9.bmp','DHVheli10.bmp','DHVheli11.bmp','DHVheli12.bmp',
                        'DHVheli13.bmp','DHVheli14.bmp','DHVheli15.bmp','DHVheli16.bmp'
                    ]
                },
                'valid': True
            },
            'Fire3':{
                'lwir': {
                    'base': 'DHV_images/Fire_sequence/part_3/rad',
                    'content': [
                        'RADheli20.bmp','RADheli21.bmp','RADheli22.bmp','RADheli23.bmp','RADheli24.bmp',
                        'RADheli25.bmp','RADheli26.bmp','RADheli27.bmp','RADheli28.bmp','RADheli29.bmp',
                        'RADheli30.bmp','RADheli31.bmp','RADheli32.bmp','RADheli33.bmp','RADheli34.bmp',
                        'RADheli35.bmp','RADheli36.bmp','RADheli37.bmp','RADheli38.bmp','RADheli39.bmp',
                        'RADheli40.bmp','RADheli41.bmp','RADheli42.bmp','RADheli43.bmp','RADheli44.bmp',
                        'RADheli45.bmp','RADheli46.bmp','RADheli47.bmp','RADheli48.bmp','RADheli49.bmp',
                        'RADheli50.bmp','RADheli51.bmp','RADheli52.bmp','RADheli53.bmp','RADheli54.bmp',
                        'RADheli55.bmp','RADheli56.bmp','RADheli57.bmp','RADheli58.bmp','RADheli59.bmp',
                        'RADheli60.bmp','RADheli61.bmp','RADheli62.bmp','RADheli63.bmp','RADheli64.bmp',
                        'RADheli65.bmp','RADheli66.bmp','RADheli67.bmp','RADheli68.bmp','RADheli69.bmp',
                        'RADheli70.bmp','RADheli71.bmp','RADheli72.bmp','RADheli73.bmp','RADheli74.bmp',
                        'RADheli75.bmp','RADheli76.bmp','RADheli77.bmp','RADheli78.bmp','RADheli79.bmp',
                        'RADheli80.bmp'
                    ]
                },
                'vis': {
                    'base': 'DHV_images/Fire_sequence/part_3/dhv',
                    'content': [
                        'DHVheli20.bmp','DHVheli21.bmp','DHVheli22.bmp','DHVheli23.bmp','DHVheli24.bmp',
                        'DHVheli25.bmp','DHVheli26.bmp','DHVheli27.bmp','DHVheli28.bmp','DHVheli29.bmp',
                        'DHVheli30.bmp','DHVheli31.bmp','DHVheli32.bmp','DHVheli33.bmp','DHVheli34.bmp',
                        'DHVheli35.bmp','DHVheli36.bmp','DHVheli37.bmp','DHVheli38.bmp','DHVheli39.bmp',
                        'DHVheli40.bmp','DHVheli41.bmp','DHVheli42.bmp','DHVheli43.bmp','DHVheli44.bmp',
                        'DHVheli45.bmp','DHVheli46.bmp','DHVheli47.bmp','DHVheli48.bmp','DHVheli49.bmp',
                        'DHVheli50.bmp','DHVheli51.bmp','DHVheli52.bmp','DHVheli53.bmp','DHVheli54.bmp',
                        'DHVheli55.bmp','DHVheli56.bmp','DHVheli57.bmp','DHVheli58.bmp','DHVheli59.bmp',
                        'DHVheli60.bmp','DHVheli61.bmp','DHVheli62.bmp','DHVheli63.bmp','DHVheli64.bmp',
                        'DHVheli65.bmp','DHVheli66.bmp','DHVheli67.bmp','DHVheli68.bmp','DHVheli69.bmp',
                        'DHVheli70.bmp','DHVheli71.bmp','DHVheli72.bmp','DHVheli73.bmp','DHVheli74.bmp',
                        'DHVheli75.bmp','DHVheli76.bmp','DHVheli77.bmp','DHVheli78.bmp','DHVheli79.bmp',
                        'DHVheli80.bmp'
                    ]
                },
                'valid': True
            },
            'Duine':{
                'lwir': {
                    'base': 'FEL_images/Duine_sequence/thermal',
                    'content': [
                        '7400i.bmp','7401i.bmp','7402i.bmp','7403i.bmp','7404i.bmp',
                        '7405i.bmp','7406i.bmp','7407i.bmp','7408i.bmp','7409i.bmp',
                        '7410i.bmp','7411i.bmp','7412i.bmp','7413i.bmp','7414i.bmp',
                        '7415i.bmp','7416i.bmp','7417i.bmp','7418i.bmp','7419i.bmp',
                        '7420i.bmp','7421i.bmp','7422i.bmp'
                    ]
                },
                'vis': {
                    'base': 'FEL_images/Duine_sequence/visual',
                    'content': [
                        '7400v.bmp','7401v.bmp','7402v.bmp','7403v.bmp','7404v.bmp',
                        '7405v.bmp','7406v.bmp','7407v.bmp','7408v.bmp','7409v.bmp',
                        '7410v.bmp','7411v.bmp','7412v.bmp','7413v.bmp','7414v.bmp',
                        '7415v.bmp','7416v.bmp','7417v.bmp','7418v.bmp','7419v.bmp',
                        '7420v.bmp','7421v.bmp','7422v.bmp'
                    ]
                },
                'valid': True
            },
            'Nato_camp':{
                'lwir': {
                    'base': 'FEL_images/Nato_camp_sequence/thermal',
                    'content': [
                        '1800i.bmp','1801i.bmp','1802i.bmp','1803i.bmp','1804i.bmp',
                        '1805i.bmp','1806i.bmp','1807i.bmp','1808i.bmp','1809i.bmp',
                        '1810i.bmp','1811i.bmp','1812i.bmp','1813i.bmp','1814i.bmp',
                        '1815i.bmp','1816i.bmp','1817i.bmp','1818i.bmp','1819i.bmp',
                        '1820i.bmp','1821i.bmp','1822i.bmp','1823i.bmp','1824i.bmp',
                        '1825i.bmp','1826i.bmp','1827i.bmp','1828i.bmp','1829i.bmp',
                        '1830i.bmp','1831i.bmp',
                    ]
                },
                'vis': {
                    'base': 'FEL_images/Nato_camp_sequence/visual',
                    'content': [
                        '1800v.bmp','1801v.bmp','1802v.bmp','1803v.bmp','1804v.bmp',
                        '1805v.bmp','1806v.bmp','1807v.bmp','1808v.bmp','1809v.bmp',
                        '1810v.bmp','1811v.bmp','1812v.bmp','1813v.bmp','1814v.bmp',
                        '1815v.bmp','1816v.bmp','1817v.bmp','1818v.bmp','1819v.bmp',
                        '1820v.bmp','1821v.bmp','1822v.bmp','1823v.bmp','1824v.bmp',
                        '1825v.bmp','1826v.bmp','1827v.bmp','1828v.bmp','1829v.bmp',
                        '1830v.bmp','1831v.bmp',
                    ]
                },
                'valid': True
            },
            'Tree':{
                'lwir': {
                    'base': 'FEL_images/Tree_sequence/thermal',
                    'content': [
                        '4900i.bmp','4901i.bmp','4902i.bmp','4903i.bmp','4904i.bmp',
                        '4905i.bmp','4906i.bmp','4907i.bmp','4908i.bmp','4909i.bmp',
                        '4910i.bmp','4911i.bmp','4912i.bmp','4913i.bmp','4914i.bmp',
                        '4915i.bmp','4916i.bmp','4917i.bmp','4918i.bmp'
                    ]
                },
                'vis': {
                    'base': 'FEL_images/Tree_sequence/visual',
                    'content': [
                        '4900v.bmp','4901v.bmp','4902v.bmp','4903v.bmp','4904v.bmp',
                        '4905v.bmp','4906v.bmp','4907v.bmp','4908v.bmp','4909v.bmp',
                        '4910v.bmp','4911v.bmp','4912v.bmp','4913v.bmp','4914v.bmp',
                        '4915v.bmp','4916v.bmp','4917v.bmp','4918v.bmp'
                    ]
                },
                'valid': True
            }
        }
    }
    url = "https://figshare.com/ndownloader/files/1475454"
    md5 = "1ab9ce3b84dd3e5894630c13abd20953"

    def __init__(
        self,
        root: Union[str, Path],
        transform: Optional[Callable] = None,
        download: bool = True,
        mode: Optional[str] = ['both', 'pairs', 'sequence'][0],
        img_type: Optional[str] = ['both', 'lwir', 'nir'][1],
        fusion: bool = False, 
        fusion_path: Union[Path, str] = '',
        fused_extension: Optional[str] = 'png',
        export_root: Optional[Union[str,Path]] = None,
        exported: bool = False,
        export_lwir_dir: str = 'lwir',
        export_nir_dir: str = 'nir',
        export_vis_dir: str = 'vis',
        dataloader: bool = True,
    ) -> None:
        super().__init__(root, transform=transform)
        self.folder = 'TNO_Image_Fusion_Dataset'
        self._base_folder = Path(self.root) / "tno"
        assert mode in ['both', 'pairs', 'sequence']
        self.mode = mode
        assert img_type in ['both', 'lwir', 'nir']
        self.img_type = img_type
        self.fusion = fusion
        self.fusion_path = fusion_path
        self.fused_extension = fused_extension
        if self.fusion:
            assert self.fusion_path != ''
            self.fusion_path = Path(self.fusion_path)
        self.dataloader = dataloader
        if export_root is None:
            self.export_root = Path(self.root) / 'tno' / 'tno'
        else:
            self.export_root = Path(export_root)
        self.export_lwir_dir = export_lwir_dir
        self.export_nir_dir = export_nir_dir
        self.export_vis_dir = export_vis_dir
        self.exported = exported
        if self.exported:
            self.build_exported()
        else:
            self.build_origin()

        if download:
            self.download()
    
    def _load_image(self, path):
        img = Image.open(path).convert("L")
        return self.transform(img) if self.transform else img

    def __getitem__(self, idx: int):
        res = {'vis': self._load_image(self.data[idx]['vis'])}
        if not self.dataloader:
            res.update({'vis_path': self.data[idx]['vis']})
        if 'lwir' in self.data[idx]:
            if not self.dataloader:
                res.update({'lwir_path': self.data[idx]['lwir']})
            res.update({'lwir': self._load_image(self.data[idx]['lwir'])})
        if 'nir' in self.data[idx]:
            if not self.dataloader:
                res.update({'nir_path': self.data[idx]['nir']})
            res.update({'nir': self._load_image(self.data[idx]['nir'])})
        if self.fusion:
            if not self.dataloader:
                res.update({'fused_path': Path(self.fusion_path) / f"{self.data[idx]['vis'].stem}.{self.fused_extension}"})
            res.update({'fused': self._load_image(Path(self.fusion_path) / f"{self.data[idx]['vis'].stem}.{self.fused_extension}")})
        return res
    
    def __len__(self):
        return len(self.data)
    
    def build_exported(self):
        self.data = []
        vis_list = [i.name for i in (self.export_root / self.export_vis_dir).iterdir()]
        lwir_list = [i.name for i in (self.export_root / self.export_lwir_dir).iterdir()]
        nir_list = [i.name for i in (self.export_root / self.export_nir_dir).iterdir()]
        if self.img_type == 'lwir':
            for i in lwir_list:
                assert i in vis_list
                self.data.append({
                    'lwir': self.export_root / self.export_lwir_dir / i,
                    'vis': self.export_root / self.export_vis_dir / i,
                })
        if self.img_type == 'nir':
            for i in nir_list:
                assert i in vis_list
                self.data.append({
                    'nir': self.export_root / self.export_nir_dir / i,
                    'vis': self.export_root / self.export_vis_dir / i,
                })
        if self.img_type == 'both':
            for i in nir_list:
                if i not in lwir_list:
                    continue
                assert i in vis_list
                self.data.append({
                    'lwir': self.export_root / self.export_lwir_dir / i,
                    'nir': self.export_root / self.export_nir_dir / i,
                    'vis': self.export_root / self.export_vis_dir / i,
                })
        
    def build_origin(self):
        self.data = []
        if self.mode in ['both', 'pairs']:
            for _,v in self.file['pairs'].items():
                if v['valid'] == False:
                    continue
                if self.img_type == 'lwir':
                    if 'lwir' not in v:
                        continue
                    self.data.append({
                        'lwir': self._base_folder / self.folder / v['lwir'],
                        'vis': self._base_folder / self.folder / v['vis']
                    })
                if self.img_type == 'nir':
                    if 'nir' not in v:
                        continue
                    self.data.append({
                        'nir': self._base_folder / self.folder / v['nir'],
                        'vis': self._base_folder / self.folder / v['vis']
                    })
                if self.img_type == 'both':
                    if ('lwir' not in v) or ('nir' not in v) :
                        continue
                    self.data.append({
                        'lwir': self._base_folder / self.folder / v['lwir'],
                        'nir': self._base_folder / self.folder / v['nir'],
                        'vis': self._base_folder / self.folder / v['vis']
                    })
        if self.mode in ['both', 'sequence']:
            for _,v in self.file['sequence'].items():
                if v['valid'] == False:
                    continue
                if self.img_type == 'lwir':
                    if 'lwir' not in v:
                        continue
                    for i,j in zip(v['lwir']['content'], v['vis']['content']):
                        self.data.append({
                            'lwir': self._base_folder / self.folder / v['lwir']['base'] / i,
                            'vis': self._base_folder / self.folder / v['vis']['base'] / j
                        })
                if self.img_type == 'nir':
                    if 'nir' not in v:
                        continue
                    for i,j in zip(v['nir']['content'], v['vis']['content']):
                        self.data.append({
                            'nir': self._base_folder / self.folder / v['nir']['base'] / i,
                            'vis': self._base_folder / self.folder / v['vis']['base'] / j
                        })
                if self.img_type == 'both':
                    if ('lwir' not in v) or ('nir' not in v) :
                        continue
                    for i,j,k in zip(v['lwir']['content'], v['nir']['content'], v['vis']['content']):
                        self.data.append({
                            'lwir': self._base_folder / self.folder / v['lwir']['base'] / i,
                            'nir': self._base_folder / self.folder / v['nir']['base'] / j,
                            'vis': self._base_folder / self.folder / v['vis']['base'] / k
                        })
    
    def _scale_bad_image(self,bad_scale_img_dir):
        bad_scale_img = Image.open(bad_scale_img_dir)
        width, height = bad_scale_img.size
        cropped_image = bad_scale_img.crop((0, 10, width, height))
        cropped_image.save(bad_scale_img_dir)
    
    def _resize_bad_image(self,bad_size_img_dir):
        bad_img = Image.open(bad_size_img_dir)
        resized_image = bad_img.resize((640,480), resample=1) # Resampling.LANCZOS
        resized_image.save(bad_size_img_dir)
    
    def _rgb_to_gray(self,bad_color_image_dir):
        bad_img = Image.open(bad_color_image_dir)
        gray_image = bad_img.convert('L')
        gray_image.save(bad_color_image_dir)

    def download(self):
        valid = True
        for d in self.data:
            for _,v in d.items():
                if not v.exists():
                    valid = False
        if valid == False:
            download_and_extract_archive(
                        url=self.url,
                        download_root=self._base_folder,
                        extract_root=self._base_folder,
                        filename="tno_temp.zip",
                        md5=self.md5,
                        remove_finished=False
                    )
            self._scale_bad_image(self._base_folder / self.folder / 'Triclobs_images' / 'Marne_15' / 'Marne_15_IR.bmp')
            self._scale_bad_image(self._base_folder / self.folder / 'Triclobs_images' / 'Marne_15' / 'Marne_15_II.bmp')
            self._resize_bad_image(self._base_folder / self.folder / 'Triclobs_images' / 'Movie_24' / 'Movie_24_IR.bmp')
            self._rgb_to_gray(self._base_folder / self.folder / 'DHV_images' / 'bench' / 'IR_37rad.bmp')
            self._rgb_to_gray(self._base_folder / self.folder / 'DHV_images' / 'wall' / 'IR_163rad.bmp')
            
            if (self._base_folder / 'tno').exists() == False:
                (self._base_folder / 'tno').mkdir() # export default dir
    
    def export(self, dest_dir = None):
        '''
        Export TNO dataset to a folder for operation with matlab.
        
        MATLAB Usage Example:
        
        # %% Read JSON config file
        # filename = 'config.json';
        # fileID = fopen(filename, 'r', 'n', 'utf8');
        # jsonData = fread(fileID, inf, 'uint8');
        # jsonData = char(jsonData');
        # fclose(fileID);
        # 
        # %% Parse JSON data
        # config = jsondecode(jsonData);
        # disp(config);
        # 
        # %% Access specific fields
        # visJson = config.vis_json;
        # nirJson = config.nir_json;
        # lwirJson = config.lwir_json;
        # visNirPairs = config.vis_nir_pairs;
        # visLwirPairs = config.vis_lwir_pairs;
        # visNirLwirPairs = config.vis_nir_lwir_pairs;
        # 
        # %% Example: Access vis_json content
        # disp(visJson);
        '''
        assert self.exported == False
        # make dir
        if dest_dir is None:
            dest_dir = Path(self.root) / 'tno' / 'tno'
        dest_dir = Path(dest_dir)
        assert dest_dir.exists()
        dest_vis_dir = dest_dir / self.export_vis_dir
        dest_lwir_dir = dest_dir / self.export_lwir_dir
        dest_nir_dir = dest_dir / self.export_nir_dir
        if dest_vis_dir.exists() == False:
            dest_vis_dir.mkdir()
        if dest_lwir_dir.exists() == False:
            dest_lwir_dir.mkdir()
        if dest_nir_dir.exists() == False:
            dest_nir_dir.mkdir()
        export_list = []
        index_counter = 1
        
        # pair images
        for _,v in self.file['pairs'].items():
            d = {
                'id': index_counter,
                'vis': self._base_folder / self.folder / v['vis']
            }
            if 'lwir' in v:
                d['lwir'] = self._base_folder / self.folder / v['lwir']
            if 'nir' in v:
                d['nir'] = self._base_folder / self.folder / v['nir']
            export_list.append(d)
            index_counter = index_counter + 1
        
        # sequence images
        for _,v in self.file['sequence'].items(): # all sequence are lwir and vis
            for i,j in zip(v['lwir']['content'], v['vis']['content']):
                export_list.append({
                    'id': index_counter,
                    'lwir': self._base_folder / self.folder / v['lwir']['base'] / i,
                    'vis': self._base_folder / self.folder / v['vis']['base'] / j
                })
                index_counter = index_counter + 1

        # copy images
        import shutil
        for d in export_list:
            shutil.copy(d['vis'],dest_vis_dir / f'{d['id']}.{d['vis'].name.split(".")[-1].lower()}')
            if 'nir' in d:
                shutil.copy(d['nir'],dest_nir_dir / f'{d['id']}.{d['nir'].name.split(".")[-1].lower()}')
            if 'lwir' in d:
                shutil.copy(d['lwir'],dest_lwir_dir / f'{d['id']}.{d['lwir'].name.split(".")[-1].lower()}')

        # save config file
        import json
        vis_json = {}            # Mapping vis id to origin path
        nir_json = {}            # Mapping nir id to origin path
        lwir_json = {}           # Mapping lwir id to origin path
        vis_nir = []             # id of vis and nir pairs
        vis_lwir = []            # id of vis and lwir pairs
        vis_nir_lwir = []        # id of vis nir and lwir pairs
        for d in export_list:
            vis_json[str(d['id'])] = str(d['vis'])
            if 'nir' in d:
                nir_json[str(d['id'])] = str(d['nir'])
            if 'lwir' in d:
                lwir_json[str(d['id'])] = str(d['lwir'])
            if 'nir' in d and 'lwir' in d:
                vis_nir_lwir.append(d['id'])
            if 'nir' in d:
                vis_nir.append(d['id'])
            if 'lwir' in d:
                vis_lwir.append(d['id'])
        config_data = {
            "vis": vis_json,
            "nir": nir_json,
            "lwir": lwir_json,
            "vis_nir_pairs": vis_nir,
            "vis_lwir_pairs": vis_lwir,
            "vis_nir_lwir_pairs": vis_nir_lwir
        }
        dest_config_dir = dest_dir / "config.json"
        with open(dest_config_dir, 'w') as json_file:
            json.dump(config_data, json_file, indent=4)
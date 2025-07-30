# -*- coding: utf-8 -*-
"""dataset module from the GeoDataKit: provides example datasets

This module provides exampel datasets for testing and demonstrating the
various tools from this package.

Datasets are provided in the form of :class:`pandas.DataFrame` gather in a dict
called `dataset`.

List of datasets:
    -orientation: A dataset to manipulate orientations
"""

import pandas as pd

def get_dataset(name:str):
    """
    Accessor to the datasets.

    Parameters
    ----------
    name : str
        name of the selected dataset.

    Returns
    -------
    A :class:`pd.DataFrame` containing the dataset

    """
    return dataset[name]

def get_description(name:str):
    """
    Access the description of a given dataset.

    Parameters
    ----------
    name : str
        name of the dataset.

    Returns
    -------
    A string containing the description of the dataset.

    """
    return dataset_description[name]

def list_dataset(description:bool = False):
    """Provides a list of available dataset
    
    Parameters
    ----------
    description: bool, optional
        if True, a description of the datasets is also returned
        
    Returns
    ----------
    A list containing the name of the dataset that can be used as keys 
    for retrieving it with `get_dataset(name)`.
    If `description` is True, a `dict()` associating each key with its 
    description (Datasets with missing description are ignored).
    """
    return list(dataset) if description is False else\
        {key:dataset_description[key] for key in dataset if key in dataset_description}

dataset_description = {
    "orientation": "A series of orientation values given as azimuth from North. \
The orientation values are contained in the \"strike_deg\" column. They \
are given in degrees, clockwise from North, ranging from 0 to 360 °. \
The values are categorized by the \"category\" column. \
A total of 300 values are contained in the dataset, grouped in \
3 categories:\n\
 - Cat1:  50 values, random around  50 °, ranging [35,65]\n\
 - Cat2: 150 values, random around 320 °, ranging [290,350]\n\
 - Rand: 100 values, random ranging [0,360]\n\
Values are rounded to unit integers."
    }

dataset = {
    "orientation": pd.DataFrame(
            {"strike_deg":[106, 108, 111,  95,  92, 110, 100,  97, 110, 106, 114,  89,  92,
       108,  90, 103, 110,  97, 107, 106, 104, 103,  86, 108, 107, 106,
        96, 112, 114,  88,  95,  93, 100,  98, 114,  88, 110, 103,  89,
       101,  95, 111, 108, 110, 109,  90,  98,  93, 115, 108, 334, 340,
       322, 329, 328, 336, 312, 339, 332, 312, 310, 345, 334, 325, 300,
       330, 325, 326, 303, 349, 333, 313, 339, 342, 322, 325, 346, 347,
       347, 319, 339, 307, 297, 349, 327, 319, 320, 309, 308, 305, 323,
       291, 306, 347, 297, 313, 333, 293, 305, 346, 350, 299, 340, 295,
       342, 327, 329, 295, 346, 311, 345, 328, 336, 346, 336, 318, 308,
       336, 346, 306, 301, 320, 326, 303, 302, 291, 332, 305, 325, 294,
       311, 316, 312, 321, 321, 343, 343, 300, 312, 316, 318, 304, 312,
       348, 318, 332, 309, 306, 291, 335, 318, 333, 314, 327, 342, 334,
       339, 315, 327, 300, 296, 336, 311, 300, 329, 321, 327, 304, 339,
       335, 318, 346, 318, 314, 302, 297, 306, 299, 320, 300, 346, 309,
       297, 315, 303, 346, 332, 344, 303, 340, 298, 338, 327, 304, 296,
       320, 350, 329, 300, 349, 170, 157, 132, 137,   1, 328, 224, 145,
       172,  53, 296, 175, 127, 250, 358, 233, 212, 150, 119, 142, 304,
       106, 139,  11, 163, 326, 282, 158, 332, 261,  40, 165, 242, 278,
       346, 167,  98, 324, 262, 129, 273,  90,  42, 155,  27, 241, 257,
       207, 314,  83, 250, 232, 310, 318,  50,  94, 297, 314,  96, 278,
       117, 334, 108, 238,  45,  44, 243, 171,  44, 147, 185, 192, 344,
       275, 109, 338, 126, 279, 225, 342, 115, 289, 147, 131, 180,  12,
       326, 293,   3, 291, 122,   2, 254, 286,  74,  16,  69, 116, 196, 47],
             "category":['Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1',
       'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1',
       'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1',
       'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1',
       'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1',
       'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1', 'Cat1',
       'Cat1', 'Cat1', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2', 'Cat2',
       'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand',
       'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand',
       'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand',
       'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand',
       'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand',
       'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand',
       'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand',
       'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand',
       'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand',
       'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand',
       'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand',
       'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand', 'Rand',
       'Rand', 'Rand', 'Rand', 'Rand']}
        )
}

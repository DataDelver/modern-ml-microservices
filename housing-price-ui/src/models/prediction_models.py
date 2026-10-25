from typing import Literal, Optional
from pydantic import BaseModel, Field


class PricePredictionRequest(BaseModel):
    """Request model for predicting a single housing price."""

    id: int = Field(ge=1, serialization_alias='Id')

    ms_sub_class: int = Field(ge=20, le=190, serialization_alias='MSSubClass')

    ms_zoning: Literal['A', 'C', 'FV', 'I', 'RH', 'RL', 'RP', 'RM'] = Field(serialization_alias='MSZoning')

    lot_frontage: Optional[float] = Field(default=None, ge=0, serialization_alias='LotFrontage')

    lot_area: int = Field(ge=0, serialization_alias='LotArea')

    street: Literal['Grvl', 'Pave'] = Field(serialization_alias='Street')

    lot_shape: Literal['Reg', 'IR1', 'IR2', 'IR3'] = Field(serialization_alias='LotShape')

    land_contour: Literal['Lvl', 'Bnk', 'HLS', 'Low'] = Field(serialization_alias='LandContour')

    utilities: Literal['AllPub', 'NoSewr', 'NoSeWa', 'ELO'] = Field(serialization_alias='Utilities')

    lot_config: Literal['Inside', 'Corner', 'CulDSac', 'FR2', 'FR3'] = Field(serialization_alias='LotConfig')

    land_slope: Literal['Gtl', 'Mod', 'Sev'] = Field(serialization_alias='LandSlope')

    neighborhood: Literal[
        'Blmngtn',
        'Blueste',
        'BrDale',
        'BrkSide',
        'ClearCr',
        'CollgCr',
        'Crawfor',
        'Edwards',
        'Gilbert',
        'IDOTRR',
        'MeadowV',
        'Mitchel',
        'NAmes',
        'NoRidge',
        'NPkVill',
        'NridgHt',
        'NWAmes',
        'OldTown',
        'SWISU',
        'Sawyer',
        'SawyerW',
        'Somerst',
        'StoneBr',
        'Timber',
        'Veend',
        'Veenker',
        'Whitstr',
    ] = Field(serialization_alias='Neighborhood')

    condition_1: Literal['Artery', 'Feedr', 'Norm', 'RRNn', 'RRAn', 'PosN', 'PosA', 'RRAe', 'RRNe'] = Field(
        serialization_alias='Condition1'
    )

    condition_2: Literal['Artery', 'Feedr', 'Norm', 'RRNn', 'RRAn', 'PosN', 'PosA', 'RRAe', 'RRNe', 'NA'] = Field(
        serialization_alias='Condition2'
    )

    bldg_type: Literal['1Fam', '2fmCon', 'Duplex', 'TwnhsE', 'Twnhs'] = Field(serialization_alias='BldgType')

    house_style: Literal['1Story', '1.5Fin', '1.5Unf', '2Story', '2.5Fin', '2.5Unf', 'SFoyer', 'SLvl'] = Field(
        serialization_alias='HouseStyle'
    )

    overall_qual: int = Field(ge=1, le=10, serialization_alias='OverallQual')

    overall_cond: int = Field(ge=1, le=10, serialization_alias='OverallCond')

    year_built: int = Field(ge=1872, serialization_alias='YearBuilt')

    year_remod_add: int = Field(ge=1872, serialization_alias='YearRemodAdd')

    roof_style: Literal['Flat', 'Gable', 'Gambrel', 'Hip', 'Mansard', 'Shed'] = Field(serialization_alias='RoofStyle')

    roof_matl: Literal['ClyTile', 'CompShg', 'Membran', 'Metal', 'Roll', 'Tar&Grv', 'WdShake', 'WdShngl'] = Field(
        serialization_alias='RoofMatl'
    )

    exterior_1st: Literal[
        'AsbShng',
        'AsphShn',
        'BrkComm',
        'BrkFace',
        'CemntBd',
        'HdBoard',
        'ImStucc',
        'MetalSd',
        'Plywood',
        'Stone',
        'Stucco',
        'VinylSd',
        'Wd Sdng',
        'WdShing',
    ] = Field(serialization_alias='Exterior1st')

    exterior_2nd: Literal[
        'AsbShng',
        'AsphShn',
        'BrkComm',
        'BrkFace',
        'CemntBd',
        'HdBoard',
        'ImStucc',
        'MetalSd',
        'Plywood',
        'Stone',
        'Stucco',
        'VinylSd',
        'Wd Sdng',
        'WdShing',
    ] = Field(serialization_alias='Exterior2nd')

    mas_vnr_area: Optional[float] = Field(default=None, ge=0, serialization_alias='MasVnrArea')

    exter_qual: Literal['Ex', 'Gd', 'TA', 'Fa', 'Po'] = Field(serialization_alias='ExterQual')

    exter_cond: Literal['Ex', 'Gd', 'TA', 'Fa', 'Po'] = Field(serialization_alias='ExterCond')

    foundation: Literal['BrkTil', 'CBlock', 'PConc', 'Slab', 'Stone', 'Wood'] = Field(serialization_alias='Foundation')

    bsmt_qual: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']] = Field(
        default=None, serialization_alias='BsmtQual'
    )

    bsmt_cond: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']] = Field(
        default=None, serialization_alias='BsmtCond'
    )

    bsmt_exposure: Optional[Literal['Gd', 'Av', 'Mn', 'No', 'NA']] = Field(
        default=None, serialization_alias='BsmtExposure'
    )

    bsmt_fin_type_1: Optional[Literal['GLQ', 'ALQ', 'BLQ', 'Rec', 'LwQ', 'Unf', 'NA']] = Field(
        default=None, serialization_alias='BsmtFinType1'
    )

    bsmt_fin_sf_1: int = Field(ge=0, serialization_alias='BsmtFinSF1')

    bsmt_fin_type_2: Optional[Literal['GLQ', 'ALQ', 'BLQ', 'Rec', 'LwQ', 'Unf', 'NA']] = Field(
        default=None, serialization_alias='BsmtFinType2'
    )

    bsmt_fin_sf_2: int = Field(ge=0, serialization_alias='BsmtFinSF2')

    bsmt_unf_sf: int = Field(ge=0, serialization_alias='BsmtUnfSF')

    total_bsmt_sf: int = Field(ge=0, serialization_alias='TotalBsmtSF')

    heating: Literal['Floor', 'GasA', 'GasW', 'Grav', 'OthW', 'Wall'] = Field(serialization_alias='Heating')

    heating_qc: Literal['Ex', 'Gd', 'TA', 'Fa', 'Po'] = Field(serialization_alias='HeatingQC')

    central_air: Literal['N', 'Y'] = Field(serialization_alias='CentralAir')

    electrical: Optional[Literal['SBrkr', 'FuseA', 'FuseF', 'FuseP', 'Mix']] = Field(
        default=None, serialization_alias='Electrical'
    )

    first_flr_sf: int = Field(ge=0, serialization_alias='1stFlrSF')

    second_flr_sf: int = Field(ge=0, serialization_alias='2ndFlrSF')

    low_qual_fin_sf: int = Field(ge=0, serialization_alias='LowQualFinSF')

    gr_liv_area: int = Field(ge=0, serialization_alias='GrLivArea')

    bsmt_full_bath: int = Field(ge=0, serialization_alias='BsmtFullBath')

    bsmt_half_bath: int = Field(ge=0, serialization_alias='BsmtHalfBath')

    full_bath: int = Field(ge=0, serialization_alias='FullBath')

    half_bath: int = Field(ge=0, serialization_alias='HalfBath')

    bedroom_abv_gr: int = Field(ge=0, serialization_alias='BedroomAbvGr')

    kitchen_abv_gr: int = Field(ge=0, serialization_alias='KitchenAbvGr')

    kitchen_qual: Literal['Ex', 'Gd', 'TA', 'Fa', 'Po'] = Field(serialization_alias='KitchenQual')

    tot_rms_abv_grd: int = Field(ge=0, serialization_alias='TotRmsAbvGrd')

    functional: Literal['Typ', 'Min1', 'Min2', 'Mod', 'Maj1', 'Maj2', 'Sev', 'Sal'] = Field(
        serialization_alias='Functional'
    )

    fireplaces: int = Field(ge=0, serialization_alias='Fireplaces')

    garage_type: Optional[Literal['2Types', 'Attchd', 'Basment', 'BuiltIn', 'CarPort', 'Detchd', 'NA']] = Field(
        default=None, serialization_alias='GarageType'
    )

    garage_yr_blt: Optional[int] = Field(default=None, ge=1800, serialization_alias='GarageYrBlt')

    garage_finish: Optional[Literal['Fin', 'RFn', 'Unf', 'NA']] = Field(
        default=None, serialization_alias='GarageFinish'
    )

    garage_cars: int = Field(ge=0, serialization_alias='GarageCars')

    garage_area: int = Field(ge=0, serialization_alias='GarageArea')

    garage_qual: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']] = Field(
        default=None, serialization_alias='GarageQual'
    )

    garage_cond: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']] = Field(
        default=None, serialization_alias='GarageCond'
    )

    paved_drive: Literal['Y', 'P', 'N'] = Field(serialization_alias='PavedDrive')

    wood_deck_sf: int = Field(ge=0, serialization_alias='WoodDeckSF')

    open_porch_sf: int = Field(ge=0, serialization_alias='OpenPorchSF')

    enclosed_porch: int = Field(ge=0, serialization_alias='EnclosedPorch')

    three_ssn_porch: int = Field(ge=0, serialization_alias='3SsnPorch')

    screen_porch: int = Field(ge=0, serialization_alias='ScreenPorch')

    pool_area: int = Field(ge=0, serialization_alias='PoolArea')

    misc_val: int = Field(ge=0, serialization_alias='MiscVal')

    mo_sold: int = Field(ge=1, le=12, serialization_alias='MoSold')

    yr_sold: int = Field(ge=1800, serialization_alias='YrSold')

    sale_type: Literal['WD', 'CWD', 'VWD', 'New', 'COD', 'Con', 'ConLw', 'ConLI', 'ConLD', 'Oth'] = Field(
        serialization_alias='SaleType'
    )

    sale_condition: Literal['Normal', 'Abnorml', 'AdjLand', 'Alloca', 'Family', 'Partial'] = Field(
        serialization_alias='SaleCondition'
    )


class PricePredictionBatchRequest(BaseModel):
    """Batch request model for predicting multiple housing prices."""

    data: list[PricePredictionRequest]


class PricePredictionResponse(BaseModel):
    """Response model for a single housing price prediction."""

    model_config = {'populate_by_name': True}

    id: int = Field(ge=1)
    predicted_price: float = Field(gt=0, validation_alias='predictedPrice')


class PricePredictionBatchResponse(BaseModel):
    """Response model for batch housing price predictions."""

    predictions: list[PricePredictionResponse]

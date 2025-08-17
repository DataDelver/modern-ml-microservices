from shared.data_model_base import ViewBase
from typing import Literal, Optional
from pydantic import Field


class PricePredictionRequest(ViewBase):
    """View model for the request to predict housing prices."""

    id: int = Field(ge=1, serialization_alias='Id')
    """Unique identifier for the housing unit."""

    ms_sub_class: int = Field(ge=20, le=190, serialization_alias='MSSubClass')
    """Identifies the type of dwelling involved in the sale"""

    ms_zoning: Literal['A', 'C', 'FV', 'I', 'RH', 'RL', 'RP', 'RM'] = Field(serialization_alias='MSZoning')
    """Identifies the general zoning classification of the sale"""

    lot_frontage: Optional[float] = Field(default=None, ge=0, serialization_alias='LotFrontage')
    """Linear feet of street connected to the property"""

    lot_area: int = Field(ge=0, serialization_alias='LotArea')
    """Lot size in square feet"""

    street: Literal['Grvl', 'Pave'] = Field(serialization_alias='Street')
    """Type of road access to the property"""

    lot_shape: Literal['Reg', 'IR1', 'IR2', 'IR3'] = Field(serialization_alias='LotShape')
    """General shape of the property"""

    land_contour: Literal['Lvl', 'Bnk', 'HLS', 'Low'] = Field(serialization_alias='LandContour')
    """Flatness of the property"""

    utilities: Literal['AllPub', 'NoSewr', 'NoSeWa', 'ELO'] = Field(serialization_alias='Utilities')
    """Type of utilities available"""

    lot_config: Literal['Inside', 'Corner', 'CulDSac', 'FR2', 'FR3'] = Field(serialization_alias='LotConfig')
    """Lot configuration"""

    land_slope: Literal['Gtl', 'Mod', 'Sev'] = Field(serialization_alias='LandSlope')
    """Slope of the property"""

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
        'Whitstr',
        'ClearCr',
        'CollgCr',
    ] = Field(serialization_alias='Neighborhood')
    """Physical locations within Ames city limits"""

    condition_1: Literal['Artery', 'Feedr', 'Norm', 'RRNn', 'RRAn', 'PosN', 'PosA', 'RRAe', 'RRNe'] = Field(
        serialization_alias='Condition1'
    )
    """Proximity to various conditions"""

    condition_2: Literal['Artery', 'Feedr', 'Norm', 'RRNn', 'RRAn', 'PosN', 'PosA', 'RRAe', 'RRNe', 'NA'] = Field(
        serialization_alias='Condition2'
    )
    """Proximity to various conditions"""

    bldg_type: Literal['1Fam', '2fmCon', 'Duplex', 'TwnhsE', 'Twnhs'] = Field(serialization_alias='BldgType')
    """Type of dwelling involved in the sale"""

    house_style: Literal['1Story', '1.5Fin', '1.5Unf', '2Story', '2.5Fin', '2.5Unf', 'SFoyer', 'SLvl'] = Field(
        serialization_alias='HouseStyle'
    )
    """Style of dwelling involved in the sale"""

    overall_qual: int = Field(ge=1, le=10, serialization_alias='OverallQual')
    """Rates the overall material and finish of the house"""

    overall_cond: int = Field(ge=1, le=10, serialization_alias='OverallCond')
    """Rates the overall condition of the house"""

    year_built: int = Field(ge=1872, serialization_alias='YearBuilt')
    """Original construction date of the house"""

    year_remod_add: int = Field(ge=1872, serialization_alias='YearRemodAdd')
    """Remodel date of the house"""

    roof_style: Literal['Flat', 'Gable', 'Gambrel', 'Hip', 'Mansard', 'Shed'] = Field(serialization_alias='RoofStyle')
    """Type of roof"""

    roof_matl: Literal['ClyTile', 'CompShg', 'Membran', 'Metal', 'Roll', 'Tar&Grv', 'WdShake', 'WdShngl'] = Field(
        serialization_alias='RoofMatl'
    )
    """Roof material"""

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
    """Exterior covering on house"""

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
    """Exterior covering on house (if more than one material)"""

    mas_vnr_area: Optional[float] = Field(default=None, ge=0, serialization_alias='MasVnrArea')
    """Masonry veneer area in square feet"""

    exter_qual: Literal['Ex', 'Gd', 'TA', 'Fa', 'Po'] = Field(serialization_alias='ExterQual')
    """Evaluates the quality of the material on the exterior"""

    exter_cond: Literal['Ex', 'Gd', 'TA', 'Fa', 'Po'] = Field(serialization_alias='ExterCond')
    """Evaluates the present condition of the material on the exterior"""

    foundation: Literal['BrkTil', 'CBlock', 'PConc', 'Slab', 'Stone', 'Wood'] = Field(serialization_alias='Foundation')
    """Type of foundation"""

    bsmt_qual: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']] = Field(
        default=None, serialization_alias='BsmtQual'
    )
    """Evaluates the height of the basement"""

    bsmt_cond: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']] = Field(
        default=None, serialization_alias='BsmtCond'
    )
    """Evaluates the general condition of the basement"""

    bsmt_exposure: Optional[Literal['Gd', 'Av', 'Mn', 'No', 'NA']] = Field(
        default=None, serialization_alias='BsmtExposure'
    )
    """Refers to walkout or garden level walls"""

    bsmt_fin_type_1: Optional[Literal['GLQ', 'ALQ', 'BLQ', 'Rec', 'LwQ', 'Unf', 'NA']] = Field(
        default=None, serialization_alias='BsmtFinType1'
    )
    """Rating of basement finished area"""

    bsmt_fin_sf_1: int = Field(ge=0, serialization_alias='BsmtFinSF1')
    """Type 1 finished square feet"""

    bsmt_fin_type_2: Optional[Literal['GLQ', 'ALQ', 'BLQ', 'Rec', 'LwQ', 'Unf', 'NA']] = Field(
        default=None, serialization_alias='BsmtFinType2'
    )
    """Rating of basement finished area (if multiple types)"""

    bsmt_fin_sf_2: int = Field(ge=0, serialization_alias='BsmtFinSF2')
    """Type 2 finished square feet"""

    bsmt_unf_sf: int = Field(ge=0, serialization_alias='BsmtUnfSF')
    """Unfinished square feet of basement area"""

    total_bsmt_sf: int = Field(ge=0, serialization_alias='TotalBsmtSF')
    """Total square feet of basement area"""

    heating: Literal['Floor', 'GasA', 'GasW', 'Grav', 'OthW', 'Wall'] = Field(serialization_alias='Heating')
    """Type of heating"""

    heating_qc: Literal['Ex', 'Gd', 'TA', 'Fa', 'Po'] = Field(serialization_alias='HeatingQC')
    """Heating quality and condition"""

    central_air: Literal['N', 'Y'] = Field(serialization_alias='CentralAir')
    """Central air conditioning"""

    electrical: Optional[Literal['SBrkr', 'FuseA', 'FuseF', 'FuseP', 'Mix']] = Field(
        default=None, serialization_alias='Electrical'
    )
    """Electrical system"""

    first_flr_sf: int = Field(ge=0, serialization_alias='1stFlrSF')
    """First floor square feet"""

    second_flr_sf: int = Field(ge=0, serialization_alias='2ndFlrSF')
    """Second floor square feet"""

    low_qual_fin_sf: int = Field(ge=0, serialization_alias='LowQualFinSF')
    """Low quality finished square feet (all floors)"""

    gr_liv_area: int = Field(ge=0, serialization_alias='GrLivArea')
    """Above grade (ground) living area square feet"""

    bsmt_full_bath: int = Field(ge=0, serialization_alias='BsmtFullBath')
    """Basement full bathrooms"""

    bsmt_half_bath: int = Field(ge=0, serialization_alias='BsmtHalfBath')
    """Basement half bathrooms"""

    full_bath: int = Field(ge=0, serialization_alias='FullBath')
    """Full bathrooms above grade"""

    half_bath: int = Field(ge=0, serialization_alias='HalfBath')
    """Half baths above grade"""

    bedroom_abv_gr: int = Field(ge=0, serialization_alias='BedroomAbvGr')
    """Bedrooms above grade (does NOT include basement bedrooms)"""

    kitchen_abv_gr: int = Field(ge=0, serialization_alias='KitchenAbvGr')
    """Kitchens above grade"""

    kitchen_qual: Literal['Ex', 'Gd', 'TA', 'Fa', 'Po'] = Field(serialization_alias='KitchenQual')
    """Kitchen quality"""

    tot_rms_abv_grd: int = Field(ge=0, serialization_alias='TotRmsAbvGrd')
    """Total rooms above grade (does not include bathrooms)"""

    functional: Literal['Typ', 'Min1', 'Min2', 'Mod', 'Maj1', 'Maj2', 'Sev', 'Sal'] = Field(
        serialization_alias='Functional'
    )
    """Home functionality (Assume typical unless deductions are warranted)"""

    fireplaces: int = Field(ge=0, serialization_alias='Fireplaces')
    """Number of fireplaces"""

    garage_type: Optional[Literal['2Types', 'Attchd', 'Basment', 'BuiltIn', 'CarPort', 'Detchd', 'NA']] = Field(
        default=None, serialization_alias='GarageType'
    )
    """Garage location"""

    garage_yr_blt: Optional[int] = Field(default=None, ge=1800, serialization_alias='GarageYrBlt')
    """Year garage was built"""

    garage_finish: Optional[Literal['Fin', 'RFn', 'Unf', 'NA']] = Field(
        default=None, serialization_alias='GarageFinish'
    )
    """Interior finish of the garage"""

    garage_cars: int = Field(ge=0, serialization_alias='GarageCars')
    """Size of garage in car capacity"""

    garage_area: int = Field(ge=0, serialization_alias='GarageArea')
    """Size of garage in square feet"""

    garage_qual: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']] = Field(
        default=None, serialization_alias='GarageQual'
    )
    """Garage quality"""

    garage_cond: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']] = Field(
        default=None, serialization_alias='GarageCond'
    )
    """Garage condition"""

    paved_drive: Literal['Y', 'P', 'N'] = Field(serialization_alias='PavedDrive')
    """Paved driveway"""

    wood_deck_sf: int = Field(ge=0, serialization_alias='WoodDeckSF')
    """Wood deck area in square feet"""

    open_porch_sf: int = Field(ge=0, serialization_alias='OpenPorchSF')
    """Open porch area in square feet"""

    enclosed_porch: int = Field(ge=0, serialization_alias='EnclosedPorch')
    """Enclosed porch area in square feet"""

    three_ssn_porch: int = Field(ge=0, serialization_alias='3SsnPorch')
    """Three season porch area in square feet"""

    screen_porch: int = Field(ge=0, serialization_alias='ScreenPorch')
    """Screen porch area in square feet"""

    pool_area: int = Field(ge=0, serialization_alias='PoolArea')
    """Pool area in square feet"""

    misc_val: int = Field(ge=0, serialization_alias='MiscVal')
    """$Value of miscellaneous feature"""

    mo_sold: int = Field(ge=1, le=12, serialization_alias='MoSold')
    """Month Sold (MM)"""

    yr_sold: int = Field(ge=1800, serialization_alias='YrSold')
    """Year Sold (YYYY)"""

    sale_type: Literal['WD', 'CWD', 'VWD', 'New', 'COD', 'Con', 'ConLw', 'ConLI', 'ConLD', 'Oth'] = Field(
        serialization_alias='SaleType'
    )
    """Type of sale"""

    sale_condition: Literal['Normal', 'Abnorml', 'AdjLand', 'Alloca', 'Family', 'Partial'] = Field(
        serialization_alias='SaleCondition'
    )
    """Condition of sale"""


class PricePredictionBatchRequest(ViewBase):
    """View model for a batch request to predict housing prices."""

    data: list[PricePredictionRequest]
    """List of housing data dictionaries to be used for predictions."""

from shared.data_model_base import ViewBase
from typing import Literal
from pydantic import Field
from typing import Optional


class PricePredictionRequest(ViewBase):
    """View model for the request to predict housing prices."""

    id: int = Field(ge=1, alias='Id')
    """Unique identifier for the housing unit."""

    ms_sub_class: Optional[int] = Field(default=None, ge=20, le=190, alias='MSSubClass')
    """Identifies the type of dwelling involved in the sale"""

    ms_zoning: Optional[Literal['A', 'C', 'FV', 'I', 'RH', 'RL', 'RP', 'RM']] = Field(default=None, alias='MSZoning')
    """Identifies the general zoning classification of the sale"""

    lot_frontage: Optional[float] = Field(default=None, ge=0, alias='LotFrontage')
    """Linear feet of street connected to the property"""

    lot_area: Optional[int] = Field(default=None, ge=0, alias='LotArea')
    """Lot size in square feet"""

    street: Optional[Literal['Grvl', 'Pave']] = Field(default=None, alias='Street')
    """Type of road access to the property"""

    alley: Optional[Literal['Grvl', 'Pave', 'NA']] = Field(default=None, alias='Alley')
    """Type of alley access to the property"""

    lot_shape: Optional[Literal['Reg', 'IR1', 'IR2', 'IR3']] = Field(default=None, alias='LotShape')
    """General shape of the property"""

    land_contour: Optional[Literal['Lvl', 'Bnk', 'HLS', 'Low']] = Field(default=None, alias='LandContour')
    """Flatness of the property"""

    utilities: Optional[Literal['AllPub', 'NoSewr', 'NoSeWa', 'ELO']] = Field(default=None, alias='Utilities')
    """Type of utilities available"""

    lot_config: Optional[Literal['Inside', 'Corner', 'CulDSac', 'FR2', 'FR3']] = Field(default=None, alias='LotConfig')
    """Lot configuration"""

    land_slope: Optional[Literal['Gtl', 'Mod', 'Sev']] = Field(default=None, alias='LandSlope')
    """Slope of the property"""

    neighborhood: Optional[
        Literal[
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
        ]
    ] = Field(default=None, alias='Neighborhood')
    """Physical locations within Ames city limits"""

    condition_1: Optional[Literal['Artery', 'Feedr', 'Norm', 'RRNn', 'RRAn', 'PosN', 'PosA', 'RRAe', 'RRNe']] = Field(
        default=None, alias='Condition1'
    )
    """Proximity to various conditions"""

    condition_2: Optional[Literal['Artery', 'Feedr', 'Norm', 'RRNn', 'RRAn', 'PosN', 'PosA', 'RRAe', 'RRNe', 'NA']] = (
        Field(default=None, alias='Condition2')
    )
    """Proximity to various conditions"""

    bldg_type: Optional[Literal['1Fam', '2fmCon', 'Duplex', 'TwnhsE', 'Twnhs']] = Field(default=None, alias='BldgType')
    """Type of dwelling involved in the sale"""

    house_style: Optional[Literal['1Story', '1.5Fin', '1.5Unf', '2Story', '2.5Fin', '2.5Unf', 'SFoyer', 'SLvl']] = (
        Field(default=None, alias='HouseStyle')
    )
    """Style of dwelling involved in the sale"""

    overall_qual: Optional[int] = Field(default=None, ge=1, le=10, alias='OverallQual')
    """Rates the overall material and finish of the house"""

    overall_cond: Optional[int] = Field(default=None, ge=1, le=10, alias='OverallCond')
    """Rates the overall condition of the house"""

    year_built: Optional[int] = Field(default=None, ge=1872, alias='YearBuilt')
    """Original construction date of the house"""

    year_remod_add: Optional[int] = Field(default=None, ge=1872, alias='YearRemodAdd')
    """Remodel date of the house"""

    roof_style: Optional[Literal['Flat', 'Gable', 'Gambrel', 'Hip', 'Mansard', 'Shed']] = Field(
        default=None, alias='RoofStyle'
    )
    """Type of roof"""

    roof_matl: Optional[Literal['ClyTile', 'CompShg', 'Membran', 'Metal', 'Roll', 'Tar&Grv', 'WdShake', 'WdShngl']] = (
        Field(default=None, alias='RoofMatl')
    )
    """Roof material"""

    exterior_1st: Optional[
        Literal[
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
        ]
    ] = Field(default=None, alias='Exterior1st')
    """Exterior covering on house"""

    exterior_2nd: Optional[
        Literal[
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
        ]
    ] = Field(default=None, alias='Exterior2nd')
    """Exterior covering on house (if more than one material)"""

    mas_vnr_type: Optional[Literal['BrkCmn', 'BrkFace', 'CBlock', 'None', 'Stone']] = Field(
        default=None, alias='MasVnrType'
    )
    """Masonry veneer type"""

    mas_vnr_area: Optional[float] = Field(default=None, ge=0, alias='MasVnrArea')
    """Masonry veneer area in square feet"""

    exter_qual: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po']] = Field(default=None, alias='ExterQual')
    """Evaluates the quality of the material on the exterior"""

    exter_cond: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po']] = Field(default=None, alias='ExterCond')
    """Evaluates the present condition of the material on the exterior"""

    foundation: Optional[Literal['BrkTil', 'CBlock', 'PConc', 'Slab', 'Stone', 'Wood']] = Field(
        default=None, alias='Foundation'
    )
    """Type of foundation"""

    bsmt_qual: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']] = Field(default=None, alias='BsmtQual')
    """Evaluates the height of the basement"""

    bsmt_cond: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']] = Field(default=None, alias='BsmtCond')
    """Evaluates the general condition of the basement"""

    bsmt_exposure: Optional[Literal['Gd', 'Av', 'Mn', 'No', 'NA']] = Field(default=None, alias='BsmtExposure')
    """Refers to walkout or garden level walls"""

    bsmt_fin_type_1: Optional[Literal['GLQ', 'ALQ', 'BLQ', 'Rec', 'LwQ', 'Unf', 'NA']] = Field(
        default=None, alias='BsmtFinType1'
    )
    """Rating of basement finished area"""

    bsmt_fin_sf_1: Optional[float] = Field(default=None, ge=0, alias='BsmtFinSF1')
    """Type 1 finished square feet"""

    bsmt_fin_type_2: Optional[Literal['GLQ', 'ALQ', 'BLQ', 'Rec', 'LwQ', 'Unf', 'NA']] = Field(
        default=None, alias='BsmtFinType2'
    )
    """Rating of basement finished area (if multiple types)"""

    bsmt_fin_sf_2: Optional[float] = Field(default=None, ge=0, alias='BsmtFinSF2')
    """Type 2 finished square feet"""

    bsmt_unf_sf: Optional[float] = Field(default=None, ge=0, alias='BsmtUnfSF')
    """Unfinished square feet of basement area"""

    total_bsmt_sf: Optional[float] = Field(default=None, ge=0, alias='TotalBsmtSF')
    """Total square feet of basement area"""

    heating: Optional[Literal['Floor', 'GasA', 'GasW', 'Grav', 'OthW', 'Wall']] = Field(default=None, alias='Heating')
    """Type of heating"""

    heating_qc: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po']] = Field(default=None, alias='HeatingQC')
    """Heating quality and condition"""

    central_air: Optional[Literal['N', 'Y']] = Field(default=None, alias='CentralAir')
    """Central air conditioning"""

    electrical: Optional[Literal['SBrkr', 'FuseA', 'FuseF', 'FuseP', 'Mix']] = Field(default=None, alias='Electrical')
    """Electrical system"""

    first_flr_sf: Optional[int] = Field(default=None, ge=0, alias='1stFlrSF')
    """First floor square feet"""

    second_flr_sf: Optional[int] = Field(default=None, ge=0, alias='2ndFlrSF')
    """Second floor square feet"""

    low_qual_fin_sf: Optional[int] = Field(default=None, ge=0, alias='LowQualFinSF')
    """Low quality finished square feet (all floors)"""

    gr_liv_area: Optional[int] = Field(default=None, ge=0, alias='GrLivArea')
    """Above grade (ground) living area square feet"""

    bsmt_full_bath: Optional[int] = Field(default=None, ge=0, alias='BsmtFullBath')
    """Basement full bathrooms"""

    bsmt_half_bath: Optional[int] = Field(default=None, ge=0, alias='BsmtHalfBath')
    """Basement half bathrooms"""

    full_bath: Optional[int] = Field(default=None, ge=0, alias='FullBath')
    """Full bathrooms above grade"""

    half_bath: Optional[int] = Field(default=None, ge=0, alias='HalfBath')
    """Half baths above grade"""

    bedroom_abv_gr: Optional[int] = Field(default=None, ge=0, alias='BedroomAbvGr')
    """Bedrooms above grade (does NOT include basement bedrooms)"""

    kitchen_abv_gr: Optional[int] = Field(default=None, ge=0, alias='KitchenAbvGr')
    """Kitchens above grade"""

    kitchen_qual: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po']] = Field(default=None, alias='KitchenQual')
    """Kitchen quality"""

    tot_rms_abv_grd: Optional[int] = Field(default=None, ge=0, alias='TotRmsAbvGrd')
    """Total rooms above grade (does not include bathrooms)"""

    functional: Optional[Literal['Typ', 'Min1', 'Min2', 'Mod', 'Maj1', 'Maj2', 'Sev', 'Sal']] = Field(
        default=None, alias='Functional'
    )
    """Home functionality (Assume typical unless deductions are warranted)"""

    fireplaces: Optional[int] = Field(default=None, ge=0, alias='Fireplaces')
    """Number of fireplaces"""

    fireplace_qu: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']] = Field(default=None, alias='FireplaceQu')
    """Fireplace quality"""

    garage_type: Optional[Literal['2Types', 'Attchd', 'Basment', 'BuiltIn', 'CarPort', 'Detchd', 'NA']] = Field(
        default=None, alias='GarageType'
    )
    """Garage location"""

    garage_yr_blt: Optional[int] = Field(default=None, ge=1800, alias='GarageYrBlt')
    """Year garage was built"""

    garage_finish: Optional[Literal['Fin', 'RFn', 'Unf', 'NA']] = Field(default=None, alias='GarageFinish')
    """Interior finish of the garage"""

    garage_cars: Optional[int] = Field(default=None, ge=0, alias='GarageCars')
    """Size of garage in car capacity"""

    garage_area: Optional[int] = Field(default=None, ge=0, alias='GarageArea')
    """Size of garage in square feet"""

    garage_qual: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']] = Field(default=None, alias='GarageQual')
    """Garage quality"""

    garage_cond: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']] = Field(default=None, alias='GarageCond')
    """Garage condition"""

    paved_drive: Optional[Literal['Y', 'P', 'N']] = Field(default=None, alias='PavedDrive')
    """Paved driveway"""

    wood_deck_sf: Optional[int] = Field(default=None, ge=0, alias='WoodDeckSF')
    """Wood deck area in square feet"""

    open_porch_sf: Optional[int] = Field(default=None, ge=0, alias='OpenPorchSF')
    """Open porch area in square feet"""

    enclosed_porch: Optional[int] = Field(default=None, ge=0, alias='EnclosedPorch')
    """Enclosed porch area in square feet"""

    three_ssn_porch: Optional[int] = Field(default=None, ge=0, alias='3SsnPorch')
    """Three season porch area in square feet"""

    screen_porch: Optional[int] = Field(default=None, ge=0, alias='ScreenPorch')
    """Screen porch area in square feet"""

    pool_area: Optional[int] = Field(default=None, ge=0, alias='PoolArea')
    """Pool area in square feet"""

    pool_qc: Optional[Literal['Ex', 'Gd', 'TA', 'Fa', 'NA']] = Field(default=None, alias='PoolQC')
    """Pool quality"""

    fence: Optional[Literal['GdPrv', 'MnPrv', 'GdWo', 'MnWw', 'NA']] = Field(default=None, alias='Fence')
    """Fence quality"""

    misc_feature: Optional[Literal['Elev', 'Gar2', 'Othr', 'Shed', 'TenC', 'NA']] = Field(
        default=None, alias='MiscFeature'
    )
    """Miscellaneous feature not covered in other categories"""

    misc_val: Optional[int] = Field(default=None, ge=0, alias='MiscVal')
    """$Value of miscellaneous feature"""

    mo_sold: Optional[int] = Field(default=None, ge=1, le=12, alias='MoSold')
    """Month Sold (MM)"""

    yr_sold: Optional[int] = Field(default=None, ge=1800, alias='YrSold')
    """Year Sold (YYYY)"""

    sale_type: Optional[Literal['WD', 'CWD', 'VWD', 'New', 'COD', 'Con', 'ConLw', 'ConLI', 'ConLD', 'Oth']] = Field(
        default=None, alias='SaleType'
    )
    """Type of sale"""

    sale_condition: Optional[Literal['Normal', 'Abnorml', 'AdjLand', 'Alloca', 'Family', 'Partial']] = Field(
        default=None, alias='SaleCondition'
    )
    """Condition of sale"""


class PricePredictionBatchRequest(ViewBase):
    """View model for a batch request to predict housing prices."""

    data: list[PricePredictionRequest]
    """List of housing data dictionaries to be used for predictions."""

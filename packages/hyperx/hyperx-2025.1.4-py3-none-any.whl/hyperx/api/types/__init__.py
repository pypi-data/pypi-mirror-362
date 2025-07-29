from __future__ import annotations
from ...library import _api, _types

from typing import TypeVar, Generic, overload
from enum import Enum, EnumMeta
from System.Collections.Generic import List, IEnumerable, Dictionary, HashSet
from System.Threading.Tasks import Task
from System import Guid, DateTime, Double, String, Boolean, Nullable

from abc import ABC, abstractmethod

T = TypeVar('T')


class DuplicatedValue:
	'''
	Allows for enums with duplicated backing values, because
	Python turns any entries with duplicate values into aliases
	for the first entry
	'''
	def __init__(self, value: int):
		self.value = value 


def GetEnumValue(enumValue: int | DuplicatedValue):
	'''
	Handles the conversion to int from any member in an enum,
	whether it is a DuplicatedValue or a raw int already
	'''
	return enumValue.value if isinstance(enumValue, DuplicatedValue) else enumValue


class OnAccess(EnumMeta):
	'''
	Runs a user-specified function whenever member is accessed.
	Based on: https://stackoverflow.com/a/62309159
	'''

	def __call__(cls, value, names=None, *, module=None, qualname=None, type=None, start=1):
		obj = super().__call__(value, names, module=module, qualname=qualname, type=type, start=start)
		if isinstance(obj, Enum) and obj._on_access:
			obj._on_access()
		return obj
	def __getattribute__(cls, name):
		obj = super().__getattribute__(name)
		if isinstance(obj, Enum) and obj._on_access:
			obj._on_access()
		return obj

	def __getitem__(cls, name):
		member = super().__getitem__(name)
		if member._on_access:
			member._on_access()
		return member
	

class DeprecatedEnum(Enum, metaclass=OnAccess):
	'''
	Based on: https://stackoverflow.com/a/62309159
	'''
	def __new__(cls, value, *args):
		member = object.__new__(cls)
		member._value_ = value
		member._args = args
		member._on_access = member.deprecate if args else None
		return member

	def deprecate(self):
		args = (self.name, ) + self._args
		import warnings
		warnings.warn("Member %r is deprecated; %s" % args, DeprecationWarning, 3)


class AnalysisId(Enum):
	UNKNOWN = 0
	PanelBucklingFlatSimpleBCSymmetricUniaxialorBiaxial = 1
	PanelBucklingFlatSimpleBCUniaxialorBiaxial = 2
	PanelBucklingFlatSimpleBCShear = 3
	PanelBucklingFlatSimpleBCSymmUniaxialorBiaxialwShearInteraction = 4
	PanelBucklingFlatSimpleBCUniaxialorBiaxialwShearInteraction = 5
	PanelBucklingFlatSimpleBCSymmUniaxialorBiaxialwTSFtransverseshearflexibility = 6
	PanelBucklingFlatSimpleBCUniaxialorBiaxialwTSF = 7
	PanelBucklingFlatSimpleBCShearwTSFTransverseShearFlexibility = 8
	PanelBucklingFlatSimpleBCUniaxialorBiaxialwTSFShearInteraction = 9
	PanelBucklingSandwichwTSF = 10
	PanelBucklingCurvedorFlatAllBC = 11
	PanelBucklingCurvedorFlatAllBCwTSFTransverseShearFlexibility = 12
	PanelBucklingFlatSimpleBCLColumnwTransverseShearFlexibility = 13
	PanelBucklingFlatSimpleBCTColumnonTranslationalSprings = 14
	StiffenerBucklingHatScissor = 15
	StiffenerBucklingFlexuralTorsionalArgyris = 16
	StiffenerBucklingFlexuralTorsionalLevy = 17
	PanelBucklingCurvedorFlatNASASP8007Method = 18
	PanelBucklingUserDefined1 = 23
	PanelBucklingUserDefined2 = 24
	BeamBucklingColumnPlane1I1 = 25
	BeamBucklingColumnPlane1wTSFI1 = 26
	BeamBucklingColumnPlane2I2 = 27
	BeamBucklingColumnPlaneMinImin = 28
	BeamBucklingLateral = 30
	BeamBucklingLateralTorsional = 31
	BeamBucklingCylindricalAxialandBendingRayleighRitz = 33
	BeamBucklingCylindricalAxialandBendingNASASP8007 = 34
	BeamBucklingUserDefined1 = 38
	BeamBucklingUserDefined2 = 39
	LocalBucklingLongitudinalDirection = 40
	LocalBucklingShearDirection = 42
	LocalBucklingInteraction = 43
	LocalBucklingInterrivet = 44
	LocalBucklingCripplingInteraction = 45
	LocalBucklingSpacingSpanSkinBiaxialwInteraction = 46
	LocalBucklingShearPermanentDeformation = 47
	CripplingIsotropicmethodNiuformedandextrudedsections = 50
	CripplingIsotropicmethodLTVformedandextrudedsections = 51
	CripplingCompositemethodMilHdbk173EincludingDij = 52
	CripplingBucklinginteractionJohnsonEuler = 53
	CripplingForcedDiagonalTension = 54
	CripplingForcedCompressionCripplingInteraction = 55
	CripplingUserDefined1 = 58
	CripplingUserDefined2 = 59
	StrainLimit = 60
	CurvatureLimit = 61
	CenterDeflectionLimit = 62
	StiffnessRequirementMembrane = 63
	StiffnessRequirementBending = 64
	FrequencyLimitPanelorBeam = 65
	FrequencyLimitObjectlocal = 66
	GeometryRule1StiffenerFlangeWidthtoFlangeThicknessRatioMin = 67
	GeometryRule2StiffenerFlangeWidthtoStiffenerHeightRatioMin = 68
	GeometryRule3StiffenerWebThicknesstoFlangeThicknessRatioMin = 69
	GeometryRule4StiffenerWebHeighttoWebThicknessRatioMax = 70
	GeometryRule5PanelHeightMax = 71
	GeometryRule40PanelWidthtoStiffenerSpacingMinofstiffeners = 72
	GeometryRule41StiffenertoSkinAreaRatioMinMax = 73
	GeometryRule42StiffenerEISlendernessRatioMin = 74
	ThermalProtectionSystemStructureTemperatureLimit = 75
	ThermalProtectionSystemMaterialSingleUseTemperatureLimit = 76
	ThermalProtectionSystemMaterialMultipleUseTemperatureLimit = 77
	ThermalProtectionSystemCryogenicLowerTemperatureLimit = 78
	WrinklingEqn1IsotropicorHoneycombCoreXYInteraction = 90
	WrinklingEqn2HoneycombCoreXYInteraction = 91
	WrinklingVinsonHoneycombXYInteraction = 92
	IntracellDimplingXYInteraction = 94
	SandwichFaceUserDefined1 = 99
	CrushingConcentratedLoad = 100
	CrushingFlexuralBendingLoad = 101
	CrushingJointSupportLoad = 102
	SandwichFlatwiseTension = 103
	SandwichFlatwiseTensionwInterlaminarShearInteraction = 104
	ShearCrimpingMinXYHexcel = 105
	ShearCrimpingMinPrincipalStressHexcel = 106
	ShearStrengthXLongitudinaldirectionHexcel = 107
	ShearStrengthYTransversedirectionHexcel = 108
	ShearStrengthInteractionQuadraticBasic = 109
	IsotropicStrengthLongitudinalDirection = 110
	IsotropicStrengthTransverseDirection = 111
	IsotropicStrengthShearDirection = 112
	IsotropicStrengthVonMisesHillInteractionYieldCriterion = 113
	IsotropicStrengthVonMisesInteractionYieldCriterion = 316
	IsotropicStrengthMaxShearCriterion = 114
	IsotropicStrengthMaxPrincipalStressCriterion = 115
	IsotropicStrengthNaca2661MaxShearStress = 116
	MicromechanicsMaxStress1stSubcell = 120
	MicromechanicsMaxStrain1stSubcell = 121
	MicromechanicsTsaiHill1stSubcell = 122
	MicromechanicsSIFT1stSubcell = 123
	MicromechanicsMaxStressAverageUnitCell = 124
	MicromechanicsMaxStrainAverageUnitCell = 125
	MicromechanicsTsaiHillAverageUnitCell = 126
	MicromechanicsSIFTAverageUnitCell = 127
	MicromechanicsMaxStressAllUnitCell = 128
	MicromechanicsMaxStrainAllUnitCell = 129
	MicromechanicsTsaiHillInteractionAllUnitCell = 130
	MicromechanicsSIFTAllUnitCell = 131
	CompositeStrengthMaxStrain1Direction = 135
	CompositeStrengthMaxStrain2Direction = 136
	CompositeStrengthMaxStrain12Direction = 137
	CompositeStrengthMaxStress1Direction = 138
	CompositeStrengthMaxStress2Direction = 139
	CompositeStrengthMaxStress12Direction = 140
	CompositeStrengthTsaiHillInteraction = 141
	CompositeStrengthTsaiWuInteraction = 142
	CompositeStrengthTsaiHahnInteraction = 143
	CompositeStrengthHoffmanInteraction = 144
	CompositeStrengthHashinMatrixCracking = 145
	CompositeStrengthHashinFiberFailure = 146
	CompositeStrengthLaRC03MatrixCracking = 147
	CompositeStrengthLaRC03FiberFailure = 148
	CompositeStrengthTsaiWuStrainPlyAllowables = 149
	CompositeStrengthTsaiWuStrainLaminateAllowables = 150
	CompositeStrengthOpenHoleTensionOHTMaxStrain1Direction = 151
	CompositeStrengthOpenHoleCompressionOHCMaxStrain1Direction = 152
	CompositeStrengthInterlaminarShearKick = 153
	CompositeStrengthPuck2dInterFiberFracture = 154
	CompositeStrengthPuck2dFiberFracture = 155
	CompositeStrengthPuck3dInterFiberFracture = 156
	CompositeStrengthPuck3dFiberFracture = 157
	CompositeStrengthUserDefined1 = 158
	CompositeStrengthUserDefined2 = 159
	JointBondedEdgeDelaminationOnset = 160
	JointBondedEdgeDelamination = 161
	JointBondedFracturePrincipalTransverse = 162
	JointBondedFractureMaxStressorStrain1direction = 163
	JointBondedDelaminationPeelDominated = 164
	JointBondedDelaminationPeelandTransverseShear1 = 165
	JointBondedDelaminationPeelandTransverseShear2 = 166
	JointBondedDelaminationTongPeelTransverseShearAxial1 = 167
	JointBondedDelaminationTongPeelTransverseShearAxial2 = 168
	JointBondedDelaminationTongPeelTransverseShearAxial3 = 169
	JointBondedDelaminationTongPeelTransverseShearAxial4 = 170
	JointBondedDelaminationTongPeelTransverseShearAxial5 = 171
	JointBondedDelaminationTongPeelTransverseShearAxial6 = 172
	JointBondedDelaminationPeelLongitudinalTransverseShear = 173
	JointBondedDelaminationPeelLongitudinalTransverseShearAxialandTransverse = 174
	JointBondedAdhesivePeelDominated = 175
	JointBondedAdhesiveVonMisesStrain = 176
	JointBondedAdhesiveMaximumPrincipalStress = 177
	JointBondedAdhesivePeelLongitudinalTransverseShear = 178
	JointBondedAdhesiveLongitudinalTransverseShearStress = 179
	JointBondedAdhesiveLongitudinalTransverseShearStrain = 180
	JointBondedDelaminationPropagationModeI = 181
	JointBondedDelaminationPropagationModeII = 182
	JointBondedDelaminationPropogationPowerLaw = 183
	JointBondedDelaminationPropogationBKcriterion = 184
	JointBondedLimitsOfApplicability = 185
	JointBoltedSingleHoleBJSFMloadedandfarfield = 190
	JointBoltedSingleHoleBJSFMBearingOnly = 191
	JointBoltedSingleHoleBJSFMBypassOnly = 192
	JointBoltedSingleHoleBearingIsotropicAllowable = 193
	JointBoltedUserDefined1 = 198
	JointBoltedUserDefined2 = 199
	ProgressiveFailureInverseABDTraceMethod = 201
	ProgressiveFailureAlternativeMethod = 202
	CompositeStrengthInterlaminarShear = 203
	CompositeStrengthFlatwiseTension = 204
	SandwichCoreUserDefined1 = 208
	SandwichCoreUserDefined2 = 209
	JointWebNormalCompressionorPulloff = 210
	JointWebShear = 211
	JointWebInteraction = 212
	GeometryRule71StiffenerAllLaminatesThicknesstoHoleDiameterRatioMinMaxRepairAngle = 216
	GeometryRule72StiffenerWebRepairThicknesstoHoleDiameterRatioMaxRepairAngle = 217
	GeometryRule73StiffenerSkinFlangeRepairThicknesstoHoleRatioMaxRepairAngle = 218
	GeometryRule74StiffenerHeightMinRepairAngle = 219
	GeometryRule75StiffenerFlangeWidthMinRepairAngle = 220
	CompositeStrengthLaminateCompressionPristine = 221
	CompositeStrengthLaminateCompressionAfterImpactCAI = 222
	CompositeStrengthLaminateCompressionOpenHoleOHC = 223
	CompositeStrengthLaminateCompressionFilledHoleFHC = 224
	CompositeStrengthLaminateCompressionBVID = 225
	CompositeStrengthLaminateTensionPristine = 226
	CompositeStrengthLaminateTensionAfterImpactTAI = 227
	CompositeStrengthLaminateTensionOpenHoleOHT = 228
	CompositeStrengthLaminateTensionFilledHoleFHT = 229
	CompositeStrengthLaminateShearPristine = 230
	CompositeStrengthLaminateShearAfterImpactSAI = 231
	IsotropicStrengthUltimateMaxPrincipalStressCriterion = 315
	MStensionOnlyYield = 330
	MStensionOnlyUltimate = 331
	MSjointSeparation = 333
	MSjointSlipUltimate = 334
	MSshearOnlyYield = 335
	MSshearOnlyUltimate = 336
	MScombinedTSBlinear = 337
	MScombinedTSBplastic = 338
	MSboltThreadShearUltimate = 348
	MSnutThreadShearUltimate = 339
	MSinsertInternalThreadShearUltimate = 340
	MSinsertExternalThreadShearUltimate = 341
	MSbearingYield = 343
	MSbearingUltimate = 344
	MSshearoutUltimate = 345
	MShoopTensionYield = 346
	MShoopTensionUltimate = 347
	MSbendingOnlyLinear = 349
	StaticJointStrengthYield = 350
	StaticJointStrengthUltimate = 351
	RivetShearStrength = 352
	PreventRivetShearFailureYield = 353
	PreventRivetShearFailureUltimate = 354
	PreventTensionLoadUltimate = 355
	PreventTensionLoadLimit = 356
	BearingBypassUltimate = 357
	MSbendingOnlyPlastic = 358
	MScombinedTS = 359
	MScombinedTBLinear = 360
	MScombinedTBPlastic = 361
	BearingOnlyComposite = 362

class LimitUltimate(Enum):
	'''
	Limit vs Ultimate loads.
	'''
	Limit = 0
	Ultimate = 1

class MarginCode(Enum):
	Value = 1
	NA = 2
	NAMaterial = 3
	LPB = 4
	GeomPass = 5
	DataReqdInfo = 6
	Bounds = 7
	PosLoad = 8
	NegLoad = 9
	Skipped = 10
	HighInfo = 11
	LowInfo = 12
	Unknown = 13
	LowFailure = 14
	DataReqdFail = 15
	GeomFail = 16
	Failed = 17
	NoData = 18

class UserConstantDataType(Enum):
	Invalid = 0
	FloatingPoint = 1
	OptionalFloatingPoint = 2
	Integer = 3
	OptionalInteger = 4
	Boolean = 5
	Selection = 6
	Text = 7
	Material = 8
	OptionalMaterial = 9

class TernaryStatusCode(Enum):
	Success = 1
	Warning = 2
	Error = 3

class FamilyConceptUID(Enum):
	Unknown = 0
	One_Stack_Unstiffened = 1
	Two_Stack_Unstiffened = 2
	Three_Stack_Unstiffened = 3
	Honeycomb_Sandwich = 4
	Foam_Sandwich = 5
	Bonded_Trusscore_Sandwich = 6
	Fastened_Trusscore_Sandwich = 7
	Bonded_Hat = 8
	Fastened_Hat = 9
	Bonded_Twosheet_Hat = 10
	Fastened_Twosheet_Hat = 11
	Bonded_I = 15
	Bonded_T = 16
	Bonded_Z = 17
	Bonded_J = 18
	Bonded_C = 19
	Bonded_Angle = 20
	Bonded_I_Continuous_Flange = 21
	Bonded_T_Continuous_Flange = 22
	Bonded_J_Continuous_Flange = 23
	Bonded_Sandwich_I = 24
	Integral_Sandwich_Blade = 25
	Fastened_I = 26
	Fastened_T = 27
	Fastened_Z = 28
	Fastened_Angle = 29
	Integral_Blade = 30
	Integral_Inverted_T = 31
	Integral_Inverted_AngleL = 32
	Reinforce_Core_Sandwich = 73
	C_Channel_Fastened = 220
	I_Frame_Fastened = 221
	Shear_Clip_Frame_Fastened = 222
	Cruciform = 223
	Grid0 = 62
	Grid90 = 63
	OrthoGrid = 64
	WaffleGrid = 65
	IsoGrid = 66
	AngleGrid = 67
	GeneralGrid = 68
	OrthoGrid_Sandwich = 69
	AngleGrid_Sandwich = 70
	Pultruded_Rod_Stiffened_Panel = 74
	I_Beam = 33
	T_Beam = 34
	C_Beam = 35
	L_Beam = 36
	Z_Beam = 37
	J_Beam = 38
	Cap_Beam = 39
	Web_Beam = 40
	Rectangular_Beam = 72
	Circular_Tube = 41
	Elliptical_Tube = 71
	Tapered_Circular_Tube = 75

class BeamPanelFamily(Enum):
	Unassigned = 0
	Unstiffened = 2
	Corrugated = 3
	Uniaxial = 4
	Grid = 5
	PRSEUS = 6
	OpenBeam = 7
	RectangularBeam = 8
	CircularBeam = 9

class FabricationRatio(Enum):
	Unknown = 0
	CompositeRSA = 1
	CompositeR1 = 2
	CompositeR2 = 3
	CompositeR5 = 6
	CompositeR6 = 7
	CompositeR7 = 8
	CompositeR8 = 9
	CompositeR9 = 10
	CompositeR10 = 11
	CompositeR11 = 12
	CompositeTheta = 13
	MetallicRSA = 21
	MetallicR1 = 22
	MetallicR2 = 23
	MetallicR3 = 24
	MetallicR4 = 25
	MetallicR5 = 26
	MetallicR6 = 27
	MetallicR10 = 31
	MetallicTheta = 33

class HeightSizingVariable(Enum):
	NotApplicable = 0
	TotalHeight = 1
	StiffenerHeight = 2
	WebHeight = 3

class MaterialMode(Enum):
	none = 0
	Metal = 1
	Composite = 2
	Any = 3

class ToolingSelectionType(Enum):
	'''
	Defines which selection a given tooling constraint is currently set to.
	'''
	Unknown = 0
	AnyValue = 1
	SpecifiedValue = 2
	SpecifiedLimitOrRange = 3

class VariableInputMode(Enum):
	UNKNOWN = 0
	Dimensions = 1
	Plies = 2
	Stock = 3

class DiscreteFieldDataType(Enum):
	'''
	Defines the type of data stored in a Discrete Field. Such as Vector, Scalar, String.
	'''
	Unknown = 0
	Vector = 1
	Scalar = 2
	String = 3

class DiscreteFieldPhysicalEntityType(Enum):
	'''
	Defines the type of physical entity that a Discrete Field applies to, such as zone, element, joint, etc.
	'''
	Unknown = 0
	Element = 1
	Zone = 2
	Joint = 3
	Grid = 4
	SectionCut = 5
	Solid = 6
	Point = 7

class DiscreteDefinitionType(Enum):
	none = 0
	LeftOpenSpanShell = 1
	RightOpenSpanShell = 2
	StiffenerFullBeam = 3
	WebShell = 4
	FootBeam = 5
	CapBeam = 6
	LeftFootSkinComboShell = 7
	RightFootSkinComboShell = 8
	LeftCapShell = 9
	RightCapShell = 10
	StiffenerPartialNoAttachedFlange = 11
	LeftWebOfHatShell = 12
	RightWebOfHatShell = 13
	CrownShell = 14
	ClosedSpanShell = 15
	LeftSkinOverFootShell = 16
	RightSkinOverFootShell = 17
	HatCombinedFootBeam = 18
	HatCombinedWebShell = 19
	CrownBeam = 20
	LeftFootShell = 21
	RightFootShell = 22
	WebFootShell = 23
	StiffenerMidBeam = 24
	WebCapShell = 25
	WebCruciformLower = 26
	WebCruciformUpper = 27

class DoePlotMode(Enum):
	RunSet = 0
	Structure = 1
	Set = 2

class DoePointType(Enum):
	none = 0
	All = 1
	Approach2 = 2
	Approach3 = 3

class FamilyCategory(Enum):
	Unknown = 0
	Panel = 1
	Beam = 2
	Joint = 3
	Unspecified = 4

class FeaSolutionType(Enum):
	Static = 0
	Buckling = 1
	Frequency = 2

class DiscreteTechnique(Enum):
	'''
	FEM Modeling technique for a Zone
	'''
	none = 0
	Two = 2
	Three = 3
	Four = 4
	Five = 5

class FemType(Enum):
	none = 0
	Unknown = 1
	GRID = 2
	CBAR = 3
	CROD = 4
	CBEAM = 5
	CBUSH = 6
	CELAS2 = 7
	CELAS3 = 8
	CQUAD4 = 9
	CQUAD8 = 10
	CQUADR = 11
	CTRIA3 = 12
	CSHEAR = 13
	CSHELL = 14
	CHEXA = 15
	CPENTA = 16
	LOAD = 18
	MAT1 = 19
	MAT2 = 20
	MAT3 = 21
	MAT5 = 22
	MAT8 = 23
	MAT9 = 24
	MAT10 = 25
	MAT11 = 26
	PBARL = 27
	PBAR = 28
	PBEAM = 29
	PBEAML = 30
	PBUSH = 31
	PCOMP = 32
	PCOMPLS = 33
	PCOMPG = 34
	PROD = 35
	PSHELL = 36
	PSHEAR = 37
	PSOLID = 38
	FORCE = 39
	MOMENT = 40
	PLOAD2 = 41
	PLOAD4 = 42
	RBE2 = 43
	RBE3 = 44
	SPC = 45
	SPC1 = 46
	TEMP = 47
	TEMPD = 48
	TEMPP1 = 49
	TEMPRB = 50
	CORD1C = 51
	CORD1R = 52
	CORD1S = 53
	CORD2C = 54
	CORD2R = 55
	CORD2S = 56
	CORD3C = 57
	CORD3R = 58
	CORD3S = 59
	MATERIAL = 60
	NODE = 61
	B31 = 62
	B32 = 63
	STRI3 = 64
	S3 = 65
	S3R = 66
	STRI65 = 67
	S4 = 68
	S4R = 69
	S8R = 70
	C3D4 = 71
	C3D10 = 72
	C3D8 = 73
	C3D8I = 74
	C3D8R = 75
	C3D6 = 76
	C3D15 = 77
	C3D20 = 78
	C3D20R = 79
	CONN3D2 = 80
	ISOTROPIC = 81
	LAMINA = 82
	ENGINEERINGCONSTANTS = 83
	BEAM = 84
	BEAMSECTION = 85
	BEAMGENERALSECTION = 86
	CONNECTORSECTION = 87
	SHELLSECTION = 88
	SHELLGENERALSECTION = 89
	SOLIDSECTION = 90
	SOLIDGENERALSECTION = 91
	ELSET = 92
	COORD3D = 93
	DISTRIBUTION = 94
	GRIDSET = 95
	DISTRIBUTIONTABLE = 96
	Rectangular = 97
	Cylindrical = 98
	Spherical = 99
	Ply = 100
	MPC = 101
	CTRIAR = 102
	CTRIA6 = 103

class ConstraintType(Enum):
	UNKNOWN = 0
	Displacement = 1
	Buckling = 2
	Moment = 3
	Frequency = 4

class DegreeOfFreedom(Enum):
	T1 = 0
	T2 = 1
	T3 = 2
	R1 = 3
	R2 = 4
	R3 = 5
	Tmag = 6
	Rmag = 7

class DisplacementShapeType(Enum):
	Unknown = 0
	Sphere = 1
	Cylinder = 2
	Plane = 3

class StiffnessCriteriaType(Enum):
	Displacement = 0
	Rotation = 1
	Buckling = 2
	Frequency = 3

class JointConceptId(Enum):
	Unassigned = 0
	Clevis = 2
	EdgeAllowable = 10
	BoltedSingleShear = 13
	BondedSingleLap = 14
	RivetedSingleShear = 15
	DoubleStrap = 16
	Doubler = 17
	SteppedLap = 18
	BoltedDoubleShear = 19
	BoltedTripleShear = 20
	BoltedQuadrupleShear = 21

class JointRangeId(Enum):
	Torque = 1
	FastenerSpacing = 2
	FastenerRows = 3
	LengthOverlap = 4
	TaperAngle = 5
	FinalThickness = 6
	PulloffNormalAllowable = 7
	CompressiveNormalAllowable = 8
	ShearAllowable = 9
	Adherend1Thickness = 10
	Adherend2Thickness = 11
	Sheet1Thickness = 12
	Sheet2Thickness = 13
	Sheet3Thickness = 20
	Sheet4Thickness = 21
	ThicknessAdhesive = 14
	ThicknessDoubler = 15
	ThicknessClevis = 16
	ThicknessStrap = 17
	LengthDoubler = 18
	NumberOfSteps = 19
	RivetSpacing = 22

class JointRangeMode(Enum):
	Torque = 1
	Length = 2
	FastenerRows = 3
	TaperAngle = 4
	Thickness = 5
	Allowable = 6
	NumberOfSteps = 7
	NxD = 8

class JointSelectionId(Enum):
	AdhesiveMaterial = 1
	UpperStrapMaterial = 2
	LowerStrapMaterial = 3
	ClevisMaterial = 4
	FastenerSelection = 5
	Adherend1Material = 6
	Adherend2Material = 7
	Sheet1Material = 8
	Sheet2Material = 9
	Sheet3Material = 13
	Sheet4Material = 14
	RivetMaterial = 10
	StrapMaterial = 11
	DoublerMaterial = 12

class BoundaryConditionType(Enum):
	Force = 1
	Displacement = 2
	Free = 3
	Fixed = 4

class DesignLoadFilteringOptions(Enum):
	DoNothing = 0
	UpdateDuringNextSizingOrAnalysis = 1
	ApplyDuringSizingOrAnalysis = 2

class DesignLoadOverrideMode(Enum):
	IncludedCases = 0
	LimitFactor = 1
	UltimateFactor = 2
	ThermalHelp = 3
	ThermalHurt = 4
	Temperature = 5

class ForceTransformType(Enum):
	HyperXConvention = 1
	SolverConvention = 2

class LoadCaseType(Enum):
	Static = 1
	Fatigue = 2

class LoadPropertyAverageElementType(Enum):
	TensionCompressionAverage = 0
	TrueAverage = 1

class LoadPropertyPeakElementScope(Enum):
	PeakDesignCase = 1
	AllDesignCases = 2

class LoadPropertyType(Enum):
	none = 0
	Average = 1
	Statistical = 2
	PeakLoad = 3
	NeighborAverage = 4
	ElementBased = 5
	UserFEA = 6
	UserBonded = 7
	UserBolted = 8
	UserGeneral = 9

class LoadSubCaseFactor(Enum):
	none = 0
	LimitOnly = 1
	UltimateOnly = 2
	LimitWithThermalHelp = 3
	LimitWithThermalHurt = 4
	UltimateWithThermalHelp = 5
	UltimateWithThermalHurt = 6
	Unfactored = 7

class TemperatureChoiceType(Enum):
	'''
	Load Case Setting selection for analysis and initial temperature.
	Analysis temperature can only be Value or Subcase.
	'''
	Analysis = 0
	Value = 1
	Subcase = 2

class AllowableMethodName(Enum):
	'''
	Method name for a laminate allowable.
	'''
	AML = 1
	Percent_0 = 2
	Percent_45 = 3
	BypassStress = 4
	Polynomial = 999

class AllowablePropertyName(Enum):
	'''
	Property name for a laminate allowable.
	'''
	Strain_Tension_Pristine = 1
	Strain_Compression_Pristine = 2
	Strain_Shear_Pristine = 3
	Strain_Tension_OHT = 4
	Strain_Compression_OHC = 5
	Stress_Bearing = 6
	Strain_Compression_CAI = 9
	Strain_Compression_FHC = 10
	Strain_Compression_BVID = 11
	Strain_Tension_TAI = 12
	Strain_Tension_FHT = 13
	Strain_Shear_SAI = 14
	Stress_PullThrough = 15
	Stress_Bearing_Bypass = 16
	Stress_Bypass = 17

class CorrectionCategory(Enum):
	'''
	Correction property category.
	'''
	ElasticStiffness = 1
	StressAllowables = 2
	StrainAllowables = 3
	LaminateStrainAllowables = 4
	BoltedJointParameters = 5
	BoltedJointStressAllowables = 6

class CorrectionEquation(DeprecatedEnum):
	'''
	Equation for a correction factor.
	'''
	Unknown = 0
	Constant = 1
	LinearPercentPly = DuplicatedValue(2)
	Linear_Percent_Ply = DuplicatedValue(2), "Use LinearPercentPly instead."
	QuadraticPercentPlyAndTemperature = DuplicatedValue(3)
	Quadratic_Percent_Ply_and_Temperature = DuplicatedValue(3), "Use QuadraticPercentPlyAndTemperature instead."
	CubicAML = DuplicatedValue(4)
	Cubic_AML = DuplicatedValue(4), "Use CubicAML instead."
	BiquadraticThickness = DuplicatedValue(5)
	Biquadratic_Thickness = DuplicatedValue(5), "Use BiquadraticThickness instead."
	QuadraticDiameterAndThickness = DuplicatedValue(6)
	Quadratic_Diameter_and_Thickness = DuplicatedValue(6), "Use QuadraticDiameterAndThickness instead."
	Table = 7

class CorrectionFactorCategory(Enum):
	Invalid = 0
	Equation = 1
	Tabular = 2

class CorrectionId(Enum):
	'''
	Correction ID for a correction factor. (Columns in HyperX)
	'''
	Invalid = 0
	Correction1 = 1
	Correction2 = 2
	Correction3 = 8
	Correction4 = 9
	Correction5 = 7
	Correction6 = 4
	Correction7 = 3
	Correction8 = 5
	Correction9 = 6

class CorrectionIndependentDefinition(DeprecatedEnum):
	'''
	Defines the type of Correction Factor.
	'''
	Unknown = 0
	Temperature = 1
	Percent0s = 2
	Percent45s = 3
	AML = 4
	IsCsk = 5
	Csk = 6
	EOverD = DuplicatedValue(7)
	e_over_D = DuplicatedValue(7), "Use EOverD instead."
	SOverD = DuplicatedValue(8)
	S_over_D = DuplicatedValue(8), "Use SOverD instead."
	Spacing = 9
	Diameter = 10
	Thickness = 11
	DOverT = DuplicatedValue(12)
	D_over_t = DuplicatedValue(12), "Use DOverT instead."
	HOverT = DuplicatedValue(13)
	H_over_t = DuplicatedValue(13), "Use HOverT instead."
	ShimThickness = 14
	PointIndex = 15
	CoreDensity = 16
	CoreThickness = 17
	Skin = 18

class CorrectionProperty(DeprecatedEnum):
	'''
	Property name for a correction factor. (Rows in HyperX)
	'''
	Et1 = 2
	Et2 = 3
	Ec1 = 5
	Ec2 = 6
	G12 = 8
	Ftu1 = 11
	Ftu2 = 12
	Fcu1 = 13
	Fcu2 = 14
	Fsu12 = 17
	Fsu13 = 18
	Fsu23 = 19
	etu1 = 32
	etu2 = 33
	ecu1 = 34
	ecu2 = 35
	eOHT = 36
	eOHC = 37
	esu12 = 38
	esu13 = 39
	esu23 = 40
	Ftu3 = 50
	D0Tension = DuplicatedValue(82)
	D0Compression = DuplicatedValue(84)
	TensionPristine = DuplicatedValue(1001)
	CompressionPristine = DuplicatedValue(1002)
	ShearPristine = DuplicatedValue(1003)
	TensionOHT = DuplicatedValue(1004)
	CompressionOHC = DuplicatedValue(1005)
	Bearing = 1006
	CompressionCAI = DuplicatedValue(1009)
	CompressionFHC = DuplicatedValue(1010)
	CompressionBVID = DuplicatedValue(1011)
	TensionTAI = DuplicatedValue(1012)
	TensionFHT = DuplicatedValue(1013)
	ShearSAI = DuplicatedValue(1014)
	PullThrough = 1015
	BearingBypass = 1016
	D0_Tension = DuplicatedValue(82), "Use D0Tension instead."
	D0_Compression = DuplicatedValue(84), "Use D0Compression instead."
	Tension_Pristine = DuplicatedValue(1001), "Use TensionPristine instead."
	Compression_Pristine = DuplicatedValue(1002), "Use CompressionPristine instead."
	Shear_Pristine = DuplicatedValue(1003), "Use ShearPristine instead."
	Tension_OHT = DuplicatedValue(1004), "Use TensionOHT instead."
	Compression_OHC = DuplicatedValue(1005), "Use CompressionOHC instead."
	Compression_CAI = DuplicatedValue(1009), "Use CompressionCAI instead."
	Compression_FHC = DuplicatedValue(1010), "Use CompressionFHC instead."
	Compression_BVID = DuplicatedValue(1011), "Use CompressionBVID instead."
	Tension_TAI = DuplicatedValue(1012), "Use TensionTAI instead."
	Tension_FHT = DuplicatedValue(1013), "Use TensionFHT instead."
	Shear_SAI = DuplicatedValue(1014), "Use ShearSAI instead."

class CorrectionValueType(Enum):
	'''
	Defines the type of the independent values on a tabular correction factor row.
	'''
	Double = 0
	Bool = 1
	Integer = 2

class EquationParameterId(DeprecatedEnum):
	'''
	Correction factor parameter names.
	'''
	none = 0
	ConstantLowValue = DuplicatedValue(1001)
	ConstantHighValue = DuplicatedValue(1002)
	ConstantConstant = DuplicatedValue(1003)
	LinearPlyLowValue = DuplicatedValue(2001)
	LinearPlyHighValue = DuplicatedValue(2002)
	LinearPlyConstant = DuplicatedValue(2003)
	LinearPlyPercent0s = DuplicatedValue(2004)
	LinearPlyPercent45s = DuplicatedValue(2005)
	LinearPlyFactorThickness = DuplicatedValue(2006)
	QuadraticPlyTempLowValue = DuplicatedValue(3001)
	QuadraticPlyTempHighValue = DuplicatedValue(3002)
	QuadraticPlyTempConstant = DuplicatedValue(3003)
	QuadraticPlyTempPercent0s = DuplicatedValue(3004)
	QuadraticPlyTempPercent45s = DuplicatedValue(3005)
	QuadraticPlyTempPercent0sSquared = DuplicatedValue(3006)
	QuadraticPlyTempPercent45sSquared = DuplicatedValue(3007)
	QuadraticPlyTempP0sTimesP45s = DuplicatedValue(3008)
	QuadraticPlyTempTemperature = DuplicatedValue(3009)
	QuadraticPlyTempTemperatureSquared = DuplicatedValue(3010)
	QuadraticPlyTempT0 = DuplicatedValue(3011)
	CubicAMLLowValue = DuplicatedValue(4001)
	CubicAMLHighValue = DuplicatedValue(4002)
	CubicAMLConstant = DuplicatedValue(4003)
	CubicAMLAMLNumber = DuplicatedValue(4004)
	CubicAMLAMLNumberSquared = DuplicatedValue(4005)
	CubicAMLAMLNumberCubed = DuplicatedValue(4006)
	BiQuadThickLowValue = DuplicatedValue(5001)
	BiQuadThickHighValue = DuplicatedValue(5002)
	BiQuadThickThreshold = DuplicatedValue(5003)
	BiQuadThickConstant1 = DuplicatedValue(5004)
	BiQuadThickFactorThickness1 = DuplicatedValue(5005)
	BiQuadThickConstant2 = DuplicatedValue(5006)
	BiQuadThickFactorThickness2 = DuplicatedValue(5007)
	BiQuadThickFactorThicknessSquared1 = DuplicatedValue(5008)
	BiQuadThickFactorThicknessSquared2 = DuplicatedValue(5009)
	QuadDiamThickLowValue = DuplicatedValue(6001)
	QuadDiamThickHighValue = DuplicatedValue(6002)
	QuadDiamThickConstant = DuplicatedValue(6003)
	QuadDiamThickDiameter = DuplicatedValue(6004)
	QuadDiamThickDiameterSquared = DuplicatedValue(6005)
	QuadDiamThickThicknessOverD = DuplicatedValue(6006)
	QuadDiamThickThicknessOverDSquared = DuplicatedValue(6007)
	Constant_Low_Value = DuplicatedValue(1001), "Use ConstantLowValue instead."
	Constant_High_Value = DuplicatedValue(1002), "Use ConstantHighValue instead."
	Constant_Constant = DuplicatedValue(1003), "Use ConstantConstant instead."
	LinearPly_Low_Value = DuplicatedValue(2001), "Use LinearPlyLowValue instead."
	LinearPly_High_Value = DuplicatedValue(2002), "Use LinearPlyHighValue instead."
	LinearPly_Constant = DuplicatedValue(2003), "Use LinearPlyConstant instead."
	LinearPly_Percent_0s = DuplicatedValue(2004), "Use LinearPlyPercent0s instead."
	LinearPly_Percent_45s = DuplicatedValue(2005), "Use LinearPlyPercent45s instead."
	LinearPly_Factor_Thickness = DuplicatedValue(2006), "Use LinearPlyFactorThickness instead."
	QuadraticPlyTemp_Low_Value = DuplicatedValue(3001), "Use QuadraticPlyTempLowValue instead."
	QuadraticPlyTemp_High_Value = DuplicatedValue(3002), "Use QuadraticPlyTempHighValue instead."
	QuadraticPlyTemp_Constant = DuplicatedValue(3003), "Use QuadraticPlyTempConstant instead."
	QuadraticPlyTemp_Percent_0s = DuplicatedValue(3004), "Use QuadraticPlyTempPercent0s instead."
	QuadraticPlyTemp_Percent_45s = DuplicatedValue(3005), "Use QuadraticPlyTempPercent45s instead."
	QuadraticPlyTemp_Percent_0s_Squared = DuplicatedValue(3006), "Use QuadraticPlyTempPercent0sSquared instead."
	QuadraticPlyTemp_Percent_45s_Squared = DuplicatedValue(3007), "Use QuadraticPlyTempPercent45sSquared instead."
	QuadraticPlyTemp_P0s_Times_P45s = DuplicatedValue(3008), "Use QuadraticPlyTempP0sTimesP45s instead."
	QuadraticPlyTemp_Temperature = DuplicatedValue(3009), "Use QuadraticPlyTempTemperature instead."
	QuadraticPlyTemp_Temperature_Squared = DuplicatedValue(3010), "Use QuadraticPlyTempTemperatureSquared instead."
	QuadraticPlyTemp_T0 = DuplicatedValue(3011), "Use QuadraticPlyTempT0 instead."
	CubicAML_Low_Value = DuplicatedValue(4001), "Use CubicAMLLowValue instead."
	CubicAML_High_Value = DuplicatedValue(4002), "Use CubicAMLHighValue instead."
	CubicAML_Constant = DuplicatedValue(4003), "Use CubicAMLConstant instead."
	CubicAML_AML_Number = DuplicatedValue(4004), "Use CubicAMLAMLNumber instead."
	CubicAML_AML_Number_Squared = DuplicatedValue(4005), "Use CubicAMLAMLNumberSquared instead."
	CubicAML_AML_Number_Cubed = DuplicatedValue(4006), "Use CubicAMLAMLNumberCubed instead."
	BiQuadThick_Low_Value = DuplicatedValue(5001), "Use BiQuadThickLowValue instead."
	BiQuadThick_High_Value = DuplicatedValue(5002), "Use BiQuadThickHighValue instead."
	BiQuadThick_Threshold = DuplicatedValue(5003), "Use BiQuadThickThreshold instead."
	BiQuadThick_Constant_1 = DuplicatedValue(5004), "Use BiQuadThickConstant1 instead."
	BiQuadThick_Factor_Thickness_1 = DuplicatedValue(5005), "Use BiQuadThickFactorThickness1 instead."
	BiQuadThick_Constant_2 = DuplicatedValue(5006), "Use BiQuadThickConstant2 instead."
	BiQuadThick_Factor_Thickness_2 = DuplicatedValue(5007), "Use BiQuadThickFactorThickness2 instead."
	BiQuadThick_Factor_Thickness_Squared_1 = DuplicatedValue(5008), "Use BiQuadThickFactorThicknessSquared1 instead."
	BiQuadThick_Factor_Thickness_Squared_2 = DuplicatedValue(5009), "Use BiQuadThickFactorThicknessSquared2 instead."
	QuadDiamThick_Low_Value = DuplicatedValue(6001), "Use QuadDiamThickLowValue instead."
	QuadDiamThick_High_Value = DuplicatedValue(6002), "Use QuadDiamThickHighValue instead."
	QuadDiamThick_Constant = DuplicatedValue(6003), "Use QuadDiamThickConstant instead."
	QuadDiamThick_Diameter = DuplicatedValue(6004), "Use QuadDiamThickDiameter instead."
	QuadDiamThick_Diameter_Squared = DuplicatedValue(6005), "Use QuadDiamThickDiameterSquared instead."
	QuadDiamThick_Thickness_Over_D = DuplicatedValue(6006), "Use QuadDiamThickThicknessOverD instead."
	QuadDiamThick_Thickness_Over_D_Squared = DuplicatedValue(6007), "Use QuadDiamThickThicknessOverDSquared instead."

class LaminateFamilySettingType(Enum):
	none = 0
	Allowed = 1
	Required = 2

class LaminateFamilyType(Enum):
	Unknown = 0
	Traditional = 1
	DoubleDouble = 2

class PlyDropPattern(Enum):
	none = 0
	Hourglass = 1
	Diamond = 2
	UpsideDownTriangle = 3
	Pyramid = 4
	Interleaved = 5
	InterleavedHourglass = 6
	Element = 7
	Stiffener = 8

class PlyStiffenerSubType(Enum):
	none = 0
	Base1 = 1
	Plank = 2
	FootCharge = 3
	WebCharge = 4
	CapCharge = 5
	CapCover = 6
	Charge = 7
	Base2 = 8
	BottomCover = 9
	TopCover = 10

class StiffenerLaminateLayerLocation(Enum):
	Base = 1
	Plank = 2
	FootCharge = 3
	WebCharge = 4
	CapCharge = 5
	BottomCover = 6
	TopCover = 7

class StiffenerProfile(Enum):
	Corrugated = 1
	IPanel = 2
	TPanel = 3
	ZPanel = 4
	JPanel = 5
	CPanel = 6
	AnglePanel = 7
	InvertedTPanel = 8
	LPanel = 9
	IsoGrid = 10
	Orthogrid = 11
	GeneralGrid = 12
	IBeam = 13
	CBeam = 14
	TBeam = 15
	ZBeam = 16
	LBeam = 17
	JBeam = 18
	RectangularBeam = 19

class MaterialType(Enum):
	'''
	Represents a material's type.
	'''
	Foam = 0
	Honeycomb = 1
	Isotropic = 2
	Laminate = 3
	Orthotropic = 5

class FamilyObjectUID(Enum):
	Default_Object = 0
	Top_Stack = 1
	Middle_Stack = 2
	Bottom_Stack = 3
	Top_Honeycomb_Face = 4
	Honeycomb_Core = 5
	Bottom_Honeycomb_Face = 6
	Top_Foam_Face = 7
	Foam_Core_Unstiffened = 8
	Bottom_Foam_Face = 9
	Corrugated_FwntTop_with_flange_Open_Span = 10
	Bwidth_Closed_Span = 11
	Wnt_face_only_Joint_Span_Corrugated = 12
	Wnt_Crown_Top_Crown_Top = 13
	Wnt_ComboTop_Bonded_Combo_Top = 14
	FwntAndWnt_ComboTop_Fastened_Flange_and_Face_Top = 15
	Bonded_FwntAndWnt_ComboTop_Bonded_Flange_and_Face_Top = 16
	B2_Web_Web_Corrugated = 17
	Wnb_Crown_bottom_Crown_Bottom = 18
	Wnb_Combo_bottom_Bonded_Combo = 19
	Wnb_face_only_Joint_Span_Corrugated = 20
	Sx_MinusOrDashIdk_Wnb_bottom_face_Bottom_Span = 21
	FwntAndWnt_Discontinuous_Spacing_Span_Corrugated = 22
	FwntTop_no_flange_Clear_Span = 25
	Wnt_face_only_Joint_Span_Uniaxial = 26
	Two_sided_Wnt_Top_Discontinuous_Flange_Top_Uniaxial = 27
	One_sided_Wnt_Top_Discontinuous_Flange_Top_Uniaxial = 28
	Two_sided_Wnt_ComboTop_Discontinuous_Bonded_Combo = 29
	One_sided_Wnt_ComboTop_Discontinuous_Bonded_Combo = 30
	Defunct_entire_span_FwntAndWnt_ComboTop_Continuous_Fastened_Flange_and_Face_Top = 31
	Entire_span_FwntAndWnt_ComboTop_Continuous_Bonded_Flange_and_Face_Top = 32
	B2_Web_Web_Uniaxial = 33
	Two_sided_Wnb_bottom_free_flange_Flange_Bottom_Uniaxial = 34
	One_sided_Wnb_bottom_free_flange_Flange_Bottom_Uniaxial = 35
	Two_sided_Wnb_Combo_bottom_Discontinuous_Bonded_Combo = 36
	Entire_span_FwnbAndWnb_ComboBot_Continuous_Bonded_Flange_and_Face_Bottom = 37
	Wnb_face_only_Joint_Span_Uniaxial = 38
	CleMinusOrDashIdkdash_Wnb_bottom_face_Bottom_Span = 39
	B2_Web_unsupported_Web = 40
	FwntAndWnt_Discontinuous_Spacing_Span_Uniaxial = 41
	Two_sided_Wnt_Top_Discontinuous_Flange_Top_OpenBeam = 43
	One_sided_Wnt_Top_Discontinuous_Flange_Top_OpenBeam = 44
	B2_Web_no_edges_free_Web = 45
	Two_sided_Wnb_bottom_free_flange_Flange_Bottom_OpenBeam = 46
	One_sided_Wnb_bottom_free_flange_Flange_Bottom_OpenBeam = 47
	B2_Web_one_edge_free_Web = 48
	TopFace_Zero_Grid = 49
	TopFace_Ninety_Grid = 50
	TopFace_OrthoGrid = 51
	BottomFace_OrthoGrid = 52
	TopFace_WaffleGrid = 53
	TopFace_AngleGrid = 54
	BottomFace_AngleGrid = 55
	TopFace_GeneralGrid = 56
	Web_Zero_Grid = 59
	Web_Ninety_Grid = 60
	Zero_Web = 61
	Ninety_Web = 62
	AngleWeb_Plus = 63
	AngleWeb_Minus = 64
	FwntTop_with_flange_Open_Span_Uniaxial = 65
	Curved_Wall = 66
	Foam_Core_Uniaxial = 67
	Open_Span = 68
	Frame_Web_Foam_Core_PRSEUS = 69
	Two_sided_Wnt_s_ComboTop_Discontinuous_Bonded_Combo = 70
	Two_sided_Wnt_f_ComboTop_Discontinuous_Bonded_Combo = 71
	B2_Web_Stringer_Web = 72
	Two_sided_Wnb_bottom_stringer_rod_and_laminate = 73
	B2_Web_Frame_Web = 74
	FwntAndWnt_Discontinuous_Spacing_Span_PRSEUS = 75
	Stringer_and_Frame_Bonded_Combo = 76
	Span_between_frames_for_rod_stiffened_panel = 77
	Web_upper = 233
	Web_lower = 234
	Mid_one_sided = 235
	SC_Foot = 236
	SC_Web = 237
	Rectangular_open_beam_Top_Wall = 843
	Rectangular_open_beam_Side_Wall = 845
	Rectangular_open_beam_Bottom_Wall = 846

class JointObject(Enum):
	'''
	Enum identifying the possible entities within a joint
	'''
	EntireJoint = 0
	Fastener = 1
	Sheet1 = 2
	Sheet2 = 3
	Sheet3 = 4
	Sheet4 = 5
	FaceSheetEndCap = 6
	EndCap = 7
	UpperAdhesive = 8
	LowerAdhesive = 9
	UpperDoubler = 10
	LowerDoubler = 11
	EdgeAllowableSheet = 12
	Rivet = 13

class ObjectGroup(Enum):
	EntireConcept = 0
	LaminateSkinTopFacesheet = 1
	Web = 2
	Foot = 3
	CapCrown = 4
	SpacingSpan = 5
	Core = 6
	Wall = 7
	Fastener = 11
	Sheet = 12
	Doubler = 13
	Rivet = 14
	Adhesive = 15
	MiddleStack = 16
	BottomFacesheet = 17

class VariableParameter(Enum):
	none = 0
	BottomFaceThicknessMaterial = 1
	BottomFlangeThickness = 2
	BottomFlangeWidth = 3
	ThreeStackCoreThicknessMaterial = 4
	WebAngle = 5
	Height = 6
	Spacing = 7
	TopFaceThicknessMaterial = 8
	TopClearSpanWidth = 9
	TopFlangeThickness = 10
	TopFlangeWidth = 11
	EllipticalTubeWallThicknessMaterial = 13
	WebThicknessMaterial = 14
	GridStiffened90WebThickness = 15
	GridStiffenedAngleWebThickness = 16
	GridStiffened0WebHeight = 17
	GridStiffened90WebHeight = 18
	GridStiffenedAngleWebHeight = 19
	GridStiffened90WebStiffenerSpacing = 20
	GridStiffenedAngleWebStiffenerSpacing = 21
	RectangularBeamTopWallThickness = 24
	RectangularBeamSideWallThicknessMaterial = 25
	RectangularBeamBottomWallThickness = 26
	BeamWidth = 28
	TubeTaperAngle = 29
	RodStiffenedStringerHeight = 31
	RodStiffenedFrameWebThicknessMaterial = 32
	RodStiffenedFrameHeight = 33
	RodStiffenedFrameSpacing = 34
	RodStiffenedFrameFlangeWidth = 35
	RodStiffenedFrameFlangeThickness = 36
	RodStiffenedRodDiameterMaterial = 37
	RodStiffenedFrameClearSpan = 38
	RodStiffenedFoamThicknessMaterial = 41
	RodStiffenedTopFaceThicknessMaterial = 42
	RodStiffenedStringerSpacing = 43
	RodStiffenedStringerFlangeWidth = 44
	RodStiffenedStringerFlangeThickness = 45
	RodStiffenedStringerClearSpan = 46
	HoneycombThicknessMaterial = 47
	FoamThicknessMaterial = 48
	HeightStiffener = 49
	HeightStiffenerWeb = 50
	CapBeamThicknessMaterial = 51
	FrameMidThickness = 52
	FrameMidWidth = 53
	FrameMidHeight = 54
	ShearClipFootThickness = 55
	ShearClipFootWidth = 56
	ShearClipWebThickness = 57
	ShearClipWebHeight = 58
	FrameWebCapThickness = 59
	ShearClipRefHeight = 60
	CorrugatedWebThicknessMaterial = 61

class LoadSetType(Enum):
	Mechanical = 0
	Thermal = 1

class ProjectModelFormat(Enum):
	UNKNOWN = 0
	MscNastran = 1
	NeiNastran = 5
	NxNastran = 6
	Abaqus = 7
	Ansys = 8
	OptiStruct = 9

class StressReportFormat(Enum):
	Word = 0
	Excel = 1

class SectionCutPropertyLocation(Enum):
	'''
	Centroid vs Origin
	'''
	Centroid = 0
	Origin = 1

class ReferencePlaneBeam(Enum):
	UNKNOWN = 0
	Neutral = 1
	Top = 2
	Bottom = 3

class ReferencePlanePanel(Enum):
	UNKNOWN = 0
	MidplaneTopFace = 1
	Midplane = 2
	MidplaneBottomFace = 3
	OML = 4
	IML = 5

class ZoneBucklingMode(Enum):
	UNKNOWN = 0
	InternalX = 1
	InternalY = 2
	ExternalX = 3
	ExternalY = 4

class SimpleStatus:
	'''
	Lots of methods need to return a Success state and an associated Message.
	'''
	def __init__(self, simpleStatus: _types.SimpleStatus):
		self._Entity = simpleStatus

	def Create_SimpleStatus_success(success: bool):
		return SimpleStatus(_types.SimpleStatus(success))

	def Create_SimpleStatus_success_message(success: bool, message: str):
		return SimpleStatus(_types.SimpleStatus(success, message))

	def Create_SimpleStatus_success_messages(success: bool, messages: list[str]):
		messagesList = List[str]()
		if messages is not None:
			for x in messages:
				if x is not None:
					messagesList.Add(x)
		return SimpleStatus(_types.SimpleStatus(success, messagesList))

	def Create_SimpleStatus_tupleInput(tupleInput: tuple[bool, str]):
		return SimpleStatus(_types.SimpleStatus(tupleInput._Entity))

	@property
	def Success(self) -> bool:
		return self._Entity.Success

	@property
	def Message(self) -> str:
		return self._Entity.Message

	@property
	def Messages(self) -> list[str]:
		return [string for string in self._Entity.Messages]

	@classmethod
	def NewSuccess(self) -> SimpleStatus:
		'''
		For when you just need a success.
		'''
		result = _api.SimpleStatus.NewSuccess
		return SimpleStatus(result) if result is not None else None

	def AddMessage(self, message: str) -> None:
		return self._Entity.AddMessage(message)

	def GetMessage(self) -> str:
		return self._Entity.GetMessage()

	def ToString(self) -> str:
		return self._Entity.ToString()

	@overload
	def Equals(self, obj: object) -> bool:
		...

	@overload
	def Equals(self, other) -> bool:
		...

	def Equals(self, item1 = None) -> bool:
		'''
		Overload 1: ``Equals(self, obj: object) -> bool``

		Overload 2: ``Equals(self, other) -> bool``
		'''
		if isinstance(item1, object):
			return self._Entity.Equals(item1)

		if isinstance(item1, SimpleStatus):
			return self._Entity.Equals(item1._Entity)

		return self._Entity.Equals(item1)

	def __eq__(self, other):
		return self.Equals(other)

	def __ne__(self, other):
		return not self.Equals(other)

	def __hash__(self) -> int:
		return self._Entity.GetHashCode()


class TernaryStatus(SimpleStatus):
	def __init__(self, ternaryStatus: _types.TernaryStatus):
		self._Entity = ternaryStatus

	def Create_TernaryStatus(status: TernaryStatusCode, message: str):
		return TernaryStatus(_types.TernaryStatus(_types.TernaryStatusCode(GetEnumValue(status.value)), message))

	@property
	def Success(self) -> bool:
		'''
		We succeed as long as we do not fail.
		'''
		return self._Entity.Success

	@property
	def Status(self) -> TernaryStatusCode:
		result = self._Entity.Status
		return TernaryStatusCode[result.ToString()] if result is not None else None

	def ToString(self) -> str:
		return self._Entity.ToString()

	@overload
	def Equals(self, obj: object) -> bool:
		...

	@overload
	def Equals(self, other: SimpleStatus) -> bool:
		...

	@overload
	def Equals(self, other) -> bool:
		...

	def Equals(self, item1 = None) -> bool:
		'''
		Overload 1: ``Equals(self, obj: object) -> bool``

		Overload 2: ``Equals(self, other: SimpleStatus) -> bool``

		Overload 3: ``Equals(self, other) -> bool``
		'''
		if isinstance(item1, object):
			return self._Entity.Equals(item1)

		if isinstance(item1, SimpleStatus):
			return self._Entity.Equals(item1._Entity)

		if isinstance(item1, TernaryStatus):
			return self._Entity.Equals(item1._Entity)

		return self._Entity.Equals(item1)

	def __eq__(self, other):
		return self.Equals(other)

	def __ne__(self, other):
		return not self.Equals(other)

	def __hash__(self) -> int:
		return self._Entity.GetHashCode()


class DesignLink:
	def __init__(self, designLink: _types.DesignLink):
		self._Entity = designLink

	def Create_DesignLink(designId: int, familyId: BeamPanelFamily, conceptId: int, linkedVariableId: int):
		return DesignLink(_types.DesignLink(designId, _types.BeamPanelFamily(GetEnumValue(familyId.value)), conceptId, linkedVariableId))

	@property
	def DesignId(self) -> int:
		return self._Entity.DesignId

	@property
	def FamilyId(self) -> BeamPanelFamily:
		result = self._Entity.FamilyId
		return BeamPanelFamily[result.ToString()] if result is not None else None

	@property
	def ConceptId(self) -> int:
		return self._Entity.ConceptId

	@property
	def LinkedVariableId(self) -> int:
		return self._Entity.LinkedVariableId

	@DesignId.setter
	def DesignId(self, value: int) -> None:
		self._Entity.DesignId = value

	@FamilyId.setter
	def FamilyId(self, value: BeamPanelFamily) -> None:
		self._Entity.FamilyId = _types.BeamPanelFamily(GetEnumValue(value.value))

	@ConceptId.setter
	def ConceptId(self, value: int) -> None:
		self._Entity.ConceptId = value

	@LinkedVariableId.setter
	def LinkedVariableId(self, value: int) -> None:
		self._Entity.LinkedVariableId = value

	@overload
	def Equals(self, obj: object) -> bool:
		...

	@overload
	def Equals(self, other) -> bool:
		...

	def Equals(self, item1 = None) -> bool:
		'''
		Overload 1: ``Equals(self, obj: object) -> bool``

		Overload 2: ``Equals(self, other) -> bool``
		'''
		if isinstance(item1, object):
			return self._Entity.Equals(item1)

		if isinstance(item1, DesignLink):
			return self._Entity.Equals(item1._Entity)

		return self._Entity.Equals(item1)

	def __eq__(self, other):
		return self.Equals(other)

	def __ne__(self, other):
		return not self.Equals(other)

	def __hash__(self) -> int:
		return self._Entity.GetHashCode()


class HyperFeaSolver:

	_ProjectModelFormat = ProjectModelFormat
	def __init__(self, hyperFeaSolver: _types.HyperFeaSolver):
		self._Entity = hyperFeaSolver

	def Create_HyperFeaSolver(projectModelFormat: ProjectModelFormat, solverPath: str, arguments: str):
		return HyperFeaSolver(_types.HyperFeaSolver(_types.ProjectModelFormat(GetEnumValue(projectModelFormat.value)), solverPath, arguments))
	@property
	def ProjectModelFormat(self) -> _ProjectModelFormat:
		result = self._Entity.ProjectModelFormat
		return ProjectModelFormat[result.ToString()] if result is not None else None

	@property
	def SolverPath(self) -> str:
		return self._Entity.SolverPath

	@property
	def Arguments(self) -> str:
		return self._Entity.Arguments

	@ProjectModelFormat.setter
	def ProjectModelFormat(self, value: ProjectModelFormat) -> None:
		self._Entity.ProjectModelFormat = _types.ProjectModelFormat(GetEnumValue(value.value))

	@SolverPath.setter
	def SolverPath(self, value: str) -> None:
		self._Entity.SolverPath = value

	@Arguments.setter
	def Arguments(self, value: str) -> None:
		self._Entity.Arguments = value


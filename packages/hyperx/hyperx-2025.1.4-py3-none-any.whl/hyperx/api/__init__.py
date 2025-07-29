from __future__ import annotations
import warnings
warnings.simplefilter("always", DeprecationWarning)
from ..library import _api, _types, ValidateDatabaseVersion

from ..api import types
from typing import TypeVar, Generic, overload
from enum import Enum
from System.Collections.Generic import List, IEnumerable, Dictionary, HashSet
from System.Threading.Tasks import Task
from System import Guid, DateTime, Action, Double, String, Boolean, Nullable

from abc import ABC, abstractmethod

T = TypeVar('T')

def MakeCSharpIntList(ints: list[int]) -> List[int]:
	'''
	Convert a python list to a C#-compatible list.
	'''
	intsList = List[int]()
	if ints is not None:
		for x in ints:
			if x is not None:
				intsList.Add(x)
	
	return intsList

def MakeCSharpStringList(strings: list[str]) -> List[str]:
	stringsList = List[str]()
	if strings is not None:
		for x in strings:
			if x is not None:
				stringsList.Add(x)
	
	return stringsList

'''
Taken from: https://stackoverflow.com/a/3862957
'''
def _all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in _all_subclasses(c)])

class AnalysisResultToReturn(Enum):
	'''
	Used to specify which analysis result to return.
	'''
	Limit = 1
	Ultimate = 2
	Minimum = 3

class CollectionModificationStatus(Enum):
	'''
	Indicates whether a collection was manipulated successfully.
	'''
	Success = 1
	DuplicateIdFailure = 2
	EntityMissingAddFailure = 3
	EntityMissingRemovalFailure = 4
	FemConnectionFailure = 5
	RunSetUsageFailure = 6
	EntityRemovalDependencyFailure = 7

class CreateDatabaseStatus(Enum):
	Success = 1
	TemplateNotFound = 2
	ImproperExtension = 3

class MaterialCreationStatus(Enum):
	'''
	Indicates whether a material was created successfully. 
	If not, this indicates why the material was not created.
	'''
	Success = 1
	DuplicateNameFailure = 2
	DuplicateFemIdFailure = 3
	MissingMaterialToCopy = 4

class DbForceUnit(Enum):
	Pounds = 1
	Newtons = 2
	Dekanewtons = 4

class DbLengthUnit(Enum):
	Inches = 1
	Feet = 2
	Meters = 3
	Centimeters = 4
	Millimeters = 5

class DbMassUnit(Enum):
	Pounds = 1
	Kilograms = 2
	Slinches = 4
	Slugs = 5
	Megagrams = 6

class DbTemperatureUnit(Enum):
	Fahrenheit = 1
	Rankine = 2
	Celsius = 3
	Kelvin = 4

class ProjectCreationStatus(Enum):
	'''
	Indicates whether a project was created successfully. 
	If not, this indicates why the project was not created.
	'''
	Success = 1
	Failure = 2
	DuplicateNameFailure = 3

class ProjectDeletionStatus(Enum):
	'''
	Indicates whether a project was deleted successfully. 
	If not, this indicates why the project was not deleted.
	'''
	Success = 1
	Failure = 2
	ProjectDoesNotExistFailure = 3
	ActiveProjectFailure = 4

class SetUnitsStatus(Enum):
	Success = 1
	Error = 2
	MixedUnitSystemError = 3

class PropertyAssignmentStatus(Enum):
	Success = 1
	Failure = 2
	FailureCollectionAssignment = 3
	PropertyIsNull = 4
	PropertyNotFoundInDb = 5
	EmptyCollection = 6
	IncompatiblePropertyAssignment = 7
	EntityDoesNotExist = 8
	IncompatibleCategoryAssignment = 9

class RundeckBulkUpdateStatus(Enum):
	NoRundecksUpdated = 0
	Success = 1
	InputFilePathDoesNotExist = 2
	ResultFilePathDoesNotExist = 3
	InputFilePathAlreadyExists = 4
	ResultFilePathAlreadyExists = 5
	InvalidPathCount = 6
	RundeckBulkUpdateFailure = 7
	SuccessButIncompatibleFem = 8

class RundeckCreationStatus(Enum):
	Success = 1
	InputFilePathAlreadyExists = 2
	ResultFilePathAlreadyExists = 3

class RundeckRemoveStatus(Enum):
	Success = 1
	InvalidId = 2
	CannotRemoveLastRundeck = 3
	CannotDeletePrimaryRundeck = 4
	RundeckNotFound = 5
	RundeckRemoveFailure = 6
	SuccessButIncompatibleFem = 7

class RundeckUpdateStatus(Enum):
	Success = 1
	InvalidId = 2
	IdDoesNotExist = 3
	RundeckAlreadyPrimary = 4
	InputPathInUse = 5
	ResultPathInUse = 6
	RundeckCommitFailure = 7
	InputPathDoesNotExist = 8
	ResultPathDoesNotExist = 9
	SuccessButIncompatibleFem = 10

class ZoneCreationStatus(Enum):
	'''
	Indicates whether a zone was created successfully. 
	If not, this indicates why the zone was not created.
	'''
	Success = 1
	DuplicateNameFailure = 2
	InvalidFamilyCategory = 3

class ZoneIdUpdateStatus(Enum):
	Success = 1
	DuplicateIdFailure = 2
	IdOutOfRangeError = 3

class UnitSystem(Enum):
	'''
	Unit system specified when starting a scripting Application.
	'''
	English = 1
	SI = 2

class IdEntity(ABC):
	'''
	Represents an entity with an ID.
	'''
	def __init__(self, idEntity: _api.IdEntity):
		self._Entity = idEntity

	@property
	def Id(self) -> int:
		return self._Entity.Id


class IdNameEntity(IdEntity):
	'''
	Represents an entity with an ID and Name.
	'''
	def __init__(self, idNameEntity: _api.IdNameEntity):
		self._Entity = idNameEntity

	@property
	def Name(self) -> str:
		return self._Entity.Name

class AnalysisDefinition(IdNameEntity):
	def __init__(self, analysisDefinition: _api.AnalysisDefinition):
		self._Entity = analysisDefinition

	@property
	def AnalysisId(self) -> int:
		warnings.warn("Do not use this property. Use Id.", DeprecationWarning, 2)
		return self._Entity.AnalysisId

	@property
	def Description(self) -> str:
		'''
		A more detailed description of the analysis criterion.
		'''
		return self._Entity.Description

	@property
	def UID(self) -> Guid:
		return self._Entity.UID

	@property
	def V205UID(self) -> Guid | None:
		return self._Entity.V205UID


class Margin:
	'''
	Represents a Margin result.
	'''
	def __init__(self, margin: _api.Margin):
		self._Entity = margin

	@property
	def AdjustedMargin(self) -> float | None:
		'''
		The adjusted margin for this ``hyperx.api.Margin``, if present.
		This value may be ``None`` when the ``hyperx.api.Margin`` has a code (see: ``hyperx.api.Margin.MarginCode``).
		'''
		return self._Entity.AdjustedMargin

	@property
	def IsFailureCode(self) -> bool:
		'''
		Indicates whether the code is a failure code or not.
		If ``True``, ``hyperx.api.Margin.IsInformationalCode`` should return ``False``.
		'''
		return self._Entity.IsFailureCode

	@property
	def IsInformationalCode(self) -> bool:
		'''
		Indicates whether the code is an informational code or not.
		If ``True``, ``hyperx.api.Margin.IsFailureCode`` should return ``False``.
		'''
		return self._Entity.IsInformationalCode

	@property
	def MarginCode(self) -> types.MarginCode:
		'''
		Returns a failure code when ``hyperx.api.Margin.IsFailureCode`` is ``True``,
		returns an informational code when ``hyperx.api.Margin.IsInformationalCode`` is ``True``,
		or returns ``hyperx.api.types.MarginCode.Value`` when the ``hyperx.api.Margin.AdjustedMargin`` has a value.
		'''
		result = self._Entity.MarginCode
		return types.MarginCode[result.ToString()] if result is not None else None

	def CompareTo(self, other) -> int:
		'''
		Compare margins to determine which is more critical.
		
		:param other: The margin to compare to
		
		:return: -1 if this margin is more critical,
		0 if the margins are equally critical,
		or 1 if the other margin is more critical.
		'''
		return self._Entity.CompareTo(other._Entity)


class AnalysisDetail:
	def __init__(self, analysisDetail: _api.AnalysisDetail):
		self._Entity = analysisDetail

	@property
	def Name(self) -> str:
		return self._Entity.Name

	@property
	def Path(self) -> list[str]:
		return [string for string in self._Entity.Path]

	@property
	def DataType(self) -> type:
		'''
		The ``hyperx.api.AnalysisDetail.Value`` can be of any type. This property provides information on the type.
		'''
		return self._Entity.DataType

	@property
	def Value(self) -> object:
		'''
		The detail value which has type ``hyperx.api.AnalysisDetail.DataType``.
		'''
		return self._Entity.Value

	@property
	def AnalysisDetails(self) -> AnalysisDetailCol:
		result = self._Entity.AnalysisDetails
		return AnalysisDetailCol(result) if result is not None else None

	def GetValue(self) -> object:
		return self._Entity.GetValue()


class AnalysisDetailCol(Generic[T]):
	def __init__(self, analysisDetailCol: _api.AnalysisDetailCol):
		self._Entity = analysisDetailCol

	@property
	def AnalysisDetailColList(self) -> tuple[AnalysisDetail]:
		return tuple([AnalysisDetail(analysisDetailCol) for analysisDetailCol in self._Entity])

	@overload
	def Get(self, name: str) -> AnalysisDetail:
		'''
		Get an ``hyperx.api.AnalysisDetail`` by name.
		
		:raises ``System.InvalidOperationException``: If the name is not found.
		'''
		...

	@overload
	def Get(self, path: tuple[str]) -> AnalysisDetail:
		...

	def Get(self, item1 = None) -> AnalysisDetail:
		'''
		Overload 1: ``Get(self, name: str) -> AnalysisDetail``

		Get an ``hyperx.api.AnalysisDetail`` by name.
		
		:raises ``System.InvalidOperationException``: If the name is not found.

		Overload 2: ``Get(self, path: tuple[str]) -> AnalysisDetail``
		'''
		if isinstance(item1, str):
			return AnalysisDetail(self._Entity.Get(item1))

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, str) for x in item1):
			pathList = List[str]()
			if item1 is not None:
				for x in item1:
					if x is not None:
						pathList.Add(x)
			pathEnumerable = IEnumerable(pathList)
			return AnalysisDetail(self._Entity.Get(pathEnumerable))

		return AnalysisDetail(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.AnalysisDetailColList[index]

	def __iter__(self):
		yield from self.AnalysisDetailColList

	def __len__(self):
		return len(self.AnalysisDetailColList)


class AnalysisResult(ABC):
	'''
	Contains result information for an analysis
	'''

	_Margin = Margin

	_AnalysisDefinition = AnalysisDefinition
	def __init__(self, analysisResult: _api.AnalysisResult):
		self._Entity = analysisResult

	@property
	def LimitUltimate(self) -> types.LimitUltimate:
		result = self._Entity.LimitUltimate
		return types.LimitUltimate[result.ToString()] if result is not None else None

	@property
	def LoadCaseId(self) -> int:
		'''
		Returns the Id that can be used to access design case objects from the ``hyperx.api.DesignLoadCol``.
		
		:return: The load case Id or 0 if the load is a user load.
		'''
		return self._Entity.LoadCaseId

	@property
	def ScenarioId(self) -> int | None:
		'''
		Applicable to User FEA loads and User General loads. Returns the scenario Id.
		'''
		return self._Entity.ScenarioId
	@property
	def Margin(self) -> _Margin:
		result = self._Entity.Margin
		return Margin(result) if result is not None else None
	@property
	def AnalysisDefinition(self) -> _AnalysisDefinition:
		result = self._Entity.AnalysisDefinition
		return AnalysisDefinition(result) if result is not None else None

	@property
	def AnalysisDetails(self) -> AnalysisDetailCol:
		result = self._Entity.AnalysisDetails
		return AnalysisDetailCol(result) if result is not None else None


class JointAnalysisResult(AnalysisResult):
	def __init__(self, jointAnalysisResult: _api.JointAnalysisResult):
		self._Entity = jointAnalysisResult

	@property
	def ObjectId(self) -> types.JointObject:
		result = self._Entity.ObjectId
		return types.JointObject[result.ToString()] if result is not None else None


class ZoneAnalysisResult(AnalysisResult):
	def __init__(self, zoneAnalysisResult: _api.ZoneAnalysisResult):
		self._Entity = zoneAnalysisResult


class ZoneAnalysisConceptResult(ZoneAnalysisResult):
	def __init__(self, zoneAnalysisConceptResult: _api.ZoneAnalysisConceptResult):
		self._Entity = zoneAnalysisConceptResult

	@property
	def ConceptId(self) -> types.FamilyConceptUID:
		result = self._Entity.ConceptId
		return types.FamilyConceptUID[result.ToString()] if result is not None else None


class ZoneAnalysisObjectResult(ZoneAnalysisResult):
	def __init__(self, zoneAnalysisObjectResult: _api.ZoneAnalysisObjectResult):
		self._Entity = zoneAnalysisObjectResult

	@property
	def ObjectId(self) -> types.FamilyObjectUID:
		result = self._Entity.ObjectId
		return types.FamilyObjectUID[result.ToString()] if result is not None else None


class ZoneAnalysisSolverResult(ZoneAnalysisResult):
	def __init__(self, zoneAnalysisSolverResult: _api.ZoneAnalysisSolverResult):
		self._Entity = zoneAnalysisSolverResult

	def Create_ZoneAnalysisSolverResult(limitUltimate: types.LimitUltimate, loadCaseId: int, scenarioId: int | None, margin: Margin, analysisDefinition: AnalysisDefinition, analysisObjectTag: Enum, analysisObjectIndex: int, analysisDetails: AnalysisDetailCol):
		return ZoneAnalysisSolverResult(_api.ZoneAnalysisSolverResult(_types.LimitUltimate(types.GetEnumValue(limitUltimate.value)), loadCaseId, scenarioId, margin._Entity, analysisDefinition._Entity, analysisObjectTag._Entity, analysisObjectIndex, analysisDetails._Entity))

	@property
	def AnalysisObjectTag(self) -> Enum:
		return self._Entity.AnalysisObjectTag

	@property
	def AnalysisObjectIndex(self) -> int:
		return self._Entity.AnalysisObjectIndex

	def GetFamilyObjectUID(self, familyId: types.BeamPanelFamily, conceptId: int) -> types.FamilyObjectUID | None:
		return types.FamilyObjectUID(self._Entity.GetFamilyObjectUID(_types.BeamPanelFamily(types.GetEnumValue(familyId.value)), conceptId))


class AssignableProperty(IdNameEntity):
	def __init__(self, assignableProperty: _api.AssignableProperty):
		self._Entity = assignableProperty


class AssignablePropertyWithFamilyCategory(AssignableProperty):
	def __init__(self, assignablePropertyWithFamilyCategory: _api.AssignablePropertyWithFamilyCategory):
		self._Entity = assignablePropertyWithFamilyCategory

	@property
	def FamilyCategory(self) -> types.FamilyCategory:
		result = self._Entity.FamilyCategory
		return types.FamilyCategory[result.ToString()] if result is not None else None


class FailureObjectGroup(IdNameEntity):
	def __init__(self, failureObjectGroup: _api.FailureObjectGroup):
		self._Entity = failureObjectGroup

	@property
	def ObjectGroup(self) -> types.ObjectGroup:
		result = self._Entity.ObjectGroup
		return types.ObjectGroup[result.ToString()] if result is not None else None

	@property
	def IsEnabled(self) -> bool:
		return self._Entity.IsEnabled

	@property
	def LimitUltimate(self) -> types.LimitUltimate:
		result = self._Entity.LimitUltimate
		return types.LimitUltimate[result.ToString()] if result is not None else None

	@property
	def RequiredMargin(self) -> float:
		return self._Entity.RequiredMargin

	@IsEnabled.setter
	def IsEnabled(self, value: bool) -> None:
		self._Entity.IsEnabled = value

	@LimitUltimate.setter
	def LimitUltimate(self, value: types.LimitUltimate) -> None:
		self._Entity.LimitUltimate = _types.LimitUltimate(types.GetEnumValue(value.value))

	@RequiredMargin.setter
	def RequiredMargin(self, value: float) -> None:
		self._Entity.RequiredMargin = value


class FailureSetting(IdNameEntity):
	'''
	Setting for a Failure Mode or a Failure Criteria.
	'''
	def __init__(self, failureSetting: _api.FailureSetting):
		self._Entity = failureSetting

	@property
	def CategoryId(self) -> int:
		return self._Entity.CategoryId

	@property
	def DataType(self) -> types.UserConstantDataType:
		result = self._Entity.DataType
		return types.UserConstantDataType[result.ToString()] if result is not None else None

	@property
	def DefaultValue(self) -> str:
		return self._Entity.DefaultValue

	@property
	def Description(self) -> str:
		return self._Entity.Description

	@property
	def EnumValues(self) -> dict[int, str]:
		enumValuesDict = {}
		for kvp in self._Entity.EnumValues:
			enumValuesDict[int(kvp.Key)] = str(kvp.Value)

		return enumValuesDict

	@property
	def PackageId(self) -> int | None:
		return self._Entity.PackageId

	@property
	def PackageSettingId(self) -> int | None:
		return self._Entity.PackageSettingId

	@property
	def UID(self) -> Guid:
		return self._Entity.UID

	@property
	def Value(self) -> str:
		'''
		Use Set[DataType]Value() methods to set the value for the setting.
		'''
		return self._Entity.Value

	def SetStringValue(self, value: str) -> None:
		return self._Entity.SetStringValue(value)

	def SetIntValue(self, value: int | None) -> None:
		return self._Entity.SetIntValue(value)

	def SetFloatValue(self, value: float | None) -> None:
		return self._Entity.SetFloatValue(value)

	def SetBoolValue(self, value: bool) -> None:
		return self._Entity.SetBoolValue(value)

	def SetSelectionValue(self, index: int) -> None:
		'''
		Set enum value by index.
		
		:raises ``System.InvalidOperationException``:
		'''
		return self._Entity.SetSelectionValue(index)


class IdEntityCol(Generic[T], ABC):
	def __init__(self, idEntityCol: _api.IdEntityCol):
		self._Entity = idEntityCol

	@property
	def Ids(self) -> tuple[int]:
		return tuple([int32 for int32 in self._Entity.Ids])

	def Contains(self, id: int) -> bool:
		return self._Entity.Contains(id)

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, id: int) -> IdEntity:
		return self._Entity.Get(id)


class IdNameEntityCol(IdEntityCol, Generic[T]):
	def __init__(self, idNameEntityCol: _api.IdNameEntityCol):
		self._Entity = idNameEntityCol
		self._CollectedClass = T

	@property
	def Names(self) -> tuple[str]:
		return tuple([string for string in self._Entity.Names])

	@overload
	def Get(self, name: str) -> IdNameEntity:
		...

	@overload
	def Get(self, id: int) -> IdNameEntity:
		...

	def Get(self, item1 = None) -> IdNameEntity:
		'''
		Overload 1: ``Get(self, name: str) -> IdNameEntity``

		Overload 2: ``Get(self, id: int) -> IdNameEntity``
		'''
		if isinstance(item1, str):
			return self._Entity.Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

		return self._Entity.Get(item1)


class FailureObjectGroupCol(IdNameEntityCol[FailureObjectGroup]):
	def __init__(self, failureObjectGroupCol: _api.FailureObjectGroupCol):
		self._Entity = failureObjectGroupCol
		self._CollectedClass = FailureObjectGroup

	@property
	def FailureObjectGroupColList(self) -> tuple[FailureObjectGroup]:
		return tuple([FailureObjectGroup(failureObjectGroupCol) for failureObjectGroupCol in self._Entity])

	@overload
	def Get(self, objectGroup: types.ObjectGroup) -> FailureObjectGroup:
		'''
		Get FailureObjectGroup by ``hyperx.api.types.ObjectGroup`` enum.
		'''
		...

	@overload
	def Get(self, name: str) -> FailureObjectGroup:
		...

	@overload
	def Get(self, id: int) -> FailureObjectGroup:
		...

	def Get(self, item1 = None) -> FailureObjectGroup:
		'''
		Overload 1: ``Get(self, objectGroup: types.ObjectGroup) -> FailureObjectGroup``

		Get FailureObjectGroup by ``hyperx.api.types.ObjectGroup`` enum.

		Overload 2: ``Get(self, name: str) -> FailureObjectGroup``

		Overload 3: ``Get(self, id: int) -> FailureObjectGroup``
		'''
		if isinstance(item1, types.ObjectGroup):
			return FailureObjectGroup(self._Entity.Get(_types.ObjectGroup(types.GetEnumValue(item1.value))))

		if isinstance(item1, str):
			return FailureObjectGroup(super().Get(item1))

		if isinstance(item1, int):
			return FailureObjectGroup(super().Get(item1))

		return FailureObjectGroup(self._Entity.Get(_types.ObjectGroup(types.GetEnumValue(item1.value))))

	def __getitem__(self, index: int):
		return self.FailureObjectGroupColList[index]

	def __iter__(self):
		yield from self.FailureObjectGroupColList

	def __len__(self):
		return len(self.FailureObjectGroupColList)


class FailureSettingCol(IdNameEntityCol[FailureSetting]):
	def __init__(self, failureSettingCol: _api.FailureSettingCol):
		self._Entity = failureSettingCol
		self._CollectedClass = FailureSetting

	@property
	def FailureSettingColList(self) -> tuple[FailureSetting]:
		failureSettingColList = []
		subclasses = {x.__name__: x for x in _all_subclasses(FailureSetting)}
		for failureSettingCol in self._Entity:
			if type(failureSettingCol).__name__ in subclasses.keys():
				thisType = subclasses[type(failureSettingCol).__name__]
				failureSettingColList.append(thisType(failureSettingCol))
			else:
				raise Exception(f"Could not wrap item in FailureSettingCol. This should not happen.")
		return tuple(failureSettingColList)

	@overload
	def Get(self, name: str) -> FailureSetting:
		...

	@overload
	def Get(self, id: int) -> FailureSetting:
		...

	def Get(self, item1 = None) -> FailureSetting:
		'''
		Overload 1: ``Get(self, name: str) -> FailureSetting``

		Overload 2: ``Get(self, id: int) -> FailureSetting``
		'''
		if isinstance(item1, str):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = FailureSetting
			for subclass in _all_subclasses(FailureSetting):
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, int):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = FailureSetting
			for subclass in _all_subclasses(FailureSetting):
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		result = self._Entity.Get(item1)
		thisClass = type(result).__name__
		givenClass = FailureSetting
		for subclass in _all_subclasses(FailureSetting):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def __getitem__(self, index: int):
		return self.FailureSettingColList[index]

	def __iter__(self):
		yield from self.FailureSettingColList

	def __len__(self):
		return len(self.FailureSettingColList)


class FailureCriterion(IdNameEntity):
	def __init__(self, failureCriterion: _api.FailureCriterion):
		self._Entity = failureCriterion

	@property
	def Id(self) -> int:
		'''
		Obsolete! Use ``hyperx.api.FailureCriterion.Identifier`` instead.
		'''
		warnings.warn("Use Identifier property instead", DeprecationWarning, 2)
		return self._Entity.Id

	@property
	def Identifier(self) -> str:
		return self._Entity.Identifier

	@property
	def Description(self) -> str:
		return self._Entity.Description

	@property
	def IsEnabled(self) -> bool | None:
		'''
		True if the analysis is enabled (``None`` if the object list has inconsistent settings)
		'''
		return self._Entity.IsEnabled

	@property
	def LimitUltimate(self) -> types.LimitUltimate | None:
		'''
		Limit/ultimate setting for the analysis (``None`` if the object list has inconsistent settings)
		'''
		result = self._Entity.LimitUltimate
		return types.LimitUltimate[result.ToString()] if result is not None else None

	@property
	def ObjectGroups(self) -> FailureObjectGroupCol:
		result = self._Entity.ObjectGroups
		return FailureObjectGroupCol(result) if result is not None else None

	@property
	def RequiredMargin(self) -> float | None:
		'''
		Required margin for the analysis (``None`` if the object list has inconsistent settings)
		'''
		return self._Entity.RequiredMargin

	@property
	def Settings(self) -> FailureSettingCol:
		result = self._Entity.Settings
		return FailureSettingCol(result) if result is not None else None

	@IsEnabled.setter
	def IsEnabled(self, value: bool | None) -> None:
		self._Entity.IsEnabled = value

	@LimitUltimate.setter
	def LimitUltimate(self, value: types.LimitUltimate | None) -> None:
		self._Entity.LimitUltimate = value if value is None else _types.LimitUltimate(types.GetEnumValue(value.value))

	@RequiredMargin.setter
	def RequiredMargin(self, value: float | None) -> None:
		self._Entity.RequiredMargin = value


class IdNameEntityRenameable(IdNameEntity):
	def __init__(self, idNameEntityRenameable: _api.IdNameEntityRenameable):
		self._Entity = idNameEntityRenameable

	def Rename(self, name: str) -> None:
		return self._Entity.Rename(name)


class FailureCriterionCol(IdNameEntityCol[FailureCriterion]):
	def __init__(self, failureCriterionCol: _api.FailureCriterionCol):
		self._Entity = failureCriterionCol
		self._CollectedClass = FailureCriterion

	@property
	def FailureCriterionColList(self) -> tuple[FailureCriterion]:
		return tuple([FailureCriterion(failureCriterionCol) for failureCriterionCol in self._Entity])

	def GetByIdentifier(self, identifier: str) -> FailureCriterion:
		'''
		Get a ``hyperx.api.FailureCriterion`` by ``hyperx.api.FailureCriterion.Identifier``.
		<br /><br />
		Throws a ``System.Collections.Generic.KeyNotFoundException`` if a ``hyperx.api.FailureCriterion`` with the ``identifier`` is not found.
		
		:raises ``System.Collections.Generic.KeyNotFoundException``:
		'''
		return FailureCriterion(self._Entity.GetByIdentifier(identifier))

	@overload
	def Get(self, name: str) -> FailureCriterion:
		...

	@overload
	def Get(self, id: int) -> FailureCriterion:
		...

	def Get(self, item1 = None) -> FailureCriterion:
		'''
		Overload 1: ``Get(self, name: str) -> FailureCriterion``

		Overload 2: ``Get(self, id: int) -> FailureCriterion``
		'''
		if isinstance(item1, str):
			return FailureCriterion(super().Get(item1))

		if isinstance(item1, int):
			return FailureCriterion(super().Get(item1))

		return FailureCriterion(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.FailureCriterionColList[index]

	def __iter__(self):
		yield from self.FailureCriterionColList

	def __len__(self):
		return len(self.FailureCriterionColList)


class FailureMode(IdNameEntityRenameable):
	def __init__(self, failureMode: _api.FailureMode):
		self._Entity = failureMode

	@property
	def AnalysisCategoryId(self) -> int:
		return self._Entity.AnalysisCategoryId

	@property
	def AnalysisCategoryName(self) -> str:
		return self._Entity.AnalysisCategoryName

	@property
	def Criteria(self) -> FailureCriterionCol:
		result = self._Entity.Criteria
		return FailureCriterionCol(result) if result is not None else None

	@property
	def Settings(self) -> FailureSettingCol:
		result = self._Entity.Settings
		return FailureSettingCol(result) if result is not None else None

	def Copy(self) -> FailureMode:
		'''
		Creates and returns a copy of this ``hyperx.api.FailureMode``.
		
		:return: The new copied ``hyperx.api.FailureMode``.
		'''
		return FailureMode(self._Entity.Copy())


class FailureModeCol(IdNameEntityCol[FailureMode]):
	def __init__(self, failureModeCol: _api.FailureModeCol):
		self._Entity = failureModeCol
		self._CollectedClass = FailureMode

	@property
	def FailureModeColList(self) -> tuple[FailureMode]:
		return tuple([FailureMode(failureModeCol) for failureModeCol in self._Entity])

	@overload
	def CreateFailureMode(self, failureModeCategoryId: int, name: str = None) -> FailureMode:
		'''
		Create a FailureMode by Id.
		
		:return: The created FailureMode.
		'''
		...

	@overload
	def CreateFailureMode(self, failureModeCategory: str, name: str = None) -> FailureMode:
		'''
		Create a FailureMode by category.
		
		:return: The created FailureMode.
		'''
		...

	@overload
	def DeleteFailureMode(self, name: str) -> bool:
		'''
		Delete a ``hyperx.api.FailureMode``.
		
		:return: ``False`` if there is no failure mode in the collection with the given name.
		'''
		...

	@overload
	def DeleteFailureMode(self, id: int) -> bool:
		'''
		Delete a ``hyperx.api.FailureMode``.
		
		:return: ``False`` if there is no failure mode in the collection with the given ID.
		'''
		...

	@overload
	def Get(self, name: str) -> FailureMode:
		...

	@overload
	def Get(self, id: int) -> FailureMode:
		...

	def CreateFailureMode(self, item1 = None, item2 = None) -> FailureMode:
		'''
		Overload 1: ``CreateFailureMode(self, failureModeCategoryId: int, name: str = None) -> FailureMode``

		Create a FailureMode by Id.
		
		:return: The created FailureMode.

		Overload 2: ``CreateFailureMode(self, failureModeCategory: str, name: str = None) -> FailureMode``

		Create a FailureMode by category.
		
		:return: The created FailureMode.
		'''
		if isinstance(item1, int) and isinstance(item2, str):
			return FailureMode(self._Entity.CreateFailureMode(item1, item2))

		if isinstance(item1, str) and isinstance(item2, str):
			return FailureMode(self._Entity.CreateFailureMode(item1, item2))

		return FailureMode(self._Entity.CreateFailureMode(item1, item2))

	def DeleteFailureMode(self, item1 = None) -> bool:
		'''
		Overload 1: ``DeleteFailureMode(self, name: str) -> bool``

		Delete a ``hyperx.api.FailureMode``.
		
		:return: ``False`` if there is no failure mode in the collection with the given name.

		Overload 2: ``DeleteFailureMode(self, id: int) -> bool``

		Delete a ``hyperx.api.FailureMode``.
		
		:return: ``False`` if there is no failure mode in the collection with the given ID.
		'''
		if isinstance(item1, str):
			return self._Entity.DeleteFailureMode(item1)

		if isinstance(item1, int):
			return self._Entity.DeleteFailureMode(item1)

		return self._Entity.DeleteFailureMode(item1)

	def Get(self, item1 = None) -> FailureMode:
		'''
		Overload 1: ``Get(self, name: str) -> FailureMode``

		Overload 2: ``Get(self, id: int) -> FailureMode``
		'''
		if isinstance(item1, str):
			return FailureMode(super().Get(item1))

		if isinstance(item1, int):
			return FailureMode(super().Get(item1))

		return FailureMode(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.FailureModeColList[index]

	def __iter__(self):
		yield from self.FailureModeColList

	def __len__(self):
		return len(self.FailureModeColList)


class AnalysisProperty(AssignablePropertyWithFamilyCategory):
	def __init__(self, analysisProperty: _api.AnalysisProperty):
		self._Entity = analysisProperty

	@property
	def FailureModes(self) -> FailureModeCol:
		result = self._Entity.FailureModes
		return FailureModeCol(result) if result is not None else None

	@overload
	def AddFailureMode(self, id: int) -> None:
		'''
		Add a failure mode to the ``hyperx.api.AnalysisProperty`` by the ``hyperx.api.FailureMode`` Id.
		'''
		...

	@overload
	def AddFailureMode(self, ids: tuple[int]) -> None:
		'''
		Adds a collection of failure modes to the ``hyperx.api.AnalysisProperty`` by the ``hyperx.api.FailureMode`` Id.
		'''
		...

	@overload
	def RemoveFailureMode(self, id: int) -> None:
		'''
		Remove a failure mode from the ``hyperx.api.AnalysisProperty`` by the ``hyperx.api.FailureMode`` Id.
		'''
		...

	@overload
	def RemoveFailureMode(self, ids: tuple[int]) -> None:
		'''
		Remove a collection of failure modes from the ``hyperx.api.AnalysisProperty`` by the ``hyperx.api.FailureMode`` Id.
		'''
		...

	def AssignTo(self, entityIds: tuple[int]) -> PropertyAssignmentStatus:
		'''
		Assigns the ``hyperx.api.AnalysisProperty`` to a collection of entity Ids
		where the entity type is determined by the ``hyperx.api.AssignablePropertyWithFamilyCategory.FamilyCategory`` property.
		
		:return: ``hyperx.api.PropertyAssignmentStatus.Success`` if the operation executes successfully.
		'''
		entityIdsList = MakeCSharpIntList(entityIds)
		entityIdsEnumerable = IEnumerable(entityIdsList)
		return PropertyAssignmentStatus[self._Entity.AssignTo(entityIdsEnumerable).ToString()]

	def Copy(self) -> AnalysisProperty:
		'''
		Creates and returns a copy of this ``hyperx.api.AnalysisProperty``.
		
		:return: The new copied ``hyperx.api.AnalysisProperty``.
		'''
		return AnalysisProperty(self._Entity.Copy())

	def AddFailureMode(self, item1 = None) -> None:
		'''
		Overload 1: ``AddFailureMode(self, id: int) -> None``

		Add a failure mode to the ``hyperx.api.AnalysisProperty`` by the ``hyperx.api.FailureMode`` Id.

		Overload 2: ``AddFailureMode(self, ids: tuple[int]) -> None``

		Adds a collection of failure modes to the ``hyperx.api.AnalysisProperty`` by the ``hyperx.api.FailureMode`` Id.
		'''
		if isinstance(item1, int):
			return self._Entity.AddFailureMode(item1)

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			idsList = MakeCSharpIntList(item1)
			idsEnumerable = IEnumerable(idsList)
			return self._Entity.AddFailureMode(idsEnumerable)

		return self._Entity.AddFailureMode(item1)

	def RemoveFailureMode(self, item1 = None) -> None:
		'''
		Overload 1: ``RemoveFailureMode(self, id: int) -> None``

		Remove a failure mode from the ``hyperx.api.AnalysisProperty`` by the ``hyperx.api.FailureMode`` Id.

		Overload 2: ``RemoveFailureMode(self, ids: tuple[int]) -> None``

		Remove a collection of failure modes from the ``hyperx.api.AnalysisProperty`` by the ``hyperx.api.FailureMode`` Id.
		'''
		if isinstance(item1, int):
			return self._Entity.RemoveFailureMode(item1)

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			idsList = MakeCSharpIntList(item1)
			idsEnumerable = IEnumerable(idsList)
			return self._Entity.RemoveFailureMode(idsEnumerable)

		return self._Entity.RemoveFailureMode(item1)


class DesignProperty(AssignablePropertyWithFamilyCategory):
	def __init__(self, designProperty: _api.DesignProperty):
		self._Entity = designProperty

	def AssignTo(self, entityIds: tuple[int]) -> PropertyAssignmentStatus:
		'''
		Assigns the ``hyperx.api.DesignProperty`` to a collection of ``entityIds``
		where the entity type is determined by the ``hyperx.api.AssignablePropertyWithFamilyCategory.FamilyCategory`` property.
		
		:return: ``hyperx.api.PropertyAssignmentStatus.Success`` if the operation executes successfully.
		'''
		entityIdsList = MakeCSharpIntList(entityIds)
		entityIdsEnumerable = IEnumerable(entityIdsList)
		return PropertyAssignmentStatus[self._Entity.AssignTo(entityIdsEnumerable).ToString()]

	def Copy(self, newName: str = None) -> DesignProperty:
		'''
		Creates and returns a copy of this ``hyperx.api.DesignProperty``.
		
		:return: The new copied ``hyperx.api.DesignProperty``.
		'''
		result = self._Entity.Copy(newName)
		thisClass = type(result).__name__
		givenClass = DesignProperty
		for subclass in _all_subclasses(DesignProperty):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None


class LoadProperty(AssignableProperty):
	def __init__(self, loadProperty: _api.LoadProperty):
		self._Entity = loadProperty

	@property
	def Category(self) -> types.FamilyCategory:
		'''
		The ``hyperx.api.types.FamilyCategory`` of the ``hyperx.api.LoadProperty``.
		'''
		result = self._Entity.Category
		return types.FamilyCategory[result.ToString()] if result is not None else None

	@property
	def Type(self) -> types.LoadPropertyType:
		'''
		The ``hyperx.api.types.LoadPropertyType`` of the ``hyperx.api.LoadProperty``.
		'''
		result = self._Entity.Type
		return types.LoadPropertyType[result.ToString()] if result is not None else None

	@property
	def IsZeroCurvature(self) -> bool:
		'''
		Explains where the moment reference is relative to for User FEA or User General Panel Loads.
		
		:return: ``True`` if moment reference is relative to zero curvature or
		``False`` to indicate the moment reference is relative to the panel reference plane.
		'''
		return self._Entity.IsZeroCurvature

	@property
	def ModificationDate(self) -> DateTime:
		return self._Entity.ModificationDate

	def AssignTo(self, entityIds: tuple[int], category: types.FamilyCategory) -> PropertyAssignmentStatus:
		'''
		Assign this ``hyperx.api.LoadProperty`` to entities represented by ``entityIds``.
		
		:return: ``hyperx.api.PropertyAssignmentStatus.Success`` if the assignment is successful.
		'''
		entityIdsList = MakeCSharpIntList(entityIds)
		entityIdsEnumerable = IEnumerable(entityIdsList)
		return PropertyAssignmentStatus[self._Entity.AssignTo(entityIdsEnumerable, _types.FamilyCategory(types.GetEnumValue(category.value))).ToString()]

	def Copy(self) -> LoadProperty:
		'''
		Creates and returns a copy of this ``hyperx.api.LoadProperty``.
		
		:return: The new copied ``hyperx.api.LoadProperty``.
		'''
		result = self._Entity.Copy()
		thisClass = type(result).__name__
		givenClass = LoadProperty
		for subclass in _all_subclasses(LoadProperty):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None


class DesignLoadSubcase(IdNameEntity):
	def __init__(self, designLoadSubcase: _api.DesignLoadSubcase):
		self._Entity = designLoadSubcase

	@property
	def RunDeckId(self) -> int | None:
		return self._Entity.RunDeckId

	@property
	def IsThermal(self) -> bool | None:
		return self._Entity.IsThermal

	@property
	def IsEditable(self) -> bool | None:
		return self._Entity.IsEditable

	@property
	def Description(self) -> str:
		return self._Entity.Description

	@property
	def ModificationDate(self) -> DateTime | None:
		return self._Entity.ModificationDate

	@property
	def NastranSubcaseId(self) -> int | None:
		return self._Entity.NastranSubcaseId

	@property
	def NastranLoadId(self) -> int | None:
		return self._Entity.NastranLoadId

	@property
	def NastranSpcId(self) -> int | None:
		return self._Entity.NastranSpcId

	@property
	def AbaqusStepName(self) -> str:
		return self._Entity.AbaqusStepName

	@property
	def AbaqusLoadCaseName(self) -> str:
		return self._Entity.AbaqusLoadCaseName

	@property
	def AbaqusStepTime(self) -> float | None:
		return self._Entity.AbaqusStepTime

	@property
	def RunDeckOrder(self) -> int | None:
		return self._Entity.RunDeckOrder

	@property
	def SolutionType(self) -> types.FeaSolutionType | None:
		result = self._Entity.SolutionType
		return types.FeaSolutionType[result.ToString()] if result is not None else None


class DesignLoadSubcaseMultiplier(IdNameEntity):
	def __init__(self, designLoadSubcaseMultiplier: _api.DesignLoadSubcaseMultiplier):
		self._Entity = designLoadSubcaseMultiplier

	@property
	def LimitFactor(self) -> float:
		return self._Entity.LimitFactor

	@property
	def Subcase(self) -> DesignLoadSubcase:
		result = self._Entity.Subcase
		return DesignLoadSubcase(result) if result is not None else None

	@property
	def UltimateFactor(self) -> float:
		return self._Entity.UltimateFactor

	@property
	def Value(self) -> float:
		return self._Entity.Value


class DesignLoadSubcaseTemperature(IdNameEntity):
	def __init__(self, designLoadSubcaseTemperature: _api.DesignLoadSubcaseTemperature):
		self._Entity = designLoadSubcaseTemperature

	@property
	def HasTemperatureSubcase(self) -> bool:
		'''
		If the analysis temperature does not have an associated load set id
		(i.e. the TemperatureChoiceType is equal to Value), the Id will be set to 0
		and this field will be false
		'''
		return self._Entity.HasTemperatureSubcase

	@property
	def Subcase(self) -> DesignLoadSubcase:
		result = self._Entity.Subcase
		return DesignLoadSubcase(result) if result is not None else None

	@property
	def TemperatureChoiceType(self) -> types.TemperatureChoiceType:
		result = self._Entity.TemperatureChoiceType
		return types.TemperatureChoiceType[result.ToString()] if result is not None else None

	@property
	def Value(self) -> float:
		return self._Entity.Value


class DesignLoadSubcaseMultiplierCol(IdNameEntityCol[DesignLoadSubcaseMultiplier]):
	def __init__(self, designLoadSubcaseMultiplierCol: _api.DesignLoadSubcaseMultiplierCol):
		self._Entity = designLoadSubcaseMultiplierCol
		self._CollectedClass = DesignLoadSubcaseMultiplier

	@property
	def DesignLoadSubcaseMultiplierColList(self) -> tuple[DesignLoadSubcaseMultiplier]:
		return tuple([DesignLoadSubcaseMultiplier(designLoadSubcaseMultiplierCol) for designLoadSubcaseMultiplierCol in self._Entity])

	@overload
	def Get(self, name: str) -> DesignLoadSubcaseMultiplier:
		...

	@overload
	def Get(self, id: int) -> DesignLoadSubcaseMultiplier:
		...

	def Get(self, item1 = None) -> DesignLoadSubcaseMultiplier:
		'''
		Overload 1: ``Get(self, name: str) -> DesignLoadSubcaseMultiplier``

		Overload 2: ``Get(self, id: int) -> DesignLoadSubcaseMultiplier``
		'''
		if isinstance(item1, str):
			return DesignLoadSubcaseMultiplier(super().Get(item1))

		if isinstance(item1, int):
			return DesignLoadSubcaseMultiplier(super().Get(item1))

		return DesignLoadSubcaseMultiplier(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.DesignLoadSubcaseMultiplierColList[index]

	def __iter__(self):
		yield from self.DesignLoadSubcaseMultiplierColList

	def __len__(self):
		return len(self.DesignLoadSubcaseMultiplierColList)


class DesignLoad(IdNameEntity):
	def __init__(self, designLoad: _api.DesignLoad):
		self._Entity = designLoad

	@property
	def AnalysisTemperature(self) -> DesignLoadSubcaseTemperature:
		result = self._Entity.AnalysisTemperature
		return DesignLoadSubcaseTemperature(result) if result is not None else None

	@property
	def InitialTemperature(self) -> DesignLoadSubcaseTemperature:
		result = self._Entity.InitialTemperature
		return DesignLoadSubcaseTemperature(result) if result is not None else None

	@property
	def Description(self) -> str:
		return self._Entity.Description

	@property
	def IsActive(self) -> bool:
		return self._Entity.IsActive

	@property
	def IsEditable(self) -> bool:
		return self._Entity.IsEditable

	@property
	def IsVirtual(self) -> bool:
		return self._Entity.IsVirtual

	@property
	def ModificationDate(self) -> DateTime:
		return self._Entity.ModificationDate

	@property
	def SubcaseMultipliers(self) -> DesignLoadSubcaseMultiplierCol:
		result = self._Entity.SubcaseMultipliers
		return DesignLoadSubcaseMultiplierCol(result) if result is not None else None

	@property
	def Types(self) -> list[types.LoadCaseType]:
		'''
		e.g. Static, Fatigue.
		'''
		return [types.LoadCaseType[loadCaseType.ToString()] for loadCaseType in self._Entity.Types]

	@property
	def UID(self) -> Guid:
		return self._Entity.UID

	@IsActive.setter
	def IsActive(self, value: bool) -> None:
		self._Entity.IsActive = value


class JointDesignResult(IdEntity):
	def __init__(self, jointDesignResult: _api.JointDesignResult):
		self._Entity = jointDesignResult


class ZoneDesignResult(IdEntity):
	def __init__(self, zoneDesignResult: _api.ZoneDesignResult):
		self._Entity = zoneDesignResult

	@property
	def VariableParameter(self) -> types.VariableParameter:
		result = self._Entity.VariableParameter
		return types.VariableParameter[result.ToString()] if result is not None else None

	@property
	def Value(self) -> float:
		return self._Entity.Value

	@property
	def MaterialId(self) -> int | None:
		warnings.warn("Use Material instead.", DeprecationWarning, 2)
		return self._Entity.MaterialId

	@property
	def MaterialType(self) -> types.MaterialType | None:
		result = self._Entity.MaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def Material(self) -> str:
		return self._Entity.Material


class Vector3d:
	'''
	Represents a readonly 3D vector.
	'''
	def __init__(self, vector3d: _api.Vector3d):
		self._Entity = vector3d

	def Create_Vector3d(x: float, y: float, z: float):
		return Vector3d(_api.Vector3d(x, y, z))

	@property
	def X(self) -> float:
		return self._Entity.X

	@property
	def Y(self) -> float:
		return self._Entity.Y

	@property
	def Z(self) -> float:
		return self._Entity.Z

	@overload
	def Equals(self, other) -> bool:
		...

	@overload
	def Equals(self, obj: object) -> bool:
		...

	def Equals(self, item1 = None) -> bool:
		'''
		Overload 1: ``Equals(self, other) -> bool``

		Overload 2: ``Equals(self, obj: object) -> bool``
		'''
		if isinstance(item1, Vector3d):
			return self._Entity.Equals(item1._Entity)

		if isinstance(item1, object):
			return self._Entity.Equals(item1)

		return self._Entity.Equals(item1._Entity)

	def __eq__(self, other):
		return self.Equals(other)

	def __ne__(self, other):
		return not self.Equals(other)

	def __hash__(self) -> int:
		return self._Entity.GetHashCode()


class DiscreteField(IdNameEntityRenameable):
	'''
	Represents a table of discrete field data.
	'''
	def __init__(self, discreteField: _api.DiscreteField):
		self._Entity = discreteField

	@property
	def Columns(self) -> dict[int, str]:
		'''
		Lookup of Columns by Id, Name.
		'''
		columnsDict = {}
		for kvp in self._Entity.Columns:
			columnsDict[int(kvp.Key)] = str(kvp.Value)

		return columnsDict

	@property
	def ColumnCount(self) -> int:
		return self._Entity.ColumnCount

	@property
	def DataType(self) -> types.DiscreteFieldDataType:
		result = self._Entity.DataType
		return types.DiscreteFieldDataType[result.ToString()] if result is not None else None

	@property
	def PhysicalEntityType(self) -> types.DiscreteFieldPhysicalEntityType:
		result = self._Entity.PhysicalEntityType
		return types.DiscreteFieldPhysicalEntityType[result.ToString()] if result is not None else None

	@property
	def PointIds(self) -> list[Vector3d]:
		'''
		Get a list of the points for a Discrete Field (point-based only).
		'''
		return [Vector3d(vector3d) for vector3d in self._Entity.PointIds]

	@property
	def RowCount(self) -> int:
		return self._Entity.RowCount

	@property
	def RowIds(self) -> list[int]:
		'''
		Get a list of the entity IDs for a Discrete Field (not point-based).
		'''
		return [int32 for int32 in self._Entity.RowIds]

	def AddColumn(self, name: str) -> int:
		'''
		Create a new column with the given name. Returns the Id of the newly created column
		Not valid for discrete fields containing vector data.
		'''
		return self._Entity.AddColumn(name)

	def AddPointRow(self, pointId: Vector3d) -> None:
		'''
		Create an empty row in a point-based table.
		'''
		return self._Entity.AddPointRow(pointId._Entity)

	@overload
	def ReadNumericCell(self, entityId: int, columnId: int) -> float | None:
		'''
		Valid only for non-point-based discrete fields containing scalar or vector data.
		'''
		...

	@overload
	def ReadNumericCell(self, pointId: Vector3d, columnId: int) -> float | None:
		'''
		Valid only for point-based discrete fields containing scalar or vector data.
		'''
		...

	@overload
	def ReadStringCell(self, entityId: int, columnId: int) -> str:
		'''
		Valid only for non point-based discrete fields containing string-based data.
		'''
		...

	@overload
	def ReadStringCell(self, pointId: Vector3d, columnId: int) -> str:
		'''
		Valid only for point-based discrete fields containing string-based data.
		'''
		...

	def SetColumnName(self, columnId: int, name: str) -> None:
		return self._Entity.SetColumnName(columnId, name)

	@overload
	def SetNumericValue(self, entityId: int, columnId: int, value: float) -> None:
		...

	@overload
	def SetNumericValues(self, valuesByEntityId: dict[int, tuple[float]]) -> None:
		'''
		Set real values for entity based discrete fields in bulk.
		If an entity is included in the lookup, all values for that entity must be set in the collection of values.
		If an existing entity is included in the lookup with no values, it will be removed from the dataset.
		
		:raises ``System.InvalidOperationException``:
		'''
		...

	@overload
	def SetNumericValue(self, pointId: Vector3d, columnId: int, value: float) -> None:
		...

	@overload
	def SetNumericValues(self, valuesByPoint: dict[Vector3d, tuple[float]]) -> None:
		'''
		Set real values for point based discrete fields in bulk.
		If a point is included in the lookup, all values for that point must be set in the collection of values.
		If an existing point is included in the lookup with no values, it will be removed from the dataset.
		
		:raises ``System.InvalidOperationException``:
		'''
		...

	@overload
	def SetStringValue(self, entityId: int, columnId: int, value: str) -> None:
		...

	@overload
	def SetStringValues(self, valuesByEntityId: dict[int, tuple[str]]) -> None:
		'''
		Set string values for entity based discrete fields in bulk.
		If an entity is included in the lookup, all strings for that entity must be set in the collection of strings.
		If an existing entity is included in the lookup with no strings, it will be removed from the dataset.
		
		:raises ``System.InvalidOperationException``:
		'''
		...

	@overload
	def SetStringValue(self, pointId: Vector3d, columnId: int, value: str) -> None:
		...

	@overload
	def SetStringValues(self, valuesByPoint: dict[Vector3d, tuple[str]]) -> None:
		'''
		Set string values for point based discrete fields in bulk.
		If a point is included in the lookup, all strings for that point must be set in the collection of strings.
		If an existing point is included in the lookup with no strings, it will be removed from the dataset.
		
		:raises ``System.InvalidOperationException``:
		'''
		...

	def DeleteAllRows(self) -> None:
		'''
		Delete all rows for this discrete field.
		'''
		return self._Entity.DeleteAllRows()

	def DeleteColumn(self, columnId: int) -> None:
		'''
		Delete a specified column for this discrete field. Columns are 1-indexed.
		Not valid for discrete fields containing vector data.
		'''
		return self._Entity.DeleteColumn(columnId)

	def DeletePointRow(self, pointId: Vector3d) -> None:
		'''
		Delete a specific row for a point-based table.
		'''
		return self._Entity.DeletePointRow(pointId._Entity)

	def DeleteRow(self, entityId: int) -> None:
		'''
		Delete a specific row for a non-point-based table.
		'''
		return self._Entity.DeleteRow(entityId)

	def DeleteRowsAndColumns(self) -> None:
		'''
		Delete all rows and columns for this discrete field.
		Not valid for discrete fields containing vector data.
		'''
		return self._Entity.DeleteRowsAndColumns()

	def ReadNumericCell(self, item1 = None, item2 = None) -> float | None:
		'''
		Overload 1: ``ReadNumericCell(self, entityId: int, columnId: int) -> float | None``

		Valid only for non-point-based discrete fields containing scalar or vector data.

		Overload 2: ``ReadNumericCell(self, pointId: Vector3d, columnId: int) -> float | None``

		Valid only for point-based discrete fields containing scalar or vector data.
		'''
		if isinstance(item1, int) and isinstance(item2, int):
			return self._Entity.ReadNumericCell(item1, item2)

		if isinstance(item1, Vector3d) and isinstance(item2, int):
			return self._Entity.ReadNumericCell(item1._Entity, item2)

		return self._Entity.ReadNumericCell(item1, item2)

	def ReadStringCell(self, item1 = None, item2 = None) -> str:
		'''
		Overload 1: ``ReadStringCell(self, entityId: int, columnId: int) -> str``

		Valid only for non point-based discrete fields containing string-based data.

		Overload 2: ``ReadStringCell(self, pointId: Vector3d, columnId: int) -> str``

		Valid only for point-based discrete fields containing string-based data.
		'''
		if isinstance(item1, int) and isinstance(item2, int):
			return self._Entity.ReadStringCell(item1, item2)

		if isinstance(item1, Vector3d) and isinstance(item2, int):
			return self._Entity.ReadStringCell(item1._Entity, item2)

		return self._Entity.ReadStringCell(item1, item2)

	def SetNumericValue(self, item1 = None, item2 = None, item3 = None) -> None:
		'''
		Overload 1: ``SetNumericValue(self, entityId: int, columnId: int, value: float) -> None``

		Overload 2: ``SetNumericValue(self, pointId: Vector3d, columnId: int, value: float) -> None``
		'''
		if isinstance(item1, int) and isinstance(item2, int) and (isinstance(item3, float) or isinstance(item3, int)):
			return self._Entity.SetNumericValue(item1, item2, item3)

		if isinstance(item1, Vector3d) and isinstance(item2, int) and (isinstance(item3, float) or isinstance(item3, int)):
			return self._Entity.SetNumericValue(item1._Entity, item2, item3)

		return self._Entity.SetNumericValue(item1, item2, item3)

	def SetNumericValues(self, item1 = None) -> None:
		'''
		Overload 1: ``SetNumericValues(self, valuesByEntityId: dict[int, tuple[float]]) -> None``

		Set real values for entity based discrete fields in bulk.
		If an entity is included in the lookup, all values for that entity must be set in the collection of values.
		If an existing entity is included in the lookup with no values, it will be removed from the dataset.
		
		:raises ``System.InvalidOperationException``:

		Overload 2: ``SetNumericValues(self, valuesByPoint: dict[Vector3d, tuple[float]]) -> None``

		Set real values for point based discrete fields in bulk.
		If a point is included in the lookup, all values for that point must be set in the collection of values.
		If an existing point is included in the lookup with no values, it will be removed from the dataset.
		
		:raises ``System.InvalidOperationException``:
		'''
		if isinstance(item1, dict) and item1 and isinstance(list(item1.keys())[0], int) and (isinstance(list(item1.values())[0], tuple) or isinstance(list(item1.values())[0], list) or isinstance(list(item1.values())[0], set)) and list(item1.values())[0] and any((isinstance(x, float) or x is None or isinstance(x, int)) for x in list(item1.values())[0]):
			valuesByEntityIdDict = Dictionary[int, IEnumerable[Nullable[Double]]]()
			for kvp in item1:
				dictValue = item1[kvp]
				dictValueList = List[Nullable[Double]]()
				if dictValue is not None:
					for x in dictValue:
						dictValueList.Add(x)
				dictValueEnumerable = IEnumerable(dictValueList)
				valuesByEntityIdDict.Add(kvp, dictValueEnumerable)
			return self._Entity.SetNumericValues(valuesByEntityIdDict)

		if isinstance(item1, dict) and item1 and isinstance(list(item1.keys())[0], Vector3d) and (isinstance(list(item1.values())[0], tuple) or isinstance(list(item1.values())[0], list) or isinstance(list(item1.values())[0], set)) and list(item1.values())[0] and any((isinstance(x, float) or x is None or isinstance(x, int)) for x in list(item1.values())[0]):
			valuesByPointDict = Dictionary[_api.Vector3d, IEnumerable[Nullable[Double]]]()
			for kvp in item1:
				dictValue = item1[kvp]
				dictValueList = List[Nullable[Double]]()
				if dictValue is not None:
					for x in dictValue:
						dictValueList.Add(x)
				dictValueEnumerable = IEnumerable(dictValueList)
				valuesByPointDict.Add(kvp._Entity, dictValueEnumerable)
			return self._Entity.SetNumericValues(valuesByPointDict)

		return self._Entity.SetNumericValues(item1)

	def SetStringValue(self, item1 = None, item2 = None, item3 = None) -> None:
		'''
		Overload 1: ``SetStringValue(self, entityId: int, columnId: int, value: str) -> None``

		Overload 2: ``SetStringValue(self, pointId: Vector3d, columnId: int, value: str) -> None``
		'''
		if isinstance(item1, int) and isinstance(item2, int) and isinstance(item3, str):
			return self._Entity.SetStringValue(item1, item2, item3)

		if isinstance(item1, Vector3d) and isinstance(item2, int) and isinstance(item3, str):
			return self._Entity.SetStringValue(item1._Entity, item2, item3)

		return self._Entity.SetStringValue(item1, item2, item3)

	def SetStringValues(self, item1 = None) -> None:
		'''
		Overload 1: ``SetStringValues(self, valuesByEntityId: dict[int, tuple[str]]) -> None``

		Set string values for entity based discrete fields in bulk.
		If an entity is included in the lookup, all strings for that entity must be set in the collection of strings.
		If an existing entity is included in the lookup with no strings, it will be removed from the dataset.
		
		:raises ``System.InvalidOperationException``:

		Overload 2: ``SetStringValues(self, valuesByPoint: dict[Vector3d, tuple[str]]) -> None``

		Set string values for point based discrete fields in bulk.
		If a point is included in the lookup, all strings for that point must be set in the collection of strings.
		If an existing point is included in the lookup with no strings, it will be removed from the dataset.
		
		:raises ``System.InvalidOperationException``:
		'''
		if isinstance(item1, dict) and item1 and isinstance(list(item1.keys())[0], int) and (isinstance(list(item1.values())[0], tuple) or isinstance(list(item1.values())[0], list) or isinstance(list(item1.values())[0], set)) and list(item1.values())[0] and any(isinstance(x, str) for x in list(item1.values())[0]):
			valuesByEntityIdDict = Dictionary[int, IEnumerable[String]]()
			for kvp in item1:
				dictValue = item1[kvp]
				dictValueList = List[str]()
				if dictValue is not None:
					for x in dictValue:
						if x is not None:
							dictValueList.Add(x)
				dictValueEnumerable = IEnumerable(dictValueList)
				valuesByEntityIdDict.Add(kvp, dictValueEnumerable)
			return self._Entity.SetStringValues(valuesByEntityIdDict)

		if isinstance(item1, dict) and item1 and isinstance(list(item1.keys())[0], Vector3d) and (isinstance(list(item1.values())[0], tuple) or isinstance(list(item1.values())[0], list) or isinstance(list(item1.values())[0], set)) and list(item1.values())[0] and any(isinstance(x, str) for x in list(item1.values())[0]):
			valuesByPointDict = Dictionary[_api.Vector3d, IEnumerable[String]]()
			for kvp in item1:
				dictValue = item1[kvp]
				dictValueList = List[str]()
				if dictValue is not None:
					for x in dictValue:
						if x is not None:
							dictValueList.Add(x)
				dictValueEnumerable = IEnumerable(dictValueList)
				valuesByPointDict.Add(kvp._Entity, dictValueEnumerable)
			return self._Entity.SetStringValues(valuesByPointDict)

		return self._Entity.SetStringValues(item1)


class Node(IdEntity):
	def __init__(self, node: _api.Node):
		self._Entity = node

	@property
	def X(self) -> float:
		return self._Entity.X

	@property
	def Y(self) -> float:
		return self._Entity.Y

	@property
	def Z(self) -> float:
		return self._Entity.Z


class Centroid:
	def __init__(self, centroid: _api.Centroid):
		self._Entity = centroid

	@property
	def X(self) -> float:
		return self._Entity.X

	@property
	def Y(self) -> float:
		return self._Entity.Y

	@property
	def Z(self) -> float:
		return self._Entity.Z


class Element(IdEntity):

	_Centroid = Centroid
	def __init__(self, element: _api.Element):
		self._Entity = element

	@property
	def MarginOfSafety(self) -> float | None:
		return self._Entity.MarginOfSafety
	@property
	def Centroid(self) -> _Centroid:
		result = self._Entity.Centroid
		return Centroid(result) if result is not None else None

	@property
	def Nodes(self) -> list[Node]:
		return [Node(node) for node in self._Entity.Nodes]


class PlateElement(Element):
	def __init__(self, plateElement: _api.PlateElement):
		self._Entity = plateElement

	@property
	def MaterialDirection(self) -> Vector3d:
		'''
		Global material direction for plate elements
		If setting more than one ``hyperx.api.PlateElement.MaterialDirection``, use ``hyperx.api.PlateElementBulkUpdater`` to avoid major performance hits.
		'''
		result = self._Entity.MaterialDirection
		return Vector3d(result) if result is not None else None

	@MaterialDirection.setter
	def MaterialDirection(self, value: Vector3d) -> None:
		self._Entity.MaterialDirection = value._Entity


class FailureModeCategory(IdNameEntity):
	def __init__(self, failureModeCategory: _api.FailureModeCategory):
		self._Entity = failureModeCategory

	@property
	def PackageId(self) -> int | None:
		return self._Entity.PackageId


class Folder(IdNameEntity):
	def __init__(self, folder: _api.Folder):
		self._Entity = folder

	@property
	def ParentFolder(self) -> Folder:
		result = self._Entity.ParentFolder
		return Folder(result) if result is not None else None

	@property
	def ChildFolders(self) -> FolderCol:
		result = self._Entity.ChildFolders
		return FolderCol(result) if result is not None else None

	@property
	def Items(self) -> list[IdNameEntity]:
		items = []
		subclasses = {x.__name__: x for x in _all_subclasses(IdNameEntity)}
		for idNameEntity in self._Entity.Items:
			if type(idNameEntity).__name__ in subclasses.keys():
				thisType = subclasses[type(idNameEntity).__name__]
				items.append(thisType(idNameEntity))
			else:
				raise Exception(f"Could not wrap item in Items. This should not happen.")
		return items

	def AddItem(self, item: IdNameEntity) -> None:
		return self._Entity.AddItem(item._Entity)

	def AddItems(self, items: tuple[IdNameEntity]) -> None:
		itemsList = List[type(items[0]._Entity)]()
		if items is not None:
			for x in items:
				if x is not None:
					itemsList.Add(x._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return self._Entity.AddItems(itemsEnumerable)

	def RemoveItem(self, item: IdNameEntity) -> None:
		return self._Entity.RemoveItem(item._Entity)

	def RemoveItems(self, items: tuple[IdNameEntity]) -> None:
		itemsList = List[type(items[0]._Entity)]()
		if items is not None:
			for x in items:
				if x is not None:
					itemsList.Add(x._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return self._Entity.RemoveItems(itemsEnumerable)


class EntityWithAssignableProperties(IdNameEntityRenameable):
	def __init__(self, entityWithAssignableProperties: _api.EntityWithAssignableProperties):
		self._Entity = entityWithAssignableProperties

	@property
	def AssignedAnalysisProperty(self) -> AnalysisProperty:
		'''
		Get the analysis property assigned to this Entity. Returns ``None`` if none is assigned.
		'''
		result = self._Entity.AssignedAnalysisProperty
		return AnalysisProperty(result) if result is not None else None

	@property
	def AssignedDesignProperty(self) -> DesignProperty:
		'''
		Get the design property assigned to this Entity. Returns ``None`` if none is assigned.
		'''
		result = self._Entity.AssignedDesignProperty
		thisClass = type(result).__name__
		givenClass = DesignProperty
		for subclass in _all_subclasses(DesignProperty):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@property
	def AssignedLoadProperty(self) -> LoadProperty:
		'''
		Get the load property assigned to this Entity. Returns ``None`` if none is assigned.
		'''
		result = self._Entity.AssignedLoadProperty
		thisClass = type(result).__name__
		givenClass = LoadProperty
		for subclass in _all_subclasses(LoadProperty):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def AssignAnalysisProperty(self, id: int) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self._Entity.AssignAnalysisProperty(id).ToString()]

	def AssignDesignProperty(self, id: int) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self._Entity.AssignDesignProperty(id).ToString()]

	def AssignLoadProperty(self, id: int) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self._Entity.AssignLoadProperty(id).ToString()]

	def AssignProperty(self, property: AssignableProperty) -> PropertyAssignmentStatus:
		'''
		Assign a Property to this entity.
		'''
		return PropertyAssignmentStatus[self._Entity.AssignProperty(property._Entity).ToString()]


class AnalysisResultCol(Generic[T]):
	def __init__(self, analysisResultCol: _api.AnalysisResultCol):
		self._Entity = analysisResultCol

	@property
	def AnalysisResultColList(self) -> tuple[AnalysisResult]:
		analysisResultColList = []
		subclasses = {x.__name__: x for x in _all_subclasses(AnalysisResult)}
		for analysisResultCol in self._Entity:
			if type(analysisResultCol).__name__ in subclasses.keys():
				thisType = subclasses[type(analysisResultCol).__name__]
				analysisResultColList.append(thisType(analysisResultCol))
			else:
				raise Exception(f"Could not wrap item in AnalysisResultCol. This should not happen.")
		return tuple(analysisResultColList)

	def Count(self) -> int:
		return self._Entity.Count()

	def __getitem__(self, index: int):
		return self.AnalysisResultColList[index]

	def __iter__(self):
		yield from self.AnalysisResultColList

	def __len__(self):
		return len(self.AnalysisResultColList)


class ZoneJointEntity(EntityWithAssignableProperties):
	'''
	Abstract base for a Zone or Joint.
	'''
	def __init__(self, zoneJointEntity: _api.ZoneJointEntity):
		self._Entity = zoneJointEntity

	@abstractmethod
	def GetMinimumMargin(self) -> Margin:
		return Margin(self._Entity.GetMinimumMargin())

	@abstractmethod
	def GetControllingResult(self) -> AnalysisResult:
		result = self._Entity.GetControllingResult()
		thisClass = type(result).__name__
		givenClass = AnalysisResult
		for subclass in _all_subclasses(AnalysisResult):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@abstractmethod
	def GetAllResults(self) -> AnalysisResultCol:
		'''
		Obselete. Use ``hyperx.api.ZoneJointEntity.GetControllingResultsPerCriterion`` instead.
		'''
		return AnalysisResultCol(self._Entity.GetAllResults())

	@abstractmethod
	def GetControllingResultsPerCriterion(self) -> AnalysisResultCol:
		return AnalysisResultCol(self._Entity.GetControllingResultsPerCriterion())


class JointDesignResultCol(IdEntityCol[JointDesignResult]):
	def __init__(self, jointDesignResultCol: _api.JointDesignResultCol):
		self._Entity = jointDesignResultCol
		self._CollectedClass = JointDesignResult

	@property
	def JointDesignResultColList(self) -> tuple[JointDesignResult]:
		jointDesignResultColList = []
		subclasses = {x.__name__: x for x in _all_subclasses(JointDesignResult)}
		for jointDesignResultCol in self._Entity:
			if type(jointDesignResultCol).__name__ in subclasses.keys():
				thisType = subclasses[type(jointDesignResultCol).__name__]
				jointDesignResultColList.append(thisType(jointDesignResultCol))
			else:
				raise Exception(f"Could not wrap item in JointDesignResultCol. This should not happen.")
		return tuple(jointDesignResultColList)

	@overload
	def Get(self, jointSelectionId: types.JointSelectionId) -> JointDesignResult:
		'''
		Get a JointSizingResult for a JointSelectionId
		
		:return: Null if the item is not found or the item is a JointRangeSizingResult item
		'''
		...

	@overload
	def Get(self, jointRangeId: types.JointRangeId) -> JointDesignResult:
		'''
		Get a JointSizingResult for a JointRangeId
		
		:return: Null if the item is not found or the item is a JointSelectionSizingResult item
		'''
		...

	@overload
	def Get(self, id: int) -> JointDesignResult:
		...

	def Get(self, item1 = None) -> JointDesignResult:
		'''
		Overload 1: ``Get(self, jointSelectionId: types.JointSelectionId) -> JointDesignResult``

		Get a JointSizingResult for a JointSelectionId
		
		:return: Null if the item is not found or the item is a JointRangeSizingResult item

		Overload 2: ``Get(self, jointRangeId: types.JointRangeId) -> JointDesignResult``

		Get a JointSizingResult for a JointRangeId
		
		:return: Null if the item is not found or the item is a JointSelectionSizingResult item

		Overload 3: ``Get(self, id: int) -> JointDesignResult``
		'''
		if isinstance(item1, types.JointSelectionId):
			result = self._Entity.Get(_types.JointSelectionId(types.GetEnumValue(item1.value)))
			thisClass = type(result).__name__
			givenClass = JointDesignResult
			for subclass in _all_subclasses(JointDesignResult):
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, types.JointRangeId):
			result = self._Entity.Get(_types.JointRangeId(types.GetEnumValue(item1.value)))
			thisClass = type(result).__name__
			givenClass = JointDesignResult
			for subclass in _all_subclasses(JointDesignResult):
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, int):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = JointDesignResult
			for subclass in _all_subclasses(JointDesignResult):
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		result = self._Entity.Get(_types.JointSelectionId(types.GetEnumValue(item1.value)))
		thisClass = type(result).__name__
		givenClass = JointDesignResult
		for subclass in _all_subclasses(JointDesignResult):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def __getitem__(self, index: int):
		return self.JointDesignResultColList[index]

	def __iter__(self):
		yield from self.JointDesignResultColList

	def __len__(self):
		return len(self.JointDesignResultColList)


class Joint(ZoneJointEntity):
	def __init__(self, joint: _api.Joint):
		self._Entity = joint

	@property
	def JointRangeSizingResults(self) -> JointDesignResultCol:
		result = self._Entity.JointRangeSizingResults
		return JointDesignResultCol(result) if result is not None else None

	@property
	def JointSelectionSizingResults(self) -> JointDesignResultCol:
		result = self._Entity.JointSelectionSizingResults
		return JointDesignResultCol(result) if result is not None else None

	def GetAllResults(self) -> AnalysisResultCol:
		return AnalysisResultCol(self._Entity.GetAllResults())

	def GetControllingResultsPerCriterion(self) -> AnalysisResultCol:
		return AnalysisResultCol(self._Entity.GetControllingResultsPerCriterion())

	def GetControllingResult(self) -> AnalysisResult:
		result = self._Entity.GetControllingResult()
		thisClass = type(result).__name__
		givenClass = AnalysisResult
		for subclass in _all_subclasses(AnalysisResult):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def GetMinimumMargin(self) -> Margin:
		return Margin(self._Entity.GetMinimumMargin())


class DesignLoadOverride(IdEntity):
	def __init__(self, designLoadOverride: _api.DesignLoadOverride):
		self._Entity = designLoadOverride

	@property
	def LimitFactor(self) -> float | None:
		return self._Entity.LimitFactor

	@property
	def UltimateFactor(self) -> float | None:
		return self._Entity.UltimateFactor

	@property
	def HelpFactor(self) -> float | None:
		return self._Entity.HelpFactor

	@property
	def HurtFactor(self) -> float | None:
		return self._Entity.HurtFactor

	@property
	def Temperature(self) -> float | None:
		return self._Entity.Temperature

	@LimitFactor.setter
	def LimitFactor(self, value: float | None) -> None:
		self._Entity.LimitFactor = value

	@UltimateFactor.setter
	def UltimateFactor(self, value: float | None) -> None:
		self._Entity.UltimateFactor = value

	@HelpFactor.setter
	def HelpFactor(self, value: float | None) -> None:
		self._Entity.HelpFactor = value

	@HurtFactor.setter
	def HurtFactor(self, value: float | None) -> None:
		self._Entity.HurtFactor = value

	@Temperature.setter
	def Temperature(self, value: float | None) -> None:
		self._Entity.Temperature = value


class ZoneDesignResultCol(IdEntityCol[ZoneDesignResult]):
	def __init__(self, zoneDesignResultCol: _api.ZoneDesignResultCol):
		self._Entity = zoneDesignResultCol
		self._CollectedClass = ZoneDesignResult

	@property
	def ZoneDesignResultColList(self) -> tuple[ZoneDesignResult]:
		return tuple([ZoneDesignResult(zoneDesignResultCol) for zoneDesignResultCol in self._Entity])

	@property
	def SelectedCandidate(self) -> int:
		return self._Entity.SelectedCandidate

	@property
	def Weight(self) -> float:
		return self._Entity.Weight

	@overload
	def Get(self, parameterId: types.VariableParameter) -> ZoneDesignResult:
		...

	@overload
	def Get(self, id: int) -> ZoneDesignResult:
		...

	def Get(self, item1 = None) -> ZoneDesignResult:
		'''
		Overload 1: ``Get(self, parameterId: types.VariableParameter) -> ZoneDesignResult``

		Overload 2: ``Get(self, id: int) -> ZoneDesignResult``
		'''
		if isinstance(item1, types.VariableParameter):
			return ZoneDesignResult(self._Entity.Get(_types.VariableParameter(types.GetEnumValue(item1.value))))

		if isinstance(item1, int):
			return ZoneDesignResult(super().Get(item1))

		return ZoneDesignResult(self._Entity.Get(_types.VariableParameter(types.GetEnumValue(item1.value))))

	def __getitem__(self, index: int):
		return self.ZoneDesignResultColList[index]

	def __iter__(self):
		yield from self.ZoneDesignResultColList

	def __len__(self):
		return len(self.ZoneDesignResultColList)


class ZoneBase(ZoneJointEntity):
	'''
	Abstract for regular Zones and Panel Segments.
	'''

	_Centroid = Centroid
	def __init__(self, zoneBase: _api.ZoneBase):
		self._Entity = zoneBase
	@property
	def Centroid(self) -> _Centroid:
		result = self._Entity.Centroid
		return Centroid(result) if result is not None else None

	@property
	def Id(self) -> int:
		'''
		Unlike most entities with IDs, the ID of a Zone can be manually set with the RenumberZone(id) method.
		'''
		return self._Entity.Id

	@property
	def Weight(self) -> float | None:
		return self._Entity.Weight

	@property
	def IncludedDesignLoads(self) -> tuple[str]:
		return tuple([string for string in self._Entity.IncludedDesignLoads])

	@property
	def DesignLoadOverrides(self) -> dict[str, DesignLoadOverride]:
		'''
		Design load overrides keyed by ``hyperx.api.DesignLoad`` name.
		'''
		designLoadOverridesDict = {}
		for kvp in self._Entity.DesignLoadOverrides:
			designLoadOverridesDict[str(kvp.Key)] = DesignLoadOverride(kvp.Value)

		return designLoadOverridesDict

	@property
	def NonOptimumFactor(self) -> float:
		return self._Entity.NonOptimumFactor

	@property
	def AddedWeight(self) -> float:
		'''
		Beam Units: English = lb/ft | Standard = kg/m.
		Panel Units: English = lb/ft² | Standard = kg/m².
		'''
		return self._Entity.AddedWeight

	@property
	def SuperimposePanel(self) -> bool:
		return self._Entity.SuperimposePanel

	@property
	def BucklingImperfection(self) -> float:
		return self._Entity.BucklingImperfection

	@property
	def IsBeamColumn(self) -> bool:
		return self._Entity.IsBeamColumn

	@property
	def SuperimposeBoundaryCondition(self) -> int:
		return self._Entity.SuperimposeBoundaryCondition

	@property
	def IsZeroOutFeaMoments(self) -> bool:
		return self._Entity.IsZeroOutFeaMoments

	@property
	def IsZeroOutFeaTransverseShears(self) -> bool:
		return self._Entity.IsZeroOutFeaTransverseShears

	@property
	def MechanicalLimit(self) -> float:
		return self._Entity.MechanicalLimit

	@property
	def MechanicalUltimate(self) -> float:
		return self._Entity.MechanicalUltimate

	@property
	def ThermalHelp(self) -> float:
		return self._Entity.ThermalHelp

	@property
	def ThermalHurt(self) -> float:
		return self._Entity.ThermalHurt

	@property
	def FatigueKTSkin(self) -> float:
		return self._Entity.FatigueKTSkin

	@property
	def FatigueKTStiff(self) -> float:
		return self._Entity.FatigueKTStiff

	@property
	def XSpan(self) -> float:
		'''
		Units: English = in | Standard = mm.
		'''
		return self._Entity.XSpan

	@property
	def EARequired(self) -> float | None:
		'''
		Units: English = lb | Standard = N.
		'''
		return self._Entity.EARequired

	@property
	def EI1Required(self) -> float | None:
		'''
		Units: English = lb/in² | Standard = N/m².
		'''
		return self._Entity.EI1Required

	@property
	def EI2Required(self) -> float | None:
		'''
		Units: English = lb/in² | Standard = N/m².
		'''
		return self._Entity.EI2Required

	@property
	def GJRequired(self) -> float | None:
		'''
		Units: English = lb/in² | Standard = N/m².
		'''
		return self._Entity.GJRequired

	@property
	def EAAuto(self) -> float | None:
		'''
		Units: English = lb | Standard = N.
		'''
		return self._Entity.EAAuto

	@property
	def EI1Auto(self) -> float | None:
		'''
		Units: English = lb/in² | Standard = N/m².
		'''
		return self._Entity.EI1Auto

	@property
	def EI2Auto(self) -> float | None:
		'''
		Units: English = lb/in² | Standard = N/m².
		'''
		return self._Entity.EI2Auto

	@property
	def GJAuto(self) -> float | None:
		'''
		Units: English = lb/in² | Standard = N/m².
		'''
		return self._Entity.GJAuto

	@property
	def Ex(self) -> float | None:
		'''
		Units: English = µin/in | Standard = µm/m.
		'''
		return self._Entity.Ex

	@property
	def Dmid(self) -> float | None:
		'''
		Units: English = in | Standard = mm.
		'''
		return self._Entity.Dmid

	@IncludedDesignLoads.setter
	def IncludedDesignLoads(self, value: tuple[str]) -> None:
		valueList = List[str]()
		if value is not None:
			for x in value:
				if x is not None:
					valueList.Add(x)
		valueEnumerable = IEnumerable(valueList)
		self._Entity.IncludedDesignLoads = valueEnumerable

	def IncludeAllDesignLoads(self) -> None:
		'''
		Convenience method for including all design loads in analysis, in the event any have been previously excluded via design load overrides.
		'''
		return self._Entity.IncludeAllDesignLoads()

	def GetObjectName(self, objectId: types.FamilyObjectUID) -> str:
		return self._Entity.GetObjectName(_types.FamilyObjectUID(types.GetEnumValue(objectId.value)))

	def GetConceptName(self) -> str:
		return self._Entity.GetConceptName()

	def GetZoneDesignResults(self, solutionId: int = 1) -> ZoneDesignResultCol:
		'''
		Returns a collection of Zone Design Results for a Solution Id (default 1)
		'''
		return ZoneDesignResultCol(self._Entity.GetZoneDesignResults(solutionId))

	def RenumberZone(self, newId: int) -> ZoneIdUpdateStatus:
		'''
		Attempt to update a zone's ID.
		'''
		return ZoneIdUpdateStatus[self._Entity.RenumberZone(newId).ToString()]

	def GetResults(self) -> AnalysisResultCol:
		'''
		Get all analysis results for this zone.
		Analysis details must be available to get results.
		If analysis details are unavailable, use ``hyperx.api.ZoneBase.GetControllingResultsPerCriterion`` or rerun analysis to populate them.
		'''
		return AnalysisResultCol(self._Entity.GetResults())

	def GetAllResults(self) -> AnalysisResultCol:
		return AnalysisResultCol(self._Entity.GetAllResults())

	def GetControllingResultsPerCriterion(self) -> AnalysisResultCol:
		return AnalysisResultCol(self._Entity.GetControllingResultsPerCriterion())

	def GetControllingResult(self) -> AnalysisResult:
		result = self._Entity.GetControllingResult()
		thisClass = type(result).__name__
		givenClass = AnalysisResult
		for subclass in _all_subclasses(AnalysisResult):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def GetMinimumMargin(self) -> Margin:
		return Margin(self._Entity.GetMinimumMargin())

	@NonOptimumFactor.setter
	def NonOptimumFactor(self, value: float) -> None:
		self._Entity.NonOptimumFactor = value

	@AddedWeight.setter
	def AddedWeight(self, value: float) -> None:
		self._Entity.AddedWeight = value

	@SuperimposePanel.setter
	def SuperimposePanel(self, value: bool) -> None:
		self._Entity.SuperimposePanel = value

	@BucklingImperfection.setter
	def BucklingImperfection(self, value: float) -> None:
		self._Entity.BucklingImperfection = value

	@IsBeamColumn.setter
	def IsBeamColumn(self, value: bool) -> None:
		self._Entity.IsBeamColumn = value

	@SuperimposeBoundaryCondition.setter
	def SuperimposeBoundaryCondition(self, value: int) -> None:
		self._Entity.SuperimposeBoundaryCondition = value

	@IsZeroOutFeaMoments.setter
	def IsZeroOutFeaMoments(self, value: bool) -> None:
		self._Entity.IsZeroOutFeaMoments = value

	@IsZeroOutFeaTransverseShears.setter
	def IsZeroOutFeaTransverseShears(self, value: bool) -> None:
		self._Entity.IsZeroOutFeaTransverseShears = value

	@MechanicalLimit.setter
	def MechanicalLimit(self, value: float) -> None:
		self._Entity.MechanicalLimit = value

	@MechanicalUltimate.setter
	def MechanicalUltimate(self, value: float) -> None:
		self._Entity.MechanicalUltimate = value

	@ThermalHelp.setter
	def ThermalHelp(self, value: float) -> None:
		self._Entity.ThermalHelp = value

	@ThermalHurt.setter
	def ThermalHurt(self, value: float) -> None:
		self._Entity.ThermalHurt = value

	@FatigueKTSkin.setter
	def FatigueKTSkin(self, value: float) -> None:
		self._Entity.FatigueKTSkin = value

	@FatigueKTStiff.setter
	def FatigueKTStiff(self, value: float) -> None:
		self._Entity.FatigueKTStiff = value

	@XSpan.setter
	def XSpan(self, value: float) -> None:
		self._Entity.XSpan = value

	@EARequired.setter
	def EARequired(self, value: float | None) -> None:
		self._Entity.EARequired = value

	@EI1Required.setter
	def EI1Required(self, value: float | None) -> None:
		self._Entity.EI1Required = value

	@EI2Required.setter
	def EI2Required(self, value: float | None) -> None:
		self._Entity.EI2Required = value

	@GJRequired.setter
	def GJRequired(self, value: float | None) -> None:
		self._Entity.GJRequired = value

	@Ex.setter
	def Ex(self, value: float | None) -> None:
		self._Entity.Ex = value

	@Dmid.setter
	def Dmid(self, value: float | None) -> None:
		self._Entity.Dmid = value


class ElementCol(IdEntityCol[Element]):
	def __init__(self, elementCol: _api.ElementCol):
		self._Entity = elementCol
		self._CollectedClass = Element

	@property
	def ElementColList(self) -> tuple[Element]:
		return tuple([Element(elementCol) for elementCol in self._Entity])

	@property
	def PlateIds(self) -> tuple[int]:
		return tuple([int32 for int32 in self._Entity.PlateIds])

	@property
	def PlateElements(self) -> tuple[PlateElement]:
		return tuple([PlateElement(plateElement) for plateElement in self._Entity.PlateElements])

	def __getitem__(self, index: int):
		return self.ElementColList[index]

	def __iter__(self):
		yield from self.ElementColList

	def __len__(self):
		return len(self.ElementColList)


class PanelSegment(ZoneBase):
	def __init__(self, panelSegment: _api.PanelSegment):
		self._Entity = panelSegment

	@property
	def ElementsByObjectOrSkin(self) -> dict[types.DiscreteDefinitionType, ElementCol]:
		'''
		Return elements in the object / skin.
		'''
		elementsByObjectOrSkinDict = {}
		for kvp in self._Entity.ElementsByObjectOrSkin:
			elementsByObjectOrSkinDict[types.DiscreteDefinitionType[kvp.Key.ToString()]] = ElementCol(kvp.Value)

		return elementsByObjectOrSkinDict

	@property
	def Skins(self) -> tuple[types.DiscreteDefinitionType]:
		return tuple([types.DiscreteDefinitionType[discreteDefinitionType.ToString()] for discreteDefinitionType in self._Entity.Skins])

	@property
	def Objects(self) -> tuple[types.DiscreteDefinitionType]:
		return tuple([types.DiscreteDefinitionType[discreteDefinitionType.ToString()] for discreteDefinitionType in self._Entity.Objects])

	@property
	def DiscreteTechnique(self) -> types.DiscreteTechnique | None:
		result = self._Entity.DiscreteTechnique
		return types.DiscreteTechnique[result.ToString()] if result is not None else None

	@property
	def LeftSkinZoneId(self) -> int | None:
		return self._Entity.LeftSkinZoneId

	@property
	def RightSkinZoneId(self) -> int | None:
		return self._Entity.RightSkinZoneId

	def GetElements(self, discreteDefinitionType: types.DiscreteDefinitionType) -> ElementCol:
		return ElementCol(self._Entity.GetElements(_types.DiscreteDefinitionType(types.GetEnumValue(discreteDefinitionType.value))))

	def SetObjectElements(self, discreteDefinitionType: types.DiscreteDefinitionType, elementIds: tuple[int]) -> None:
		elementIdsList = MakeCSharpIntList(elementIds)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		return self._Entity.SetObjectElements(_types.DiscreteDefinitionType(types.GetEnumValue(discreteDefinitionType.value)), elementIdsEnumerable)


class Zone(ZoneBase):
	'''
	Abstract for regular Zones (not Panel Segments).
	'''
	def __init__(self, zone: _api.Zone):
		self._Entity = zone

	@property
	def Elements(self) -> ElementCol:
		result = self._Entity.Elements
		return ElementCol(result) if result is not None else None

	def AddElements(self, elementIds: tuple[int]) -> None:
		elementIdsList = MakeCSharpIntList(elementIds)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		return self._Entity.AddElements(elementIdsEnumerable)


class EntityWithAssignablePropertiesCol(IdNameEntityCol, Generic[T]):
	def __init__(self, entityWithAssignablePropertiesCol: _api.EntityWithAssignablePropertiesCol):
		self._Entity = entityWithAssignablePropertiesCol
		self._CollectedClass = T

	def AssignPropertyToAll(self, property: AssignableProperty) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self._Entity.AssignPropertyToAll(property._Entity).ToString()]

	@overload
	def Get(self, name: str) -> EntityWithAssignableProperties:
		...

	@overload
	def Get(self, id: int) -> EntityWithAssignableProperties:
		...

	def Get(self, item1 = None) -> EntityWithAssignableProperties:
		'''
		Overload 1: ``Get(self, name: str) -> EntityWithAssignableProperties``

		Overload 2: ``Get(self, id: int) -> EntityWithAssignableProperties``
		'''
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

		return self._Entity.Get(item1)


class JointCol(EntityWithAssignablePropertiesCol[Joint]):
	def __init__(self, jointCol: _api.JointCol):
		self._Entity = jointCol
		self._CollectedClass = Joint

	@property
	def JointColList(self) -> tuple[Joint]:
		return tuple([Joint(jointCol) for jointCol in self._Entity])

	@overload
	def Get(self, name: str) -> Joint:
		...

	@overload
	def Get(self, id: int) -> Joint:
		...

	def Get(self, item1 = None) -> Joint:
		'''
		Overload 1: ``Get(self, name: str) -> Joint``

		Overload 2: ``Get(self, id: int) -> Joint``
		'''
		if isinstance(item1, str):
			return Joint(super().Get(item1))

		if isinstance(item1, int):
			return Joint(super().Get(item1))

		return Joint(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.JointColList[index]

	def __iter__(self):
		yield from self.JointColList

	def __len__(self):
		return len(self.JointColList)


class PanelSegmentCol(EntityWithAssignablePropertiesCol[PanelSegment]):
	def __init__(self, panelSegmentCol: _api.PanelSegmentCol):
		self._Entity = panelSegmentCol
		self._CollectedClass = PanelSegment

	@property
	def PanelSegmentColList(self) -> tuple[PanelSegment]:
		return tuple([PanelSegment(panelSegmentCol) for panelSegmentCol in self._Entity])

	@overload
	def Get(self, name: str) -> PanelSegment:
		...

	@overload
	def Get(self, id: int) -> PanelSegment:
		...

	def Get(self, item1 = None) -> PanelSegment:
		'''
		Overload 1: ``Get(self, name: str) -> PanelSegment``

		Overload 2: ``Get(self, id: int) -> PanelSegment``
		'''
		if isinstance(item1, str):
			return PanelSegment(super().Get(item1))

		if isinstance(item1, int):
			return PanelSegment(super().Get(item1))

		return PanelSegment(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.PanelSegmentColList[index]

	def __iter__(self):
		yield from self.PanelSegmentColList

	def __len__(self):
		return len(self.PanelSegmentColList)


class ZoneCol(EntityWithAssignablePropertiesCol[Zone]):
	def __init__(self, zoneCol: _api.ZoneCol):
		self._Entity = zoneCol
		self._CollectedClass = Zone

	@property
	def ZoneColList(self) -> tuple[Zone]:
		zoneColList = []
		subclasses = {x.__name__: x for x in _all_subclasses(Zone)}
		for zoneCol in self._Entity:
			if type(zoneCol).__name__ in subclasses.keys():
				thisType = subclasses[type(zoneCol).__name__]
				zoneColList.append(thisType(zoneCol))
			else:
				raise Exception(f"Could not wrap item in ZoneCol. This should not happen.")
		return tuple(zoneColList)

	@overload
	def Get(self, name: str) -> Zone:
		...

	@overload
	def Get(self, id: int) -> Zone:
		...

	def Get(self, item1 = None) -> Zone:
		'''
		Overload 1: ``Get(self, name: str) -> Zone``

		Overload 2: ``Get(self, id: int) -> Zone``
		'''
		if isinstance(item1, str):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = Zone
			for subclass in _all_subclasses(Zone):
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, int):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = Zone
			for subclass in _all_subclasses(Zone):
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		result = self._Entity.Get(item1)
		thisClass = type(result).__name__
		givenClass = Zone
		for subclass in _all_subclasses(Zone):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def __getitem__(self, index: int):
		return self.ZoneColList[index]

	def __iter__(self):
		yield from self.ZoneColList

	def __len__(self):
		return len(self.ZoneColList)


class ZoneJointContainer(IdNameEntityRenameable):
	'''
	Represents an entity that contains a collection of Zones and Joints.
	'''

	_Centroid = Centroid
	def __init__(self, zoneJointContainer: _api.ZoneJointContainer):
		self._Entity = zoneJointContainer
	@property
	def Centroid(self) -> _Centroid:
		'''
		Centroid center determined by weight.
		'''
		result = self._Entity.Centroid
		return Centroid(result) if result is not None else None

	@property
	def Joints(self) -> JointCol:
		result = self._Entity.Joints
		return JointCol(result) if result is not None else None

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		result = self._Entity.PanelSegments
		return PanelSegmentCol(result) if result is not None else None

	@property
	def TotalBeamLength(self) -> float:
		'''
		Summation of beam lengths.
		'''
		return self._Entity.TotalBeamLength

	@property
	def TotalPanelArea(self) -> float:
		'''
		Summation of panel areas.
		'''
		return self._Entity.TotalPanelArea

	@property
	def TotalZoneWeight(self) -> float:
		'''
		Get the total weight of all zones contained in this object.
		'''
		return self._Entity.TotalZoneWeight

	@property
	def Zones(self) -> ZoneCol:
		result = self._Entity.Zones
		return ZoneCol(result) if result is not None else None

	@overload
	def AddJoint(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	@abstractmethod
	def AddJoint(self, joint: Joint) -> CollectionModificationStatus:
		...

	@overload
	def RemoveJoint(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	def RemoveJoint(self, joint: Joint) -> CollectionModificationStatus:
		...

	@overload
	@abstractmethod
	def RemoveJoints(self, jointIds: tuple[int]) -> CollectionModificationStatus:
		...

	@overload
	def RemoveJoints(self, joints: tuple[Joint]) -> CollectionModificationStatus:
		...

	@overload
	def AddZone(self, id: int) -> CollectionModificationStatus:
		'''
		Add an existing zone to this entity.
		'''
		...

	@overload
	def AddZones(self, ids: tuple[int]) -> CollectionModificationStatus:
		'''
		Add existing zones to this entity.
		'''
		...

	@overload
	def AddZone(self, zone: Zone) -> CollectionModificationStatus:
		'''
		Add an existing zone to this entity.
		'''
		...

	@overload
	@abstractmethod
	def AddZones(self, zones: tuple[Zone]) -> CollectionModificationStatus:
		'''
		Add existing zones to this entity
		'''
		...

	@overload
	def RemoveZone(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	def RemoveZone(self, zone: Zone) -> CollectionModificationStatus:
		...

	@overload
	@abstractmethod
	def RemoveZones(self, zoneIds: tuple[int]) -> CollectionModificationStatus:
		...

	@overload
	def RemoveZones(self, zones: tuple[Zone]) -> CollectionModificationStatus:
		...

	@overload
	def AddPanelSegment(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	@abstractmethod
	def AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus:
		'''
		Add an existing panel segment to this entity
		'''
		...

	@overload
	def RemovePanelSegment(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	def RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus:
		...

	@overload
	@abstractmethod
	def RemovePanelSegments(self, segmentIds: tuple[int]) -> CollectionModificationStatus:
		...

	@overload
	def RemovePanelSegments(self, segments: tuple[PanelSegment]) -> CollectionModificationStatus:
		...

	def AddJoint(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``AddJoint(self, id: int) -> CollectionModificationStatus``

		Overload 2: ``AddJoint(self, joint: Joint) -> CollectionModificationStatus``
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.AddJoint(item1).ToString()]

		if isinstance(item1, Joint):
			return CollectionModificationStatus[self._Entity.AddJoint(item1._Entity).ToString()]

		return CollectionModificationStatus[self._Entity.AddJoint(item1).ToString()]

	def RemoveJoint(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemoveJoint(self, id: int) -> CollectionModificationStatus``

		Overload 2: ``RemoveJoint(self, joint: Joint) -> CollectionModificationStatus``
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.RemoveJoint(item1).ToString()]

		if isinstance(item1, Joint):
			return CollectionModificationStatus[self._Entity.RemoveJoint(item1._Entity).ToString()]

		return CollectionModificationStatus[self._Entity.RemoveJoint(item1).ToString()]

	def RemoveJoints(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemoveJoints(self, jointIds: tuple[int]) -> CollectionModificationStatus``

		Overload 2: ``RemoveJoints(self, joints: tuple[Joint]) -> CollectionModificationStatus``
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			jointIdsList = MakeCSharpIntList(item1)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self._Entity.RemoveJoints(jointIdsEnumerable).ToString()]

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, Joint) for x in item1):
			jointsList = List[_api.Joint]()
			if item1 is not None:
				for x in item1:
					if x is not None:
						jointsList.Add(x._Entity)
			jointsEnumerable = IEnumerable(jointsList)
			return CollectionModificationStatus[self._Entity.RemoveJoints(jointsEnumerable).ToString()]

		return CollectionModificationStatus[self._Entity.RemoveJoints(item1).ToString()]

	def AddZone(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``AddZone(self, id: int) -> CollectionModificationStatus``

		Add an existing zone to this entity.

		Overload 2: ``AddZone(self, zone: Zone) -> CollectionModificationStatus``

		Add an existing zone to this entity.
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.AddZone(item1).ToString()]

		if isinstance(item1, Zone):
			return CollectionModificationStatus[self._Entity.AddZone(item1._Entity).ToString()]

		return CollectionModificationStatus[self._Entity.AddZone(item1).ToString()]

	def AddZones(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``AddZones(self, ids: tuple[int]) -> CollectionModificationStatus``

		Add existing zones to this entity.

		Overload 2: ``AddZones(self, zones: tuple[Zone]) -> CollectionModificationStatus``

		Add existing zones to this entity
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			idsList = MakeCSharpIntList(item1)
			idsEnumerable = IEnumerable(idsList)
			return CollectionModificationStatus[self._Entity.AddZones(idsEnumerable).ToString()]

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, Zone) for x in item1):
			zonesList = List[_api.Zone]()
			if item1 is not None:
				for x in item1:
					if x is not None:
						zonesList.Add(x._Entity)
			zonesEnumerable = IEnumerable(zonesList)
			return CollectionModificationStatus[self._Entity.AddZones(zonesEnumerable).ToString()]

		return CollectionModificationStatus[self._Entity.AddZones(item1).ToString()]

	def RemoveZone(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemoveZone(self, id: int) -> CollectionModificationStatus``

		Overload 2: ``RemoveZone(self, zone: Zone) -> CollectionModificationStatus``
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.RemoveZone(item1).ToString()]

		if isinstance(item1, Zone):
			return CollectionModificationStatus[self._Entity.RemoveZone(item1._Entity).ToString()]

		return CollectionModificationStatus[self._Entity.RemoveZone(item1).ToString()]

	def RemoveZones(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemoveZones(self, zoneIds: tuple[int]) -> CollectionModificationStatus``

		Overload 2: ``RemoveZones(self, zones: tuple[Zone]) -> CollectionModificationStatus``
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return CollectionModificationStatus[self._Entity.RemoveZones(zoneIdsEnumerable).ToString()]

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, Zone) for x in item1):
			zonesList = List[_api.Zone]()
			if item1 is not None:
				for x in item1:
					if x is not None:
						zonesList.Add(x._Entity)
			zonesEnumerable = IEnumerable(zonesList)
			return CollectionModificationStatus[self._Entity.RemoveZones(zonesEnumerable).ToString()]

		return CollectionModificationStatus[self._Entity.RemoveZones(item1).ToString()]

	def AddPanelSegment(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``AddPanelSegment(self, id: int) -> CollectionModificationStatus``

		Overload 2: ``AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus``

		Add an existing panel segment to this entity
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.AddPanelSegment(item1).ToString()]

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self._Entity.AddPanelSegment(item1._Entity).ToString()]

		return CollectionModificationStatus[self._Entity.AddPanelSegment(item1).ToString()]

	def RemovePanelSegment(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemovePanelSegment(self, id: int) -> CollectionModificationStatus``

		Overload 2: ``RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus``
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.RemovePanelSegment(item1).ToString()]

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self._Entity.RemovePanelSegment(item1._Entity).ToString()]

		return CollectionModificationStatus[self._Entity.RemovePanelSegment(item1).ToString()]

	def RemovePanelSegments(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemovePanelSegments(self, segmentIds: tuple[int]) -> CollectionModificationStatus``

		Overload 2: ``RemovePanelSegments(self, segments: tuple[PanelSegment]) -> CollectionModificationStatus``
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			segmentIdsList = MakeCSharpIntList(item1)
			segmentIdsEnumerable = IEnumerable(segmentIdsList)
			return CollectionModificationStatus[self._Entity.RemovePanelSegments(segmentIdsEnumerable).ToString()]

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, PanelSegment) for x in item1):
			segmentsList = List[_api.PanelSegment]()
			if item1 is not None:
				for x in item1:
					if x is not None:
						segmentsList.Add(x._Entity)
			segmentsEnumerable = IEnumerable(segmentsList)
			return CollectionModificationStatus[self._Entity.RemovePanelSegments(segmentsEnumerable).ToString()]

		return CollectionModificationStatus[self._Entity.RemovePanelSegments(item1).ToString()]


class AutomatedConstraint(IdNameEntityRenameable):
	def __init__(self, automatedConstraint: _api.AutomatedConstraint):
		self._Entity = automatedConstraint

	@property
	def ConstraintType(self) -> types.StiffnessCriteriaType:
		'''
		StiffnessCriteriaType of the Automated Constraint>
		'''
		result = self._Entity.ConstraintType
		return types.StiffnessCriteriaType[result.ToString()] if result is not None else None

	@property
	def Set(self) -> str:
		'''
		The Set of the Automated Constraint.
		'''
		return self._Entity.Set

	@property
	def DesignLoadCases(self) -> list[str]:
		'''
		The assigned Design Loads of the Automated Constraint.
		'''
		return [string for string in self._Entity.DesignLoadCases]

	@Set.setter
	def Set(self, value: str) -> None:
		self._Entity.Set = value

	def AddDesignLoadCases(self, designLoadCases: tuple[str]) -> None:
		'''
		Add a list of Design Loads to the Automated Constraint by name.
		
		:raises ``System.InvalidOperationException``: Throws if a Design Load is not valid for the StiffnessCriteriaType.
		'''
		designLoadCasesList = List[str]()
		if designLoadCases is not None:
			for x in designLoadCases:
				if x is not None:
					designLoadCasesList.Add(x)
		designLoadCasesEnumerable = IEnumerable(designLoadCasesList)
		return self._Entity.AddDesignLoadCases(designLoadCasesEnumerable)

	def RemoveDesignLoadCases(self, designLoadCases: tuple[str]) -> None:
		'''
		Remove a list of Design Loads from the AutomatedConstraint by name.
		
		:raises ``System.InvalidOperationException``: Throws if executing this method would remove all assigned Design Loads.
		'''
		designLoadCasesList = List[str]()
		if designLoadCases is not None:
			for x in designLoadCases:
				if x is not None:
					designLoadCasesList.Add(x)
		designLoadCasesEnumerable = IEnumerable(designLoadCasesList)
		return self._Entity.RemoveDesignLoadCases(designLoadCasesEnumerable)


class ModalAutomatedConstraint(AutomatedConstraint):
	def __init__(self, modalAutomatedConstraint: _api.ModalAutomatedConstraint):
		self._Entity = modalAutomatedConstraint

	@property
	def Eigenvalue(self) -> float:
		return self._Entity.Eigenvalue

	@Eigenvalue.setter
	def Eigenvalue(self, value: float) -> None:
		self._Entity.Eigenvalue = value


class BucklingAutomatedConstraint(ModalAutomatedConstraint):
	def __init__(self, bucklingAutomatedConstraint: _api.BucklingAutomatedConstraint):
		self._Entity = bucklingAutomatedConstraint


class StaticAutomatedConstraint(AutomatedConstraint):
	def __init__(self, staticAutomatedConstraint: _api.StaticAutomatedConstraint):
		self._Entity = staticAutomatedConstraint

	@property
	def VirtualDesignLoad(self) -> str:
		'''
		Virtual Design Load for a Static Automated Constraint.
		'''
		return self._Entity.VirtualDesignLoad

	@property
	def GridId(self) -> int:
		'''
		Associated grid for a Static Automated Constraint.
		'''
		return self._Entity.GridId

	@property
	def Orientation(self) -> types.DisplacementShapeType:
		'''
		Orientation for a Static Automated Constraint.
		'''
		result = self._Entity.Orientation
		return types.DisplacementShapeType[result.ToString()] if result is not None else None

	@property
	def HasVector(self) -> bool:
		'''
		Indicates whether a Static Automated Constraint has a vector. Dependent on Orientation.
		'''
		return self._Entity.HasVector

	@property
	def X(self) -> float | None:
		'''
		X value of the vector of a Static Automated Constraint.
		'''
		return self._Entity.X

	@property
	def Y(self) -> float | None:
		'''
		Y value of the vector of a Static Automated Constraint.
		'''
		return self._Entity.Y

	@property
	def Z(self) -> float | None:
		'''
		Z value of the vector of a Static Automated Constraint.
		'''
		return self._Entity.Z

	@VirtualDesignLoad.setter
	def VirtualDesignLoad(self, value: str) -> None:
		self._Entity.VirtualDesignLoad = value

	@GridId.setter
	def GridId(self, value: int) -> None:
		self._Entity.GridId = value

	@Orientation.setter
	def Orientation(self, value: types.DisplacementShapeType) -> None:
		self._Entity.Orientation = _types.DisplacementShapeType(types.GetEnumValue(value.value))

	@X.setter
	def X(self, value: float | None) -> None:
		self._Entity.X = value

	@Y.setter
	def Y(self, value: float | None) -> None:
		self._Entity.Y = value

	@Z.setter
	def Z(self, value: float | None) -> None:
		self._Entity.Z = value


class DisplacementAutomatedConstraint(StaticAutomatedConstraint):
	def __init__(self, displacementAutomatedConstraint: _api.DisplacementAutomatedConstraint):
		self._Entity = displacementAutomatedConstraint

	@property
	def Limit(self) -> float:
		'''
		Limit for an Automated Constraint. Units: English = in | Standard = mm.
		'''
		return self._Entity.Limit

	@Limit.setter
	def Limit(self, value: float) -> None:
		self._Entity.Limit = value


class FrequencyAutomatedConstraint(ModalAutomatedConstraint):
	def __init__(self, frequencyAutomatedConstraint: _api.FrequencyAutomatedConstraint):
		self._Entity = frequencyAutomatedConstraint


class RotationAutomatedConstraint(StaticAutomatedConstraint):
	def __init__(self, rotationAutomatedConstraint: _api.RotationAutomatedConstraint):
		self._Entity = rotationAutomatedConstraint

	@property
	def Limit(self) -> float:
		'''
		Limit for an Automated Constraint.
		'''
		return self._Entity.Limit

	@Limit.setter
	def Limit(self, value: float) -> None:
		self._Entity.Limit = value


class ManualConstraint(IdNameEntityRenameable):
	def __init__(self, manualConstraint: _api.ManualConstraint):
		self._Entity = manualConstraint

	@property
	def ConstraintType(self) -> types.ConstraintType:
		'''
		The type of Manual Constraint.
		'''
		result = self._Entity.ConstraintType
		return types.ConstraintType[result.ToString()] if result is not None else None

	@property
	def Set(self) -> str:
		'''
		The Set associated with the Manual Constraint.
		'''
		return self._Entity.Set

	@property
	def Limit(self) -> float:
		'''
		Limit Units:
		
		ConstraintType of Displacement -> English = in | Standard = mm.
		
		ConstraintType of Moment -> English = lb*in | Standard = N*mm.
		
		Other ConstraintType -> Unitless.
		'''
		return self._Entity.Limit

	@property
	def A11(self) -> bool:
		'''
		Indicates if A11 is active for the Manual Constraint.
		'''
		return self._Entity.A11

	@property
	def A22(self) -> bool:
		'''
		Indicates if A22 is active for the Manual Constraint.
		'''
		return self._Entity.A22

	@property
	def A33(self) -> bool:
		'''
		Indicates if A33 is active for the Manual Constraint.
		'''
		return self._Entity.A33

	@property
	def D11(self) -> bool:
		'''
		Indicates if D11 is active for the Manual Constraint.
		'''
		return self._Entity.D11

	@property
	def D22(self) -> bool:
		'''
		Indicates if D22 is active for the Manual Constraint.
		'''
		return self._Entity.D22

	@property
	def D33(self) -> bool:
		'''
		Indicates if D33 is active for the Manual Constraint.
		'''
		return self._Entity.D33

	@property
	def EA(self) -> bool:
		'''
		Indicates if EA is active for the Manual Constraint.
		'''
		return self._Entity.EA

	@property
	def EI1(self) -> bool:
		'''
		Indicates if EI1 is active for the Manual Constraint.
		'''
		return self._Entity.EI1

	@property
	def EI2(self) -> bool:
		'''
		Indicates if EI2 is active for the Manual Constraint.
		'''
		return self._Entity.EI2

	@property
	def GJ(self) -> bool:
		'''
		Indicates if GJ is active for the Manual Constraint.
		'''
		return self._Entity.GJ

	@property
	def IsActive(self) -> bool:
		'''
		Indiactes if the Manual Constraint is active.
		'''
		return self._Entity.IsActive

	@Set.setter
	def Set(self, value: str) -> None:
		self._Entity.Set = value

	@Limit.setter
	def Limit(self, value: float) -> None:
		self._Entity.Limit = value

	@A11.setter
	def A11(self, value: bool) -> None:
		self._Entity.A11 = value

	@A22.setter
	def A22(self, value: bool) -> None:
		self._Entity.A22 = value

	@A33.setter
	def A33(self, value: bool) -> None:
		self._Entity.A33 = value

	@D11.setter
	def D11(self, value: bool) -> None:
		self._Entity.D11 = value

	@D22.setter
	def D22(self, value: bool) -> None:
		self._Entity.D22 = value

	@D33.setter
	def D33(self, value: bool) -> None:
		self._Entity.D33 = value

	@EA.setter
	def EA(self, value: bool) -> None:
		self._Entity.EA = value

	@EI1.setter
	def EI1(self, value: bool) -> None:
		self._Entity.EI1 = value

	@EI2.setter
	def EI2(self, value: bool) -> None:
		self._Entity.EI2 = value

	@GJ.setter
	def GJ(self, value: bool) -> None:
		self._Entity.GJ = value

	@IsActive.setter
	def IsActive(self, value: bool) -> None:
		self._Entity.IsActive = value


class ManualConstraintWithDesignLoad(ManualConstraint):
	def __init__(self, manualConstraintWithDesignLoad: _api.ManualConstraintWithDesignLoad):
		self._Entity = manualConstraintWithDesignLoad

	@property
	def UseAllDesignLoads(self) -> bool:
		'''
		Indicates whether a specific Design Load is used or all.
		'''
		return self._Entity.UseAllDesignLoads

	@property
	def DesignLoadCase(self) -> str:
		'''
		The specific Design Load for the Manual Constraint.
		'''
		return self._Entity.DesignLoadCase

	@UseAllDesignLoads.setter
	def UseAllDesignLoads(self, value: bool) -> None:
		self._Entity.UseAllDesignLoads = value

	@DesignLoadCase.setter
	def DesignLoadCase(self, value: str) -> None:
		self._Entity.DesignLoadCase = value


class BucklingManualConstraint(ManualConstraintWithDesignLoad):
	def __init__(self, bucklingManualConstraint: _api.BucklingManualConstraint):
		self._Entity = bucklingManualConstraint


class DisplacementManualConstraint(ManualConstraintWithDesignLoad):
	def __init__(self, displacementManualConstraint: _api.DisplacementManualConstraint):
		self._Entity = displacementManualConstraint

	@property
	def DOF(self) -> types.DegreeOfFreedom:
		'''
		DOF of a Displacement Manual Constraint.
		'''
		result = self._Entity.DOF
		return types.DegreeOfFreedom[result.ToString()] if result is not None else None

	@property
	def Nodes(self) -> list[int]:
		'''
		Associated Nodes of a Displacement Manual Constraint.
		'''
		return [int32 for int32 in self._Entity.Nodes]

	@property
	def RefNodes(self) -> list[int]:
		'''
		Associated Ref Nodes of a Displacement Manual Constraint.
		'''
		return [int32 for int32 in self._Entity.RefNodes]

	@DOF.setter
	def DOF(self, value: types.DegreeOfFreedom) -> None:
		self._Entity.DOF = _types.DegreeOfFreedom(types.GetEnumValue(value.value))

	def AddNodes(self, ids: tuple[int]) -> None:
		'''
		Add a list of Nodes to the Displacement Manual Constraint.
		
		:raises ``System.InvalidOperationException``: Throws if the Node is not in the FEM.
		'''
		idsList = MakeCSharpIntList(ids)
		idsEnumerable = IEnumerable(idsList)
		return self._Entity.AddNodes(idsEnumerable)

	def RemoveNodes(self, ids: tuple[int]) -> None:
		'''
		Remove a list of Nodes from the Displacement Manual Constraint.
		
		:raises ``System.InvalidOperationException``: Throws if the execution of the method will remove all Nodes.
		'''
		idsList = MakeCSharpIntList(ids)
		idsEnumerable = IEnumerable(idsList)
		return self._Entity.RemoveNodes(idsEnumerable)

	def AddRefNodes(self, ids: tuple[int]) -> None:
		'''
		Add a list of Ref Nodes to the Displacement Manual Constraint.
		
		:raises ``System.InvalidOperationException``:
		'''
		idsList = MakeCSharpIntList(ids)
		idsEnumerable = IEnumerable(idsList)
		return self._Entity.AddRefNodes(idsEnumerable)

	def RemoveRefNodes(self, ids: tuple[int]) -> None:
		'''
		Remove a list of Ref Nodes from the Displacement Manual Constraint.
		'''
		idsList = MakeCSharpIntList(ids)
		idsEnumerable = IEnumerable(idsList)
		return self._Entity.RemoveRefNodes(idsEnumerable)


class FrequencyManualConstraint(ManualConstraintWithDesignLoad):
	def __init__(self, frequencyManualConstraint: _api.FrequencyManualConstraint):
		self._Entity = frequencyManualConstraint


class StaticMomentManualConstraint(ManualConstraint):
	def __init__(self, staticMomentManualConstraint: _api.StaticMomentManualConstraint):
		self._Entity = staticMomentManualConstraint


class AutomatedConstraintCol(IdNameEntityCol[AutomatedConstraint]):
	def __init__(self, automatedConstraintCol: _api.AutomatedConstraintCol):
		self._Entity = automatedConstraintCol
		self._CollectedClass = AutomatedConstraint

	@property
	def AutomatedConstraintColList(self) -> tuple[AutomatedConstraint]:
		automatedConstraintColList = []
		subclasses = {x.__name__: x for x in _all_subclasses(AutomatedConstraint)}
		for automatedConstraintCol in self._Entity:
			if type(automatedConstraintCol).__name__ in subclasses.keys():
				thisType = subclasses[type(automatedConstraintCol).__name__]
				automatedConstraintColList.append(thisType(automatedConstraintCol))
			else:
				raise Exception(f"Could not wrap item in AutomatedConstraintCol. This should not happen.")
		return tuple(automatedConstraintColList)

	def AddBucklingConstraint(self, designLoads: tuple[str], eigenvalue: float, name: str = None) -> BucklingAutomatedConstraint:
		'''
		Add an Automated Constraint of type Buckling.
		'''
		designLoadsList = List[str]()
		if designLoads is not None:
			for x in designLoads:
				if x is not None:
					designLoadsList.Add(x)
		designLoadsEnumerable = IEnumerable(designLoadsList)
		return BucklingAutomatedConstraint(self._Entity.AddBucklingConstraint(designLoadsEnumerable, eigenvalue, name))

	def AddFrequencyConstraint(self, designLoads: tuple[str], eigenvalue: float, name: str = None) -> FrequencyAutomatedConstraint:
		'''
		Add an Automated Constraint of type Frequency.
		'''
		designLoadsList = List[str]()
		if designLoads is not None:
			for x in designLoads:
				if x is not None:
					designLoadsList.Add(x)
		designLoadsEnumerable = IEnumerable(designLoadsList)
		return FrequencyAutomatedConstraint(self._Entity.AddFrequencyConstraint(designLoadsEnumerable, eigenvalue, name))

	def AddDisplacementConstraint(self, designLoads: tuple[str], gridId: int, limit: float, name: str = None) -> DisplacementAutomatedConstraint:
		'''
		Add an Automated Constraint of type Displacement.
		'''
		designLoadsList = List[str]()
		if designLoads is not None:
			for x in designLoads:
				if x is not None:
					designLoadsList.Add(x)
		designLoadsEnumerable = IEnumerable(designLoadsList)
		return DisplacementAutomatedConstraint(self._Entity.AddDisplacementConstraint(designLoadsEnumerable, gridId, limit, name))

	def AddRotationConstraint(self, designLoads: tuple[str], gridId: int, limit: float, name: str = None) -> RotationAutomatedConstraint:
		'''
		Add an Automated Constraint of type Rotation.
		'''
		designLoadsList = List[str]()
		if designLoads is not None:
			for x in designLoads:
				if x is not None:
					designLoadsList.Add(x)
		designLoadsEnumerable = IEnumerable(designLoadsList)
		return RotationAutomatedConstraint(self._Entity.AddRotationConstraint(designLoadsEnumerable, gridId, limit, name))

	@overload
	def Delete(self, id: int) -> bool:
		'''
		Delete an Automated Constraint by id.
		'''
		...

	@overload
	def Delete(self, name: str) -> bool:
		'''
		Delete an Automated Constraint by name.
		'''
		...

	@overload
	def GetBuckling(self, id: int) -> BucklingAutomatedConstraint:
		...

	@overload
	def GetBuckling(self, name: str) -> BucklingAutomatedConstraint:
		...

	@overload
	def GetFrequency(self, id: int) -> FrequencyAutomatedConstraint:
		...

	@overload
	def GetFrequency(self, name: str) -> FrequencyAutomatedConstraint:
		...

	@overload
	def GetRotation(self, id: int) -> RotationAutomatedConstraint:
		...

	@overload
	def GetRotation(self, name: str) -> RotationAutomatedConstraint:
		...

	@overload
	def GetDisplacement(self, id: int) -> DisplacementAutomatedConstraint:
		...

	@overload
	def GetDisplacement(self, name: str) -> DisplacementAutomatedConstraint:
		...

	@overload
	def Get(self, name: str) -> AutomatedConstraint:
		...

	@overload
	def Get(self, id: int) -> AutomatedConstraint:
		...

	def Delete(self, item1 = None) -> bool:
		'''
		Overload 1: ``Delete(self, id: int) -> bool``

		Delete an Automated Constraint by id.

		Overload 2: ``Delete(self, name: str) -> bool``

		Delete an Automated Constraint by name.
		'''
		if isinstance(item1, int):
			return self._Entity.Delete(item1)

		if isinstance(item1, str):
			return self._Entity.Delete(item1)

		return self._Entity.Delete(item1)

	def GetBuckling(self, item1 = None) -> BucklingAutomatedConstraint:
		'''
		Overload 1: ``GetBuckling(self, id: int) -> BucklingAutomatedConstraint``

		Overload 2: ``GetBuckling(self, name: str) -> BucklingAutomatedConstraint``
		'''
		if isinstance(item1, int):
			return BucklingAutomatedConstraint(self._Entity.GetBuckling(item1))

		if isinstance(item1, str):
			return BucklingAutomatedConstraint(self._Entity.GetBuckling(item1))

		return BucklingAutomatedConstraint(self._Entity.GetBuckling(item1))

	def GetFrequency(self, item1 = None) -> FrequencyAutomatedConstraint:
		'''
		Overload 1: ``GetFrequency(self, id: int) -> FrequencyAutomatedConstraint``

		Overload 2: ``GetFrequency(self, name: str) -> FrequencyAutomatedConstraint``
		'''
		if isinstance(item1, int):
			return FrequencyAutomatedConstraint(self._Entity.GetFrequency(item1))

		if isinstance(item1, str):
			return FrequencyAutomatedConstraint(self._Entity.GetFrequency(item1))

		return FrequencyAutomatedConstraint(self._Entity.GetFrequency(item1))

	def GetRotation(self, item1 = None) -> RotationAutomatedConstraint:
		'''
		Overload 1: ``GetRotation(self, id: int) -> RotationAutomatedConstraint``

		Overload 2: ``GetRotation(self, name: str) -> RotationAutomatedConstraint``
		'''
		if isinstance(item1, int):
			return RotationAutomatedConstraint(self._Entity.GetRotation(item1))

		if isinstance(item1, str):
			return RotationAutomatedConstraint(self._Entity.GetRotation(item1))

		return RotationAutomatedConstraint(self._Entity.GetRotation(item1))

	def GetDisplacement(self, item1 = None) -> DisplacementAutomatedConstraint:
		'''
		Overload 1: ``GetDisplacement(self, id: int) -> DisplacementAutomatedConstraint``

		Overload 2: ``GetDisplacement(self, name: str) -> DisplacementAutomatedConstraint``
		'''
		if isinstance(item1, int):
			return DisplacementAutomatedConstraint(self._Entity.GetDisplacement(item1))

		if isinstance(item1, str):
			return DisplacementAutomatedConstraint(self._Entity.GetDisplacement(item1))

		return DisplacementAutomatedConstraint(self._Entity.GetDisplacement(item1))

	def Get(self, item1 = None) -> AutomatedConstraint:
		'''
		Overload 1: ``Get(self, name: str) -> AutomatedConstraint``

		Overload 2: ``Get(self, id: int) -> AutomatedConstraint``
		'''
		if isinstance(item1, str):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = AutomatedConstraint
			for subclass in _all_subclasses(AutomatedConstraint):
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, int):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = AutomatedConstraint
			for subclass in _all_subclasses(AutomatedConstraint):
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		result = self._Entity.Get(item1)
		thisClass = type(result).__name__
		givenClass = AutomatedConstraint
		for subclass in _all_subclasses(AutomatedConstraint):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def __getitem__(self, index: int):
		return self.AutomatedConstraintColList[index]

	def __iter__(self):
		yield from self.AutomatedConstraintColList

	def __len__(self):
		return len(self.AutomatedConstraintColList)


class ManualConstraintCol(IdNameEntityCol[ManualConstraint]):
	def __init__(self, manualConstraintCol: _api.ManualConstraintCol):
		self._Entity = manualConstraintCol
		self._CollectedClass = ManualConstraint

	@property
	def ManualConstraintColList(self) -> tuple[ManualConstraint]:
		return tuple([ManualConstraint(manualConstraintCol) for manualConstraintCol in self._Entity])

	@overload
	def GetFrequency(self, id: int) -> FrequencyManualConstraint:
		...

	@overload
	def GetFrequency(self, name: str) -> FrequencyManualConstraint:
		...

	@overload
	def GetBuckling(self, id: int) -> BucklingManualConstraint:
		...

	@overload
	def GetBuckling(self, name: str) -> BucklingManualConstraint:
		...

	@overload
	def GetDisplacement(self, id: int) -> DisplacementManualConstraint:
		...

	@overload
	def GetDisplacement(self, name: str) -> DisplacementManualConstraint:
		...

	@overload
	def GetStaticMoment(self, id: int) -> StaticMomentManualConstraint:
		...

	@overload
	def GetStaticMoment(self, name: str) -> StaticMomentManualConstraint:
		...

	def AddFrequencyConstraint(self, setName: str, limit: float, name: str = None) -> FrequencyManualConstraint:
		'''
		Add a Manual Constraint of type Frequency.
		'''
		return FrequencyManualConstraint(self._Entity.AddFrequencyConstraint(setName, limit, name))

	def AddBucklingConstraint(self, setName: str, limit: float, name: str = None) -> BucklingManualConstraint:
		'''
		Add a Manual Constraint of type Buckling.
		'''
		return BucklingManualConstraint(self._Entity.AddBucklingConstraint(setName, limit, name))

	def AddStaticMomentManualConstraint(self, setName: str, limit: float, name: str = None) -> StaticMomentManualConstraint:
		'''
		Add a Manual Constraint of type Static Moment.
		'''
		return StaticMomentManualConstraint(self._Entity.AddStaticMomentManualConstraint(setName, limit, name))

	def AddDisplacementConstraint(self, setName: str, gridIds: list[int], limit: float, name: str = None) -> DisplacementManualConstraint:
		'''
		Add a Manual Constraint of type Displacement.
		'''
		gridIdsList = MakeCSharpIntList(gridIds)
		return DisplacementManualConstraint(self._Entity.AddDisplacementConstraint(setName, gridIdsList, limit, name))

	@overload
	def DeleteConstraint(self, name: str) -> bool:
		'''
		Delete a Manual Constraint by name.
		
		:return: False if the constraint is not in the collection.
		'''
		...

	@overload
	def DeleteConstraint(self, id: int) -> bool:
		'''
		Delete a Manual Constraint by id.
		
		:return: Return false if the constraint is not in the collection.
		'''
		...

	@overload
	def Get(self, name: str) -> ManualConstraint:
		...

	@overload
	def Get(self, id: int) -> ManualConstraint:
		...

	def GetFrequency(self, item1 = None) -> FrequencyManualConstraint:
		'''
		Overload 1: ``GetFrequency(self, id: int) -> FrequencyManualConstraint``

		Overload 2: ``GetFrequency(self, name: str) -> FrequencyManualConstraint``
		'''
		if isinstance(item1, int):
			return FrequencyManualConstraint(self._Entity.GetFrequency(item1))

		if isinstance(item1, str):
			return FrequencyManualConstraint(self._Entity.GetFrequency(item1))

		return FrequencyManualConstraint(self._Entity.GetFrequency(item1))

	def GetBuckling(self, item1 = None) -> BucklingManualConstraint:
		'''
		Overload 1: ``GetBuckling(self, id: int) -> BucklingManualConstraint``

		Overload 2: ``GetBuckling(self, name: str) -> BucklingManualConstraint``
		'''
		if isinstance(item1, int):
			return BucklingManualConstraint(self._Entity.GetBuckling(item1))

		if isinstance(item1, str):
			return BucklingManualConstraint(self._Entity.GetBuckling(item1))

		return BucklingManualConstraint(self._Entity.GetBuckling(item1))

	def GetDisplacement(self, item1 = None) -> DisplacementManualConstraint:
		'''
		Overload 1: ``GetDisplacement(self, id: int) -> DisplacementManualConstraint``

		Overload 2: ``GetDisplacement(self, name: str) -> DisplacementManualConstraint``
		'''
		if isinstance(item1, int):
			return DisplacementManualConstraint(self._Entity.GetDisplacement(item1))

		if isinstance(item1, str):
			return DisplacementManualConstraint(self._Entity.GetDisplacement(item1))

		return DisplacementManualConstraint(self._Entity.GetDisplacement(item1))

	def GetStaticMoment(self, item1 = None) -> StaticMomentManualConstraint:
		'''
		Overload 1: ``GetStaticMoment(self, id: int) -> StaticMomentManualConstraint``

		Overload 2: ``GetStaticMoment(self, name: str) -> StaticMomentManualConstraint``
		'''
		if isinstance(item1, int):
			return StaticMomentManualConstraint(self._Entity.GetStaticMoment(item1))

		if isinstance(item1, str):
			return StaticMomentManualConstraint(self._Entity.GetStaticMoment(item1))

		return StaticMomentManualConstraint(self._Entity.GetStaticMoment(item1))

	def DeleteConstraint(self, item1 = None) -> bool:
		'''
		Overload 1: ``DeleteConstraint(self, name: str) -> bool``

		Delete a Manual Constraint by name.
		
		:return: False if the constraint is not in the collection.

		Overload 2: ``DeleteConstraint(self, id: int) -> bool``

		Delete a Manual Constraint by id.
		
		:return: Return false if the constraint is not in the collection.
		'''
		if isinstance(item1, str):
			return self._Entity.DeleteConstraint(item1)

		if isinstance(item1, int):
			return self._Entity.DeleteConstraint(item1)

		return self._Entity.DeleteConstraint(item1)

	def Get(self, item1 = None) -> ManualConstraint:
		'''
		Overload 1: ``Get(self, name: str) -> ManualConstraint``

		Overload 2: ``Get(self, id: int) -> ManualConstraint``
		'''
		if isinstance(item1, str):
			return ManualConstraint(super().Get(item1))

		if isinstance(item1, int):
			return ManualConstraint(super().Get(item1))

		return ManualConstraint(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.ManualConstraintColList[index]

	def __iter__(self):
		yield from self.ManualConstraintColList

	def __len__(self):
		return len(self.ManualConstraintColList)


class HyperFea:
	def __init__(self, hyperFea: _api.HyperFea):
		self._Entity = hyperFea

	@property
	def ManualConstraints(self) -> ManualConstraintCol:
		'''
		The Manual Constraints for the project.
		'''
		result = self._Entity.ManualConstraints
		return ManualConstraintCol(result) if result is not None else None

	@property
	def AutomatedConstraints(self) -> AutomatedConstraintCol:
		'''
		The Automated Constraints for the project.
		'''
		result = self._Entity.AutomatedConstraints
		return AutomatedConstraintCol(result) if result is not None else None

	def RunIterations(self, numberOfIterations: int, startWithSizing: bool, stressReportFormat: types.StressReportFormat = None) -> None:
		'''
		Run HyperFEA.
		
		:param stressReportFormat: In the case where it is , no reports will be generated.
		
		:raises ``System.InvalidOperationException``:
		'''
		return self._Entity.RunIterations(numberOfIterations, startWithSizing, stressReportFormat if stressReportFormat is None else _types.StressReportFormat(types.GetEnumValue(stressReportFormat.value)))

	@overload
	def SetupSolver(self, solverPath: str, arguments: str) -> types.SimpleStatus:
		'''
		Setup FEA solver.
		'''
		...

	@overload
	def SetupSolver(self, solverPath: str, arguments: str, isBatchRun: bool) -> types.SimpleStatus:
		'''
		Setup the solver command for running FEA.
		
		:param isBatchRun: Flag that indicates whether to run a custom batch file or the standard solver exectuable.
		'''
		...

	def TestSolver(self) -> types.SimpleStatus:
		'''
		Test FEA solver setup.
		'''
		return types.SimpleStatus(self._Entity.TestSolver())

	def GetSolverSetup(self) -> types.HyperFeaSolver:
		'''
		Get the current FEA solver setup.
		'''
		return types.HyperFeaSolver(self._Entity.GetSolverSetup())

	def SetupSolver(self, item1 = None, item2 = None, item3 = None) -> types.SimpleStatus:
		'''
		Overload 1: ``SetupSolver(self, solverPath: str, arguments: str) -> types.SimpleStatus``

		Setup FEA solver.

		Overload 2: ``SetupSolver(self, solverPath: str, arguments: str, isBatchRun: bool) -> types.SimpleStatus``

		Setup the solver command for running FEA.
		
		:param isBatchRun: Flag that indicates whether to run a custom batch file or the standard solver exectuable.
		'''
		if isinstance(item1, str) and isinstance(item2, str) and isinstance(item3, bool):
			return types.SimpleStatus(self._Entity.SetupSolver(item1, item2, item3))

		if isinstance(item1, str) and isinstance(item2, str):
			return types.SimpleStatus(self._Entity.SetupSolver(item1, item2))

		return types.SimpleStatus(self._Entity.SetupSolver(item1, item2, item3))


class HyperXpertPoint:
	def __init__(self, hyperXpertPoint: _api.HyperXpertPoint):
		self._Entity = hyperXpertPoint

	@property
	def Weight(self) -> float:
		return self._Entity.Weight

	@property
	def V(self) -> float:
		return self._Entity.V

	@property
	def Variables(self) -> list[str]:
		return [string for string in self._Entity.Variables]


class RunSet(IdNameEntity):
	def __init__(self, runSet: _api.RunSet):
		self._Entity = runSet


class RunSetSpecifier:
	'''
	Used to specify runsets as an input to some methods.
	'''
	def __init__(self, runSetSpecifier: _api.RunSetSpecifier):
		self._Entity = runSetSpecifier

	def Create_RunSetSpecifier(projectId: int, runSetId: int):
		return RunSetSpecifier(_api.RunSetSpecifier(projectId, runSetId))

	@property
	def ProjectId(self) -> int:
		return self._Entity.ProjectId

	@property
	def RunSetId(self) -> int:
		return self._Entity.RunSetId


class FoamTemperature:
	'''
	Foam material temperature dependent properties.
	'''
	def __init__(self, foamTemperature: _api.FoamTemperature):
		self._Entity = foamTemperature

	@property
	def Temperature(self) -> float:
		'''
		Temperature. Eng: Farenheit / SI: Celsius
		'''
		return self._Entity.Temperature

	@property
	def Et(self) -> float:
		'''
		Et. Eng: Msi / SI: GPa
		'''
		return self._Entity.Et

	@property
	def Ec(self) -> float:
		'''
		Ec. Eng: Msi / SI: GPa
		'''
		return self._Entity.Ec

	@property
	def G(self) -> float:
		'''
		G. Eng: Msi / SI: GPa
		'''
		return self._Entity.G

	@property
	def Ef(self) -> float | None:
		'''
		Ef. Eng: Msi / SI: GPa
		'''
		return self._Entity.Ef

	@property
	def Ftu(self) -> float:
		'''
		Ftu. Eng: ksi / SI: MPa
		'''
		return self._Entity.Ftu

	@property
	def Fcu(self) -> float:
		'''
		Fcu. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fcu

	@property
	def Fsu(self) -> float:
		'''
		Fsu. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fsu

	@property
	def Ffu(self) -> float | None:
		'''
		Ffu. Eng: ksi / SI: MPa
		'''
		return self._Entity.Ffu

	@property
	def K(self) -> float | None:
		'''
		K. Eng: B-ft/ft^2/hr/Farenheit / SI: W/m/Kelvin
		'''
		return self._Entity.K

	@property
	def C(self) -> float | None:
		'''
		C. Eng: B/lb/Farenheit / SI: J/g/K
		'''
		return self._Entity.C

	@Temperature.setter
	def Temperature(self, value: float) -> None:
		self._Entity.Temperature = value

	@Et.setter
	def Et(self, value: float) -> None:
		self._Entity.Et = value

	@Ec.setter
	def Ec(self, value: float) -> None:
		self._Entity.Ec = value

	@G.setter
	def G(self, value: float) -> None:
		self._Entity.G = value

	@Ef.setter
	def Ef(self, value: float | None) -> None:
		self._Entity.Ef = value

	@Ftu.setter
	def Ftu(self, value: float) -> None:
		self._Entity.Ftu = value

	@Fcu.setter
	def Fcu(self, value: float) -> None:
		self._Entity.Fcu = value

	@Fsu.setter
	def Fsu(self, value: float) -> None:
		self._Entity.Fsu = value

	@Ffu.setter
	def Ffu(self, value: float | None) -> None:
		self._Entity.Ffu = value

	@K.setter
	def K(self, value: float | None) -> None:
		self._Entity.K = value

	@C.setter
	def C(self, value: float | None) -> None:
		self._Entity.C = value


class Foam:
	'''
	Foam material.
	'''
	def __init__(self, foam: _api.Foam):
		self._Entity = foam

	@property
	def MaterialFamilyName(self) -> str:
		'''
		The material family for this material. When the material is saved, a new family will be created if none matching this name exists.
		'''
		return self._Entity.MaterialFamilyName

	@property
	def Id(self) -> int:
		return self._Entity.Id

	@property
	def CreationDate(self) -> DateTime:
		'''
		Date the material was created.
		'''
		return self._Entity.CreationDate

	@property
	def ModificationDate(self) -> DateTime:
		'''
		Most recent modification date of the material.
		'''
		return self._Entity.ModificationDate

	@property
	def Name(self) -> str:
		'''
		Name of this material.
		'''
		return self._Entity.Name

	@property
	def Wet(self) -> bool:
		return self._Entity.Wet

	@property
	def Density(self) -> float:
		'''
		Density. Eng: lbm/in^3 / SI: kg/m^3
		'''
		return self._Entity.Density

	@property
	def Form(self) -> str:
		return self._Entity.Form

	@property
	def Specification(self) -> str:
		return self._Entity.Specification

	@property
	def MaterialDescription(self) -> str:
		return self._Entity.MaterialDescription

	@property
	def UserNote(self) -> str:
		return self._Entity.UserNote

	@property
	def FemMaterialId(self) -> int | None:
		'''
		Linked FEM Material ID. Null if none exists.
		'''
		return self._Entity.FemMaterialId

	@property
	def Cost(self) -> float | None:
		return self._Entity.Cost

	@property
	def BucklingStiffnessKnockdown(self) -> float | None:
		return self._Entity.BucklingStiffnessKnockdown

	@property
	def Absorption(self) -> float | None:
		return self._Entity.Absorption

	@property
	def Manufacturer(self) -> str:
		return self._Entity.Manufacturer

	@property
	def FoamTemperatureProperties(self) -> list[FoamTemperature]:
		'''
		List of this material's temperature-dependent properties.
		'''
		return [FoamTemperature(foamTemperature) for foamTemperature in self._Entity.FoamTemperatureProperties]

	def AddTemperatureProperty(self, temperature: float, et: float, ec: float, g: float, ftu: float, fcu: float, fsu: float, ef: float = None, ffu: float = None, k: float = None, c: float = None) -> FoamTemperature:
		'''
		Adds a temperature-dependent property for a material.
		
		:return: The newly created temperature-dependent property.
		'''
		return FoamTemperature(self._Entity.AddTemperatureProperty(temperature, et, ec, g, ftu, fcu, fsu, ef, ffu, k, c))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		'''
		Deletes a temperature-dependent property for a material.
		'''
		return self._Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> FoamTemperature:
		'''
		Retrieve a Temperature from this material's temperature-dependent properties. Allows a degree of tolerance to avoid issues with floating point numbers.
		
		:param LookupTemperature: Temperature to search for.
		
		:return: The temperature, if a matching one was found. Returns ``None`` if none exists.
		'''
		return FoamTemperature(self._Entity.GetTemperature(lookupTemperature))

	@MaterialFamilyName.setter
	def MaterialFamilyName(self, value: str) -> None:
		self._Entity.MaterialFamilyName = value

	@Name.setter
	def Name(self, value: str) -> None:
		self._Entity.Name = value

	@Wet.setter
	def Wet(self, value: bool) -> None:
		self._Entity.Wet = value

	@Density.setter
	def Density(self, value: float) -> None:
		self._Entity.Density = value

	@Form.setter
	def Form(self, value: str) -> None:
		self._Entity.Form = value

	@Specification.setter
	def Specification(self, value: str) -> None:
		self._Entity.Specification = value

	@MaterialDescription.setter
	def MaterialDescription(self, value: str) -> None:
		self._Entity.MaterialDescription = value

	@UserNote.setter
	def UserNote(self, value: str) -> None:
		self._Entity.UserNote = value

	@FemMaterialId.setter
	def FemMaterialId(self, value: int | None) -> None:
		self._Entity.FemMaterialId = value

	@Cost.setter
	def Cost(self, value: float | None) -> None:
		self._Entity.Cost = value

	@BucklingStiffnessKnockdown.setter
	def BucklingStiffnessKnockdown(self, value: float | None) -> None:
		self._Entity.BucklingStiffnessKnockdown = value

	@Absorption.setter
	def Absorption(self, value: float | None) -> None:
		self._Entity.Absorption = value

	@Manufacturer.setter
	def Manufacturer(self, value: str) -> None:
		self._Entity.Manufacturer = value

	def Save(self) -> None:
		'''
		Save any changes to this foam material to the database.
		'''
		return self._Entity.Save()


class HoneycombTemperature:
	'''
	Honeycomb material temperature dependent properties.
	'''
	def __init__(self, honeycombTemperature: _api.HoneycombTemperature):
		self._Entity = honeycombTemperature

	@property
	def Temperature(self) -> float:
		'''
		Temperature. Eng: Farenheit / SI: Celsius
		'''
		return self._Entity.Temperature

	@property
	def Et(self) -> float:
		'''
		Et. Eng: Msi / SI: GPa
		'''
		return self._Entity.Et

	@property
	def Ec(self) -> float:
		'''
		Ec. Eng: Msi / SI: GPa
		'''
		return self._Entity.Ec

	@property
	def Gw(self) -> float:
		'''
		Gw. Eng: Msi / SI: GPa
		'''
		return self._Entity.Gw

	@property
	def Gl(self) -> float:
		'''
		Gl. Eng: Msi / SI: GPa
		'''
		return self._Entity.Gl

	@property
	def Ftu(self) -> float:
		'''
		Ftu, Tension. Eng: ksi / SI: MPa
		'''
		return self._Entity.Ftu

	@property
	def Fcus(self) -> float:
		'''
		Stabilized, Fcus. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fcus

	@property
	def Fcub(self) -> float:
		'''
		Bare, Fcub. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fcub

	@property
	def Fcuc(self) -> float:
		'''
		Crush, Fcuc. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fcuc

	@property
	def Fsuw(self) -> float:
		'''
		Fsuw. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fsuw

	@property
	def Fsul(self) -> float:
		'''
		Fsul. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fsul

	@property
	def SScfl(self) -> float | None:
		'''
		Factor at 0.5" thick, SScfl.
		'''
		return self._Entity.SScfl

	@property
	def SScfh(self) -> float | None:
		'''
		Factor at 1.5" thick, SScfl.
		'''
		return self._Entity.SScfh

	@property
	def Kl(self) -> float | None:
		'''
		Kl. Eng: B-ft/ft^2/hr/Farenheit / SI: W/m/Kelvin
		'''
		return self._Entity.Kl

	@property
	def Kw(self) -> float | None:
		'''
		Kw. Eng: B-ft/ft^2/hr/Farenheit / SI: W/m/Kelvin
		'''
		return self._Entity.Kw

	@property
	def Kt(self) -> float | None:
		'''
		Kt. Eng: B-ft/ft^2/hr/Farenheit / SI: W/m/Kelvin
		'''
		return self._Entity.Kt

	@property
	def C(self) -> float | None:
		'''
		C. Eng: B/lb/Farenheit / SI: J/g/K
		'''
		return self._Entity.C

	@Temperature.setter
	def Temperature(self, value: float) -> None:
		self._Entity.Temperature = value

	@Et.setter
	def Et(self, value: float) -> None:
		self._Entity.Et = value

	@Ec.setter
	def Ec(self, value: float) -> None:
		self._Entity.Ec = value

	@Gw.setter
	def Gw(self, value: float) -> None:
		self._Entity.Gw = value

	@Gl.setter
	def Gl(self, value: float) -> None:
		self._Entity.Gl = value

	@Ftu.setter
	def Ftu(self, value: float) -> None:
		self._Entity.Ftu = value

	@Fcus.setter
	def Fcus(self, value: float) -> None:
		self._Entity.Fcus = value

	@Fcub.setter
	def Fcub(self, value: float) -> None:
		self._Entity.Fcub = value

	@Fcuc.setter
	def Fcuc(self, value: float) -> None:
		self._Entity.Fcuc = value

	@Fsuw.setter
	def Fsuw(self, value: float) -> None:
		self._Entity.Fsuw = value

	@Fsul.setter
	def Fsul(self, value: float) -> None:
		self._Entity.Fsul = value

	@SScfl.setter
	def SScfl(self, value: float | None) -> None:
		self._Entity.SScfl = value

	@SScfh.setter
	def SScfh(self, value: float | None) -> None:
		self._Entity.SScfh = value

	@Kl.setter
	def Kl(self, value: float | None) -> None:
		self._Entity.Kl = value

	@Kw.setter
	def Kw(self, value: float | None) -> None:
		self._Entity.Kw = value

	@Kt.setter
	def Kt(self, value: float | None) -> None:
		self._Entity.Kt = value

	@C.setter
	def C(self, value: float | None) -> None:
		self._Entity.C = value


class Honeycomb:
	'''
	Honeycomb material.
	'''
	def __init__(self, honeycomb: _api.Honeycomb):
		self._Entity = honeycomb

	@property
	def MaterialFamilyName(self) -> str:
		'''
		The material family for this material. When the material is saved, a new family will be created if none matching this name exists.
		'''
		return self._Entity.MaterialFamilyName

	@property
	def Id(self) -> int:
		return self._Entity.Id

	@property
	def CreationDate(self) -> DateTime:
		'''
		Date the material was created.
		'''
		return self._Entity.CreationDate

	@property
	def ModificationDate(self) -> DateTime:
		'''
		Most recent modification date of the material.
		'''
		return self._Entity.ModificationDate

	@property
	def Name(self) -> str:
		'''
		Name of this material.
		'''
		return self._Entity.Name

	@property
	def Wet(self) -> bool:
		return self._Entity.Wet

	@property
	def Density(self) -> float:
		'''
		Density. Eng: lbm/in^3 / SI: kg/m^3
		'''
		return self._Entity.Density

	@property
	def Form(self) -> str:
		return self._Entity.Form

	@property
	def Specification(self) -> str:
		return self._Entity.Specification

	@property
	def MaterialDescription(self) -> str:
		return self._Entity.MaterialDescription

	@property
	def UserNote(self) -> str:
		return self._Entity.UserNote

	@property
	def FemMaterialId(self) -> int | None:
		'''
		Linked FEM Material ID. Null if none exists.
		'''
		return self._Entity.FemMaterialId

	@property
	def Cost(self) -> float | None:
		return self._Entity.Cost

	@property
	def CellSize(self) -> float | None:
		'''
		Cell size. Eng: in / SI: mm
		'''
		return self._Entity.CellSize

	@property
	def Manufacturer(self) -> str:
		return self._Entity.Manufacturer

	@property
	def HoneycombTemperatureProperties(self) -> list[HoneycombTemperature]:
		'''
		List of this material's temperature-dependent properties.
		'''
		return [HoneycombTemperature(honeycombTemperature) for honeycombTemperature in self._Entity.HoneycombTemperatureProperties]

	def AddTemperatureProperty(self, temperature: float, et: float, ec: float, gw: float, gl: float, ftu: float, fcus: float, fcub: float, fcuc: float, fsuw: float, fsul: float, sScfl: float = None, sScfh: float = None, k1: float = None, k2: float = None, k3: float = None, c: float = None) -> HoneycombTemperature:
		'''
		Adds a temperature-dependent property for a material.
		
		:return: The newly created temperature-dependent property.
		'''
		return HoneycombTemperature(self._Entity.AddTemperatureProperty(temperature, et, ec, gw, gl, ftu, fcus, fcub, fcuc, fsuw, fsul, sScfl, sScfh, k1, k2, k3, c))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		'''
		Deletes a temperature-dependent property for a material.
		'''
		return self._Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> HoneycombTemperature:
		'''
		Retrieve a Temperature from this material's temperature-dependent properties. Allows a degree of tolerance to avoid issues with floating point numbers.
		
		:param LookupTemperature: Temperature to search for.
		
		:return: The temperature, if a matching one was found. Returns ``None`` if none exists.
		'''
		return HoneycombTemperature(self._Entity.GetTemperature(lookupTemperature))

	@MaterialFamilyName.setter
	def MaterialFamilyName(self, value: str) -> None:
		self._Entity.MaterialFamilyName = value

	@Name.setter
	def Name(self, value: str) -> None:
		self._Entity.Name = value

	@Wet.setter
	def Wet(self, value: bool) -> None:
		self._Entity.Wet = value

	@Density.setter
	def Density(self, value: float) -> None:
		self._Entity.Density = value

	@Form.setter
	def Form(self, value: str) -> None:
		self._Entity.Form = value

	@Specification.setter
	def Specification(self, value: str) -> None:
		self._Entity.Specification = value

	@MaterialDescription.setter
	def MaterialDescription(self, value: str) -> None:
		self._Entity.MaterialDescription = value

	@UserNote.setter
	def UserNote(self, value: str) -> None:
		self._Entity.UserNote = value

	@FemMaterialId.setter
	def FemMaterialId(self, value: int | None) -> None:
		self._Entity.FemMaterialId = value

	@Cost.setter
	def Cost(self, value: float | None) -> None:
		self._Entity.Cost = value

	@CellSize.setter
	def CellSize(self, value: float | None) -> None:
		self._Entity.CellSize = value

	@Manufacturer.setter
	def Manufacturer(self, value: str) -> None:
		self._Entity.Manufacturer = value

	def Save(self) -> None:
		'''
		Save any changes to this honeycomb material to the database.
		'''
		return self._Entity.Save()


class IsotropicTemperature:
	'''
	Isotropic material temperature dependent properties.
	'''
	def __init__(self, isotropicTemperature: _api.IsotropicTemperature):
		self._Entity = isotropicTemperature

	@property
	def Temperature(self) -> float:
		'''
		Temperature. Eng: Farenheit / SI: Celsius
		'''
		return self._Entity.Temperature

	@property
	def Et(self) -> float:
		'''
		Et. Eng: Msi / SI: GPa
		'''
		return self._Entity.Et

	@property
	def Ec(self) -> float:
		'''
		Ec. Eng: Msi / SI: GPa
		'''
		return self._Entity.Ec

	@property
	def G(self) -> float:
		'''
		G. Eng: Msi / SI: GPa
		'''
		return self._Entity.G

	@property
	def n(self) -> float | None:
		'''
		n, Ramberg-Osgood.
		'''
		return self._Entity.n

	@property
	def F02(self) -> float | None:
		'''
		F02, Ramberg-Osgood. Eng: Msi / SI: GPa
		'''
		return self._Entity.F02

	@property
	def FtuL(self) -> float:
		'''
		FtuL. Eng: ksi / SI: MPa
		'''
		return self._Entity.FtuL

	@property
	def FtyL(self) -> float:
		'''
		FtyL. Eng: ksi / SI: MPa
		'''
		return self._Entity.FtyL

	@property
	def FcyL(self) -> float:
		'''
		FcyL. Eng: ksi / SI: MPa
		'''
		return self._Entity.FcyL

	@property
	def FtuLT(self) -> float:
		'''
		FtuLT. Eng: ksi / SI: MPa
		'''
		return self._Entity.FtuLT

	@property
	def FtyLT(self) -> float:
		'''
		FtyLT. Eng: ksi / SI: MPa
		'''
		return self._Entity.FtyLT

	@property
	def FcyLT(self) -> float:
		'''
		FcyLT. Eng: ksi / SI: MPa
		'''
		return self._Entity.FcyLT

	@property
	def Fsu(self) -> float:
		'''
		Fsu. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fsu

	@property
	def Fbru15(self) -> float | None:
		'''
		Fbru15. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fbru15

	@property
	def Fbry15(self) -> float | None:
		'''
		Fbry15. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fbry15

	@property
	def Fbru20(self) -> float | None:
		'''
		Fbru20. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fbru20

	@property
	def Fbry20(self) -> float | None:
		'''
		F02. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fbry20

	@property
	def alpha(self) -> float:
		'''
		alpha. Eng: µin/in/Farenheit / SI: µm/m/Kelvin
		'''
		return self._Entity.alpha

	@property
	def K(self) -> float | None:
		'''
		K. Eng: B-ft/ft^2/hr/Farenheit / SI: W/m/Kelvin
		'''
		return self._Entity.K

	@property
	def C(self) -> float | None:
		'''
		C. Eng: B/lb/Farenheit / SI: J/g/K
		'''
		return self._Entity.C

	@property
	def etyL(self) -> float | None:
		'''
		Tension, etyL. Eng: µin/in / SI: µm/m
		'''
		return self._Entity.etyL

	@property
	def ecyL(self) -> float | None:
		'''
		Compression, ecyL. Eng: µin/in / SI: µm/m
		'''
		return self._Entity.ecyL

	@property
	def etyLT(self) -> float | None:
		'''
		Tension, etyLT. Eng: µin/in / SI: µm/m
		'''
		return self._Entity.etyLT

	@property
	def ecyLT(self) -> float | None:
		'''
		Compression, ecyLT. Eng: µin/in / SI: µm/m
		'''
		return self._Entity.ecyLT

	@property
	def esu(self) -> float | None:
		'''
		Shear, Ultimate, esu. Eng: µin/in / SI: µm/m
		'''
		return self._Entity.esu

	@property
	def Fpadh(self) -> float | None:
		'''
		Peel Stress, Fpadh. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fpadh

	@property
	def Fsadh(self) -> float | None:
		'''
		Interlaminar Shear Stress, Fsadh. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fsadh

	@property
	def esadh(self) -> float | None:
		'''
		Shear Strain, Eng: µin/in / SI: µm/m.
		'''
		return self._Entity.esadh

	@property
	def cd(self) -> float | None:
		'''
		Characteristic Distance. Eng: in / SI: m
		'''
		return self._Entity.cd

	@property
	def Ffwt(self) -> float | None:
		'''
		Flatwise Tension, Ffwt. Eng: ksi / SI: MPa
		'''
		return self._Entity.Ffwt

	@property
	def Ffxz(self) -> float | None:
		'''
		Shear, Longitudinal, Ffxz. Eng: ksi / SI: MPa
		'''
		return self._Entity.Ffxz

	@property
	def Ffyz(self) -> float | None:
		'''
		Shear, Transverse, Ffyz. Eng: ksi / SI: MPa
		'''
		return self._Entity.Ffyz

	@property
	def FtFatigue(self) -> float | None:
		'''
		Tension, FtFatigue. Eng: ksi / SI: MPa
		'''
		return self._Entity.FtFatigue

	@property
	def FcFatigue(self) -> float | None:
		'''
		Compression, FtFatigue. Eng: ksi / SI: MPa
		'''
		return self._Entity.FcFatigue

	@Temperature.setter
	def Temperature(self, value: float) -> None:
		self._Entity.Temperature = value

	@Et.setter
	def Et(self, value: float) -> None:
		self._Entity.Et = value

	@Ec.setter
	def Ec(self, value: float) -> None:
		self._Entity.Ec = value

	@G.setter
	def G(self, value: float) -> None:
		self._Entity.G = value

	@n.setter
	def n(self, value: float | None) -> None:
		self._Entity.n = value

	@F02.setter
	def F02(self, value: float | None) -> None:
		self._Entity.F02 = value

	@FtuL.setter
	def FtuL(self, value: float) -> None:
		self._Entity.FtuL = value

	@FtyL.setter
	def FtyL(self, value: float) -> None:
		self._Entity.FtyL = value

	@FcyL.setter
	def FcyL(self, value: float) -> None:
		self._Entity.FcyL = value

	@FtuLT.setter
	def FtuLT(self, value: float) -> None:
		self._Entity.FtuLT = value

	@FtyLT.setter
	def FtyLT(self, value: float) -> None:
		self._Entity.FtyLT = value

	@FcyLT.setter
	def FcyLT(self, value: float) -> None:
		self._Entity.FcyLT = value

	@Fsu.setter
	def Fsu(self, value: float) -> None:
		self._Entity.Fsu = value

	@Fbru15.setter
	def Fbru15(self, value: float | None) -> None:
		self._Entity.Fbru15 = value

	@Fbry15.setter
	def Fbry15(self, value: float | None) -> None:
		self._Entity.Fbry15 = value

	@Fbru20.setter
	def Fbru20(self, value: float | None) -> None:
		self._Entity.Fbru20 = value

	@Fbry20.setter
	def Fbry20(self, value: float | None) -> None:
		self._Entity.Fbry20 = value

	@alpha.setter
	def alpha(self, value: float) -> None:
		self._Entity.alpha = value

	@K.setter
	def K(self, value: float | None) -> None:
		self._Entity.K = value

	@C.setter
	def C(self, value: float | None) -> None:
		self._Entity.C = value

	@etyL.setter
	def etyL(self, value: float | None) -> None:
		self._Entity.etyL = value

	@ecyL.setter
	def ecyL(self, value: float | None) -> None:
		self._Entity.ecyL = value

	@etyLT.setter
	def etyLT(self, value: float | None) -> None:
		self._Entity.etyLT = value

	@ecyLT.setter
	def ecyLT(self, value: float | None) -> None:
		self._Entity.ecyLT = value

	@esu.setter
	def esu(self, value: float | None) -> None:
		self._Entity.esu = value

	@Fpadh.setter
	def Fpadh(self, value: float | None) -> None:
		self._Entity.Fpadh = value

	@Fsadh.setter
	def Fsadh(self, value: float | None) -> None:
		self._Entity.Fsadh = value

	@esadh.setter
	def esadh(self, value: float | None) -> None:
		self._Entity.esadh = value

	@cd.setter
	def cd(self, value: float | None) -> None:
		self._Entity.cd = value

	@Ffwt.setter
	def Ffwt(self, value: float | None) -> None:
		self._Entity.Ffwt = value

	@Ffxz.setter
	def Ffxz(self, value: float | None) -> None:
		self._Entity.Ffxz = value

	@Ffyz.setter
	def Ffyz(self, value: float | None) -> None:
		self._Entity.Ffyz = value

	@FtFatigue.setter
	def FtFatigue(self, value: float | None) -> None:
		self._Entity.FtFatigue = value

	@FcFatigue.setter
	def FcFatigue(self, value: float | None) -> None:
		self._Entity.FcFatigue = value


class Isotropic:
	'''
	Isotropic material.
	'''
	def __init__(self, isotropic: _api.Isotropic):
		self._Entity = isotropic

	@property
	def MaterialFamilyName(self) -> str:
		'''
		The material family for this material. When the material is saved, a new family will be created if none matching this name exists.
		'''
		return self._Entity.MaterialFamilyName

	@property
	def Id(self) -> int:
		return self._Entity.Id

	@property
	def CreationDate(self) -> DateTime:
		'''
		Date the material was created.
		'''
		return self._Entity.CreationDate

	@property
	def ModificationDate(self) -> DateTime:
		'''
		Most recent modification date of the material.
		'''
		return self._Entity.ModificationDate

	@property
	def Name(self) -> str:
		'''
		Name of this material.
		'''
		return self._Entity.Name

	@property
	def Form(self) -> str:
		return self._Entity.Form

	@property
	def Specification(self) -> str:
		return self._Entity.Specification

	@property
	def Temper(self) -> str:
		return self._Entity.Temper

	@property
	def Basis(self) -> str:
		return self._Entity.Basis

	@property
	def Density(self) -> float:
		'''
		Density. Eng: lbm/in^3 / SI: kg/m^3
		'''
		return self._Entity.Density

	@property
	def MaterialDescription(self) -> str:
		return self._Entity.MaterialDescription

	@property
	def UserNote(self) -> str:
		return self._Entity.UserNote

	@property
	def FemMaterialId(self) -> int | None:
		'''
		Linked FEM Material ID. Null if none exists.
		'''
		return self._Entity.FemMaterialId

	@property
	def Cost(self) -> float | None:
		return self._Entity.Cost

	@property
	def BucklingStiffnessKnockdown(self) -> float | None:
		return self._Entity.BucklingStiffnessKnockdown

	@property
	def IsotropicTemperatureProperties(self) -> list[IsotropicTemperature]:
		'''
		List of this material's temperature-dependent properties.
		'''
		return [IsotropicTemperature(isotropicTemperature) for isotropicTemperature in self._Entity.IsotropicTemperatureProperties]

	def AddTemperatureProperty(self, temperature: float, et: float, ec: float, g: float, ftuL: float, ftyL: float, fcyL: float, ftuLT: float, ftyLT: float, fcyLT: float, fsu: float, alpha: float, n: float = None, f02: float = None, k: float = None, c: float = None, fbru15: float = None, fbry15: float = None, fbru20: float = None, fbry20: float = None, etyL: float = None, ecyL: float = None, etyLT: float = None, ecyLT: float = None, esu: float = None, fpadh: float = None, fsadh: float = None, esadh: float = None, cd: float = None, ffwt: float = None, ffxz: float = None, ffyz: float = None, ftFatigue: float = None, fcFatigue: float = None) -> IsotropicTemperature:
		'''
		Adds a temperature-dependent property for a material.
		
		:return: The newly created temperature-dependent property.
		'''
		return IsotropicTemperature(self._Entity.AddTemperatureProperty(temperature, et, ec, g, ftuL, ftyL, fcyL, ftuLT, ftyLT, fcyLT, fsu, alpha, n, f02, k, c, fbru15, fbry15, fbru20, fbry20, etyL, ecyL, etyLT, ecyLT, esu, fpadh, fsadh, esadh, cd, ffwt, ffxz, ffyz, ftFatigue, fcFatigue))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		'''
		Deletes a temperature-dependent property for a material.
		'''
		return self._Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> IsotropicTemperature:
		'''
		Retrieve a Temperature from this material's temperature-dependent properties. Allows a degree of tolerance to avoid issues with floating point numbers.
		
		:param LookupTemperature: Temperature to search for.
		
		:return: The temperature, if a matching one was found. Returns ``None`` if none exists.
		'''
		return IsotropicTemperature(self._Entity.GetTemperature(lookupTemperature))

	@MaterialFamilyName.setter
	def MaterialFamilyName(self, value: str) -> None:
		self._Entity.MaterialFamilyName = value

	@Name.setter
	def Name(self, value: str) -> None:
		self._Entity.Name = value

	@Form.setter
	def Form(self, value: str) -> None:
		self._Entity.Form = value

	@Specification.setter
	def Specification(self, value: str) -> None:
		self._Entity.Specification = value

	@Temper.setter
	def Temper(self, value: str) -> None:
		self._Entity.Temper = value

	@Basis.setter
	def Basis(self, value: str) -> None:
		self._Entity.Basis = value

	@Density.setter
	def Density(self, value: float) -> None:
		self._Entity.Density = value

	@MaterialDescription.setter
	def MaterialDescription(self, value: str) -> None:
		self._Entity.MaterialDescription = value

	@UserNote.setter
	def UserNote(self, value: str) -> None:
		self._Entity.UserNote = value

	@FemMaterialId.setter
	def FemMaterialId(self, value: int | None) -> None:
		self._Entity.FemMaterialId = value

	@Cost.setter
	def Cost(self, value: float | None) -> None:
		self._Entity.Cost = value

	@BucklingStiffnessKnockdown.setter
	def BucklingStiffnessKnockdown(self, value: float | None) -> None:
		self._Entity.BucklingStiffnessKnockdown = value

	def Save(self) -> None:
		'''
		Save any changes to this isotropic material to the database.
		'''
		return self._Entity.Save()


class LaminateBase(ABC):
	def __init__(self, laminateBase: _api.LaminateBase):
		self._Entity = laminateBase

	@property
	def Id(self) -> int:
		return self._Entity.Id

	@property
	def Name(self) -> str:
		return self._Entity.Name

	@property
	def IsEditable(self) -> bool:
		return self._Entity.IsEditable

	@property
	def MaterialFamilyName(self) -> str:
		return self._Entity.MaterialFamilyName

	@property
	def LayerCount(self) -> int:
		'''
		The total number of layers in this laminate.
		'''
		return self._Entity.LayerCount

	@property
	def Density(self) -> float:
		'''
		Density. Eng: lbm/in^3 / SI: kg/m^3
		'''
		return self._Entity.Density

	@property
	def Thickness(self) -> float:
		'''
		Thickness. Eng: in / SI: mm
		'''
		return self._Entity.Thickness

	@property
	def LaminateFamilyId(self) -> int | None:
		return self._Entity.LaminateFamilyId

	@property
	def LaminateFamilyOrder(self) -> int | None:
		return self._Entity.LaminateFamilyOrder

	@property
	def HyperLaminate(self) -> bool:
		return self._Entity.HyperLaminate

	@abstractmethod
	def Save(self) -> None:
		'''
		Save the laminate.
		'''
		return self._Entity.Save()

	@Name.setter
	def Name(self, value: str) -> None:
		self._Entity.Name = value

	@MaterialFamilyName.setter
	def MaterialFamilyName(self, value: str) -> None:
		self._Entity.MaterialFamilyName = value


class LaminateFamily(IdNameEntity):
	def __init__(self, laminateFamily: _api.LaminateFamily):
		self._Entity = laminateFamily

	@property
	def Laminates(self) -> list[LaminateBase]:
		laminates = []
		subclasses = {x.__name__: x for x in _all_subclasses(LaminateBase)}
		for laminateBase in self._Entity.Laminates:
			if type(laminateBase).__name__ in subclasses.keys():
				thisType = subclasses[type(laminateBase).__name__]
				laminates.append(thisType(laminateBase))
			else:
				raise Exception(f"Could not wrap item in Laminates. This should not happen.")
		return laminates

	@property
	def ModificationDate(self) -> DateTime:
		'''
		Most recent modification date of the material.
		'''
		return self._Entity.ModificationDate

	@property
	def PlankSetting(self) -> types.LaminateFamilySettingType:
		result = self._Entity.PlankSetting
		return types.LaminateFamilySettingType[result.ToString()] if result is not None else None

	@property
	def PlankMinRatio(self) -> float:
		return self._Entity.PlankMinRatio

	@property
	def PlankMaxRatio(self) -> float:
		return self._Entity.PlankMaxRatio

	@property
	def FootChargeSetting(self) -> types.LaminateFamilySettingType:
		result = self._Entity.FootChargeSetting
		return types.LaminateFamilySettingType[result.ToString()] if result is not None else None

	@property
	def FootChargeMinRatio(self) -> float:
		return self._Entity.FootChargeMinRatio

	@property
	def FootChargeMaxRatio(self) -> float:
		return self._Entity.FootChargeMaxRatio

	@property
	def WebChargeSetting(self) -> types.LaminateFamilySettingType:
		result = self._Entity.WebChargeSetting
		return types.LaminateFamilySettingType[result.ToString()] if result is not None else None

	@property
	def WebChargeMinRatio(self) -> float:
		return self._Entity.WebChargeMinRatio

	@property
	def WebChargeMaxRatio(self) -> float:
		return self._Entity.WebChargeMaxRatio

	@property
	def CapChargeSetting(self) -> types.LaminateFamilySettingType:
		result = self._Entity.CapChargeSetting
		return types.LaminateFamilySettingType[result.ToString()] if result is not None else None

	@property
	def CapChargeMinRatio(self) -> float:
		return self._Entity.CapChargeMinRatio

	@property
	def CapChargeMaxRatio(self) -> float:
		return self._Entity.CapChargeMaxRatio

	@property
	def CapCoverSetting(self) -> types.LaminateFamilySettingType:
		result = self._Entity.CapCoverSetting
		return types.LaminateFamilySettingType[result.ToString()] if result is not None else None

	@property
	def CapCoverMinRatio(self) -> float:
		return self._Entity.CapCoverMinRatio

	@property
	def CapCoverMaxRatio(self) -> float:
		return self._Entity.CapCoverMaxRatio

	@property
	def DropPattern(self) -> types.PlyDropPattern:
		result = self._Entity.DropPattern
		return types.PlyDropPattern[result.ToString()] if result is not None else None

	@property
	def LaminateStiffenerProfile(self) -> types.StiffenerProfile | None:
		result = self._Entity.LaminateStiffenerProfile
		return types.StiffenerProfile[result.ToString()] if result is not None else None


class LaminateLayerBase(ABC):
	def __init__(self, laminateLayerBase: _api.LaminateLayerBase):
		self._Entity = laminateLayerBase

	@property
	def LayerId(self) -> int:
		'''
		The index of the layer.
		'''
		return self._Entity.LayerId

	@property
	def LayerMaterial(self) -> str:
		'''
		Material used in the ply layer.
		'''
		return self._Entity.LayerMaterial

	@property
	def LayerMaterialType(self) -> types.MaterialType:
		'''
		Type of material used in the ply layer.
		'''
		result = self._Entity.LayerMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def Angle(self) -> float:
		'''
		Ply angle.
		'''
		return self._Entity.Angle

	@property
	def Thickness(self) -> float:
		'''
		Length. English Units: in; SI Units: millimeters.
		'''
		return self._Entity.Thickness

	@property
	def IsFabric(self) -> bool:
		return self._Entity.IsFabric

	def SetThickness(self, thickness: float) -> None:
		'''
		Set the thickness of a layer.
		
		:raises ``System.InvalidOperationException``: Throws if the material of the layer is set to an orthotropic.
		'''
		return self._Entity.SetThickness(thickness)

	@overload
	def SetMaterial(self, matId: int) -> bool:
		'''
		Sets the material of a layer by id.
		
		:return: False if the material does not exist.
		'''
		...

	@overload
	def SetMaterial(self, matName: str) -> bool:
		'''
		Sets the material of a layer by name.
		
		:return: False if the material does not exist.
		'''
		...

	@Angle.setter
	@abstractmethod
	def Angle(self, value: float) -> None:
		self._Entity.Angle = value

	def SetMaterial(self, item1 = None) -> bool:
		'''
		Overload 1: ``SetMaterial(self, matId: int) -> bool``

		Sets the material of a layer by id.
		
		:return: False if the material does not exist.

		Overload 2: ``SetMaterial(self, matName: str) -> bool``

		Sets the material of a layer by name.
		
		:return: False if the material does not exist.
		'''
		if isinstance(item1, int):
			return self._Entity.SetMaterial(item1)

		if isinstance(item1, str):
			return self._Entity.SetMaterial(item1)

		return self._Entity.SetMaterial(item1)


class LaminateLayer(LaminateLayerBase):
	'''
	Layer in a non-stiffener laminate.
	'''
	def __init__(self, laminateLayer: _api.LaminateLayer):
		self._Entity = laminateLayer

	@property
	def LayerId(self) -> int:
		'''
		The index of the layer.
		'''
		return self._Entity.LayerId

	@property
	def LayerMaterialType(self) -> types.MaterialType:
		'''
		Type of material used in the layer.
		'''
		result = self._Entity.LayerMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def Angle(self) -> float:
		'''
		Layer angle.
		'''
		return self._Entity.Angle

	@property
	def Thickness(self) -> float:
		'''
		Length. English Units: in; SI Units: millimeters.
		'''
		return self._Entity.Thickness

	@property
	def IsFabric(self) -> bool:
		return self._Entity.IsFabric

	@Angle.setter
	def Angle(self, value: float) -> None:
		self._Entity.Angle = value

	@overload
	def SetMaterial(self, matId: int) -> bool:
		'''
		Sets the material of a layer by id.
		
		:return: False if the material does not exist.
		'''
		...

	@overload
	def SetMaterial(self, matName: str) -> bool:
		'''
		Sets the material of a layer by name.
		
		:return: False if the material does not exist.
		'''
		...

	def SetMaterial(self, item1 = None) -> bool:
		'''
		Overload 1: ``SetMaterial(self, matId: int) -> bool``

		Sets the material of a layer by id.
		
		:return: False if the material does not exist.

		Overload 2: ``SetMaterial(self, matName: str) -> bool``

		Sets the material of a layer by name.
		
		:return: False if the material does not exist.
		'''
		if isinstance(item1, int):
			return bool(super().SetMaterial(item1))

		if isinstance(item1, str):
			return bool(super().SetMaterial(item1))

		return self._Entity.SetMaterial(item1)


class Laminate(LaminateBase):
	'''
	Laminate
	'''
	def __init__(self, laminate: _api.Laminate):
		self._Entity = laminate

	@property
	def Layers(self) -> list[LaminateLayer]:
		return [LaminateLayer(laminateLayer) for laminateLayer in self._Entity.Layers]

	def AddLayer(self, materialName: str, angle: float, thickness: float = None) -> LaminateLayer:
		'''
		Adds a layer to the laminate.
		
		:param thickness: If the material is orthotropic, don't provide a thickness. For all other material types, providing a thickness is required.
		
		:return: The added layer.
		'''
		return LaminateLayer(self._Entity.AddLayer(materialName, angle, thickness))

	def InsertLayer(self, layerId: int, materialName: str, angle: float, thickness: float = None) -> LaminateLayer:
		'''
		Inserts a layer into the laminate before the layer with the specified ``layerId``.
		``layerId`` is 1 indexed.
		
		:param thickness: If the material is orthotropic, don't provide a thickness. For all other material types, providing a thickness is required.
		
		:return: The inserted layer.
		'''
		return LaminateLayer(self._Entity.InsertLayer(layerId, materialName, angle, thickness))

	def RemoveLayer(self, layerId: int) -> bool:
		'''
		Removes a layer from the laminate.
		
		:return: False if the specified layer is not found.
		'''
		return self._Entity.RemoveLayer(layerId)

	def Save(self) -> None:
		'''
		Save any changes to this laminate material to the database.
		'''
		return self._Entity.Save()


class StiffenerLaminateLayer(LaminateLayerBase):
	'''
	Stiffener Laminate Layer
	'''
	def __init__(self, stiffenerLaminateLayer: _api.StiffenerLaminateLayer):
		self._Entity = stiffenerLaminateLayer

	@property
	def LayerLocations(self) -> list[types.StiffenerLaminateLayerLocation]:
		return [types.StiffenerLaminateLayerLocation[stiffenerLaminateLayerLocation.ToString()] for stiffenerLaminateLayerLocation in self._Entity.LayerLocations]

	@property
	def LayerId(self) -> int:
		return self._Entity.LayerId

	@property
	def LayerMaterialType(self) -> types.MaterialType:
		result = self._Entity.LayerMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def Angle(self) -> float:
		return self._Entity.Angle

	@property
	def Thickness(self) -> float:
		return self._Entity.Thickness

	@property
	def IsFabric(self) -> bool:
		return self._Entity.IsFabric

	def AddLayerLocation(self, location: types.StiffenerLaminateLayerLocation) -> None:
		'''
		Add a layer location to this layer.
		
		:raises ``System.InvalidOperationException``: Throws if this layer cannot have multiple locations assigned.
		:raises ``System.ArgumentException``: Throws if the given location is invalid for this layer.
		'''
		return self._Entity.AddLayerLocation(_types.StiffenerLaminateLayerLocation(types.GetEnumValue(location.value)))

	def RemoveLayerLocation(self, location: types.StiffenerLaminateLayerLocation) -> bool:
		'''
		Remove a layer location from LayerLocations.
		
		:return: False if there is only 1 layer location to start with or if the location is not found.
		'''
		return self._Entity.RemoveLayerLocation(_types.StiffenerLaminateLayerLocation(types.GetEnumValue(location.value)))

	@Angle.setter
	def Angle(self, value: float) -> None:
		self._Entity.Angle = value

	@overload
	def SetMaterial(self, matId: int) -> bool:
		'''
		Sets the material of a layer by id.
		
		:return: False if the material does not exist.
		'''
		...

	@overload
	def SetMaterial(self, matName: str) -> bool:
		'''
		Sets the material of a layer by name.
		
		:return: False if the material does not exist.
		'''
		...

	def SetMaterial(self, item1 = None) -> bool:
		'''
		Overload 1: ``SetMaterial(self, matId: int) -> bool``

		Sets the material of a layer by id.
		
		:return: False if the material does not exist.

		Overload 2: ``SetMaterial(self, matName: str) -> bool``

		Sets the material of a layer by name.
		
		:return: False if the material does not exist.
		'''
		if isinstance(item1, int):
			return bool(super().SetMaterial(item1))

		if isinstance(item1, str):
			return bool(super().SetMaterial(item1))

		return self._Entity.SetMaterial(item1)


class StiffenerLaminate(LaminateBase):
	'''
	Stiffener Laminate
	'''
	def __init__(self, stiffenerLaminate: _api.StiffenerLaminate):
		self._Entity = stiffenerLaminate

	@property
	def Layers(self) -> list[StiffenerLaminateLayer]:
		'''
		Laminate layers.
		'''
		return [StiffenerLaminateLayer(stiffenerLaminateLayer) for stiffenerLaminateLayer in self._Entity.Layers]

	@property
	def LaminateStiffenerProfile(self) -> types.StiffenerProfile:
		result = self._Entity.LaminateStiffenerProfile
		return types.StiffenerProfile[result.ToString()] if result is not None else None

	@overload
	def AddLayer(self, location: types.StiffenerLaminateLayerLocation, materialName: str, angle: float, thickness: float = None) -> StiffenerLaminateLayer:
		'''
		Add layer to stiffener laminate by section.
		
		:param thickness: If the material is orthotropic, don't provide a thickness. For all other material types, providing a thickness is required.
		
		:return: The created StiffenerLaminateLayer.
		
		:raises ``System.ArgumentException``:
		'''
		...

	@overload
	def InsertLayer(self, location: types.StiffenerLaminateLayerLocation, layerId: int, materialName: str, angle: float, thickness: float = None) -> StiffenerLaminateLayer:
		'''
		Insert layer into stiffener laminate at ``layerId`` by section.
		``layerId`` is 1 indexed.
		
		:param thickness: If the material is orthotropic, don't provide a thickness.
		
		:raises ``System.ArgumentException``:
		'''
		...

	@overload
	def AddLayer(self, locations: tuple[types.StiffenerLaminateLayerLocation], materialName: str, angle: float, thickness: float = None) -> StiffenerLaminateLayer:
		'''
		Add layer to stiffener laminate by collection of sections.
		
		:param thickness: If the material is orthotropic, don't provide a thickness. For all other material types, providing a thickness is required.
		
		:raises ``System.ArgumentException``:
		'''
		...

	@overload
	def InsertLayer(self, locations: tuple[types.StiffenerLaminateLayerLocation], layerId: int, materialName: str, angle: float, thickness: float = None) -> StiffenerLaminateLayer:
		'''
		Insert layer into stiffener laminate at ``layerId`` by collection of sections.
		``layerId`` is 1 indexed.
		
		:param thickness: If the material is orthotropic, don't provide a thickness. For all other material types, providing a thickness is required.
		
		:raises ``System.ArgumentException``:
		'''
		...

	def RemoveLayer(self, layerId: int) -> bool:
		'''
		Remove a layer by ``layerId``.
		``layerId`` is 1 indexed.
		
		:return: False if the layerId does not correspond with a layer.
		'''
		return self._Entity.RemoveLayer(layerId)

	def Save(self) -> None:
		'''
		Save laminate to database.
		
		:raises ``System.InvalidOperationException``:
		'''
		return self._Entity.Save()

	def AddLayer(self, item1 = None, item2 = None, item3 = None, item4 = None) -> StiffenerLaminateLayer:
		'''
		Overload 1: ``AddLayer(self, location: types.StiffenerLaminateLayerLocation, materialName: str, angle: float, thickness: float = None) -> StiffenerLaminateLayer``

		Add layer to stiffener laminate by section.
		
		:param thickness: If the material is orthotropic, don't provide a thickness. For all other material types, providing a thickness is required.
		
		:return: The created StiffenerLaminateLayer.
		
		:raises ``System.ArgumentException``:

		Overload 2: ``AddLayer(self, locations: tuple[types.StiffenerLaminateLayerLocation], materialName: str, angle: float, thickness: float = None) -> StiffenerLaminateLayer``

		Add layer to stiffener laminate by collection of sections.
		
		:param thickness: If the material is orthotropic, don't provide a thickness. For all other material types, providing a thickness is required.
		
		:raises ``System.ArgumentException``:
		'''
		if isinstance(item1, types.StiffenerLaminateLayerLocation) and isinstance(item2, str) and (isinstance(item3, float) or isinstance(item3, int)) and (isinstance(item4, float) or item4 is None or isinstance(item4, int)):
			return StiffenerLaminateLayer(self._Entity.AddLayer(_types.StiffenerLaminateLayerLocation(types.GetEnumValue(item1.value)), item2, item3, item4))

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, types.StiffenerLaminateLayerLocation) for x in item1) and isinstance(item2, str) and (isinstance(item3, float) or isinstance(item3, int)) and (isinstance(item4, float) or item4 is None or isinstance(item4, int)):
			locationsList = List[_types.StiffenerLaminateLayerLocation]()
			if item1 is not None:
				for x in item1:
					if x is not None:
						locationsList.Add(_types.StiffenerLaminateLayerLocation(types.GetEnumValue(x.value)))
			locationsEnumerable = IEnumerable(locationsList)
			return StiffenerLaminateLayer(self._Entity.AddLayer(locationsEnumerable, item2, item3, item4))

		return StiffenerLaminateLayer(self._Entity.AddLayer(_types.StiffenerLaminateLayerLocation(types.GetEnumValue(item1.value)), item2, item3, item4))

	def InsertLayer(self, item1 = None, item2 = None, item3 = None, item4 = None, item5 = None) -> StiffenerLaminateLayer:
		'''
		Overload 1: ``InsertLayer(self, location: types.StiffenerLaminateLayerLocation, layerId: int, materialName: str, angle: float, thickness: float = None) -> StiffenerLaminateLayer``

		Insert layer into stiffener laminate at ``layerId`` by section.
		``layerId`` is 1 indexed.
		
		:param thickness: If the material is orthotropic, don't provide a thickness.
		
		:raises ``System.ArgumentException``:

		Overload 2: ``InsertLayer(self, locations: tuple[types.StiffenerLaminateLayerLocation], layerId: int, materialName: str, angle: float, thickness: float = None) -> StiffenerLaminateLayer``

		Insert layer into stiffener laminate at ``layerId`` by collection of sections.
		``layerId`` is 1 indexed.
		
		:param thickness: If the material is orthotropic, don't provide a thickness. For all other material types, providing a thickness is required.
		
		:raises ``System.ArgumentException``:
		'''
		if isinstance(item1, types.StiffenerLaminateLayerLocation) and isinstance(item2, int) and isinstance(item3, str) and (isinstance(item4, float) or isinstance(item4, int)) and (isinstance(item5, float) or item5 is None or isinstance(item5, int)):
			return StiffenerLaminateLayer(self._Entity.InsertLayer(_types.StiffenerLaminateLayerLocation(types.GetEnumValue(item1.value)), item2, item3, item4, item5))

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, types.StiffenerLaminateLayerLocation) for x in item1) and isinstance(item2, int) and isinstance(item3, str) and (isinstance(item4, float) or isinstance(item4, int)) and (isinstance(item5, float) or item5 is None or isinstance(item5, int)):
			locationsList = List[_types.StiffenerLaminateLayerLocation]()
			if item1 is not None:
				for x in item1:
					if x is not None:
						locationsList.Add(_types.StiffenerLaminateLayerLocation(types.GetEnumValue(x.value)))
			locationsEnumerable = IEnumerable(locationsList)
			return StiffenerLaminateLayer(self._Entity.InsertLayer(locationsEnumerable, item2, item3, item4, item5))

		return StiffenerLaminateLayer(self._Entity.InsertLayer(_types.StiffenerLaminateLayerLocation(types.GetEnumValue(item1.value)), item2, item3, item4, item5))


class OrthotropicCorrectionFactorBase(ABC):
	'''
	Orthotropic material correction factor.
	'''
	def __init__(self, orthotropicCorrectionFactorBase: _api.OrthotropicCorrectionFactorBase):
		self._Entity = orthotropicCorrectionFactorBase

	@property
	def CorrectionId(self) -> types.CorrectionId:
		'''
		Correction ID for this correction factor.
		'''
		result = self._Entity.CorrectionId
		return types.CorrectionId[result.ToString()] if result is not None else None

	@property
	def PropertyId(self) -> types.CorrectionProperty:
		'''
		Property for this correction factor.
		'''
		result = self._Entity.PropertyId
		return types.CorrectionProperty[result.ToString()] if result is not None else None


class OrthotropicCorrectionFactorPoint:
	'''
	Pointer to an Equation-based or Tabular Correction Factor.
	'''
	def __init__(self, orthotropicCorrectionFactorPoint: _api.OrthotropicCorrectionFactorPoint):
		self._Entity = orthotropicCorrectionFactorPoint

	def Create_OrthotropicCorrectionFactorPoint(property: types.CorrectionProperty, id: types.CorrectionId):
		return OrthotropicCorrectionFactorPoint(_api.OrthotropicCorrectionFactorPoint(_types.CorrectionProperty(types.GetEnumValue(property.value)), _types.CorrectionId(types.GetEnumValue(id.value))))

	@property
	def CorrectionProperty(self) -> types.CorrectionProperty:
		result = self._Entity.CorrectionProperty
		return types.CorrectionProperty[result.ToString()] if result is not None else None

	@property
	def CorrectionId(self) -> types.CorrectionId:
		result = self._Entity.CorrectionId
		return types.CorrectionId[result.ToString()] if result is not None else None

	@overload
	def Equals(self, other) -> bool:
		...

	@overload
	def Equals(self, obj: object) -> bool:
		...

	def Equals(self, item1 = None) -> bool:
		'''
		Overload 1: ``Equals(self, other) -> bool``

		Overload 2: ``Equals(self, obj: object) -> bool``
		'''
		if isinstance(item1, OrthotropicCorrectionFactorPoint):
			return self._Entity.Equals(item1._Entity)

		if isinstance(item1, object):
			return self._Entity.Equals(item1)

		return self._Entity.Equals(item1._Entity)

	def __hash__(self) -> int:
		return self._Entity.GetHashCode()


class OrthotropicCorrectionFactorValue:
	'''
	Orthotropic material equation-based correction factor value. (NOT TABULAR)
	'''
	def __init__(self, orthotropicCorrectionFactorValue: _api.OrthotropicCorrectionFactorValue):
		self._Entity = orthotropicCorrectionFactorValue

	@property
	def Property(self) -> types.CorrectionProperty:
		'''
		Property for the correction factor containing this value.
		'''
		result = self._Entity.Property
		return types.CorrectionProperty[result.ToString()] if result is not None else None

	@property
	def Correction(self) -> types.CorrectionId:
		'''
		Correction ID for the correction factor containing this value.
		'''
		result = self._Entity.Correction
		return types.CorrectionId[result.ToString()] if result is not None else None

	@property
	def Equation(self) -> types.CorrectionEquation:
		'''
		Equation for the correction factor containing this value.
		'''
		result = self._Entity.Equation
		return types.CorrectionEquation[result.ToString()] if result is not None else None

	@property
	def EquationParameter(self) -> types.EquationParameterId:
		'''
		Represents a parameter for a given equation.
		Specify with the EquationParameterName enum.
		'''
		result = self._Entity.EquationParameter
		return types.EquationParameterId[result.ToString()] if result is not None else None

	@property
	def Value(self) -> float | None:
		'''
		Actual value stored.
		'''
		return self._Entity.Value

	@Value.setter
	def Value(self, value: float | None) -> None:
		self._Entity.Value = value


class OrthotropicEquationCorrectionFactor(OrthotropicCorrectionFactorBase):
	'''
	Represents an equation-based orthotropic material correction factor.
	'''
	def __init__(self, orthotropicEquationCorrectionFactor: _api.OrthotropicEquationCorrectionFactor):
		self._Entity = orthotropicEquationCorrectionFactor

	@property
	def Equation(self) -> types.CorrectionEquation:
		'''
		Equation for this correction factor.
		'''
		result = self._Entity.Equation
		return types.CorrectionEquation[result.ToString()] if result is not None else None

	@property
	def OrthotropicCorrectionValues(self) -> dict[types.EquationParameterId, OrthotropicCorrectionFactorValue]:
		'''
		Dictionary of correction factor values for this correction factor.
		'''
		orthotropicCorrectionValuesDict = {}
		for kvp in self._Entity.OrthotropicCorrectionValues:
			orthotropicCorrectionValuesDict[types.EquationParameterId[kvp.Key.ToString()]] = OrthotropicCorrectionFactorValue(kvp.Value)

		return orthotropicCorrectionValuesDict

	def AddCorrectionFactorValue(self, equationParameterName: types.EquationParameterId, valueToAdd: float) -> OrthotropicCorrectionFactorValue:
		'''
		Add a correction factor value for a given correction factor.
		
		:param equationParameterName: This represents the parameter of the equation that should be changed.
		:param valueToAdd: This is the value that will be assigned to the chosen parameter.
		'''
		return OrthotropicCorrectionFactorValue(self._Entity.AddCorrectionFactorValue(_types.EquationParameterId(types.GetEnumValue(equationParameterName.value)), valueToAdd))


class TabularCorrectionFactorIndependentValue:
	'''
	Contains an independent value for a tabular correction factor row.
	'''
	def __init__(self, tabularCorrectionFactorIndependentValue: _api.TabularCorrectionFactorIndependentValue):
		self._Entity = tabularCorrectionFactorIndependentValue

	@property
	def BoolValue(self) -> bool:
		return self._Entity.BoolValue

	@property
	def DoubleValue(self) -> float:
		return self._Entity.DoubleValue

	@property
	def IntValue(self) -> int:
		return self._Entity.IntValue

	@property
	def ValueType(self) -> types.CorrectionValueType:
		result = self._Entity.ValueType
		return types.CorrectionValueType[result.ToString()] if result is not None else None


class TabularCorrectionFactorRow:
	'''
	Row data for a tabular correction factor.
	'''
	def __init__(self, tabularCorrectionFactorRow: _api.TabularCorrectionFactorRow):
		self._Entity = tabularCorrectionFactorRow

	@property
	def DependentValue(self) -> float:
		'''
		The "dependent value" K. The last item on the row.
		'''
		return self._Entity.DependentValue

	@property
	def IndependentValues(self) -> dict[types.CorrectionIndependentDefinition, TabularCorrectionFactorIndependentValue]:
		'''
		Data for the "independent values" on the given row, mapped by their CorrectionIndependentDefinition.
		This is everything but the "dependent value", i.e. the last value on the row on the form.
		'''
		independentValuesDict = {}
		for kvp in self._Entity.IndependentValues:
			independentValuesDict[types.CorrectionIndependentDefinition[kvp.Key.ToString()]] = TabularCorrectionFactorIndependentValue(kvp.Value)

		return independentValuesDict


class OrthotropicTabularCorrectionFactor(OrthotropicCorrectionFactorBase):
	'''
	Tabular correction factor.
	'''
	def __init__(self, orthotropicTabularCorrectionFactor: _api.OrthotropicTabularCorrectionFactor):
		self._Entity = orthotropicTabularCorrectionFactor

	@property
	def CorrectionFactorRows(self) -> dict[int, TabularCorrectionFactorRow]:
		'''
		Determine the correction factor rows for this tabular correction factor.
		Map of correctionPointId to row.
		'''
		correctionFactorRowsDict = {}
		for kvp in self._Entity.CorrectionFactorRows:
			correctionFactorRowsDict[int(kvp.Key)] = TabularCorrectionFactorRow(kvp.Value)

		return correctionFactorRowsDict

	@property
	def CorrectionIndependentDefinitions(self) -> set[types.CorrectionIndependentDefinition]:
		'''
		These correspond to the independent values for this correction factor.
		These are represented by the column headers on the correction factors form in the UI.
		'''
		return {types.CorrectionIndependentDefinition[correctionIndependentDefinition.ToString()] for correctionIndependentDefinition in self._Entity.CorrectionIndependentDefinitions}

	@overload
	def SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: float) -> None:
		'''
		Set independent value for a specified row and the independent value within the row.
		'''
		...

	@overload
	def SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: bool) -> None:
		'''
		Set independent value for a specified row and the independent value within the row.
		'''
		...

	@overload
	def SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: int) -> None:
		'''
		Set independent value for a specified row and the independent value within the row.
		'''
		...

	def SetKValue(self, correctionPointId: int, value: float) -> None:
		'''
		Set the dependent value for a specified row.
		'''
		return self._Entity.SetKValue(correctionPointId, value)

	def SetIndependentValue(self, item1 = None, item2 = None, item3 = None) -> None:
		'''
		Overload 1: ``SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: float) -> None``

		Set independent value for a specified row and the independent value within the row.

		Overload 2: ``SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: bool) -> None``

		Set independent value for a specified row and the independent value within the row.

		Overload 3: ``SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: int) -> None``

		Set independent value for a specified row and the independent value within the row.
		'''
		if isinstance(item1, int) and isinstance(item2, types.CorrectionIndependentDefinition) and (isinstance(item3, float) or isinstance(item3, int)):
			return self._Entity.SetIndependentValue(item1, _types.CorrectionIndependentDefinition(types.GetEnumValue(item2.value)), item3)

		if isinstance(item1, int) and isinstance(item2, types.CorrectionIndependentDefinition) and isinstance(item3, bool):
			return self._Entity.SetIndependentValue(item1, _types.CorrectionIndependentDefinition(types.GetEnumValue(item2.value)), item3)

		if isinstance(item1, int) and isinstance(item2, types.CorrectionIndependentDefinition) and isinstance(item3, int):
			return self._Entity.SetIndependentValue(item1, _types.CorrectionIndependentDefinition(types.GetEnumValue(item2.value)), item3)

		return self._Entity.SetIndependentValue(item1, _types.CorrectionIndependentDefinition(types.GetEnumValue(item2.value)), item3)


class OrthotropicAllowableCurvePoint:
	'''
	Represents a point on a laminate allowable curve.
	'''
	def __init__(self, orthotropicAllowableCurvePoint: _api.OrthotropicAllowableCurvePoint):
		self._Entity = orthotropicAllowableCurvePoint

	@property
	def Property_ID(self) -> types.AllowablePropertyName:
		result = self._Entity.Property_ID
		return types.AllowablePropertyName[result.ToString()] if result is not None else None

	@property
	def Temperature(self) -> float | None:
		return self._Entity.Temperature

	@property
	def X(self) -> float | None:
		'''
		This represents either an X value for an AML or Percent0/45 Degree Fibers method, or an
		AllowablePolynomialCoefficient enumeration representing which coefficient will be entered.
		'''
		return self._Entity.X

	@property
	def XAsCoefficient(self) -> str:
		'''
		If the X corresponds to a polynomial coefficient, this property will return a meaningful string representation of it.
		Otherwise, returns a string showing the number.
		'''
		return self._Entity.XAsCoefficient

	@property
	def Y(self) -> float | None:
		'''
		This represents either a Y value for an AML or Percent0/45 Degree Fibers method,
		or the value of a coefficient for a polynomial method.
		Note that this value may or may not be affected by the unit system depending on the context of its usage.
		'''
		return self._Entity.Y

	@Property_ID.setter
	def Property_ID(self, value: types.AllowablePropertyName) -> None:
		self._Entity.Property_ID = _types.AllowablePropertyName(types.GetEnumValue(value.value))

	@Temperature.setter
	def Temperature(self, value: float | None) -> None:
		self._Entity.Temperature = value

	@X.setter
	def X(self, value: float | None) -> None:
		self._Entity.X = value

	@Y.setter
	def Y(self, value: float | None) -> None:
		self._Entity.Y = value


class OrthotropicEffectiveLaminate:
	'''
	Orthotropic material effective laminate properties. Read-only from the API.
	Check if material is an effective laminate with orthotropic.IsEffectiveLaminate.
	'''
	def __init__(self, orthotropicEffectiveLaminate: _api.OrthotropicEffectiveLaminate):
		self._Entity = orthotropicEffectiveLaminate

	@property
	def Percent_tape_0(self) -> float | None:
		return self._Entity.Percent_tape_0

	@property
	def Percent_tape_90(self) -> float | None:
		return self._Entity.Percent_tape_90

	@property
	def Percent_tape_45(self) -> float | None:
		return self._Entity.Percent_tape_45

	@property
	def Percent_fabric_0(self) -> float | None:
		return self._Entity.Percent_fabric_0

	@property
	def Percent_fabric_90(self) -> float | None:
		return self._Entity.Percent_fabric_90

	@property
	def Percent_fabric_45(self) -> float | None:
		return self._Entity.Percent_fabric_45

	@property
	def Tape_Orthotropic(self) -> str:
		'''
		Tape material associated with effective orthotropic material.
		'''
		return self._Entity.Tape_Orthotropic

	@property
	def Fabric_Orthotropic(self) -> str:
		'''
		Fabric material associated with effective orthotropic material.
		'''
		return self._Entity.Fabric_Orthotropic

	@property
	def Valid(self) -> bool:
		return self._Entity.Valid

	@property
	def Use_tape_allowables(self) -> bool:
		return self._Entity.Use_tape_allowables


class OrthotropicLaminateAllowable:
	'''
	Orthotropic material laminate allowable properties.
	'''
	def __init__(self, orthotropicLaminateAllowable: _api.OrthotropicLaminateAllowable):
		self._Entity = orthotropicLaminateAllowable

	@property
	def Property_ID(self) -> types.AllowablePropertyName:
		result = self._Entity.Property_ID
		return types.AllowablePropertyName[result.ToString()] if result is not None else None

	@property
	def Method_ID(self) -> types.AllowableMethodName:
		result = self._Entity.Method_ID
		return types.AllowableMethodName[result.ToString()] if result is not None else None

	@Property_ID.setter
	def Property_ID(self, value: types.AllowablePropertyName) -> None:
		self._Entity.Property_ID = _types.AllowablePropertyName(types.GetEnumValue(value.value))

	@Method_ID.setter
	def Method_ID(self, value: types.AllowableMethodName) -> None:
		self._Entity.Method_ID = _types.AllowableMethodName(types.GetEnumValue(value.value))


class OrthotropicTemperature:
	'''
	Orthotropic material temperature dependent properties.
	'''
	def __init__(self, orthotropicTemperature: _api.OrthotropicTemperature):
		self._Entity = orthotropicTemperature

	@property
	def alpha1(self) -> float:
		'''
		alpha1. Eng: µin/in/Farenheit / SI: µm/m/Kelvin
		'''
		return self._Entity.alpha1

	@property
	def alpha2(self) -> float:
		'''
		alpha2. Eng: µin/in/Farenheit / SI: µm/m/Kelvin
		'''
		return self._Entity.alpha2

	@property
	def C(self) -> float | None:
		'''
		C. Eng: B/lb/Farenheit / SI: J/g/K
		'''
		return self._Entity.C

	@property
	def cd(self) -> float | None:
		'''
		Characteristic Distance. Eng: in / SI: m
		'''
		return self._Entity.cd

	@property
	def d0Compression(self) -> float | None:
		'''
		D0c. Eng: in / SI: m
		'''
		return self._Entity.d0Compression

	@property
	def d0Tension(self) -> float | None:
		'''
		D0t. Eng: in / SI: m
		'''
		return self._Entity.d0Tension

	@property
	def Ec1(self) -> float:
		'''
		Ec1. Eng: Msi / SI: GPa
		'''
		return self._Entity.Ec1

	@property
	def Ec2(self) -> float:
		'''
		Ec2. Eng: Msi / SI: GPa
		'''
		return self._Entity.Ec2

	@property
	def ecu1(self) -> float:
		'''
		ecu1. Eng: µin/in / SI: µm/m
		'''
		return self._Entity.ecu1

	@property
	def ecu2(self) -> float:
		'''
		ecu2. Eng: µin/in / SI: µm/m
		'''
		return self._Entity.ecu2

	@property
	def ecuai(self) -> float | None:
		'''
		Compression, eOHC. Eng: µin/in / SI: µm/m
		'''
		return self._Entity.ecuai

	@property
	def ecuoh(self) -> float | None:
		'''
		Tension, eOHT. Eng: µin/in / SI: µm/m
		'''
		return self._Entity.ecuoh

	@property
	def esu12(self) -> float:
		'''
		In-Plane, esu12. Eng: µin/in / SI: µm/m
		'''
		return self._Entity.esu12

	@property
	def Et1(self) -> float:
		'''
		Et1. Eng: Msi / SI: GPa
		'''
		return self._Entity.Et1

	@property
	def Et2(self) -> float:
		'''
		Et2. Eng: Msi / SI: GPa
		'''
		return self._Entity.Et2

	@property
	def etu1(self) -> float:
		'''
		etu1. Eng: µin/in / SI: µm/m
		'''
		return self._Entity.etu1

	@property
	def etu2(self) -> float:
		'''
		etu2. Eng: µin/in / SI: µm/m
		'''
		return self._Entity.etu2

	@property
	def Fcu1(self) -> float:
		'''
		Fcu1. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fcu1

	@property
	def Fcu2(self) -> float:
		'''
		Fcu2. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fcu2

	@property
	def Fsu12(self) -> float:
		'''
		Fsu12. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fsu12

	@property
	def Fsu13(self) -> float | None:
		'''
		Fsu13. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fsu13

	@property
	def Fsu23(self) -> float | None:
		'''
		Fsu23. Eng: ksi / SI: MPa
		'''
		return self._Entity.Fsu23

	@property
	def Ftu1(self) -> float:
		'''
		Ftu1. Eng: ksi / SI: MPa
		'''
		return self._Entity.Ftu1

	@property
	def Ftu2(self) -> float:
		'''
		Ftu2. Eng: ksi / SI: MPa
		'''
		return self._Entity.Ftu2

	@property
	def Ftu3(self) -> float | None:
		'''
		Ftu3. Eng: ksi / SI: MPa
		'''
		return self._Entity.Ftu3

	@property
	def G12(self) -> float:
		'''
		G12. Eng: Msi / SI: GPa
		'''
		return self._Entity.G12

	@property
	def G13(self) -> float | None:
		'''
		G13. Eng: Msi / SI: GPa
		'''
		return self._Entity.G13

	@property
	def G23(self) -> float | None:
		'''
		G23. Eng: Msi / SI: GPa
		'''
		return self._Entity.G23

	@property
	def GIc(self) -> float | None:
		'''
		GIC. Eng: in-lb/in^2 / SI: J/m^2
		'''
		return self._Entity.GIc

	@property
	def GIIc(self) -> float | None:
		'''
		GIIC. Eng: in-lb/in^2 / SI: J/m^2
		'''
		return self._Entity.GIIc

	@property
	def K1(self) -> float | None:
		'''
		K1. Eng: B-ft/ft^2/hr/Farenheit / SI: W/m/Kelvin
		'''
		return self._Entity.K1

	@property
	def K2(self) -> float | None:
		'''
		K2. Eng: B-ft/ft^2/hr/Farenheit / SI: W/m/Kelvin
		'''
		return self._Entity.K2

	@property
	def OrthotropicAllowableCurvePoints(self) -> list[OrthotropicAllowableCurvePoint]:
		'''
		Access the relevant curve points based on the material's selection of method or polynomial.
		'''
		return [OrthotropicAllowableCurvePoint(orthotropicAllowableCurvePoint) for orthotropicAllowableCurvePoint in self._Entity.OrthotropicAllowableCurvePoints]

	@property
	def Temperature(self) -> float:
		'''
		Temperature. Eng: Farenheit / SI: Celsius
		'''
		return self._Entity.Temperature

	@property
	def TLc(self) -> float | None:
		'''
		Puck Inclination Parameter, TLc.
		'''
		return self._Entity.TLc

	@property
	def TLt(self) -> float | None:
		'''
		Puck Inclination Parameter, TLt.
		'''
		return self._Entity.TLt

	@property
	def TTc(self) -> float | None:
		'''
		Puck Inclination Parameter, TTc.
		'''
		return self._Entity.TTc

	@property
	def TTt(self) -> float | None:
		'''
		Puck Inclination Parameter, TTt.
		'''
		return self._Entity.TTt

	@property
	def vc12(self) -> float:
		return self._Entity.vc12

	@property
	def vt12(self) -> float | None:
		return self._Entity.vt12

	@alpha1.setter
	def alpha1(self, value: float) -> None:
		self._Entity.alpha1 = value

	@alpha2.setter
	def alpha2(self, value: float) -> None:
		self._Entity.alpha2 = value

	@C.setter
	def C(self, value: float | None) -> None:
		self._Entity.C = value

	@cd.setter
	def cd(self, value: float | None) -> None:
		self._Entity.cd = value

	@d0Compression.setter
	def d0Compression(self, value: float | None) -> None:
		self._Entity.d0Compression = value

	@d0Tension.setter
	def d0Tension(self, value: float | None) -> None:
		self._Entity.d0Tension = value

	@Ec1.setter
	def Ec1(self, value: float) -> None:
		self._Entity.Ec1 = value

	@Ec2.setter
	def Ec2(self, value: float) -> None:
		self._Entity.Ec2 = value

	@ecu1.setter
	def ecu1(self, value: float) -> None:
		self._Entity.ecu1 = value

	@ecu2.setter
	def ecu2(self, value: float) -> None:
		self._Entity.ecu2 = value

	@ecuai.setter
	def ecuai(self, value: float | None) -> None:
		self._Entity.ecuai = value

	@ecuoh.setter
	def ecuoh(self, value: float | None) -> None:
		self._Entity.ecuoh = value

	@esu12.setter
	def esu12(self, value: float) -> None:
		self._Entity.esu12 = value

	@Et1.setter
	def Et1(self, value: float) -> None:
		self._Entity.Et1 = value

	@Et2.setter
	def Et2(self, value: float) -> None:
		self._Entity.Et2 = value

	@etu1.setter
	def etu1(self, value: float) -> None:
		self._Entity.etu1 = value

	@etu2.setter
	def etu2(self, value: float) -> None:
		self._Entity.etu2 = value

	@Fcu1.setter
	def Fcu1(self, value: float) -> None:
		self._Entity.Fcu1 = value

	@Fcu2.setter
	def Fcu2(self, value: float) -> None:
		self._Entity.Fcu2 = value

	@Fsu12.setter
	def Fsu12(self, value: float) -> None:
		self._Entity.Fsu12 = value

	@Fsu13.setter
	def Fsu13(self, value: float | None) -> None:
		self._Entity.Fsu13 = value

	@Fsu23.setter
	def Fsu23(self, value: float | None) -> None:
		self._Entity.Fsu23 = value

	@Ftu1.setter
	def Ftu1(self, value: float) -> None:
		self._Entity.Ftu1 = value

	@Ftu2.setter
	def Ftu2(self, value: float) -> None:
		self._Entity.Ftu2 = value

	@Ftu3.setter
	def Ftu3(self, value: float | None) -> None:
		self._Entity.Ftu3 = value

	@G12.setter
	def G12(self, value: float) -> None:
		self._Entity.G12 = value

	@G13.setter
	def G13(self, value: float | None) -> None:
		self._Entity.G13 = value

	@G23.setter
	def G23(self, value: float | None) -> None:
		self._Entity.G23 = value

	@GIc.setter
	def GIc(self, value: float | None) -> None:
		self._Entity.GIc = value

	@GIIc.setter
	def GIIc(self, value: float | None) -> None:
		self._Entity.GIIc = value

	@K1.setter
	def K1(self, value: float | None) -> None:
		self._Entity.K1 = value

	@K2.setter
	def K2(self, value: float | None) -> None:
		self._Entity.K2 = value

	@Temperature.setter
	def Temperature(self, value: float) -> None:
		self._Entity.Temperature = value

	@TLc.setter
	def TLc(self, value: float | None) -> None:
		self._Entity.TLc = value

	@TLt.setter
	def TLt(self, value: float | None) -> None:
		self._Entity.TLt = value

	@TTc.setter
	def TTc(self, value: float | None) -> None:
		self._Entity.TTc = value

	@TTt.setter
	def TTt(self, value: float | None) -> None:
		self._Entity.TTt = value

	@vc12.setter
	def vc12(self, value: float) -> None:
		self._Entity.vc12 = value

	@vt12.setter
	def vt12(self, value: float | None) -> None:
		self._Entity.vt12 = value

	def AddCurvePoint(self, property: types.AllowablePropertyName, x: float, y: float) -> OrthotropicAllowableCurvePoint:
		'''
		Add a curve point to a laminate allowable curve.
		
		:param x: x represents an x-value (for a non-polynomial method) or an allowable polynomial coefficient (represented by an enum).
		
		:return: The newly created curve point.
		'''
		return OrthotropicAllowableCurvePoint(self._Entity.AddCurvePoint(_types.AllowablePropertyName(types.GetEnumValue(property.value)), x, y))

	def DeleteCurvePoint(self, property: types.AllowablePropertyName, x: float) -> bool:
		'''
		Deletes a temperature-dependent property for a material.
		
		:param x: x represents an x-value (for a non-polynomial method) or an allowable polynomial coefficient (represented by an enum).
		'''
		return self._Entity.DeleteCurvePoint(_types.AllowablePropertyName(types.GetEnumValue(property.value)), x)

	def GetCurvePoint(self, property: types.AllowablePropertyName, x: float) -> OrthotropicAllowableCurvePoint:
		'''
		Retrieve an allowable curve point from this temperature's allowable curve points.
		
		:param x: x represents an x-value (for a non-polynomial method) or an allowable polynomial coefficient (represented by an enum).
		
		:return: The Laminate Allowable, if a matching one was found. Returns ``None`` if none exists.
		'''
		return OrthotropicAllowableCurvePoint(self._Entity.GetCurvePoint(_types.AllowablePropertyName(types.GetEnumValue(property.value)), x))


class Orthotropic:
	'''
	Orthotropic material.
	'''

	_OrthotropicEffectiveLaminate = OrthotropicEffectiveLaminate
	def __init__(self, orthotropic: _api.Orthotropic):
		self._Entity = orthotropic

	@property
	def MaterialFamilyName(self) -> str:
		'''
		The material family for this material. When the material is saved, a new family will be created if none matching this name exists.
		'''
		return self._Entity.MaterialFamilyName

	@property
	def Id(self) -> int:
		return self._Entity.Id

	@property
	def CreationDate(self) -> DateTime:
		'''
		Date the material was created.
		'''
		return self._Entity.CreationDate

	@property
	def ModificationDate(self) -> DateTime:
		'''
		Most recent modification date of the material.
		'''
		return self._Entity.ModificationDate

	@property
	def Name(self) -> str:
		'''
		Name of this material.
		'''
		return self._Entity.Name

	@property
	def Form(self) -> str:
		return self._Entity.Form

	@property
	def Specification(self) -> str:
		return self._Entity.Specification

	@property
	def Basis(self) -> str:
		return self._Entity.Basis

	@property
	def Wet(self) -> bool:
		return self._Entity.Wet

	@property
	def Thickness(self) -> float:
		'''
		Thickness. Eng: in / SI: mm
		'''
		return self._Entity.Thickness

	@property
	def Density(self) -> float:
		'''
		Density. Eng: lbm/in^3 / SI: kg/m^3
		'''
		return self._Entity.Density

	@property
	def FiberVolume(self) -> float | None:
		'''
		Fiber Volume. Expressed as a percentage.
		'''
		return self._Entity.FiberVolume

	@property
	def GlassTransition(self) -> float | None:
		return self._Entity.GlassTransition

	@property
	def Manufacturer(self) -> str:
		return self._Entity.Manufacturer

	@property
	def Processes(self) -> str:
		return self._Entity.Processes

	@property
	def MaterialDescription(self) -> str:
		return self._Entity.MaterialDescription

	@property
	def UserNote(self) -> str:
		return self._Entity.UserNote

	@property
	def BendingCorrectionFactor(self) -> float:
		return self._Entity.BendingCorrectionFactor

	@property
	def FemMaterialId(self) -> int | None:
		'''
		Linked FEM Material ID. Null if none exists.
		'''
		return self._Entity.FemMaterialId

	@property
	def Cost(self) -> float | None:
		return self._Entity.Cost

	@property
	def BucklingStiffnessKnockdown(self) -> float:
		return self._Entity.BucklingStiffnessKnockdown

	@property
	def OrthotropicTemperatureProperties(self) -> list[OrthotropicTemperature]:
		'''
		List of this material's temperature-dependent properties.
		'''
		return [OrthotropicTemperature(orthotropicTemperature) for orthotropicTemperature in self._Entity.OrthotropicTemperatureProperties]

	@property
	def OrthotropicLaminateAllowables(self) -> list[OrthotropicLaminateAllowable]:
		'''
		List of this material's laminate allowable properties.
		'''
		return [OrthotropicLaminateAllowable(orthotropicLaminateAllowable) for orthotropicLaminateAllowable in self._Entity.OrthotropicLaminateAllowables]
	@property
	def OrthotropicEffectiveLaminate(self) -> _OrthotropicEffectiveLaminate:
		'''
		Contains Effective Laminate data if this material is an effective laminate, otherwise ``None``.
		'''
		result = self._Entity.OrthotropicEffectiveLaminate
		return OrthotropicEffectiveLaminate(result) if result is not None else None

	@property
	def OrthotropicEquationCorrectionFactors(self) -> dict[OrthotropicCorrectionFactorPoint, OrthotropicEquationCorrectionFactor]:
		'''
		Dictionary of this material's equation-based correction factors.
		'''
		orthotropicEquationCorrectionFactorsDict = {}
		for kvp in self._Entity.OrthotropicEquationCorrectionFactors:
			orthotropicEquationCorrectionFactorsDict[OrthotropicCorrectionFactorPoint(kvp.Key)] = OrthotropicEquationCorrectionFactor(kvp.Value)

		return orthotropicEquationCorrectionFactorsDict

	@property
	def OrthotropicTabularCorrectionFactors(self) -> dict[OrthotropicCorrectionFactorPoint, OrthotropicTabularCorrectionFactor]:
		'''
		Dictionary of this material's tabular correction factors.
		'''
		orthotropicTabularCorrectionFactorsDict = {}
		for kvp in self._Entity.OrthotropicTabularCorrectionFactors:
			orthotropicTabularCorrectionFactorsDict[OrthotropicCorrectionFactorPoint(kvp.Key)] = OrthotropicTabularCorrectionFactor(kvp.Value)

		return orthotropicTabularCorrectionFactorsDict

	def AddTemperatureProperty(self, temperature: float, et1: float, et2: float, vt12: float, ec1: float, ec2: float, vc12: float, g12: float, ftu1: float, ftu2: float, fcu1: float, fcu2: float, fsu12: float, alpha1: float, alpha2: float, etu1: float, etu2: float, ecu1: float, ecu2: float, esu12: float) -> OrthotropicTemperature:
		'''
		Adds a temperature-dependent property for a material.
		
		:return: The newly created temperature-dependent property.
		'''
		return OrthotropicTemperature(self._Entity.AddTemperatureProperty(temperature, et1, et2, vt12, ec1, ec2, vc12, g12, ftu1, ftu2, fcu1, fcu2, fsu12, alpha1, alpha2, etu1, etu2, ecu1, ecu2, esu12))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		'''
		Deletes a temperature-dependent property for a material.
		'''
		return self._Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> OrthotropicTemperature:
		'''
		Retrieve a Temperature from this material's temperature-dependent properties. Allows a degree of tolerance to avoid issues with floating point numbers.
		
		:param LookupTemperature: Temperature to search for.
		
		:return: The temperature, if a matching one was found. Returns ``None`` if none exists.
		'''
		return OrthotropicTemperature(self._Entity.GetTemperature(lookupTemperature))

	def IsEffectiveLaminate(self) -> bool:
		'''
		Returns true if this material is an effective laminate.
		'''
		return self._Entity.IsEffectiveLaminate()

	def HasLaminateAllowable(self, property: types.AllowablePropertyName) -> bool:
		'''
		Returns true if this material has a specified laminate allowable property.
		'''
		return self._Entity.HasLaminateAllowable(_types.AllowablePropertyName(types.GetEnumValue(property.value)))

	def AddLaminateAllowable(self, property: types.AllowablePropertyName, method: types.AllowableMethodName) -> OrthotropicLaminateAllowable:
		'''
		Adds a laminate allowable to this material.
		An orthotropic material can only have one laminate allowable of each property (as specified by the property argument).
		
		:param property: The strain or stress property for a laminate allowable.
		:param method: The method for a laminate allowable (AML, Percent 0/45, Polynomial).
		
		:return: The newly created laminate allowable.
		'''
		return OrthotropicLaminateAllowable(self._Entity.AddLaminateAllowable(_types.AllowablePropertyName(types.GetEnumValue(property.value)), _types.AllowableMethodName(types.GetEnumValue(method.value))))

	def GetLaminateAllowable(self, lookupAllowableProperty: types.AllowablePropertyName) -> OrthotropicLaminateAllowable:
		'''
		Retrieve a Laminate allowable from this material's laminate allowables.
		
		:param LookupAllowableProperty: Laminate allowable property to search for.
		
		:return: The Laminate Allowable, if a matching one was found. Returns ``None`` if none exists.
		'''
		return OrthotropicLaminateAllowable(self._Entity.GetLaminateAllowable(_types.AllowablePropertyName(types.GetEnumValue(lookupAllowableProperty.value))))

	def AddEquationCorrectionFactor(self, propertyId: types.CorrectionProperty, correctionId: types.CorrectionId, equationId: types.CorrectionEquation) -> OrthotropicEquationCorrectionFactor:
		'''
		Adds an equation-based correction factor for this material.
		
		:param propertyId: The ID of the property to be affected by the correction factor. Specified with a CorrectionPropertyName enum.
		:param correctionId: The ID for the type of correction factor to be applied. Specified with a CorrectionIDName enum.
		:param equationId: The ID for the type of correction factor equation to use. Specified with a CorrectionEquationName enum.
		
		:return: The newly created correction factor.
		'''
		return OrthotropicEquationCorrectionFactor(self._Entity.AddEquationCorrectionFactor(_types.CorrectionProperty(types.GetEnumValue(propertyId.value)), _types.CorrectionId(types.GetEnumValue(correctionId.value)), _types.CorrectionEquation(types.GetEnumValue(equationId.value))))

	def GetEquationCorrectionFactor(self, property: types.CorrectionProperty, correction: types.CorrectionId) -> OrthotropicEquationCorrectionFactor:
		'''
		Retrieve a Correction Factor from this material's correction factors.
		
		:param property: CorrectionPropertyName to search for.
		:param correction: CorrectionIDName to search for.
		
		:return: The OrthotropicCorrectionFactor, if a matching one was found. Returns ``None`` if none exists.
		'''
		return OrthotropicEquationCorrectionFactor(self._Entity.GetEquationCorrectionFactor(_types.CorrectionProperty(types.GetEnumValue(property.value)), _types.CorrectionId(types.GetEnumValue(correction.value))))

	def GetTabularCorrectionFactor(self, property: types.CorrectionProperty, correction: types.CorrectionId) -> OrthotropicTabularCorrectionFactor:
		'''
		Retrieve a Correction Factor from this material's correction factors.
		
		:param property: CorrectionPropertyName to search for.
		:param correction: CorrectionIDName to search for.
		
		:return: The OrthotropicCorrectionFactor, if a matching one was found. Returns ``None`` if none exists.
		'''
		return OrthotropicTabularCorrectionFactor(self._Entity.GetTabularCorrectionFactor(_types.CorrectionProperty(types.GetEnumValue(property.value)), _types.CorrectionId(types.GetEnumValue(correction.value))))

	@MaterialFamilyName.setter
	def MaterialFamilyName(self, value: str) -> None:
		self._Entity.MaterialFamilyName = value

	@Name.setter
	def Name(self, value: str) -> None:
		self._Entity.Name = value

	@Form.setter
	def Form(self, value: str) -> None:
		self._Entity.Form = value

	@Specification.setter
	def Specification(self, value: str) -> None:
		self._Entity.Specification = value

	@Basis.setter
	def Basis(self, value: str) -> None:
		self._Entity.Basis = value

	@Wet.setter
	def Wet(self, value: bool) -> None:
		self._Entity.Wet = value

	@Thickness.setter
	def Thickness(self, value: float) -> None:
		self._Entity.Thickness = value

	@Density.setter
	def Density(self, value: float) -> None:
		self._Entity.Density = value

	@FiberVolume.setter
	def FiberVolume(self, value: float | None) -> None:
		self._Entity.FiberVolume = value

	@GlassTransition.setter
	def GlassTransition(self, value: float | None) -> None:
		self._Entity.GlassTransition = value

	@Manufacturer.setter
	def Manufacturer(self, value: str) -> None:
		self._Entity.Manufacturer = value

	@Processes.setter
	def Processes(self, value: str) -> None:
		self._Entity.Processes = value

	@MaterialDescription.setter
	def MaterialDescription(self, value: str) -> None:
		self._Entity.MaterialDescription = value

	@UserNote.setter
	def UserNote(self, value: str) -> None:
		self._Entity.UserNote = value

	@BendingCorrectionFactor.setter
	def BendingCorrectionFactor(self, value: float) -> None:
		self._Entity.BendingCorrectionFactor = value

	@FemMaterialId.setter
	def FemMaterialId(self, value: int | None) -> None:
		self._Entity.FemMaterialId = value

	@Cost.setter
	def Cost(self, value: float | None) -> None:
		self._Entity.Cost = value

	@BucklingStiffnessKnockdown.setter
	def BucklingStiffnessKnockdown(self, value: float) -> None:
		self._Entity.BucklingStiffnessKnockdown = value

	def Save(self) -> None:
		'''
		Save any changes to this orthotropic material to the database.
		'''
		return self._Entity.Save()


class Vector2d:
	'''
	Represents a readonly 2D vector.
	'''
	def __init__(self, vector2d: _api.Vector2d):
		self._Entity = vector2d

	def Create_Vector2d(x: float, y: float):
		return Vector2d(_api.Vector2d(x, y))

	@property
	def X(self) -> float:
		return self._Entity.X

	@property
	def Y(self) -> float:
		return self._Entity.Y

	@overload
	def Equals(self, other) -> bool:
		...

	@overload
	def Equals(self, obj: object) -> bool:
		...

	def Equals(self, item1 = None) -> bool:
		'''
		Overload 1: ``Equals(self, other) -> bool``

		Overload 2: ``Equals(self, obj: object) -> bool``
		'''
		if isinstance(item1, Vector2d):
			return self._Entity.Equals(item1._Entity)

		if isinstance(item1, object):
			return self._Entity.Equals(item1)

		return self._Entity.Equals(item1._Entity)

	def __eq__(self, other):
		return self.Equals(other)

	def __ne__(self, other):
		return not self.Equals(other)

	def __hash__(self) -> int:
		return self._Entity.GetHashCode()


class ElementSet(IdNameEntity):
	'''
	A set of elements defined in the input file.
	'''
	def __init__(self, elementSet: _api.ElementSet):
		self._Entity = elementSet

	@property
	def Elements(self) -> ElementCol:
		result = self._Entity.Elements
		return ElementCol(result) if result is not None else None


class FemProperty(IdNameEntity):
	'''
	A property description.
	'''
	def __init__(self, femProperty: _api.FemProperty):
		self._Entity = femProperty

	@property
	def Elements(self) -> ElementCol:
		result = self._Entity.Elements
		return ElementCol(result) if result is not None else None

	@property
	def FemType(self) -> types.FemType:
		result = self._Entity.FemType
		return types.FemType[result.ToString()] if result is not None else None


class ElementSetCol(IdEntityCol[ElementSet]):
	def __init__(self, elementSetCol: _api.ElementSetCol):
		self._Entity = elementSetCol
		self._CollectedClass = ElementSet

	@property
	def ElementSetColList(self) -> tuple[ElementSet]:
		return tuple([ElementSet(elementSetCol) for elementSetCol in self._Entity])

	def __getitem__(self, index: int):
		return self.ElementSetColList[index]

	def __iter__(self):
		yield from self.ElementSetColList

	def __len__(self):
		return len(self.ElementSetColList)


class FemPropertyCol(IdEntityCol[FemProperty]):
	def __init__(self, femPropertyCol: _api.FemPropertyCol):
		self._Entity = femPropertyCol
		self._CollectedClass = FemProperty

	@property
	def FemPropertyColList(self) -> tuple[FemProperty]:
		return tuple([FemProperty(femPropertyCol) for femPropertyCol in self._Entity])

	def __getitem__(self, index: int):
		return self.FemPropertyColList[index]

	def __iter__(self):
		yield from self.FemPropertyColList

	def __len__(self):
		return len(self.FemPropertyColList)


class FemDataSet:
	def __init__(self, femDataSet: _api.FemDataSet):
		self._Entity = femDataSet

	@property
	def FemProperties(self) -> FemPropertyCol:
		result = self._Entity.FemProperties
		return FemPropertyCol(result) if result is not None else None

	@property
	def ElementSets(self) -> ElementSetCol:
		result = self._Entity.ElementSets
		return ElementSetCol(result) if result is not None else None


class PluginPackage(IdNameEntity):
	def __init__(self, pluginPackage: _api.PluginPackage):
		self._Entity = pluginPackage

	@property
	def FilePath(self) -> str:
		return self._Entity.FilePath

	@property
	def Version(self) -> str:
		return self._Entity.Version

	@property
	def Description(self) -> str:
		return self._Entity.Description

	@property
	def ModificationDate(self) -> DateTime:
		return self._Entity.ModificationDate


class Ply(IdNameEntity):
	def __init__(self, ply: _api.Ply):
		self._Entity = ply

	@property
	def InnerCurves(self) -> list[int]:
		return [int32 for int32 in self._Entity.InnerCurves]

	@property
	def OuterCurves(self) -> list[int]:
		return [int32 for int32 in self._Entity.OuterCurves]

	@property
	def FiberDirectionCurves(self) -> list[int]:
		return [int32 for int32 in self._Entity.FiberDirectionCurves]

	@property
	def Area(self) -> float:
		return self._Entity.Area

	@property
	def Description(self) -> str:
		return self._Entity.Description

	@property
	def Elements(self) -> ElementCol:
		result = self._Entity.Elements
		return ElementCol(result) if result is not None else None

	@property
	def MaterialId(self) -> int:
		return self._Entity.MaterialId

	@property
	def MaterialName(self) -> str:
		return self._Entity.MaterialName

	@property
	def Orientation(self) -> int:
		'''
		This must be an integer in the range of [-90, 90]
		'''
		return self._Entity.Orientation

	@property
	def Sequence(self) -> int:
		return self._Entity.Sequence

	@property
	def StructureId(self) -> int:
		'''
		The structure that contains this ply.
		'''
		return self._Entity.StructureId

	@property
	def Thickness(self) -> float:
		return self._Entity.Thickness


class Rundeck(IdEntity):
	def __init__(self, rundeck: _api.Rundeck):
		self._Entity = rundeck

	@property
	def InputFilePath(self) -> str:
		return self._Entity.InputFilePath

	@property
	def IsPrimary(self) -> bool:
		'''
		This returns true for the primary rundeck.
		Note that the primary rundeck always has ID 1.
		'''
		return self._Entity.IsPrimary

	@property
	def ResultFilePath(self) -> str:
		return self._Entity.ResultFilePath

	def SetInputFilePath(self, filepath: str) -> RundeckUpdateStatus:
		'''
		The rundeck's input file path will point to the provided file path
		
		:param filepath: The path to the rundeck
		'''
		return RundeckUpdateStatus[self._Entity.SetInputFilePath(filepath).ToString()]

	def SetResultFilePath(self, filepath: str) -> RundeckUpdateStatus:
		'''
		The rundeck's result file path will point to the provided file path
		
		:param filepath: The path to the result file
		'''
		return RundeckUpdateStatus[self._Entity.SetResultFilePath(filepath).ToString()]


class RundeckPathPair:
	def __init__(self, rundeckPathPair: _api.RundeckPathPair):
		self._Entity = rundeckPathPair

	@property
	def InputFilePath(self) -> str:
		return self._Entity.InputFilePath

	@property
	def ResultFilePath(self) -> str:
		return self._Entity.ResultFilePath

	@InputFilePath.setter
	def InputFilePath(self, value: str) -> None:
		self._Entity.InputFilePath = value

	@ResultFilePath.setter
	def ResultFilePath(self, value: str) -> None:
		self._Entity.ResultFilePath = value


class BeamLoads:
	def __init__(self, beamLoads: _api.BeamLoads):
		self._Entity = beamLoads

	@property
	def AxialForce(self) -> float | None:
		return self._Entity.AxialForce

	@property
	def MomentX(self) -> float | None:
		return self._Entity.MomentX

	@property
	def MomentY(self) -> float | None:
		return self._Entity.MomentY

	@property
	def ShearX(self) -> float | None:
		return self._Entity.ShearX

	@property
	def ShearY(self) -> float | None:
		return self._Entity.ShearY

	@property
	def Torque(self) -> float | None:
		return self._Entity.Torque


class SectionCut(IdNameEntity):
	def __init__(self, sectionCut: _api.SectionCut):
		self._Entity = sectionCut

	@property
	def ParentFolder(self) -> Folder:
		result = self._Entity.ParentFolder
		return Folder(result) if result is not None else None

	@property
	def ReferencePoint(self) -> types.SectionCutPropertyLocation:
		result = self._Entity.ReferencePoint
		return types.SectionCutPropertyLocation[result.ToString()] if result is not None else None

	@property
	def HorizontalVector(self) -> Vector3d:
		result = self._Entity.HorizontalVector
		return Vector3d(result) if result is not None else None

	@property
	def NormalVector(self) -> Vector3d:
		result = self._Entity.NormalVector
		return Vector3d(result) if result is not None else None

	@property
	def OriginVector(self) -> Vector3d:
		result = self._Entity.OriginVector
		return Vector3d(result) if result is not None else None

	@property
	def VerticalVector(self) -> Vector3d:
		'''
		Derived from the cross of the Normal and the Horizontal.
		'''
		result = self._Entity.VerticalVector
		return Vector3d(result) if result is not None else None

	@property
	def MaxAngleBound(self) -> float | None:
		'''
		Max Principal Angle Bound
		'''
		return self._Entity.MaxAngleBound

	@property
	def MinAngleBound(self) -> float | None:
		'''
		Min Principal Angle Bound
		'''
		return self._Entity.MinAngleBound

	@property
	def MinStiffnessEihh(self) -> float | None:
		return self._Entity.MinStiffnessEihh

	@property
	def MinStiffnessEivv(self) -> float | None:
		return self._Entity.MinStiffnessEivv

	@property
	def MinStiffnessGJ(self) -> float | None:
		return self._Entity.MinStiffnessGJ

	@property
	def ZoneStiffnessDistribution(self) -> float:
		'''
		Set the zone stiffness distribution. This should be a value between 0 and 1.
		 Values closer to 0 are more even and heavier. Values closer to 1 are more targeted and lighter.
		'''
		return self._Entity.ZoneStiffnessDistribution

	@property
	def CN_hmax(self) -> float | None:
		return self._Entity.CN_hmax

	@property
	def CN_hmin(self) -> float | None:
		return self._Entity.CN_hmin

	@property
	def CN_vmax(self) -> float | None:
		return self._Entity.CN_vmax

	@property
	def CN_vmin(self) -> float | None:
		return self._Entity.CN_vmin

	@property
	def CQ_hmax(self) -> float | None:
		return self._Entity.CQ_hmax

	@property
	def CQ_hmin(self) -> float | None:
		return self._Entity.CQ_hmin

	@property
	def CQ_vmax(self) -> float | None:
		return self._Entity.CQ_vmax

	@property
	def CQ_vmin(self) -> float | None:
		return self._Entity.CQ_vmin

	@property
	def CG(self) -> Vector2d:
		result = self._Entity.CG
		return Vector2d(result) if result is not None else None

	@property
	def CN(self) -> Vector2d:
		result = self._Entity.CN
		return Vector2d(result) if result is not None else None

	@property
	def CQ(self) -> Vector2d:
		result = self._Entity.CQ
		return Vector2d(result) if result is not None else None

	@property
	def EnclosedArea(self) -> float:
		return self._Entity.EnclosedArea

	@property
	def NumberOfCells(self) -> int:
		return self._Entity.NumberOfCells

	@property
	def EIhh(self) -> float | None:
		return self._Entity.EIhh

	@property
	def EIhv(self) -> float | None:
		return self._Entity.EIhv

	@property
	def EIvv(self) -> float | None:
		return self._Entity.EIvv

	@property
	def GJ(self) -> float | None:
		return self._Entity.GJ

	@property
	def EA(self) -> float | None:
		return self._Entity.EA

	@property
	def EImax(self) -> float | None:
		return self._Entity.EImax

	@property
	def EImin(self) -> float | None:
		return self._Entity.EImin

	@property
	def PrincipalAngle(self) -> float | None:
		'''
		φ
		'''
		return self._Entity.PrincipalAngle

	@property
	def Elements(self) -> ElementCol:
		result = self._Entity.Elements
		return ElementCol(result) if result is not None else None

	@property
	def PlateElements(self) -> ElementCol:
		result = self._Entity.PlateElements
		return ElementCol(result) if result is not None else None

	@property
	def BeamElements(self) -> ElementCol:
		result = self._Entity.BeamElements
		return ElementCol(result) if result is not None else None

	def AlignToHorizontalPrincipalAxes(self) -> None:
		'''
		Set this Section Cut's horizontal vector to be equal to its principal axis horizontal vector.
		'''
		return self._Entity.AlignToHorizontalPrincipalAxes()

	def AlignToVerticalPrincipalAxes(self) -> None:
		'''
		Set this Section Cut's horizontal vector to be equal to its principal axis vertical vector.
		'''
		return self._Entity.AlignToVerticalPrincipalAxes()

	@ReferencePoint.setter
	def ReferencePoint(self, value: types.SectionCutPropertyLocation) -> None:
		self._Entity.ReferencePoint = _types.SectionCutPropertyLocation(types.GetEnumValue(value.value))

	def SetHorizontalVector(self, vector: Vector3d) -> None:
		return self._Entity.SetHorizontalVector(vector._Entity)

	def SetNormalVector(self, vector: Vector3d) -> None:
		return self._Entity.SetNormalVector(vector._Entity)

	def SetOrigin(self, vector: Vector3d) -> None:
		return self._Entity.SetOrigin(vector._Entity)

	@MaxAngleBound.setter
	def MaxAngleBound(self, value: float | None) -> None:
		self._Entity.MaxAngleBound = value

	@MinAngleBound.setter
	def MinAngleBound(self, value: float | None) -> None:
		self._Entity.MinAngleBound = value

	@MinStiffnessEihh.setter
	def MinStiffnessEihh(self, value: float | None) -> None:
		self._Entity.MinStiffnessEihh = value

	@MinStiffnessEivv.setter
	def MinStiffnessEivv(self, value: float | None) -> None:
		self._Entity.MinStiffnessEivv = value

	@MinStiffnessGJ.setter
	def MinStiffnessGJ(self, value: float | None) -> None:
		self._Entity.MinStiffnessGJ = value

	@ZoneStiffnessDistribution.setter
	def ZoneStiffnessDistribution(self, value: float) -> None:
		self._Entity.ZoneStiffnessDistribution = value

	@CN_hmax.setter
	def CN_hmax(self, value: float | None) -> None:
		self._Entity.CN_hmax = value

	@CN_hmin.setter
	def CN_hmin(self, value: float | None) -> None:
		self._Entity.CN_hmin = value

	@CN_vmax.setter
	def CN_vmax(self, value: float | None) -> None:
		self._Entity.CN_vmax = value

	@CN_vmin.setter
	def CN_vmin(self, value: float | None) -> None:
		self._Entity.CN_vmin = value

	@CQ_hmax.setter
	def CQ_hmax(self, value: float | None) -> None:
		self._Entity.CQ_hmax = value

	@CQ_hmin.setter
	def CQ_hmin(self, value: float | None) -> None:
		self._Entity.CQ_hmin = value

	@CQ_vmax.setter
	def CQ_vmax(self, value: float | None) -> None:
		self._Entity.CQ_vmax = value

	@CQ_vmin.setter
	def CQ_vmin(self, value: float | None) -> None:
		self._Entity.CQ_vmin = value

	def GetBeamLoads(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> BeamLoads:
		return BeamLoads(self._Entity.GetBeamLoads(loadCaseId, _types.LoadSubCaseFactor(types.GetEnumValue(factor.value))))

	def InclinationAngle(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> float | None:
		return self._Entity.InclinationAngle(loadCaseId, _types.LoadSubCaseFactor(types.GetEnumValue(factor.value)))

	def HorizontalIntercept(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> float | None:
		return self._Entity.HorizontalIntercept(loadCaseId, _types.LoadSubCaseFactor(types.GetEnumValue(factor.value)))

	def VerticalIntercept(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> float | None:
		return self._Entity.VerticalIntercept(loadCaseId, _types.LoadSubCaseFactor(types.GetEnumValue(factor.value)))

	def SetElements(self, elements: list[int]) -> bool:
		'''
		Returns true if successful.
		'''
		elementsList = MakeCSharpIntList(elements)
		return self._Entity.SetElements(elementsList)

	def SetElementsByIntersection(self) -> None:
		return self._Entity.SetElementsByIntersection()


class Set(ZoneJointContainer):
	def __init__(self, set: _api.Set):
		self._Entity = set

	@property
	def ParentFolder(self) -> Folder:
		result = self._Entity.ParentFolder
		return Folder(result) if result is not None else None

	@property
	def Joints(self) -> JointCol:
		result = self._Entity.Joints
		return JointCol(result) if result is not None else None

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		result = self._Entity.PanelSegments
		return PanelSegmentCol(result) if result is not None else None

	@property
	def Zones(self) -> ZoneCol:
		result = self._Entity.Zones
		return ZoneCol(result) if result is not None else None

	@overload
	def AddJoint(self, joint: Joint) -> CollectionModificationStatus:
		...

	@overload
	def AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus:
		...

	@overload
	def AddZones(self, zones: tuple[Zone]) -> CollectionModificationStatus:
		...

	@overload
	def RemoveJoints(self, jointIds: tuple[int]) -> CollectionModificationStatus:
		...

	@overload
	def RemovePanelSegments(self, segmentIds: tuple[int]) -> CollectionModificationStatus:
		...

	@overload
	def RemoveZones(self, zoneIds: tuple[int]) -> CollectionModificationStatus:
		...

	@overload
	def AddJoint(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	def RemoveJoint(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	def RemoveJoint(self, joint: Joint) -> CollectionModificationStatus:
		...

	@overload
	def RemoveJoints(self, joints: tuple[Joint]) -> CollectionModificationStatus:
		...

	@overload
	def AddZone(self, id: int) -> CollectionModificationStatus:
		'''
		Add an existing zone to this entity.
		'''
		...

	@overload
	def AddZones(self, ids: tuple[int]) -> CollectionModificationStatus:
		'''
		Add existing zones to this entity.
		'''
		...

	@overload
	def AddZone(self, zone: Zone) -> CollectionModificationStatus:
		'''
		Add an existing zone to this entity.
		'''
		...

	@overload
	def RemoveZone(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	def RemoveZone(self, zone: Zone) -> CollectionModificationStatus:
		...

	@overload
	def RemoveZones(self, zones: tuple[Zone]) -> CollectionModificationStatus:
		...

	@overload
	def AddPanelSegment(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	def RemovePanelSegment(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	def RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus:
		...

	@overload
	def RemovePanelSegments(self, segments: tuple[PanelSegment]) -> CollectionModificationStatus:
		...

	def AddJoint(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``AddJoint(self, joint: Joint) -> CollectionModificationStatus``

		Overload 2: ``AddJoint(self, id: int) -> CollectionModificationStatus``
		'''
		if isinstance(item1, Joint):
			return CollectionModificationStatus[self._Entity.AddJoint(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddJoint(item1))

		return CollectionModificationStatus[self._Entity.AddJoint(item1._Entity).ToString()]

	def AddPanelSegment(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus``

		Overload 2: ``AddPanelSegment(self, id: int) -> CollectionModificationStatus``
		'''
		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self._Entity.AddPanelSegment(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddPanelSegment(item1))

		return CollectionModificationStatus[self._Entity.AddPanelSegment(item1._Entity).ToString()]

	def AddZones(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``AddZones(self, zones: tuple[Zone]) -> CollectionModificationStatus``

		Overload 2: ``AddZones(self, ids: tuple[int]) -> CollectionModificationStatus``

		Add existing zones to this entity.
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, Zone) for x in item1):
			zonesList = List[_api.Zone]()
			if item1 is not None:
				for x in item1:
					if x is not None:
						zonesList.Add(x._Entity)
			zonesEnumerable = IEnumerable(zonesList)
			return CollectionModificationStatus[self._Entity.AddZones(zonesEnumerable).ToString()]

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			return CollectionModificationStatus(super().AddZones(item1))

		return CollectionModificationStatus[self._Entity.AddZones(item1).ToString()]

	def RemoveJoints(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemoveJoints(self, jointIds: tuple[int]) -> CollectionModificationStatus``

		Overload 2: ``RemoveJoints(self, joints: tuple[Joint]) -> CollectionModificationStatus``
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			jointIdsList = MakeCSharpIntList(item1)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self._Entity.RemoveJoints(jointIdsEnumerable).ToString()]

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, Joint) for x in item1):
			return CollectionModificationStatus(super().RemoveJoints(item1))

		return CollectionModificationStatus[self._Entity.RemoveJoints(item1).ToString()]

	def RemovePanelSegments(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemovePanelSegments(self, segmentIds: tuple[int]) -> CollectionModificationStatus``

		Overload 2: ``RemovePanelSegments(self, segments: tuple[PanelSegment]) -> CollectionModificationStatus``
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			segmentIdsList = MakeCSharpIntList(item1)
			segmentIdsEnumerable = IEnumerable(segmentIdsList)
			return CollectionModificationStatus[self._Entity.RemovePanelSegments(segmentIdsEnumerable).ToString()]

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, PanelSegment) for x in item1):
			return CollectionModificationStatus(super().RemovePanelSegments(item1))

		return CollectionModificationStatus[self._Entity.RemovePanelSegments(item1).ToString()]

	def RemoveZones(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemoveZones(self, zoneIds: tuple[int]) -> CollectionModificationStatus``

		Overload 2: ``RemoveZones(self, zones: tuple[Zone]) -> CollectionModificationStatus``
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return CollectionModificationStatus[self._Entity.RemoveZones(zoneIdsEnumerable).ToString()]

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, Zone) for x in item1):
			return CollectionModificationStatus(super().RemoveZones(item1))

		return CollectionModificationStatus[self._Entity.RemoveZones(item1).ToString()]

	def RemoveJoint(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemoveJoint(self, id: int) -> CollectionModificationStatus``

		Overload 2: ``RemoveJoint(self, joint: Joint) -> CollectionModificationStatus``
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemoveJoint(item1))

		if isinstance(item1, Joint):
			return CollectionModificationStatus(super().RemoveJoint(item1))

		return CollectionModificationStatus[self._Entity.RemoveJoint(item1).ToString()]

	def AddZone(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``AddZone(self, id: int) -> CollectionModificationStatus``

		Add an existing zone to this entity.

		Overload 2: ``AddZone(self, zone: Zone) -> CollectionModificationStatus``

		Add an existing zone to this entity.
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddZone(item1))

		if isinstance(item1, Zone):
			return CollectionModificationStatus(super().AddZone(item1))

		return CollectionModificationStatus[self._Entity.AddZone(item1).ToString()]

	def RemoveZone(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemoveZone(self, id: int) -> CollectionModificationStatus``

		Overload 2: ``RemoveZone(self, zone: Zone) -> CollectionModificationStatus``
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemoveZone(item1))

		if isinstance(item1, Zone):
			return CollectionModificationStatus(super().RemoveZone(item1))

		return CollectionModificationStatus[self._Entity.RemoveZone(item1).ToString()]

	def RemovePanelSegment(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemovePanelSegment(self, id: int) -> CollectionModificationStatus``

		Overload 2: ``RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus``
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemovePanelSegment(item1))

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus(super().RemovePanelSegment(item1))

		return CollectionModificationStatus[self._Entity.RemovePanelSegment(item1).ToString()]


class PlyCol(IdNameEntityCol[Ply]):
	def __init__(self, plyCol: _api.PlyCol):
		self._Entity = plyCol
		self._CollectedClass = Ply

	@property
	def PlyColList(self) -> tuple[Ply]:
		return tuple([Ply(plyCol) for plyCol in self._Entity])

	def Delete(self, id: int) -> CollectionModificationStatus:
		return CollectionModificationStatus[self._Entity.Delete(id).ToString()]

	def DeleteAll(self) -> None:
		'''
		Delete all plies in the collection.
		'''
		return self._Entity.DeleteAll()

	def ExportToCSV(self, filepath: str) -> None:
		'''
		This feature is in development and may not work as expected. Use at your own risk!
		'''
		return self._Entity.ExportToCSV(filepath)

	def ImportCSV(self, filepath: str) -> None:
		return self._Entity.ImportCSV(filepath)

	@overload
	def Get(self, name: str) -> Ply:
		...

	@overload
	def Get(self, id: int) -> Ply:
		...

	def Get(self, item1 = None) -> Ply:
		'''
		Overload 1: ``Get(self, name: str) -> Ply``

		Overload 2: ``Get(self, id: int) -> Ply``
		'''
		if isinstance(item1, str):
			return Ply(super().Get(item1))

		if isinstance(item1, int):
			return Ply(super().Get(item1))

		return Ply(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.PlyColList[index]

	def __iter__(self):
		yield from self.PlyColList

	def __len__(self):
		return len(self.PlyColList)


class Structure(ZoneJointContainer):
	def __init__(self, structure: _api.Structure):
		self._Entity = structure

	@property
	def ParentFolder(self) -> Folder:
		result = self._Entity.ParentFolder
		return Folder(result) if result is not None else None

	@property
	def Plies(self) -> PlyCol:
		result = self._Entity.Plies
		return PlyCol(result) if result is not None else None

	@property
	def Joints(self) -> JointCol:
		result = self._Entity.Joints
		return JointCol(result) if result is not None else None

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		result = self._Entity.PanelSegments
		return PanelSegmentCol(result) if result is not None else None

	@property
	def Zones(self) -> ZoneCol:
		result = self._Entity.Zones
		return ZoneCol(result) if result is not None else None

	def ExportVCP(self, fileName: str) -> None:
		'''
		Export VCP with this structure's element centroids.
		'''
		return self._Entity.ExportVCP(fileName)

	def AddElementsAndAssignDesigns(self, elementIds: tuple[int], overrideMetalDesigns: bool = False, overrideLaminateDesigns: bool = False) -> types.SimpleStatus:
		elementIdsList = MakeCSharpIntList(elementIds)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		return types.SimpleStatus(self._Entity.AddElementsAndAssignDesigns(elementIdsEnumerable, overrideMetalDesigns, overrideLaminateDesigns))

	def AddElements(self, elementIds: tuple[int]) -> CollectionModificationStatus:
		elementIdsList = MakeCSharpIntList(elementIds)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		return CollectionModificationStatus[self._Entity.AddElements(elementIdsEnumerable).ToString()]

	@overload
	def AddJoint(self, joint: Joint) -> CollectionModificationStatus:
		...

	@overload
	def AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus:
		...

	def AddPfemPropertiesAndAssignDesigns(self, pfemPropertyIds: tuple[int], overrideMetalDesigns: bool = False, overrideLaminateDesigns: bool = False) -> types.SimpleStatus:
		pfemPropertyIdsList = MakeCSharpIntList(pfemPropertyIds)
		pfemPropertyIdsEnumerable = IEnumerable(pfemPropertyIdsList)
		return types.SimpleStatus(self._Entity.AddPfemPropertiesAndAssignDesigns(pfemPropertyIdsEnumerable, overrideMetalDesigns, overrideLaminateDesigns))

	def AddPfemProperties(self, pfemPropertyIds: tuple[int]) -> CollectionModificationStatus:
		pfemPropertyIdsList = MakeCSharpIntList(pfemPropertyIds)
		pfemPropertyIdsEnumerable = IEnumerable(pfemPropertyIdsList)
		return CollectionModificationStatus[self._Entity.AddPfemProperties(pfemPropertyIdsEnumerable).ToString()]

	@overload
	def AddZones(self, zones: tuple[Zone]) -> CollectionModificationStatus:
		...

	def CreateZone(self, elementIds: tuple[int], name: str = None) -> Zone:
		elementIdsList = MakeCSharpIntList(elementIds)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		result = self._Entity.CreateZone(elementIdsEnumerable, name)
		thisClass = type(result).__name__
		givenClass = Zone
		for subclass in _all_subclasses(Zone):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def CreatePanelSegment(self, discreteTechnique: types.DiscreteTechnique, discreteElementLkp: dict[types.DiscreteDefinitionType, list[int]], name: str = None) -> PanelSegment:
		discreteElementLkpDict = Dictionary[_types.DiscreteDefinitionType, List[int]]()
		for kvp in discreteElementLkp:
			dictValue = discreteElementLkp[kvp]
			dictValueList = MakeCSharpIntList(dictValue)
			discreteElementLkpDict.Add(_types.DiscreteDefinitionType(types.GetEnumValue(kvp.value)), dictValueList)
		return PanelSegment(self._Entity.CreatePanelSegment(_types.DiscreteTechnique(types.GetEnumValue(discreteTechnique.value)), discreteElementLkpDict, name))

	@overload
	def Remove(self, zoneIds: tuple[int], jointIds: tuple[int]) -> CollectionModificationStatus:
		...

	@overload
	def Remove(self, zoneIds: tuple[int], jointIds: tuple[int], panelSegmentIds: tuple[int]) -> CollectionModificationStatus:
		...

	@overload
	def RemoveJoints(self, jointIds: tuple[int]) -> CollectionModificationStatus:
		...

	@overload
	def RemovePanelSegments(self, segmentIds: tuple[int]) -> CollectionModificationStatus:
		...

	@overload
	def RemoveZones(self, zoneIds: tuple[int]) -> CollectionModificationStatus:
		'''
		Sends provided zones back to unused FEM
		'''
		...

	@overload
	def AddJoint(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	def RemoveJoint(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	def RemoveJoint(self, joint: Joint) -> CollectionModificationStatus:
		...

	@overload
	def RemoveJoints(self, joints: tuple[Joint]) -> CollectionModificationStatus:
		...

	@overload
	def AddZone(self, id: int) -> CollectionModificationStatus:
		'''
		Add an existing zone to this entity.
		'''
		...

	@overload
	def AddZones(self, ids: tuple[int]) -> CollectionModificationStatus:
		'''
		Add existing zones to this entity.
		'''
		...

	@overload
	def AddZone(self, zone: Zone) -> CollectionModificationStatus:
		'''
		Add an existing zone to this entity.
		'''
		...

	@overload
	def RemoveZone(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	def RemoveZone(self, zone: Zone) -> CollectionModificationStatus:
		...

	@overload
	def RemoveZones(self, zones: tuple[Zone]) -> CollectionModificationStatus:
		...

	@overload
	def AddPanelSegment(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	def RemovePanelSegment(self, id: int) -> CollectionModificationStatus:
		...

	@overload
	def RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus:
		...

	@overload
	def RemovePanelSegments(self, segments: tuple[PanelSegment]) -> CollectionModificationStatus:
		...

	def AddJoint(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``AddJoint(self, joint: Joint) -> CollectionModificationStatus``

		Overload 2: ``AddJoint(self, id: int) -> CollectionModificationStatus``
		'''
		if isinstance(item1, Joint):
			return CollectionModificationStatus[self._Entity.AddJoint(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddJoint(item1))

		return CollectionModificationStatus[self._Entity.AddJoint(item1._Entity).ToString()]

	def AddPanelSegment(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus``

		Overload 2: ``AddPanelSegment(self, id: int) -> CollectionModificationStatus``
		'''
		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self._Entity.AddPanelSegment(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddPanelSegment(item1))

		return CollectionModificationStatus[self._Entity.AddPanelSegment(item1._Entity).ToString()]

	def AddZones(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``AddZones(self, zones: tuple[Zone]) -> CollectionModificationStatus``

		Overload 2: ``AddZones(self, ids: tuple[int]) -> CollectionModificationStatus``

		Add existing zones to this entity.
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, Zone) for x in item1):
			zonesList = List[_api.Zone]()
			if item1 is not None:
				for x in item1:
					if x is not None:
						zonesList.Add(x._Entity)
			zonesEnumerable = IEnumerable(zonesList)
			return CollectionModificationStatus[self._Entity.AddZones(zonesEnumerable).ToString()]

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			return CollectionModificationStatus(super().AddZones(item1))

		return CollectionModificationStatus[self._Entity.AddZones(item1).ToString()]

	def Remove(self, item1 = None, item2 = None, item3 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``Remove(self, zoneIds: tuple[int], jointIds: tuple[int]) -> CollectionModificationStatus``

		Overload 2: ``Remove(self, zoneIds: tuple[int], jointIds: tuple[int], panelSegmentIds: tuple[int]) -> CollectionModificationStatus``
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1) and (isinstance(item2, tuple) or isinstance(item2, list) or isinstance(item2, set)) and item2 and any(isinstance(x, int) for x in item2) and (isinstance(item3, tuple) or isinstance(item3, list) or isinstance(item3, set)) and item3 and any(isinstance(x, int) for x in item3):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			jointIdsList = MakeCSharpIntList(item2)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			panelSegmentIdsList = MakeCSharpIntList(item3)
			panelSegmentIdsEnumerable = IEnumerable(panelSegmentIdsList)
			return CollectionModificationStatus[self._Entity.Remove(zoneIdsEnumerable, jointIdsEnumerable, panelSegmentIdsEnumerable).ToString()]

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1) and (isinstance(item2, tuple) or isinstance(item2, list) or isinstance(item2, set)) and item2 and any(isinstance(x, int) for x in item2):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			jointIdsList = MakeCSharpIntList(item2)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self._Entity.Remove(zoneIdsEnumerable, jointIdsEnumerable).ToString()]

		return CollectionModificationStatus[self._Entity.Remove(item1, item2, item3).ToString()]

	def RemoveJoints(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemoveJoints(self, jointIds: tuple[int]) -> CollectionModificationStatus``

		Overload 2: ``RemoveJoints(self, joints: tuple[Joint]) -> CollectionModificationStatus``
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			jointIdsList = MakeCSharpIntList(item1)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self._Entity.RemoveJoints(jointIdsEnumerable).ToString()]

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, Joint) for x in item1):
			return CollectionModificationStatus(super().RemoveJoints(item1))

		return CollectionModificationStatus[self._Entity.RemoveJoints(item1).ToString()]

	def RemovePanelSegments(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemovePanelSegments(self, segmentIds: tuple[int]) -> CollectionModificationStatus``

		Overload 2: ``RemovePanelSegments(self, segments: tuple[PanelSegment]) -> CollectionModificationStatus``
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			segmentIdsList = MakeCSharpIntList(item1)
			segmentIdsEnumerable = IEnumerable(segmentIdsList)
			return CollectionModificationStatus[self._Entity.RemovePanelSegments(segmentIdsEnumerable).ToString()]

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, PanelSegment) for x in item1):
			return CollectionModificationStatus(super().RemovePanelSegments(item1))

		return CollectionModificationStatus[self._Entity.RemovePanelSegments(item1).ToString()]

	def RemoveZones(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemoveZones(self, zoneIds: tuple[int]) -> CollectionModificationStatus``

		Sends provided zones back to unused FEM

		Overload 2: ``RemoveZones(self, zones: tuple[Zone]) -> CollectionModificationStatus``
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return CollectionModificationStatus[self._Entity.RemoveZones(zoneIdsEnumerable).ToString()]

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, Zone) for x in item1):
			return CollectionModificationStatus(super().RemoveZones(item1))

		return CollectionModificationStatus[self._Entity.RemoveZones(item1).ToString()]

	def RemoveJoint(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemoveJoint(self, id: int) -> CollectionModificationStatus``

		Overload 2: ``RemoveJoint(self, joint: Joint) -> CollectionModificationStatus``
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemoveJoint(item1))

		if isinstance(item1, Joint):
			return CollectionModificationStatus(super().RemoveJoint(item1))

		return CollectionModificationStatus[self._Entity.RemoveJoint(item1).ToString()]

	def AddZone(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``AddZone(self, id: int) -> CollectionModificationStatus``

		Add an existing zone to this entity.

		Overload 2: ``AddZone(self, zone: Zone) -> CollectionModificationStatus``

		Add an existing zone to this entity.
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddZone(item1))

		if isinstance(item1, Zone):
			return CollectionModificationStatus(super().AddZone(item1))

		return CollectionModificationStatus[self._Entity.AddZone(item1).ToString()]

	def RemoveZone(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemoveZone(self, id: int) -> CollectionModificationStatus``

		Overload 2: ``RemoveZone(self, zone: Zone) -> CollectionModificationStatus``
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemoveZone(item1))

		if isinstance(item1, Zone):
			return CollectionModificationStatus(super().RemoveZone(item1))

		return CollectionModificationStatus[self._Entity.RemoveZone(item1).ToString()]

	def RemovePanelSegment(self, item1 = None) -> CollectionModificationStatus:
		'''
		Overload 1: ``RemovePanelSegment(self, id: int) -> CollectionModificationStatus``

		Overload 2: ``RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus``
		'''
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemovePanelSegment(item1))

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus(super().RemovePanelSegment(item1))

		return CollectionModificationStatus[self._Entity.RemovePanelSegment(item1).ToString()]


class AnalysisPropertyCol(IdNameEntityCol[AnalysisProperty]):
	def __init__(self, analysisPropertyCol: _api.AnalysisPropertyCol):
		self._Entity = analysisPropertyCol
		self._CollectedClass = AnalysisProperty

	@property
	def AnalysisPropertyColList(self) -> tuple[AnalysisProperty]:
		return tuple([AnalysisProperty(analysisPropertyCol) for analysisPropertyCol in self._Entity])

	def CreateAnalysisProperty(self, type: types.FamilyCategory, name: str = None) -> AnalysisProperty:
		'''
		Creates and returns an ``hyperx.api.AnalysisProperty``.
		HyperX will handle any naming conflicts, so it is important to use the returned ``hyperx.api.AnalysisProperty``
		which may have a different name to what was provided.
		
		:return: The created ``hyperx.api.AnalysisProperty``.
		'''
		return AnalysisProperty(self._Entity.CreateAnalysisProperty(_types.FamilyCategory(types.GetEnumValue(type.value)), name))

	@overload
	def DeleteAnalysisProperty(self, name: str) -> bool:
		'''
		Delete an ``hyperx.api.AnalysisProperty``.
		
		:return: ``False`` if there is no analysis property in the collection with the given name.
		'''
		...

	@overload
	def DeleteAnalysisProperty(self, id: int) -> bool:
		'''
		Delete an ``hyperx.api.AnalysisProperty``.
		
		:return: ``False`` if there is no analysis property in the collection with the given ID.
		'''
		...

	@overload
	def Get(self, name: str) -> AnalysisProperty:
		...

	@overload
	def Get(self, id: int) -> AnalysisProperty:
		...

	def DeleteAnalysisProperty(self, item1 = None) -> bool:
		'''
		Overload 1: ``DeleteAnalysisProperty(self, name: str) -> bool``

		Delete an ``hyperx.api.AnalysisProperty``.
		
		:return: ``False`` if there is no analysis property in the collection with the given name.

		Overload 2: ``DeleteAnalysisProperty(self, id: int) -> bool``

		Delete an ``hyperx.api.AnalysisProperty``.
		
		:return: ``False`` if there is no analysis property in the collection with the given ID.
		'''
		if isinstance(item1, str):
			return self._Entity.DeleteAnalysisProperty(item1)

		if isinstance(item1, int):
			return self._Entity.DeleteAnalysisProperty(item1)

		return self._Entity.DeleteAnalysisProperty(item1)

	def Get(self, item1 = None) -> AnalysisProperty:
		'''
		Overload 1: ``Get(self, name: str) -> AnalysisProperty``

		Overload 2: ``Get(self, id: int) -> AnalysisProperty``
		'''
		if isinstance(item1, str):
			return AnalysisProperty(super().Get(item1))

		if isinstance(item1, int):
			return AnalysisProperty(super().Get(item1))

		return AnalysisProperty(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.AnalysisPropertyColList[index]

	def __iter__(self):
		yield from self.AnalysisPropertyColList

	def __len__(self):
		return len(self.AnalysisPropertyColList)


class DesignPropertyCol(IdNameEntityCol[DesignProperty]):
	def __init__(self, designPropertyCol: _api.DesignPropertyCol):
		self._Entity = designPropertyCol
		self._CollectedClass = DesignProperty

	@property
	def DesignPropertyColList(self) -> tuple[DesignProperty]:
		designPropertyColList = []
		subclasses = {x.__name__: x for x in _all_subclasses(DesignProperty)}
		for designPropertyCol in self._Entity:
			if type(designPropertyCol).__name__ in subclasses.keys():
				thisType = subclasses[type(designPropertyCol).__name__]
				designPropertyColList.append(thisType(designPropertyCol))
			else:
				raise Exception(f"Could not wrap item in DesignPropertyCol. This should not happen.")
		return tuple(designPropertyColList)

	def CreateDesignProperty(self, familyConcept: types.FamilyConceptUID, materialMode: types.MaterialMode = types.MaterialMode.Any, name: str = None, discreteTechnique: types.DiscreteTechnique = None) -> DesignProperty:
		'''
		Creates and returns a ``hyperx.api.DesignProperty``.
		HyperX will handle any naming conflicts, so it is important to use the returned ``hyperx.api.DesignProperty``
		which may have a different name to what was provided.
		
		:return: The created ``hyperx.api.DesignProperty``.
		'''
		result = self._Entity.CreateDesignProperty(_types.FamilyConceptUID(types.GetEnumValue(familyConcept.value)), _types.MaterialMode(types.GetEnumValue(materialMode.value)), name, discreteTechnique if discreteTechnique is None else _types.DiscreteTechnique(types.GetEnumValue(discreteTechnique.value)))
		thisClass = type(result).__name__
		givenClass = DesignProperty
		for subclass in _all_subclasses(DesignProperty):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@overload
	def DeleteDesignProperty(self, name: str) -> bool:
		'''
		Delete a ``hyperx.api.DesignProperty``.
		
		:return: ``False`` if there is no design property in the collection with the given name.
		'''
		...

	@overload
	def DeleteDesignProperty(self, id: int) -> bool:
		'''
		Delete a ``hyperx.api.DesignProperty``.
		
		:return: ``False`` if there is no design property in the collection with the given ID.
		'''
		...

	@overload
	def Get(self, name: str) -> DesignProperty:
		...

	@overload
	def Get(self, id: int) -> DesignProperty:
		...

	def DeleteDesignProperty(self, item1 = None) -> bool:
		'''
		Overload 1: ``DeleteDesignProperty(self, name: str) -> bool``

		Delete a ``hyperx.api.DesignProperty``.
		
		:return: ``False`` if there is no design property in the collection with the given name.

		Overload 2: ``DeleteDesignProperty(self, id: int) -> bool``

		Delete a ``hyperx.api.DesignProperty``.
		
		:return: ``False`` if there is no design property in the collection with the given ID.
		'''
		if isinstance(item1, str):
			return self._Entity.DeleteDesignProperty(item1)

		if isinstance(item1, int):
			return self._Entity.DeleteDesignProperty(item1)

		return self._Entity.DeleteDesignProperty(item1)

	def Get(self, item1 = None) -> DesignProperty:
		'''
		Overload 1: ``Get(self, name: str) -> DesignProperty``

		Overload 2: ``Get(self, id: int) -> DesignProperty``
		'''
		if isinstance(item1, str):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = DesignProperty
			for subclass in _all_subclasses(DesignProperty):
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, int):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = DesignProperty
			for subclass in _all_subclasses(DesignProperty):
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		result = self._Entity.Get(item1)
		thisClass = type(result).__name__
		givenClass = DesignProperty
		for subclass in _all_subclasses(DesignProperty):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def __getitem__(self, index: int):
		return self.DesignPropertyColList[index]

	def __iter__(self):
		yield from self.DesignPropertyColList

	def __len__(self):
		return len(self.DesignPropertyColList)


class LoadPropertyCol(IdNameEntityCol[LoadProperty]):
	def __init__(self, loadPropertyCol: _api.LoadPropertyCol):
		self._Entity = loadPropertyCol
		self._CollectedClass = LoadProperty

	@property
	def LoadPropertyColList(self) -> tuple[LoadProperty]:
		loadPropertyColList = []
		subclasses = {x.__name__: x for x in _all_subclasses(LoadProperty)}
		for loadPropertyCol in self._Entity:
			if type(loadPropertyCol).__name__ in subclasses.keys():
				thisType = subclasses[type(loadPropertyCol).__name__]
				loadPropertyColList.append(thisType(loadPropertyCol))
			else:
				raise Exception(f"Could not wrap item in LoadPropertyCol. This should not happen.")
		return tuple(loadPropertyColList)

	def CreateLoadProperty(self, loadPropertyType: types.LoadPropertyType, category: types.FamilyCategory, name: str = None) -> LoadProperty:
		'''
		Creates and returns a new ``hyperx.api.LoadProperty``.
		HyperX will handle any naming conflicts, so it is important to use the returned ``hyperx.api.LoadProperty``
		which may have a different name to what was provided.
		
		:return: The created ``hyperx.api.LoadProperty``.
		'''
		result = self._Entity.CreateLoadProperty(_types.LoadPropertyType(types.GetEnumValue(loadPropertyType.value)), _types.FamilyCategory(types.GetEnumValue(category.value)), name)
		thisClass = type(result).__name__
		givenClass = LoadProperty
		for subclass in _all_subclasses(LoadProperty):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@overload
	def DeleteLoadProperty(self, id: int) -> bool:
		'''
		Remove a ``hyperx.api.LoadProperty`` by ``id``.
		
		:return: ``True`` if successfully deleted.
		'''
		...

	@overload
	def DeleteLoadProperty(self, name: str) -> bool:
		'''
		Remove a ``hyperx.api.LoadProperty`` by ``name``.
		
		:return: ``True`` if successfully deleted.
		'''
		...

	@overload
	def Get(self, name: str) -> LoadProperty:
		...

	@overload
	def Get(self, id: int) -> LoadProperty:
		...

	def DeleteLoadProperty(self, item1 = None) -> bool:
		'''
		Overload 1: ``DeleteLoadProperty(self, id: int) -> bool``

		Remove a ``hyperx.api.LoadProperty`` by ``id``.
		
		:return: ``True`` if successfully deleted.

		Overload 2: ``DeleteLoadProperty(self, name: str) -> bool``

		Remove a ``hyperx.api.LoadProperty`` by ``name``.
		
		:return: ``True`` if successfully deleted.
		'''
		if isinstance(item1, int):
			return self._Entity.DeleteLoadProperty(item1)

		if isinstance(item1, str):
			return self._Entity.DeleteLoadProperty(item1)

		return self._Entity.DeleteLoadProperty(item1)

	def Get(self, item1 = None) -> LoadProperty:
		'''
		Overload 1: ``Get(self, name: str) -> LoadProperty``

		Overload 2: ``Get(self, id: int) -> LoadProperty``
		'''
		if isinstance(item1, str):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = LoadProperty
			for subclass in _all_subclasses(LoadProperty):
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, int):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = LoadProperty
			for subclass in _all_subclasses(LoadProperty):
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		result = self._Entity.Get(item1)
		thisClass = type(result).__name__
		givenClass = LoadProperty
		for subclass in _all_subclasses(LoadProperty):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def __getitem__(self, index: int):
		return self.LoadPropertyColList[index]

	def __iter__(self):
		yield from self.LoadPropertyColList

	def __len__(self):
		return len(self.LoadPropertyColList)


class DesignLoadCol(IdNameEntityCol[DesignLoad]):
	def __init__(self, designLoadCol: _api.DesignLoadCol):
		self._Entity = designLoadCol
		self._CollectedClass = DesignLoad

	@property
	def DesignLoadColList(self) -> tuple[DesignLoad]:
		return tuple([DesignLoad(designLoadCol) for designLoadCol in self._Entity])

	@property
	def FilterOptions(self) -> types.DesignLoadFilteringOptions:
		'''
		Options to determine how design load filtering is applied or updated during sizing and analysis.
		'''
		result = self._Entity.FilterOptions
		return types.DesignLoadFilteringOptions[result.ToString()] if result is not None else None

	@FilterOptions.setter
	def FilterOptions(self, value: types.DesignLoadFilteringOptions) -> None:
		self._Entity.FilterOptions = _types.DesignLoadFilteringOptions(types.GetEnumValue(value.value))

	def SetIsActiveById(self, designLoads: set[int], isActive: bool) -> types.SimpleStatus:
		'''
		Set the ``hyperx.api.DesignLoad.IsActive></see> flag for a set of ``hyperx.api.DesignLoad></see> based on the ``isActive`` parameter.
		'''
		designLoadsSet = HashSet[int]()
		if designLoads is not None:
			for x in designLoads:
				if x is not None:
					designLoadsSet.Add(x)
		return types.SimpleStatus(self._Entity.SetIsActiveById(designLoadsSet, isActive))

	def SetIsActiveByName(self, designLoads: set[str], isActive: bool) -> types.SimpleStatus:
		'''
		Set the ``hyperx.api.DesignLoad.IsActive></see> flag for a set of ``hyperx.api.DesignLoad></see> based on the ``isActive`` parameter.
		'''
		designLoadsSet = HashSet[str]()
		if designLoads is not None:
			for x in designLoads:
				if x is not None:
					designLoadsSet.Add(x)
		return types.SimpleStatus(self._Entity.SetIsActiveByName(designLoadsSet, isActive))

	@overload
	def Get(self, name: str) -> DesignLoad:
		...

	@overload
	def Get(self, id: int) -> DesignLoad:
		...

	def Get(self, item1 = None) -> DesignLoad:
		'''
		Overload 1: ``Get(self, name: str) -> DesignLoad``

		Overload 2: ``Get(self, id: int) -> DesignLoad``
		'''
		if isinstance(item1, str):
			return DesignLoad(super().Get(item1))

		if isinstance(item1, int):
			return DesignLoad(super().Get(item1))

		return DesignLoad(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.DesignLoadColList[index]

	def __iter__(self):
		yield from self.DesignLoadColList

	def __len__(self):
		return len(self.DesignLoadColList)


class DiscreteFieldCol(IdNameEntityCol[DiscreteField]):
	def __init__(self, discreteFieldCol: _api.DiscreteFieldCol):
		self._Entity = discreteFieldCol
		self._CollectedClass = DiscreteField

	@property
	def DiscreteFieldColList(self) -> tuple[DiscreteField]:
		return tuple([DiscreteField(discreteFieldCol) for discreteFieldCol in self._Entity])

	def Create(self, entityType: types.DiscreteFieldPhysicalEntityType, dataType: types.DiscreteFieldDataType, name: str = None) -> DiscreteField:
		'''
		Create a new DiscreteField.
		
		:return: The created DiscreteField.
		'''
		return DiscreteField(self._Entity.Create(_types.DiscreteFieldPhysicalEntityType(types.GetEnumValue(entityType.value)), _types.DiscreteFieldDataType(types.GetEnumValue(dataType.value)), name))

	def CreateFromVCP(self, filepath: str) -> list[DiscreteField]:
		'''
		Create a list of DiscreteFields from VCP.
		
		:return: The list of created DiscreteFields.
		
		:raises ``System.InvalidOperationException``:
		'''
		return [DiscreteField(discreteField) for discreteField in self._Entity.CreateFromVCP(filepath)]

	def Delete(self, id: int) -> CollectionModificationStatus:
		'''
		In the event of getting a CollectionModificationStatus.EntityMissingRemovalFailure,
		note that the discrete field is associated with a ply, and therefore cannot be deleted.
		'''
		return CollectionModificationStatus[self._Entity.Delete(id).ToString()]

	def CreateByPointMapToElements(self, elementIds: tuple[int], discreteFieldIds: tuple[int], suffix: str = None, tolerance: float = None) -> list[DiscreteField]:
		'''
		Create Discrete Fields by mapping existing Point-based Discrete Fields to new element-based Discrete Fields.
		
		:return: The list of created DiscreteFields.
		
		:raises ``System.InvalidOperationException``:
		'''
		elementIdsList = MakeCSharpIntList(elementIds)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		discreteFieldIdsList = MakeCSharpIntList(discreteFieldIds)
		discreteFieldIdsEnumerable = IEnumerable(discreteFieldIdsList)
		return [DiscreteField(discreteField) for discreteField in self._Entity.CreateByPointMapToElements(elementIdsEnumerable, discreteFieldIdsEnumerable, suffix, tolerance)]

	@overload
	def Get(self, name: str) -> DiscreteField:
		...

	@overload
	def Get(self, id: int) -> DiscreteField:
		...

	def Get(self, item1 = None) -> DiscreteField:
		'''
		Overload 1: ``Get(self, name: str) -> DiscreteField``

		Overload 2: ``Get(self, id: int) -> DiscreteField``
		'''
		if isinstance(item1, str):
			return DiscreteField(super().Get(item1))

		if isinstance(item1, int):
			return DiscreteField(super().Get(item1))

		return DiscreteField(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.DiscreteFieldColList[index]

	def __iter__(self):
		yield from self.DiscreteFieldColList

	def __len__(self):
		return len(self.DiscreteFieldColList)


class FolderCol(IdNameEntityCol[Folder]):
	def __init__(self, folderCol: _api.FolderCol):
		self._Entity = folderCol
		self._CollectedClass = Folder

	@property
	def FolderColList(self) -> tuple[Folder]:
		return tuple([Folder(folderCol) for folderCol in self._Entity])

	@property
	def ParentFolder(self) -> Folder:
		result = self._Entity.ParentFolder
		return Folder(result) if result is not None else None

	def AddFolder(self, name: str) -> Folder:
		return Folder(self._Entity.AddFolder(name))

	def AddFolders(self, names: tuple[str]) -> tuple[Folder]:
		namesList = List[str]()
		if names is not None:
			for x in names:
				if x is not None:
					namesList.Add(x)
		namesEnumerable = IEnumerable(namesList)
		return [Folder(folder) for folder in self._Entity.AddFolders(namesEnumerable)]

	def DeleteFolder(self, folder: Folder) -> bool:
		return self._Entity.DeleteFolder(folder._Entity)

	def DeleteFolders(self, folders: tuple[Folder]) -> bool:
		foldersList = List[_api.Folder]()
		if folders is not None:
			for x in folders:
				if x is not None:
					foldersList.Add(x._Entity)
		foldersEnumerable = IEnumerable(foldersList)
		return self._Entity.DeleteFolders(foldersEnumerable)

	@overload
	def Get(self, name: str) -> Folder:
		...

	@overload
	def Get(self, id: int) -> Folder:
		...

	def Get(self, item1 = None) -> Folder:
		'''
		Overload 1: ``Get(self, name: str) -> Folder``

		Overload 2: ``Get(self, id: int) -> Folder``
		'''
		if isinstance(item1, str):
			return Folder(super().Get(item1))

		if isinstance(item1, int):
			return Folder(super().Get(item1))

		return Folder(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.FolderColList[index]

	def __iter__(self):
		yield from self.FolderColList

	def __len__(self):
		return len(self.FolderColList)


class ZoneJointContainerCol(IdNameEntityCol, Generic[T]):
	def __init__(self, zoneJointContainerCol: _api.ZoneJointContainerCol):
		self._Entity = zoneJointContainerCol
		self._CollectedClass = T

	@abstractmethod
	def Create(self, name: str) -> ZoneJointContainer:
		return self._Entity.Create(name)

	@overload
	def Get(self, name: str) -> ZoneJointContainer:
		...

	@overload
	def Get(self, id: int) -> ZoneJointContainer:
		...

	def Get(self, item1 = None) -> ZoneJointContainer:
		'''
		Overload 1: ``Get(self, name: str) -> ZoneJointContainer``

		Overload 2: ``Get(self, id: int) -> ZoneJointContainer``
		'''
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

		return self._Entity.Get(item1)


class RundeckCol(IdEntityCol[Rundeck]):
	def __init__(self, rundeckCol: _api.RundeckCol):
		self._Entity = rundeckCol
		self._CollectedClass = Rundeck

	@property
	def RundeckColList(self) -> tuple[Rundeck]:
		return tuple([Rundeck(rundeckCol) for rundeckCol in self._Entity])

	def AddRundeck(self, inputPath: str, resultPath: str = None) -> Rundeck:
		'''
		The specified rundeck at the given filepath will be added to the project's
		collection of rundecks
		
		:param inputPath: The path to the rundeck
		:param resultPath: The path to the rundeck's corresponding result file
		'''
		return Rundeck(self._Entity.AddRundeck(inputPath, resultPath))

	def ReassignPrimary(self, id: int) -> RundeckUpdateStatus:
		'''
		The specified rundeck will be updated to become the new primary rundeck.
		It is best practice to call ``hyperx.api.Project.RegeneratePfem`` after
		reassigning the primary rundeck
		'''
		return RundeckUpdateStatus[self._Entity.ReassignPrimary(id).ToString()]

	def RemoveRundeck(self, id: int) -> RundeckRemoveStatus:
		'''
		The specified rundeck at the given filepath will be removed from the project's
		collection of rundecks
		
		:param id: The id of the rundeck to remove
		'''
		return RundeckRemoveStatus[self._Entity.RemoveRundeck(id).ToString()]

	def UpdateAllRundecks(self, newPaths: tuple[RundeckPathPair]) -> RundeckBulkUpdateStatus:
		'''
		Updates the path of all rundecks. The order of newPaths should correspond with the rundeck ids (i.e. The first item in newPaths will update the primary rundeck's paths).
		'''
		newPathsList = List[_api.RundeckPathPair]()
		if newPaths is not None:
			for x in newPaths:
				if x is not None:
					newPathsList.Add(x._Entity)
		newPathsEnumerable = IEnumerable(newPathsList)
		return RundeckBulkUpdateStatus[self._Entity.UpdateAllRundecks(newPathsEnumerable).ToString()]

	def GetRundeckPathSetters(self) -> list[RundeckPathPair]:
		'''
		Get RundeckPathSetters to be edited and input to UpdateAllRundecks.
		'''
		return [RundeckPathPair(rundeckPathPair) for rundeckPathPair in self._Entity.GetRundeckPathSetters()]

	def ReplaceStringInAllPaths(self, stringToReplace: str, newString: str) -> RundeckBulkUpdateStatus:
		'''
		Replace a given string with a new string in every rundeck path. This is useful when pointing to rundecks of the same name in a new directory.
		'''
		return RundeckBulkUpdateStatus[self._Entity.ReplaceStringInAllPaths(stringToReplace, newString).ToString()]

	def __getitem__(self, index: int):
		return self.RundeckColList[index]

	def __iter__(self):
		yield from self.RundeckColList

	def __len__(self):
		return len(self.RundeckColList)


class SectionCutCol(IdNameEntityCol[SectionCut]):
	def __init__(self, sectionCutCol: _api.SectionCutCol):
		self._Entity = sectionCutCol
		self._CollectedClass = SectionCut

	@property
	def SectionCutColList(self) -> tuple[SectionCut]:
		return tuple([SectionCut(sectionCutCol) for sectionCutCol in self._Entity])

	@property
	def Folders(self) -> FolderCol:
		result = self._Entity.Folders
		return FolderCol(result) if result is not None else None

	def Create(self, origin: Vector3d, normal: Vector3d, horizontal: Vector3d, name: str = None) -> SectionCut:
		return SectionCut(self._Entity.Create(origin._Entity, normal._Entity, horizontal._Entity, name))

	def Delete(self, id: int) -> CollectionModificationStatus:
		return CollectionModificationStatus[self._Entity.Delete(id).ToString()]

	@overload
	def Get(self, name: str) -> SectionCut:
		...

	@overload
	def Get(self, id: int) -> SectionCut:
		...

	def Get(self, item1 = None) -> SectionCut:
		'''
		Overload 1: ``Get(self, name: str) -> SectionCut``

		Overload 2: ``Get(self, id: int) -> SectionCut``
		'''
		if isinstance(item1, str):
			return SectionCut(super().Get(item1))

		if isinstance(item1, int):
			return SectionCut(super().Get(item1))

		return SectionCut(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.SectionCutColList[index]

	def __iter__(self):
		yield from self.SectionCutColList

	def __len__(self):
		return len(self.SectionCutColList)


class SetCol(ZoneJointContainerCol[Set]):
	def __init__(self, setCol: _api.SetCol):
		self._Entity = setCol
		self._CollectedClass = Set

	@property
	def SetColList(self) -> tuple[Set]:
		return tuple([Set(setCol) for setCol in self._Entity])

	@property
	def Folders(self) -> FolderCol:
		result = self._Entity.Folders
		return FolderCol(result) if result is not None else None

	def Create(self, name: str = None) -> Set:
		'''
		Attempt to create a new Set.
		
		:param name: The name of the set to be created.
		
		:return: The created Set.
		'''
		return Set(self._Entity.Create(name))

	@overload
	def Get(self, name: str) -> Set:
		...

	@overload
	def Get(self, id: int) -> Set:
		...

	def Get(self, item1 = None) -> Set:
		'''
		Overload 1: ``Get(self, name: str) -> Set``

		Overload 2: ``Get(self, id: int) -> Set``
		'''
		if isinstance(item1, str):
			return Set(super().Get(item1))

		if isinstance(item1, int):
			return Set(super().Get(item1))

		return Set(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.SetColList[index]

	def __iter__(self):
		yield from self.SetColList

	def __len__(self):
		return len(self.SetColList)


class StructureCol(ZoneJointContainerCol[Structure]):
	def __init__(self, structureCol: _api.StructureCol):
		self._Entity = structureCol
		self._CollectedClass = Structure

	@property
	def StructureColList(self) -> tuple[Structure]:
		return tuple([Structure(structureCol) for structureCol in self._Entity])

	@property
	def Folders(self) -> FolderCol:
		result = self._Entity.Folders
		return FolderCol(result) if result is not None else None

	def Create(self, name: str = None) -> Structure:
		'''
		Attempt to create a new structure.
		If the specified name is already used, it will be deconflicted.
		
		:param name: The name of the structure to be created.
		
		:return: Return the new Structure
		'''
		return Structure(self._Entity.Create(name))

	@overload
	def DeleteStructure(self, structure: Structure) -> bool:
		'''
		Returns true if the structure was deleted from the collection. Returns false if the structure could not be found or if there are run sets in the project.
		'''
		...

	@overload
	def DeleteStructure(self, name: str) -> bool:
		'''
		Returns true if the structure was deleted from the collection. Returns false if the structure could not be found or if there are run sets in the project.
		'''
		...

	@overload
	def DeleteStructure(self, id: int) -> bool:
		'''
		Returns true if the structure was deleted from the collection. Returns false if the structure could not be found or if there are run sets in the project.
		'''
		...

	@overload
	def Get(self, name: str) -> Structure:
		...

	@overload
	def Get(self, id: int) -> Structure:
		...

	def DeleteStructure(self, item1 = None) -> bool:
		'''
		Overload 1: ``DeleteStructure(self, structure: Structure) -> bool``

		Returns true if the structure was deleted from the collection. Returns false if the structure could not be found or if there are run sets in the project.

		Overload 2: ``DeleteStructure(self, name: str) -> bool``

		Returns true if the structure was deleted from the collection. Returns false if the structure could not be found or if there are run sets in the project.

		Overload 3: ``DeleteStructure(self, id: int) -> bool``

		Returns true if the structure was deleted from the collection. Returns false if the structure could not be found or if there are run sets in the project.
		'''
		if isinstance(item1, Structure):
			return self._Entity.DeleteStructure(item1._Entity)

		if isinstance(item1, str):
			return self._Entity.DeleteStructure(item1)

		if isinstance(item1, int):
			return self._Entity.DeleteStructure(item1)

		return self._Entity.DeleteStructure(item1._Entity)

	def Get(self, item1 = None) -> Structure:
		'''
		Overload 1: ``Get(self, name: str) -> Structure``

		Overload 2: ``Get(self, id: int) -> Structure``
		'''
		if isinstance(item1, str):
			return Structure(super().Get(item1))

		if isinstance(item1, int):
			return Structure(super().Get(item1))

		return Structure(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.StructureColList[index]

	def __iter__(self):
		yield from self.StructureColList

	def __len__(self):
		return len(self.StructureColList)


class Project:
	'''
	Represents a HyperX project within a database.
	'''

	_HyperFea = HyperFea

	_FemDataSet = FemDataSet
	def __init__(self, project: _api.Project):
		self._Entity = project
	@property
	def HyperFea(self) -> _HyperFea:
		result = self._Entity.HyperFea
		return HyperFea(result) if result is not None else None

	@property
	def WorkingFolder(self) -> str:
		return self._Entity.WorkingFolder
	@property
	def FemDataSet(self) -> _FemDataSet:
		result = self._Entity.FemDataSet
		return FemDataSet(result) if result is not None else None

	@property
	def Beams(self) -> ZoneCol:
		result = self._Entity.Beams
		return ZoneCol(result) if result is not None else None

	@property
	def Id(self) -> int:
		return self._Entity.Id

	@property
	def Joints(self) -> JointCol:
		result = self._Entity.Joints
		return JointCol(result) if result is not None else None

	@property
	def Name(self) -> str:
		return self._Entity.Name

	@property
	def Panels(self) -> ZoneCol:
		result = self._Entity.Panels
		return ZoneCol(result) if result is not None else None

	@property
	def Rundecks(self) -> RundeckCol:
		result = self._Entity.Rundecks
		return RundeckCol(result) if result is not None else None

	@property
	def Sets(self) -> SetCol:
		result = self._Entity.Sets
		return SetCol(result) if result is not None else None

	@property
	def Structures(self) -> StructureCol:
		result = self._Entity.Structures
		return StructureCol(result) if result is not None else None

	@property
	def Zones(self) -> ZoneCol:
		result = self._Entity.Zones
		return ZoneCol(result) if result is not None else None

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		result = self._Entity.PanelSegments
		return PanelSegmentCol(result) if result is not None else None

	@property
	def SectionCuts(self) -> SectionCutCol:
		result = self._Entity.SectionCuts
		return SectionCutCol(result) if result is not None else None

	@property
	def DesignLoads(self) -> DesignLoadCol:
		result = self._Entity.DesignLoads
		return DesignLoadCol(result) if result is not None else None

	@property
	def DiscreteFieldTables(self) -> DiscreteFieldCol:
		result = self._Entity.DiscreteFieldTables
		return DiscreteFieldCol(result) if result is not None else None

	@property
	def AnalysisProperties(self) -> AnalysisPropertyCol:
		'''
		Analysis Properties for this project.
		'''
		result = self._Entity.AnalysisProperties
		return AnalysisPropertyCol(result) if result is not None else None

	@property
	def DesignProperties(self) -> DesignPropertyCol:
		'''
		Design properties for this project.
		'''
		result = self._Entity.DesignProperties
		return DesignPropertyCol(result) if result is not None else None

	@property
	def LoadProperties(self) -> LoadPropertyCol:
		'''
		Load Properties for this project.
		'''
		result = self._Entity.LoadProperties
		return LoadPropertyCol(result) if result is not None else None

	@property
	def FemFormat(self) -> types.ProjectModelFormat:
		result = self._Entity.FemFormat
		return types.ProjectModelFormat[result.ToString()] if result is not None else None

	def Upload(self, uploadSetName: str, company: str, program: str, tags: tuple[str], notes: str, zoneIds: set[int], jointIds: set[int]) -> types.SimpleStatus:
		'''
		Does some checks to make sure the given parameters are valid, then uploads the given zones and joints to the Dashboard.
		The URL and authentication token are taken from the last Dashboard login made through HyperX.
		
		:param uploadSetName: The name of the set of data uploaded to the Dashboard.
		:param company: The name of the company to associate with the upload set. This company object must be made through the Dashboard UI.
		:param program: The name of the program to associated with the upload set. A new program will be created if the program name does not already exist.
		:param tags: The list of tags to be associated with the upload set. Any tags that do not exist will be created automatically on upload.
		:param notes: The notes to be associated with the upload set.
		:param zoneIds: The zone IDs to include in the upload set.
		:param jointIds: The joint IDs to include in the upload set.
		
		:return: Returns a successful SimpleStatus if the upload succeeded. Returns an unsuccessful SimpleStatus with error info otherwise.
		'''
		tagsList = List[str]()
		if tags is not None:
			for x in tags:
				if x is not None:
					tagsList.Add(x)
		tagsEnumerable = IEnumerable(tagsList)
		zoneIdsSet = HashSet[int]()
		if zoneIds is not None:
			for x in zoneIds:
				if x is not None:
					zoneIdsSet.Add(x)
		jointIdsSet = HashSet[int]()
		if jointIds is not None:
			for x in jointIds:
				if x is not None:
					jointIdsSet.Add(x)
		return types.SimpleStatus(self._Entity.Upload(uploadSetName, company, program, tagsEnumerable, notes, zoneIdsSet, jointIdsSet))

	def GetDashboardCompanies(self) -> list[str]:
		'''
		This method fetches an array of Dashboard company names that are available to the user who is currently logged in. The URL and authentication token are taken from the last
		Dashboard login made through HyperX.
		
		:return: Returns an array of company names. If certain web related errors are encountered, an empty array will be returned.
		'''
		return list[str](self._Entity.GetDashboardCompanies())

	def GetDashboardPrograms(self, companyName: str) -> list[str]:
		'''
		This method fetches an array of Dashboard program names that are available to the user who is currently logged in. The URL and authentication token are taken from the last
		Dashboard login made through HyperX.
		
		:return: Returns an array of program names. If certain web related errors are encountered, an empty array will be returned. If the provided company cannot be found, a ``None``
		value will be returned.
		'''
		return list[str](self._Entity.GetDashboardPrograms(companyName))

	def GetDashboardTags(self, companyName: str) -> list[str]:
		'''
		This method fetches an array of Dashboard tags that are available to the user who is currently logged in. The URL and authentication token are taken from the last
		Dashboard login made through HyperX.
		
		:return: Returns an array of tag names. If certain web related errors are encountered, an empty array will be returned. If the provided company could not be found, a 
		``None`` value will be returned.
		'''
		return list[str](self._Entity.GetDashboardTags(companyName))

	def GenerateSolverSizingInputFile(self, inputFile: str = None, zones: set[int] = None, joints: set[int] = None, sectionCuts: set[int] = None, panelSegments: set[int] = None) -> str:
		'''
		Generate sizing input file for solver with the specified items targeted.
		Returns filepath.
		'''
		zonesSet = HashSet[int]()
		if zones is not None:
			for x in zones:
				if x is not None:
					zonesSet.Add(x)
		jointsSet = HashSet[int]()
		if joints is not None:
			for x in joints:
				if x is not None:
					jointsSet.Add(x)
		sectionCutsSet = HashSet[int]()
		if sectionCuts is not None:
			for x in sectionCuts:
				if x is not None:
					sectionCutsSet.Add(x)
		panelSegmentsSet = HashSet[int]()
		if panelSegments is not None:
			for x in panelSegments:
				if x is not None:
					panelSegmentsSet.Add(x)
		return self._Entity.GenerateSolverSizingInputFile(inputFile, zones if zones is None else zonesSet, joints if joints is None else jointsSet, sectionCuts if sectionCuts is None else sectionCutsSet, panelSegments if panelSegments is None else panelSegmentsSet)

	def GenerateSolverAnalysisInputFile(self, inputFile: str = None, zones: set[int] = None, joints: set[int] = None, sectionCuts: set[int] = None, panelSegments: set[int] = None) -> str:
		'''
		Generate analysis input file for solver with the specified items targeted.
		Returns filepath.
		'''
		zonesSet = HashSet[int]()
		if zones is not None:
			for x in zones:
				if x is not None:
					zonesSet.Add(x)
		jointsSet = HashSet[int]()
		if joints is not None:
			for x in joints:
				if x is not None:
					jointsSet.Add(x)
		sectionCutsSet = HashSet[int]()
		if sectionCuts is not None:
			for x in sectionCuts:
				if x is not None:
					sectionCutsSet.Add(x)
		panelSegmentsSet = HashSet[int]()
		if panelSegments is not None:
			for x in panelSegments:
				if x is not None:
					panelSegmentsSet.Add(x)
		return self._Entity.GenerateSolverAnalysisInputFile(inputFile, zones if zones is None else zonesSet, joints if joints is None else jointsSet, sectionCuts if sectionCuts is None else sectionCutsSet, panelSegments if panelSegments is None else panelSegmentsSet)

	def FullRunSolverSizing(self, inputFile: str = None, outputFile: str = None, zones: set[int] = None, joints: set[int] = None, sectionCuts: set[int] = None, panelSegments: set[int] = None, nThreads: int = None) -> types.SimpleStatus:
		'''
		Run solver in sizing mode with the specified items targeted.
		Generates input file, runs solver, reads output.
		Returns true on success.
		'''
		zonesSet = HashSet[int]()
		if zones is not None:
			for x in zones:
				if x is not None:
					zonesSet.Add(x)
		jointsSet = HashSet[int]()
		if joints is not None:
			for x in joints:
				if x is not None:
					jointsSet.Add(x)
		sectionCutsSet = HashSet[int]()
		if sectionCuts is not None:
			for x in sectionCuts:
				if x is not None:
					sectionCutsSet.Add(x)
		panelSegmentsSet = HashSet[int]()
		if panelSegments is not None:
			for x in panelSegments:
				if x is not None:
					panelSegmentsSet.Add(x)
		return types.SimpleStatus(self._Entity.FullRunSolverSizing(inputFile, outputFile, zones if zones is None else zonesSet, joints if joints is None else jointsSet, sectionCuts if sectionCuts is None else sectionCutsSet, panelSegments if panelSegments is None else panelSegmentsSet, nThreads))

	def FullRunSolverAnalysis(self, inputFile: str = None, outputFile: str = None, zones: set[int] = None, joints: set[int] = None, sectionCuts: set[int] = None, panelSegments: set[int] = None, nThreads: int = None) -> types.SimpleStatus:
		'''
		Run solver in analysis mode with the specified items targeted. 
		Generates input file, runs solver, reads output.
		Returns true on success.
		'''
		zonesSet = HashSet[int]()
		if zones is not None:
			for x in zones:
				if x is not None:
					zonesSet.Add(x)
		jointsSet = HashSet[int]()
		if joints is not None:
			for x in joints:
				if x is not None:
					jointsSet.Add(x)
		sectionCutsSet = HashSet[int]()
		if sectionCuts is not None:
			for x in sectionCuts:
				if x is not None:
					sectionCutsSet.Add(x)
		panelSegmentsSet = HashSet[int]()
		if panelSegments is not None:
			for x in panelSegments:
				if x is not None:
					panelSegmentsSet.Add(x)
		return types.SimpleStatus(self._Entity.FullRunSolverAnalysis(inputFile, outputFile, zones if zones is None else zonesSet, joints if joints is None else jointsSet, sectionCuts if sectionCuts is None else sectionCutsSet, panelSegments if panelSegments is None else panelSegmentsSet, nThreads))

	def RunSolver(self, inputFile: str, outputFile: str = None, nThreads: int = None) -> types.SimpleStatus:
		'''
		Run solver with pre-generated input file.
		Returns true on success.
		'''
		return types.SimpleStatus(self._Entity.RunSolver(inputFile, outputFile, nThreads))

	def ReadSolverResultFile(self, isSizing: bool, outputFile: str) -> types.SimpleStatus:
		'''
		Read results from output file, given approach, design properties lookup, and global design variable lookup
		'''
		return types.SimpleStatus(self._Entity.ReadSolverResultFile(isSizing, outputFile))

	def GeneratePeakLoadFiles(self, zones: set[int]) -> None:
		zonesSet = HashSet[int]()
		if zones is not None:
			for x in zones:
				if x is not None:
					zonesSet.Add(x)
		return self._Entity.GeneratePeakLoadFiles(zonesSet)

	def Dispose(self) -> None:
		return self._Entity.Dispose()

	def PackageProject(self, destinationFilePath: str, includeFemInputFiles: bool = True, includeFemOutputFiles: bool = True, includeWorkingFolder: bool = True, includeLoadFiles: bool = True, includePluginPackages: bool = False, removeAllOtherProjects: bool = False, deleteUnusedPropertiesAndMaterials: bool = False, mapFemFilesToRelativePaths: bool = True, additionalFiles: tuple[str] = None) -> types.SimpleStatus:
		'''
		Create a .hxp project package from the ActiveProject.
		'''
		additionalFilesList = List[str]()
		if additionalFiles is not None:
			for x in additionalFiles:
				if x is not None:
					additionalFilesList.Add(x)
		additionalFilesEnumerable = IEnumerable(additionalFilesList)
		return types.SimpleStatus(self._Entity.PackageProject(destinationFilePath, includeFemInputFiles, includeFemOutputFiles, includeWorkingFolder, includeLoadFiles, includePluginPackages, removeAllOtherProjects, deleteUnusedPropertiesAndMaterials, mapFemFilesToRelativePaths, additionalFiles if additionalFiles is None else additionalFilesEnumerable))

	def ImportFeaResults(self, alwaysImport: bool = False) -> str:
		'''
		Manually import design loads.
		
		:param alwaysImport: If true, loads are imported even if loads have already previously been imported.
		
		:return: Any warnings during import. String with length 0 if no warnings.
		
		:raises ``System.InvalidOperationException``: Throws on failure.
		'''
		return self._Entity.ImportFeaResults(alwaysImport)

	def SetFemFormat(self, femFormat: types.ProjectModelFormat) -> None:
		return self._Entity.SetFemFormat(_types.ProjectModelFormat(types.GetEnumValue(femFormat.value)))

	def SetFemUnits(self, femForceId: DbForceUnit, femLengthId: DbLengthUnit, femMassId: DbMassUnit, femTemperatureId: DbTemperatureUnit) -> SetUnitsStatus:
		return SetUnitsStatus[self._Entity.SetFemUnits(_api.DbForceUnit(types.GetEnumValue(femForceId.value)), _api.DbLengthUnit(types.GetEnumValue(femLengthId.value)), _api.DbMassUnit(types.GetEnumValue(femMassId.value)), _api.DbTemperatureUnit(types.GetEnumValue(femTemperatureId.value))).ToString()]

	def SizeJoints(self, joints: tuple[Joint] = None) -> types.SimpleStatus:
		'''
		Size a list of joints.
		'''
		jointsList = List[_api.Joint]()
		if joints is not None:
			for x in joints:
				if x is not None:
					jointsList.Add(x._Entity)
		jointsEnumerable = IEnumerable(jointsList)
		return types.SimpleStatus(self._Entity.SizeJoints(joints if joints is None else jointsEnumerable))

	def GetJointsWithoutResults(self, joints: tuple[Joint]) -> set[int]:
		'''
		Given a list of joints, returns the ids of the joints that were passed in but did not have results.
		If the list of joints is not a subset of the joints passed into the previous joint sizing operation, a new sizing operation will be kicked off.
		'''
		jointsList = List[_api.Joint]()
		if joints is not None:
			for x in joints:
				if x is not None:
					jointsList.Add(x._Entity)
		jointsEnumerable = IEnumerable(jointsList)
		return set[int](self._Entity.GetJointsWithoutResults(jointsEnumerable))

	@overload
	def AnalyzeZones(self, zones: tuple[ZoneBase] = None) -> types.TernaryStatus:
		'''
		Analyze a list of zones.
		Marked as success if sizing completes normally or with warnings.
		'''
		...

	@overload
	def AnalyzeZones(self, zoneIds: tuple[int]) -> types.TernaryStatus:
		'''
		Analyze a list of zones by ID.
		Marked as success if sizing completes normally or with warnings.
		'''
		...

	@overload
	def SizeZones(self, zones: tuple[ZoneBase] = None) -> types.TernaryStatus:
		'''
		Size a list of zones.
		Marked as success if sizing completes normally or with warnings.
		
		:param zones: The zones to be sized.
		'''
		...

	@overload
	def SizeZones(self, zoneIds: tuple[int]) -> types.TernaryStatus:
		'''
		Size a list of zones by ID.
		Marked as success if sizing completes normally or with warnings.
		'''
		...

	def CreateNonFeaZone(self, category: types.FamilyCategory, name: str = None) -> Zone:
		'''
		Create a non-FEA zone by name and category.
		'''
		result = self._Entity.CreateNonFeaZone(_types.FamilyCategory(types.GetEnumValue(category.value)), name)
		thisClass = type(result).__name__
		givenClass = Zone
		for subclass in _all_subclasses(Zone):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def ReturnToUnusedFem(self, zoneNumbers: tuple[int] = None, jointIds: tuple[int] = None) -> None:
		'''
		Return zones to unused FEM or delete non-FEA zones.
		
		:raises ``System.InvalidOperationException``: Throws if run sets exist in this project.
		'''
		zoneNumbersList = MakeCSharpIntList(zoneNumbers)
		zoneNumbersEnumerable = IEnumerable(zoneNumbersList)
		jointIdsList = MakeCSharpIntList(jointIds)
		jointIdsEnumerable = IEnumerable(jointIdsList)
		return self._Entity.ReturnToUnusedFem(zoneNumbers if zoneNumbers is None else zoneNumbersEnumerable, jointIds if jointIds is None else jointIdsEnumerable)

	def UnimportFemAsync(self) -> Task:
		return Task(self._Entity.UnimportFemAsync())

	def ExportFem(self, destinationFolder: str) -> None:
		return self._Entity.ExportFem(destinationFolder)

	def ImportCad(self, filePath: str) -> None:
		'''
		Import CAD from a file.
		'''
		return self._Entity.ImportCad(filePath)

	@overload
	def ExportCad(self, filePath: str) -> None:
		'''
		Export all CAD for this project to a file.
		'''
		...

	@overload
	def ExportCad(self, cadIds: tuple[int], filePath: str) -> None:
		'''
		Export CAD by Id.
		'''
		...

	def RegeneratePfem(self) -> None:
		'''
		Regenerates and displays the preview FEM. If running a script outside of the Script Runner,
		do not call this method
		'''
		return self._Entity.RegeneratePfem()

	@overload
	def CopyResultsToOverrides(self, forceDeletePlies: bool, zones: tuple[ZoneBase]) -> types.SimpleStatus:
		...

	@overload
	def CopyResultsToOverrides(self, forceDeletePlies: bool, zoneIds: tuple[int]) -> types.SimpleStatus:
		...

	def CreateHyperXpertPoints(self, runsets: set[int], plotMode: types.DoePlotMode, pointType: types.DoePointType, generateVariabilityForLinked: bool, filterNonGeometry: bool) -> list[HyperXpertPoint]:
		'''
		Create HyperXpert points based on specific run sets.
		'''
		runsetsSet = HashSet[int]()
		if runsets is not None:
			for x in runsets:
				if x is not None:
					runsetsSet.Add(x)
		return [HyperXpertPoint(hyperXpertPoint) for hyperXpertPoint in self._Entity.CreateHyperXpertPoints(runsetsSet, _types.DoePlotMode(types.GetEnumValue(plotMode.value)), _types.DoePointType(types.GetEnumValue(pointType.value)), generateVariabilityForLinked, filterNonGeometry)]

	def GetRunSets(self) -> list[RunSet]:
		return [RunSet(runSet) for runSet in self._Entity.GetRunSets()]

	def AnalyzeZones(self, item1 = None) -> types.TernaryStatus:
		'''
		Overload 1: ``AnalyzeZones(self, zones: tuple[ZoneBase] = None) -> types.TernaryStatus``

		Analyze a list of zones.
		Marked as success if sizing completes normally or with warnings.

		Overload 2: ``AnalyzeZones(self, zoneIds: tuple[int]) -> types.TernaryStatus``

		Analyze a list of zones by ID.
		Marked as success if sizing completes normally or with warnings.
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, ZoneBase) for x in item1):
			zonesList = List[_api.ZoneBase]()
			if item1 is not None:
				for x in item1:
					if x is not None:
						zonesList.Add(x._Entity)
			zonesEnumerable = IEnumerable(zonesList)
			return types.TernaryStatus(self._Entity.AnalyzeZones(item1 if item1 is None else zonesEnumerable))

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return types.TernaryStatus(self._Entity.AnalyzeZones(zoneIdsEnumerable))

		return types.TernaryStatus(self._Entity.AnalyzeZones(item1))

	def SizeZones(self, item1 = None) -> types.TernaryStatus:
		'''
		Overload 1: ``SizeZones(self, zones: tuple[ZoneBase] = None) -> types.TernaryStatus``

		Size a list of zones.
		Marked as success if sizing completes normally or with warnings.
		
		:param zones: The zones to be sized.

		Overload 2: ``SizeZones(self, zoneIds: tuple[int]) -> types.TernaryStatus``

		Size a list of zones by ID.
		Marked as success if sizing completes normally or with warnings.
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, ZoneBase) for x in item1):
			zonesList = List[_api.ZoneBase]()
			if item1 is not None:
				for x in item1:
					if x is not None:
						zonesList.Add(x._Entity)
			zonesEnumerable = IEnumerable(zonesList)
			return types.TernaryStatus(self._Entity.SizeZones(item1 if item1 is None else zonesEnumerable))

		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return types.TernaryStatus(self._Entity.SizeZones(zoneIdsEnumerable))

		return types.TernaryStatus(self._Entity.SizeZones(item1))

	def ExportCad(self, item1 = None, item2 = None) -> None:
		'''
		Overload 1: ``ExportCad(self, filePath: str) -> None``

		Export all CAD for this project to a file.

		Overload 2: ``ExportCad(self, cadIds: tuple[int], filePath: str) -> None``

		Export CAD by Id.
		'''
		if (isinstance(item1, tuple) or isinstance(item1, list) or isinstance(item1, set)) and item1 and any(isinstance(x, int) for x in item1) and isinstance(item2, str):
			cadIdsList = MakeCSharpIntList(item1)
			cadIdsEnumerable = IEnumerable(cadIdsList)
			return self._Entity.ExportCad(cadIdsEnumerable, item2)

		if isinstance(item1, str):
			return self._Entity.ExportCad(item1)

		return self._Entity.ExportCad(item1, item2)

	def CopyResultsToOverrides(self, item1 = None, item2 = None) -> types.SimpleStatus:
		'''
		Overload 1: ``CopyResultsToOverrides(self, forceDeletePlies: bool, zones: tuple[ZoneBase]) -> types.SimpleStatus``

		Overload 2: ``CopyResultsToOverrides(self, forceDeletePlies: bool, zoneIds: tuple[int]) -> types.SimpleStatus``
		'''
		if isinstance(item1, bool) and (isinstance(item2, tuple) or isinstance(item2, list) or isinstance(item2, set)) and item2 and any(isinstance(x, ZoneBase) for x in item2):
			zonesList = List[_api.ZoneBase]()
			if item2 is not None:
				for x in item2:
					if x is not None:
						zonesList.Add(x._Entity)
			zonesEnumerable = IEnumerable(zonesList)
			return types.SimpleStatus(self._Entity.CopyResultsToOverrides(item1, zonesEnumerable))

		if isinstance(item1, bool) and (isinstance(item2, tuple) or isinstance(item2, list) or isinstance(item2, set)) and item2 and any(isinstance(x, int) for x in item2):
			zoneIdsList = MakeCSharpIntList(item2)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return types.SimpleStatus(self._Entity.CopyResultsToOverrides(item1, zoneIdsEnumerable))

		return types.SimpleStatus(self._Entity.CopyResultsToOverrides(item1, item2))


class ProjectInfo(IdNameEntityRenameable):
	def __init__(self, projectInfo: _api.ProjectInfo):
		self._Entity = projectInfo


class FailureModeCategoryCol(IdNameEntityCol[FailureModeCategory]):
	def __init__(self, failureModeCategoryCol: _api.FailureModeCategoryCol):
		self._Entity = failureModeCategoryCol
		self._CollectedClass = FailureModeCategory

	@property
	def FailureModeCategoryColList(self) -> tuple[FailureModeCategory]:
		return tuple([FailureModeCategory(failureModeCategoryCol) for failureModeCategoryCol in self._Entity])

	@overload
	def Get(self, name: str) -> FailureModeCategory:
		...

	@overload
	def Get(self, id: int) -> FailureModeCategory:
		...

	def Get(self, item1 = None) -> FailureModeCategory:
		'''
		Overload 1: ``Get(self, name: str) -> FailureModeCategory``

		Overload 2: ``Get(self, id: int) -> FailureModeCategory``
		'''
		if isinstance(item1, str):
			return FailureModeCategory(super().Get(item1))

		if isinstance(item1, int):
			return FailureModeCategory(super().Get(item1))

		return FailureModeCategory(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.FailureModeCategoryColList[index]

	def __iter__(self):
		yield from self.FailureModeCategoryColList

	def __len__(self):
		return len(self.FailureModeCategoryColList)


class FoamCol(Generic[T]):
	def __init__(self, foamCol: _api.FoamCol):
		self._Entity = foamCol

	@property
	def FoamColList(self) -> tuple[Foam]:
		return tuple([Foam(foamCol) for foamCol in self._Entity])

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, materialName: str) -> Foam:
		'''
		Look up an Foam material by its name.
		'''
		return Foam(self._Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		'''
		Check if an foam material exists in this collection.
		'''
		return self._Entity.Contains(materialName)

	def Create(self, materialFamilyName: str, density: float, newMaterialName: str = None, femId: int = None) -> Foam:
		'''
		Create a Foam material.
		
		:param femId: Defaults to 0 when there is no linked FEM.
		
		:return: The created Foam.
		
		:raises ``System.ArgumentException``: Throws on duplicate femId.
		'''
		return Foam(self._Entity.Create(materialFamilyName, density, newMaterialName, femId))

	def Copy(self, fmToCopyName: str, newMaterialName: str = None, femId: int = None) -> Foam:
		'''
		Copy a Foam material.
		
		:param femId: Defaults to 0 when there is no linked FEM.
		
		:return: The new copied Foam.
		
		:raises ``System.ArgumentException``: Throws on nonexistent Foam material to copy or duplicate femId.
		'''
		return Foam(self._Entity.Copy(fmToCopyName, newMaterialName, femId))

	def Delete(self, materialName: str) -> bool:
		'''
		Delete a foam material by name.
		Returns false if the method the material is not found.
		'''
		return self._Entity.Delete(materialName)

	def __getitem__(self, index: int):
		return self.FoamColList[index]

	def __iter__(self):
		yield from self.FoamColList

	def __len__(self):
		return len(self.FoamColList)


class HoneycombCol(Generic[T]):
	def __init__(self, honeycombCol: _api.HoneycombCol):
		self._Entity = honeycombCol

	@property
	def HoneycombColList(self) -> tuple[Honeycomb]:
		return tuple([Honeycomb(honeycombCol) for honeycombCol in self._Entity])

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, materialName: str) -> Honeycomb:
		'''
		Look up an Honeycomb material by its name.
		'''
		return Honeycomb(self._Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		'''
		Check if an honeycomb material exists in this collection.
		'''
		return self._Entity.Contains(materialName)

	def Create(self, materialFamilyName: str, density: float, newMaterialName: str = None, femId: int = None) -> Honeycomb:
		'''
		Create a Honeycomb material.
		
		:param femId: Defaults to 0 when there is no linked FEM.
		
		:return: The created Honeycomb.
		
		:raises ``System.ArgumentException``: Throws on duplicate femId.
		'''
		return Honeycomb(self._Entity.Create(materialFamilyName, density, newMaterialName, femId))

	def Copy(self, honeyToCopyName: str, newMaterialName: str = None, femId: int = None) -> Honeycomb:
		'''
		Copy a Honeycomb.
		
		:param femId: Defaults to 0 when there is no linked FEM.
		
		:return: The new copied Honeycomb.
		
		:raises ``System.ArgumentException``: Throws on nonexistent Honeycomb material to copy or duplicate femId.
		'''
		return Honeycomb(self._Entity.Copy(honeyToCopyName, newMaterialName, femId))

	def Delete(self, materialName: str) -> bool:
		'''
		Delete a honeycomb material by name.
		Returns false if the method the material is not found.
		'''
		return self._Entity.Delete(materialName)

	def __getitem__(self, index: int):
		return self.HoneycombColList[index]

	def __iter__(self):
		yield from self.HoneycombColList

	def __len__(self):
		return len(self.HoneycombColList)


class IsotropicCol(Generic[T]):
	def __init__(self, isotropicCol: _api.IsotropicCol):
		self._Entity = isotropicCol

	@property
	def IsotropicColList(self) -> tuple[Isotropic]:
		return tuple([Isotropic(isotropicCol) for isotropicCol in self._Entity])

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, materialName: str) -> Isotropic:
		'''
		Look up an Isotropic material by its name.
		'''
		return Isotropic(self._Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		'''
		Check if an isotropic material exists in this collection.
		'''
		return self._Entity.Contains(materialName)

	def Create(self, materialFamilyName: str, density: float, newMaterialName: str = None, femId: int = None) -> Isotropic:
		'''
		Create an Isotropic material.
		
		:param femId: Defaults to 0 when there is no linked FEM.
		
		:return: The created Isotropic.
		
		:raises ``System.ArgumentException``: Throws on duplicate femId.
		'''
		return Isotropic(self._Entity.Create(materialFamilyName, density, newMaterialName, femId))

	def Copy(self, isoToCopyName: str, newMaterialName: str = None, femId: int = None) -> Isotropic:
		'''
		Copy an Isotropic material.
		
		:param femId: Defaults to 0 when there is no linked FEM.
		
		:return: The new copied Isotropic.
		
		:raises ``System.ArgumentException``: Throws on nonexistent Isotropic material to copy or duplicate femId.
		'''
		return Isotropic(self._Entity.Copy(isoToCopyName, newMaterialName, femId))

	def Delete(self, materialName: str) -> bool:
		'''
		Delete an isotropic material by name.
		Returns false if the method the material is not found.
		'''
		return self._Entity.Delete(materialName)

	def __getitem__(self, index: int):
		return self.IsotropicColList[index]

	def __iter__(self):
		yield from self.IsotropicColList

	def __len__(self):
		return len(self.IsotropicColList)


class LaminateFamilyCol(IdNameEntityCol[LaminateFamily]):
	def __init__(self, laminateFamilyCol: _api.LaminateFamilyCol):
		self._Entity = laminateFamilyCol
		self._CollectedClass = LaminateFamily

	@property
	def LaminateFamilyColList(self) -> tuple[LaminateFamily]:
		return tuple([LaminateFamily(laminateFamilyCol) for laminateFamilyCol in self._Entity])

	@overload
	def Get(self, name: str) -> LaminateFamily:
		...

	@overload
	def Get(self, id: int) -> LaminateFamily:
		...

	def Get(self, item1 = None) -> LaminateFamily:
		'''
		Overload 1: ``Get(self, name: str) -> LaminateFamily``

		Overload 2: ``Get(self, id: int) -> LaminateFamily``
		'''
		if isinstance(item1, str):
			return LaminateFamily(super().Get(item1))

		if isinstance(item1, int):
			return LaminateFamily(super().Get(item1))

		return LaminateFamily(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.LaminateFamilyColList[index]

	def __iter__(self):
		yield from self.LaminateFamilyColList

	def __len__(self):
		return len(self.LaminateFamilyColList)


class LaminateCol(Generic[T]):
	def __init__(self, laminateCol: _api.LaminateCol):
		self._Entity = laminateCol

	@property
	def LaminateColList(self) -> tuple[Laminate]:
		return tuple([Laminate(laminateCol) for laminateCol in self._Entity])

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, laminateName: str) -> LaminateBase:
		'''
		Look up a Laminate by its name.
		
		:raises ``System.ArgumentException``:
		'''
		result = self._Entity.Get(laminateName)
		thisClass = type(result).__name__
		givenClass = LaminateBase
		for subclass in _all_subclasses(LaminateBase):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def Contains(self, laminateName: str) -> bool:
		return self._Entity.Contains(laminateName)

	def CreateLaminate(self, materialFamily: str, laminateName: str = None) -> Laminate:
		'''
		Create laminate.
		
		:return: The created laminate.
		'''
		return Laminate(self._Entity.CreateLaminate(materialFamily, laminateName))

	def CreateStiffenerLaminate(self, materialFamily: str, stiffenerProfile: types.StiffenerProfile, laminateName: str = None) -> StiffenerLaminate:
		'''
		Create a stiffener laminate.
		
		:return: The created stiffener laminate.
		'''
		return StiffenerLaminate(self._Entity.CreateStiffenerLaminate(materialFamily, _types.StiffenerProfile(types.GetEnumValue(stiffenerProfile.value)), laminateName))

	def Copy(self, laminateToCopyName: str, newLaminateName: str = None) -> LaminateBase:
		'''
		Copy a laminate material by name.
		
		:return: The copied laminate.
		
		:raises ``System.ArgumentException``: Throws if the laminate to copy doesn't exist.
		'''
		result = self._Entity.Copy(laminateToCopyName, newLaminateName)
		thisClass = type(result).__name__
		givenClass = LaminateBase
		for subclass in _all_subclasses(LaminateBase):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def Delete(self, name: str) -> bool:
		'''
		Delete a laminate material by name.
		Returns false if the material is not found or removed.
		'''
		return self._Entity.Delete(name)

	def GetLaminate(self, name: str) -> Laminate:
		'''
		Get a laminate by name.
		
		:return: The laminate.
		
		:raises ``System.ArgumentException``:
		'''
		return Laminate(self._Entity.GetLaminate(name))

	def GetStiffenerLaminate(self, name: str) -> StiffenerLaminate:
		'''
		Get a stiffener laminate by name.
		
		:return: The stiffener laminate.
		
		:raises ``System.ArgumentException``:
		'''
		return StiffenerLaminate(self._Entity.GetStiffenerLaminate(name))

	def __getitem__(self, index: int):
		return self.LaminateColList[index]

	def __iter__(self):
		yield from self.LaminateColList

	def __len__(self):
		return len(self.LaminateColList)


class OrthotropicCol(Generic[T]):
	def __init__(self, orthotropicCol: _api.OrthotropicCol):
		self._Entity = orthotropicCol

	@property
	def OrthotropicColList(self) -> tuple[Orthotropic]:
		return tuple([Orthotropic(orthotropicCol) for orthotropicCol in self._Entity])

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, materialName: str) -> Orthotropic:
		'''
		Look up an Orthotropic material by its name.
		'''
		return Orthotropic(self._Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		'''
		Check if an orthotropic material exists in this collection.
		'''
		return self._Entity.Contains(materialName)

	def Create(self, materialFamilyName: str, thickness: float, density: float, newMaterialName: str = None, femId: int = None) -> Orthotropic:
		'''
		Create an Orthotropic material.
		
		:param femId: Defaults to 0 when there is no linked FEM.
		
		:return: The created Orthotropic.
		
		:raises ``System.ArgumentException``: Throws on duplicate femId.
		'''
		return Orthotropic(self._Entity.Create(materialFamilyName, thickness, density, newMaterialName, femId))

	def Copy(self, orthoToCopyName: str, newMaterialName: str = None, femId: int = None) -> Orthotropic:
		'''
		Copy an Orthotropic material.
		
		:param femId: Defaults to 0 when there is no linked FEM.
		
		:return: The new copied Orthotropic.
		
		:raises ``System.ArgumentException``: Throws on nonexistent Orthotropic material to copy or duplicate femId.
		'''
		return Orthotropic(self._Entity.Copy(orthoToCopyName, newMaterialName, femId))

	def Delete(self, materialName: str) -> bool:
		'''
		Delete an orthotropic material by name.
		Returns false if the method the material is not found.
		'''
		return self._Entity.Delete(materialName)

	def GenerateEffectiveLaminates(self, tapeMaterialId: int | None, fabricMaterialId: int | None, namePrefix: str, minTape0: int = 10, maxTape0: int = 50, stepTape0: int = 10, minTape45: int = 20, maxTape45: int = 60, stepTape45: int = 20, minTape90: int = 10, maxTape90: int = 50, stepTape90: int = 10, minFabric0: int = 10, maxFabric0: int = 50, stepFabric0: int = 10, minFabric45: int = 20, maxFabric45: int = 60, stepFabric45: int = 10, minFabric90: int = 10, maxFabric90: int = 50, stepFabric90: int = 10) -> list[Orthotropic]:
		'''
		Generate effective laminates with the specified ply angle constraints.
		
		:raises ``System.ArgumentException``:
		'''
		return [Orthotropic(orthotropic) for orthotropic in self._Entity.GenerateEffectiveLaminates(tapeMaterialId, fabricMaterialId, namePrefix, minTape0, maxTape0, stepTape0, minTape45, maxTape45, stepTape45, minTape90, maxTape90, stepTape90, minFabric0, maxFabric0, stepFabric0, minFabric45, maxFabric45, stepFabric45, minFabric90, maxFabric90, stepFabric90)]

	def CreateEffectiveLaminate(self, tapeMaterialId: int | None, fabricMaterialId: int | None, namePrefix: str, tape0: int, tape45: int, tape90: int, fabric0: int, fabric45: int, fabric90: int) -> Orthotropic:
		'''
		Create an effective laminate with the specified ply angle percentages.
		
		:raises ``System.ArgumentException``:
		'''
		return Orthotropic(self._Entity.CreateEffectiveLaminate(tapeMaterialId, fabricMaterialId, namePrefix, tape0, tape45, tape90, fabric0, fabric45, fabric90))

	def __getitem__(self, index: int):
		return self.OrthotropicColList[index]

	def __iter__(self):
		yield from self.OrthotropicColList

	def __len__(self):
		return len(self.OrthotropicColList)


class PluginPackageCol(IdNameEntityCol[PluginPackage]):
	def __init__(self, pluginPackageCol: _api.PluginPackageCol):
		self._Entity = pluginPackageCol
		self._CollectedClass = PluginPackage

	@property
	def PluginPackageColList(self) -> tuple[PluginPackage]:
		return tuple([PluginPackage(pluginPackageCol) for pluginPackageCol in self._Entity])

	def AddPluginPackage(self, path: str) -> PluginPackage:
		'''
		Add a plugin package by path.
		
		:return: The added PluginPackage.
		'''
		return PluginPackage(self._Entity.AddPluginPackage(path))

	@overload
	def RemovePluginPackage(self, name: str) -> bool:
		'''
		Remove a plugin package by name.
		
		:return: False if the package is not found.
		'''
		...

	@overload
	def RemovePluginPackage(self, id: int) -> bool:
		'''
		Remove a plugin package by id.
		
		:return: False if the package is not found.
		'''
		...

	def ClearAllPluginPackages(self) -> None:
		'''
		Clears all packages out of the database
		'''
		return self._Entity.ClearAllPluginPackages()

	def GetPluginPackages(self) -> list[PluginPackage]:
		'''
		Gets a list of package info
		Includes name, id, file path, version, description, and modification date
		
		:return: A list of all packages in the collection.
		'''
		return [PluginPackage(pluginPackage) for pluginPackage in self._Entity.GetPluginPackages()]

	@overload
	def Get(self, name: str) -> PluginPackage:
		...

	@overload
	def Get(self, id: int) -> PluginPackage:
		...

	def RemovePluginPackage(self, item1 = None) -> bool:
		'''
		Overload 1: ``RemovePluginPackage(self, name: str) -> bool``

		Remove a plugin package by name.
		
		:return: False if the package is not found.

		Overload 2: ``RemovePluginPackage(self, id: int) -> bool``

		Remove a plugin package by id.
		
		:return: False if the package is not found.
		'''
		if isinstance(item1, str):
			return self._Entity.RemovePluginPackage(item1)

		if isinstance(item1, int):
			return self._Entity.RemovePluginPackage(item1)

		return self._Entity.RemovePluginPackage(item1)

	def Get(self, item1 = None) -> PluginPackage:
		'''
		Overload 1: ``Get(self, name: str) -> PluginPackage``

		Overload 2: ``Get(self, id: int) -> PluginPackage``
		'''
		if isinstance(item1, str):
			return PluginPackage(super().Get(item1))

		if isinstance(item1, int):
			return PluginPackage(super().Get(item1))

		return PluginPackage(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.PluginPackageColList[index]

	def __iter__(self):
		yield from self.PluginPackageColList

	def __len__(self):
		return len(self.PluginPackageColList)


class ProjectInfoCol(IdNameEntityCol[ProjectInfo]):
	def __init__(self, projectInfoCol: _api.ProjectInfoCol):
		self._Entity = projectInfoCol
		self._CollectedClass = ProjectInfo

	@property
	def ProjectInfoColList(self) -> tuple[ProjectInfo]:
		return tuple([ProjectInfo(projectInfoCol) for projectInfoCol in self._Entity])

	@overload
	def Get(self, name: str) -> ProjectInfo:
		...

	@overload
	def Get(self, id: int) -> ProjectInfo:
		...

	def Get(self, item1 = None) -> ProjectInfo:
		'''
		Overload 1: ``Get(self, name: str) -> ProjectInfo``

		Overload 2: ``Get(self, id: int) -> ProjectInfo``
		'''
		if isinstance(item1, str):
			return ProjectInfo(super().Get(item1))

		if isinstance(item1, int):
			return ProjectInfo(super().Get(item1))

		return ProjectInfo(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.ProjectInfoColList[index]

	def __iter__(self):
		yield from self.ProjectInfoColList

	def __len__(self):
		return len(self.ProjectInfoColList)


class Application:
	'''
	HyperX scripting application.
	This API is not guaranteed to be thread-safe.
	Calls into a single application instance or its descendents are not safe to be called concurrently.
	
	However, it is safe enough for integration testing to have multiple
	application instances with a single process.
	'''

	_UnitSystem = UnitSystem
	def __init__(self, application: _api.Application):
		if isinstance(application, Application):
			self._Entity = application._Entity
		else:
			self._Entity = application
		ValidateDatabaseVersion(Application.Version())
	@property
	def UnitSystem(self) -> _UnitSystem:
		result = self._Entity.UnitSystem
		return UnitSystem[result.ToString()] if result is not None else None

	@classmethod
	def CompilationDate(self) -> str:
		'''
		Date that this version of the API was compiled.
		'''
		return _api.Application.CompilationDate

	@property
	def DatabasePath(self) -> str:
		return self._Entity.DatabasePath

	@property
	def ActiveProject(self) -> Project:
		'''
		The currently active project.
		Only one project is ever active at a time.
		'''
		result = self._Entity.ActiveProject
		return Project(result) if result is not None else None

	@property
	def UiRunnerMode(self) -> bool:
		'''
		True while the API is being used through the HyperX UI. Otherwise false.
		'''
		return self._Entity.UiRunnerMode

	@classmethod
	def Version(self) -> str:
		'''
		Get the current HyperX version number.
		'''
		return _api.Application.Version

	@property
	def FailureModeCategories(self) -> FailureModeCategoryCol:
		result = self._Entity.FailureModeCategories
		return FailureModeCategoryCol(result) if result is not None else None

	@property
	def FailureModes(self) -> FailureModeCol:
		result = self._Entity.FailureModes
		return FailureModeCol(result) if result is not None else None

	@property
	def Packages(self) -> PluginPackageCol:
		result = self._Entity.Packages
		return PluginPackageCol(result) if result is not None else None

	@property
	def Foams(self) -> FoamCol:
		'''
		Contains all foam materials.
		'''
		result = self._Entity.Foams
		return FoamCol(result) if result is not None else None

	@property
	def Honeycombs(self) -> HoneycombCol:
		'''
		Contains all honeycomb materials.
		'''
		result = self._Entity.Honeycombs
		return HoneycombCol(result) if result is not None else None

	@property
	def Isotropics(self) -> IsotropicCol:
		'''
		Contains all isotropic materials.
		'''
		result = self._Entity.Isotropics
		return IsotropicCol(result) if result is not None else None

	@property
	def Laminates(self) -> LaminateCol:
		'''
		Contains all laminate materials.
		'''
		result = self._Entity.Laminates
		return LaminateCol(result) if result is not None else None

	@property
	def LaminateFamilies(self) -> LaminateFamilyCol:
		'''
		Contains all laminate families.
		'''
		result = self._Entity.LaminateFamilies
		return LaminateFamilyCol(result) if result is not None else None

	@property
	def AnalysisProperties(self) -> AnalysisPropertyCol:
		'''
		Analysis Properties for this database.
		'''
		result = self._Entity.AnalysisProperties
		return AnalysisPropertyCol(result) if result is not None else None

	@property
	def DesignProperties(self) -> DesignPropertyCol:
		'''
		Design Properties for this database.
		'''
		result = self._Entity.DesignProperties
		return DesignPropertyCol(result) if result is not None else None

	@property
	def LoadProperties(self) -> LoadPropertyCol:
		'''
		Load Properties for this database.
		'''
		result = self._Entity.LoadProperties
		return LoadPropertyCol(result) if result is not None else None

	@property
	def Orthotropics(self) -> OrthotropicCol:
		'''
		Contains all orthotropic materials.
		'''
		result = self._Entity.Orthotropics
		return OrthotropicCol(result) if result is not None else None

	@property
	def ProjectInfos(self) -> ProjectInfoCol:
		'''
		Contains all projects.
		'''
		result = self._Entity.ProjectInfos
		return ProjectInfoCol(result) if result is not None else None

	@property
	def UserName(self) -> str:
		return self._Entity.UserName

	@UserName.setter
	def UserName(self, value: str) -> None:
		self._Entity.UserName = value

	def PauseUpdates(self) -> None:
		'''
		Pause the sending of updates as items are created.Once resumed, all updates will be
		processed.
		'''
		return self._Entity.PauseUpdates()

	def ResumeUpdates(self) -> None:
		'''
		Resume the sending of updates.Any paused updates will be processed.
		'''
		return self._Entity.ResumeUpdates()

	def UnpackageProject(self, sourcePackagePath: str, destinationFolder: str = None, includeFemInputOutputFiles: bool = True, includeWorkingFolder: bool = True, includeLoadFiles: bool = True, includeAdditionalFiles: bool = True) -> types.SimpleStatus:
		'''
		Unpackage the source .hxp package into the destination folder.
		The destination folder should be empty.
		'''
		return types.SimpleStatus(self._Entity.UnpackageProject(sourcePackagePath, destinationFolder, includeFemInputOutputFiles, includeWorkingFolder, includeLoadFiles, includeAdditionalFiles))

	def CompareDatabases(self, outputPath: str, originalDatabasePath: str, modifiedDatabasePath: str, originalProject: str = None, modifiedProject: str = None, compareAssignableProperties: bool = True, compareMaterialsFastenersAndRivets: bool = True, compareProjectSetup: bool = False) -> types.SimpleStatus:
		return types.SimpleStatus(self._Entity.CompareDatabases(outputPath, originalDatabasePath, modifiedDatabasePath, originalProject, modifiedProject, compareAssignableProperties, compareMaterialsFastenersAndRivets, compareProjectSetup))

	def CloseDatabase(self, delay: int = 1) -> None:
		'''
		Close the currently open database if one exists.
		
		:param delay: Delay closing the connection for this many seconds.
		'''
		return self._Entity.CloseDatabase(delay)

	def CopyProject(self, projectId: int, newName: str = None, copyDesignProperties: bool = True, copyAnalysisProperties: bool = True, copyLoadProperties: bool = True, copyWorkingFolder: bool = True) -> ProjectInfo:
		'''
		Copy a project
		
		:param projectId: Id of the project to copy
		:param newName: Name for the new project
		:param copyDesignProperties: Flag indicating whether design properties should be copied in the new project
		:param copyAnalysisProperties: Flag indicating whether analysis properties should be copied in the new project
		:param copyLoadProperties: Flag indicating whether load properties should be copied in the new project
		:param copyWorkingFolder: Flag indicating whether working folder should be copied
		
		:return: The ProjectInfo for the copied project.
		'''
		return ProjectInfo(self._Entity.CopyProject(projectId, newName, copyDesignProperties, copyAnalysisProperties, copyLoadProperties, copyWorkingFolder))

	def CreateDatabaseFromTemplate(self, templateName: str, newPath: str) -> None:
		'''
		Create a new database.
		
		:param templateName: The name of the template to base this database on.
		:param newPath: The path to the new database.
		'''
		return self._Entity.CreateDatabaseFromTemplate(templateName, newPath)

	def CreateProject(self, projectName: str = None) -> ProjectInfo:
		'''
		Create a Project.
		
		:return: The ProjectInfo for the created Project.
		'''
		return ProjectInfo(self._Entity.CreateProject(projectName))

	def DeleteProject(self, projectName: str) -> ProjectDeletionStatus:
		return ProjectDeletionStatus[self._Entity.DeleteProject(projectName).ToString()]

	def Dispose(self) -> None:
		'''
		Dispose of the application. Should be explicitly called after the application
		is no longer needed unless the application is wrapped with a using clause.
		'''
		return self._Entity.Dispose()

	def GetAnalyses(self) -> dict[int, AnalysisDefinition]:
		'''
		Get all Analysis Definitions in the database.
		'''
		warnings.warn("This method is slated to be deleted. Do not use.", DeprecationWarning, 2)
		return dict[int, AnalysisDefinition](self._Entity.GetAnalyses())

	def Login(self, userName: str, password: str = "") -> None:
		'''
		Login to the Scripting API with a specified username and password.
		
		:param userName: Username to login with.
		:param password: Password to log in with
		'''
		return self._Entity.Login(userName, password)

	def Migrate(self, databasePath: str) -> str:
		'''
		Migrate the database to the latest version.
		
		:return: File path to the new database file
		'''
		return self._Entity.Migrate(databasePath)

	def CheckDatabaseIsUpToDate(self, databasePath: str) -> bool:
		'''
		Returns true if the database version matches the version of this scripting API.
		Otherwise returns false.
		'''
		return self._Entity.CheckDatabaseIsUpToDate(databasePath)

	def OpenDatabase(self, databasePath: str) -> None:
		'''
		Open a database to manipulate with the API.
		
		:param databasePath: File path to the DB.
		'''
		return self._Entity.OpenDatabase(databasePath)

	def SelectProject(self, projectName: str) -> Project:
		'''
		Select the active project.
		Activating a project will deactivate the current project (if present).
		'''
		return Project(self._Entity.SelectProject(projectName))

	def ImportMaterialsFromExcel(self, filePath: str, deletePlies: bool = False, updateMaterialsInUseInOtherProjects: bool = False) -> types.SimpleStatus:
		'''
		Import materials from an Excel spreadsheet. Returns true on successful import.
		
		:param deletePlies: Determines whether to update laminate or laminate families with changes that will delete plies in structures.
		:param updateMaterialsInUseInOtherProjects: Determines whether to update materials in use by projects outside the active project.
		'''
		return types.SimpleStatus(self._Entity.ImportMaterialsFromExcel(filePath, deletePlies, updateMaterialsInUseInOtherProjects))

	def CreateHyperXpertPoints(self, runSetSpecifiers: set[RunSetSpecifier], plotMode: types.DoePlotMode, pointType: types.DoePointType, generateVariabilityForLinked: bool, filterNonGeometry: bool) -> list[HyperXpertPoint]:
		'''
		Create HyperXpert points based on specific run sets.
		'''
		runSetSpecifiersSet = HashSet[_api.RunSetSpecifier]()
		if runSetSpecifiers is not None:
			for x in runSetSpecifiers:
				if x is not None:
					runSetSpecifiersSet.Add(x._Entity)
		return [HyperXpertPoint(hyperXpertPoint) for hyperXpertPoint in self._Entity.CreateHyperXpertPoints(runSetSpecifiersSet, _types.DoePlotMode(types.GetEnumValue(plotMode.value)), _types.DoePointType(types.GetEnumValue(pointType.value)), generateVariabilityForLinked, filterNonGeometry)]

	def GetRunSetsByProject(self) -> dict[int, list[RunSet]]:
		'''
		Gets a dictionary mapping ProjectId to a List of RunSets.
		'''
		return dict[int, list[RunSet]](self._Entity.GetRunSetsByProject())


class FabricationCriterionRatio(IdEntity):
	def __init__(self, fabricationCriterionRatio: _api.FabricationCriterionRatio):
		self._Entity = fabricationCriterionRatio

	@property
	def FabricationRatioId(self) -> types.FabricationRatio:
		result = self._Entity.FabricationRatioId
		return types.FabricationRatio[result.ToString()] if result is not None else None

	@property
	def Check(self) -> bool:
		return self._Entity.Check

	@Check.setter
	def Check(self, value: bool) -> None:
		self._Entity.Check = value


class JointDesignProperty(DesignProperty):
	def __init__(self, jointDesignProperty: _api.JointDesignProperty):
		self._Entity = jointDesignProperty


class SizingMaterial(IdEntity):
	def __init__(self, sizingMaterial: _api.SizingMaterial):
		self._Entity = sizingMaterial

	@property
	def MaterialId(self) -> int:
		return self._Entity.MaterialId

	@property
	def MaterialName(self) -> str:
		return self._Entity.MaterialName

	@property
	def MaterialType(self) -> types.MaterialType:
		result = self._Entity.MaterialType
		return types.MaterialType[result.ToString()] if result is not None else None


class SizingMaterialCol(IdEntityCol[SizingMaterial]):
	def __init__(self, sizingMaterialCol: _api.SizingMaterialCol):
		self._Entity = sizingMaterialCol
		self._CollectedClass = SizingMaterial

	@property
	def SizingMaterialColList(self) -> tuple[SizingMaterial]:
		return tuple([SizingMaterial(sizingMaterialCol) for sizingMaterialCol in self._Entity])

	@overload
	def Get(self, name: str) -> SizingMaterial:
		'''
		Get a sizing material by name.
		
		:raises ``System.ArgumentException``: Throws if the material is not in the database or if the material is not in the list of sizing materials.
		'''
		...

	@overload
	def Contains(self, name: str) -> bool:
		'''
		Check if the list of sizing materials contains a material by name.
		
		:return: ``False`` if the material does not exist in the database or is not in the list of sizing materials.
		'''
		...

	@overload
	def AddSizingMaterial(self, materialId: int) -> bool:
		'''
		Add a ``hyperx.api.SizingMaterial`` by ``materialId`` to the list of sizing materials.
		
		:return: ``False`` if the material was not found.
		
		:raises ``System.InvalidOperationException``:
		'''
		...

	@overload
	def AddSizingMaterial(self, name: str) -> bool:
		'''
		Add a ``hyperx.api.SizingMaterial`` by ``name`` to the list of sizing materials.
		
		:return: ``False`` if the material was not found.
		
		:raises ``System.InvalidOperationException``:
		'''
		...

	def AddSizingMaterialsByName(self, materialNames: tuple[str], ignoreMissingMaterials: bool = False) -> types.TernaryStatus:
		'''
		Add a set of ``hyperx.api.SizingMaterial`` by ``materialNames`` to the list of sizing materials.
		
		:return: ``hyperx.api.types.TernaryStatus`` with information about whether materials were successfully added or failed.
		
		:raises ``System.InvalidOperationException``:
		'''
		materialNamesList = List[str]()
		if materialNames is not None:
			for x in materialNames:
				if x is not None:
					materialNamesList.Add(x)
		materialNamesEnumerable = IEnumerable(materialNamesList)
		return types.TernaryStatus(self._Entity.AddSizingMaterialsByName(materialNamesEnumerable, ignoreMissingMaterials))

	def AddSizingMaterialsById(self, materialIds: tuple[int], ignoreMissingMaterials: bool = False) -> types.TernaryStatus:
		'''
		Add a set of ``hyperx.api.SizingMaterial`` by ``materialIds`` to the list of sizing materials.
		
		:return: ``hyperx.api.types.TernaryStatus`` with information about whether materials were successfully added or failed.
		
		:raises ``System.InvalidOperationException``:
		'''
		materialIdsList = MakeCSharpIntList(materialIds)
		materialIdsEnumerable = IEnumerable(materialIdsList)
		return types.TernaryStatus(self._Entity.AddSizingMaterialsById(materialIdsEnumerable, ignoreMissingMaterials))

	@overload
	def RemoveSizingMaterial(self, materialId: int) -> bool:
		'''
		Remove a ``hyperx.api.SizingMaterial`` by ``materialId`` from the list of sizing materials.
		
		:return: ``False`` if the material is not in the list of sizing materials.
		'''
		...

	@overload
	def RemoveSizingMaterial(self, name: str) -> bool:
		'''
		Remove a ``hyperx.api.SizingMaterial`` by ``name`` from the list of sizing materials.
		
		:return: ``False`` if the material is not in the list of sizing materials.
		
		:raises ``System.InvalidOperationException``:
		'''
		...

	def RemoveSizingMaterialsById(self, materialIds: tuple[int], ignoreMissingMaterials: bool = False) -> types.TernaryStatus:
		'''
		Remove a set of ``hyperx.api.SizingMaterial`` by ``materialIds`` from the list of sizing materials.
		
		:return: ``hyperx.api.types.TernaryStatus`` with information about whether materials were successfully removed or failed.
		
		:raises ``System.InvalidOperationException``:
		'''
		materialIdsList = MakeCSharpIntList(materialIds)
		materialIdsEnumerable = IEnumerable(materialIdsList)
		return types.TernaryStatus(self._Entity.RemoveSizingMaterialsById(materialIdsEnumerable, ignoreMissingMaterials))

	def RemoveSizingMaterialsByName(self, materialNames: tuple[str], ignoreMissingMaterials: bool = False) -> types.TernaryStatus:
		'''
		Remove a set of ``hyperx.api.SizingMaterial`` by ``materialNames`` from the list of sizing materials.
		
		:return: ``hyperx.api.types.TernaryStatus`` with information about whether materials were successfully removed or failed.
		
		:raises ``System.InvalidOperationException``:
		'''
		materialNamesList = List[str]()
		if materialNames is not None:
			for x in materialNames:
				if x is not None:
					materialNamesList.Add(x)
		materialNamesEnumerable = IEnumerable(materialNamesList)
		return types.TernaryStatus(self._Entity.RemoveSizingMaterialsByName(materialNamesEnumerable, ignoreMissingMaterials))

	def RemoveAllSizingMaterials(self) -> None:
		'''
		Remove all ``hyperx.api.SizingMaterial`` from the list of sizing materials.
		'''
		return self._Entity.RemoveAllSizingMaterials()

	@overload
	def Contains(self, id: int) -> bool:
		...

	@overload
	def Get(self, id: int) -> SizingMaterial:
		...

	def Get(self, item1 = None) -> SizingMaterial:
		'''
		Overload 1: ``Get(self, name: str) -> SizingMaterial``

		Get a sizing material by name.
		
		:raises ``System.ArgumentException``: Throws if the material is not in the database or if the material is not in the list of sizing materials.

		Overload 2: ``Get(self, id: int) -> SizingMaterial``
		'''
		if isinstance(item1, str):
			return SizingMaterial(self._Entity.Get(item1))

		if isinstance(item1, int):
			return SizingMaterial(super().Get(item1))

		return SizingMaterial(self._Entity.Get(item1))

	def Contains(self, item1 = None) -> bool:
		'''
		Overload 1: ``Contains(self, name: str) -> bool``

		Check if the list of sizing materials contains a material by name.
		
		:return: ``False`` if the material does not exist in the database or is not in the list of sizing materials.

		Overload 2: ``Contains(self, id: int) -> bool``
		'''
		if isinstance(item1, str):
			return self._Entity.Contains(item1)

		if isinstance(item1, int):
			return bool(super().Contains(item1))

		return self._Entity.Contains(item1)

	def AddSizingMaterial(self, item1 = None) -> bool:
		'''
		Overload 1: ``AddSizingMaterial(self, materialId: int) -> bool``

		Add a ``hyperx.api.SizingMaterial`` by ``materialId`` to the list of sizing materials.
		
		:return: ``False`` if the material was not found.
		
		:raises ``System.InvalidOperationException``:

		Overload 2: ``AddSizingMaterial(self, name: str) -> bool``

		Add a ``hyperx.api.SizingMaterial`` by ``name`` to the list of sizing materials.
		
		:return: ``False`` if the material was not found.
		
		:raises ``System.InvalidOperationException``:
		'''
		if isinstance(item1, int):
			return self._Entity.AddSizingMaterial(item1)

		if isinstance(item1, str):
			return self._Entity.AddSizingMaterial(item1)

		return self._Entity.AddSizingMaterial(item1)

	def RemoveSizingMaterial(self, item1 = None) -> bool:
		'''
		Overload 1: ``RemoveSizingMaterial(self, materialId: int) -> bool``

		Remove a ``hyperx.api.SizingMaterial`` by ``materialId`` from the list of sizing materials.
		
		:return: ``False`` if the material is not in the list of sizing materials.

		Overload 2: ``RemoveSizingMaterial(self, name: str) -> bool``

		Remove a ``hyperx.api.SizingMaterial`` by ``name`` from the list of sizing materials.
		
		:return: ``False`` if the material is not in the list of sizing materials.
		
		:raises ``System.InvalidOperationException``:
		'''
		if isinstance(item1, int):
			return self._Entity.RemoveSizingMaterial(item1)

		if isinstance(item1, str):
			return self._Entity.RemoveSizingMaterial(item1)

		return self._Entity.RemoveSizingMaterial(item1)

	def __getitem__(self, index: int):
		return self.SizingMaterialColList[index]

	def __iter__(self):
		yield from self.SizingMaterialColList

	def __len__(self):
		return len(self.SizingMaterialColList)


class ZoneOverride(IdEntity):
	def __init__(self, zoneOverride: _api.ZoneOverride):
		self._Entity = zoneOverride

	@property
	def AllowMaterials(self) -> bool:
		return self._Entity.AllowMaterials

	@property
	def ProjectId(self) -> int:
		return self._Entity.ProjectId

	@property
	def DesignId(self) -> int:
		'''
		The ``hyperx.api.DesignVariable`` Id associated with this override.
		'''
		return self._Entity.DesignId

	@property
	def FamilyId(self) -> types.BeamPanelFamily:
		'''
		The ``hyperx.api.types.BeamPanelFamily`` Id associated with this override.
		'''
		result = self._Entity.FamilyId
		return types.BeamPanelFamily[result.ToString()] if result is not None else None

	@property
	def ConceptId(self) -> int:
		'''
		The ``hyperx.api.ZoneDesignProperty.ConceptId`` associated with this override.
		'''
		return self._Entity.ConceptId

	@property
	def VariableId(self) -> int:
		'''
		The ``hyperx.api.DesignVariable`` Id associated with this override.
		'''
		return self._Entity.VariableId

	@property
	def MinBound(self) -> float | None:
		'''
		Minimum sizing bound for this override.
		You cannot set a ``hyperx.api.ZoneOverride.MinBound`` if your override sizing materials are laminate ``hyperx.api.types.MaterialType``.
		
		:raises ``System.InvalidOperationException``: In the case of laminates, the  is , and setting it will throw an error.
		'''
		return self._Entity.MinBound

	@property
	def MaxBound(self) -> float | None:
		'''
		Maximum sizing bound for this override.
		You cannot set a ``hyperx.api.ZoneOverride.MaxBound`` if your override sizing materials are laminate ``hyperx.api.types.MaterialType``.
		In the case of laminates, the ``hyperx.api.ZoneOverride.MaxBound`` is ``None``, and setting it will throw an error.
		'''
		return self._Entity.MaxBound

	@property
	def StepSize(self) -> float | None:
		'''
		Sizing step size for this override.
		You cannot set a ``hyperx.api.ZoneOverride.StepSize`` if your override sizing materials are laminate ``hyperx.api.types.MaterialType``.
		In the case of laminates, the ``hyperx.api.ZoneOverride.StepSize`` is ``None``, and setting it will throw an error.
		'''
		return self._Entity.StepSize

	@property
	def MinPlies(self) -> int | None:
		'''
		Ply-based sizing min bound for this override. Applicable to Effective Laminate sizing where the sizing dimension is plies.
		'''
		return self._Entity.MinPlies

	@property
	def MaxPlies(self) -> int | None:
		'''
		Ply-based sizing max bound for this override. Applicable to Effective Laminate sizing where the sizing dimension is plies.
		'''
		return self._Entity.MaxPlies

	@property
	def PlyStepSize(self) -> int | None:
		'''
		Ply-based sizing step size for this override. Applicable to Effective Laminate sizing where the sizing dimension is plies.
		'''
		return self._Entity.PlyStepSize

	@property
	def InputMode(self) -> types.VariableInputMode | None:
		result = self._Entity.InputMode
		return types.VariableInputMode[result.ToString()] if result is not None else None

	@property
	def SizingMaterials(self) -> SizingMaterialCol:
		'''
		Collection of ``hyperx.api.SizingMaterial`` candidates
		'''
		result = self._Entity.SizingMaterials
		return SizingMaterialCol(result) if result is not None else None

	@property
	def AnalysisValue(self) -> float | None:
		'''
		Get and set analysis value.
		You cannot set an analysis value if your analysis material is a laminate ``hyperx.api.types.MaterialType``.
		In the case of a laminate, the analysis value is ``None``, and setting it will throw an error.
		'''
		return self._Entity.AnalysisValue

	@property
	def AnalysisMaterial(self) -> str:
		'''
		Get and set the analysis material by name.
		
		:raises ``System.Exception``: If no analysis material is set when trying to get the
		'''
		return self._Entity.AnalysisMaterial

	@property
	def AnalysisMaterialType(self) -> types.MaterialType | None:
		result = self._Entity.AnalysisMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@MinBound.setter
	def MinBound(self, value: float | None) -> None:
		self._Entity.MinBound = value

	@MaxBound.setter
	def MaxBound(self, value: float | None) -> None:
		self._Entity.MaxBound = value

	@StepSize.setter
	def StepSize(self, value: float | None) -> None:
		self._Entity.StepSize = value

	@MinPlies.setter
	def MinPlies(self, value: int | None) -> None:
		self._Entity.MinPlies = value

	@MaxPlies.setter
	def MaxPlies(self, value: int | None) -> None:
		self._Entity.MaxPlies = value

	@PlyStepSize.setter
	def PlyStepSize(self, value: int | None) -> None:
		self._Entity.PlyStepSize = value

	@AnalysisValue.setter
	def AnalysisValue(self, value: float | None) -> None:
		self._Entity.AnalysisValue = value

	@AnalysisMaterial.setter
	def AnalysisMaterial(self, value: str) -> None:
		self._Entity.AnalysisMaterial = value


class ToolingConstraint(IdNameEntity):
	'''
	Tooling constraints are a feature of Design Properties for Zones.
	'''
	def __init__(self, toolingConstraint: _api.ToolingConstraint):
		self._Entity = toolingConstraint

	@property
	def ConstraintMax(self) -> float:
		'''
		The max constraint bound for the range constraint type.
		'''
		return self._Entity.ConstraintMax

	@property
	def ConstraintMin(self) -> float:
		'''
		The min constraint bound for the range constraint type.
		'''
		return self._Entity.ConstraintMin

	@property
	def ConstraintValue(self) -> float:
		'''
		The value for this ``hyperx.api.ToolingConstraint``.
		Use ``hyperx.api.ToolingConstraint.ToolingSelectionType`` to determine how this value is used.
		'''
		return self._Entity.ConstraintValue

	@property
	def ToolingSelectionType(self) -> types.ToolingSelectionType:
		'''
		Defines which ``hyperx.api.types.ToolingSelectionType`` a given tooling constraint is currently set to.
		'''
		result = self._Entity.ToolingSelectionType
		return types.ToolingSelectionType[result.ToString()] if result is not None else None

	def SetToAnyValue(self) -> None:
		'''
		Change the ``hyperx.api.ToolingConstraint.ToolingSelectionType`` to ``hyperx.api.types.ToolingSelectionType.AnyValue``.
		'''
		return self._Entity.SetToAnyValue()

	def SetToInequality(self, value: float) -> None:
		'''
		Set the tooling constraint to an inequality if the constraint type is an inequality.
		Sets the ``hyperx.api.ToolingConstraint.ToolingSelectionType`` to ``hyperx.api.types.ToolingSelectionType.SpecifiedLimitOrRange``.
		
		:raises ``System.InvalidOperationException``: If the constraint type is not an inequality.
		'''
		return self._Entity.SetToInequality(value)

	def SetToRange(self, min: float, max: float) -> None:
		'''
		Set the tooling constraint to a range if the constraint type is a range.
		Sets the ``hyperx.api.ToolingConstraint.ToolingSelectionType`` to ``hyperx.api.types.ToolingSelectionType.SpecifiedLimitOrRange``.
		
		:raises ``System.InvalidOperationException``: If the constraint type is not .
		'''
		return self._Entity.SetToRange(min, max)

	def SetToValue(self, value: float) -> None:
		'''
		Set the tooling constraint to a value.
		Sets the ``hyperx.api.ToolingConstraint.ToolingSelectionType`` to ``hyperx.api.types.ToolingSelectionType.SpecifiedValue``.
		
		:raises ``System.InvalidOperationException``:
		'''
		return self._Entity.SetToValue(value)


class ZoneOverrideCol(IdEntityCol[ZoneOverride]):
	def __init__(self, zoneOverrideCol: _api.ZoneOverrideCol):
		self._Entity = zoneOverrideCol
		self._CollectedClass = ZoneOverride

	@property
	def ZoneOverrideColList(self) -> tuple[ZoneOverride]:
		return tuple([ZoneOverride(zoneOverrideCol) for zoneOverrideCol in self._Entity])

	def Get(self, zoneNumber: int) -> ZoneOverride:
		'''
		Get override for a ``hyperx.api.Zone`` by the Id
		'''
		return ZoneOverride(self._Entity.Get(zoneNumber))

	def __getitem__(self, index: int):
		return self.ZoneOverrideColList[index]

	def __iter__(self):
		yield from self.ZoneOverrideColList

	def __len__(self):
		return len(self.ZoneOverrideColList)


class DesignVariable(IdEntity):
	'''
	Holds design variable data.
	Min, max, steps, materials.
	'''
	def __init__(self, designVariable: _api.DesignVariable):
		self._Entity = designVariable

	@property
	def VariableParameter(self) -> types.VariableParameter:
		result = self._Entity.VariableParameter
		return types.VariableParameter[result.ToString()] if result is not None else None

	@property
	def AllowMaterials(self) -> bool:
		'''
		Returns ``True`` if this item supports assigning materials.
		'''
		return self._Entity.AllowMaterials

	@property
	def IsDependentVariable(self) -> bool:
		'''
		Returns ``True`` if this design variable is dependent on other design variables.
		'''
		return self._Entity.IsDependentVariable

	@property
	def Max(self) -> float | None:
		'''
		Maximum bound for this row.
		You cannot set a Max if your ``hyperx.api.DesignVariable.SizingMaterialType`` is a laminate ``hyperx.api.types.MaterialType``.
		In the case of laminates, the Max is determined by the laminate thickness, and setting it will throw an error.
		'''
		return self._Entity.Max

	@property
	def Min(self) -> float | None:
		'''
		Minimum bound for this row.
		You cannot set a Min if your ``hyperx.api.DesignVariable.SizingMaterialType`` is a laminate ``hyperx.api.types.MaterialType``.
		In the case of laminates, the Min is determined by the laminate thickness, and setting it will throw an error.
		'''
		return self._Entity.Min

	@property
	def Name(self) -> str:
		return self._Entity.Name

	@property
	def StepSize(self) -> float | None:
		'''
		Step size for this row.
		You cannot set a StepSize if your ``hyperx.api.DesignVariable.SizingMaterialType`` is a laminate ``hyperx.api.types.MaterialType``.
		In the case of laminates, the StepSize is ``None``, and setting it will throw an error.
		'''
		return self._Entity.StepSize

	@property
	def UseAnalysis(self) -> bool:
		'''
		Use Analysis for Sizing while in Detailed Sizing.
		'''
		return self._Entity.UseAnalysis

	@property
	def AnalysisMaterial(self) -> str:
		'''
		Get and set analysis material by name
		'''
		return self._Entity.AnalysisMaterial

	@property
	def AnalysisMaterialType(self) -> types.MaterialType | None:
		'''
		Get analysis material type
		'''
		result = self._Entity.AnalysisMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def SizingMaterialType(self) -> types.MaterialType | None:
		'''
		Get sizing material type
		'''
		result = self._Entity.SizingMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def AnalysisValue(self) -> float | None:
		'''
		Get and set analysis value
		You cannot set an analysis value if your analysis material is a laminate ``hyperx.api.types.MaterialType``.
		In the case of a laminate, the analysis value is derived from thickness, and setting it will throw an error.
		'''
		return self._Entity.AnalysisValue

	@property
	def Overrides(self) -> ZoneOverrideCol:
		'''
		Collection of overrides by zone for the design variable
		'''
		result = self._Entity.Overrides
		return ZoneOverrideCol(result) if result is not None else None

	@property
	def SizingMaterials(self) -> SizingMaterialCol:
		'''
		Collection of ``hyperx.api.SizingMaterial`` candidates
		'''
		result = self._Entity.SizingMaterials
		return SizingMaterialCol(result) if result is not None else None

	@Max.setter
	def Max(self, value: float | None) -> None:
		self._Entity.Max = value

	@Min.setter
	def Min(self, value: float | None) -> None:
		self._Entity.Min = value

	@StepSize.setter
	def StepSize(self, value: float | None) -> None:
		self._Entity.StepSize = value

	@UseAnalysis.setter
	def UseAnalysis(self, value: bool) -> None:
		self._Entity.UseAnalysis = value

	@AnalysisMaterial.setter
	def AnalysisMaterial(self, value: str) -> None:
		self._Entity.AnalysisMaterial = value

	@AnalysisValue.setter
	def AnalysisValue(self, value: float | None) -> None:
		self._Entity.AnalysisValue = value

	@overload
	def AddMaterials(self, materialIds: set[int]) -> None:
		'''
		Obsolete use ``hyperx.api.DesignVariable.SizingMaterials`` instead.
		<br />
		Add sizing materials by material Id.
		'''
		...

	@overload
	def AddMaterials(self, materialNames: set[str]) -> None:
		'''
		Obsolete use ``hyperx.api.DesignVariable.SizingMaterials`` instead.
		<br />
		Add sizing materials by material Name.
		'''
		...

	def GetSizingMaterials(self) -> list[int]:
		'''
		Obsolete use ``hyperx.api.DesignVariable.SizingMaterials`` instead.
		<br />
		Get a list of material Ids used for sizing, if they exist.
		'''
		warnings.warn("Use SizingMaterials collection instead.", DeprecationWarning, 2)
		return [int32 for int32 in self._Entity.GetSizingMaterials()]

	def RemoveSizingMaterials(self, materialIds: tuple[int] = None) -> None:
		'''
		Obsolete use ``hyperx.api.DesignVariable.SizingMaterials`` instead.
		<br />
		Remove sizing materials assigned to this variable by a collection of Ids.
		
		:param materialIds: If not specified, remove all materials.
		'''
		materialIdsList = MakeCSharpIntList(materialIds)
		materialIdsEnumerable = IEnumerable(materialIdsList)
		warnings.warn("Use SizingMaterials collection instead.", DeprecationWarning, 2)
		return self._Entity.RemoveSizingMaterials(materialIds if materialIds is None else materialIdsEnumerable)

	def GetAnalysisMaterial(self) -> int | None:
		'''
		Obsolete use ``hyperx.api.DesignVariable.AnalysisMaterial`` instead.
		<br />
		Get the material used for analysis, if it exists.
		'''
		warnings.warn("Use AnalysisMaterial property instead.", DeprecationWarning, 2)
		return self._Entity.GetAnalysisMaterial()

	def RemoveAnalysisMaterial(self) -> None:
		'''
		Remove the analysis material assigned to this variable.
		'''
		return self._Entity.RemoveAnalysisMaterial()

	def AddMaterials(self, item1 = None) -> None:
		'''
		Overload 1: ``AddMaterials(self, materialIds: set[int]) -> None``

		Obsolete use ``hyperx.api.DesignVariable.SizingMaterials`` instead.
		<br />
		Add sizing materials by material Id.

		Overload 2: ``AddMaterials(self, materialNames: set[str]) -> None``

		Obsolete use ``hyperx.api.DesignVariable.SizingMaterials`` instead.
		<br />
		Add sizing materials by material Name.
		'''
		if isinstance(item1, set) and item1 and any(isinstance(x, int) for x in item1):
			materialIdsSet = HashSet[int]()
			if item1 is not None:
				for x in item1:
					if x is not None:
						materialIdsSet.Add(x)
			warnings.warn("Use SizingMaterials collection instead.", DeprecationWarning, 2)
			return self._Entity.AddMaterials(materialIdsSet)

		if isinstance(item1, set) and item1 and any(isinstance(x, str) for x in item1):
			materialNamesSet = HashSet[str]()
			if item1 is not None:
				for x in item1:
					if x is not None:
						materialNamesSet.Add(x)
			warnings.warn("Use SizingMaterials collection instead.", DeprecationWarning, 2)
			return self._Entity.AddMaterials(materialNamesSet)

		warnings.warn("Use SizingMaterials collection instead.", DeprecationWarning, 2)
		return self._Entity.AddMaterials(item1)


class FabricationCriterionRatioCol(IdEntityCol[FabricationCriterionRatio]):
	def __init__(self, fabricationCriterionRatioCol: _api.FabricationCriterionRatioCol):
		self._Entity = fabricationCriterionRatioCol
		self._CollectedClass = FabricationCriterionRatio

	@property
	def FabricationCriterionRatioColList(self) -> tuple[FabricationCriterionRatio]:
		return tuple([FabricationCriterionRatio(fabricationCriterionRatioCol) for fabricationCriterionRatioCol in self._Entity])

	@overload
	def Get(self, fabricationRatioId: types.FabricationRatio) -> FabricationCriterionRatio:
		...

	@overload
	def Get(self, id: int) -> FabricationCriterionRatio:
		...

	def Get(self, item1 = None) -> FabricationCriterionRatio:
		'''
		Overload 1: ``Get(self, fabricationRatioId: types.FabricationRatio) -> FabricationCriterionRatio``

		Overload 2: ``Get(self, id: int) -> FabricationCriterionRatio``
		'''
		if isinstance(item1, types.FabricationRatio):
			return FabricationCriterionRatio(self._Entity.Get(_types.FabricationRatio(types.GetEnumValue(item1.value))))

		if isinstance(item1, int):
			return FabricationCriterionRatio(super().Get(item1))

		return FabricationCriterionRatio(self._Entity.Get(_types.FabricationRatio(types.GetEnumValue(item1.value))))

	def __getitem__(self, index: int):
		return self.FabricationCriterionRatioColList[index]

	def __iter__(self):
		yield from self.FabricationCriterionRatioColList

	def __len__(self):
		return len(self.FabricationCriterionRatioColList)


class ToolingConstraintCol(IdNameEntityCol[ToolingConstraint]):
	def __init__(self, toolingConstraintCol: _api.ToolingConstraintCol):
		self._Entity = toolingConstraintCol
		self._CollectedClass = ToolingConstraint

	@property
	def ToolingConstraintColList(self) -> tuple[ToolingConstraint]:
		return tuple([ToolingConstraint(toolingConstraintCol) for toolingConstraintCol in self._Entity])

	@overload
	def Get(self, name: str) -> ToolingConstraint:
		...

	@overload
	def Get(self, id: int) -> ToolingConstraint:
		...

	def Get(self, item1 = None) -> ToolingConstraint:
		'''
		Overload 1: ``Get(self, name: str) -> ToolingConstraint``

		Overload 2: ``Get(self, id: int) -> ToolingConstraint``
		'''
		if isinstance(item1, str):
			return ToolingConstraint(super().Get(item1))

		if isinstance(item1, int):
			return ToolingConstraint(super().Get(item1))

		return ToolingConstraint(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.ToolingConstraintColList[index]

	def __iter__(self):
		yield from self.ToolingConstraintColList

	def __len__(self):
		return len(self.ToolingConstraintColList)


class DesignVariableCol(IdEntityCol[DesignVariable]):
	def __init__(self, designVariableCol: _api.DesignVariableCol):
		self._Entity = designVariableCol
		self._CollectedClass = DesignVariable

	@property
	def DesignVariableColList(self) -> tuple[DesignVariable]:
		return tuple([DesignVariable(designVariableCol) for designVariableCol in self._Entity])

	@overload
	def Get(self, parameterId: types.VariableParameter) -> DesignVariable:
		'''
		Gets a ``hyperx.api.DesignVariable`` from a ``hyperx.api.types.VariableParameter``.
		
		:raises ``System.ArgumentException``: If the design property does not contain the requested .
		'''
		...

	@overload
	def Get(self, id: int) -> DesignVariable:
		...

	def Get(self, item1 = None) -> DesignVariable:
		'''
		Overload 1: ``Get(self, parameterId: types.VariableParameter) -> DesignVariable``

		Gets a ``hyperx.api.DesignVariable`` from a ``hyperx.api.types.VariableParameter``.
		
		:raises ``System.ArgumentException``: If the design property does not contain the requested .

		Overload 2: ``Get(self, id: int) -> DesignVariable``
		'''
		if isinstance(item1, types.VariableParameter):
			return DesignVariable(self._Entity.Get(_types.VariableParameter(types.GetEnumValue(item1.value))))

		if isinstance(item1, int):
			return DesignVariable(super().Get(item1))

		return DesignVariable(self._Entity.Get(_types.VariableParameter(types.GetEnumValue(item1.value))))

	def __getitem__(self, index: int):
		return self.DesignVariableColList[index]

	def __iter__(self):
		yield from self.DesignVariableColList

	def __len__(self):
		return len(self.DesignVariableColList)


class ZoneDesignProperty(DesignProperty):
	def __init__(self, zoneDesignProperty: _api.ZoneDesignProperty):
		self._Entity = zoneDesignProperty

	@property
	def FamilyId(self) -> types.BeamPanelFamily:
		result = self._Entity.FamilyId
		return types.BeamPanelFamily[result.ToString()] if result is not None else None

	@property
	def ConceptId(self) -> int:
		return self._Entity.ConceptId

	@property
	def FamilyConceptUID(self) -> types.FamilyConceptUID:
		result = self._Entity.FamilyConceptUID
		return types.FamilyConceptUID[result.ToString()] if result is not None else None

	@property
	def ToolingConstraints(self) -> ToolingConstraintCol:
		'''
		Get a ``hyperx.api.ToolingConstraint`` collection for this ``hyperx.api.ZoneDesignProperty``.
		'''
		result = self._Entity.ToolingConstraints
		return ToolingConstraintCol(result) if result is not None else None

	@property
	def DesignVariables(self) -> DesignVariableCol:
		'''
		Get a ``hyperx.api.DesignVariable`` collection for this ``hyperx.api.ZoneDesignProperty``.
		'''
		result = self._Entity.DesignVariables
		return DesignVariableCol(result) if result is not None else None

	@property
	def HeightSizingVariable(self) -> types.HeightSizingVariable:
		result = self._Entity.HeightSizingVariable
		return types.HeightSizingVariable[result.ToString()] if result is not None else None

	@property
	def HasFabricationCriteria(self) -> bool:
		return self._Entity.HasFabricationCriteria

	@property
	def FabricationCriterionRatios(self) -> FabricationCriterionRatioCol:
		'''
		Gets a ``hyperx.api.FabricationCriterionRatioCol`` of fabrication criterion ratios.
		'''
		result = self._Entity.FabricationCriterionRatios
		return FabricationCriterionRatioCol(result) if result is not None else None

	@property
	def DiscreteStiffenerTechnique(self) -> types.DiscreteTechnique | None:
		result = self._Entity.DiscreteStiffenerTechnique
		return types.DiscreteTechnique[result.ToString()] if result is not None else None

	@HeightSizingVariable.setter
	def HeightSizingVariable(self, value: types.HeightSizingVariable) -> None:
		self._Entity.HeightSizingVariable = _types.HeightSizingVariable(types.GetEnumValue(value.value))


class BulkUpdaterBase(ABC):
	def __init__(self, bulkUpdaterBase: _api.BulkUpdaterBase):
		self._Entity = bulkUpdaterBase

	def Update(self, func: Action) -> None:
		entityType = self._Entity.GetType().BaseType.GenericTypeArguments[0]
		funcAction = Action[entityType](func)
		return self._Entity.Update(funcAction)


class LoadPropertyUserRowBulkUpdater(BulkUpdaterBase):
	def __init__(self, loadPropertyUserRowBulkUpdater: _api.LoadPropertyUserRowBulkUpdater):
		self._Entity = loadPropertyUserRowBulkUpdater


class LoadPropertyUserRow(IdNameEntity):
	def __init__(self, loadPropertyUserRow: _api.LoadPropertyUserRow):
		self._Entity = loadPropertyUserRow

	@property
	def LoadScenarioId(self) -> int:
		return self._Entity.LoadScenarioId

	@property
	def LoadPropertyId(self) -> int:
		return self._Entity.LoadPropertyId

	@property
	def Type(self) -> types.LoadSetType:
		result = self._Entity.Type
		return types.LoadSetType[result.ToString()] if result is not None else None

	@property
	def ReferenceTemperature(self) -> float:
		'''
		Units: English = °F | Standard = °C.
		'''
		return self._Entity.ReferenceTemperature

	@property
	def PressureOrTemperature(self) -> float:
		'''
		Mechanical => Pressure: Units: English = psi | Standard = MPa.
		Thermal => Temperature: Units: English = °F | Standard = °C.
		'''
		return self._Entity.PressureOrTemperature

	@property
	def LimitFactor(self) -> float:
		return self._Entity.LimitFactor

	@property
	def UltimateFactor(self) -> float:
		return self._Entity.UltimateFactor

	@ReferenceTemperature.setter
	def ReferenceTemperature(self, value: float) -> None:
		self._Entity.ReferenceTemperature = value

	@PressureOrTemperature.setter
	def PressureOrTemperature(self, value: float) -> None:
		self._Entity.PressureOrTemperature = value

	@LimitFactor.setter
	def LimitFactor(self, value: float) -> None:
		self._Entity.LimitFactor = value

	@UltimateFactor.setter
	def UltimateFactor(self, value: float) -> None:
		self._Entity.UltimateFactor = value


class LoadPropertyUserBeamRow(LoadPropertyUserRow):
	def __init__(self, loadPropertyUserBeamRow: _api.LoadPropertyUserBeamRow):
		self._Entity = loadPropertyUserBeamRow

	@property
	def M1A(self) -> float:
		'''
		Units: English = lb*in | Standard = N*mm.
		'''
		return self._Entity.M1A

	@property
	def M2A(self) -> float:
		'''
		Units: English = lb*in | Standard = N*mm.
		'''
		return self._Entity.M2A

	@property
	def M1B(self) -> float:
		'''
		Units: English = lb*in | Standard = N*mm.
		'''
		return self._Entity.M1B

	@property
	def M2B(self) -> float:
		'''
		Units: English = lb*in | Standard = N*mm.
		'''
		return self._Entity.M2B

	@property
	def V1(self) -> float:
		'''
		Units: English = lb | Standard = N.
		'''
		return self._Entity.V1

	@property
	def V2(self) -> float:
		'''
		Units: English = lb | Standard = N.
		'''
		return self._Entity.V2

	@property
	def Axial(self) -> float:
		'''
		Units: English = lb | Standard = N.
		'''
		return self._Entity.Axial

	@property
	def Torque(self) -> float:
		'''
		Units: English = lb*in | Standard = N*mm.
		'''
		return self._Entity.Torque

	@M1A.setter
	def M1A(self, value: float) -> None:
		self._Entity.M1A = value

	@M2A.setter
	def M2A(self, value: float) -> None:
		self._Entity.M2A = value

	@M1B.setter
	def M1B(self, value: float) -> None:
		self._Entity.M1B = value

	@M2B.setter
	def M2B(self, value: float) -> None:
		self._Entity.M2B = value

	@V1.setter
	def V1(self, value: float) -> None:
		self._Entity.V1 = value

	@V2.setter
	def V2(self, value: float) -> None:
		self._Entity.V2 = value

	@Axial.setter
	def Axial(self, value: float) -> None:
		self._Entity.Axial = value

	@Torque.setter
	def Torque(self, value: float) -> None:
		self._Entity.Torque = value


class LoadPropertyUserFeaBeamRow(LoadPropertyUserBeamRow):
	def __init__(self, loadPropertyUserFeaBeamRow: _api.LoadPropertyUserFeaBeamRow):
		self._Entity = loadPropertyUserFeaBeamRow

	def SetName(self, name: str) -> None:
		'''
		Set the name for the scenario
		'''
		return self._Entity.SetName(name)


class LoadPropertyUserFeaBeamRowBulkUpdater(LoadPropertyUserRowBulkUpdater):
	def __init__(self, loadPropertyUserFeaBeamRowBulkUpdater: _api.LoadPropertyUserFeaBeamRowBulkUpdater):
		self._Entity = loadPropertyUserFeaBeamRowBulkUpdater

	@staticmethod
	def GetBulkUpdater(application: Application, items: tuple[LoadPropertyUserFeaBeamRow]) -> LoadPropertyUserFeaBeamRowBulkUpdater:
		itemsList = List[_api.LoadPropertyUserFeaBeamRow]()
		if items is not None:
			for x in items:
				if x is not None:
					itemsList.Add(x._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return LoadPropertyUserFeaBeamRowBulkUpdater(_api.LoadPropertyUserFeaBeamRowBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class LoadPropertyUserPanelJointRow(LoadPropertyUserRow):
	def __init__(self, loadPropertyUserPanelJointRow: _api.LoadPropertyUserPanelJointRow):
		self._Entity = loadPropertyUserPanelJointRow

	@property
	def Nx(self) -> float:
		'''
		Units: English = lb/in | Standard = N/mm.
		'''
		return self._Entity.Nx

	@property
	def Ny(self) -> float:
		'''
		Units: English = lb/in | Standard = N/mm.
		'''
		return self._Entity.Ny

	@property
	def Nxy(self) -> float:
		'''
		Units: English = lb/in | Standard = N/mm.
		'''
		return self._Entity.Nxy

	@property
	def Mx(self) -> float:
		'''
		Units: English = lb*in/in | Standard = N*mm/mm.
		'''
		return self._Entity.Mx

	@property
	def My(self) -> float:
		'''
		Units: English = lb*in/in | Standard = N*mm/mm.
		'''
		return self._Entity.My

	@property
	def Mxy(self) -> float:
		'''
		Units: English = lb*in/in | Standard = N*mm/mm.
		'''
		return self._Entity.Mxy

	@property
	def Qx(self) -> float:
		'''
		Units: English = lb/in | Standard = N/mm.
		'''
		return self._Entity.Qx

	@property
	def Qy(self) -> float:
		'''
		Units: English = lb/in | Standard = N/mm.
		'''
		return self._Entity.Qy

	@Nx.setter
	def Nx(self, value: float) -> None:
		self._Entity.Nx = value

	@Ny.setter
	def Ny(self, value: float) -> None:
		self._Entity.Ny = value

	@Nxy.setter
	def Nxy(self, value: float) -> None:
		self._Entity.Nxy = value

	@Mx.setter
	def Mx(self, value: float) -> None:
		self._Entity.Mx = value

	@My.setter
	def My(self, value: float) -> None:
		self._Entity.My = value

	@Mxy.setter
	def Mxy(self, value: float) -> None:
		self._Entity.Mxy = value

	@Qx.setter
	def Qx(self, value: float) -> None:
		self._Entity.Qx = value

	@Qy.setter
	def Qy(self, value: float) -> None:
		self._Entity.Qy = value


class LoadPropertyUserFeaJointRow(LoadPropertyUserPanelJointRow):
	def __init__(self, loadPropertyUserFeaJointRow: _api.LoadPropertyUserFeaJointRow):
		self._Entity = loadPropertyUserFeaJointRow

	def SetName(self, name: str) -> None:
		'''
		Set the name for the scenario
		'''
		return self._Entity.SetName(name)


class LoadPropertyUserFeaJointRowBulkUpdater(LoadPropertyUserRowBulkUpdater):
	def __init__(self, loadPropertyUserFeaJointRowBulkUpdater: _api.LoadPropertyUserFeaJointRowBulkUpdater):
		self._Entity = loadPropertyUserFeaJointRowBulkUpdater

	@staticmethod
	def GetBulkUpdater(application: Application, items: tuple[LoadPropertyUserFeaJointRow]) -> LoadPropertyUserFeaJointRowBulkUpdater:
		itemsList = List[_api.LoadPropertyUserFeaJointRow]()
		if items is not None:
			for x in items:
				if x is not None:
					itemsList.Add(x._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return LoadPropertyUserFeaJointRowBulkUpdater(_api.LoadPropertyUserFeaJointRowBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class LoadPropertyUserFeaPanelRow(LoadPropertyUserPanelJointRow):
	def __init__(self, loadPropertyUserFeaPanelRow: _api.LoadPropertyUserFeaPanelRow):
		self._Entity = loadPropertyUserFeaPanelRow

	def SetName(self, name: str) -> None:
		'''
		Set the name for the scenario
		'''
		return self._Entity.SetName(name)


class LoadPropertyUserFeaPanelRowBulkUpdater(LoadPropertyUserRowBulkUpdater):
	def __init__(self, loadPropertyUserFeaPanelRowBulkUpdater: _api.LoadPropertyUserFeaPanelRowBulkUpdater):
		self._Entity = loadPropertyUserFeaPanelRowBulkUpdater

	@staticmethod
	def GetBulkUpdater(application: Application, items: tuple[LoadPropertyUserFeaPanelRow]) -> LoadPropertyUserFeaPanelRowBulkUpdater:
		itemsList = List[_api.LoadPropertyUserFeaPanelRow]()
		if items is not None:
			for x in items:
				if x is not None:
					itemsList.Add(x._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return LoadPropertyUserFeaPanelRowBulkUpdater(_api.LoadPropertyUserFeaPanelRowBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class LoadPropertyUserGeneralBeamRow(LoadPropertyUserBeamRow):
	def __init__(self, loadPropertyUserGeneralBeamRow: _api.LoadPropertyUserGeneralBeamRow):
		self._Entity = loadPropertyUserGeneralBeamRow

	@property
	def M1A(self) -> float:
		'''
		Moment Units: English = lb*in | Standard = N*mm.
		Curvature Units: English = 1/in | Standard = 1/mm.
		'''
		return self._Entity.M1A

	@property
	def M2A(self) -> float:
		'''
		Moment Units: English = lb*in | Standard = N*mm.
		Curvature Units: English = 1/in | Standard = 1/mm.
		'''
		return self._Entity.M2A

	@property
	def M1B(self) -> float:
		'''
		Moment Units: English = lb*in | Standard = N*mm.
		Curvature Units: English = 1/in | Standard = 1/mm.
		'''
		return self._Entity.M1B

	@property
	def M2B(self) -> float:
		'''
		Moment Units: English = lb*in | Standard = N*mm.
		Curvature Units: English = 1/in | Standard = 1/mm.
		'''
		return self._Entity.M2B

	@property
	def V1(self) -> float:
		'''
		Shear Units: English = lb | Standard = N.
		'''
		return self._Entity.V1

	@property
	def V2(self) -> float:
		'''
		Shear Units: English = lb | Standard = N.
		'''
		return self._Entity.V2

	@property
	def Axial(self) -> float:
		'''
		Axial Units: English = lb | Standard = N.
		Strain Units: English = µin/in | Standard = µm/m.
		'''
		return self._Entity.Axial

	@property
	def Torque(self) -> float:
		'''
		Torque Units: English = lb*in | Standard = N*mm.
		'''
		return self._Entity.Torque

	@property
	def M1AType(self) -> types.BoundaryConditionType:
		'''
		Force => M1A | Displacement => κ1A | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.M1AType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def M2AType(self) -> types.BoundaryConditionType:
		'''
		Force => M2A | Displacement => κ2A | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.M2AType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def M1BType(self) -> types.BoundaryConditionType:
		'''
		Force => M1B | Displacement => κ1B | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.M1BType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def M2BType(self) -> types.BoundaryConditionType:
		'''
		Force => M2B | Displacement => κ2B | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.M2BType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def V1Type(self) -> types.BoundaryConditionType:
		'''
		Force => V1 | Free => Free.
		'''
		result = self._Entity.V1Type
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def V2Type(self) -> types.BoundaryConditionType:
		'''
		Force => V2 | Free => Free.
		'''
		result = self._Entity.V2Type
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def AxialType(self) -> types.BoundaryConditionType:
		'''
		Force => Axial | Displacement => ε | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.AxialType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def TorqueType(self) -> types.BoundaryConditionType:
		'''
		Force => Torque | Displacement => φ | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.TorqueType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@M1A.setter
	def M1A(self, value: float) -> None:
		self._Entity.M1A = value

	@M2A.setter
	def M2A(self, value: float) -> None:
		self._Entity.M2A = value

	@M1B.setter
	def M1B(self, value: float) -> None:
		self._Entity.M1B = value

	@M2B.setter
	def M2B(self, value: float) -> None:
		self._Entity.M2B = value

	@V1.setter
	def V1(self, value: float) -> None:
		self._Entity.V1 = value

	@V2.setter
	def V2(self, value: float) -> None:
		self._Entity.V2 = value

	@Axial.setter
	def Axial(self, value: float) -> None:
		self._Entity.Axial = value

	@Torque.setter
	def Torque(self, value: float) -> None:
		self._Entity.Torque = value


class LoadPropertyUserGeneralBeamRowBulkUpdater(LoadPropertyUserRowBulkUpdater):
	def __init__(self, loadPropertyUserGeneralBeamRowBulkUpdater: _api.LoadPropertyUserGeneralBeamRowBulkUpdater):
		self._Entity = loadPropertyUserGeneralBeamRowBulkUpdater

	@staticmethod
	def GetBulkUpdater(application: Application, items: tuple[LoadPropertyUserGeneralBeamRow]) -> LoadPropertyUserGeneralBeamRowBulkUpdater:
		itemsList = List[_api.LoadPropertyUserGeneralBeamRow]()
		if items is not None:
			for x in items:
				if x is not None:
					itemsList.Add(x._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return LoadPropertyUserGeneralBeamRowBulkUpdater(_api.LoadPropertyUserGeneralBeamRowBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class LoadPropertyUserGeneralPanelRow(LoadPropertyUserPanelJointRow):
	def __init__(self, loadPropertyUserGeneralPanelRow: _api.LoadPropertyUserGeneralPanelRow):
		self._Entity = loadPropertyUserGeneralPanelRow

	@property
	def Nx(self) -> float:
		'''
		Unit Force Units: English = lb/in | Standard = N/mm.
		Strain Units: English = µin/in | Standard = µm/m.
		'''
		return self._Entity.Nx

	@property
	def Ny(self) -> float:
		'''
		Unit Force Units: English = lb/in | Standard = N/mm.
		Strain Units: English = µin/in | Standard = µm/m.
		'''
		return self._Entity.Ny

	@property
	def Nxy(self) -> float:
		'''
		Unit Force Units: English = lb/in | Standard = N/mm.
		Strain Units: English = µin/in | Standard = µm/m.
		'''
		return self._Entity.Nxy

	@property
	def Mx(self) -> float:
		'''
		Moment Units: English = lb*in | Standard = N*mm.
		Curvature Units: English = 1/in | Standard = 1/mm.
		'''
		return self._Entity.Mx

	@property
	def My(self) -> float:
		'''
		Moment Units: English = lb*in | Standard = N*mm.
		Curvature Units: English = 1/in | Standard = 1/mm.
		'''
		return self._Entity.My

	@property
	def Mxy(self) -> float:
		'''
		Moment Units: English = lb*in | Standard = N*mm.
		Curvature Units: English = 1/in | Standard = 1/mm.
		'''
		return self._Entity.Mxy

	@property
	def Qx(self) -> float:
		'''
		Unit Force Units: English = lb/in | Standard = N/mm.
		'''
		return self._Entity.Qx

	@property
	def Qy(self) -> float:
		'''
		Unit Force Units: English = lb/in | Standard = N/mm.
		'''
		return self._Entity.Qy

	@property
	def NxType(self) -> types.BoundaryConditionType:
		'''
		Force => Nx | Displacement => εx | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.NxType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def NyType(self) -> types.BoundaryConditionType:
		'''
		Force => Ny | Displacement => εy | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.NyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def NxyType(self) -> types.BoundaryConditionType:
		'''
		Force => Nxy | Displacement => τxy | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.NxyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MxType(self) -> types.BoundaryConditionType:
		'''
		Force => Mx | Displacement => κx | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.MxType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MyType(self) -> types.BoundaryConditionType:
		'''
		Force => My | Displacement => κy | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.MyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MxyType(self) -> types.BoundaryConditionType:
		'''
		Force => Mxy | Displacement => γxy | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.MxyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def QxType(self) -> types.BoundaryConditionType:
		'''
		Force => Qx | Free => Free.
		'''
		result = self._Entity.QxType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def QyType(self) -> types.BoundaryConditionType:
		'''
		Force => Qy | Free => Free.
		'''
		result = self._Entity.QyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@Nx.setter
	def Nx(self, value: float) -> None:
		self._Entity.Nx = value

	@Ny.setter
	def Ny(self, value: float) -> None:
		self._Entity.Ny = value

	@Nxy.setter
	def Nxy(self, value: float) -> None:
		self._Entity.Nxy = value

	@Mx.setter
	def Mx(self, value: float) -> None:
		self._Entity.Mx = value

	@My.setter
	def My(self, value: float) -> None:
		self._Entity.My = value

	@Mxy.setter
	def Mxy(self, value: float) -> None:
		self._Entity.Mxy = value

	@Qx.setter
	def Qx(self, value: float) -> None:
		self._Entity.Qx = value

	@Qy.setter
	def Qy(self, value: float) -> None:
		self._Entity.Qy = value


class LoadPropertyUserGeneralPanelRowBulkUpdater(LoadPropertyUserRowBulkUpdater):
	def __init__(self, loadPropertyUserGeneralPanelRowBulkUpdater: _api.LoadPropertyUserGeneralPanelRowBulkUpdater):
		self._Entity = loadPropertyUserGeneralPanelRowBulkUpdater

	@staticmethod
	def GetBulkUpdater(application: Application, items: tuple[LoadPropertyUserGeneralPanelRow]) -> LoadPropertyUserGeneralPanelRowBulkUpdater:
		itemsList = List[_api.LoadPropertyUserGeneralPanelRow]()
		if items is not None:
			for x in items:
				if x is not None:
					itemsList.Add(x._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return LoadPropertyUserGeneralPanelRowBulkUpdater(_api.LoadPropertyUserGeneralPanelRowBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class LoadPropertyFea(LoadProperty):
	def __init__(self, loadPropertyFea: _api.LoadPropertyFea):
		self._Entity = loadPropertyFea

	@property
	def HasNx(self) -> bool:
		return self._Entity.HasNx

	@property
	def HasNy(self) -> bool:
		return self._Entity.HasNy

	@property
	def HasNxy(self) -> bool:
		return self._Entity.HasNxy

	@property
	def HasMx(self) -> bool:
		return self._Entity.HasMx

	@property
	def HasMy(self) -> bool:
		return self._Entity.HasMy

	@property
	def HasMxy(self) -> bool:
		return self._Entity.HasMxy

	@property
	def HasQx(self) -> bool:
		return self._Entity.HasQx

	@property
	def HasQy(self) -> bool:
		return self._Entity.HasQy

	@property
	def HasM1a(self) -> bool:
		return self._Entity.HasM1a

	@property
	def HasM1b(self) -> bool:
		return self._Entity.HasM1b

	@property
	def M2a(self) -> bool:
		warnings.warn("Prefer HasM2a", DeprecationWarning, 2)
		return self._Entity.M2a

	@property
	def HasM2a(self) -> bool:
		return self._Entity.HasM2a

	@property
	def HasM2b(self) -> bool:
		return self._Entity.HasM2b

	@property
	def V1(self) -> bool:
		warnings.warn("Prefer HasV1", DeprecationWarning, 2)
		return self._Entity.V1

	@property
	def HasV1(self) -> bool:
		return self._Entity.HasV1

	@property
	def V2(self) -> bool:
		warnings.warn("Prefer HasV2", DeprecationWarning, 2)
		return self._Entity.V2

	@property
	def HasV2(self) -> bool:
		return self._Entity.HasV2

	@property
	def Axial(self) -> bool:
		warnings.warn("Prefer HasAxial", DeprecationWarning, 2)
		return self._Entity.Axial

	@property
	def HasAxial(self) -> bool:
		return self._Entity.HasAxial

	@property
	def Torque(self) -> bool:
		warnings.warn("Prefer HasTorque", DeprecationWarning, 2)
		return self._Entity.Torque

	@property
	def HasTorque(self) -> bool:
		return self._Entity.HasTorque

	@property
	def Tension(self) -> bool:
		return self._Entity.Tension

	@property
	def Shear(self) -> bool:
		return self._Entity.Shear

	@property
	def Moment(self) -> bool:
		return self._Entity.Moment

	@HasNx.setter
	def HasNx(self, value: bool) -> None:
		self._Entity.HasNx = value

	@HasNy.setter
	def HasNy(self, value: bool) -> None:
		self._Entity.HasNy = value

	@HasNxy.setter
	def HasNxy(self, value: bool) -> None:
		self._Entity.HasNxy = value

	@HasMx.setter
	def HasMx(self, value: bool) -> None:
		self._Entity.HasMx = value

	@HasMy.setter
	def HasMy(self, value: bool) -> None:
		self._Entity.HasMy = value

	@HasMxy.setter
	def HasMxy(self, value: bool) -> None:
		self._Entity.HasMxy = value

	@HasQx.setter
	def HasQx(self, value: bool) -> None:
		self._Entity.HasQx = value

	@HasQy.setter
	def HasQy(self, value: bool) -> None:
		self._Entity.HasQy = value

	@HasM1a.setter
	def HasM1a(self, value: bool) -> None:
		self._Entity.HasM1a = value

	@HasM1b.setter
	def HasM1b(self, value: bool) -> None:
		self._Entity.HasM1b = value

	@M2a.setter
	def M2a(self, value: bool) -> None:
		self._Entity.M2a = value

	@HasM2a.setter
	def HasM2a(self, value: bool) -> None:
		self._Entity.HasM2a = value

	@HasM2b.setter
	def HasM2b(self, value: bool) -> None:
		self._Entity.HasM2b = value

	@V1.setter
	def V1(self, value: bool) -> None:
		self._Entity.V1 = value

	@HasV1.setter
	def HasV1(self, value: bool) -> None:
		self._Entity.HasV1 = value

	@V2.setter
	def V2(self, value: bool) -> None:
		self._Entity.V2 = value

	@HasV2.setter
	def HasV2(self, value: bool) -> None:
		self._Entity.HasV2 = value

	@Axial.setter
	def Axial(self, value: bool) -> None:
		self._Entity.Axial = value

	@HasAxial.setter
	def HasAxial(self, value: bool) -> None:
		self._Entity.HasAxial = value

	@Torque.setter
	def Torque(self, value: bool) -> None:
		self._Entity.Torque = value

	@HasTorque.setter
	def HasTorque(self, value: bool) -> None:
		self._Entity.HasTorque = value

	@Tension.setter
	def Tension(self, value: bool) -> None:
		self._Entity.Tension = value

	@Shear.setter
	def Shear(self, value: bool) -> None:
		self._Entity.Shear = value

	@Moment.setter
	def Moment(self, value: bool) -> None:
		self._Entity.Moment = value


class LoadPropertyAverage(LoadPropertyFea):
	def __init__(self, loadPropertyAverage: _api.LoadPropertyAverage):
		self._Entity = loadPropertyAverage

	@property
	def ElementType(self) -> types.LoadPropertyAverageElementType:
		result = self._Entity.ElementType
		return types.LoadPropertyAverageElementType[result.ToString()] if result is not None else None

	@ElementType.setter
	def ElementType(self, value: types.LoadPropertyAverageElementType) -> None:
		self._Entity.ElementType = _types.LoadPropertyAverageElementType(types.GetEnumValue(value.value))


class LoadPropertyElementBased(LoadPropertyFea):
	def __init__(self, loadPropertyElementBased: _api.LoadPropertyElementBased):
		self._Entity = loadPropertyElementBased


class LoadPropertyNeighborAverage(LoadPropertyFea):
	def __init__(self, loadPropertyNeighborAverage: _api.LoadPropertyNeighborAverage):
		self._Entity = loadPropertyNeighborAverage

	@property
	def NumberOfNeighborsPerSide(self) -> int:
		return self._Entity.NumberOfNeighborsPerSide

	@NumberOfNeighborsPerSide.setter
	def NumberOfNeighborsPerSide(self, value: int) -> None:
		self._Entity.NumberOfNeighborsPerSide = value


class LoadPropertyPeakLoad(LoadPropertyFea):
	def __init__(self, loadPropertyPeakLoad: _api.LoadPropertyPeakLoad):
		self._Entity = loadPropertyPeakLoad

	@property
	def ElementScope(self) -> types.LoadPropertyPeakElementScope:
		result = self._Entity.ElementScope
		return types.LoadPropertyPeakElementScope[result.ToString()] if result is not None else None

	@ElementScope.setter
	def ElementScope(self, value: types.LoadPropertyPeakElementScope) -> None:
		self._Entity.ElementScope = _types.LoadPropertyPeakElementScope(types.GetEnumValue(value.value))


class LoadPropertyStatistical(LoadPropertyFea):
	def __init__(self, loadPropertyStatistical: _api.LoadPropertyStatistical):
		self._Entity = loadPropertyStatistical

	@property
	def NSigma(self) -> int:
		return self._Entity.NSigma

	@NSigma.setter
	def NSigma(self, value: int) -> None:
		self._Entity.NSigma = value


class LoadPropertyUserFeaRowCol(IdNameEntityCol, Generic[T]):
	def __init__(self, loadPropertyUserFeaRowCol: _api.LoadPropertyUserFeaRowCol):
		self._Entity = loadPropertyUserFeaRowCol
		self._CollectedClass = T

	def AddScenario(self, name: str = None) -> LoadPropertyUserRow:
		'''
		Adds a load scenario with default values.
		'''
		return self._Entity.AddScenario(name)

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool:
		'''
		Delete a load scenario by id.
		'''
		...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool:
		'''
		Delete a load scenario by name.
		'''
		...

	@overload
	def Get(self, name: str) -> LoadPropertyUserRow:
		...

	@overload
	def Get(self, id: int) -> LoadPropertyUserRow:
		...

	def DeleteScenario(self, item1 = None) -> bool:
		'''
		Overload 1: ``DeleteScenario(self, scenarioId: int) -> bool``

		Delete a load scenario by id.

		Overload 2: ``DeleteScenario(self, scenarioName: str) -> bool``

		Delete a load scenario by name.
		'''
		if isinstance(item1, int):
			return self._Entity.DeleteScenario(item1)

		if isinstance(item1, str):
			return self._Entity.DeleteScenario(item1)

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserRow:
		'''
		Overload 1: ``Get(self, name: str) -> LoadPropertyUserRow``

		Overload 2: ``Get(self, id: int) -> LoadPropertyUserRow``
		'''
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

		return self._Entity.Get(item1)


class LoadPropertyUserFeaBeamRowCol(LoadPropertyUserFeaRowCol[LoadPropertyUserFeaBeamRow]):
	def __init__(self, loadPropertyUserFeaBeamRowCol: _api.LoadPropertyUserFeaBeamRowCol):
		self._Entity = loadPropertyUserFeaBeamRowCol
		self._CollectedClass = LoadPropertyUserFeaBeamRow

	@property
	def LoadPropertyUserFeaBeamRowColList(self) -> tuple[LoadPropertyUserFeaBeamRow]:
		return tuple([LoadPropertyUserFeaBeamRow(loadPropertyUserFeaBeamRowCol) for loadPropertyUserFeaBeamRowCol in self._Entity])

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool:
		...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool:
		...

	@overload
	def Get(self, name: str) -> LoadPropertyUserFeaBeamRow:
		...

	@overload
	def Get(self, id: int) -> LoadPropertyUserFeaBeamRow:
		...

	def DeleteScenario(self, item1 = None) -> bool:
		'''
		Overload 1: ``DeleteScenario(self, scenarioId: int) -> bool``

		Overload 2: ``DeleteScenario(self, scenarioName: str) -> bool``
		'''
		if isinstance(item1, int):
			return bool(super().DeleteScenario(item1))

		if isinstance(item1, str):
			return bool(super().DeleteScenario(item1))

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserFeaBeamRow:
		'''
		Overload 1: ``Get(self, name: str) -> LoadPropertyUserFeaBeamRow``

		Overload 2: ``Get(self, id: int) -> LoadPropertyUserFeaBeamRow``
		'''
		if isinstance(item1, str):
			return LoadPropertyUserFeaBeamRow(super().Get(item1))

		if isinstance(item1, int):
			return LoadPropertyUserFeaBeamRow(super().Get(item1))

		return LoadPropertyUserFeaBeamRow(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.LoadPropertyUserFeaBeamRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserFeaBeamRowColList

	def __len__(self):
		return len(self.LoadPropertyUserFeaBeamRowColList)


class LoadPropertyUserFeaBeam(LoadProperty):
	def __init__(self, loadPropertyUserFeaBeam: _api.LoadPropertyUserFeaBeam):
		self._Entity = loadPropertyUserFeaBeam

	@property
	def UserFeaRows(self) -> LoadPropertyUserFeaBeamRowCol:
		'''
		Load property row data
		'''
		result = self._Entity.UserFeaRows
		return LoadPropertyUserFeaBeamRowCol(result) if result is not None else None


class LoadPropertyUserFeaJointRowCol(LoadPropertyUserFeaRowCol[LoadPropertyUserFeaJointRow]):
	def __init__(self, loadPropertyUserFeaJointRowCol: _api.LoadPropertyUserFeaJointRowCol):
		self._Entity = loadPropertyUserFeaJointRowCol
		self._CollectedClass = LoadPropertyUserFeaJointRow

	@property
	def LoadPropertyUserFeaJointRowColList(self) -> tuple[LoadPropertyUserFeaJointRow]:
		return tuple([LoadPropertyUserFeaJointRow(loadPropertyUserFeaJointRowCol) for loadPropertyUserFeaJointRowCol in self._Entity])

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool:
		...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool:
		...

	@overload
	def Get(self, name: str) -> LoadPropertyUserFeaJointRow:
		...

	@overload
	def Get(self, id: int) -> LoadPropertyUserFeaJointRow:
		...

	def DeleteScenario(self, item1 = None) -> bool:
		'''
		Overload 1: ``DeleteScenario(self, scenarioId: int) -> bool``

		Overload 2: ``DeleteScenario(self, scenarioName: str) -> bool``
		'''
		if isinstance(item1, int):
			return bool(super().DeleteScenario(item1))

		if isinstance(item1, str):
			return bool(super().DeleteScenario(item1))

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserFeaJointRow:
		'''
		Overload 1: ``Get(self, name: str) -> LoadPropertyUserFeaJointRow``

		Overload 2: ``Get(self, id: int) -> LoadPropertyUserFeaJointRow``
		'''
		if isinstance(item1, str):
			return LoadPropertyUserFeaJointRow(super().Get(item1))

		if isinstance(item1, int):
			return LoadPropertyUserFeaJointRow(super().Get(item1))

		return LoadPropertyUserFeaJointRow(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.LoadPropertyUserFeaJointRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserFeaJointRowColList

	def __len__(self):
		return len(self.LoadPropertyUserFeaJointRowColList)


class LoadPropertyUserFeaJoint(LoadProperty):
	def __init__(self, loadPropertyUserFeaJoint: _api.LoadPropertyUserFeaJoint):
		self._Entity = loadPropertyUserFeaJoint

	@property
	def UserFeaRows(self) -> LoadPropertyUserFeaJointRowCol:
		'''
		Load property row data
		'''
		result = self._Entity.UserFeaRows
		return LoadPropertyUserFeaJointRowCol(result) if result is not None else None


class LoadPropertyUserFeaPanelRowCol(LoadPropertyUserFeaRowCol[LoadPropertyUserFeaPanelRow]):
	def __init__(self, loadPropertyUserFeaPanelRowCol: _api.LoadPropertyUserFeaPanelRowCol):
		self._Entity = loadPropertyUserFeaPanelRowCol
		self._CollectedClass = LoadPropertyUserFeaPanelRow

	@property
	def LoadPropertyUserFeaPanelRowColList(self) -> tuple[LoadPropertyUserFeaPanelRow]:
		return tuple([LoadPropertyUserFeaPanelRow(loadPropertyUserFeaPanelRowCol) for loadPropertyUserFeaPanelRowCol in self._Entity])

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool:
		...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool:
		...

	@overload
	def Get(self, name: str) -> LoadPropertyUserFeaPanelRow:
		...

	@overload
	def Get(self, id: int) -> LoadPropertyUserFeaPanelRow:
		...

	def DeleteScenario(self, item1 = None) -> bool:
		'''
		Overload 1: ``DeleteScenario(self, scenarioId: int) -> bool``

		Overload 2: ``DeleteScenario(self, scenarioName: str) -> bool``
		'''
		if isinstance(item1, int):
			return bool(super().DeleteScenario(item1))

		if isinstance(item1, str):
			return bool(super().DeleteScenario(item1))

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserFeaPanelRow:
		'''
		Overload 1: ``Get(self, name: str) -> LoadPropertyUserFeaPanelRow``

		Overload 2: ``Get(self, id: int) -> LoadPropertyUserFeaPanelRow``
		'''
		if isinstance(item1, str):
			return LoadPropertyUserFeaPanelRow(super().Get(item1))

		if isinstance(item1, int):
			return LoadPropertyUserFeaPanelRow(super().Get(item1))

		return LoadPropertyUserFeaPanelRow(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.LoadPropertyUserFeaPanelRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserFeaPanelRowColList

	def __len__(self):
		return len(self.LoadPropertyUserFeaPanelRowColList)


class LoadPropertyUserFeaPanel(LoadProperty):
	def __init__(self, loadPropertyUserFeaPanel: _api.LoadPropertyUserFeaPanel):
		self._Entity = loadPropertyUserFeaPanel

	@property
	def UserFeaRows(self) -> LoadPropertyUserFeaPanelRowCol:
		'''
		Load property row data
		'''
		result = self._Entity.UserFeaRows
		return LoadPropertyUserFeaPanelRowCol(result) if result is not None else None

	def SetIsZeroCurvature(self, isZeroCurvature: bool) -> None:
		'''
		Is there an enum for this?
		'''
		return self._Entity.SetIsZeroCurvature(isZeroCurvature)


class LoadPropertyUserGeneralDoubleRow(IdNameEntity):
	def __init__(self, loadPropertyUserGeneralDoubleRow: _api.LoadPropertyUserGeneralDoubleRow):
		self._Entity = loadPropertyUserGeneralDoubleRow

	@property
	def MechanicalRow(self) -> LoadPropertyUserRow:
		result = self._Entity.MechanicalRow
		thisClass = type(result).__name__
		givenClass = LoadPropertyUserRow
		for subclass in _all_subclasses(LoadPropertyUserRow):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@property
	def ThermalRow(self) -> LoadPropertyUserRow:
		result = self._Entity.ThermalRow
		thisClass = type(result).__name__
		givenClass = LoadPropertyUserRow
		for subclass in _all_subclasses(LoadPropertyUserRow):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def SetName(self, name: str) -> None:
		'''
		Update name for the scenario
		'''
		return self._Entity.SetName(name)


class LoadPropertyUserGeneralBeamDoubleRow(LoadPropertyUserGeneralDoubleRow):
	def __init__(self, loadPropertyUserGeneralBeamDoubleRow: _api.LoadPropertyUserGeneralBeamDoubleRow):
		self._Entity = loadPropertyUserGeneralBeamDoubleRow

	@property
	def MechanicalRow(self) -> LoadPropertyUserRow:
		result = self._Entity.MechanicalRow
		thisClass = type(result).__name__
		givenClass = LoadPropertyUserRow
		for subclass in _all_subclasses(LoadPropertyUserRow):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@property
	def ThermalRow(self) -> LoadPropertyUserRow:
		result = self._Entity.ThermalRow
		thisClass = type(result).__name__
		givenClass = LoadPropertyUserRow
		for subclass in _all_subclasses(LoadPropertyUserRow):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@property
	def M1AType(self) -> types.BoundaryConditionType:
		result = self._Entity.M1AType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def M2AType(self) -> types.BoundaryConditionType:
		result = self._Entity.M2AType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def M1BType(self) -> types.BoundaryConditionType:
		result = self._Entity.M1BType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def M2BType(self) -> types.BoundaryConditionType:
		result = self._Entity.M2BType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def V1Type(self) -> types.BoundaryConditionType:
		result = self._Entity.V1Type
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def V2Type(self) -> types.BoundaryConditionType:
		result = self._Entity.V2Type
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def AxialType(self) -> types.BoundaryConditionType:
		result = self._Entity.AxialType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def TorqueType(self) -> types.BoundaryConditionType:
		result = self._Entity.TorqueType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	def SetM1AType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set M1A type for the scenario
		'''
		return self._Entity.SetM1AType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetM2AType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set M2A type for the scenario
		'''
		return self._Entity.SetM2AType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetM1BType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set M1B type for the scenario
		'''
		return self._Entity.SetM1BType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetM2BType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set M2B type for the scenario
		'''
		return self._Entity.SetM2BType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetV1Type(self, type: types.BoundaryConditionType) -> None:
		'''
		Set V1 type for the scenario
		'''
		return self._Entity.SetV1Type(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetV2Type(self, type: types.BoundaryConditionType) -> None:
		'''
		Set V2 type for the scenario
		'''
		return self._Entity.SetV2Type(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetAxialType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Axial type for the scenario
		'''
		return self._Entity.SetAxialType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetTorqueType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set torque type for the scenario
		'''
		return self._Entity.SetTorqueType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))


class LoadPropertyUserGeneralRowCol(IdNameEntityCol, Generic[T]):
	def __init__(self, loadPropertyUserGeneralRowCol: _api.LoadPropertyUserGeneralRowCol):
		self._Entity = loadPropertyUserGeneralRowCol
		self._CollectedClass = T

	def AddScenario(self, name: str = None) -> LoadPropertyUserGeneralDoubleRow:
		'''
		Add scenario.
		'''
		return self._Entity.AddScenario(name)

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool:
		'''
		Delete scenario by ID.
		'''
		...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool:
		'''
		Delete scenario by ID.
		'''
		...

	@overload
	def Get(self, name: str) -> LoadPropertyUserGeneralDoubleRow:
		...

	@overload
	def Get(self, id: int) -> LoadPropertyUserGeneralDoubleRow:
		...

	def DeleteScenario(self, item1 = None) -> bool:
		'''
		Overload 1: ``DeleteScenario(self, scenarioId: int) -> bool``

		Delete scenario by ID.

		Overload 2: ``DeleteScenario(self, scenarioName: str) -> bool``

		Delete scenario by ID.
		'''
		if isinstance(item1, int):
			return self._Entity.DeleteScenario(item1)

		if isinstance(item1, str):
			return self._Entity.DeleteScenario(item1)

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserGeneralDoubleRow:
		'''
		Overload 1: ``Get(self, name: str) -> LoadPropertyUserGeneralDoubleRow``

		Overload 2: ``Get(self, id: int) -> LoadPropertyUserGeneralDoubleRow``
		'''
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

		return self._Entity.Get(item1)


class LoadPropertyUserGeneralBeamRowCol(LoadPropertyUserGeneralRowCol[LoadPropertyUserGeneralBeamDoubleRow]):
	def __init__(self, loadPropertyUserGeneralBeamRowCol: _api.LoadPropertyUserGeneralBeamRowCol):
		self._Entity = loadPropertyUserGeneralBeamRowCol
		self._CollectedClass = LoadPropertyUserGeneralBeamDoubleRow

	@property
	def LoadPropertyUserGeneralBeamRowColList(self) -> tuple[LoadPropertyUserGeneralBeamDoubleRow]:
		return tuple([LoadPropertyUserGeneralBeamDoubleRow(loadPropertyUserGeneralBeamRowCol) for loadPropertyUserGeneralBeamRowCol in self._Entity])

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool:
		...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool:
		...

	@overload
	def Get(self, name: str) -> LoadPropertyUserGeneralBeamDoubleRow:
		...

	@overload
	def Get(self, id: int) -> LoadPropertyUserGeneralBeamDoubleRow:
		...

	def DeleteScenario(self, item1 = None) -> bool:
		'''
		Overload 1: ``DeleteScenario(self, scenarioId: int) -> bool``

		Overload 2: ``DeleteScenario(self, scenarioName: str) -> bool``
		'''
		if isinstance(item1, int):
			return bool(super().DeleteScenario(item1))

		if isinstance(item1, str):
			return bool(super().DeleteScenario(item1))

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserGeneralBeamDoubleRow:
		'''
		Overload 1: ``Get(self, name: str) -> LoadPropertyUserGeneralBeamDoubleRow``

		Overload 2: ``Get(self, id: int) -> LoadPropertyUserGeneralBeamDoubleRow``
		'''
		if isinstance(item1, str):
			return LoadPropertyUserGeneralBeamDoubleRow(super().Get(item1))

		if isinstance(item1, int):
			return LoadPropertyUserGeneralBeamDoubleRow(super().Get(item1))

		return LoadPropertyUserGeneralBeamDoubleRow(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.LoadPropertyUserGeneralBeamRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserGeneralBeamRowColList

	def __len__(self):
		return len(self.LoadPropertyUserGeneralBeamRowColList)


class LoadPropertyUserGeneralBeam(LoadProperty):
	def __init__(self, loadPropertyUserGeneralBeam: _api.LoadPropertyUserGeneralBeam):
		self._Entity = loadPropertyUserGeneralBeam

	@property
	def UserGeneralRows(self) -> LoadPropertyUserGeneralBeamRowCol:
		'''
		Load property row data
		'''
		result = self._Entity.UserGeneralRows
		return LoadPropertyUserGeneralBeamRowCol(result) if result is not None else None

	@property
	def IsIncludingThermal(self) -> bool:
		'''
		Bool indicating whether there is a row in each scenario for thermal loads.
		Setting adds a thermal row for every "double row" in the collection.
		To see this change on any rows, you must get the row from the collection again.
		'''
		return self._Entity.IsIncludingThermal

	@IsIncludingThermal.setter
	def IsIncludingThermal(self, value: bool) -> None:
		self._Entity.IsIncludingThermal = value


class LoadPropertyUserGeneralBoltedRow(IdEntity):
	def __init__(self, loadPropertyUserGeneralBoltedRow: _api.LoadPropertyUserGeneralBoltedRow):
		self._Entity = loadPropertyUserGeneralBoltedRow

	@property
	def LoadPropertyId(self) -> int:
		return self._Entity.LoadPropertyId

	@property
	def LoadScenarioId(self) -> int:
		return self._Entity.LoadScenarioId

	@property
	def Fx(self) -> float:
		'''
		Units: English = lb | Standard = N.
		'''
		return self._Entity.Fx

	@property
	def Fy(self) -> float:
		'''
		Units: English = lb | Standard = N.
		'''
		return self._Entity.Fy

	@property
	def Fz(self) -> float:
		'''
		Units: English = lb | Standard = N.
		'''
		return self._Entity.Fz

	@property
	def Mx(self) -> float:
		'''
		Units: English = lb*in | Standard = N*mm.
		'''
		return self._Entity.Mx

	@property
	def My(self) -> float:
		'''
		Units: English = lb*in | Standard = N*mm.
		'''
		return self._Entity.My

	@property
	def Mz(self) -> float:
		'''
		Units: English = lb*in | Standard = N*mm.
		'''
		return self._Entity.Mz

	@property
	def NxBypass(self) -> float:
		'''
		Units: English = lb/in | Standard = N/mm.
		'''
		return self._Entity.NxBypass

	@property
	def NyBypass(self) -> float:
		'''
		Units: English = lb/in | Standard = N/mm.
		'''
		return self._Entity.NyBypass

	@property
	def NxyBypass(self) -> float:
		'''
		Units: English = lb/in | Standard = N/mm.
		'''
		return self._Entity.NxyBypass

	@property
	def LimitFactor(self) -> float:
		return self._Entity.LimitFactor

	@property
	def UltimateFactor(self) -> float:
		return self._Entity.UltimateFactor

	@Fx.setter
	def Fx(self, value: float) -> None:
		self._Entity.Fx = value

	@Fy.setter
	def Fy(self, value: float) -> None:
		self._Entity.Fy = value

	@Fz.setter
	def Fz(self, value: float) -> None:
		self._Entity.Fz = value

	@Mx.setter
	def Mx(self, value: float) -> None:
		self._Entity.Mx = value

	@My.setter
	def My(self, value: float) -> None:
		self._Entity.My = value

	@Mz.setter
	def Mz(self, value: float) -> None:
		self._Entity.Mz = value

	@NxBypass.setter
	def NxBypass(self, value: float) -> None:
		self._Entity.NxBypass = value

	@NyBypass.setter
	def NyBypass(self, value: float) -> None:
		self._Entity.NyBypass = value

	@NxyBypass.setter
	def NxyBypass(self, value: float) -> None:
		self._Entity.NxyBypass = value

	@LimitFactor.setter
	def LimitFactor(self, value: float) -> None:
		self._Entity.LimitFactor = value

	@UltimateFactor.setter
	def UltimateFactor(self, value: float) -> None:
		self._Entity.UltimateFactor = value


class LoadPropertyUserGeneralBoltedRowCol(IdEntityCol[LoadPropertyUserGeneralBoltedRow]):
	def __init__(self, loadPropertyUserGeneralBoltedRowCol: _api.LoadPropertyUserGeneralBoltedRowCol):
		self._Entity = loadPropertyUserGeneralBoltedRowCol
		self._CollectedClass = LoadPropertyUserGeneralBoltedRow

	@property
	def LoadPropertyUserGeneralBoltedRowColList(self) -> tuple[LoadPropertyUserGeneralBoltedRow]:
		return tuple([LoadPropertyUserGeneralBoltedRow(loadPropertyUserGeneralBoltedRowCol) for loadPropertyUserGeneralBoltedRowCol in self._Entity])

	def AddScenario(self) -> None:
		'''
		Adds a load scenario with default values
		'''
		return self._Entity.AddScenario()

	def DeleteScenario(self, scenarioId: int) -> bool:
		'''
		Delete a load scenario by id
		'''
		return self._Entity.DeleteScenario(scenarioId)

	def __getitem__(self, index: int):
		return self.LoadPropertyUserGeneralBoltedRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserGeneralBoltedRowColList

	def __len__(self):
		return len(self.LoadPropertyUserGeneralBoltedRowColList)


class LoadPropertyUserGeneralBolted(LoadProperty):
	def __init__(self, loadPropertyUserGeneralBolted: _api.LoadPropertyUserGeneralBolted):
		self._Entity = loadPropertyUserGeneralBolted

	@property
	def UserGeneralBoltedRows(self) -> LoadPropertyUserGeneralBoltedRowCol:
		'''
		Load property row data
		'''
		result = self._Entity.UserGeneralBoltedRows
		return LoadPropertyUserGeneralBoltedRowCol(result) if result is not None else None


class LoadPropertyUserGeneralBondedRow(IdEntity):
	def __init__(self, loadPropertyUserGeneralBondedRow: _api.LoadPropertyUserGeneralBondedRow):
		self._Entity = loadPropertyUserGeneralBondedRow

	@property
	def LoadPropertyId(self) -> int:
		return self._Entity.LoadPropertyId

	@property
	def JointConceptId(self) -> types.JointConceptId:
		result = self._Entity.JointConceptId
		return types.JointConceptId[result.ToString()] if result is not None else None

	@property
	def BondedBcId(self) -> int:
		return self._Entity.BondedBcId

	@property
	def AxialType(self) -> types.BoundaryConditionType:
		'''
		Force => Ny | Displacement => v | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.AxialType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MomentType(self) -> types.BoundaryConditionType:
		'''
		Force => My | Displacement => β | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.MomentType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def TransverseType(self) -> types.BoundaryConditionType:
		'''
		Force => Qy | Displacement => w | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.TransverseType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def ShearType(self) -> types.BoundaryConditionType:
		'''
		Force => Nxy | Displacement => u | Free => Free | Fixed => Fixed.
		'''
		result = self._Entity.ShearType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def Axial(self) -> float:
		'''
		Unit Force Units: English = lb/in | Standard = N/mm.
		Length Units: English = in | Standard = mm.
		'''
		return self._Entity.Axial

	@property
	def Moment(self) -> float:
		'''
		Unit Moment Units: English = lb*in/in | Standard = N*mm/mm.
		'''
		return self._Entity.Moment

	@property
	def Transverse(self) -> float:
		'''
		Unit Force Units: English = lb/in | Standard = N/mm.
		Length Units: English = in | Standard = mm.
		'''
		return self._Entity.Transverse

	@property
	def Shear(self) -> float:
		'''
		Unit Force Units: English = lb/in | Standard = N/mm.
		Length Units: English = in | Standard = mm.
		'''
		return self._Entity.Shear

	@AxialType.setter
	def AxialType(self, value: types.BoundaryConditionType) -> None:
		self._Entity.AxialType = _types.BoundaryConditionType(types.GetEnumValue(value.value))

	@MomentType.setter
	def MomentType(self, value: types.BoundaryConditionType) -> None:
		self._Entity.MomentType = _types.BoundaryConditionType(types.GetEnumValue(value.value))

	@TransverseType.setter
	def TransverseType(self, value: types.BoundaryConditionType) -> None:
		self._Entity.TransverseType = _types.BoundaryConditionType(types.GetEnumValue(value.value))

	@ShearType.setter
	def ShearType(self, value: types.BoundaryConditionType) -> None:
		self._Entity.ShearType = _types.BoundaryConditionType(types.GetEnumValue(value.value))

	@Axial.setter
	def Axial(self, value: float) -> None:
		self._Entity.Axial = value

	@Moment.setter
	def Moment(self, value: float) -> None:
		self._Entity.Moment = value

	@Transverse.setter
	def Transverse(self, value: float) -> None:
		self._Entity.Transverse = value

	@Shear.setter
	def Shear(self, value: float) -> None:
		self._Entity.Shear = value

	def UpdateRow(self) -> None:
		return self._Entity.UpdateRow()


class LoadPropertyUserGeneralBondedRowCol(IdEntityCol[LoadPropertyUserGeneralBondedRow]):
	def __init__(self, loadPropertyUserGeneralBondedRowCol: _api.LoadPropertyUserGeneralBondedRowCol):
		self._Entity = loadPropertyUserGeneralBondedRowCol
		self._CollectedClass = LoadPropertyUserGeneralBondedRow

	@property
	def LoadPropertyUserGeneralBondedRowColList(self) -> tuple[LoadPropertyUserGeneralBondedRow]:
		return tuple([LoadPropertyUserGeneralBondedRow(loadPropertyUserGeneralBondedRowCol) for loadPropertyUserGeneralBondedRowCol in self._Entity])

	def __getitem__(self, index: int):
		return self.LoadPropertyUserGeneralBondedRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserGeneralBondedRowColList

	def __len__(self):
		return len(self.LoadPropertyUserGeneralBondedRowColList)


class LoadPropertyJoint(IdEntity):
	def __init__(self, loadPropertyJoint: _api.LoadPropertyJoint):
		self._Entity = loadPropertyJoint

	@property
	def UserGeneralBondedRows(self) -> LoadPropertyUserGeneralBondedRowCol:
		result = self._Entity.UserGeneralBondedRows
		return LoadPropertyUserGeneralBondedRowCol(result) if result is not None else None

	@property
	def LoadPropertyId(self) -> int:
		return self._Entity.LoadPropertyId

	@property
	def JConceptId(self) -> types.JointConceptId:
		'''
		Bonded joint concept; UserGeneralBondedRows will automatically be updated upon changing Joint Concept Id, so any data will be cleared
		'''
		result = self._Entity.JConceptId
		return types.JointConceptId[result.ToString()] if result is not None else None

	@property
	def Ex(self) -> float | None:
		return self._Entity.Ex

	@property
	def Kx(self) -> float | None:
		return self._Entity.Kx

	@property
	def Kxy(self) -> float | None:
		return self._Entity.Kxy

	@property
	def Temperature(self) -> float | None:
		return self._Entity.Temperature

	@JConceptId.setter
	def JConceptId(self, value: types.JointConceptId) -> None:
		self._Entity.JConceptId = _types.JointConceptId(types.GetEnumValue(value.value))

	@Ex.setter
	def Ex(self, value: float | None) -> None:
		self._Entity.Ex = value

	@Kx.setter
	def Kx(self, value: float | None) -> None:
		self._Entity.Kx = value

	@Kxy.setter
	def Kxy(self, value: float | None) -> None:
		self._Entity.Kxy = value

	@Temperature.setter
	def Temperature(self, value: float | None) -> None:
		self._Entity.Temperature = value


class LoadPropertyUserGeneralBonded(LoadProperty):

	_LoadPropertyJoint = LoadPropertyJoint
	def __init__(self, loadPropertyUserGeneralBonded: _api.LoadPropertyUserGeneralBonded):
		self._Entity = loadPropertyUserGeneralBonded
	@property
	def LoadPropertyJoint(self) -> _LoadPropertyJoint:
		'''
		Load Property Joint for UserBonded loads
		'''
		result = self._Entity.LoadPropertyJoint
		return LoadPropertyJoint(result) if result is not None else None


class LoadPropertyUserGeneralPanelDoubleRow(LoadPropertyUserGeneralDoubleRow):
	def __init__(self, loadPropertyUserGeneralPanelDoubleRow: _api.LoadPropertyUserGeneralPanelDoubleRow):
		self._Entity = loadPropertyUserGeneralPanelDoubleRow

	@property
	def MechanicalRow(self) -> LoadPropertyUserRow:
		result = self._Entity.MechanicalRow
		thisClass = type(result).__name__
		givenClass = LoadPropertyUserRow
		for subclass in _all_subclasses(LoadPropertyUserRow):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@property
	def ThermalRow(self) -> LoadPropertyUserRow:
		result = self._Entity.ThermalRow
		thisClass = type(result).__name__
		givenClass = LoadPropertyUserRow
		for subclass in _all_subclasses(LoadPropertyUserRow):
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@property
	def NxType(self) -> types.BoundaryConditionType:
		result = self._Entity.NxType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def NyType(self) -> types.BoundaryConditionType:
		result = self._Entity.NyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def NxyType(self) -> types.BoundaryConditionType:
		result = self._Entity.NxyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MxType(self) -> types.BoundaryConditionType:
		result = self._Entity.MxType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MyType(self) -> types.BoundaryConditionType:
		result = self._Entity.MyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MxyType(self) -> types.BoundaryConditionType:
		result = self._Entity.MxyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def QxType(self) -> types.BoundaryConditionType:
		result = self._Entity.QxType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def QyType(self) -> types.BoundaryConditionType:
		result = self._Entity.QyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	def SetNxType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Nx type for the scenario
		'''
		return self._Entity.SetNxType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetNyType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Ny type for the scenario
		'''
		return self._Entity.SetNyType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetNxyType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Nxy type for the scenario
		'''
		return self._Entity.SetNxyType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetMxType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Mx type for the scenario
		'''
		return self._Entity.SetMxType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetMyType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set My type for the scenario
		'''
		return self._Entity.SetMyType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetMxyType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Mxy type for the scenario
		'''
		return self._Entity.SetMxyType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetQxType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Qx type for the scenario
		'''
		return self._Entity.SetQxType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))

	def SetQyType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Qy type for the scenario
		'''
		return self._Entity.SetQyType(_types.BoundaryConditionType(types.GetEnumValue(type.value)))


class LoadPropertyUserGeneralPanelRowCol(LoadPropertyUserGeneralRowCol[LoadPropertyUserGeneralPanelDoubleRow]):
	def __init__(self, loadPropertyUserGeneralPanelRowCol: _api.LoadPropertyUserGeneralPanelRowCol):
		self._Entity = loadPropertyUserGeneralPanelRowCol
		self._CollectedClass = LoadPropertyUserGeneralPanelDoubleRow

	@property
	def LoadPropertyUserGeneralPanelRowColList(self) -> tuple[LoadPropertyUserGeneralPanelDoubleRow]:
		return tuple([LoadPropertyUserGeneralPanelDoubleRow(loadPropertyUserGeneralPanelRowCol) for loadPropertyUserGeneralPanelRowCol in self._Entity])

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool:
		...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool:
		...

	@overload
	def Get(self, name: str) -> LoadPropertyUserGeneralPanelDoubleRow:
		...

	@overload
	def Get(self, id: int) -> LoadPropertyUserGeneralPanelDoubleRow:
		...

	def DeleteScenario(self, item1 = None) -> bool:
		'''
		Overload 1: ``DeleteScenario(self, scenarioId: int) -> bool``

		Overload 2: ``DeleteScenario(self, scenarioName: str) -> bool``
		'''
		if isinstance(item1, int):
			return bool(super().DeleteScenario(item1))

		if isinstance(item1, str):
			return bool(super().DeleteScenario(item1))

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserGeneralPanelDoubleRow:
		'''
		Overload 1: ``Get(self, name: str) -> LoadPropertyUserGeneralPanelDoubleRow``

		Overload 2: ``Get(self, id: int) -> LoadPropertyUserGeneralPanelDoubleRow``
		'''
		if isinstance(item1, str):
			return LoadPropertyUserGeneralPanelDoubleRow(super().Get(item1))

		if isinstance(item1, int):
			return LoadPropertyUserGeneralPanelDoubleRow(super().Get(item1))

		return LoadPropertyUserGeneralPanelDoubleRow(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.LoadPropertyUserGeneralPanelRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserGeneralPanelRowColList

	def __len__(self):
		return len(self.LoadPropertyUserGeneralPanelRowColList)


class LoadPropertyUserGeneralPanel(LoadProperty):
	def __init__(self, loadPropertyUserGeneralPanel: _api.LoadPropertyUserGeneralPanel):
		self._Entity = loadPropertyUserGeneralPanel

	@property
	def UserGeneralRows(self) -> LoadPropertyUserGeneralPanelRowCol:
		'''
		Load property row data
		'''
		result = self._Entity.UserGeneralRows
		return LoadPropertyUserGeneralPanelRowCol(result) if result is not None else None

	@property
	def IsIncludingThermal(self) -> bool:
		'''
		Bool indicating whether there is a row in each scenario for thermal loads.
		Setting adds a thermal row for every "double row" in the collection.
		To see this change on any rows, you must get the row from the collection again.
		'''
		return self._Entity.IsIncludingThermal

	@IsIncludingThermal.setter
	def IsIncludingThermal(self, value: bool) -> None:
		self._Entity.IsIncludingThermal = value

	def SetIsZeroCurvature(self, isZeroCurvature: bool) -> None:
		return self._Entity.SetIsZeroCurvature(isZeroCurvature)


class JointSelectionDesignResult(JointDesignResult):
	def __init__(self, jointSelectionDesignResult: _api.JointSelectionDesignResult):
		self._Entity = jointSelectionDesignResult

	@property
	def JointSelectionId(self) -> types.JointSelectionId:
		result = self._Entity.JointSelectionId
		return types.JointSelectionId[result.ToString()] if result is not None else None


class JointFastenerDesignResult(JointSelectionDesignResult):
	def __init__(self, jointFastenerDesignResult: _api.JointFastenerDesignResult):
		self._Entity = jointFastenerDesignResult

	@property
	def FastenerBoltId(self) -> int:
		return self._Entity.FastenerBoltId

	@property
	def FastenerCodeId(self) -> int:
		return self._Entity.FastenerCodeId


class JointMaterialDesignResult(JointSelectionDesignResult):
	def __init__(self, jointMaterialDesignResult: _api.JointMaterialDesignResult):
		self._Entity = jointMaterialDesignResult

	@property
	def MaterialId(self) -> int:
		warnings.warn("Use Material instead.", DeprecationWarning, 2)
		return self._Entity.MaterialId

	@property
	def MaterialType(self) -> types.MaterialType:
		result = self._Entity.MaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def Material(self) -> str:
		return self._Entity.Material


class JointRangeDesignResult(JointDesignResult):
	def __init__(self, jointRangeDesignResult: _api.JointRangeDesignResult):
		self._Entity = jointRangeDesignResult

	@property
	def JointRangeId(self) -> types.JointRangeId:
		result = self._Entity.JointRangeId
		return types.JointRangeId[result.ToString()] if result is not None else None

	@property
	def JointRangeMode(self) -> types.JointRangeMode:
		result = self._Entity.JointRangeMode
		return types.JointRangeMode[result.ToString()] if result is not None else None

	@property
	def Value(self) -> float:
		return self._Entity.Value


class JointRivetDesignResult(JointSelectionDesignResult):
	def __init__(self, jointRivetDesignResult: _api.JointRivetDesignResult):
		self._Entity = jointRivetDesignResult

	@property
	def RivetId(self) -> int:
		return self._Entity.RivetId

	@property
	def RivetDiameterId(self) -> int:
		return self._Entity.RivetDiameterId


class PlateElementBulkUpdater(BulkUpdaterBase):
	def __init__(self, plateElementBulkUpdater: _api.PlateElementBulkUpdater):
		self._Entity = plateElementBulkUpdater

	@staticmethod
	def GetBulkUpdater(application: Application, items: tuple[PlateElement]) -> PlateElementBulkUpdater:
		itemsList = List[_api.PlateElement]()
		if items is not None:
			for x in items:
				if x is not None:
					itemsList.Add(x._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return PlateElementBulkUpdater(_api.PlateElementBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class Environment(ABC):
	'''
	Represents HyperX's execution environment (where HyperX is installed).
	'''
	@classmethod
	def InstallLocation(self) -> str:
		return _api.Environment.InstallLocation

	@classmethod
	def ApiVersion(self) -> str:
		'''
		The scripting API version of this HyperX environment
		'''
		return _api.Environment.ApiVersion

	@staticmethod
	def SetLocation(location: str) -> None:
		'''
		Set the directory location of the HyperX binaries.
		* This method is *not* required for Python and IronPython client application.
		* This method is required for C# and VB.NET clients as these applications
		need HyperX.Scripting.dll alongside its binaries.
		
		:param location: Path to the binaries.
		'''
		return _api.Environment.SetLocation(location)

	@staticmethod
	def Initialize() -> None:
		'''
		Initialize the HyperX scripting environment.
		'''
		return _api.Environment.Initialize()


class FailureCriterionSetting(FailureSetting):
	'''
	Setting for a Failure Criteria.
	'''
	def __init__(self, failureCriterionSetting: _api.FailureCriterionSetting):
		self._Entity = failureCriterionSetting


class FailureModeSetting(FailureSetting):
	'''
	Setting for a Failure Mode.
	'''
	def __init__(self, failureModeSetting: _api.FailureModeSetting):
		self._Entity = failureModeSetting


class HelperFunctions(ABC):
	@staticmethod
	def NullableSingle(input: float) -> float:
		return _api.HelperFunctions.NullableSingle(input)

	@staticmethod
	def GetFamilyObjectForObjectId(familyId: types.BeamPanelFamily, objectId: int) -> types.FamilyObjectUID:
		return types.FamilyObjectUID(_api.HelperFunctions.GetFamilyObjectForObjectId(_types.BeamPanelFamily(types.GetEnumValue(familyId.value)), objectId))


class IBulkUpdatableEntity:
	def __init__(self, iBulkUpdatableEntity: _api.IBulkUpdatableEntity):
		self._Entity = iBulkUpdatableEntity

	pass


class LaminatePlyData:
	'''
	Per ply data for Laminate materials
	'''
	def __init__(self, laminatePlyData: _api.LaminatePlyData):
		self._Entity = laminatePlyData

	@property
	def MaterialId(self) -> int:
		'''
		IMPORTANT: This is the ID of the laminate to which this ply belongs, different than ``hyperx.api.LaminatePlyData.PlyMaterialId``
		'''
		return self._Entity.MaterialId

	@property
	def PlyId(self) -> int:
		return self._Entity.PlyId

	@property
	def PlyMaterialId(self) -> int:
		'''
		ID of the material used in this ply
		'''
		return self._Entity.PlyMaterialId

	@property
	def PlyMaterialType(self) -> types.MaterialType:
		result = self._Entity.PlyMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def Angle(self) -> float:
		'''
		Ply angle
		'''
		return self._Entity.Angle

	@property
	def Thickness(self) -> float:
		return self._Entity.Thickness

	@property
	def IsFabric(self) -> bool:
		return self._Entity.IsFabric

	@property
	def FamilyPlyId(self) -> int | None:
		return self._Entity.FamilyPlyId

	@property
	def OriginalPlyId(self) -> int:
		return self._Entity.OriginalPlyId

	@property
	def OriginalFamilyPlyId(self) -> int | None:
		return self._Entity.OriginalFamilyPlyId

	@property
	def DisplaySequenceId(self) -> int | None:
		return self._Entity.DisplaySequenceId

	@property
	def PlyStiffenerSubType(self) -> types.PlyStiffenerSubType:
		result = self._Entity.PlyStiffenerSubType
		return types.PlyStiffenerSubType[result.ToString()] if result is not None else None

	@property
	def Object1(self) -> bool:
		return self._Entity.Object1

	@property
	def Object2(self) -> bool:
		return self._Entity.Object2

	@property
	def Object3(self) -> bool:
		return self._Entity.Object3

	@property
	def IsInverted(self) -> bool:
		return self._Entity.IsInverted

	@property
	def IsFullStructure(self) -> bool:
		return self._Entity.IsFullStructure

	@property
	def UseTrueFiberDirection(self) -> bool:
		return self._Entity.UseTrueFiberDirection

	@property
	def IsInFoot(self) -> bool:
		return self._Entity.IsInFoot

	@property
	def IsInWeb(self) -> bool:
		return self._Entity.IsInWeb

	@property
	def IsInCap(self) -> bool:
		return self._Entity.IsInCap

	def SetMaterial(self, matId: int) -> bool:
		'''
		Sets the material of a ply to the matId. This includes: PlyMaterialId and PlyMaterialType, and updates Thickness and IsFabric
		
		:return: False if the ply is not editable
		'''
		return self._Entity.SetMaterial(matId)

	def SetAngle(self, angle: float) -> bool:
		'''
		Sets the angle of a ply
		
		:return: False if the ply is not editable
		'''
		return self._Entity.SetAngle(angle)


class Beam(Zone):
	def __init__(self, beam: _api.Beam):
		self._Entity = beam

	@property
	def Length(self) -> float:
		return self._Entity.Length

	@property
	def Phi(self) -> float | None:
		return self._Entity.Phi

	@property
	def K1(self) -> float | None:
		'''
		Units: English = 1/in | Standard = 1/mm.
		'''
		return self._Entity.K1

	@property
	def K2(self) -> float | None:
		'''
		Units: English = 1/in | Standard = 1/mm.
		'''
		return self._Entity.K2

	@property
	def ReferencePlane(self) -> types.ReferencePlaneBeam:
		result = self._Entity.ReferencePlane
		return types.ReferencePlaneBeam[result.ToString()] if result is not None else None

	@Phi.setter
	def Phi(self, value: float | None) -> None:
		self._Entity.Phi = value

	@K1.setter
	def K1(self, value: float | None) -> None:
		self._Entity.K1 = value

	@K2.setter
	def K2(self, value: float | None) -> None:
		self._Entity.K2 = value

	@ReferencePlane.setter
	def ReferencePlane(self, value: types.ReferencePlaneBeam) -> None:
		self._Entity.ReferencePlane = _types.ReferencePlaneBeam(types.GetEnumValue(value.value))


class ZoneBaseBulkUpdater(BulkUpdaterBase):
	def __init__(self, zoneBaseBulkUpdater: _api.ZoneBaseBulkUpdater):
		self._Entity = zoneBaseBulkUpdater

	@staticmethod
	def GetBulkUpdater(application: Application, items: tuple[ZoneBase]) -> ZoneBaseBulkUpdater:
		itemsList = List[_api.ZoneBase]()
		if items is not None:
			for x in items:
				if x is not None:
					itemsList.Add(x._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return ZoneBaseBulkUpdater(_api.ZoneBaseBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class BeamBulkUpdater(ZoneBaseBulkUpdater):
	def __init__(self, beamBulkUpdater: _api.BeamBulkUpdater):
		self._Entity = beamBulkUpdater

	@staticmethod
	def GetBulkUpdater(application: Application, items: tuple[Beam]) -> BeamBulkUpdater:
		itemsList = List[_api.Beam]()
		if items is not None:
			for x in items:
				if x is not None:
					itemsList.Add(x._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return BeamBulkUpdater(_api.BeamBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class Panel(Zone):
	def __init__(self, panel: _api.Panel):
		self._Entity = panel

	@property
	def Area(self) -> float:
		return self._Entity.Area

	@property
	def ReferencePlane(self) -> types.ReferencePlanePanel:
		result = self._Entity.ReferencePlane
		return types.ReferencePlanePanel[result.ToString()] if result is not None else None

	@property
	def AddedOffset(self) -> float:
		'''
		Units: English = in | Standard = mm.
		'''
		return self._Entity.AddedOffset

	@property
	def YSpan(self) -> float:
		'''
		Units: English = in | Standard = mm.
		'''
		return self._Entity.YSpan

	@property
	def IsCurved(self) -> bool:
		return self._Entity.IsCurved

	@property
	def Radius(self) -> float:
		'''
		Units: English = in | Standard = mm.
		'''
		return self._Entity.Radius

	@property
	def IsFullCylinder(self) -> bool:
		return self._Entity.IsFullCylinder

	@property
	def BucklingMode(self) -> types.ZoneBucklingMode:
		result = self._Entity.BucklingMode
		return types.ZoneBucklingMode[result.ToString()] if result is not None else None

	@property
	def PerformLocalPostbuckling(self) -> bool:
		return self._Entity.PerformLocalPostbuckling

	@property
	def A11Required(self) -> float | None:
		'''
		Units: English = lb/in | N/mm.
		'''
		return self._Entity.A11Required

	@property
	def A22Required(self) -> float | None:
		'''
		Units: English = lb/in | N/mm.
		'''
		return self._Entity.A22Required

	@property
	def A33Required(self) -> float | None:
		'''
		Units: English = lb/in | N/mm.
		'''
		return self._Entity.A33Required

	@property
	def D11Required(self) -> float | None:
		'''
		Units: English = lb*in²/in | Standard = N*mm²/mm.
		'''
		return self._Entity.D11Required

	@property
	def D22Required(self) -> float | None:
		'''
		Units: English = lb*in²/in | Standard = N*mm²/mm.
		'''
		return self._Entity.D22Required

	@property
	def D33Required(self) -> float | None:
		'''
		Units: English = lb*in²/in | Standard = N*mm²/mm.
		'''
		return self._Entity.D33Required

	@property
	def A11Auto(self) -> float | None:
		'''
		Units: English = lb/in | N/mm.
		'''
		return self._Entity.A11Auto

	@property
	def A22Auto(self) -> float | None:
		'''
		Units: English = lb/in | N/mm.
		'''
		return self._Entity.A22Auto

	@property
	def A33Auto(self) -> float | None:
		'''
		Units: English = lb/in | N/mm.
		'''
		return self._Entity.A33Auto

	@property
	def D11Auto(self) -> float | None:
		'''
		Units: English = lb*in²/in | Standard = N*mm²/mm.
		'''
		return self._Entity.D11Auto

	@property
	def D22Auto(self) -> float | None:
		'''
		Units: English = lb*in²/in | Standard = N*mm²/mm.
		'''
		return self._Entity.D22Auto

	@property
	def D33Auto(self) -> float | None:
		'''
		Units: English = lb*in²/in | Standard = N*mm²/mm.
		'''
		return self._Entity.D33Auto

	@property
	def Ey(self) -> float | None:
		'''
		Units: English = µin/in | Standard = µm/m.
		'''
		return self._Entity.Ey

	@property
	def Kx(self) -> float | None:
		'''
		Units: English = 1/in | Standard = 1/mm.
		'''
		return self._Entity.Kx

	@property
	def Ky(self) -> float | None:
		'''
		Units: English = 1/in | Standard = 1/mm.
		'''
		return self._Entity.Ky

	@property
	def HoneycombCoreAngle(self) -> float:
		'''
		Units: English = degrees | Standard = degrees
		'''
		return self._Entity.HoneycombCoreAngle

	@ReferencePlane.setter
	def ReferencePlane(self, value: types.ReferencePlanePanel) -> None:
		self._Entity.ReferencePlane = _types.ReferencePlanePanel(types.GetEnumValue(value.value))

	@AddedOffset.setter
	def AddedOffset(self, value: float) -> None:
		self._Entity.AddedOffset = value

	@YSpan.setter
	def YSpan(self, value: float) -> None:
		self._Entity.YSpan = value

	@IsCurved.setter
	def IsCurved(self, value: bool) -> None:
		self._Entity.IsCurved = value

	@Radius.setter
	def Radius(self, value: float) -> None:
		self._Entity.Radius = value

	@IsFullCylinder.setter
	def IsFullCylinder(self, value: bool) -> None:
		self._Entity.IsFullCylinder = value

	@BucklingMode.setter
	def BucklingMode(self, value: types.ZoneBucklingMode) -> None:
		self._Entity.BucklingMode = _types.ZoneBucklingMode(types.GetEnumValue(value.value))

	@PerformLocalPostbuckling.setter
	def PerformLocalPostbuckling(self, value: bool) -> None:
		self._Entity.PerformLocalPostbuckling = value

	@A11Required.setter
	def A11Required(self, value: float | None) -> None:
		self._Entity.A11Required = value

	@A22Required.setter
	def A22Required(self, value: float | None) -> None:
		self._Entity.A22Required = value

	@A33Required.setter
	def A33Required(self, value: float | None) -> None:
		self._Entity.A33Required = value

	@D11Required.setter
	def D11Required(self, value: float | None) -> None:
		self._Entity.D11Required = value

	@D22Required.setter
	def D22Required(self, value: float | None) -> None:
		self._Entity.D22Required = value

	@D33Required.setter
	def D33Required(self, value: float | None) -> None:
		self._Entity.D33Required = value

	@Ey.setter
	def Ey(self, value: float | None) -> None:
		self._Entity.Ey = value

	@Kx.setter
	def Kx(self, value: float | None) -> None:
		self._Entity.Kx = value

	@Ky.setter
	def Ky(self, value: float | None) -> None:
		self._Entity.Ky = value

	@HoneycombCoreAngle.setter
	def HoneycombCoreAngle(self, value: float) -> None:
		self._Entity.HoneycombCoreAngle = value


class PanelBulkUpdater(ZoneBaseBulkUpdater):
	def __init__(self, panelBulkUpdater: _api.PanelBulkUpdater):
		self._Entity = panelBulkUpdater

	@staticmethod
	def GetBulkUpdater(application: Application, items: tuple[Panel]) -> PanelBulkUpdater:
		itemsList = List[_api.Panel]()
		if items is not None:
			for x in items:
				if x is not None:
					itemsList.Add(x._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return PanelBulkUpdater(_api.PanelBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class PanelSegmentBulkUpdater(ZoneBaseBulkUpdater):
	def __init__(self, panelSegmentBulkUpdater: _api.PanelSegmentBulkUpdater):
		self._Entity = panelSegmentBulkUpdater

	@staticmethod
	def GetBulkUpdater(application: Application, items: tuple[PanelSegment]) -> PanelSegmentBulkUpdater:
		itemsList = List[_api.PanelSegment]()
		if items is not None:
			for x in items:
				if x is not None:
					itemsList.Add(x._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return PanelSegmentBulkUpdater(_api.PanelSegmentBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class ZoneBulkUpdater(ZoneBaseBulkUpdater):
	def __init__(self, zoneBulkUpdater: _api.ZoneBulkUpdater):
		self._Entity = zoneBulkUpdater

	@staticmethod
	def GetBulkUpdater(application: Application, items: tuple[Zone]) -> ZoneBulkUpdater:
		itemsList = List[_api.Zone]()
		if items is not None:
			for x in items:
				if x is not None:
					itemsList.Add(x._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return ZoneBulkUpdater(_api.ZoneBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


# Library for using the COM-Interface of Zuken E3.series with python
# Important differences to common E3 COM functionality:
# 	-The first, empty element of lists is removed
# 	-As python does not support call-by-reference there are additional returns for [out] parameters
# This file was created for E3.series 27.00 (TLB version 27.00)
# 
# mypy: ignore-errors

import typing
from win32com.client import VARIANT
from win32com.client import CDispatch
import pythoncom
from .tools import _get_default_dbe, _get_default_app, _raw_connect_dbe, _raw_connect_app, _variant_to_dict, _dict_to_variant

DLLDEFAULTVALUE = "-353353"

# -------------------- IBundleInterface--------------------
class Bundle:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Bundle. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasAttribute(name)

	def GetPinCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPinCount()

	def GetPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSymbolCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSymbolCount()

	def GetSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsShield(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsShield()

	def GetBundleCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBundleCount()

	def GetBundleIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetBundleIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetParentBundleId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetParentBundleId()

	def GetRootBundleId(self, bndid:int) -> int:
		"""
		:bndid [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetRootBundleId(bndid)

	def Create(self, aroundids:list[int]) -> int:
		"""
		:aroundids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.Create(aroundids)
		return ret[0]

	def CreateIn(self, cableid:int) -> int:
		"""
		:cableid [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateIn(cableid)

	def Capture(self, cabwirids:list[int]) -> int:
		"""
		:cabwirids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.Capture(cabwirids)
		return ret[0]

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete()

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetName(name)

	def IsTwisted(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsTwisted()

	def IsBundle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsBundle()

	def CreateShield(self, aroundids:list[int]) -> int:
		"""
		:aroundids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.CreateShield(aroundids)
		return ret[0]

	def CreateTwist(self, aroundids:list[int]) -> int:
		"""
		:aroundids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.CreateTwist(aroundids)
		return ret[0]

	def CreateBundle(self, aroundids:list[int]) -> int:
		"""
		:aroundids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.CreateBundle(aroundids)
		return ret[0]

	def CreateShieldIn(self, cableid:int) -> int:
		"""
		:cableid [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateShieldIn(cableid)

	def CreateTwistIn(self, cableid:int) -> int:
		"""
		:cableid [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateTwistIn(cableid)

	def CreateBundleIn(self, cableid:int) -> int:
		"""
		:cableid [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateBundleIn(cableid)

	def PlaceAll(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PlaceAll()

	def GetCableCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCableCount()

	def GetCableIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCableIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAnyCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAnyCount()

	def GetAnyIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAnyIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetCoreCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCoreCount()

	def GetCoreIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCoreIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def ReleaseIDs(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		ret = self._obj.ReleaseIDs(ids)
		return ret[0]

	def GetOverbraidIdEx(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.GetOverbraidIdEx()

	def GetRootOverbraidId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.GetRootOverbraidId()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

# -------------------- IAttributeInterface--------------------
class Attribute:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Attribute. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 7.20
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 7.20
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 7.20
		"""
		return self._obj.GetName()

	def GetInternalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 7.20
		"""
		return self._obj.GetInternalName()

	def GetValue(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 7.20
		"""
		return self._obj.GetValue()

	def GetInternalValue(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 7.20
		"""
		return self._obj.GetInternalValue()

	def SetValue(self, value:str) -> int:
		"""
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 7.20
		"""
		return self._obj.SetValue(value)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 7.20
		"""
		return self._obj.Delete()

	def GetTextIds(self, txttyp:int=0, search_string:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:txttyp [IN]: int Default value =0
		:search_string [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 7.20
		"""
		dummy=0
		ret, ids = self._obj.GetTextIds(dummy, txttyp, search_string)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTextCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 7.20
		"""
		return self._obj.GetTextCount()

	def DisplayAttribute(self, id:int=0) -> int:
		"""
		:id [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 7.20
		"""
		return self._obj.DisplayAttribute(id)

	def GetOwnerId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 7.20
		"""
		return self._obj.GetOwnerId()

	def GetFormattedValue(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 7.20
		"""
		return self._obj.GetFormattedValue()

	def DisplayValueAt(self, sheetid:int, x:float, y:float, bindid:int=0) -> int:
		"""
		:sheetid [IN]: int
		:x [IN]: float
		:y [IN]: float
		:bindid [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 7.20
		"""
		return self._obj.DisplayValueAt(sheetid, x, y, bindid)

	def IsLockChangeable(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 14.00
		"""
		return self._obj.IsLockChangeable()

	def GetLockChangeable(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 14.00
		"""
		return self._obj.GetLockChangeable()

	def SetLockChangeable(self, lockchangeable:bool) -> int:
		"""
		:lockchangeable [IN]: bool
		:Return: int

		Available since TLB-Versions: 14.00
		"""
		return self._obj.SetLockChangeable(lockchangeable)

	def FormatValue(self, name:str, value:str) -> str:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: str

		Available since TLB-Versions: 14.11
		"""
		return self._obj.FormatValue(name, value)

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

# -------------------- IClipboardInterface--------------------
class Clipboard:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Clipboard. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.30
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 18.30
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 18.30
		"""
		return self._obj.GetName()

	def GetAnyIds(self, flags:int) -> tuple[int, tuple[int,...]]:
		"""
		:flags [IN]: int
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 18.30
		"""
		dummy=0
		ret, ids = self._obj.GetAnyIds(flags, dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CommitToProject(self, flags:int, viewnumber:int=0) -> int:
		"""
		:flags [IN]: int
		:viewnumber [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 18.30
		"""
		return self._obj.CommitToProject(flags, viewnumber)

	def GetCollidingIds(self, flags:int) -> tuple[int, tuple[int,...]]:
		"""
		:flags [IN]: int
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 18.30
		"""
		dummy=0
		ret, ids = self._obj.GetCollidingIds(flags, dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.30
		"""
		return self._obj.Delete()

	def DeleteForced(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.DeleteForced()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

# -------------------- IComponentInterface--------------------
class Component:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Component. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 15.00
		"""
		return self._obj.GetName()

	def GetVersion(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 15.00
		"""
		return self._obj.GetVersion()

	def GetSupplyPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		dummy=0
		ret, ids = self._obj.GetSupplyPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 15.00
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.HasAttribute(name)

	def Search(self, name:str, version:str) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.Search(name, version)

	def GetModelName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 15.00
		"""
		return self._obj.GetModelName()

	def GetValidModelCharacteristics(self) -> tuple[int, tuple[str,...]]:
		"""
		:characteristics [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		dummy=0
		ret, characteristics = self._obj.GetValidModelCharacteristics(dummy)
		characteristics = characteristics[1:] if type(characteristics) == tuple and len(characteristics) > 0 else tuple()
		return ret, characteristics

	def GetFormboardSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		dummy=0
		ret, ids = self._obj.GetFormboardSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def Rename(self, name:str, version:str) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.Rename(name, version)

	def GetViewDefinitions(self) -> tuple[int, tuple[tuple[int,int],...]]:
		"""
		:viewDefinitions [OUT]: tuple[tuple[int,int],...]
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		dummy=0
		return self._obj.GetViewDefinitions(dummy)

	def GetPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 17.10
		"""
		dummy=0
		ret, ids = self._obj.GetPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSubType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetSubType()

	def GetComponentType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		return self._obj.GetComponentType()

	def GetStateIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 22.10
		"""
		dummy=0
		ret, ids = self._obj.GetStateIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

# -------------------- IConnectionInterface--------------------
class Connection:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Connection. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasAttribute(name)

	def DisplayAttributeValue(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DisplayAttributeValue(name)

	def DisplayAttributeValueAt(self, name:str, sheetid:int, x:float, y:float) -> int:
		"""
		:name [IN]: str
		:sheetid [IN]: int
		:x [IN]: float
		:y [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DisplayAttributeValueAt(name, sheetid, x, y)

	def SetAttributeVisibility(self, name:str, onoff:int) -> int:
		"""
		:name [IN]: str
		:onoff [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeVisibility(name, onoff)

	def IsValid(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsValid()

	def GetPinCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPinCount()

	def GetPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetCoreCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCoreCount()

	def GetCoreIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCoreIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetReferenceSymbolCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetReferenceSymbolCount()

	def GetReferenceSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetReferenceSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSignalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSignalName()

	def SetSignalName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetSignalName(name)

	def Highlight(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Highlight()

	def GetNetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetNetId()

	def GetNetSegmentCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetNetSegmentCount()

	def GetNetSegmentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNetSegmentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetPinGroupsCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPinGroupsCount()

	def GetPinGroupsIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetPinGroupsIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetPinGroupCount(self, num:int) -> int:
		"""
		:num [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPinGroupCount(num)

	def GetPinGroupIds(self, num:int) -> tuple[int, tuple[int,...]]:
		"""
		:num [IN]: int
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetPinGroupIds(num, dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsView(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsView()

	def GetViewNumber(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetViewNumber()

	def Create(self, shti:int, pnts:int, x:list[float], y:list[float], PointTypArr:list[int]=pythoncom.Empty) -> int:
		"""
		:shti [IN]: int
		:pnts [IN]: int
		:x [IN]: list[float]
		:y [IN]: list[float]
		:PointTypArr [IN]: list[int] Default value =pythoncom.Empty
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		x = [0.] + x
		y = [0.] + y
		if PointTypArr != pythoncom.Empty:
			PointTypArr = [0] + PointTypArr
		return self._obj.Create(shti, pnts, x, y, PointTypArr)

	def CreateOnFormboard(self, shti:int, pnts:int, x:list[float], y:list[float], PointTypArr:list[int]=pythoncom.Empty) -> typing.Union[tuple[int,...],int]:
		"""
		:shti [IN]: int
		:pnts [IN]: int
		:x [IN]: list[float]
		:y [IN]: list[float]
		:PointTypArr [IN]: list[int] Default value =pythoncom.Empty
		:Return: typing.Union[tuple[int,...],int]

		Available since TLB-Versions: 8.50
		"""
		x = [0.] + x
		y = [0.] + y
		if PointTypArr != pythoncom.Empty:
			PointTypArr = [0] + PointTypArr
		ret = self._obj.CreateOnFormboard(shti, pnts, x, y, PointTypArr)
		if type(ret) is tuple:
			ret = ret[1:] if type(ret) == tuple and len(ret) > 0 else tuple()
		return ret

	def GetTranslatedSignalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 16.00
		"""
		return self._obj.GetTranslatedSignalName()

	def CreateConnectionBetweenPoints(self, shti:int, x1:float, y1:float, x2:float, y2:float, flags:int=0) -> int:
		"""
		:shti [IN]: int
		:x1 [IN]: float
		:y1 [IN]: float
		:x2 [IN]: float
		:y2 [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.CreateConnectionBetweenPoints(shti, x1, y1, x2, y2, flags)

	def CreateConnection(self, flags:int, shti:int, pnts:int, x:list[float], y:list[float], PointTypArr:list[int]=pythoncom.Empty) -> tuple[int, tuple[int,...]]:
		"""
		:flags [IN]: int
		:shti [IN]: int
		:pnts [IN]: int
		:x [IN]: list[float]
		:y [IN]: list[float]
		:connections [OUT]: tuple[int,...]
		:PointTypArr [IN]: list[int] Default value =pythoncom.Empty
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		dummy=0
		x = [0.] + x
		y = [0.] + y
		ret, connections = self._obj.CreateConnection(flags, shti, pnts, x, y, dummy, PointTypArr)
		connections = connections[1:] if type(connections) == tuple and len(connections) > 0 else tuple()
		return ret, connections

# -------------------- IExternalDocumentInterface--------------------
class ExternalDocument:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize ExternalDocument. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def SetName(self, newname:str) -> str:
		"""
		:newname [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetName(newname)

	def Display(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Display()

	def Remove(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Remove()

	def Visible(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Visible()

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete()

	def Create(self, modi:int, name:str, file:str) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:file [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Create(modi, name, file)

	def Search(self, modi:int, name:str) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Search(modi, name)

	def Save(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Save()

	def InsertFile(self, modi:int, name:str, file:str) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:file [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.InsertFile(modi, name, file)

	def GetFile(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFile()

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasAttribute(name)

	def GetAssignment(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAssignment()

	def SetAssignment(self, newass:str) -> int:
		"""
		:newass [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAssignment(newass)

	def GetLocation(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLocation()

	def SetLocation(self, newloc:str) -> int:
		"""
		:newloc [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLocation(newloc)

	def SetCompleteName(self, newnam:str, newass:str, newloc:str) -> int:
		"""
		:newnam [IN]: str
		:newass [IN]: str
		:newloc [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetCompleteName(newnam, newass, newloc)

	def MoveTo(self, position:int, before:int=0) -> int:
		"""
		:position [IN]: int
		:before [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.MoveTo(position, before)

	def CheckOut(self, lock:bool=True) -> int:
		"""
		:lock [IN]: bool Default value =True
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CheckOut(lock)

	def CheckIn(self, unlock:bool=True) -> int:
		"""
		:unlock [IN]: bool Default value =True
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CheckIn(unlock)

	def IsReadOnly(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsReadOnly()

	def GetOwner(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetOwner()

	def SetVisible(self, visible:int=1) -> int:
		"""
		:visible [IN]: int Default value =1
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetVisible(visible)

	def IsVisible(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsVisible()

	def SetCompleteNameEx(self, newnam:str, newass:str, newloc:str, onlygiven:bool) -> int:
		"""
		:newnam [IN]: str
		:newass [IN]: str
		:newloc [IN]: str
		:onlygiven [IN]: bool
		:Return: int

		Available since TLB-Versions: 9.20
		"""
		return self._obj.SetCompleteNameEx(newnam, newass, newloc, onlygiven)

	def GetInternalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 16.05
		"""
		return self._obj.GetInternalName()

	def DisplayEx(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.DisplayEx(flags)

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

# -------------------- IFieldInterface--------------------
class Field:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Field. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetName(name)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def GetType(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetType()

	def GetVersion(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetVersion()

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasAttribute(name)

	def GetTextCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTextCount()

	def GetTextIds(self, txttyp:int=0, search_string:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:txttyp [IN]: int Default value =0
		:search_string [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTextIds(dummy, txttyp, search_string)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSchemaLocation(self) -> tuple[int, float, float, str, str, str]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:grid [OUT]: str
		:column_value [OUT]: str
		:row_value [OUT]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetSchemaLocation(dummy, dummy, dummy, dummy, dummy)

	def GetArea(self) -> tuple[int, float, float, float, float]:
		"""
		:xmin [OUT]: float
		:ymin [OUT]: float
		:xmax [OUT]: float
		:ymax [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetArea(dummy, dummy, dummy, dummy)

	def GetGraphId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphId()

	def Jump(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Jump()

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete()

	def GetSymbolCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSymbolCount()

	def GetSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def Place(self, shti:int, x1:float, y1:float, x2:float, y2:float, moveall:bool=False) -> int:
		"""
		:shti [IN]: int
		:x1 [IN]: float
		:y1 [IN]: float
		:x2 [IN]: float
		:y2 [IN]: float
		:moveall [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Place(shti, x1, y1, x2, y2, moveall)

	def GetInsideNetSegmentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetInsideNetSegmentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetCrossingNetSegmentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCrossingNetSegmentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetInsideTextIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetInsideTextIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetInsideGraphIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetInsideGraphIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetInsideSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetInsideSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetParentFieldId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetParentFieldId()

	def GetCrossingFieldIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCrossingFieldIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetInsideFieldIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetInsideFieldIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAllInsideFieldIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAllInsideFieldIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTypeName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTypeName()

	def GetInsidePanelConnectionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetInsidePanelConnectionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetCrossingPanelConnectionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCrossingPanelConnectionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAssignedOptionExpressions(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressions(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def SetOptionExpressions(self, expressions:list[str]) -> int:
		"""
		:expressions [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 9.12
		"""
		return self._obj.SetOptionExpressions(expressions)

	def SetCompleteName(self, newdev:str, newass:str, newloc:str, onlygiven:bool=False) -> int:
		"""
		:newdev [IN]: str
		:newass [IN]: str
		:newloc [IN]: str
		:onlygiven [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 9.20
		"""
		return self._obj.SetCompleteName(newdev, newass, newloc, onlygiven)

	def SetDeviceAssignment(self, newass:str) -> int:
		"""
		:newass [IN]: str
		:Return: int

		Available since TLB-Versions: 9.20
		"""
		return self._obj.SetDeviceAssignment(newass)

	def GetDeviceAssignment(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.20
		"""
		return self._obj.GetDeviceAssignment()

	def SetDeviceLocation(self, newloc:str) -> int:
		"""
		:newloc [IN]: str
		:Return: int

		Available since TLB-Versions: 9.20
		"""
		return self._obj.SetDeviceLocation(newloc)

	def GetDeviceLocation(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.20
		"""
		return self._obj.GetDeviceLocation()

	def SetDeviceName(self, newdev:str) -> int:
		"""
		:newdev [IN]: str
		:Return: int

		Available since TLB-Versions: 9.20
		"""
		return self._obj.SetDeviceName(newdev)

	def GetDeviceName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.20
		"""
		return self._obj.GetDeviceName()

	def GetAssignedOptionExpressionsEx(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 9.23
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressionsEx(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def GetInterruptBorder(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 10.22
		"""
		return self._obj.GetInterruptBorder()

	def SetInterruptBorder(self, interrupt:bool) -> bool:
		"""
		:interrupt [IN]: bool
		:Return: bool

		Available since TLB-Versions: 10.22
		"""
		return self._obj.SetInterruptBorder(interrupt)

	def GetInterruptBorderGap(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 10.22
		"""
		return self._obj.GetInterruptBorderGap()

	def SetInterruptBorderGap(self, gap:float) -> float:
		"""
		:gap [IN]: float
		:Return: float

		Available since TLB-Versions: 10.22
		"""
		return self._obj.SetInterruptBorderGap(gap)

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

# -------------------- IGraphInterface--------------------
class Graph:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Graph. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetId(id)

	def CreateText(self, shti:int, text:str, x:float, y:float) -> int:
		"""
		:shti [IN]: int
		:text [IN]: str
		:x [IN]: float
		:y [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.CreateText(shti, text, x, y)

	def CreateRotatedText(self, shti:int, text:str, x:float, y:float, rotation:float) -> int:
		"""
		:shti [IN]: int
		:text [IN]: str
		:x [IN]: float
		:y [IN]: float
		:rotation [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.CreateRotatedText(shti, text, x, y, rotation)

	def CreateLine(self, shti:int, x1:float, y1:float, x2:float, y2:float) -> int:
		"""
		:shti [IN]: int
		:x1 [IN]: float
		:y1 [IN]: float
		:x2 [IN]: float
		:y2 [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.CreateLine(shti, x1, y1, x2, y2)

	def CreateRectangle(self, shti:int, x1:float, y1:float, x2:float, y2:float) -> int:
		"""
		:shti [IN]: int
		:x1 [IN]: float
		:y1 [IN]: float
		:x2 [IN]: float
		:y2 [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.CreateRectangle(shti, x1, y1, x2, y2)

	def CreateMeasure(self, shti:int, x1:float, y1:float, x2:float, y2:float) -> int:
		"""
		:shti [IN]: int
		:x1 [IN]: float
		:y1 [IN]: float
		:x2 [IN]: float
		:y2 [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.CreateMeasure(shti, x1, y1, x2, y2)

	def CreatePolygon(self, shti:int, pnts:int, x:list[int], y:list[int]) -> int:
		"""
		:shti [IN]: int
		:pnts [IN]: int
		:x [IN]: list[int]
		:y [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.CreatePolygon(shti, pnts, x, y)

	def CreateCircle(self, shti:int, x:float, y:float, radius:float) -> int:
		"""
		:shti [IN]: int
		:x [IN]: float
		:y [IN]: float
		:radius [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.CreateCircle(shti, x, y, radius)

	def CreateArc(self, shti:int, x:float, y:float, radius:float, start:float, end:float) -> int:
		"""
		:shti [IN]: int
		:x [IN]: float
		:y [IN]: float
		:radius [IN]: float
		:start [IN]: float
		:end [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.CreateArc(shti, x, y, radius, start, end)

	def Place(self, x:float, y:float) -> int:
		"""
		:x [IN]: float
		:y [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.Place(x, y)

	def GetType(self) -> int:
		"""
		:Return: int, Enum type Available: e3series.types.GraphType.

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetType()

	def GetLevel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetLevel()

	def SetLevel(self, newlev:int) -> int:
		"""
		:newlev [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetLevel(newlev)

	def GetGraphCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetGraphCount()

	def GetGraphIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetGraphIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.Delete()

	def GetColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetColour()

	def SetColour(self, newcol:int) -> int:
		"""
		:newcol [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetColour(newcol)

	def GetHatchColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetHatchColour()

	def SetHatchColour(self, newcol:int) -> int:
		"""
		:newcol [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetHatchColour(newcol)

	def GetAssignedOptionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetAssignedOptionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateImage(self, sheetid:int, xpos:float, ypos:float, xsize:float, ysize:float, filename:str, embed:int=1) -> int:
		"""
		:sheetid [IN]: int
		:xpos [IN]: float
		:ypos [IN]: float
		:xsize [IN]: float
		:ysize [IN]: float
		:filename [IN]: str
		:embed [IN]: int Default value =1
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.CreateImage(sheetid, xpos, ypos, xsize, ysize, filename, embed)

	def GetImageInfo(self) -> tuple[int, float, float, float, float, str, int]:
		"""
		:xpos [OUT]: float
		:ypos [OUT]: float
		:xsize [OUT]: float
		:ysize [OUT]: float
		:filename [OUT]: str
		:embed [OUT]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		return self._obj.GetImageInfo(dummy, dummy, dummy, dummy, dummy, dummy)

	def SetImageInfo(self, xpos:float, ypos:float, xsize:float, ysize:float, filename:str="", embed:int=-1) -> int:
		"""
		:xpos [IN]: float
		:ypos [IN]: float
		:xsize [IN]: float
		:ysize [IN]: float
		:filename [IN]: str Default value =""
		:embed [IN]: int Default value =-1
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetImageInfo(xpos, ypos, xsize, ysize, filename, embed)

	def IsRedlined(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.IsRedlined()

	def GetLineColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetLineColour()

	def SetLineColour(self, newcol:int) -> int:
		"""
		:newcol [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetLineColour(newcol)

	def GetLineWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetLineWidth()

	def SetLineWidth(self, newwid:float) -> float:
		"""
		:newwid [IN]: float
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetLineWidth(newwid)

	def GetLineStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetLineStyle()

	def SetLineStyle(self, newstyle:int) -> int:
		"""
		:newstyle [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetLineStyle(newstyle)

	def GetHatchLineWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetHatchLineWidth()

	def SetHatchLineWidth(self, newwid:float) -> float:
		"""
		:newwid [IN]: float
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetHatchLineWidth(newwid)

	def GetHatchLineStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetHatchLineStyle()

	def SetHatchLineStyle(self, newstyle:int) -> int:
		"""
		:newstyle [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetHatchLineStyle(newstyle)

	def GetHatchLineDistance(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetHatchLineDistance()

	def SetHatchLineDistance(self, newdist:float) -> float:
		"""
		:newdist [IN]: float
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetHatchLineDistance(newdist)

	def GetArrows(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetArrows()

	def SetArrows(self, newarrows:int) -> int:
		"""
		:newarrows [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetArrows(newarrows)

	def GetHatchPattern(self) -> tuple[int, float, float]:
		"""
		:angle1 [OUT]: float
		:angle2 [OUT]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		return self._obj.GetHatchPattern(dummy, dummy)

	def SetHatchPattern(self, newpat:int, angle1:float, angle2:float) -> int:
		"""
		:newpat [IN]: int
		:angle1 [IN]: float
		:angle2 [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetHatchPattern(newpat, angle1, angle2)

	def GetTypeId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetTypeId()

	def CreateFromSymbol(self, shti:int, x:float, y:float, rot:str, scale:float, maintaintextsize:bool, symnam:str, symver:str) -> int:
		"""
		:shti [IN]: int
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: str
		:scale [IN]: float
		:maintaintextsize [IN]: bool
		:symnam [IN]: str
		:symver [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.CreateFromSymbol(shti, x, y, rot, scale, maintaintextsize, symnam, symver)

	def GetArc(self) -> tuple[int, float, float, float, float, float]:
		"""
		:xm [OUT]: float
		:ym [OUT]: float
		:rad [OUT]: float
		:startang [OUT]: float
		:endang [OUT]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		return self._obj.GetArc(dummy, dummy, dummy, dummy, dummy)

	def GetCircle(self) -> tuple[int, float, float, float]:
		"""
		:xm [OUT]: float
		:ym [OUT]: float
		:rad [OUT]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		return self._obj.GetCircle(dummy, dummy, dummy)

	def GetLine(self) -> tuple[int, float, float, float, float]:
		"""
		:x1 [OUT]: float
		:y1 [OUT]: float
		:x2 [OUT]: float
		:y2 [OUT]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		return self._obj.GetLine(dummy, dummy, dummy, dummy)

	def GetPolygon(self) -> tuple[int, int, tuple[float,...], tuple[float,...]]:
		"""
		:npnts [OUT]: int
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, npnts, xarr, yarr = self._obj.GetPolygon(dummy, dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		return ret, npnts, xarr, yarr

	def GetRectangle(self) -> tuple[int, float, float, float, float]:
		"""
		:x1 [OUT]: float
		:y1 [OUT]: float
		:x2 [OUT]: float
		:y2 [OUT]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		return self._obj.GetRectangle(dummy, dummy, dummy, dummy)

	def SaveImage(self, filename:str) -> int:
		"""
		:filename [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SaveImage(filename)

	def CreateGroup(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.CreateGroup(ids)

	def UnGroup(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.UnGroup(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetParentID(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetParentID()

	def SetParentID(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetParentID(id)

	def CreateCurve(self, shti:int, pnts:int, x:list[float], y:list[float]) -> int:
		"""
		:shti [IN]: int
		:pnts [IN]: int
		:x [IN]: list[float]
		:y [IN]: list[float]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		x = [0.] + x
		y = [0.] + y
		return self._obj.CreateCurve(shti, pnts, x, y)

	def GetCurve(self) -> tuple[int, int, tuple[float,...], tuple[float,...]]:
		"""
		:npnts [OUT]: int
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, npnts, xarr, yarr = self._obj.GetCurve(dummy, dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		return ret, npnts, xarr, yarr

	def GetAssignedOptionExpressions(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressions(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def SetOptionExpressions(self, expressions:list[str]) -> int:
		"""
		:expressions [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 9.12
		"""
		return self._obj.SetOptionExpressions(expressions)

	def GetAssignedOptionExpressionsEx(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 9.23
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressionsEx(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.AddAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.DeleteAttribute(name)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 11.00
		"""
		return self._obj.GetAttributeValue(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.HasAttribute(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.SetAttributeValue(name, value)

	def CreateCloud(self, shti:int, pnts:int, x:list[float], y:list[float]) -> int:
		"""
		:shti [IN]: int
		:pnts [IN]: int
		:x [IN]: list[float]
		:y [IN]: list[float]
		:Return: int

		Available since TLB-Versions: 16.70
		"""
		x = [0.] + x
		y = [0.] + y
		return self._obj.CreateCloud(shti, pnts, x, y)

	def GetCloud(self) -> tuple[int, int, tuple[float,...], tuple[float,...]]:
		"""
		:npnts [OUT]: int
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 16.70
		"""
		dummy=0
		ret, npnts, xarr, yarr = self._obj.GetCloud(dummy, dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		return ret, npnts, xarr, yarr

	def SetRedlined(self, onoff:bool) -> int:
		"""
		:onoff [IN]: bool Default value =TRUE
		:Return: int

		Available since TLB-Versions: 17.04
		"""
		return self._obj.SetRedlined(onoff)

	def OptimizeGraphicObjects(self, ids:list[int], mode:int, angle:int) -> tuple[int, list[int]]:
		"""
		:ids [IN/OUT]: list[int]
		:mode [IN]: int
		:angle [IN]: int
		:Return: int

		Available since TLB-Versions: 22.00, 21.01, 20.22
		"""
		ret, ids = self._obj.OptimizeGraphicObjects(ids, mode, angle)
		ids = ids[1:] if type(ids) == list and len(ids) > 0 else []
		return ret, ids

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def SendToForeground(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 24.22
		"""
		return self._obj.SendToForeground()

	def SendToBackground(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 24.22
		"""
		return self._obj.SendToBackground()

# -------------------- IModuleInterface--------------------
class Module:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Module. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.SetId(id)

	def GetLevel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetLevel()

	def GetParentModuleId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetParentModuleId()

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetName()

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.SetName(name)

	def GetFileName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetFileName()

	def GetTypeName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetTypeName()

	def IsTypeLoadable(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.IsTypeLoadable()

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.HasAttribute(name)

	def GetPortCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetPortCount()

	def GetPortIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		dummy=0
		ret, ids = self._obj.GetPortIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def Search(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.Search(name)

	def GetParentSheetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetParentSheetId()

	def GetSheetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		dummy=0
		ret, ids = self._obj.GetSheetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetModuleIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		dummy=0
		ret, ids = self._obj.GetModuleIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

# -------------------- IModulePortInterface--------------------
class ModulePort:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize ModulePort. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetName()

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.SetName(name)

	def GetSymbolIds(self) -> tuple[int, tuple[int,...], tuple[int,...]]:
		"""
		:OnBlockId [OUT]: tuple[int,...]
		:OnSheetId [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		dummy=0
		ret, OnBlockId, OnSheetId = self._obj.GetSymbolIds(dummy, dummy)
		OnBlockId = OnBlockId[1:] if type(OnBlockId) == tuple and len(OnBlockId) > 0 else tuple()
		OnSheetId = OnSheetId[1:] if type(OnSheetId) == tuple and len(OnSheetId) > 0 else tuple()
		return ret, OnBlockId, OnSheetId

	def GetModuleId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetModuleId()

	def IsBus(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.IsBus()

	def GetSignalId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetSignalId()

	def GetBusName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetBusName()

	def SetBusName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.SetBusName(name)

	def GetSignalIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		dummy=0
		ret, ids = self._obj.GetSignalIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

# -------------------- INetSegmentInterface--------------------
class NetSegment:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize NetSegment. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetName()

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.HasAttribute(name)

	def DisplayAttributeValue(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.DisplayAttributeValue(name)

	def DisplayAttributeValueAt(self, name:str, sheetid:int, x:float, y:float) -> int:
		"""
		:name [IN]: str
		:sheetid [IN]: int
		:x [IN]: float
		:y [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.DisplayAttributeValueAt(name, sheetid, x, y)

	def SetAttributeVisibility(self, name:str, onoff:int) -> int:
		"""
		:name [IN]: str
		:onoff [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetAttributeVisibility(name, onoff)

	def GetCoreCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetCoreCount()

	def GetCoreIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetCoreIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSignalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetSignalName()

	def SetSignalName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetSignalName(name)

	def Highlight(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.Highlight()

	def GetNetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetNetId()

	def GetLength(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetLength()

	def SetLength(self, newlen:float) -> float:
		"""
		:newlen [IN]: float
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetLength(newlen)

	def GetLineSegments(self) -> tuple[int, int, tuple[int,...], tuple[int,...], tuple[int,...]]:
		"""
		:shtid [OUT]: int
		:xarr [OUT]: tuple[int,...]
		:yarr [OUT]: tuple[int,...]
		:PointTypArr [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, shtid, xarr, yarr, PointTypArr = self._obj.GetLineSegments(dummy, dummy, dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		PointTypArr = PointTypArr[1:] if type(PointTypArr) == tuple and len(PointTypArr) > 0 else tuple()
		return ret, shtid, xarr, yarr, PointTypArr

	def SetLineColour(self, newcol:int) -> int:
		"""
		:newcol [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetLineColour(newcol)

	def SetLineStyle(self, newstl:int) -> int:
		"""
		:newstl [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetLineStyle(newstl)

	def SetLineWidth(self, newwid:float) -> int:
		"""
		:newwid [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetLineWidth(newwid)

	def SetLineLevel(self, newlev:int) -> int:
		"""
		:newlev [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetLineLevel(newlev)

	def GetSymbolCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetSymbolCount()

	def GetSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAssignedOptionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetAssignedOptionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.Delete()

	def GetBusName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetBusName()

	def SetBusName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetBusName(name)

	def GetSignalIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetSignalIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsView(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.IsView()

	def IsBus(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.IsBus()

	def IsPanelPath(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.IsPanelPath()

	def IsOffline(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.IsOffline()

	def GetLevel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetLevel()

	def SetLevel(self, level:int) -> int:
		"""
		:level [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetLevel(level)

	def GetLineStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetLineStyle()

	def GetLineColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetLineColour()

	def GetLineWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetLineWidth()

	def GetNodeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetNodeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetConnectedSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetConnectedSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetEffectiveDirection(self) -> tuple[int, int, int]:
		"""
		:fromID [OUT]: int
		:toID [OUT]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		return self._obj.GetEffectiveDirection(dummy, dummy)

	def SetEffectiveDirection(self, toID:int) -> int:
		"""
		:toID [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetEffectiveDirection(toID)

	def GetManufacturingLength(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetManufacturingLength()

	def SetManufacturingLength(self, newval:float) -> float:
		"""
		:newval [IN]: float
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetManufacturingLength(newval)

	def GetSchemaLength(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetSchemaLength()

	def AdjustSchemaLength(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.AdjustSchemaLength()

	def GetRotation(self, anchorid:int) -> float:
		"""
		:anchorid [IN]: int
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetRotation(anchorid)

	def SetRotation(self, anchorid:int, newval:float) -> float:
		"""
		:anchorid [IN]: int
		:newval [IN]: float
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetRotation(anchorid, newval)

	def GetOuterDiameter(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetOuterDiameter()

	def GetAssignedOptionExpressions(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressions(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def SetOptionExpressions(self, expressions:list[str]) -> int:
		"""
		:expressions [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 9.12
		"""
		return self._obj.SetOptionExpressions(expressions)

	def GetConnectLineIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.22
		"""
		dummy=0
		ret, ids = self._obj.GetConnectLineIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAssignedOptionExpressionsEx(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 9.23
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressionsEx(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def SetSchemaLength(self, newval:float) -> float:
		"""
		:newval [IN]: float
		:Return: float

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetSchemaLength(newval)

	def GetTranslatedSignalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 11.00
		"""
		return self._obj.GetTranslatedSignalName()

	def SetIgnoreForCablingTable(self, set:bool) -> int:
		"""
		:set [IN]: bool
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		return self._obj.SetIgnoreForCablingTable(set)

	def GetBundleSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 20.20
		"""
		dummy=0
		ret, ids = self._obj.GetBundleSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsBusbar(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		return self._obj.IsBusbar()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

# -------------------- IOptionInterface--------------------
class Option:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Option. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetName(name)

	def Create(self, name:str, parent:int=0, position:int=0, before:int=0) -> int:
		"""
		:name [IN]: str
		:parent [IN]: int Default value =0
		:position [IN]: int Default value =0
		:before [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Create(name, parent, position, before)

	def Delete(self, _del:int) -> int:
		"""
		:_del [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete(_del)

	def Search(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Search(name)

	def IsActive(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsActive()

	def Activate(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Activate()

	def Deactivate(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Deactivate()

	def Add(self, devi:int) -> int:
		"""
		:devi [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Add(devi)

	def Remove(self, devi:int) -> int:
		"""
		:devi [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Remove(devi)

	def GetFullName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFullName()

	def GetInternalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetInternalName()

	def GetFullInternalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFullInternalName()

	def GetDescription(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDescription()

	def GetInternalDescription(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetInternalDescription()

	def IsAssignable(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsAssignable()

	def IsVariant(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsVariant()

	def GetOptionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetOptionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetParentOptionId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetParentOptionId()

	def GetPropertyFlags(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPropertyFlags()

	def SetPropertyFlags(self, newflags:int) -> int:
		"""
		:newflags [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPropertyFlags(newflags)

	def GetAllDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAllDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSheetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSheetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNetSegmentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNetSegmentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetGraphIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetGraphIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTextIds(self, txttyp:int=0, search_string:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:txttyp [IN]: int Default value =0
		:search_string [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTextIds(dummy, txttyp, search_string)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def MoveTo(self, vari:int, before:int=0) -> int:
		"""
		:vari [IN]: int
		:before [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.MoveTo(vari, before)

	def Highlight(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Highlight()

	def ResetHighlight(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ResetHighlight()

	def IsHighlighted(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsHighlighted()

	def SetDescription(self, newval:str) -> int:
		"""
		:newval [IN]: str
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.SetDescription(newval)

	def GetFieldIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		dummy=0
		ret, ids = self._obj.GetFieldIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsPackage(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.IsPackage()

	def IsConfiguration(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.IsConfiguration()

	def CreatePackage(self, name:str, posId:int, before:int) -> int:
		"""
		:name [IN]: str
		:posId [IN]: int
		:before [IN]: int
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.CreatePackage(name, posId, before)

	def CreateConfiguration(self, name:str, posId:int, before:int) -> int:
		"""
		:name [IN]: str
		:posId [IN]: int
		:before [IN]: int
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.CreateConfiguration(name, posId, before)

	def ActivateAndLockOtherActivations(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.ActivateAndLockOtherActivations()

	def UnLockOtherActivations(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.UnLockOtherActivations()

	def GetInclusiveOptionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		dummy=0
		ret, ids = self._obj.GetInclusiveOptionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetExclusiveOptionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		dummy=0
		ret, ids = self._obj.GetExclusiveOptionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def AssignToID(self, parentid:int, how:int) -> int:
		"""
		:parentid [IN]: int
		:how [IN]: int
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.AssignToID(parentid, how)

	def UnassignFromID(self, parentid:int) -> int:
		"""
		:parentid [IN]: int
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.UnassignFromID(parentid)

	def SetXMLVariantID(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		return self._obj.SetXMLVariantID(name)

	def GetXMLVariantID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.30
		"""
		return self._obj.GetXMLVariantID()

	def IsObjectActive(self, objid:int) -> int:
		"""
		:objid [IN]: int
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.IsObjectActive(objid)

	def IsHarnessFamily(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.IsHarnessFamily()

	def IsHarnessDerivative(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.IsHarnessDerivative()

	def CreateHarnessFamily(self, name:str, posId:int, before:int) -> int:
		"""
		:name [IN]: str
		:posId [IN]: int
		:before [IN]: int
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.CreateHarnessFamily(name, posId, before)

	def CreateHarnessDerivative(self, name:str, posId:int, before:int) -> int:
		"""
		:name [IN]: str
		:posId [IN]: int
		:before [IN]: int
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.CreateHarnessDerivative(name, posId, before)

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		return self._obj.AddAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		return self._obj.DeleteAttribute(name)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 16.00
		"""
		return self._obj.GetAttributeValue(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		return self._obj.HasAttribute(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		return self._obj.SetAttributeValue(name, value)

	def Sort(self, sortMode:int=0) -> int:
		"""
		:sortMode [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		return self._obj.Sort(sortMode)

	def GetAllDeviantAttributeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 17.04
		"""
		dummy=0
		ret, ids = self._obj.GetAllDeviantAttributeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsInUseByObject(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.15
		"""
		return self._obj.IsInUseByObject()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

# -------------------- IOutlineInterface--------------------
class Outline:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Outline. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def GetType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetType()

	def GetPosition(self) -> tuple[int, float, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetPosition(dummy, dummy, dummy)

	def GetRadius(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetRadius()

	def GetHeight(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetHeight()

	def GetSymbolCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSymbolCount()

	def GetSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTypeId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTypeId()

	def GetPathEx(self) -> tuple[int, tuple[float,...], tuple[float,...], tuple[float,...]]:
		"""
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:zarr [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, xarr, yarr, zarr = self._obj.GetPathEx(dummy, dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		zarr = zarr[1:] if type(zarr) == tuple and len(zarr) > 0 else tuple()
		return ret, xarr, yarr, zarr

	def UseInE3CutOut(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 14.11
		"""
		return self._obj.UseInE3CutOut()

	def SetUseInE3CutOut(self, set:bool) -> int:
		"""
		:set [IN]: bool
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.SetUseInE3CutOut(set)

	def UseCutOutGraphic(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 21.10
		"""
		return self._obj.UseCutOutGraphic()

	def SetUseCutOutGraphic(self, set:bool) -> int:
		"""
		:set [IN]: bool
		:Return: int

		Available since TLB-Versions: 21.10
		"""
		return self._obj.SetUseCutOutGraphic(set)

	def IsThreadedHole(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.31
		"""
		return self._obj.IsThreadedHole()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def SetCreatesThreadedHole(self, set:bool, flags:int=0) -> int:
		"""
		:set [IN]: bool
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00
		"""
		return self._obj.SetCreatesThreadedHole(set, flags)

# -------------------- ISheetInterface--------------------
class Sheet:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Sheet. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def SetName(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetName(name)

	def Remove(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Remove()

	def Visible(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Visible()

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete()

	def GetDrawingArea(self) -> tuple[int, float, float, float, float]:
		"""
		:xmin [OUT]: float
		:ymin [OUT]: float
		:xmax [OUT]: float
		:ymax [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetDrawingArea(dummy, dummy, dummy, dummy)

	def GetTextCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTextCount()

	def GetTextIds(self, txttyp:int=0, search_string:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:txttyp [IN]: int Default value =0
		:search_string [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTextIds(dummy, txttyp, search_string)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSymbolCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSymbolCount()

	def GetSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def Create(self, modi:int, name:str, symbol:str, position:int, before:int) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:symbol [IN]: str
		:position [IN]: int
		:before [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Create(modi, name, symbol, position, before)

	def CreatePanel(self, modi:int, name:str, symbol:str, position:int, before:int, refx:float, refy:float, refscale:float) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:symbol [IN]: str
		:position [IN]: int
		:before [IN]: int
		:refx [IN]: float
		:refy [IN]: float
		:refscale [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreatePanel(modi, name, symbol, position, before, refx, refy, refscale)

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def Search(self, modi:int, name:str) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Search(modi, name)

	def GetGraphCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphCount()

	def GetGraphIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetGraphIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetModuleCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetModuleCount()

	def GetModuleIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetModuleIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def PlacePart(self, name:str, version:str, x:float, y:float, rot:float) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PlacePart(name, version, x, y, rot)

	def GetNetSegmentCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetNetSegmentCount()

	def GetNetSegmentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNetSegmentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def PrintOut(self, scale:float) -> int:
		"""
		:scale [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PrintOut(scale)

	def Export(self, format:str, version:int, file:str, flags:int=0) -> int:
		"""
		:format [IN]: str
		:version [IN]: int
		:file [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Export(format, version, file, flags)

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasAttribute(name)

	def ImportDXF(self, filename:str, scale:float, x:float, y:float, rot:int, font:str, flags:int=0) -> int:
		"""
		:filename [IN]: str
		:scale [IN]: float
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: int
		:font [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ImportDXF(filename, scale, x, y, rot, font, flags)

	def GetAssignment(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAssignment()

	def SetAssignment(self, newass:str) -> int:
		"""
		:newass [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAssignment(newass)

	def GetLocation(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLocation()

	def SetLocation(self, newloc:str) -> int:
		"""
		:newloc [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLocation(newloc)

	def SetCompleteName(self, newnam:str, newass:str, newloc:str) -> int:
		"""
		:newnam [IN]: str
		:newass [IN]: str
		:newloc [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetCompleteName(newnam, newass, newloc)

	def GetOpenNetsegmentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetOpenNetsegmentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetEmbeddedSheetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetEmbeddedSheetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsEmbedded(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsEmbedded()

	def GetParentSheetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetParentSheetId()

	def ExportImageArea(self, format:str, version:int, file:str, xl:float, yl:float, xr:float, yr:float, width:int, height:int, clrdepth:int, gray:int, dpiX:int, dpiY:int, compressionmode:int) -> int:
		"""
		:format [IN]: str
		:version [IN]: int
		:file [IN]: str
		:xl [IN]: float
		:yl [IN]: float
		:xr [IN]: float
		:yr [IN]: float
		:width [IN]: int
		:height [IN]: int
		:clrdepth [IN]: int
		:gray [IN]: int
		:dpiX [IN]: int
		:dpiY [IN]: int
		:compressionmode [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ExportImageArea(format, version, file, xl, yl, xr, yr, width, height, clrdepth, gray, dpiX, dpiY, compressionmode)

	def ExportImage(self, format:str, version:int, file:str, dpi:int=0, compressionmode:int=0) -> int:
		"""
		:format [IN]: str
		:version [IN]: int
		:file [IN]: str
		:dpi [IN]: int Default value =0
		:compressionmode [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ExportImage(format, version, file, dpi, compressionmode)

	def ExportImageSelection(self, format:str, version:int, file:str, percentage:int, width:int, height:int, clrdepth:int, gray:int, dpiX:int, dpiY:int, compressionmode:int) -> int:
		"""
		:format [IN]: str
		:version [IN]: int
		:file [IN]: str
		:percentage [IN]: int
		:width [IN]: int
		:height [IN]: int
		:clrdepth [IN]: int
		:gray [IN]: int
		:dpiX [IN]: int
		:dpiY [IN]: int
		:compressionmode [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ExportImageSelection(format, version, file, percentage, width, height, clrdepth, gray, dpiX, dpiY, compressionmode)

	def SetFormat(self, sym:str, rot:str="") -> int:
		"""
		:sym [IN]: str
		:rot [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFormat(sym, rot)

	def GetFormat(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFormat()

	def GetPanelConnectionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetPanelConnectionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetRedlinedGraphTextIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetRedlinedGraphTextIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetRedlinedGraphIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetRedlinedGraphIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateBoard(self, brdi:int, name:str, symbol:str, position:int, before:int, refx:float, refy:float, refscale:float) -> int:
		"""
		:brdi [IN]: int
		:name [IN]: str
		:symbol [IN]: str
		:position [IN]: int
		:before [IN]: int
		:refx [IN]: float
		:refy [IN]: float
		:refscale [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateBoard(brdi, name, symbol, position, before, refx, refy, refscale)

	def GetInsideSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetInsideSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetInsideGraphIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetInsideGraphIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetInsidePanelConnectionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetInsidePanelConnectionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def ShareWithID(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ShareWithID(id)

	def IsShared(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsShared()

	def GetBaseId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBaseId()

	def GetSharedIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSharedIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetVisibleArea(self) -> tuple[int, tuple[float,...], tuple[float,...], tuple[float,...], tuple[float,...]]:
		"""
		:xmin [OUT]: tuple[float,...]
		:ymin [OUT]: tuple[float,...]
		:xmax [OUT]: tuple[float,...]
		:ymax [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, xmin, ymin, xmax, ymax = self._obj.GetVisibleArea(dummy, dummy, dummy, dummy)
		xmin = xmin[1:] if type(xmin) == tuple and len(xmin) > 0 else tuple()
		ymin = ymin[1:] if type(ymin) == tuple and len(ymin) > 0 else tuple()
		xmax = xmax[1:] if type(xmax) == tuple and len(xmax) > 0 else tuple()
		ymax = ymax[1:] if type(ymax) == tuple and len(ymax) > 0 else tuple()
		return ret, xmin, ymin, xmax, ymax

	def SetVisibleArea(self, xmin:float, ymin:float, xmax:float, ymax:float) -> int:
		"""
		:xmin [IN]: float
		:ymin [IN]: float
		:xmax [IN]: float
		:ymax [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetVisibleArea(xmin, ymin, xmax, ymax)

	def IsReadOnly(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsReadOnly()

	def GetSchematicTypes(self) -> tuple[int, tuple[int,...]]:
		"""
		:types [OUT]: tuple[int,...], Enum type Available: e3series.types.SchematicType.
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, types = self._obj.GetSchematicTypes(dummy)
		types = types[1:] if type(types) == tuple and len(types) > 0 else tuple()
		return ret, types

	def GetAssignedOptionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAssignedOptionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def ToGrid(self, xpos:float, ypos:float) -> tuple[int, float, float]:
		"""
		:xpos [IN/OUT]: float
		:ypos [IN/OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ToGrid(xpos, ypos)

	def MoveTo(self, position:int, before:int=0) -> int:
		"""
		:position [IN]: int
		:before [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.MoveTo(position, before)

	def GetContentModified(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetContentModified()

	def SetContentModified(self, value:int) -> bool:
		"""
		:value [IN]: int
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetContentModified(value)

	def GetDimensionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetDimensionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def SetPanelRegion(self, xoff:float, yoff:float, scale:float) -> int:
		"""
		:xoff [IN]: float
		:yoff [IN]: float
		:scale [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPanelRegion(xoff, yoff, scale)

	def GetPanelRegion(self) -> tuple[int, float, float, float]:
		"""
		:xoff [OUT]: float
		:yoff [OUT]: float
		:scale [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetPanelRegion(dummy, dummy, dummy)

	def ImportDGN(self, filename:str, scale:float, x:float, y:float, rot:int, font:str, flags:int) -> int:
		"""
		:filename [IN]: str
		:scale [IN]: float
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: int
		:font [IN]: str
		:flags [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ImportDGN(filename, scale, x, y, rot, font, flags)

	def CreateFormboard(self, modi:int, name:str, symbol:str, position:int, before:int, flags:int) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:symbol [IN]: str
		:position [IN]: int
		:before [IN]: int
		:flags [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateFormboard(modi, name, symbol, position, before, flags)

	def IsFormboard(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsFormboard()

	def GetOwner(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetOwner()

	def IsClipboardPart(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsClipboardPart()

	def SetCharacteristic(self, characteristic:str) -> int:
		"""
		:characteristic [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetCharacteristic(characteristic)

	def GetCharacteristic(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCharacteristic()

	def GetValidCharacteristics(self) -> tuple[int, tuple[str,...]]:
		"""
		:characteristics [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, characteristics = self._obj.GetValidCharacteristics(dummy)
		characteristics = characteristics[1:] if type(characteristics) == tuple and len(characteristics) > 0 else tuple()
		return ret, characteristics

	def GetHyperlinkTextIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetHyperlinkTextIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetGroupIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetGroupIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsTerminalPlan(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsTerminalPlan()

	def GetWorkingArea(self) -> tuple[int, float, float, float, float]:
		"""
		:xmin [OUT]: float
		:ymin [OUT]: float
		:xmax [OUT]: float
		:ymax [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetWorkingArea(dummy, dummy, dummy, dummy)

	def SetSchematicTypes(self, types:list[int]) -> int:
		"""
		:types [IN]: list[int], Enum type Available: e3series.types.SchematicType.
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.SetSchematicTypes(types)
		return ret[0]

	def GetAssignedOptionExpressions(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressions(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def Is2DView(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.Is2DView()

	def CreateFunctionalDesign(self, modi:int, name:str, symbol:str, position:int, before:int, flags:int) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:symbol [IN]: str
		:position [IN]: int
		:before [IN]: int
		:flags [IN]: int
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.CreateFunctionalDesign(modi, name, symbol, position, before, flags)

	def IsFunctionalDesign(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 9.00
		"""
		return self._obj.IsFunctionalDesign()

	def GetGetterOptionHandlingMode(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetGetterOptionHandlingMode()

	def SetGetterOptionHandlingMode(self, mode:int) -> int:
		"""
		:mode [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetGetterOptionHandlingMode(mode)

	def SetOptionExpressions(self, expressions:list[str]) -> int:
		"""
		:expressions [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 9.12
		"""
		return self._obj.SetOptionExpressions(expressions)

	def SetCompleteNameEx(self, newnam:str, newass:str, newloc:str, onlygiven:bool) -> int:
		"""
		:newnam [IN]: str
		:newass [IN]: str
		:newloc [IN]: str
		:onlygiven [IN]: bool
		:Return: int

		Available since TLB-Versions: 9.20
		"""
		return self._obj.SetCompleteNameEx(newnam, newass, newloc, onlygiven)

	def GetAssignedOptionExpressionsEx(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 9.23
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressionsEx(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def GetRegionArea(self) -> tuple[int, float, float, float, float]:
		"""
		:xmin [OUT]: float
		:ymin [OUT]: float
		:xmax [OUT]: float
		:ymax [OUT]: float
		:Return: int

		Available since TLB-Versions: 9.30
		"""
		dummy=0
		return self._obj.GetRegionArea(dummy, dummy, dummy, dummy)

	def CreateTopology(self, modi:int, name:str, symbol:str, position:int, before:int, refscale:float) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:symbol [IN]: str
		:position [IN]: int
		:before [IN]: int
		:refscale [IN]: float
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.CreateTopology(modi, name, symbol, position, before, refscale)

	def IsTopology(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsTopology()

	def LockObject(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.LockObject()

	def UnlockObject(self, password:str) -> int:
		"""
		:password [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.UnlockObject(password)

	def IsLocked(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsLocked()

	def IsPanel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsPanel()

	def SetTopologyRegion(self, xoff:float, yoff:float, scale:float) -> int:
		"""
		:xoff [IN]: float
		:yoff [IN]: float
		:scale [IN]: float
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetTopologyRegion(xoff, yoff, scale)

	def GetTopologyRegion(self) -> tuple[int, float, float, float]:
		"""
		:xoff [OUT]: float
		:yoff [OUT]: float
		:scale [OUT]: float
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		return self._obj.GetTopologyRegion(dummy, dummy, dummy)

	def CreateFormboardEx(self, modi:int, name:str, symbol:str, position:int, before:int, refx:float, refy:float, refscale:float) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:symbol [IN]: str
		:position [IN]: int
		:before [IN]: int
		:refx [IN]: float
		:refy [IN]: float
		:refscale [IN]: float
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		return self._obj.CreateFormboardEx(modi, name, symbol, position, before, refx, refy, refscale)

	def SetSheetRegion(self, xoff:float, yoff:float, scale:float) -> int:
		"""
		:xoff [IN]: float
		:yoff [IN]: float
		:scale [IN]: float
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		return self._obj.SetSheetRegion(xoff, yoff, scale)

	def GetSheetRegion(self) -> tuple[int, float, float, float]:
		"""
		:xoff [OUT]: float
		:yoff [OUT]: float
		:scale [OUT]: float
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		dummy=0
		return self._obj.GetSheetRegion(dummy, dummy, dummy)

	def GetInsideNetSegmentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		dummy=0
		ret, ids = self._obj.GetInsideNetSegmentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsParentSheet(self, flags:int) -> int:
		"""
		:flags [IN]: int
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		return self._obj.IsParentSheet(flags)

	def PlacePartEx(self, name:str, version:str, flags:int, x:float, y:float, rot:float) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:flags [IN]: int
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: float
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.PlacePartEx(name, version, flags, x, y, rot)

	def CheckoutReadonlyReferencedSheets(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 11.80
		"""
		return self._obj.CheckoutReadonlyReferencedSheets()

	def GetOwners(self) -> tuple[int, tuple[int,...]]:
		"""
		:owners [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 17.16
		"""
		dummy=0
		ret, owners = self._obj.GetOwners(dummy)
		owners = owners[1:] if type(owners) == tuple and len(owners) > 0 else tuple()
		return ret, owners

	def AlignObjects(self, reference:int, ids:list[int], mode:int) -> int:
		"""
		:reference [IN]: int
		:ids [IN]: list[int]
		:mode [IN]: int
		:Return: int

		Available since TLB-Versions: 17.70
		"""
		return self._obj.AlignObjects(reference, ids, mode)

	def DisplayEx(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.DisplayEx(flags)

	def IsLockedByAccessControl(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.IsLockedByAccessControl()

	def CreateTopologyEx(self, modi:int, name:str, symbol:str, position:int, before:int, refx:float, refy:float, refscale:float, flags:int=0) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:symbol [IN]: str
		:position [IN]: int
		:before [IN]: int
		:refx [IN]: float
		:refy [IN]: float
		:refscale [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.CreateTopologyEx(modi, name, symbol, position, before, refx, refy, refscale, flags)

	def GetProduct(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 20.00, 19.34
		"""
		return self._obj.GetProduct()

	def SetProduct(self, newproduct:str) -> int:
		"""
		:newproduct [IN]: str
		:Return: int

		Available since TLB-Versions: 20.00, 19.34
		"""
		return self._obj.SetProduct(newproduct)

	def GetDXFSize(self, filename:str, font:str) -> tuple[int, float, float, float]:
		"""
		:filename [IN]: str
		:font [IN]: str
		:dx [OUT]: float
		:dy [OUT]: float
		:scale [OUT]: float
		:Return: int

		Available since TLB-Versions: 20.00, 19.01
		"""
		dummy=0
		return self._obj.GetDXFSize(filename, font, dummy, dummy, dummy)

	def SelectIds(self, symbolIds:list[int]) -> tuple[int, list[int]]:
		"""
		:symbolIds [IN]: list[int]
		:selectedIds [OUT]: list[int]
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		dummy=0
		ret, selectedIds = self._obj.SelectIds(symbolIds, dummy)
		selectedIds = [] if selectedIds is None else selectedIds
		selectedIds = selectedIds[1:] if type(selectedIds) == list and len(selectedIds) > 0 else []
		return ret, selectedIds

	def IsReadOnlyInProject(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 21.00, 20.70, 20.03, 19.31
		"""
		return self._obj.IsReadOnlyInProject()

	def SetReadOnlyInProject(self, readonlyproject:bool) -> int:
		"""
		:readonlyproject [IN]: bool
		:Return: int

		Available since TLB-Versions: 21.00, 20.70, 20.03, 19.31
		"""
		return self._obj.SetReadOnlyInProject(readonlyproject)

	def GetEmbeddedObjectIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		dummy=0
		ret, ids = self._obj.GetEmbeddedObjectIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def Get2DViewSheetDisplayOnlyBorder(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.Get2DViewSheetDisplayOnlyBorder()

	def Set2DViewSheetDisplayOnlyBorder(self, display_border:bool) -> int:
		"""
		:display_border [IN]: bool
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.Set2DViewSheetDisplayOnlyBorder(display_border)

	def GetSlotIdsFrom2DView(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 21.12
		"""
		dummy=0
		ret, ids = self._obj.GetSlotIdsFrom2DView(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

	def GetDisplayModelViewAtPosition(self, flags:int=0) -> tuple[int, float]:
		"""
		:view_distance [OUT]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.00
		"""
		dummy=0
		return self._obj.GetDisplayModelViewAtPosition(dummy, flags)

	def SetDisplayModelViewAtPosition(self, display_model_view_at_position:bool, view_distance:float, flags:int=0) -> int:
		"""
		:display_model_view_at_position [IN]: bool
		:view_distance [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.00
		"""
		return self._obj.SetDisplayModelViewAtPosition(display_model_view_at_position, view_distance, flags)

	def Get2DViewDisplayInOriginalOrientation(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 24.00
		"""
		return self._obj.Get2DViewDisplayInOriginalOrientation()

	def Get2DViewSheetDisplaySlots(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 25.00
		"""
		return self._obj.Get2DViewSheetDisplaySlots()

	def Set2DViewSheetDisplaySlots(self, display_slots:bool) -> int:
		"""
		:display_slots [IN]: bool
		:Return: int

		Available since TLB-Versions: 25.00
		"""
		return self._obj.Set2DViewSheetDisplaySlots(display_slots)

# -------------------- ISignalInterface--------------------
class Signal:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Signal. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetName(name)

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasAttribute(name)

	def SetAttributeVisibility(self, name:str, onoff:int) -> int:
		"""
		:name [IN]: str
		:onoff [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeVisibility(name, onoff)

	def Search(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Search(name)

	def GetNetSegmentCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetNetSegmentCount()

	def GetNetSegmentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNetSegmentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetPinCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPinCount()

	def GetPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def Highlight(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Highlight()

	def FindPanelPath(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.FindPanelPath()

	def DisplayAttributeValueAt(self, name:str, sheetid:int, x:float, y:float) -> int:
		"""
		:name [IN]: str
		:sheetid [IN]: int
		:x [IN]: float
		:y [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DisplayAttributeValueAt(name, sheetid, x, y)

	def GetDefaultWires(self) -> tuple[int, tuple[str,...], tuple[str,...]]:
		"""
		:wiregroups [OUT]: tuple[str,...]
		:wirenames [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, wiregroups, wirenames = self._obj.GetDefaultWires(dummy, dummy)
		wiregroups = wiregroups[1:] if type(wiregroups) == tuple and len(wiregroups) > 0 else tuple()
		wirenames = wirenames[1:] if type(wirenames) == tuple and len(wirenames) > 0 else tuple()
		return ret, wiregroups, wirenames

	def SetDefaultWires(self, wiregroups:list[str], wirenames:list[str]) -> int:
		"""
		:wiregroups [IN]: list[str]
		:wirenames [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.SetDefaultWires(wiregroups, wirenames)
		return ret[0]

	def GetCoreCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCoreCount()

	def GetCoreIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCoreIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSignalClassId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetSignalClassId()

	def Create(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		return self._obj.Create(name)

	def GetTranslatedName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 11.00
		"""
		return self._obj.GetTranslatedName()

	def HighlightCoreLogicLinesOfSignal(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		return self._obj.HighlightCoreLogicLinesOfSignal()

	def SetNameFormat(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		return self._obj.SetNameFormat(name)

	def GetNameFormat(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 16.00
		"""
		return self._obj.GetNameFormat()

	def SetRecalcFormattedName(self, recalculate:int) -> int:
		"""
		:recalculate [IN]: int
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		return self._obj.SetRecalcFormattedName(recalculate)

	def GetRecalcFormattedName(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		return self._obj.GetRecalcFormattedName()

	def AddDefaultWireEx(self, wiregroup:str, wirename:str) -> int:
		"""
		:wiregroup [IN]: str
		:wirename [IN]: str
		:Return: int

		Available since TLB-Versions: 19.12
		"""
		return self._obj.AddDefaultWireEx(wiregroup, wirename)

	def DeleteDefaultWireEx(self, wiregroup:str, wirename:str) -> int:
		"""
		:wiregroup [IN]: str
		:wirename [IN]: str
		:Return: int

		Available since TLB-Versions: 19.12
		"""
		return self._obj.DeleteDefaultWireEx(wiregroup, wirename)

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

# -------------------- ICavityPartInterface--------------------
class CavityPart:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize CavityPart. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetCavityPartType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.GetCavityPartType()

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.SetId(id)

	def GetValue(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 18.00
		"""
		return self._obj.GetValue()

	def SetValue(self, value:str) -> int:
		"""
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.SetValue(value)

	def GetOwner(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.GetOwner()

	def GetCabwirInfos(self) -> tuple[int, tuple[int,...]]:
		"""
		:cabWirs [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		dummy=0
		ret, cabWirs = self._obj.GetCabwirInfos(dummy)
		cabWirs = cabWirs[1:] if type(cabWirs) == tuple and len(cabWirs) > 0 else tuple()
		return ret, cabWirs

	def SetDisableAutomaticSelection(self, DisableAutomaticSelection:bool) -> int:
		"""
		:DisableAutomaticSelection [IN]: bool
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.SetDisableAutomaticSelection(DisableAutomaticSelection)

	def GetDisableAutomaticSelection(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.GetDisableAutomaticSelection()

	def Create(self, pinid:int, name:str, _type:int) -> int:
		"""
		:pinid [IN]: int
		:name [IN]: str
		:_type [IN]: int
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.Create(pinid, name, _type)

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 18.00
		"""
		return self._obj.GetAttributeValue(name)

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.AddAttributeValue(name, value)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.DeleteAttribute(name)

	def IsActive(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.IsActive()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

# -------------------- ISymbolInterface--------------------
class Symbol:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Symbol. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetName(name)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def GetVersion(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetVersion()

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttribute(name)

	def GetPinCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPinCount()

	def GetPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTextCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTextCount()

	def GetTextIds(self, txttyp:int=0, search_string:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:txttyp [IN]: int Default value =0
		:search_string [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTextIds(dummy, txttyp, search_string)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsShield(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsShield()

	def IsDynamic(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsDynamic()

	def GetSchemaLocation(self) -> tuple[int, float, float, str, str, str]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:grid [OUT]: str
		:column_value [OUT]: str
		:row_value [OUT]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetSchemaLocation(dummy, dummy, dummy, dummy, dummy)

	def Load(self, name:str, version:str) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Load(name, version)

	def GetArea(self) -> tuple[int, float, float, float, float]:
		"""
		:xmin [OUT]: float
		:ymin [OUT]: float
		:xmax [OUT]: float
		:ymax [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetArea(dummy, dummy, dummy, dummy)

	def Place(self, shti:int, x:float, y:float, rot:str="", scale:float=0, maintaintextsize:bool=False) -> int:
		"""
		:shti [IN]: int
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: str Default value =""
		:scale [IN]: float Default value =0
		:maintaintextsize [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Place(shti, x, y, rot, scale, maintaintextsize)

	def GetMasterCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetMasterCount()

	def GetMasterIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetMasterIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSlaveCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSlaveCount()

	def GetSlaveIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSlaveIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def Jump(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Jump()

	def SetDeviceName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDeviceName(name)

	def SetDeviceAssignment(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDeviceAssignment(name)

	def SetDeviceLocation(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDeviceLocation(name)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete()

	def GetCode(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCode()

	def GetSymbolCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSymbolCount()

	def GetSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetRotation(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetRotation()

	def GetScaling(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetScaling()

	def GetLevel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLevel()

	def IsConnectorMaster(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsConnectorMaster()

	def GetTypeName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTypeName()

	def IsConnected(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsConnected()

	def SetDeviceCompleteName(self, name:str, ass:str, loc:str, onlygiven:bool=True) -> int:
		"""
		:name [IN]: str
		:ass [IN]: str
		:loc [IN]: str
		:onlygiven [IN]: bool Default value =True
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDeviceCompleteName(name, ass, loc, onlygiven)

	def SetType(self, name:str, version:str) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetType(name, version)

	def GetType(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetType()

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasAttribute(name)

	def PlacePins(self, pinarray:list[int], symname:str, vers:str, shti:int, x:float, y:float, rot:str, scale:float=0) -> int:
		"""
		:pinarray [IN]: list[int]
		:symname [IN]: str
		:vers [IN]: str
		:shti [IN]: int
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: str
		:scale [IN]: float Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.PlacePins(pinarray, symname, vers, shti, x, y, rot, scale)
		return ret[0]

	def PlaceDynamic(self, shti:int, x:float, y:float, height:float, width:float, texttemplate:str="", fitsymbol:int=0) -> int:
		"""
		:shti [IN]: int
		:x [IN]: float
		:y [IN]: float
		:height [IN]: float
		:width [IN]: float
		:texttemplate [IN]: str Default value =""
		:fitsymbol [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PlaceDynamic(shti, x, y, height, width, texttemplate, fitsymbol)

	def HasPassWirePins(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasPassWirePins()

	def SetLevel(self, level:int) -> int:
		"""
		:level [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLevel(level)

	def SetAsMaster(self, on:int) -> int:
		"""
		:on [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAsMaster(on)

	def IsMaster(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsMaster()

	def PlaceBlock(self, shti:int, x:float, y:float, width:float, height:float, parent:int=0) -> int:
		"""
		:shti [IN]: int
		:x [IN]: float
		:y [IN]: float
		:width [IN]: float
		:height [IN]: float
		:parent [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PlaceBlock(shti, x, y, width, height, parent)

	def IsTwisted(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsTwisted()

	def IsBundle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsBundle()

	def GetTransformationMatrix(self) -> tuple[int, tuple[tuple[float,...],...]]:
		"""
		:array [OUT]: tuple[tuple[float,...],...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetTransformationMatrix(dummy)

	def GetSheetReferenceInfo(self) -> tuple[int, int, int, str, str]:
		"""
		:inout [OUT]: int
		:_type [OUT]: int
		:refnam [OUT]: str
		:signam [OUT]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetSheetReferenceInfo(dummy, dummy, dummy, dummy)

	def AddToSheetReference(self, symi:int) -> int:
		"""
		:symi [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddToSheetReference(symi)

	def GetSymbolTypeName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSymbolTypeName()

	def GetSchematicTypes(self) -> tuple[int, tuple[int,...]]:
		"""
		:types [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, types = self._obj.GetSchematicTypes(dummy)
		types = types[1:] if type(types) == tuple and len(types) > 0 else tuple()
		return ret, types

	def GetAssignedOptionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAssignedOptionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def PlaceInteractively(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PlaceInteractively()

	def AssignTo(self, assignto:int, nonodeassignment:int=0) -> int:
		"""
		:assignto [IN]: int
		:nonodeassignment [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AssignTo(assignto, nonodeassignment)

	def PlaceAsGraphic(self, shti:int, x:float, y:float, rot:str, scale:float, maintaintextsize:bool, srcid:int) -> int:
		"""
		:shti [IN]: int
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: str
		:scale [IN]: float
		:maintaintextsize [IN]: bool
		:srcid [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PlaceAsGraphic(shti, x, y, rot, scale, maintaintextsize, srcid)

	def GetGateId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGateId()

	def SetGateId(self, symid:int) -> int:
		"""
		:symid [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGateId(symid)

	def SetCharacteristic(self, characteristic:str) -> int:
		"""
		:characteristic [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetCharacteristic(characteristic)

	def GetCharacteristic(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCharacteristic()

	def GetValidCharacteristics(self) -> tuple[int, tuple[str,...]]:
		"""
		:characteristics [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, characteristics = self._obj.GetValidCharacteristics(dummy)
		characteristics = characteristics[1:] if type(characteristics) == tuple and len(characteristics) > 0 else tuple()
		return ret, characteristics

	def IsBlock(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsBlock()

	def SetBlockOutlineColour(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockOutlineColour(value)

	def GetBlockOutlineColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockOutlineColour()

	def SetBlockOutlineStyle(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockOutlineStyle(value)

	def GetBlockOutlineStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockOutlineStyle()

	def SetBlockOutlineWidth(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockOutlineWidth(value)

	def GetBlockOutlineWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockOutlineWidth()

	def SetBlockHatchPattern(self, value:int, angle1:float, angle2:float) -> int:
		"""
		:value [IN]: int
		:angle1 [IN]: float
		:angle2 [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockHatchPattern(value, angle1, angle2)

	def GetBlockHatchPattern(self) -> tuple[int, float, float]:
		"""
		:angle1 [OUT]: float
		:angle2 [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetBlockHatchPattern(dummy, dummy)

	def SetBlockHatchColour(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockHatchColour(value)

	def GetBlockHatchColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockHatchColour()

	def SetBlockHatchStyle(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockHatchStyle(value)

	def GetBlockHatchStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockHatchStyle()

	def SetBlockHatchWidth(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockHatchWidth(value)

	def GetBlockHatchWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockHatchWidth()

	def SetBlockHatchDistance(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockHatchDistance(value)

	def GetBlockHatchDistance(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockHatchDistance()

	def GetGroupId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGroupId()

	def Ungroup(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Ungroup()

	def IsFormboard(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsFormboard()

	def PlaceTable(self, fromid:int, x:float, y:float, rot:str="", scale:float=0, maintaintextsize:bool=False) -> int:
		"""
		:fromid [IN]: int
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: str Default value =""
		:scale [IN]: float Default value =0
		:maintaintextsize [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PlaceTable(fromid, x, y, rot, scale, maintaintextsize)

	def IsPinView(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsPinView()

	def PlacePinView(self, pinid:int, shti:int, symname:str, version:str, x:float, y:float, rot:str, scale:float=0, maintaintextsize:bool=False) -> int:
		"""
		:pinid [IN]: int
		:shti [IN]: int
		:symname [IN]: str
		:version [IN]: str
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: str
		:scale [IN]: float Default value =0
		:maintaintextsize [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PlacePinView(pinid, shti, symname, version, x, y, rot, scale, maintaintextsize)

	def GetDynamicParentId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDynamicParentId()

	def GetDynamicChildrenIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetDynamicChildrenIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsDynamicFixed(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsDynamicFixed()

	def SetScaling(self, scale:float) -> float:
		"""
		:scale [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetScaling(scale)

	def SetDBTextSize(self, txtsiz:bool) -> int:
		"""
		:txtsiz [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDBTextSize(txtsiz)

	def GetDBTextSize(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDBTextSize()

	def GetBoundIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetBoundIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetHyperlinkTextIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetHyperlinkTextIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetDisplayLength(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayLength()

	def GetDisplayWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayWidth()

	def SetDisplayLength(self, length:float) -> int:
		"""
		:length [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayLength(length)

	def SetDisplayWidth(self, width:float) -> int:
		"""
		:width [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayWidth(width)

	def GetPlacedArea(self) -> tuple[int, float, float, float, float]:
		"""
		:xmin [OUT]: float
		:ymin [OUT]: float
		:xmax [OUT]: float
		:ymax [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetPlacedArea(dummy, dummy, dummy, dummy)

	def GetAssignedOptionExpressions(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressions(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def HasNoGraphic(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.HasNoGraphic()

	def GetDevicePinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetDevicePinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSharedPinGroupState(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetSharedPinGroupState()

	def SetSharedPinGroupState(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetSharedPinGroupState(newval)

	def SetOptionExpressions(self, expressions:list[str]) -> int:
		"""
		:expressions [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 9.12
		"""
		return self._obj.SetOptionExpressions(expressions)

	def IsProtection(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.22
		"""
		return self._obj.IsProtection()

	def GetAssignedOptionExpressionsEx(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 9.23
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressionsEx(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def AssignFunctionalPorts(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		ret = self._obj.AssignFunctionalPorts(ids)
		return ret[0]

	def GetTargetObjectId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		return self._obj.GetTargetObjectId()

	def GetReferenceTextExtent(self) -> tuple[int, tuple[float,...], tuple[float,...]]:
		"""
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 10.40
		"""
		dummy=0
		ret, xarr, yarr = self._obj.GetReferenceTextExtent(dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		return ret, xarr, yarr

	def GetReferenceTextExtentSingleLine(self) -> tuple[int, int, tuple[float,...], tuple[float,...]]:
		"""
		:nlines [OUT]: int
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 10.40
		"""
		dummy=0
		return self._obj.GetReferenceTextExtentSingleLine(dummy, dummy, dummy)

	def GetReferenceText(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.41
		"""
		return self._obj.GetReferenceText()

	def GetReferenceTextSingleLine(self) -> tuple[int, tuple[str,...]]:
		"""
		:textarr [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 10.41
		"""
		dummy=0
		ret, textarr = self._obj.GetReferenceTextSingleLine(dummy)
		textarr = textarr[1:] if type(textarr) == tuple and len(textarr) > 0 else tuple()
		return ret, textarr

	def GetSymbolExtend(self) -> tuple[int, tuple[float,...], tuple[float,...]]:
		"""
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 10.46
		"""
		dummy=0
		ret, xarr, yarr = self._obj.GetSymbolExtend(dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		return ret, xarr, yarr

	def GetSchemaLocationShared(self, shtid:int) -> tuple[int, float, float, str, str, str]:
		"""
		:shtid [IN]: int
		:x [OUT]: float
		:y [OUT]: float
		:grid [OUT]: str
		:column_value [OUT]: str
		:row_value [OUT]: str
		:Return: int

		Available since TLB-Versions: 11.20
		"""
		dummy=0
		return self._obj.GetSchemaLocationShared(shtid, dummy, dummy, dummy, dummy, dummy)

	def GetPlacedPolygon(self) -> tuple[int, int, tuple[int,...], tuple[int,...]]:
		"""
		:npnts [OUT]: int
		:xarr [OUT]: tuple[int,...]
		:yarr [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		dummy=0
		ret, npnts, xarr, yarr = self._obj.GetPlacedPolygon(dummy, dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		return ret, npnts, xarr, yarr

	def RemoveFromSheetReference(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 17.33
		"""
		return self._obj.RemoveFromSheetReference()

	def GetSymbolTypeId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.23
		"""
		return self._obj.GetSymbolTypeId()

	def GetTableOneRowForEachCore(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetTableOneRowForEachCore()

	def SetTableOneRowForEachCore(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetTableOneRowForEachCore(newval)

	def GetTablePinsWithoutCores(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetTablePinsWithoutCores()

	def SetTablePinsWithoutCores(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetTablePinsWithoutCores(newval)

	def GetTableBreakTableAfter(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetTableBreakTableAfter()

	def SetTableBreakTableAfter(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetTableBreakTableAfter(newval)

	def GetTableBreakTableAfterNumberOfRows(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetTableBreakTableAfterNumberOfRows()

	def SetTableBreakTableAfterNumberOfRows(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetTableBreakTableAfterNumberOfRows(newval)

	def GetSubType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetSubType()

	def SendToForeground(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 20.00, 19.01, 18.33, 17.43
		"""
		return self._obj.SendToForeground()

	def SendToBackground(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 20.00, 19.01, 18.33, 17.43
		"""
		return self._obj.SendToBackground()

	def GetSymbolType(self) -> int:
		"""
		:Return: int, Enum type Available: e3series.types.SymbolType.

		Available since TLB-Versions: 20.00, 19.01
		"""
		return self._obj.GetSymbolType()

	def AssignToConnector(self, AssignToPinIds:list[int], AssignToPinIds_connected:list[int], flags:list[int]) -> int:
		"""
		:AssignToPinIds [IN]: list[int]
		:AssignToPinIds_connected [IN]: list[int]
		:flags [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 21.00, 20.01, 19.31
		"""
		return self._obj.AssignToConnector(AssignToPinIds, AssignToPinIds_connected, flags)

	def SetSelected(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.SetSelected(newval)

	def ModifyBlockSize(self, border:int, delta:float, flags:int=0) -> int:
		"""
		:border [IN]: int
		:delta [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 21.12
		"""
		return self._obj.ModifyBlockSize(border, delta, flags)

	def SetStateId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 22.10
		"""
		return self._obj.SetStateId(id)

	def GetStateId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 22.10
		"""
		return self._obj.GetStateId()

	def GetStateIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 22.10
		"""
		dummy=0
		ret, ids = self._obj.GetStateIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

# -------------------- ITextInterface--------------------
class Text:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Text. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetId(id)

	def GetType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetType()

	def GetText(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetText()

	def SetText(self, newtext:str) -> int:
		"""
		:newtext [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetText(newtext)

	def GetSchemaLocation(self) -> tuple[int, float, float, str, str, str]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:grid [OUT]: str
		:column_value [OUT]: str
		:row_value [OUT]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		return self._obj.GetSchemaLocation(dummy, dummy, dummy, dummy, dummy)

	def GetLeftJustifiedSchemaLocation(self) -> tuple[int, float, float, str]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:grid [OUT]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		return self._obj.GetLeftJustifiedSchemaLocation(dummy, dummy, dummy)

	def GetHeight(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetHeight()

	def SetHeight(self, newval:float) -> int:
		"""
		:newval [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetHeight(newval)

	def GetLevel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetLevel()

	def SetLevel(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetLevel(newval)

	def GetMode(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetMode()

	def SetMode(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetMode(newval)

	def GetStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetStyle()

	def SetStyle(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetStyle(newval)

	def GetColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetColour()

	def SetColour(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetColour(newval)

	def GetFontName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetFontName()

	def SetFontName(self, newname:str) -> int:
		"""
		:newname [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetFontName(newname)

	def GetVisibility(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetVisibility()

	def SetVisibility(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetVisibility(newval)

	def GetRotation(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetRotation()

	def GetLanguageID(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetLanguageID()

	def SetLanguageID(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetLanguageID(newval)

	def GetAssignedOptionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetAssignedOptionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAlignment(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetAlignment()

	def SetAlignment(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetAlignment(newval)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.Delete()

	def GetTypeId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetTypeId()

	def SetSchemaLocation(self, x:float, y:float) -> int:
		"""
		:x [IN]: float
		:y [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetSchemaLocation(x, y)

	def GetInternalText(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetInternalText()

	def GetRightJustifiedSchemaLocation(self) -> tuple[int, float, float, str]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:grid [OUT]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		return self._obj.GetRightJustifiedSchemaLocation(dummy, dummy, dummy)

	def GetWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetWidth()

	def SetBallooning(self, onoff:bool, _type:int) -> int:
		"""
		:onoff [IN]: bool
		:_type [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetBallooning(onoff, _type)

	def GetBallooning(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetBallooning()

	def IsRedlined(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.IsRedlined()

	def GetAllowedLength(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetAllowedLength()

	def SetRotation(self, rotation:float) -> float:
		"""
		:rotation [IN]: float
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetRotation(rotation)

	def GetSingleLine(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetSingleLine()

	def SetSingleLine(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetSingleLine(newval)

	def GetBox(self) -> tuple[int, float, float]:
		"""
		:xsize [OUT]: float
		:ysize [OUT]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		return self._obj.GetBox(dummy, dummy)

	def SetBox(self, xsize:float, ysize:float) -> int:
		"""
		:xsize [IN]: float
		:ysize [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetBox(xsize, ysize)

	def DeleteBox(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.DeleteBox()

	def GetLocking(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetLocking()

	def SetLocking(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetLocking(newval)

	def GetHyperlinkAddress(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetHyperlinkAddress()

	def SetHyperlinkAddress(self, newtext:str) -> int:
		"""
		:newtext [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetHyperlinkAddress(newtext)

	def CalculateBoxAt(self, shti:int, text:str, x:float, y:float, rotation:float, height:float, mode:int, style:int, fontname:str, just:int, balloon:int) -> tuple[int, tuple[float,...], tuple[float,...]]:
		"""
		:shti [IN]: int
		:text [IN]: str
		:x [IN]: float
		:y [IN]: float
		:rotation [IN]: float
		:height [IN]: float
		:mode [IN]: int
		:style [IN]: int
		:fontname [IN]: str
		:just [IN]: int
		:balloon [IN]: int
		:bx [OUT]: tuple[float,...]
		:by [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, bx, by = self._obj.CalculateBoxAt(shti, text, x, y, rotation, height, mode, style, fontname, just, balloon, dummy, dummy)
		bx = bx[1:] if type(bx) == tuple and len(bx) > 0 else tuple()
		by = by[1:] if type(by) == tuple and len(by) > 0 else tuple()
		return ret, bx, by

	def SetOptionExpressions(self, expressions:list[str]) -> int:
		"""
		:expressions [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 9.12
		"""
		return self._obj.SetOptionExpressions(expressions)

	def GetAssignedOptionExpressionsEx(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 9.23
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressionsEx(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def GetTextExtent(self) -> tuple[int, tuple[float,...], tuple[float,...]]:
		"""
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 10.40
		"""
		dummy=0
		ret, xarr, yarr = self._obj.GetTextExtent(dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		return ret, xarr, yarr

	def GetTextExtentSingleLine(self) -> tuple[int, int, tuple[tuple[float,...],...], tuple[tuple[float,...],...]]:
		"""
		:nlines [OUT]: int
		:xarr [OUT]: tuple[tuple[float,...],...]
		:yarr [OUT]: tuple[tuple[float,...],...]
		:Return: int

		Available since TLB-Versions: 10.40
		"""
		dummy=0
		ret, nlines, xarr, yarr = self._obj.GetTextExtentSingleLine(dummy, dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		return ret, nlines, xarr, yarr

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.AddAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.DeleteAttribute(name)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 11.00
		"""
		return self._obj.GetAttributeValue(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.HasAttribute(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.SetAttributeValue(name, value)

	def SetRedlined(self, onoff:bool) -> int:
		"""
		:onoff [IN]: bool Default value =TRUE
		:Return: int

		Available since TLB-Versions: 17.04
		"""
		return self._obj.SetRedlined(onoff)

	def GetPictogram(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 17.70
		"""
		return self._obj.GetPictogram()

	def SetPictogram(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 17.70
		"""
		return self._obj.SetPictogram(newval)

	def GetLinearMeasureWithoutUnit(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 17.70
		"""
		return self._obj.GetLinearMeasureWithoutUnit()

	def SetLinearMeasureWithoutUnit(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 17.70
		"""
		return self._obj.SetLinearMeasureWithoutUnit(newval)

	def CalculateBoxHeightEx(self, width:float, text:str, fontName:str, fontSize:float, fontMode:int, fontStyle:int) -> tuple[int, float, float, int]:
		"""
		:width [IN]: float
		:text [IN]: str
		:fontName [IN]: str
		:fontSize [IN]: float
		:fontMode [IN]: int
		:fontStyle [IN]: int
		:recHeight [OUT]: float
		:recWidth [OUT]: float
		:lines [OUT]: int
		:Return: int

		Available since TLB-Versions: 18.12, 17.33
		"""
		dummy=0
		return self._obj.CalculateBoxHeightEx(width, text, fontName, fontSize, fontMode, fontStyle, dummy, dummy, dummy)

	def SendToForeground(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.12
		"""
		return self._obj.SendToForeground()

	def SendToBackground(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.12
		"""
		return self._obj.SendToBackground()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

# -------------------- IVariantInterface--------------------
class Variant:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Variant. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 3.00
		"""
		return self._obj.GetName()

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.SetName(name)

	def Create(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.Create(name)

	def Delete(self, _del:int) -> int:
		"""
		:_del [IN]: int
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.Delete(_del)

	def Search(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.Search(name)

	def IsActive(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 3.00
		"""
		return self._obj.IsActive()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

# -------------------- ISlotInterface--------------------
class Slot:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Slot. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.SetId(id)

	def GetMountType(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.00
		"""
		return self._obj.GetMountType()

	def GetFixType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.GetFixType()

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.00
		"""
		return self._obj.GetName()

	def GetPosition(self, point:int) -> tuple[int, float, float, float]:
		"""
		:point [IN]: int
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		dummy=0
		return self._obj.GetPosition(point, dummy, dummy, dummy)

	def GetMountedDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 19.22
		"""
		dummy=0
		ret, ids = self._obj.GetMountedDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetDirection(self) -> tuple[int, float, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		dummy=0
		return self._obj.GetDirection(dummy, dummy, dummy)

	def GetRotation(self) -> tuple[int, float]:
		"""
		:angle [OUT]: float
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		dummy=0
		return self._obj.GetRotation(dummy)

	def GetDefinedDirection(self) -> tuple[int, float, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:Return: int

		Available since TLB-Versions: 21.12
		"""
		dummy=0
		return self._obj.GetDefinedDirection(dummy, dummy, dummy)

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetSlotName(self, flags:int=0) -> str:
		"""
		:flags [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 24.11
		"""
		return self._obj.GetSlotName(flags)

	def GetAreaPolygon(self, flags:int=0) -> tuple[int, float, float, float]:
		"""
		:xarr [OUT]: float
		:yarr [OUT]: float
		:zarr [OUT]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.30
		"""
		dummy=0
		return self._obj.GetAreaPolygon(dummy, dummy, dummy, flags)

	def SetMountType(self, newval:str, flags:int=0) -> int:
		"""
		:newval [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00
		"""
		return self._obj.SetMountType(newval, flags)

	def GetDefinedRotation(self, flags:int=0) -> tuple[int, float]:
		"""
		:angle [OUT]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.01
		"""
		dummy=0
		return self._obj.GetDefinedRotation(dummy, flags)

# -------------------- INetInterface--------------------
class Net:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Net. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasAttribute(name)

	def SetAttributeVisibility(self, name:str, onoff:int) -> int:
		"""
		:name [IN]: str
		:onoff [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeVisibility(name, onoff)

	def DisplayAttributeValueAt(self, name:str, sheetid:int, x:float, y:float) -> int:
		"""
		:name [IN]: str
		:sheetid [IN]: int
		:x [IN]: float
		:y [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DisplayAttributeValueAt(name, sheetid, x, y)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def GetParentId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetParentId()

	def GetNetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNetSegmentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNetSegmentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsSignalTransferred(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsSignalTransferred()

	def SetTransferSignal(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetTransferSignal(value)

	def GetPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetCoreIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCoreIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetHarnessId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetHarnessId()

	def SplitHarness(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SplitHarness()

	def GetSignalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 15.10
		"""
		return self._obj.GetSignalName()

	def GetTranslatedSignalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 15.10
		"""
		return self._obj.GetTranslatedSignalName()

	def SetSignalName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 15.10
		"""
		return self._obj.SetSignalName(name)

	def SetSignalNameOnLocalNet(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 15.10
		"""
		return self._obj.SetSignalNameOnLocalNet(name)

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

# -------------------- IUserMenuItemInterface--------------------
class UserMenuItem:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize UserMenuItem. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def Create(self, id:int, text:str, command:str, parameters:str, folder:str, image:str, shortcut:str, visible:int, wait:int, flags:int=1) -> int:
		"""
		:id [IN]: int
		:text [IN]: str
		:command [IN]: str
		:parameters [IN]: str
		:folder [IN]: str
		:image [IN]: str
		:shortcut [IN]: str
		:visible [IN]: int
		:wait [IN]: int
		:flags [IN]: int Default value =1
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Create(id, text, command, parameters, folder, image, shortcut, visible, wait, flags)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete()

	def GetText(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetText()

	def SetText(self, newval:str) -> int:
		"""
		:newval [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetText(newval)

	def GetCommand(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCommand()

	def SetCommand(self, newval:str) -> int:
		"""
		:newval [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetCommand(newval)

	def GetParameters(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetParameters()

	def SetParameters(self, newval:str) -> int:
		"""
		:newval [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetParameters(newval)

	def GetFolder(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFolder()

	def SetFolder(self, newval:str) -> int:
		"""
		:newval [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFolder(newval)

	def GetImage(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetImage()

	def SetImage(self, newval:str) -> int:
		"""
		:newval [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetImage(newval)

	def GetShortCut(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetShortCut()

	def SetShortCut(self, newval:str) -> int:
		"""
		:newval [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetShortCut(newval)

	def GetVisible(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetVisible()

	def SetVisible(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetVisible(newval)

	def GetEnable(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetEnable()

	def SetEnable(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetEnable(newval)

	def GetWaitForEndOfCommand(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetWaitForEndOfCommand()

	def SetWaitForEndOfCommand(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetWaitForEndOfCommand(newval)

	def CreateSeparator(self, text:str) -> int:
		"""
		:text [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateSeparator(text)

	def CreateUserTool(self, text:str, command:str) -> int:
		"""
		:text [IN]: str
		:command [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateUserTool(text, command)

	def UpdateUserInterface(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateUserInterface()

	def CreateContextUserTool(self, text:str, command:str) -> int:
		"""
		:text [IN]: str
		:command [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateContextUserTool(text, command)

	def CreateContextSeparator(self, text:str) -> int:
		"""
		:text [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateContextSeparator(text)

	def DeleteContext(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteContext()

	def IsDeleted(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsDeleted()

	def UnDelete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UnDelete()

	def GetType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetType()

	def GetDescription(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDescription()

	def SetDescription(self, newval:str) -> int:
		"""
		:newval [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDescription(newval)

	def DeleteUserTool(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.DeleteUserTool()

# -------------------- IStructureNodeInterface--------------------
class StructureNode:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize StructureNode. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def GetParentId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetParentId()

	def GetTypeName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTypeName()

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetName(name)

	def Create(self, name:str, typname:str, parentid:int, afterid:int) -> int:
		"""
		:name [IN]: str
		:typname [IN]: str
		:parentid [IN]: int
		:afterid [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Create(name, typname, parentid, afterid)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete()

	def GetStructureNodeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetStructureNodeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSheetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSheetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetExternalDocumentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetExternalDocumentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAllDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAllDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasAttribute(name)

	def MoveTo(self, parentId:int, afterId:int=0) -> int:
		"""
		:parentId [IN]: int
		:afterId [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.MoveTo(parentId, afterId)

	def SetStructureNodeIds(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.SetStructureNodeIds(ids)
		return ret[0]

	def SetSheetIds(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.SetSheetIds(ids)
		return ret[0]

	def SetExternalDocumentIds(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.SetExternalDocumentIds(ids)
		return ret[0]

	def IsObjectTypeAllowed(self, sheets:bool, devices:bool) -> int:
		"""
		:sheets [IN]: bool
		:devices [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsObjectTypeAllowed(sheets, devices)

	def GetInternalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetInternalName()

	def GetAllSignalIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.20
		"""
		dummy=0
		ret, ids = self._obj.GetAllSignalIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def Highlight(self, colour:int, width:float) -> int:
		"""
		:colour [IN]: int
		:width [IN]: float
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		return self._obj.Highlight(colour, width)

	def ResetHighlight(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		return self._obj.ResetHighlight()

	def IsLocked(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.IsLocked()

	def LockObject(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.LockObject()

	def UnlockObject(self, password:str) -> int:
		"""
		:password [IN]: str
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.UnlockObject(password)

	def DeleteForced(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.70
		"""
		return self._obj.DeleteForced()

	def IsLockedByAccessControl(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.IsLockedByAccessControl()

	def GetSheetAndExternalDocumentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 19.22
		"""
		dummy=0
		ret, ids = self._obj.GetSheetAndExternalDocumentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

# -------------------- ITreeInterface--------------------
class Tree:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Tree. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, treeid:int) -> int:
		"""
		:treeid [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(treeid)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetName(name)

	def GetVisibleObjectTypes(self) -> tuple[int, tuple[int,...]]:
		"""
		:type_array [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, type_array = self._obj.GetVisibleObjectTypes(dummy)
		type_array = type_array[1:] if type(type_array) == tuple and len(type_array) > 0 else tuple()
		return ret, type_array

	def SetVisibleObjectTypes(self, type_array:list[int]) -> int:
		"""
		:type_array [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.SetVisibleObjectTypes(type_array)
		return ret[0]

	def GetSortingMethod(self) -> tuple[int, int, tuple[tuple[str,int,str,str,int],...], tuple[tuple[str,str,int],...]]:
		"""
		:flags [OUT]: int
		:structure [OUT]: tuple[tuple[str,int,str,str,int],...]
		:freetab [OUT]: tuple[tuple[str,str,int],...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, flags, structure, freetab = self._obj.GetSortingMethod(dummy, dummy, dummy)
		structure = structure[1:] if type(structure) == tuple and len(structure) > 0 else tuple()
		freetab = freetab[1:] if type(freetab) == tuple and len(freetab) > 0 else tuple()
		return ret, flags, structure, freetab

	def SetSortingMethod(self, flags:int, structure:list[tuple[str,int,str,str,int]], freetab:list[tuple[str,str,int]]) -> int:
		"""
		:flags [IN]: int
		:structure [IN]: list[tuple[str,int,str,str,int]]
		:freetab [IN]: list[tuple[str,str,int]]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		structure = [("",0,"","",0)] + structure
		freetab = [("","",0)] + freetab
		ret = self._obj.SetSortingMethod(flags, structure, freetab)
		return ret[0]

	def SetIcon(self, filename:str, index:int=0) -> int:
		"""
		:filename [IN]: str
		:index [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetIcon(filename, index)

	def GetSelectedSheetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedSheetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedCableIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedCableIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedTerminalIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedTerminalIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedConnectorIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedConnectorIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedBlockIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedBlockIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedAllDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedAllDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedBundleIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedBundleIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedStructureNodeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedStructureNodeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsVisible(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsVisible()

	def IsActive(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsActive()

	def Create(self, name:str, position:int=0, before:int=0) -> int:
		"""
		:name [IN]: str
		:position [IN]: int Default value =0
		:before [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Create(name, position, before)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete()

	def GetSelectedExternalDocumentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedExternalDocumentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNames(self) -> tuple[int, tuple[str,...]]:
		"""
		:names [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		dummy=0
		ret, names = self._obj.GetNames(dummy)
		names = names[1:] if type(names) == tuple and len(names) > 0 else tuple()
		return ret, names

	def SetNames(self, names:list[str]) -> int:
		"""
		:names [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		ret = self._obj.SetNames(names)
		return ret[0]

	def GetSelectedSheetIdsByFolder(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedSheetIdsByFolder(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedExternalDocumentIdsByFolder(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedExternalDocumentIdsByFolder(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedAllDeviceIdsByFolder(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedAllDeviceIdsByFolder(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def ViewSignalTree(self, bShowTree:bool) -> int:
		"""
		:bShowTree [IN]: bool
		:Return: int

		Available since TLB-Versions: 10.20
		"""
		return self._obj.ViewSignalTree(bShowTree)

	def GetVisibleInfoTypesEx(self) -> tuple[int, tuple[int,...], tuple[int,...], tuple[int,...]]:
		"""
		:views [OUT]: tuple[int,...]
		:schematicTypes [OUT]: tuple[int,...]
		:formboardSheetIds [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 16.70
		"""
		dummy=0
		ret, views, schematicTypes, formboardSheetIds = self._obj.GetVisibleInfoTypesEx(dummy, dummy, dummy)
		views = views[1:] if type(views) == tuple and len(views) > 0 else tuple()
		schematicTypes = schematicTypes[1:] if type(schematicTypes) == tuple and len(schematicTypes) > 0 else tuple()
		formboardSheetIds = formboardSheetIds[1:] if type(formboardSheetIds) == tuple and len(formboardSheetIds) > 0 else tuple()
		return ret, views, schematicTypes, formboardSheetIds

	def SetVisibleInfoTypesEx(self, views:list[int], schematicTypes:list[int], formboardSheetIds:list[int]) -> int:
		"""
		:views [IN]: list[int]
		:schematicTypes [IN]: list[int]
		:formboardSheetIds [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 16.70
		"""
		return self._obj.SetVisibleInfoTypesEx(views, schematicTypes, formboardSheetIds)

	def GetTreeType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 17.03
		"""
		return self._obj.GetTreeType()

	def GetSelectedBusbarIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedBusbarIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

# -------------------- IDimensionInterface--------------------
class Dimension:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Dimension. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete()

	def Create(self, shtid:int, x1:float, y1:float, x2:float, y2:float, flags:int, distance:float, text:str, tx:float, ty:float) -> int:
		"""
		:shtid [IN]: int
		:x1 [IN]: float
		:y1 [IN]: float
		:x2 [IN]: float
		:y2 [IN]: float
		:flags [IN]: int
		:distance [IN]: float
		:text [IN]: str
		:tx [IN]: float
		:ty [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Create(shtid, x1, y1, x2, y2, flags, distance, text, tx, ty)

	def GetParameters(self) -> tuple[int, float, float, float, float, float, int, str, float, float]:
		"""
		:x1 [OUT]: float
		:y1 [OUT]: float
		:x2 [OUT]: float
		:y2 [OUT]: float
		:distance [OUT]: float
		:flags [OUT]: int
		:text [OUT]: str
		:tx [OUT]: float
		:ty [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetParameters(dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy)

	def SetArrowMode(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetArrowMode(value)

	def GetArrowMode(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetArrowMode()

	def SetExtension(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetExtension(value)

	def GetExtension(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetExtension()

	def SetLineWidth(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLineWidth(value)

	def GetLineWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLineWidth()

	def SetPrecision(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPrecision(value)

	def GetPrecision(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPrecision()

	def SetOffset(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetOffset(value)

	def GetOffset(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetOffset()

	def SetPrefix(self, value:str) -> str:
		"""
		:value [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPrefix(value)

	def GetPrefix(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPrefix()

	def SetSuffix(self, value:str) -> str:
		"""
		:value [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetSuffix(value)

	def GetSuffix(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSuffix()

	def SetText(self, text:str, fixed:int) -> int:
		"""
		:text [IN]: str
		:fixed [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetText(text, fixed)

	def GetText(self) -> tuple[int, str, int]:
		"""
		:text [OUT]: str
		:fixed [OUT]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetText(dummy, dummy)

	def SetLevel(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLevel(value)

	def GetLevel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLevel()

	def SetColour(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetColour(value)

	def GetColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetColour()

	def SetTextFontName(self, text:str) -> str:
		"""
		:text [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetTextFontName(text)

	def GetTextFontName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTextFontName()

	def SetTextStyle(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetTextStyle(value)

	def GetTextStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTextStyle()

	def SetTextHeight(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetTextHeight(value)

	def GetTextHeight(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTextHeight()

	def SetTextColour(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetTextColour(value)

	def GetTextColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTextColour()

	def GetDimensionedIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:anyids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, anyids = self._obj.GetDimensionedIds(dummy)
		anyids = anyids[1:] if type(anyids) == tuple and len(anyids) > 0 else tuple()
		return ret, anyids

	def IsAlongPath(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.IsAlongPath()

	def SetHideLongerPart(self, value:bool) -> int:
		"""
		:value [IN]: bool
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetHideLongerPart(value)

	def GetHideLongerPart(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetHideLongerPart()

	def SetSuffixSizeFactor(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetSuffixSizeFactor(value)

	def GetSuffixSizeFactor(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetSuffixSizeFactor()

	def SetDisplayAttribute(self, attnam:str) -> int:
		"""
		:attnam [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetDisplayAttribute(attnam)

	def GetDisplayAttribute(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetDisplayAttribute()

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.AddAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.DeleteAttribute(name)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 11.00
		"""
		return self._obj.GetAttributeValue(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.HasAttribute(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		return self._obj.SetAttributeValue(name, value)

	def SetExtensionLineOffset(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 11.80
		"""
		return self._obj.SetExtensionLineOffset(value)

	def GetExtensionLineOffset(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 11.80
		"""
		return self._obj.GetExtensionLineOffset()

	def CreateEx(self, dimtyp:int, sheet:int, x:list[float], y:list[float], flags:int=0) -> int:
		"""
		:dimtyp [IN]: int
		:sheet [IN]: int
		:x [IN]: list[float]
		:y [IN]: list[float]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 15.82
		"""
		x = [0.] + x
		y = [0.] + y
		return self._obj.CreateEx(dimtyp, sheet, x, y, flags)

	def IsRunningDimension(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 15.82
		"""
		return self._obj.IsRunningDimension()

	def IsPartOfDimension(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 15.82
		"""
		return self._obj.IsPartOfDimension()

	def GetPartIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 15.82
		"""
		dummy=0
		ret, ids = self._obj.GetPartIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def SetRunningDimTextRotation(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 15.82
		"""
		return self._obj.SetRunningDimTextRotation(value)

	def GetRunningDimTextRotation(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 15.82
		"""
		return self._obj.GetRunningDimTextRotation()

	def IsRedlined(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 17.04
		"""
		return self._obj.IsRedlined()

	def SetRedlined(self, onoff:bool) -> int:
		"""
		:onoff [IN]: bool Default value =TRUE
		:Return: int

		Available since TLB-Versions: 17.04
		"""
		return self._obj.SetRedlined(onoff)

	def GetCenterTextPosition(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.GetCenterTextPosition()

	def SetCenterTextPosition(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.SetCenterTextPosition(value)

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

# -------------------- IDllInterface--------------------
class Dll:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Dll. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def Load(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 6.00
		"""
		return self._obj.Load(name)

	def Call(self, method:str, item1:str=DLLDEFAULTVALUE, item2:str=DLLDEFAULTVALUE, item3:str=DLLDEFAULTVALUE, item4:str=DLLDEFAULTVALUE, item5:str=DLLDEFAULTVALUE) -> int:
		"""
		:method [IN]: str
		:item1 [IN]: str Default value =DLLDEFAULTVALUE
		:item2 [IN]: str Default value =DLLDEFAULTVALUE
		:item3 [IN]: str Default value =DLLDEFAULTVALUE
		:item4 [IN]: str Default value =DLLDEFAULTVALUE
		:item5 [IN]: str Default value =DLLDEFAULTVALUE
		:Return: int

		Available since TLB-Versions: 6.00
		"""
		return self._obj.Call(method, item1, item2, item3, item4, item5)

	def Unload(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 6.00
		"""
		return self._obj.Unload()

# -------------------- IGroupInterface--------------------
class Group:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Group. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def Create(self, ids:list[int], name:str="") -> int:
		"""
		:ids [IN]: list[int]
		:name [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.Create(ids, name)
		return ret[0]

	def Delete(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.Delete(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetItems(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetItems(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def AddItems(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.AddItems(ids)
		return ret[0]

	def RemoveItems(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.RemoveItems(ids)
		return ret[0]

	def GetGroupId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGroupId(id)

	def GetLocation(self) -> tuple[int, float, float, float, str, str, str]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:grid [OUT]: str
		:column_value [OUT]: str
		:row_value [OUT]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetLocation(dummy, dummy, dummy, dummy, dummy, dummy)

	def Place(self, shtid:int, x:float, y:float, z:float, rotation:float) -> int:
		"""
		:shtid [IN]: int
		:x [IN]: float
		:y [IN]: float
		:z [IN]: float
		:rotation [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Place(shtid, x, y, z, rotation)

	def DeleteContents(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteContents()

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetName(name)

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeIds(self, name:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:name [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, name)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttribute(name)

	def GetPartName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.00
		"""
		return self._obj.GetPartName()

	def SetPartName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.SetPartName(name)

	def IsPart(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.IsPart()

	def IsSubCircuit(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.IsSubCircuit()

	def UpdatePart(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.UpdatePart()

	def Unplace(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		return self._obj.Unplace()

	def DeleteUnplaced(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		return self._obj.DeleteUnplaced()

	def IsUnplaced(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		return self._obj.IsUnplaced()

	def PlaceInteractively(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		return self._obj.PlaceInteractively()

	def UpdateDrawingForProjectGeneration(self, flags:int, substitutes:list[tuple[str,str]], allowedTexttypes:list[str]=pythoncom.Empty, allowedAttributenames:list[str]=pythoncom.Empty, resultArray:tuple[typing.Any,...]=0) -> int:
		"""
		:flags [IN]: int
		:substitutes [IN]: list[tuple[str,str]]
		:allowedTexttypes [IN]: list[str] Default value =pythoncom.Empty
		:allowedAttributenames [IN]: list[str] Default value =pythoncom.Empty
		:resultArray [IN]: tuple[typing.Any,...] Default value =0
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		substitutes = [("","")] + substitutes
		return self._obj.UpdateDrawingForProjectGeneration(flags, substitutes, allowedTexttypes, allowedAttributenames, resultArray)

	def GetGroupType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 22.41, 23.50
		"""
		return self._obj.GetGroupType()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetAnyIds(self, flags:int) -> tuple[int, dict[int,tuple[int,...]]]:
		"""
		:flags [IN]: int
		:anyIds [OUT]: dict[int,tuple[int,...]]
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		dummy=0
		ret, anyIds = self._obj.GetAnyIds(flags, dummy)
		anyIds = _variant_to_dict(anyIds)
		for i0 in anyIds.keys():
			anyIds[i0] = anyIds[i0][1:] if type(anyIds[i0]) == tuple and len(anyIds[i0]) > 0 else tuple()
		return ret, anyIds

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 26.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 26.00
		"""
		return self._obj.SetGUID(guid)

# -------------------- IFunctionalUnitInterface--------------------
class FunctionalUnit:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize FunctionalUnit. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def Create(self, fdbID:int, name:str, symnam:str, symver:str) -> int:
		"""
		:fdbID [IN]: int
		:name [IN]: str
		:symnam [IN]: str
		:symver [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Create(fdbID, name, symnam, symver)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete()

	def GetFunctionalPortIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetFunctionalPortIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsDynamic(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsDynamic()

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.HasAttribute(name)

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetName(name)

	def GetDeviceId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetDeviceId()

	def GetSchemaSymbolId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetSchemaSymbolId()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

# -------------------- IFunctionalPortInterface--------------------
class FunctionalPort:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize FunctionalPort. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def Create(self, fuId:int, name:str) -> int:
		"""
		:fuId [IN]: int
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Create(fuId, name)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete()

	def SetSignalName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetSignalName(name)

	def GetSignalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSignalName()

	def SetConnectorName(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetConnectorName(name)

	def GetConnectorName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConnectorName()

	def SetPinName(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPinName(name)

	def GetPinName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPinName()

	def SetConnectorPinID(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetConnectorPinID(id)

	def GetConnectorPinID(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConnectorPinID()

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def GetNodeID(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetNodeID()

	def SetNodeID(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetNodeID(id)

	def GetFunctionalUnitId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetFunctionalUnitId()

	def SetPinID(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetPinID(id)

	def GetPinID(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetPinID()

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetName(name)

	def SetPortType(self, _type:int) -> int:
		"""
		:_type [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetPortType(_type)

	def GetPortType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetPortType()

	def SetSignalEquiv(self, signalequiv:int) -> int:
		"""
		:signalequiv [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetSignalEquiv(signalequiv)

	def GetSignalEquiv(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetSignalEquiv()

	def SetUserDefined(self, _type:int=1) -> int:
		"""
		:_type [IN]: int Default value =1
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetUserDefined(_type)

	def GetUserDefined(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetUserDefined()

	def GetConnectedPorts(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, ids = self._obj.GetConnectedPorts(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSignalEqvPorts(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, ids = self._obj.GetSignalEqvPorts(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTranslatedSignalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 11.00
		"""
		return self._obj.GetTranslatedSignalName()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

# -------------------- IConnectLineInterface--------------------
class ConnectLine:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize ConnectLine. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.22
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 9.22
		"""
		return self._obj.SetId(id)

	def GetCoordinates(self) -> tuple[int, tuple[float,...], tuple[float,...], tuple[float,...], tuple[int,...]]:
		"""
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:zarr [OUT]: tuple[float,...]
		:PointTypArr [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.22
		"""
		dummy=0
		ret, xarr, yarr, zarr, PointTypArr = self._obj.GetCoordinates(dummy, dummy, dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		zarr = zarr[1:] if type(zarr) == tuple and len(zarr) > 0 else tuple()
		PointTypArr = PointTypArr[1:] if type(PointTypArr) == tuple and len(PointTypArr) > 0 else tuple()
		return ret, xarr, yarr, zarr, PointTypArr

	def GetProtectionSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.22
		"""
		dummy=0
		ret, ids = self._obj.GetProtectionSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def AddProtectionSymbolId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 9.22
		"""
		return self._obj.AddProtectionSymbolId(id)

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

# -------------------- ISignalClassInterface--------------------
class SignalClass:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize SignalClass. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetId(id)

	def Create(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.Create(name)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.Delete()

	def AddSignalId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.AddSignalId(id)

	def RemoveSignalId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.RemoveSignalId(id)

	def GetSignalIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, ids = self._obj.GetSignalIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetName()

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetName(name)

	def Search(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.Search(name)

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.HasAttribute(name)

	def DisplayaAttributeValueAt(self, name:str, sheetid:int, x:float, y:float) -> int:
		"""
		:name [IN]: str
		:sheetid [IN]: int
		:x [IN]: float
		:y [IN]: float
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.DisplayaAttributeValueAt(name, sheetid, x, y)

	def SetAttributeVisibility(self, name:str, onoff:int) -> int:
		"""
		:name [IN]: str
		:onoff [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetAttributeVisibility(name, onoff)

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

# -------------------- IAttributeDefinitionInterface--------------------
class AttributeDefinition:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize AttributeDefinition. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 15.31
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 15.31
		"""
		return self._obj.SetId(id)

	def Search(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 15.31
		"""
		return self._obj.Search(name)

	def Get(self) -> tuple[int, tuple[tuple[str,str],...]]:
		"""
		:attributeDefinition [OUT]: tuple[tuple[str,str],...], Enum types Available: e3series.types.AD_Direction, AD_Owner, AD_Ratio, AD_Type, AD_UniqueValue.
		:Return: int

		Available since TLB-Versions: 15.31
		"""
		dummy=0
		ret, attributeDefinition = self._obj.Get(dummy)
		attributeDefinition = attributeDefinition[1:] if type(attributeDefinition) == tuple and len(attributeDefinition) > 0 else tuple()
		attributeDefinition = tuple( i0[1:] if type(i0) == tuple and len(i0) > 0 else tuple() for i0 in attributeDefinition)
		return ret, attributeDefinition

	def Set(self, attributeDefinition:list[tuple[str,str]]) -> int:
		"""
		:attributeDefinition [IN]: list[tuple[str,str]], Enum types Available: e3series.types.AD_Direction, AD_Owner, AD_Ratio, AD_Type, AD_UniqueValue.
		:Return: int

		Available since TLB-Versions: 15.31
		"""
		attributeDefinition = [("","")] + attributeDefinition
		attributeDefinition = [tuple((None,) + i0) for i0 in attributeDefinition]
		return self._obj.Set(attributeDefinition)

	def GetFromDatabase(self) -> tuple[int, dict[str,tuple[tuple[str,str],...]]]:
		"""
		:attributeDefinitions [OUT]: dict[str,tuple[tuple[str,str],...]], Enum types Available: e3series.types.AD_Direction, AD_Owner, AD_Ratio, AD_Type, AD_UniqueValue.
		:Return: int

		Available since TLB-Versions: 15.31
		"""
		dummy=0
		ret, attributeDefinitions = self._obj.GetFromDatabase(dummy)
		attributeDefinitions = _variant_to_dict(attributeDefinitions)
		for i0 in attributeDefinitions.keys():
			attributeDefinitions[i0] = attributeDefinitions[i0][1:] if type(attributeDefinitions[i0]) == tuple and len(attributeDefinitions[i0]) > 0 else tuple()
			attributeDefinitions[i0] = tuple( i1[1:] if type(i1) == tuple and len(i1) > 0 else tuple() for i1 in attributeDefinitions[i0])
		return ret, attributeDefinitions

	def GetInternalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 15.31
		"""
		return self._obj.GetInternalName()

	def GetName(self, languageId:int=0) -> str:
		"""
		:languageId [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 15.31
		"""
		return self._obj.GetName(languageId)

	def SetName(self, languageId:int, newName:str) -> int:
		"""
		:languageId [IN]: int
		:newName [IN]: str
		:Return: int

		Available since TLB-Versions: 15.31
		"""
		return self._obj.SetName(languageId, newName)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 15.31
		"""
		return self._obj.Delete()

	def Create(self, name:str, attributeDefinition:list[tuple[str,str]]) -> int:
		"""
		:name [IN]: str
		:attributeDefinition [IN]: list[tuple[str,str]], Enum types Available: e3series.types.AD_Direction, AD_Owner, AD_Ratio, AD_Type, AD_UniqueValue.
		:Return: int

		Available since TLB-Versions: 15.31
		"""
		attributeDefinition = [("","")] + attributeDefinition
		attributeDefinition = [tuple((None,) + i0) for i0 in attributeDefinition]
		return self._obj.Create(name, attributeDefinition)

	def Update(self, flags:int) -> int:
		"""
		:flags [IN]: int
		:Return: int

		Available since TLB-Versions: 15.31
		"""
		return self._obj.Update(flags)

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetValueListName(self, flags:int=0) -> str:
		"""
		:flags [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 27.00, 26.01, 25.34
		"""
		return self._obj.GetValueListName(flags)

	def GetAttributeListValues(self, attributelistname:str, flags:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:attributelistname [IN]: str
		:values [OUT]: tuple[str,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 27.00, 26.01, 25.34
		"""
		dummy=0
		ret, values = self._obj.GetAttributeListValues(attributelistname, dummy, flags)
		values = values[1:] if type(values) == tuple and len(values) > 0 else tuple()
		return ret, values

# -------------------- IEmbeddedObjectInterface--------------------
class EmbeddedObject:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize EmbeddedObject. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.SetId(id)

	def Create(self, filename:str, shti:int, x:float, y:float) -> int:
		"""
		:filename [IN]: str
		:shti [IN]: int
		:x [IN]: float
		:y [IN]: float
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.Create(filename, shti, x, y)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.Delete()

	def Move(self, shti:int, x:float, y:float) -> int:
		"""
		:shti [IN]: int
		:x [IN]: float
		:y [IN]: float
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.Move(shti, x, y)

	def Resize(self, width:float, height:float) -> int:
		"""
		:width [IN]: float
		:height [IN]: float
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.Resize(width, height)

	def Open(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.Open()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

# -------------------- IStateInterface--------------------
class State:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize State. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.SetId(id)

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 22.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> int:
		"""
		:gid [IN]: str
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 22.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> int:
		"""
		:guid [IN]: str
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.SetGUID(guid)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 22.00
		"""
		return self._obj.GetName()

	def GetAttributeIds(self, name:str) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, name)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 22.00
		"""
		return self._obj.GetAttributeValue(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.HasAttribute(name)

	def GetOwnerId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.GetOwnerId()

	def GetOwnerType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.GetOwnerType()

	def GetStateType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.GetStateType()

	def GetOwnerIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		dummy=0
		ret, ids = self._obj.GetOwnerIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

# -------------------- IProjectConfiguratorInterface--------------------
class ProjectConfigurator:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize ProjectConfigurator. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def Delete(self, targetId:int, flags:int=0) -> tuple[int, tuple[int, int, str]]:
		"""
		:errorMessages [OUT]: tuple[int, int, str]
		:targetId [IN]: int
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00
		"""
		dummy=0
		return self._obj.Delete(dummy, targetId, flags)

	def DeleteSheet(self, sheetId:int, flags:int=0) -> tuple[int, tuple[int, int, str]]:
		"""
		:errorMessages [OUT]: tuple[int, int, str]
		:sheetId [IN]: int
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00
		"""
		dummy=0
		return self._obj.DeleteSheet(dummy, sheetId, flags)

	def DeleteDevice(self, devId:int, forced:bool, flags:int=0) -> tuple[int, tuple[int, int, str]]:
		"""
		:errorMessages [OUT]: tuple[int, int, str]
		:devId [IN]: int
		:forced [IN]: bool
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00
		"""
		dummy=0
		return self._obj.DeleteDevice(dummy, devId, forced, flags)

	def AddAttribute(self, targetId:int, attributeName:str, value:str, objectType1:int, objectType2:int, name:str="", flags:int=0) -> tuple[int, tuple[int, int, str]]:
		"""
		:errorMessages [OUT]: tuple[int, int, str]
		:targetId [IN]: int
		:attributeName [IN]: str
		:value [IN]: str
		:objectType1 [IN]: int
		:objectType2 [IN]: int
		:name [IN]: str Default value =""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00
		"""
		dummy=0
		return self._obj.AddAttribute(dummy, targetId, attributeName, value, objectType1, objectType2, name, flags)

	def DeleteAttribute(self, targetId:int, attributeName:str, value:str, objectType1:int, objectType2:int, name:str="", flags:int=0) -> tuple[int, tuple[int, int, str]]:
		"""
		:errorMessages [OUT]: tuple[int, int, str]
		:targetId [IN]: int
		:attributeName [IN]: str
		:value [IN]: str
		:objectType1 [IN]: int
		:objectType2 [IN]: int
		:name [IN]: str Default value =""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00
		"""
		dummy=0
		return self._obj.DeleteAttribute(dummy, targetId, attributeName, value, objectType1, objectType2, name, flags)

	def DeleteAndReconnect(self, targetId:int, flags:int=0) -> tuple[int, tuple[int, int, str]]:
		"""
		:errorMessages [OUT]: tuple[int, int, str]
		:targetId [IN]: int
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00
		"""
		dummy=0
		return self._obj.DeleteAndReconnect(dummy, targetId, flags)

	def ChangeComponent(self, targetId:int, newComponent:str, oldComponent:str="", newVersion:str="", oldVersion:str="", flags:int=0) -> tuple[int, list[tuple[int, int, str]]]:
		"""
		:errorMessages [OUT]: list[tuple[int, int, str]]
		:targetId [IN]: int
		:newComponent [IN]: str
		:oldComponent [IN]: str Default value =""
		:newVersion [IN]: str Default value =""
		:oldVersion [IN]: str Default value =""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00
		"""
		dummy=0
		return self._obj.ChangeComponent(dummy, targetId, newComponent, oldComponent, newVersion, oldVersion, flags)

	def SwapSymbol(self, targetId:int, newPin:str, newSymbol:str="", flags:int=0) -> tuple[int, tuple[int, int, str]]:
		"""
		:errorMessages [OUT]: tuple[int, int, str]
		:targetId [IN]: int
		:newPin [IN]: str
		:newSymbol [IN]: str Default value =""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.01
		"""
		dummy=0
		return self._obj.SwapSymbol(dummy, targetId, newPin, newSymbol, flags)

# -------------------- IDbeComponentInterface--------------------
class DbeComponent:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize DbeComponent. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetId(id)

	def Save(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.Save()

	def Remove(self, save_changes:bool=False) -> int:
		"""
		:save_changes [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.Remove(save_changes)

	def GetAttributeIds(self, end:int=0, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:end [IN]: int Default value =0
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, end, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def AddAttributeValue(self, name:str, value:str, end:int=0) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:end [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.AddAttributeValue(name, value, end)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetName()

	def GetVersion(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetVersion()

	def GetSubType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetSubType()

	def SetSubType(self, subtype:int) -> int:
		"""
		:subtype [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetSubType(subtype)

	def GetComponentType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.01
		"""
		return self._obj.GetComponentType()

	def SetModelName(self, modelName:str, flags:int=0) -> int:
		"""
		:modelName [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		return self._obj.SetModelName(modelName, flags)

	def GetModelName(self, flags:int=0) -> str:
		"""
		:flags [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 24.11
		"""
		return self._obj.GetModelName(flags)

# -------------------- IDbeAttributeInterface--------------------
class DbeAttribute:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize DbeAttribute. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetId(id)

	def SetValue(self, value:str) -> int:
		"""
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetValue(value)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.Delete()

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.01
		"""
		return self._obj.GetName()

	def GetInternalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.01
		"""
		return self._obj.GetInternalName()

	def GetInternalValue(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.01
		"""
		return self._obj.GetInternalValue()

	def GetFormattedValue(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.01
		"""
		return self._obj.GetFormattedValue()

	def GetValue(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.01
		"""
		return self._obj.GetValue()

# -------------------- IDbeSymbolInterface--------------------
class DbeSymbol:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize DbeSymbol. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetId(id)

	def Save(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.Save()

	def Remove(self, save_changes:bool=False) -> int:
		"""
		:save_changes [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.Remove(save_changes)

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetGraphicIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		ret, ids = self._obj.GetGraphicIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTextIds(self, texttype:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:texttype [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		ret, ids = self._obj.GetTextIds(dummy, texttype)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetName()

	def GetVersion(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetVersion()

	def GetCharacteristic(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetCharacteristic()

	def GetSubType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetSubType()

	def SetSubType(self, subtype:int) -> int:
		"""
		:subtype [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetSubType(subtype)

	def FitSpaceRequirement(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.01
		"""
		return self._obj.FitSpaceRequirement()

	def GetSymbolType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.01
		"""
		return self._obj.GetSymbolType()

	def ImportDXF(self, filename:str, scale:float, x:float, y:float, rot:int, font:str) -> int:
		"""
		:filename [IN]: str
		:scale [IN]: float
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: int
		:font [IN]: str
		:Return: int

		Available since TLB-Versions: 19.01
		"""
		return self._obj.ImportDXF(filename, scale, x, y, rot, font)

	def GetDXFSize(self, filename:str, font:str) -> tuple[int, float, float, float]:
		"""
		:filename [IN]: str
		:font [IN]: str
		:dx [OUT]: float
		:dy [OUT]: float
		:scale [OUT]: float
		:Return: int

		Available since TLB-Versions: 19.01
		"""
		dummy=0
		return self._obj.GetDXFSize(filename, font, dummy, dummy, dummy)

	def PlaceSymbol(self, symname:str, version:str, x:float, y:float, rot:str, flags:int=0) -> int:
		"""
		:symname [IN]: str
		:version [IN]: str
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 19.41
		"""
		return self._obj.PlaceSymbol(symname, version, x, y, rot, flags)

	def GetNodeIds(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 21.21
		"""
		dummy=0
		ret, ids = self._obj.GetNodeIds(dummy, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

# -------------------- IDbeTextInterface--------------------
class DbeText:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize DbeText. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetId(id)

	def Create(self, id:int, texttype:int, x:float, y:float, textvalue:str="") -> int:
		"""
		:id [IN]: int
		:texttype [IN]: int
		:x [IN]: float
		:y [IN]: float
		:textvalue [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.Create(id, texttype, x, y, textvalue)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.Delete()

	def GetColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetColour()

	def SetColour(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetColour(value)

	def GetAlignment(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetAlignment()

	def SetAlignment(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetAlignment(newval)

	def GetBallooning(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetBallooning()

	def SetBallooning(self, onoff:bool, _type:int) -> int:
		"""
		:onoff [IN]: bool
		:_type [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetBallooning(onoff, _type)

	def GetFontName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetFontName()

	def SetFontName(self, newname:str) -> int:
		"""
		:newname [IN]: str
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetFontName(newname)

	def GetHeight(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetHeight()

	def SetHeight(self, newval:float) -> int:
		"""
		:newval [IN]: float
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetHeight(newval)

	def GetLevel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetLevel()

	def SetLevel(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetLevel(newval)

	def GetLocking(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetLocking()

	def SetLocking(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetLocking(newval)

	def GetMode(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetMode()

	def SetMode(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetMode(newval)

	def GetRotation(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetRotation()

	def SetRotation(self, rotation:float) -> float:
		"""
		:rotation [IN]: float
		:Return: float

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetRotation(rotation)

	def GetSingleLine(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetSingleLine()

	def SetSingleLine(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetSingleLine(newval)

	def GetStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetStyle()

	def SetStyle(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetStyle(newval)

	def GetText(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetText()

	def SetText(self, newtext:str) -> int:
		"""
		:newtext [IN]: str
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetText(newtext)

	def GetType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetType()

	def SetType(self, texttype:int) -> int:
		"""
		:texttype [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetType(texttype)

	def GetVisibility(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.11
		"""
		return self._obj.GetVisibility()

	def SetVisibility(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 21.11
		"""
		return self._obj.SetVisibility(newval)

	def GetPosition(self) -> tuple[int, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:Return: int

		Available since TLB-Versions: 21.21
		"""
		dummy=0
		return self._obj.GetPosition(dummy, dummy)

# -------------------- IDbeGraphInterface--------------------
class DbeGraph:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize DbeGraph. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetId(id)

	def GetColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetColour()

	def SetColour(self, newcol:int) -> int:
		"""
		:newcol [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetColour(newcol)

	def GetLevel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetLevel()

	def SetLevel(self, newlev:int) -> int:
		"""
		:newlev [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetLevel(newlev)

	def SetBlobInfo(self, filename:str) -> int:
		"""
		:filename [IN]: str
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetBlobInfo(filename)

	def CreateArc(self, id:int, x:float, y:float, radius:float, start:float, end:float) -> int:
		"""
		:id [IN]: int
		:x [IN]: float
		:y [IN]: float
		:radius [IN]: float
		:start [IN]: float
		:end [IN]: float
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.CreateArc(id, x, y, radius, start, end)

	def CreateCircle(self, id:int, x:float, y:float, radius:float) -> int:
		"""
		:id [IN]: int
		:x [IN]: float
		:y [IN]: float
		:radius [IN]: float
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.CreateCircle(id, x, y, radius)

	def CreatePolygon(self, id:int, pnts:int, x:list[int], y:list[int]) -> int:
		"""
		:id [IN]: int
		:pnts [IN]: int
		:x [IN]: list[int]
		:y [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.CreatePolygon(id, pnts, x, y)

	def CreateRectangle(self, id:int, x1:float, y1:float, x2:float, y2:float) -> int:
		"""
		:id [IN]: int
		:x1 [IN]: float
		:y1 [IN]: float
		:x2 [IN]: float
		:y2 [IN]: float
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.CreateRectangle(id, x1, y1, x2, y2)

	def CreateLine(self, id:int, x1:float, y1:float, x2:float, y2:float) -> int:
		"""
		:id [IN]: int
		:x1 [IN]: float
		:y1 [IN]: float
		:x2 [IN]: float
		:y2 [IN]: float
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.CreateLine(id, x1, y1, x2, y2)

	def CreateImage(self, id:int, xpos:float, ypos:float, xsize:float, ysize:float, filename:str, embed:int=1) -> int:
		"""
		:id [IN]: int
		:xpos [IN]: float
		:ypos [IN]: float
		:xsize [IN]: float
		:ysize [IN]: float
		:filename [IN]: str
		:embed [IN]: int Default value =1
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.CreateImage(id, xpos, ypos, xsize, ysize, filename, embed)

	def CreateCurve(self, id:int, pnts:int, x:list[float], y:list[float]) -> int:
		"""
		:id [IN]: int
		:pnts [IN]: int
		:x [IN]: list[float]
		:y [IN]: list[float]
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		x = [0.] + x
		y = [0.] + y
		return self._obj.CreateCurve(id, pnts, x, y)

	def CreateCloud(self, id:int, pnts:int, x:list[float], y:list[float]) -> int:
		"""
		:id [IN]: int
		:pnts [IN]: int
		:x [IN]: list[float]
		:y [IN]: list[float]
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		x = [0.] + x
		y = [0.] + y
		return self._obj.CreateCloud(id, pnts, x, y)

	def CreateBlob(self, id:int, filename:str) -> int:
		"""
		:id [IN]: int
		:filename [IN]: str
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.CreateBlob(id, filename)

	def SaveBlob(self, filename:str) -> int:
		"""
		:filename [IN]: str
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SaveBlob(filename)

	def Place(self, x:float, y:float) -> int:
		"""
		:x [IN]: float
		:y [IN]: float
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.Place(x, y)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.Delete()

	def GetTypeId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetTypeId()

	def GetArc(self) -> tuple[int, float, float, float, float, float]:
		"""
		:xm [OUT]: float
		:ym [OUT]: float
		:rad [OUT]: float
		:startang [OUT]: float
		:endang [OUT]: float
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		return self._obj.GetArc(dummy, dummy, dummy, dummy, dummy)

	def GetCircle(self) -> tuple[int, float, float, float]:
		"""
		:xm [OUT]: float
		:ym [OUT]: float
		:rad [OUT]: float
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		return self._obj.GetCircle(dummy, dummy, dummy)

	def GetLine(self) -> tuple[int, float, float, float, float]:
		"""
		:x1 [OUT]: float
		:y1 [OUT]: float
		:x2 [OUT]: float
		:y2 [OUT]: float
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		return self._obj.GetLine(dummy, dummy, dummy, dummy)

	def GetPolygon(self) -> tuple[int, int, tuple[float,...], tuple[float,...]]:
		"""
		:npnts [OUT]: int
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		ret, npnts, xarr, yarr = self._obj.GetPolygon(dummy, dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		return ret, npnts, xarr, yarr

	def GetRectangle(self) -> tuple[int, float, float, float, float]:
		"""
		:x1 [OUT]: float
		:y1 [OUT]: float
		:x2 [OUT]: float
		:y2 [OUT]: float
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		return self._obj.GetRectangle(dummy, dummy, dummy, dummy)

	def GetCurve(self) -> tuple[int, int, tuple[float,...], tuple[float,...]]:
		"""
		:npnts [OUT]: int
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		ret, npnts, xarr, yarr = self._obj.GetCurve(dummy, dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		return ret, npnts, xarr, yarr

	def GetCloud(self) -> tuple[int, int, tuple[float,...], tuple[float,...]]:
		"""
		:npnts [OUT]: int
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		ret, npnts, xarr, yarr = self._obj.GetCloud(dummy, dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		return ret, npnts, xarr, yarr

	def GetLineColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetLineColour()

	def SetLineColour(self, newcol:int) -> int:
		"""
		:newcol [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetLineColour(newcol)

	def GetLineWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetLineWidth()

	def SetLineWidth(self, newwid:float) -> float:
		"""
		:newwid [IN]: float
		:Return: float

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetLineWidth(newwid)

	def GetLineStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetLineStyle()

	def SetLineStyle(self, newstyle:int) -> int:
		"""
		:newstyle [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetLineStyle(newstyle)

	def SetHatchColour(self, newcol:int) -> int:
		"""
		:newcol [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetHatchColour(newcol)

	def GetHatchColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetHatchColour()

	def GetHatchLineWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetHatchLineWidth()

	def SetHatchLineWidth(self, newwid:float) -> float:
		"""
		:newwid [IN]: float
		:Return: float

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetHatchLineWidth(newwid)

	def GetHatchLineStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetHatchLineStyle()

	def SetHatchLineStyle(self, newstyle:int) -> int:
		"""
		:newstyle [IN]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetHatchLineStyle(newstyle)

	def GetHatchLineDistance(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 19.00
		"""
		return self._obj.GetHatchLineDistance()

	def SetHatchLineDistance(self, newdist:float) -> float:
		"""
		:newdist [IN]: float
		:Return: float

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetHatchLineDistance(newdist)

	def GetHatchPattern(self) -> tuple[int, float, float]:
		"""
		:angle1 [OUT]: float
		:angle2 [OUT]: float
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		return self._obj.GetHatchPattern(dummy, dummy)

	def SetHatchPattern(self, newpat:int, angle1:float, angle2:float) -> int:
		"""
		:newpat [IN]: int
		:angle1 [IN]: float
		:angle2 [IN]: float
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetHatchPattern(newpat, angle1, angle2)

	def GetImageInfo(self) -> tuple[int, float, float, float, float, str, int]:
		"""
		:xpos [OUT]: float
		:ypos [OUT]: float
		:xsize [OUT]: float
		:ysize [OUT]: float
		:filename [OUT]: str
		:embed [OUT]: int
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		return self._obj.GetImageInfo(dummy, dummy, dummy, dummy, dummy, dummy)

	def SetImageInfo(self, xpos:float, ypos:float, xsize:float, ysize:float, filename:str="", embed:int=-1) -> int:
		"""
		:xpos [IN]: float
		:ypos [IN]: float
		:xsize [IN]: float
		:ysize [IN]: float
		:filename [IN]: str Default value =""
		:embed [IN]: int Default value =-1
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.SetImageInfo(xpos, ypos, xsize, ysize, filename, embed)

	def OptimizeGraphicObjects(self, ids:list[int], mode:int, angle:int) -> tuple[int, list[int]]:
		"""
		:ids [IN/OUT]: list[int]
		:mode [IN]: int
		:angle [IN]: int
		:Return: int

		Available since TLB-Versions: 22.00, 22.00, 21.01, 20.22
		"""
		ret, ids = self._obj.OptimizeGraphicObjects(ids, mode, angle)
		ids = ids[1:] if type(ids) == list and len(ids) > 0 else []
		return ret, ids

	def GetInsideGraphIds(self, flags:int= 0 ) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:flags [IN]: int Default value = 0 
		:Return: int

		Available since TLB-Versions: 22.01
		"""
		dummy=0
		ret, ids = self._obj.GetInsideGraphIds(dummy, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def SendToForeground(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 24.22
		"""
		return self._obj.SendToForeground()

	def SendToBackground(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 24.22
		"""
		return self._obj.SendToBackground()

# -------------------- IDbeModelInterface--------------------
class DbeModel:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize DbeModel. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.12
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 19.12
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.12
		"""
		return self._obj.GetName()

	def GetCharacteristic(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.12
		"""
		return self._obj.GetCharacteristic()

	def ImportDXF(self, filename:str, scale:float, x:float, y:float, rot:int, font:str) -> int:
		"""
		:filename [IN]: str
		:scale [IN]: float
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: int
		:font [IN]: str
		:Return: int

		Available since TLB-Versions: 19.12
		"""
		return self._obj.ImportDXF(filename, scale, x, y, rot, font)

	def FitSpaceRequirement(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.12
		"""
		return self._obj.FitSpaceRequirement()

	def GetDXFSize(self, filename:str, font:str) -> tuple[int, float, float, float]:
		"""
		:filename [IN]: str
		:font [IN]: str
		:dx [OUT]: float
		:dy [OUT]: float
		:scale [OUT]: float
		:Return: int

		Available since TLB-Versions: 19.12
		"""
		dummy=0
		return self._obj.GetDXFSize(filename, font, dummy, dummy, dummy)

	def Save(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.12
		"""
		return self._obj.Save()

	def Remove(self, save_changes:bool=False) -> int:
		"""
		:save_changes [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 19.12
		"""
		return self._obj.Remove(save_changes)

	def ActivateModelView(self, modelview:int) -> int:
		"""
		:modelview [IN]: int
		:Return: int

		Available since TLB-Versions: 19.12
		"""
		return self._obj.ActivateModelView(modelview)

	def GetPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		dummy=0
		ret, ids = self._obj.GetPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def PlaceSymbol(self, symname:str, version:str, x:float, y:float, rot:str, flags:int=0) -> int:
		"""
		:symname [IN]: str
		:version [IN]: str
		:x [IN]: float
		:y [IN]: float
		:rot [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 21.00, 20.11, 19.41
		"""
		return self._obj.PlaceSymbol(symname, version, x, y, rot, flags)

	def GetGraphicIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 22.00, 21.01, 20.21
		"""
		dummy=0
		ret, ids = self._obj.GetGraphicIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def ImportStep(self, filename:str, flags:int=0) -> int:
		"""
		:filename [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.ImportStep(filename, flags)

	def DisplayOverviewOfExistingViews(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.00
		"""
		return self._obj.DisplayOverviewOfExistingViews(flags)

	def ExportImage(self, format:str, version:int, file:str, dpi:int=0, compressionmode:int=0, clrdepth:int=24, flags:int=1) -> int:
		"""
		:format [IN]: str
		:version [IN]: int
		:file [IN]: str
		:dpi [IN]: int Default value =0
		:compressionmode [IN]: int Default value =0
		:clrdepth [IN]: int Default value =24
		:flags [IN]: int Default value =1
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		return self._obj.ExportImage(format, version, file, dpi, compressionmode, clrdepth, flags)

	def GetDrawingArea(self, flags:int=1) -> tuple[int, float, float, float, float]:
		"""
		:xmin [OUT]: float
		:ymin [OUT]: float
		:xmax [OUT]: float
		:ymax [OUT]: float
		:flags [IN]: int Default value =1
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		dummy=0
		return self._obj.GetDrawingArea(dummy, dummy, dummy, dummy, flags)

	def ExportImageArea(self, format:str, version:int, file:str, xl:float, yl:float, xr:float, yr:float, width:int, height:int, clrdepth:int, gray:int, dpiX:int, dpiY:int, compressionmode:int, flags:int=0) -> int:
		"""
		:format [IN]: str
		:version [IN]: int
		:file [IN]: str
		:xl [IN]: float
		:yl [IN]: float
		:xr [IN]: float
		:yr [IN]: float
		:width [IN]: int
		:height [IN]: int
		:clrdepth [IN]: int
		:gray [IN]: int
		:dpiX [IN]: int
		:dpiY [IN]: int
		:compressionmode [IN]: int
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		return self._obj.ExportImageArea(format, version, file, xl, yl, xr, yr, width, height, clrdepth, gray, dpiX, dpiY, compressionmode, flags)

	def GetAttributeIds(self, attnam:str="", flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def AddAttributeValue(self, name:str, value:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		return self._obj.AddAttributeValue(name, value, flags)

	def GetSlotIds(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		dummy=0
		ret, ids = self._obj.GetSlotIds(dummy, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def DeleteModelView(self, flags:int) -> int:
		"""
		:flags [IN]: int
		:Return: int

		Available since TLB-Versions: 24.31
		"""
		return self._obj.DeleteModelView(flags)

	def DeleteStepModel(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.31
		"""
		return self._obj.DeleteStepModel(flags)

	def GetMountingDescriptions(self, flags:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:mountingdescriptions [OUT]: tuple[str,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.23
		"""
		dummy=0
		ret, mountingdescriptions = self._obj.GetMountingDescriptions(dummy, flags)
		mountingdescriptions = mountingdescriptions[1:] if type(mountingdescriptions) == tuple and len(mountingdescriptions) > 0 else tuple()
		return ret, mountingdescriptions

	def SetMountingDescriptions(self, mountingdescriptions:list[str], flags:int=0) -> int:
		"""
		:mountingdescriptions [IN]: list[str]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.23
		"""
		ret = self._obj.SetMountingDescriptions(mountingdescriptions, flags)
		return ret[0]

	def GetJustificationPoint(self, flags:int=0) -> tuple[int, float, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.23
		"""
		dummy=0
		return self._obj.GetJustificationPoint(dummy, dummy, dummy, flags)

	def GetJustificationLine(self, flags:int=0) -> tuple[int, float, float]:
		"""
		:y [OUT]: float
		:z [OUT]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.23
		"""
		dummy=0
		return self._obj.GetJustificationLine(dummy, dummy, flags)

	def GetJustificationArea(self, flags:int=0) -> tuple[int, float]:
		"""
		:z [OUT]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.23
		"""
		dummy=0
		return self._obj.GetJustificationArea(dummy, flags)

	def SetJustificationPoint(self, x:float, y:float, z:float, flags:int=0) -> int:
		"""
		:x [IN]: float
		:y [IN]: float
		:z [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.23
		"""
		return self._obj.SetJustificationPoint(x, y, z, flags)

	def SetJustificationLine(self, y:float, z:float, flags:int=0) -> int:
		"""
		:y [IN]: float
		:z [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.23
		"""
		return self._obj.SetJustificationLine(y, z, flags)

	def SetJustificationArea(self, z:float, flags:int=0) -> int:
		"""
		:z [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.23
		"""
		return self._obj.SetJustificationArea(z, flags)

	def GetStepTransformation(self, flags:int=0) -> tuple[int, tuple[float,...]]:
		"""
		:matrix [OUT]: tuple[float,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.31
		"""
		dummy=0
		ret, matrix = self._obj.GetStepTransformation(dummy, flags)
		matrix = matrix[1:] if type(matrix) == tuple and len(matrix) > 0 else tuple()
		return ret, matrix

# -------------------- IDbeModelPinInterface--------------------
class DbeModelPin:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize DbeModelPin. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		return self._obj.SetId(id)

	def GetCrimpingRules(self) -> tuple[int, memoryview]:
		"""
		:rules [OUT]: memoryview
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		dummy=0
		return self._obj.GetCrimpingRules(dummy)

	def SetCrimpingRules(self, rules:memoryview) -> int:
		"""
		:rules [IN]: memoryview
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		ret = self._obj.SetCrimpingRules(rules)
		return ret[0]

	def GetRoutingOffset(self, flags:int=0) -> tuple[int, float, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.00
		"""
		dummy=0
		return self._obj.GetRoutingOffset(dummy, dummy, dummy, flags)

	def SetRoutingOffset(self, x:float, y:float, z:float, flags:int=0) -> int:
		"""
		:x [IN]: float
		:y [IN]: float
		:z [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.00
		"""
		return self._obj.SetRoutingOffset(x, y, z, flags)

	def GetPinProperties(self, keyList:str="", flags:int=0) -> str:
		"""
		:keyList [IN]: str Default value =""
		:flags [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 25.31
		"""
		return self._obj.GetPinProperties(keyList, flags)

	def SetPinProperties(self, jsonInput:str, flags:int=0) -> int:
		"""
		:jsonInput [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.31
		"""
		return self._obj.SetPinProperties(jsonInput, flags)

# -------------------- IDbeNodeInterface--------------------
class DbeNode:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize DbeNode. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.21
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 21.21
		"""
		return self._obj.SetId(id)

	def GetDirection(self, flags:int= 0 ) -> int:
		"""
		:flags [IN]: int Default value = 0 
		:Return: int

		Available since TLB-Versions: 21.21
		"""
		return self._obj.GetDirection(flags)

	def IsBusPin(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.21
		"""
		return self._obj.IsBusPin()

	def HasPassWires(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.21
		"""
		return self._obj.HasPassWires()

	def GetTextIds(self, texttype:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:texttype [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 21.21
		"""
		dummy=0
		ret, ids = self._obj.GetTextIds(dummy, texttype)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetPosition(self) -> tuple[int, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:Return: int

		Available since TLB-Versions: 21.21
		"""
		dummy=0
		return self._obj.GetPosition(dummy, dummy)

	def IsBusbarPin(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		return self._obj.IsBusbarPin()

# -------------------- IDbeSlotInterface--------------------
class DbeSlot:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize DbeSlot. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		return self._obj.SetId(id)

	def GetDirection(self) -> tuple[int, float, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		dummy=0
		return self._obj.GetDirection(dummy, dummy, dummy)

	def GetFixType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		return self._obj.GetFixType()

	def GetMountType(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 24.11
		"""
		return self._obj.GetMountType()

	def GetPosition(self, point:int) -> tuple[int, float, float, float]:
		"""
		:point [IN]: int
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		dummy=0
		return self._obj.GetPosition(point, dummy, dummy, dummy)

	def GetRotation(self) -> tuple[int, float]:
		"""
		:angle [OUT]: float
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		dummy=0
		return self._obj.GetRotation(dummy)

	def GetSlotName(self, flags:int=0) -> str:
		"""
		:flags [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 24.11
		"""
		return self._obj.GetSlotName(flags)

	def SetSlotName(self, name:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		return self._obj.SetSlotName(name, flags)

	def GetAreaPolygon(self, flags:int=0) -> tuple[int, tuple[float,...], tuple[float,...], tuple[float,...]]:
		"""
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:zarr [OUT]: tuple[float,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.21
		"""
		dummy=0
		ret, xarr, yarr, zarr = self._obj.GetAreaPolygon(dummy, dummy, dummy, flags)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		zarr = zarr[1:] if type(zarr) == tuple and len(zarr) > 0 else tuple()
		return ret, xarr, yarr, zarr

	def CreatePoint(self, modelid:int, xpos:float, ypos:float, zpos:float, xdir:float, ydir:float, zdir:float, rotation:float, description:str, name:str, flags:int=0) -> int:
		"""
		:modelid [IN]: int
		:xpos [IN]: float
		:ypos [IN]: float
		:zpos [IN]: float
		:xdir [IN]: float
		:ydir [IN]: float
		:zdir [IN]: float
		:rotation [IN]: float
		:description [IN]: str
		:name [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.12
		"""
		return self._obj.CreatePoint(modelid, xpos, ypos, zpos, xdir, ydir, zdir, rotation, description, name, flags)

	def CreateLine(self, modelid:int, xpos:float, ypos:float, zpos:float, xdir:float, ydir:float, zdir:float, length:float, width:float, rotation:float, description:str, name:str, flags:int=0) -> int:
		"""
		:modelid [IN]: int
		:xpos [IN]: float
		:ypos [IN]: float
		:zpos [IN]: float
		:xdir [IN]: float
		:ydir [IN]: float
		:zdir [IN]: float
		:length [IN]: float
		:width [IN]: float
		:rotation [IN]: float
		:description [IN]: str
		:name [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.12
		"""
		return self._obj.CreateLine(modelid, xpos, ypos, zpos, xdir, ydir, zdir, length, width, rotation, description, name, flags)

	def CreateAreaRectangle(self, modelid:int, xpos:float, ypos:float, zpos:float, xdir:float, ydir:float, zdir:float, length:float, width:float, description:str, name:str, flags:int=0) -> int:
		"""
		:modelid [IN]: int
		:xpos [IN]: float
		:ypos [IN]: float
		:zpos [IN]: float
		:xdir [IN]: float
		:ydir [IN]: float
		:zdir [IN]: float
		:length [IN]: float
		:width [IN]: float
		:description [IN]: str
		:name [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.12
		"""
		return self._obj.CreateAreaRectangle(modelid, xpos, ypos, zpos, xdir, ydir, zdir, length, width, description, name, flags)

	def CreateAreaPolygon(self, modelid:int, xarr:list[float], yarr:list[float], zarr:list[float], xdir:float, ydir:float, zdir:float, description:str, name:str, flags:int=0) -> int:
		"""
		:modelid [IN]: int
		:xarr [IN]: list[float]
		:yarr [IN]: list[float]
		:zarr [IN]: list[float]
		:xdir [IN]: float
		:ydir [IN]: float
		:zdir [IN]: float
		:description [IN]: str
		:name [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.12
		"""
		xarr = [0.] + xarr
		yarr = [0.] + yarr
		zarr = [0.] + zarr
		return self._obj.CreateAreaPolygon(modelid, xarr, yarr, zarr, xdir, ydir, zdir, description, name, flags)

	def Delete(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.12
		"""
		return self._obj.Delete(flags)

	def SetRotation(self, rotation:float, flags:int=0) -> int:
		"""
		:rotation [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00
		"""
		return self._obj.SetRotation(rotation, flags)

	def GetDirectionRotation(self, flags:int=0) -> tuple[int, float, float, float]:
		"""
		:xAxisRotation [OUT]: float
		:yAxisRotation [OUT]: float
		:zAxisRotation [OUT]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00
		"""
		dummy=0
		return self._obj.GetDirectionRotation(dummy, dummy, dummy, flags)

	def SetDirectionRotation(self, xAxisRotation:float, yAxisRotation:float, zAxisRotation:float, flags:int=0) -> int:
		"""
		:xAxisRotation [IN]: float
		:yAxisRotation [IN]: float
		:zAxisRotation [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00
		"""
		return self._obj.SetDirectionRotation(xAxisRotation, yAxisRotation, zAxisRotation, flags)

	def GetLength(self, flags:int= 0 ) -> tuple[int, float]:
		"""
		:length [OUT]: float
		:flags [IN]: int Default value = 0 
		:Return: int

		Available since TLB-Versions: 26.01
		"""
		dummy=0
		return self._obj.GetLength(dummy, flags)

	def SetLength(self, length:float, flags:int= 0 ) -> int:
		"""
		:length [IN]: float
		:flags [IN]: int Default value = 0 
		:Return: int

		Available since TLB-Versions: 26.01
		"""
		return self._obj.SetLength(length, flags)

	def GetWidth(self, flags:int= 0 ) -> tuple[int, float]:
		"""
		:width [OUT]: float
		:flags [IN]: int Default value = 0 
		:Return: int

		Available since TLB-Versions: 26.01
		"""
		dummy=0
		return self._obj.GetWidth(dummy, flags)

	def SetWidth(self, width:float, flags:int= 0 ) -> int:
		"""
		:width [IN]: float
		:flags [IN]: int Default value = 0 
		:Return: int

		Available since TLB-Versions: 26.01
		"""
		return self._obj.SetWidth(width, flags)

	def GetDirectionEx(self, flags:int=0) -> tuple[int, float, float, float, int]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:side [OUT]: int
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.01
		"""
		dummy=0
		return self._obj.GetDirectionEx(dummy, dummy, dummy, dummy, flags)

# -------------------- IDbeJobInterface--------------------
class DbeJob:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize DbeJob. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def CreateDbeComponentObject(self) -> DbeComponent:
		"""
		:Return: DbeComponent

		Available since TLB-Versions: 24.41
		"""
		return DbeComponent(self._obj.CreateDbeComponentObject())

	def CreateDbeAttributeObject(self) -> DbeAttribute:
		"""
		:Return: DbeAttribute

		Available since TLB-Versions: 24.41
		"""
		return DbeAttribute(self._obj.CreateDbeAttributeObject())

	def CreateDbeSymbolObject(self) -> DbeSymbol:
		"""
		:Return: DbeSymbol

		Available since TLB-Versions: 24.41
		"""
		return DbeSymbol(self._obj.CreateDbeSymbolObject())

	def CreateDbeTextObject(self) -> DbeText:
		"""
		:Return: DbeText

		Available since TLB-Versions: 24.41
		"""
		return DbeText(self._obj.CreateDbeTextObject())

	def CreateDbeGraphObject(self) -> DbeGraph:
		"""
		:Return: DbeGraph

		Available since TLB-Versions: 24.41
		"""
		return DbeGraph(self._obj.CreateDbeGraphObject())

	def CreateDbeModelObject(self) -> DbeModel:
		"""
		:Return: DbeModel

		Available since TLB-Versions: 24.41
		"""
		return DbeModel(self._obj.CreateDbeModelObject())

	def CreateDbeModelPinObject(self) -> DbeModelPin:
		"""
		:Return: DbeModelPin

		Available since TLB-Versions: 24.41
		"""
		return DbeModelPin(self._obj.CreateDbeModelPinObject())

	def CreateDbeNodeObject(self) -> DbeNode:
		"""
		:Return: DbeNode

		Available since TLB-Versions: 24.41
		"""
		return DbeNode(self._obj.CreateDbeNodeObject())

	def CreateDbeSlotObject(self) -> DbeSlot:
		"""
		:Return: DbeSlot

		Available since TLB-Versions: 24.41
		"""
		return DbeSlot(self._obj.CreateDbeSlotObject())

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.SetId(id)

	def Save(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.Save(flags)

	def SaveAs(self, name:str, compressed:bool=False, flags:int=0) -> int:
		"""
		:name [IN]: str
		:compressed [IN]: bool Default value =False
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.SaveAs(name, compressed, flags)

	def NewModel(self, name:str, baseName:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:baseName [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.NewModel(name, baseName, flags)

	def EditModel(self, name:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.EditModel(name, flags)

	def DeleteModel(self, name:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.DeleteModel(name, flags)

	def GetModelIds(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		dummy=0
		ret, ids = self._obj.GetModelIds(dummy, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetActiveModelId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.GetActiveModelId()

	def NewSymbol(self, name:str, version:str, baseName:str, baseVersion:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:baseName [IN]: str
		:baseVersion [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.NewSymbol(name, version, baseName, baseVersion, flags)

	def EditSymbol(self, name:str, version:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.EditSymbol(name, version, flags)

	def DeleteSymbol(self, name:str, version:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.DeleteSymbol(name, version, flags)

	def GetSymbolIds(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		dummy=0
		ret, ids = self._obj.GetSymbolIds(dummy, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetActiveSymbolId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.GetActiveSymbolId()

	def NewComponent(self, name:str, version:str, baseName:str, baseVersion:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:baseName [IN]: str
		:baseVersion [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.NewComponent(name, version, baseName, baseVersion, flags)

	def EditComponent(self, name:str, version:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.EditComponent(name, version, flags)

	def DeleteComponent(self, name:str, version:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.DeleteComponent(name, version, flags)

	def GetComponentIds(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		dummy=0
		ret, ids = self._obj.GetComponentIds(dummy, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetActiveComponentId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.GetActiveComponentId()

	def Close(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.Close(flags)

	def New(self, name:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.New(name, flags)

	def Create(self, name:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.Create(name, flags)

	def Open(self, name:str, flags:int=0) -> int:
		"""
		:name [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.Open(name, flags)

	def GetPath(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 24.41
		"""
		return self._obj.GetPath()

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 24.41
		"""
		return self._obj.GetName()

	def GetType(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 24.41
		"""
		return self._obj.GetType()

	def GetSettingValue(self, name:str) -> typing.Union[str,int]:
		"""
		:name [IN]: str
		:Return: typing.Union[str,int]

		Available since TLB-Versions: 24.41
		"""
		return self._obj.GetSettingValue(name)

	def SetSettingValue(self, name:str, value:typing.Union[str,int]) -> typing.Union[str,int]:
		"""
		:name [IN]: str
		:value [IN]: typing.Union[str,int]
		:Return: typing.Union[str,int]

		Available since TLB-Versions: 24.41
		"""
		return self._obj.SetSettingValue(name, value)

	def GetOutbarText(self, index:int) -> tuple[int, tuple[str,...]]:
		"""
		:index [IN]: int
		:lst [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 25.32
		"""
		dummy=0
		ret, lst = self._obj.GetOutbarText(index, dummy)
		lst = lst[1:] if type(lst) == tuple and len(lst) > 0 else tuple()
		return ret, lst

	def GetResultText(self, index:int) -> tuple[int, tuple[str,...]]:
		"""
		:index [IN]: int
		:lst [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 25.32
		"""
		dummy=0
		ret, lst = self._obj.GetResultText(index, dummy)
		lst = lst[1:] if type(lst) == tuple and len(lst) > 0 else tuple()
		return ret, lst

# -------------------- IDbeApplicationInterface--------------------
class DbeApplication:
	def __init__(self, pid: typing.Optional[int]=None) -> None:
		if pid is None:
			pid = _get_default_dbe()
		if pid is None:
			raise RuntimeError('No instance of E3.DatabaseEditor is currently running')
		self._obj = _raw_connect_dbe(pid)

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetName()

	def GetVersion(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetVersion()

	def GetFullName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetFullName()

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetId()

	def Quit(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.Quit()

	def Sleep(self, msec:int) -> int:
		"""
		:msec [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.Sleep(msec)

	def Minimize(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.Minimize()

	def Maximize(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.Maximize()

	def Display(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.Display()

	def ShowNormal(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.ShowNormal()

	def PutMessage(self, text:str, item:int=0) -> int:
		"""
		:text [IN]: str
		:item [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.PutMessage(text, item)

	def PutInfo(self, ok:int, text:str, item:int=0) -> int:
		"""
		:ok [IN]: int
		:text [IN]: str
		:item [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.PutInfo(ok, text, item)

	def PutWarning(self, ok:int, text:str, item:int=0) -> int:
		"""
		:ok [IN]: int
		:text [IN]: str
		:item [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.PutWarning(ok, text, item)

	def PutError(self, ok:int, text:str, item:int=0) -> int:
		"""
		:ok [IN]: int
		:text [IN]: str
		:item [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.PutError(ok, text, item)

	def GetTestMark(self, num:int) -> int:
		"""
		:num [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetTestMark(num)

	def SetTestMark(self, num:int, value:int) -> int:
		"""
		:num [IN]: int
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetTestMark(num, value)

	def SetPrinterLinewidth(self, linewidth:float) -> float:
		"""
		:linewidth [IN]: float
		:Return: float

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetPrinterLinewidth(linewidth)

	def GetInstallationPath(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetInstallationPath()

	def GetInstallationLanguage(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetInstallationLanguage()

	def EnableLogfile(self, en:int) -> int:
		"""
		:en [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.EnableLogfile(en)

	def GetComponentDatabase(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetComponentDatabase()

	def GetConfigurationDatabase(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetConfigurationDatabase()

	def GetSymbolDatabase(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetSymbolDatabase()

	def GetLicense(self, feature:str) -> int:
		"""
		:feature [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetLicense(feature)

	def FreeLicense(self, feature:str) -> int:
		"""
		:feature [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.FreeLicense(feature)

	def GetInfoCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetInfoCount()

	def GetWarningCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetWarningCount()

	def GetErrorCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetErrorCount()

	def GetScriptArguments(self) -> tuple[str,...]:
		"""
		:Return: tuple[str,...]

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetScriptArguments()

	def SortArrayByIndex(self, array:list[typing.Any], rows:int, columns:int, sortindex1:int, sortindex2:int) -> tuple[int, list[typing.Any]]:
		"""
		:array [IN/OUT]: list[typing.Any]
		:rows [IN]: int
		:columns [IN]: int
		:sortindex1 [IN]: int
		:sortindex2 [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SortArrayByIndex(array, rows, columns, sortindex1, sortindex2)

	def FullName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.FullName()

	def ScriptArguments(self) -> tuple[str,...]:
		"""
		:Return: tuple[str,...]

		Available since TLB-Versions: 10.00
		"""
		return self._obj.ScriptArguments()

	def IsCable(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsCable()

	def IsSchema(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsSchema()

	def IsMultiuser(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsMultiuser()

	def IsPanel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsPanel()

	def IsWire(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsWire()

	def IsSmallBusiness(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsSmallBusiness()

	def IsDemo(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsDemo()

	def IsViewer(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsViewer()

	def IsViewPlus(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsViewPlus()

	def IsStudent(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsStudent()

	def IsCaddyDemo(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsCaddyDemo()

	def GetBuild(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetBuild()

	def SortArrayByIndexEx(self, array:list[typing.Any], options:list[typing.Any]) -> tuple[int, list[typing.Any]]:
		"""
		:array [IN/OUT]: list[typing.Any]
		:options [IN]: list[typing.Any]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SortArrayByIndexEx(array, options)

	def GetRegistryVersion(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetRegistryVersion()

	def GetLanguageDatabase(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetLanguageDatabase()

	def IsRedliner(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsRedliner()

	def ClearOutputWindow(self) -> None:
		"""

		Available since TLB-Versions: 10.00
		"""
		return self._obj.ClearOutputWindow()

	def AvoidAutomaticClosing(self, avoid:bool=True) -> bool:
		"""
		:avoid [IN]: bool Default value =True
		:Return: bool

		Available since TLB-Versions: 10.00
		"""
		return self._obj.AvoidAutomaticClosing(avoid)

	def ScriptFullName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.ScriptFullName()

	def ScriptName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.ScriptName()

	def GetPluginObject(self, Plugin:typing.Any) -> typing.Any:
		"""
		:Plugin [IN]: typing.Any
		:Return: typing.Any

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetPluginObject(Plugin)

	def Include(self, text:str) -> int:
		"""
		:text [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.Include(text)

	def GetLogfileName(self, index:int=0) -> str:
		"""
		:index [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetLogfileName(index)

	def SetLogfileName(self, logfile:str, index:int=0) -> int:
		"""
		:logfile [IN]: str
		:index [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetLogfileName(logfile, index)

	def GetWorkspaceName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetWorkspaceName()

	def GetActualDatabase(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetActualDatabase()

	def SetActualDatabase(self, dbname:str) -> int:
		"""
		:dbname [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetActualDatabase(dbname)

	def GetDefinedDatabases(self) -> tuple[int, tuple[str,...]]:
		"""
		:dbnames [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, dbnames = self._obj.GetDefinedDatabases(dummy)
		dbnames = dbnames[1:] if type(dbnames) == tuple and len(dbnames) > 0 else tuple()
		return ret, dbnames

	def GetDefinedDatabaseConnectionStrings(self, dbname:str) -> tuple[int, str, str, str]:
		"""
		:dbname [IN]: str
		:cmp_cs [OUT]: str
		:sym_cs [OUT]: str
		:cnf_cs [OUT]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		return self._obj.GetDefinedDatabaseConnectionStrings(dbname, dummy, dummy, dummy)

	def SetDefinedDatabaseConnectionStrings(self, dbname:str, cmp_cs:str, sym_cs:str, cnf_cs:str) -> int:
		"""
		:dbname [IN]: str
		:cmp_cs [IN]: str
		:sym_cs [IN]: str
		:cnf_cs [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetDefinedDatabaseConnectionStrings(dbname, cmp_cs, sym_cs, cnf_cs)

	def SetLanguageDatabase(self, dbname:str) -> int:
		"""
		:dbname [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetLanguageDatabase(dbname)

	def SetTemplateFileDBE(self, templatefilename:str) -> int:
		"""
		:templatefilename [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetTemplateFileDBE(templatefilename)

	def GetTemplateFileDBE(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetTemplateFileDBE()

	def IsScriptRunning(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsScriptRunning()

	def SetTriggerReturn(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetTriggerReturn(value)

	def GetTriggerReturn(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetTriggerReturn()

	def GetComponentDatabaseTableSchema(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetComponentDatabaseTableSchema()

	def GetConfigurationDatabaseTableSchema(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetConfigurationDatabaseTableSchema()

	def GetSymbolDatabaseTableSchema(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetSymbolDatabaseTableSchema()

	def GetLanguageDatabaseTableSchema(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetLanguageDatabaseTableSchema()

	def GetProcessProperty(self, what:str) -> str:
		"""
		:what [IN]: str
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetProcessProperty(what)

	def IsFluid(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsFluid()

	def IsFormboard(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsFormboard()

	def GetTrigger(self, name:str) -> tuple[int, str]:
		"""
		:name [IN]: str
		:filename [OUT]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		return self._obj.GetTrigger(name, dummy)

	def SetTrigger(self, name:str, filename:str, active:int) -> int:
		"""
		:name [IN]: str
		:filename [IN]: str
		:active [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetTrigger(name, filename, active)

	def IsEconomy(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsEconomy()

	def GetAvailableLanguages(self) -> tuple[int, tuple[str,...]]:
		"""
		:languages [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, languages = self._obj.GetAvailableLanguages(dummy)
		languages = languages[1:] if type(languages) == tuple and len(languages) > 0 else tuple()
		return ret, languages

	def GetTranslatedText(self, text:str, language:str) -> str:
		"""
		:text [IN]: str
		:language [IN]: str
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetTranslatedText(text, language)

	def Run(self, filename:str, arguments:list[str]) -> int:
		"""
		:filename [IN]: str
		:arguments [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.Run(filename, arguments)

	def SetScriptReturn(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetScriptReturn(value)

	def GetScriptReturn(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetScriptReturn()

	def GetEnableInteractiveDialogs(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetEnableInteractiveDialogs()

	def SetEnableInteractiveDialogs(self, value:bool) -> int:
		"""
		:value [IN]: bool
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetEnableInteractiveDialogs(value)

	def IsWireWorks(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsWireWorks()

	def SetModalWindow(self, hWnd:int) -> int:
		"""
		:hWnd [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetModalWindow(hWnd)

	def GetModalWindow(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetModalWindow()

	def BeginForeignTask(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.BeginForeignTask()

	def EndForeignTask(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.EndForeignTask()

	def IsFunctionalDesign(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsFunctionalDesign()

	def GetProjectInformation(self, filename:str) -> tuple[int, str, int, int]:
		"""
		:filename [IN/OUT]: str
		:_type [OUT]: int
		:is_dbe [OUT]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		return self._obj.GetProjectInformation(filename, dummy, dummy)

	def ResetInfoCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.ResetInfoCount()

	def ResetWarningCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.ResetWarningCount()

	def ResetErrorCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.ResetErrorCount()

	def GetLicensePermanent(self, feature:str) -> int:
		"""
		:feature [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetLicensePermanent(feature)

	def FreeLicensePermanent(self, feature:str) -> int:
		"""
		:feature [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.FreeLicensePermanent(feature)

	def GetProvider(self, dbname:str) -> str:
		"""
		:dbname [IN]: str
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetProvider(dbname)

	def GetPrintCropMarks(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.GetPrintCropMarks()

	def GetPrintPageNumbers(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.GetPrintPageNumbers()

	def SetPrintPageNumbers(self, set:bool) -> int:
		"""
		:set [IN]: bool
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.SetPrintPageNumbers(set)

	def SetPrintSheetOrder(self, set:int) -> int:
		"""
		:set [IN]: int
		:Return: int

		Available since TLB-Versions: 10.20
		"""
		return self._obj.SetPrintSheetOrder(set)

	def SelectComponentFromTable(self) -> tuple[int, str, str]:
		"""
		:ComponentName [OUT]: str
		:ComponentVersion [OUT]: str
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		dummy=0
		return self._obj.SelectComponentFromTable(dummy, dummy)

	def GetDatabaseTableSelectedComponents(self) -> tuple[int, tuple[str,...], tuple[str,...]]:
		"""
		:ComponentArray [OUT]: tuple[str,...]
		:VersionArray [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		dummy=0
		ret, ComponentArray, VersionArray = self._obj.GetDatabaseTableSelectedComponents(dummy, dummy)
		ComponentArray = ComponentArray[1:] if type(ComponentArray) == tuple and len(ComponentArray) > 0 else tuple()
		VersionArray = VersionArray[1:] if type(VersionArray) == tuple and len(VersionArray) > 0 else tuple()
		return ret, ComponentArray, VersionArray

	def GetDatabaseTreeSelectedComponents(self) -> tuple[int, tuple[str,...], tuple[str,...]]:
		"""
		:ComponentName [OUT]: tuple[str,...]
		:Version [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		dummy=0
		ret, ComponentName, Version = self._obj.GetDatabaseTreeSelectedComponents(dummy, dummy)
		ComponentName = ComponentName[1:] if type(ComponentName) == tuple and len(ComponentName) > 0 else tuple()
		Version = Version[1:] if type(Version) == tuple and len(Version) > 0 else tuple()
		return ret, ComponentName, Version

	def GetDatabaseTreeSelectedSymbols(self) -> tuple[int, tuple[str,...], tuple[str,...]]:
		"""
		:SymbolName [OUT]: tuple[str,...]
		:Version [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		dummy=0
		ret, SymbolName, Version = self._obj.GetDatabaseTreeSelectedSymbols(dummy, dummy)
		SymbolName = SymbolName[1:] if type(SymbolName) == tuple and len(SymbolName) > 0 else tuple()
		Version = Version[1:] if type(Version) == tuple and len(Version) > 0 else tuple()
		return ret, SymbolName, Version

	def GetDatabaseTreeSelectedModels(self) -> tuple[int, tuple[str,...]]:
		"""
		:ModelName [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		dummy=0
		ret, ModelName = self._obj.GetDatabaseTreeSelectedModels(dummy)
		ModelName = ModelName[1:] if type(ModelName) == tuple and len(ModelName) > 0 else tuple()
		return ret, ModelName

	def ClearResultWindow(self) -> None:
		"""

		Available since TLB-Versions: 11.80
		"""
		return self._obj.ClearResultWindow()

	def BringToForeground(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 11.90
		"""
		return self._obj.BringToForeground()

	def PutErrorEx(self, flags:int, text:str, item:int, red:int, green:int, blue:int) -> int:
		"""
		:flags [IN]: int
		:text [IN]: str
		:item [IN]: int
		:red [IN]: int
		:green [IN]: int
		:blue [IN]: int
		:Return: int

		Available since TLB-Versions: 11.90
		"""
		return self._obj.PutErrorEx(flags, text, item, red, green, blue)

	def PutWarningEx(self, flags:int, text:str, item:int, red:int, green:int, blue:int) -> int:
		"""
		:flags [IN]: int
		:text [IN]: str
		:item [IN]: int
		:red [IN]: int
		:green [IN]: int
		:blue [IN]: int
		:Return: int

		Available since TLB-Versions: 11.90
		"""
		return self._obj.PutWarningEx(flags, text, item, red, green, blue)

	def PutInfoEx(self, flags:int, text:str, item:int, red:int, green:int, blue:int) -> int:
		"""
		:flags [IN]: int
		:text [IN]: str
		:item [IN]: int
		:red [IN]: int
		:green [IN]: int
		:blue [IN]: int
		:Return: int

		Available since TLB-Versions: 11.90
		"""
		return self._obj.PutInfoEx(flags, text, item, red, green, blue)

	def PutMessageEx(self, flags:int, text:str, item:int, red:int, green:int, blue:int) -> int:
		"""
		:flags [IN]: int
		:text [IN]: str
		:item [IN]: int
		:red [IN]: int
		:green [IN]: int
		:blue [IN]: int
		:Return: int

		Available since TLB-Versions: 11.90
		"""
		return self._obj.PutMessageEx(flags, text, item, red, green, blue)

	def ActivateOutputWindow(self, windowId:int) -> int:
		"""
		:windowId [IN]: int
		:Return: int

		Available since TLB-Versions: 11.90
		"""
		return self._obj.ActivateOutputWindow(windowId)

	def SetChildWindowState(self, state:int) -> int:
		"""
		:state [IN]: int
		:Return: int

		Available since TLB-Versions: 17.70
		"""
		return self._obj.SetChildWindowState(state)

	def ShowPluginWindow(self, bShowPluginWindow:bool, guid:str) -> int:
		"""
		:bShowPluginWindow [IN]: bool
		:guid [IN]: str
		:Return: int

		Available since TLB-Versions: 17.70
		"""
		return self._obj.ShowPluginWindow(bShowPluginWindow, guid)

	def ShowWindow(self, windowId:int, show:bool) -> int:
		"""
		:windowId [IN]: int
		:show [IN]: bool
		:Return: int

		Available since TLB-Versions: 17.70
		"""
		return self._obj.ShowWindow(windowId, show)

	def SaveWorkspaceConfiguration(self, name:str="") -> int:
		"""
		:name [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 18.10
		"""
		return self._obj.SaveWorkspaceConfiguration(name)

	def DeleteWorkspaceConfiguration(self, name:str="") -> int:
		"""
		:name [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 18.10
		"""
		return self._obj.DeleteWorkspaceConfiguration(name)

	def RestoreWorkspaceConfiguration(self, name:str="") -> int:
		"""
		:name [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 18.10
		"""
		return self._obj.RestoreWorkspaceConfiguration(name)

	def GetWorkspaceConfigurations(self, path:str="") -> tuple[int, tuple[str,...]]:
		"""
		:names [OUT]: tuple[str,...]
		:path [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 18.10
		"""
		dummy=0
		ret, names = self._obj.GetWorkspaceConfigurations(dummy, path)
		names = names[1:] if type(names) == tuple and len(names) > 0 else tuple()
		return ret, names

	def LoadWorkspaceConfigurationFromFile(self, name:str, path:str) -> int:
		"""
		:name [IN]: str
		:path [IN]: str
		:Return: int

		Available since TLB-Versions: 18.10
		"""
		return self._obj.LoadWorkspaceConfigurationFromFile(name, path)

	def GetCurrentWorkspaceConfiguration(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 18.10
		"""
		return self._obj.GetCurrentWorkspaceConfiguration()

	def NewComponentWithPreconditions(self, name:str, version:str, baseName:str, baseVersion:str, preconditions:dict[str,str], flags:int=0) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:baseName [IN]: str
		:baseVersion [IN]: str
		:preconditions [IN]: dict[str,str]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 20.12, 19.42
		"""
		preconditions = _dict_to_variant(preconditions)
		return self._obj.NewComponentWithPreconditions(name, version, baseName, baseVersion, preconditions, flags)

	def EditComponentWithPreconditions(self, name:str, version:str, preconditions:dict[str,str], flags:int=0) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:preconditions [IN]: dict[str,str]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 20.12, 19.42
		"""
		preconditions = _dict_to_variant(preconditions)
		return self._obj.EditComponentWithPreconditions(name, version, preconditions, flags)

	def CreateDXFfromSTEP(self, stepFile:str, outputDirectory:str, dxfVersion:int, views:int=1, color:int=-1, flags:int=0) -> int:
		"""
		:stepFile [IN]: str
		:outputDirectory [IN]: str
		:dxfVersion [IN]: int
		:views [IN]: int Default value =1
		:color [IN]: int Default value =-1
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 22.41
		"""
		return self._obj.CreateDXFfromSTEP(stepFile, outputDirectory, dxfVersion, views, color, flags)

	def SuppressMessages(self, suppress:bool, flags:int=0) -> int:
		"""
		:suppress [IN]: bool
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 23.21
		"""
		return self._obj.SuppressMessages(suppress, flags)

	def SetConfigFile(self, processType:int, filepath:str, flags:int=0) -> str:
		"""
		:processType [IN]: int
		:filepath [IN]: str
		:flags [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 24.11
		"""
		return self._obj.SetConfigFile(processType, filepath, flags)

	def GetConfigFile(self, processType:int, flags:int=0) -> str:
		"""
		:processType [IN]: int
		:flags [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 24.11
		"""
		return self._obj.GetConfigFile(processType, flags)

	def GetComponentList(self, additionalAttributes:list[str,...]=pythoncom.Empty, flags:int=0) -> tuple[int, tuple[tuple[typing.Union[str,int],...],...]]:
		"""
		:result [OUT]: tuple[tuple[typing.Union[str,int],...],...], Enum types Available: e3series.types.ComponentType, ComponentSubType.
		:additionalAttributes [IN]: list[str,...] Default value =pythoncom.Empty
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		dummy=0
		return self._obj.GetComponentList(dummy, additionalAttributes, flags)

	def GetModelList(self, additionalAttributes:tuple[str,...]=0, flags:int=0) -> tuple[int, tuple[tuple[typing.Union[str,int],...],...]]:
		"""
		:result [OUT]: tuple[tuple[typing.Union[str,int],...],...]
		:additionalAttributes [IN]: tuple[str,...] Default value =0
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		dummy=0
		return self._obj.GetModelList(dummy, additionalAttributes, flags)

	def RemoveUndoInformation(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		return self._obj.RemoveUndoInformation(flags)

	def CreateDbeJobObject(self) -> DbeJob:
		"""
		:Return: DbeJob

		Available since TLB-Versions: 24.41
		"""
		return DbeJob(self._obj.CreateDbeJobObject())

	def GetJobCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		return self._obj.GetJobCount()

	def GetJobIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 24.41
		"""
		dummy=0
		ret, ids = self._obj.GetJobIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

# -------------------- IDeviceInterface--------------------
class Device:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Device. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetName(name)

	def GetAssignment(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAssignment()

	def SetAssignment(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAssignment(name)

	def GetLocation(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLocation()

	def SetLocation(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLocation(name)

	def GetFileName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFileName()

	def SetFileName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFileName(name)

	def GetComponentName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetComponentName()

	def GetComponentVersion(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetComponentVersion()

	def SetComponentName(self, name:str, version:str) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetComponentName(name, version)

	def GetCounterpartComponentName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCounterpartComponentName()

	def GetCounterpartComponentVersion(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCounterpartComponentVersion()

	def AddAttibuteValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttibuteValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasAttribute(name)

	def GetComponentAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetComponentAttributeValue(name)

	def GetViewCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetViewCount()

	def GetViewIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetViewIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsView(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsView()

	def GetViewNumber(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetViewNumber()

	def GetOriginalId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetOriginalId()

	def GetPinCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPinCount()

	def GetPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAllPinCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAllPinCount()

	def GetAllPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAllPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSupplyPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSupplyPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNoconnPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNoconnPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetEndAttributeCount(self, which:int) -> int:
		"""
		:which [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetEndAttributeCount(which)

	def GetEndAttributeIds(self, which:int, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:which [IN]: int
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetEndAttributeIds(which, dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetEndAttributeValue(self, which:int, name:str) -> str:
		"""
		:which [IN]: int
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetEndAttributeValue(which, name)

	def SetEndAttributeValue(self, which:int, name:str, value:str) -> int:
		"""
		:which [IN]: int
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetEndAttributeValue(which, name, value)

	def DeleteEndAttribute(self, which:int, name:str) -> int:
		"""
		:which [IN]: int
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteEndAttribute(which, name)

	def HasEndAttribute(self, which:int, name:str) -> int:
		"""
		:which [IN]: int
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasEndAttribute(which, name)

	def IsTerminal(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsTerminal()

	def IsTerminalBlock(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsTerminalBlock()

	def GetTerminalBlockId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTerminalBlockId()

	def SetTerminalSequence(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.SetTerminalSequence(ids)
		return ret[0]

	def GetSymbolCount(self, get_mode:int=0) -> int:
		"""
		:get_mode [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSymbolCount(get_mode)

	def GetSymbolIds(self, get_mode:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:get_mode [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSymbolIds(dummy, get_mode)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetBundleCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBundleCount()

	def GetBundleIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetBundleIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def Create(self, name:str, assignment:str, location:str, comp:str, vers:str, after:int) -> int:
		"""
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:comp [IN]: str
		:vers [IN]: str
		:after [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Create(name, assignment, location, comp, vers, after)

	def CreateView(self, _from:int, level:int, blockid:int=0, databaseDeviceView:str="") -> int:
		"""
		:_from [IN]: int
		:level [IN]: int
		:blockid [IN]: int Default value =0
		:databaseDeviceView [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateView(_from, level, blockid, databaseDeviceView)

	def IsDevice(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsDevice()

	def CreateCable(self, name:str, assignment:str, location:str) -> int:
		"""
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateCable(name, assignment, location)

	def IsCable(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsCable()

	def IsWireGroup(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsWireGroup()

	def CreateConnector(self, name:str, assignment:str, location:str) -> int:
		"""
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateConnector(name, assignment, location)

	def IsConnector(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsConnector()

	def IsBlock(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsBlock()

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete()

	def GetMasterPinName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetMasterPinName()

	def SetMasterPinName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetMasterPinName(name)

	def Jump(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Jump()

	def Search(self, name:str, assignment:str, location:str) -> int:
		"""
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Search(name, assignment, location)

	def GetConnectorCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConnectorCount()

	def GetConnectorIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetConnectorIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetBlockId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockId()

	def GetPanelLocation(self) -> tuple[int, float, float, float, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:rot [OUT]: float
		:pivot [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetPanelLocation(dummy, dummy, dummy, dummy, dummy)

	def IsMount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsMount()

	def IsCableDuct(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsCableDuct()

	def GetMountedCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetMountedCount()

	def GetMountedIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetMountedIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetCarrierId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCarrierId()

	def GetOutlineCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetOutlineCount()

	def GetOutlineIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetOutlineIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetValidComponentCodes(self) -> tuple[int, tuple[str,...]]:
		"""
		:names [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, names = self._obj.GetValidComponentCodes(dummy)
		names = names[1:] if type(names) == tuple and len(names) > 0 else tuple()
		return ret, names

	def IsAssembly(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsAssembly()

	def IsAssemblyPart(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsAssemblyPart()

	def GetAssemblyId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAssemblyId()

	def GetDeviceCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDeviceCount()

	def GetDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAssignedOptionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAssignedOptionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSupplyId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSupplyId()

	def SetSupplyId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetSupplyId(id)

	def HasNoconn(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasNoconn()

	def SetCompleteName(self, name:str, assignment:str, location:str, onlygiven:bool=False) -> int:
		"""
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:onlygiven [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetCompleteName(name, assignment, location, onlygiven)

	def CreateAssembly(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.CreateAssembly(ids)
		return ret[0]

	def AddToAssembly(self, ids:list[int], position:int=0, before:bool=False) -> int:
		"""
		:ids [IN]: list[int]
		:position [IN]: int Default value =0
		:before [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.AddToAssembly(ids, position, before)
		return ret[0]

	def RemoveFromAssembly(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.RemoveFromAssembly(ids)
		return ret[0]

	def CreateConnectorOnBlock(self, blkid:int, name:str, assignment:str, location:str) -> int:
		"""
		:blkid [IN]: int
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateConnectorOnBlock(blkid, name, assignment, location)

	def HasPassWirePins(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasPassWirePins()

	def SetPanelLocation(self, flags:int, shti:int, x:float, y:float, z:float, rot:str, use_start_z:bool=False, place_combined:bool=False, pivot:int=0) -> int:
		"""
		:flags [IN]: int
		:shti [IN]: int
		:x [IN]: float
		:y [IN]: float
		:z [IN]: float
		:rot [IN]: str
		:use_start_z [IN]: bool Default value =False
		:place_combined [IN]: bool Default value =False
		:pivot [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPanelLocation(flags, shti, x, y, z, rot, use_start_z, place_combined, pivot)

	def CreateCableDuct(self, name:str, assignment:str, location:str, xlen:float, ywid:float, zhgt:float, templ:str) -> int:
		"""
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:xlen [IN]: float
		:ywid [IN]: float
		:zhgt [IN]: float
		:templ [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateCableDuct(name, assignment, location, xlen, ywid, zhgt, templ)

	def CreateMount(self, name:str, assignment:str, location:str, xlen:float, ywid:float, zhgt:float, slotdes:str, templ:str) -> int:
		"""
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:xlen [IN]: float
		:ywid [IN]: float
		:zhgt [IN]: float
		:slotdes [IN]: str
		:templ [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateMount(name, assignment, location, xlen, ywid, zhgt, slotdes, templ)

	def UnplacePanel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UnplacePanel()

	def FindPanelPath(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.FindPanelPath()

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetSlotIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSlotIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetMountTypes(self) -> tuple[int, tuple[str,...]]:
		"""
		:types [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, types = self._obj.GetMountTypes(dummy)
		types = types[1:] if type(types) == tuple and len(types) > 0 else tuple()
		return ret, types

	def GetCableDuctLength(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCableDuctLength()

	def CreateBlock(self, name:str="", assignment:str="", location:str="", cmpname:str="", version:str="", filename:str="") -> int:
		"""
		:name [IN]: str Default value =""
		:assignment [IN]: str Default value =""
		:location [IN]: str Default value =""
		:cmpname [IN]: str Default value =""
		:version [IN]: str Default value =""
		:filename [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateBlock(name, assignment, location, cmpname, version, filename)

	def SetLockPurgeUnused(self, id:bool) -> int:
		"""
		:id [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLockPurgeUnused(id)

	def IsLockPurgeUnused(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsLockPurgeUnused()

	def SetViewNumber(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetViewNumber(id)

	def SetInheritName(self, onoff:int) -> int:
		"""
		:onoff [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetInheritName(onoff)

	def GetInheritName(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetInheritName()

	def GetRootAssemblyId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetRootAssemblyId()

	def InsertTerminalPlan(self, parameters:dict[str,str]) -> int:
		"""
		:parameters [IN]: dict[str,str]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		parameters = _dict_to_variant(parameters)
		return self._obj.InsertTerminalPlan(parameters)

	def GetSchematicTypes(self) -> tuple[int, tuple[int,...]]:
		"""
		:types [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, types = self._obj.GetSchematicTypes(dummy)
		types = types[1:] if type(types) == tuple and len(types) > 0 else tuple()
		return ret, types

	def GetTerminalPlanSheetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ShtIds [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ShtIds = self._obj.GetTerminalPlanSheetIds(dummy)
		ShtIds = ShtIds[1:] if type(ShtIds) == tuple and len(ShtIds) > 0 else tuple()
		return ret, ShtIds

	def SetModelCharacteristic(self, characteristic:str) -> int:
		"""
		:characteristic [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetModelCharacteristic(characteristic)

	def GetModelName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetModelName()

	def GetModelCharacteristic(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetModelCharacteristic()

	def GetValidModelCharacteristics(self) -> tuple[int, tuple[str,...]]:
		"""
		:characteristics [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, characteristics = self._obj.GetValidModelCharacteristics(dummy)
		characteristics = characteristics[1:] if type(characteristics) == tuple and len(characteristics) > 0 else tuple()
		return ret, characteristics

	def GetTerminalPlanSettings(self, parameters:dict[str,str]=pythoncom.Empty) -> tuple[int, dict[str,str]]:
		"""
		:parameters [IN/OUT]: dict[str,str] Default value =pythoncom.Empty
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		parameters = _dict_to_variant(parameters)
		ret, parameters = self._obj.GetTerminalPlanSettings(parameters)
		parameters = _variant_to_dict(parameters)
		return ret, parameters

	def SetTerminalPlanSettings(self, parameters:dict[str,str]) -> int:
		"""
		:parameters [IN]: dict[str,str]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		parameters = _dict_to_variant(parameters)
		ret = self._obj.SetTerminalPlanSettings(parameters)
		return ret[0]

	def IsHose(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsHose()

	def IsTube(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsTube()

	def CreateFormboard(self, _from:int, shtid:int, blockid:int=0, databaseDeviceView:str="") -> int:
		"""
		:_from [IN]: int
		:shtid [IN]: int
		:blockid [IN]: int Default value =0
		:databaseDeviceView [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateFormboard(_from, shtid, blockid, databaseDeviceView)

	def IsFormboard(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsFormboard()

	def GetFormboardSheetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFormboardSheetId()

	def GetFormboardIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetFormboardIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTableSymbolId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTableSymbolId()

	def IsClipboardPart(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsClipboardPart()

	def GetVariantObjectProperties(self, iObjectType:int, sAttributeName:str) -> tuple[int, tuple[typing.Union[tuple[str,int,str],tuple[str,int,str,int]],...]]:
		"""
		:iObjectType [IN]: int
		:sAttributeName [IN]: str
		:arr [OUT]: tuple[typing.Union[tuple[str,int,str],tuple[str,int,str,int]],...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, arr = self._obj.GetVariantObjectProperties(iObjectType, sAttributeName, dummy)
		arr = arr[1:] if type(arr) == tuple and len(arr) > 0 else tuple()
		return ret, arr

	def SetAssignedOptionIds(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAssignedOptionIds(ids)

	def DeleteInstance(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteInstance()

	def CreateInstance(self, vari:int) -> int:
		"""
		:vari [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateInstance(vari)

	def Create2DView(self, modi:int, name:str, symbol:str, position:int, before:int) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:symbol [IN]: str
		:position [IN]: int
		:before [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Create2DView(modi, name, symbol, position, before)

	def Has2DView(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Has2DView()

	def GetAssignedOptionExpressions(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressions(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def CreateOverbraid(self, name:str, assignment:str, location:str, cmpname:str, version:str) -> int:
		"""
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:cmpname [IN]: str
		:version [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateOverbraid(name, assignment, location, cmpname, version)

	def IsOverbraid(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsOverbraid()

	def IsOverbraidPart(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsOverbraidPart()

	def GetOverbraidId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetOverbraidId()

	def GetCableCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCableCount()

	def GetCableIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCableIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAnyCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAnyCount()

	def GetAnyIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAnyIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def AddToOverbraid(self, ids:list[int]=pythoncom.Empty, position:int=0, before:bool=False) -> int:
		"""
		:ids [IN]: list[int] Default value =pythoncom.Empty
		:position [IN]: int Default value =0
		:before [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.AddToOverbraid(ids, position, before)
		return ret[0]

	def RemoveFromOverbraid(self, ids:list[int]=pythoncom.Empty) -> int:
		"""
		:ids [IN]: list[int] Default value =pythoncom.Empty
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.RemoveFromOverbraid(ids)
		return ret[0]

	def GetCoreCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCoreCount()

	def GetCoreIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCoreIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAllCoreCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAllCoreCount()

	def GetAllCoreIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAllCoreIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def SetPanelPositionLock(self, onoff:int) -> int:
		"""
		:onoff [IN]: int
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.SetPanelPositionLock(onoff)

	def GetPanelPositionLock(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.GetPanelPositionLock()

	def DeleteInstanceForced(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.DeleteInstanceForced()

	def Sort(self, sort:int=0) -> int:
		"""
		:sort [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.Sort(sort)

	def SetPanelLevel(self, nLevel:int, bChangeMounted:bool) -> int:
		"""
		:nLevel [IN]: int
		:bChangeMounted [IN]: bool
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.SetPanelLevel(nLevel, bChangeMounted)

	def GetPanelLevel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.GetPanelLevel()

	def IsHierarchicalBlock(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.IsHierarchicalBlock()

	def IsFunctionalBlock(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.IsFunctionalBlock()

	def IsModule(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.IsModule()

	def SetModule(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.SetModule(newval)

	def DeleteForced(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.DeleteForced()

	def IsFunctionalDesignBlock(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.IsFunctionalDesignBlock()

	def GetFunctionalUnitIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetFunctionalUnitIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateFunctionalDesignBlock(self, name:str, assignment:str, location:str, cmpname:str, version:str) -> int:
		"""
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:cmpname [IN]: str
		:version [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.CreateFunctionalDesignBlock(name, assignment, location, cmpname, version)

	def GetDisconnecting(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetDisconnecting()

	def SetDisconnecting(self, onOff:bool) -> int:
		"""
		:onOff [IN]: bool
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetDisconnecting(onOff)

	def GetFunctionalBlockSymbolIDs(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetFunctionalBlockSymbolIDs(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def AssignAsVariantInstance(self, devid:int, expression:str) -> int:
		"""
		:devid [IN]: int
		:expression [IN]: str
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.AssignAsVariantInstance(devid, expression)

	def GetOuterDiameter(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetOuterDiameter()

	def SetOuterDiameter(self, newval:float) -> float:
		"""
		:newval [IN]: float
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetOuterDiameter(newval)

	def IsDynamicModel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.IsDynamicModel()

	def GetDynamicModelSize(self) -> tuple[int, float, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		return self._obj.GetDynamicModelSize(dummy, dummy, dummy)

	def SetDynamicModelSize(self, x:float, y:float, z:float) -> int:
		"""
		:x [IN]: float
		:y [IN]: float
		:z [IN]: float
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		ret = self._obj.SetDynamicModelSize(x, y, z)
		return ret[0]

	def SetOptionExpressions(self, expressions:list[str]) -> int:
		"""
		:expressions [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 9.12
		"""
		return self._obj.SetOptionExpressions(expressions)

	def LoadAndPlaceComponent(self, name:str, assignment:str, location:str, comp:str, vers:str, wirename:str, after:int, options:int) -> int:
		"""
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:comp [IN]: str
		:vers [IN]: str
		:wirename [IN]: str
		:after [IN]: int
		:options [IN]: int
		:Return: int

		Available since TLB-Versions: 9.20
		"""
		return self._obj.LoadAndPlaceComponent(name, assignment, location, comp, vers, wirename, after, options)

	def GetAssignedOptionExpressionsEx(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 9.23
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressionsEx(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def SetAttributeValueVariant(self, name:str, value:str, copy:int, VariantExpression:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:copy [IN]: int
		:VariantExpression [IN]: str
		:Return: int

		Available since TLB-Versions: 9.30
		"""
		return self._obj.SetAttributeValueVariant(name, value, copy, VariantExpression)

	def SearchAll(self, name:str, assignment:str, location:str) -> tuple[int, tuple[int,...]]:
		"""
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, ids = self._obj.SearchAll(name, assignment, location, dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def LockObject(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.LockObject()

	def UnlockObject(self, password:str) -> int:
		"""
		:password [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.UnlockObject(password)

	def IsLocked(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsLocked()

	def SetInterruptSignalFlow(self, sigflow:int=1) -> int:
		"""
		:sigflow [IN]: int Default value =1
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetInterruptSignalFlow(sigflow)

	def GetInterruptSignalFlow(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetInterruptSignalFlow()

	def IsHarness(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsHarness()

	def MergeHarnesses(self, ids:list[int]=pythoncom.Empty) -> int:
		"""
		:ids [IN]: list[int] Default value =pythoncom.Empty
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		ret = self._obj.MergeHarnesses(ids)
		return ret[0]

	def GetNetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, ids = self._obj.GetNetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def SortHarness(self, ids:list[int], postion:int, options:int) -> int:
		"""
		:ids [IN]: list[int]
		:postion [IN]: int
		:options [IN]: int
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		ret = self._obj.SortHarness(ids, postion, options)
		return ret[0]

	def UpdateDisconnecting(self, options:int) -> tuple[int, tuple[int,...]]:
		"""
		:options [IN]: int
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, ids = self._obj.UpdateDisconnecting(options, dummy)
		ids = () if ids is None else ids
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsInstallationSpace(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsInstallationSpace()

	def AddToInstallationSpace(self, ids:list[int]=pythoncom.Empty) -> int:
		"""
		:ids [IN]: list[int] Default value =pythoncom.Empty
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		ret = self._obj.AddToInstallationSpace(ids)
		return ret[0]

	def RemoveFromInstallationSpace(self, ids:list[int]=pythoncom.Empty) -> int:
		"""
		:ids [IN]: list[int] Default value =pythoncom.Empty
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		ret = self._obj.RemoveFromInstallationSpace(ids)
		return ret[0]

	def GetInstallationSpace(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetInstallationSpace()

	def AssignFunctionalUnits(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		ret = self._obj.AssignFunctionalUnits(ids)
		return ret[0]

	def AssignFunctionalUnitsDynamic(self, name:str, assignment:str, location:str, _type:int, ids:list[int]=pythoncom.Empty) -> int:
		"""
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:_type [IN]: int
		:ids [IN]: list[int] Default value =pythoncom.Empty
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		ret = self._obj.AssignFunctionalUnitsDynamic(name, assignment, location, _type, ids)
		return ret[0]

	def GetConnWithInsertsId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetConnWithInsertsId()

	def IsConnWithInsertsPart(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsConnWithInsertsPart()

	def IsConnWithInserts(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsConnWithInserts()

	def SetPanelFreePlacement(self, freeplacement:int=1) -> int:
		"""
		:freeplacement [IN]: int Default value =1
		:Return: int

		Available since TLB-Versions: 11.80
		"""
		return self._obj.SetPanelFreePlacement(freeplacement)

	def GetPanelFreePlacement(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 11.80
		"""
		return self._obj.GetPanelFreePlacement()

	def IsAssignmentLockChangeable(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 14.00
		"""
		return self._obj.IsAssignmentLockChangeable()

	def GetAssignmentLockChangeable(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 14.00
		"""
		return self._obj.GetAssignmentLockChangeable()

	def SetAssignmentLockChangeable(self, lockchangeable:bool) -> int:
		"""
		:lockchangeable [IN]: bool
		:Return: int

		Available since TLB-Versions: 14.00
		"""
		return self._obj.SetAssignmentLockChangeable(lockchangeable)

	def IsLocationLockChangeable(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 14.00
		"""
		return self._obj.IsLocationLockChangeable()

	def GetLocationLockChangeable(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 14.00
		"""
		return self._obj.GetLocationLockChangeable()

	def SetLocationLockChangeable(self, lockchangeable:bool) -> int:
		"""
		:lockchangeable [IN]: bool
		:Return: int

		Available since TLB-Versions: 14.00
		"""
		return self._obj.SetLocationLockChangeable(lockchangeable)

	def IsNameLockChangeable(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 14.00
		"""
		return self._obj.IsNameLockChangeable()

	def GetNameLockChangeable(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 14.00
		"""
		return self._obj.GetNameLockChangeable()

	def SetNameLockChangeable(self, lockchangeable:bool) -> int:
		"""
		:lockchangeable [IN]: bool
		:Return: int

		Available since TLB-Versions: 14.00
		"""
		return self._obj.SetNameLockChangeable(lockchangeable)

	def SetPanelLocationEx(self, flags:int, shti:int, x:float, y:float, z:float, rot:str, use_start_z:bool=False, place_combined:bool=False, pivot:int=0, shift_key:bool=False) -> int:
		"""
		:flags [IN]: int
		:shti [IN]: int
		:x [IN]: float
		:y [IN]: float
		:z [IN]: float
		:rot [IN]: str
		:use_start_z [IN]: bool Default value =False
		:place_combined [IN]: bool Default value =False
		:pivot [IN]: int Default value =0
		:shift_key [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 14.12
		"""
		return self._obj.SetPanelLocationEx(flags, shti, x, y, z, rot, use_start_z, place_combined, pivot, shift_key)

	def IsCableDuctInletOutlet(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 15.00
		"""
		return self._obj.IsCableDuctInletOutlet()

	def IsCableDuctInletOutletPart(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 15.00
		"""
		return self._obj.IsCableDuctInletOutletPart()

	def GetCableDuctInletOutletId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.GetCableDuctInletOutletId()

	def GetCableDuctInletOutlet(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		dummy=0
		ret, ids = self._obj.GetCableDuctInletOutlet(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def SetCableDuctLength(self, newlen:float) -> int:
		"""
		:newlen [IN]: float
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.SetCableDuctLength(newlen)

	def CreateCableDuctEx(self, name:str, assignment:str, location:str, xlen:float, ywid:float, zhgt:float, templ:str, flags:int, combwidth:float) -> int:
		"""
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:xlen [IN]: float
		:ywid [IN]: float
		:zhgt [IN]: float
		:templ [IN]: str
		:flags [IN]: int
		:combwidth [IN]: float
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.CreateCableDuctEx(name, assignment, location, xlen, ywid, zhgt, templ, flags, combwidth)

	def Get3DTransparency(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 15.81
		"""
		return self._obj.Get3DTransparency()

	def Set3DTransparency(self, mode:int) -> int:
		"""
		:mode [IN]: int
		:Return: int

		Available since TLB-Versions: 15.81
		"""
		return self._obj.Set3DTransparency(mode)

	def IsPinTerminalSymbolsUsed(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 16.00
		"""
		return self._obj.IsPinTerminalSymbolsUsed()

	def SetPinTerminalSymbolsUsed(self, use:int) -> int:
		"""
		:use [IN]: int
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		return self._obj.SetPinTerminalSymbolsUsed(use)

	def GetReferenceType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 16.01
		"""
		return self._obj.GetReferenceType()

	def SetReferenceType(self, _type:int) -> int:
		"""
		:_type [IN]: int
		:Return: int

		Available since TLB-Versions: 16.01
		"""
		return self._obj.SetReferenceType(_type)

	def Create2DViewEx(self, modi:int, name:str, symbol:str, position:int=0, before:int=0, shtId:int=0, xMin:float=0, yMin:float=0, xMax:float=0, yMax:float=0, scale:float=0) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:symbol [IN]: str
		:position [IN]: int Default value =0
		:before [IN]: int Default value =0
		:shtId [IN]: int Default value =0
		:xMin [IN]: float Default value =0
		:yMin [IN]: float Default value =0
		:xMax [IN]: float Default value =0
		:yMax [IN]: float Default value =0
		:scale [IN]: float Default value =0
		:Return: int

		Available since TLB-Versions: 16.01
		"""
		return self._obj.Create2DViewEx(modi, name, symbol, position, before, shtId, xMin, yMin, xMax, yMax, scale)

	def GetAssignedOptionExpressionsWithFlags(self, Term:int=0) -> tuple[int, tuple[tuple[str,int],...]]:
		"""
		:expressions [OUT]: tuple[tuple[str,int],...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 17.00
		"""
		var_expressions = VARIANT(pythoncom.VT_TYPEMASK, 0)
		ret, expressions = self._obj.GetAssignedOptionExpressionsWithFlags(var_expressions, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def SetOptionExpressionsWithFlags(self, expressions:list[tuple[str,int]]) -> int:
		"""
		:expressions [IN]: list[tuple[str,int]]
		:Return: int

		Available since TLB-Versions: 17.00
		"""
		expressions = [("",0)] + expressions
		return self._obj.SetOptionExpressionsWithFlags(expressions)

	def GetBlockDeviceIds(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 17.00
		"""
		dummy=0
		ret, ids = self._obj.GetBlockDeviceIds(dummy, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateDeviceOnBlock(self, blkid:int, name:str, assignment:str, location:str, comp:str, vers:str, after:int) -> int:
		"""
		:blkid [IN]: int
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:comp [IN]: str
		:vers [IN]: str
		:after [IN]: int
		:Return: int

		Available since TLB-Versions: 17.00
		"""
		return self._obj.CreateDeviceOnBlock(blkid, name, assignment, location, comp, vers, after)

	def GetMountLength(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 17.00, 16.12, 15.28
		"""
		return self._obj.GetMountLength()

	def GetTerminalType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 17.70
		"""
		return self._obj.GetTerminalType()

	def AutosolveTerminalstrip(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 17.70
		"""
		return self._obj.AutosolveTerminalstrip()

	def MergeTerminals(self, ids:list[int], compname:str, mergeterminalscontinuously:bool=False) -> int:
		"""
		:ids [IN]: list[int]
		:compname [IN]: str
		:mergeterminalscontinuously [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 17.70
		"""
		return self._obj.MergeTerminals(ids, compname, mergeterminalscontinuously)

	def BridgeTerminals(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 17.70
		"""
		return self._obj.BridgeTerminals(ids)

	def GetSealedState(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.GetSealedState()

	def SetSealedState(self, _type:int) -> int:
		"""
		:_type [IN]: int
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.SetSealedState(_type)

	def GetNameEx(self, flags:int) -> str:
		"""
		:flags [IN]: int
		:Return: str

		Available since TLB-Versions: 18.02, 17.31
		"""
		return self._obj.GetNameEx(flags)

	def GetAssignmentEx(self, flags:int) -> str:
		"""
		:flags [IN]: int
		:Return: str

		Available since TLB-Versions: 18.02, 17.31
		"""
		return self._obj.GetAssignmentEx(flags)

	def GetLocationEx(self, flags:int) -> str:
		"""
		:flags [IN]: int
		:Return: str

		Available since TLB-Versions: 18.02, 17.31
		"""
		return self._obj.GetLocationEx(flags)

	def GetSpaceRequirementOnCarrier(self, carrierid:int=0) -> tuple[int, tuple[int,...], tuple[int,...], tuple[int,...]]:
		"""
		:lowerleft [OUT]: tuple[int,...]
		:upperright [OUT]: tuple[int,...]
		:origin [OUT]: tuple[int,...]
		:carrierid [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 18.12
		"""
		dummy=0
		ret, lowerleft, upperright, origin = self._obj.GetSpaceRequirementOnCarrier(dummy, dummy, dummy, carrierid)
		lowerleft = lowerleft[1:] if type(lowerleft) == tuple and len(lowerleft) > 0 else tuple()
		upperright = upperright[1:] if type(upperright) == tuple and len(upperright) > 0 else tuple()
		origin = origin[1:] if type(origin) == tuple and len(origin) > 0 else tuple()
		return ret, lowerleft, upperright, origin

	def GetValidComponentCodesEx(self, flags:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:names [OUT]: tuple[str,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 18.80
		"""
		dummy=0
		ret, names = self._obj.GetValidComponentCodesEx(dummy, flags)
		names = names[1:] if type(names) == tuple and len(names) > 0 else tuple()
		return ret, names

	def IsLockedByAccessControl(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.IsLockedByAccessControl()

	def IsFeedThroughConnector(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.IsFeedThroughConnector()

	def PlugWithMatingPins(self) -> tuple[int, tuple[int,...]]:
		"""
		:deviceIds [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		dummy=0
		ret, deviceIds = self._obj.PlugWithMatingPins(dummy)
		deviceIds = deviceIds[1:] if type(deviceIds) == tuple and len(deviceIds) > 0 else tuple()
		return ret, deviceIds

	def UnplugFromMatingPins(self) -> tuple[int, tuple[int,...]]:
		"""
		:deviceIds [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		dummy=0
		ret, deviceIds = self._obj.UnplugFromMatingPins(dummy)
		deviceIds = deviceIds[1:] if type(deviceIds) == tuple and len(deviceIds) > 0 else tuple()
		return ret, deviceIds

	def PlugWith(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		return self._obj.PlugWith(id)

	def CreateConnectorOnBlockEx(self, blkid:int, name:str, assignment:str, location:str, cmpname:str, version:str) -> int:
		"""
		:blkid [IN]: int
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:cmpname [IN]: str
		:version [IN]: str
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		return self._obj.CreateConnectorOnBlockEx(blkid, name, assignment, location, cmpname, version)

	def PlaceOnPointSlot(self, slotid:int, rotation:float=0, pivot:int=0, combined:int=0) -> tuple[int, tuple[tuple[int,int],...]]:
		"""
		:slotid [IN]: int
		:rotation [IN]: float Default value =0
		:pivot [IN]: int Default value =0
		:combined [IN]: int Default value =0
		:collisionids [OUT]: tuple[tuple[int,int],...]
		:Return: int

		Available since TLB-Versions: 20.00, 19.11
		"""
		var_collisionids = VARIANT(pythoncom.VT_TYPEMASK, 0)
		ret, collisionids = self._obj.PlaceOnPointSlot(slotid, rotation, pivot, combined, var_collisionids)
		collisionids = () if collisionids is None else collisionids
		return ret, collisionids

	def PlaceOnLineSlot(self, slotid:int, x:float, rotation:float=0, combined:int=0) -> tuple[int, tuple[tuple[int,int],...]]:
		"""
		:slotid [IN]: int
		:x [IN]: float
		:rotation [IN]: float Default value =0
		:combined [IN]: int Default value =0
		:collisionids [OUT]: tuple[tuple[int,int],...]
		:Return: int

		Available since TLB-Versions: 20.00, 19.11
		"""
		var_collisionids = VARIANT(pythoncom.VT_TYPEMASK, 0)
		ret, collisionids = self._obj.PlaceOnLineSlot(slotid, x, rotation, combined, var_collisionids)
		collisionids = () if collisionids is None else collisionids
		return ret, collisionids

	def PlaceOnAreaSlot(self, slotid:int, x:float, y:float, rotation:float=0, pivot:int=0, combined:int=0) -> tuple[int, tuple[tuple[int,int],...]]:
		"""
		:slotid [IN]: int
		:x [IN]: float
		:y [IN]: float
		:rotation [IN]: float Default value =0
		:pivot [IN]: int Default value =0
		:combined [IN]: int Default value =0
		:collisionids [OUT]: tuple[tuple[int,int],...]
		:Return: int

		Available since TLB-Versions: 20.00, 19.11
		"""
		var_collisionids = VARIANT(pythoncom.VT_TYPEMASK, 0)
		ret, collisionids = self._obj.PlaceOnAreaSlot(slotid, x, y, rotation, pivot, combined, var_collisionids)
		collisionids = () if collisionids is None else collisionids
		return ret, collisionids

	def SortTerminals(self, method:int, sub_method:int=0, sort_file:str="") -> int:
		"""
		:method [IN]: int
		:sub_method [IN]: int Default value =0
		:sort_file [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 20.00, 19.11
		"""
		return self._obj.SortTerminals(method, sub_method, sort_file)

	def GetDefinedOuterDiameter(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 20.00, 19.12, 18.42
		"""
		return self._obj.GetDefinedOuterDiameter()

	def GetMountedSlotIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 20.00, 19.22
		"""
		dummy=0
		ret, ids = self._obj.GetMountedSlotIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetOverbraidIdEx(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 20.01, 19.24
		"""
		return self._obj.GetOverbraidIdEx()

	def GetRootOverbraidId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 20.01, 19.24
		"""
		return self._obj.GetRootOverbraidId()

	def GetJustificationPoint(self) -> tuple[int, float, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:Return: int

		Available since TLB-Versions: 20.05, 19.33
		"""
		dummy=0
		return self._obj.GetJustificationPoint(dummy, dummy, dummy)

	def GetJustificationLine(self) -> tuple[int, float, float]:
		"""
		:y [OUT]: float
		:z [OUT]: float
		:Return: int

		Available since TLB-Versions: 20.05, 19.33
		"""
		dummy=0
		return self._obj.GetJustificationLine(dummy, dummy)

	def GetJustificationArea(self) -> tuple[int, float]:
		"""
		:z [OUT]: float
		:Return: int

		Available since TLB-Versions: 20.05, 19.33
		"""
		dummy=0
		return self._obj.GetJustificationArea(dummy)

	def Create2DViewOfSlots(self, modi:int, name:str, symbol:str, slotslist:list[int], position:int=0, before:int=0, shtId:int=0, xMin:float=0, yMin:float=0, xMax:float=0, yMax:float=0, scale:float=0) -> int:
		"""
		:modi [IN]: int
		:name [IN]: str
		:symbol [IN]: str
		:slotslist [IN]: list[int]
		:position [IN]: int Default value =0
		:before [IN]: int Default value =0
		:shtId [IN]: int Default value =0
		:xMin [IN]: float Default value =0
		:yMin [IN]: float Default value =0
		:xMax [IN]: float Default value =0
		:yMax [IN]: float Default value =0
		:scale [IN]: float Default value =0
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.Create2DViewOfSlots(modi, name, symbol, slotslist, position, before, shtId, xMin, yMin, xMax, yMax, scale)

	def GetSpaceRequirement(self, flags:int) -> tuple[int, tuple[float,...], tuple[float,...], tuple[float,...]]:
		"""
		:flags [IN]: int
		:lowerleft [OUT]: tuple[float,...]
		:upperright [OUT]: tuple[float,...]
		:origin [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 21.12
		"""
		dummy=0
		ret, lowerleft, upperright, origin = self._obj.GetSpaceRequirement(flags, dummy, dummy, dummy)
		lowerleft = lowerleft[1:] if type(lowerleft) == tuple and len(lowerleft) > 0 else tuple()
		upperright = upperright[1:] if type(upperright) == tuple and len(upperright) > 0 else tuple()
		origin = origin[1:] if type(origin) == tuple and len(origin) > 0 else tuple()
		return ret, lowerleft, upperright, origin

	def GetCableDuctFillLimit(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.GetCableDuctFillLimit()

	def SetCableDuctFillLimit(self, percentage:int) -> int:
		"""
		:percentage [IN]: int
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.SetCableDuctFillLimit(percentage)

	def GetCableDuctWarningLimit(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.GetCableDuctWarningLimit()

	def SetCableDuctWarningLimit(self, percentage:int) -> int:
		"""
		:percentage [IN]: int
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.SetCableDuctWarningLimit(percentage)

	def SetStateId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 22.10
		"""
		return self._obj.SetStateId(id)

	def GetStateId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 22.10
		"""
		return self._obj.GetStateId()

	def IsPreventedAgainstPhysicalChangesOfCores(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		return self._obj.IsPreventedAgainstPhysicalChangesOfCores()

	def IsBusbar(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		return self._obj.IsBusbar()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

	def GetPhysicalLength(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetPhysicalLength()

	def GetAssignedBusbarPins(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		dummy=0
		ret, ids = self._obj.GetAssignedBusbarPins(dummy, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsPlacedInPanel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 24.00
		"""
		return self._obj.IsPlacedInPanel()

	def GetPanelLocationXYZEulerAngles(self) -> tuple[int, tuple[int,...], tuple[int,...], tuple[int,...], tuple[int,...], tuple[int,...], tuple[int,...]]:
		"""
		:x [OUT]: tuple[int,...]
		:y [OUT]: tuple[int,...]
		:z [OUT]: tuple[int,...]
		:xrot [OUT]: tuple[int,...]
		:yrot [OUT]: tuple[int,...]
		:zrot [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 24.00
		"""
		dummy=0
		ret, x, y, z, xrot, yrot, zrot = self._obj.GetPanelLocationXYZEulerAngles(dummy, dummy, dummy, dummy, dummy, dummy)
		x = x[1:] if type(x) == tuple and len(x) > 0 else tuple()
		y = y[1:] if type(y) == tuple and len(y) > 0 else tuple()
		z = z[1:] if type(z) == tuple and len(z) > 0 else tuple()
		xrot = xrot[1:] if type(xrot) == tuple and len(xrot) > 0 else tuple()
		yrot = yrot[1:] if type(yrot) == tuple and len(yrot) > 0 else tuple()
		zrot = zrot[1:] if type(zrot) == tuple and len(zrot) > 0 else tuple()
		return ret, x, y, z, xrot, yrot, zrot

	def SetPanelLocationXYZEulerAngles(self, flags:int, shti:int, x:float, y:float, z:float, xrot:float, yrot:float, zrot:float, use_start_z:bool=False, place_combined:bool=False, shift_key:bool=False) -> int:
		"""
		:flags [IN]: int
		:shti [IN]: int
		:x [IN]: float
		:y [IN]: float
		:z [IN]: float
		:xrot [IN]: float
		:yrot [IN]: float
		:zrot [IN]: float
		:use_start_z [IN]: bool Default value =False
		:place_combined [IN]: bool Default value =False
		:shift_key [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 24.00
		"""
		return self._obj.SetPanelLocationXYZEulerAngles(flags, shti, x, y, z, xrot, yrot, zrot, use_start_z, place_combined, shift_key)

	def ChangeAssignedOptionExpression(self, oldval:str, newval:str, oldflags:int=0, newflags:int=0) -> int:
		"""
		:oldval [IN]: str
		:newval [IN]: str
		:oldflags [IN]: int Default value =0
		:newflags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.01, 23.31
		"""
		return self._obj.ChangeAssignedOptionExpression(oldval, newval, oldflags, newflags)

	def PlaceModelViewAsGraphic(self, sheetId:int, x:float, y:float, rotation:str, modelView:int, flags:int=0) -> int:
		"""
		:sheetId [IN]: int
		:x [IN]: float
		:y [IN]: float
		:rotation [IN]: str
		:modelView [IN]: int
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.22
		"""
		return self._obj.PlaceModelViewAsGraphic(sheetId, x, y, rotation, modelView, flags)

	def SetJustificationPoint(self, x:float, y:float, z:float, flags:int=0) -> int:
		"""
		:x [IN]: float
		:y [IN]: float
		:z [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00, 25.23
		"""
		return self._obj.SetJustificationPoint(x, y, z, flags)

	def SetJustificationLine(self, y:float, z:float, flags:int=0) -> int:
		"""
		:y [IN]: float
		:z [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00, 25.23
		"""
		return self._obj.SetJustificationLine(y, z, flags)

	def SetJustificationArea(self, z:float, flags:int=0) -> int:
		"""
		:z [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00, 25.23
		"""
		return self._obj.SetJustificationArea(z, flags)

	def GetCableDuctWireAndCoreIds(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:coreIds [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00
		"""
		dummy=0
		ret, coreIds = self._obj.GetCableDuctWireAndCoreIds(dummy, flags)
		coreIds = coreIds[1:] if type(coreIds) == tuple and len(coreIds) > 0 else tuple()
		return ret, coreIds

	def GetConnectedCableDuctIds(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:connectedCableDuctIds [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00, 25.11
		"""
		dummy=0
		ret, connectedCableDuctIds = self._obj.GetConnectedCableDuctIds(dummy, flags)
		connectedCableDuctIds = connectedCableDuctIds[1:] if type(connectedCableDuctIds) == tuple and len(connectedCableDuctIds) > 0 else tuple()
		return ret, connectedCableDuctIds

# -------------------- IInfoApplicationInterface--------------------
class InfoApplication:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize InfoApplication. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetWindowPos(self, x:float, y:float, text:str) -> str:
		"""
		:x [IN]: float
		:y [IN]: float
		:text [IN]: str
		:Return: str

		Available since TLB-Versions: 13.00
		"""
		return self._obj.GetWindowPos(x, y, text)

# -------------------- IPinInterface--------------------
class Pin:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Pin. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def SetId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetId(id)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def SetName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetName(name)

	def SetNameSymbol(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetNameSymbol(name)

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttribute(name)

	def DeleteEndAttribute(self, which:int, name:str) -> int:
		"""
		:which [IN]: int
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteEndAttribute(which, name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasAttribute(name)

	def HasEndAttribute(self, which:int, name:str) -> int:
		"""
		:which [IN]: int
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasEndAttribute(which, name)

	def GetComponentAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetComponentAttributeValue(name)

	def GetEndAttributeCount(self, which:int) -> int:
		"""
		:which [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetEndAttributeCount(which)

	def GetEndAttributeIds(self, which:int, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:which [IN]: int
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetEndAttributeIds(which, dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetEndAttributeValue(self, which:int, name:str) -> str:
		"""
		:which [IN]: int
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetEndAttributeValue(which, name)

	def SetEndAttributeValue(self, which:int, name:str, value:str) -> int:
		"""
		:which [IN]: int
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetEndAttributeValue(which, name, value)

	def GetEndPinId(self, which:int, flags:int=0) -> int:
		"""
		:which [IN]: int
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetEndPinId(which, flags)

	def SetEndPinId(self, which:int, pini:int) -> int:
		"""
		:which [IN]: int
		:pini [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetEndPinId(which, pini)

	def GetConnectedPinId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConnectedPinId()

	def GetFitting(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFitting()

	def SetFitting(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFitting(name)

	def GetValidFittings(self) -> tuple[int, tuple[str,...]]:
		"""
		:strings [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, strings = self._obj.GetValidFittings(dummy)
		strings = strings[1:] if type(strings) == tuple and len(strings) > 0 else tuple()
		return ret, strings

	def GetSchemaLocation(self) -> tuple[int, float, float, str, str, str]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:grid [OUT]: str
		:column_value [OUT]: str
		:row_value [OUT]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetSchemaLocation(dummy, dummy, dummy, dummy, dummy)

	def GetPanelLocation(self) -> tuple[int, float, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetPanelLocation(dummy, dummy, dummy)

	def GetSequenceNumber(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSequenceNumber()

	def GetCoreCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCoreCount()

	def GetCoreIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCoreIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNetSegmentCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetNetSegmentCount()

	def GetNetSegmentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNetSegmentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetDestinationCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDestinationCount()

	def GetDestinationIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetDestinationIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSignalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSignalName()

	def SetSignalName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetSignalName(name)

	def Create(self, name:str, devi:int, pini:int, before:int) -> int:
		"""
		:name [IN]: str
		:devi [IN]: int
		:pini [IN]: int
		:before [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Create(name, devi, pini, before)

	def Search(self, name:str, devi:int) -> int:
		"""
		:name [IN]: str
		:devi [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Search(name, devi)

	def IsRouted(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsRouted()

	def GetLength(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLength()

	def GetCrossSection(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCrossSection()

	def GetCrossSectionDescription(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCrossSectionDescription()

	def GetColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetColour()

	def GetColourDescription(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetColourDescription()

	def GetConnectionType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConnectionType()

	def GetConnectionTypeDescription(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConnectionTypeDescription()

	def GetWireType(self) -> tuple[int, str, str]:
		"""
		:comp [OUT]: str
		:name [OUT]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetWireType(dummy, dummy)

	def SetWireType(self, comp:str, name:str) -> int:
		"""
		:comp [IN]: str
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetWireType(comp, name)

	def GetPanelPath(self) -> tuple[int, tuple[float,...], tuple[float,...], tuple[float,...]]:
		"""
		:xarr [OUT]: tuple[float,...]
		:yarr [OUT]: tuple[float,...]
		:zarr [OUT]: tuple[float,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, xarr, yarr, zarr = self._obj.GetPanelPath(dummy, dummy, dummy)
		xarr = xarr[1:] if type(xarr) == tuple and len(xarr) > 0 else tuple()
		yarr = yarr[1:] if type(yarr) == tuple and len(yarr) > 0 else tuple()
		zarr = zarr[1:] if type(zarr) == tuple and len(zarr) > 0 else tuple()
		return ret, xarr, yarr, zarr

	def SetLength(self, length:float) -> int:
		"""
		:length [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLength(length)

	def SetCrossSection(self, crossec:float) -> int:
		"""
		:crossec [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetCrossSection(crossec)

	def SetColour(self, color:int) -> int:
		"""
		:color [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetColour(color)

	def SetColourDescription(self, color:str) -> int:
		"""
		:color [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetColourDescription(color)

	def SetCrossSectionByDescription(self, description:str) -> int:
		"""
		:description [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetCrossSectionByDescription(description)

	def GetViewCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetViewCount()

	def GetViewIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetViewIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsView(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsView()

	def GetOriginalId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetOriginalId()

	def GetLogicalEquivalenceID(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLogicalEquivalenceID()

	def GetNameEquivalenceID(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetNameEquivalenceID()

	def GetExchangeableID(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetExchangeableID()

	def GetPhysicalID(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPhysicalID()

	def GetAssignedOptionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAssignedOptionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSupplyInfo(self) -> tuple[int, int, int, str]:
		"""
		:supid [OUT]: int
		:signum [OUT]: int
		:signam [OUT]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetSupplyInfo(dummy, dummy, dummy)

	def GetCCT(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCCT()

	def GetExternSignalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetExternSignalName()

	def IsSupply(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsSupply()

	def IsNoconn(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsNoconn()

	def GetNodeType(self) -> tuple[int, tuple[int,...]]:
		"""
		:_type [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, _type = self._obj.GetNodeType(dummy)
		_type = _type[1:] if type(_type) == tuple and len(_type) > 0 else tuple()
		return ret, _type

	def HasDevice(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasDevice()

	def CreateWire(self, name:str, cabtyp:str, wirnam:str, devi:int, pini:int, before:int) -> int:
		"""
		:name [IN]: str
		:cabtyp [IN]: str
		:wirnam [IN]: str
		:devi [IN]: int
		:pini [IN]: int
		:before [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.CreateWire(name, cabtyp, wirnam, devi, pini, before)

	def SetColourByDescription(self, color:str) -> int:
		"""
		:color [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetColourByDescription(color)

	def GetFunc(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFunc()

	def GetTextCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTextCount()

	def GetTextIds(self, txttyp:int=0, search_string:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:txttyp [IN]: int Default value =0
		:search_string [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTextIds(dummy, txttyp, search_string)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def Highlight(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Highlight()

	def FindPanelPath(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.FindPanelPath()

	def SetPanelPath(self, pnts:list[float], x:list[float], y:list[float], z:list[float], use_exact_coords:bool=False) -> int:
		"""
		:pnts [IN]: list[float]
		:x [IN]: list[float]
		:y [IN]: list[float]
		:z [IN]: list[float]
		:use_exact_coords [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		pnts = [0.] + pnts
		x = [0.] + x
		y = [0.] + y
		z = [0.] + z
		return self._obj.SetPanelPath(pnts, x, y, z, use_exact_coords)

	def DeletePanelPath(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeletePanelPath()

	def GetPassPins(self) -> tuple[int, tuple[int,...], int, int]:
		"""
		:ids [OUT]: tuple[int,...]
		:ends [OUT]: int
		:ende [OUT]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids, ends, ende = self._obj.GetPassPins(dummy, dummy, dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids, ends, ende

	def GetNetSegmentPath(self, pin1i:int, pin2i:int) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:pin1i [IN]: int
		:pin2i [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNetSegmentPath(dummy, pin1i, pin2i)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetPassWires(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetPassWires(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsPassWire(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsPassWire()

	def GetCableDuctIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCableDuctIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNodeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNodeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def SetNodeId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetNodeId(id)

	def SetDeviceId(self, devid:int, pinid:int, before:int) -> int:
		"""
		:devid [IN]: int
		:pinid [IN]: int
		:before [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDeviceId(devid, pinid, before)

	def Delete(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Delete()

	def GetValidCounterparts(self) -> tuple[int, tuple[int,...]]:
		"""
		:strings [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, strings = self._obj.GetValidCounterparts(dummy)
		strings = strings[1:] if type(strings) == tuple and len(strings) > 0 else tuple()
		return ret, strings

	def GetCounterpart(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCounterpart()

	def SetCounterpart(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetCounterpart(name)

	def GetPhysicalMaxConnections(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPhysicalMaxConnections()

	def GetPhysicalMinCrossSection(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPhysicalMinCrossSection()

	def GetPhysicalMaxCrossSection(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPhysicalMaxCrossSection()

	def GetPhysicalTotalMaxCrossSection(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPhysicalTotalMaxCrossSection()

	def GetPhysicalConnectionType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPhysicalConnectionType()

	def GetPhysicalConnectionTypeDescription(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPhysicalConnectionTypeDescription()

	def GetPhysicalPosition(self) -> tuple[int, float, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetPhysicalPosition(dummy, dummy, dummy)

	def GetPhysicalConnectionDirection(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPhysicalConnectionDirection()

	def GetPanelNetSegmentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetPanelNetSegmentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateNewConnectorForPins(self, pinidarray:list[int], name:str, assignment:str, location:str) -> int:
		"""
		:pinidarray [IN]: list[int]
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.CreateNewConnectorForPins(pinidarray, name, assignment, location)
		return ret[0]

	def AddPinsToConnector(self, pinidarray:list[int], name:str, assignment:str, location:str) -> int:
		"""
		:pinidarray [IN]: list[int]
		:name [IN]: str
		:assignment [IN]: str
		:location [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.AddPinsToConnector(pinidarray, name, assignment, location)
		return ret[0]

	def SetPhysicalConnectionDirection(self, conndir:int) -> int:
		"""
		:conndir [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPhysicalConnectionDirection(conndir)

	def GetPortName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPortName()

	def IsBackShell(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsBackShell()

	def GetDefaultWires(self) -> tuple[int, tuple[str,...], tuple[str,...]]:
		"""
		:wiregroups [OUT]: tuple[str,...]
		:wirenames [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, wiregroups, wirenames = self._obj.GetDefaultWires(dummy, dummy)
		wiregroups = wiregroups[1:] if type(wiregroups) == tuple and len(wiregroups) > 0 else tuple()
		wirenames = wirenames[1:] if type(wirenames) == tuple and len(wirenames) > 0 else tuple()
		return ret, wiregroups, wirenames

	def SetDefaultWires(self, wiregroups:list[str], wirenames:list[str]) -> int:
		"""
		:wiregroups [IN]: list[str]
		:wirenames [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.SetDefaultWires(wiregroups, wirenames)
		return ret[0]

	def LockCoreEnd(self, which:int, lock:int) -> int:
		"""
		:which [IN]: int
		:lock [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.LockCoreEnd(which, lock)

	def IsCoreEndLocked(self, which:int) -> int:
		"""
		:which [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsCoreEndLocked(which)

	def LockPanelPath(self, lock:int) -> int:
		"""
		:lock [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.LockPanelPath(lock)

	def IsPanelPathLocked(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsPanelPathLocked()

	def GetDiameter(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDiameter()

	def GetDiameterDescription(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDiameterDescription()

	def GetMaterial(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetMaterial()

	def GetMaterialDescription(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetMaterialDescription()

	def GetTemplateSymbolId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTemplateSymbolId()

	def GetLocking(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLocking()

	def SetLocking(self, bSet:bool) -> int:
		"""
		:bSet [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLocking(bSet)

	def PlaceNode(self, shtid:int, x:float, y:float) -> int:
		"""
		:shtid [IN]: int
		:x [IN]: float
		:y [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PlaceNode(shtid, x, y)

	def GetTypeId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTypeId()

	def IsPinView(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsPinView()

	def GetSchematicEndPinId(self, which:int) -> int:
		"""
		:which [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSchematicEndPinId(which)

	def SetAsInternal(self, onoff:int) -> int:
		"""
		:onoff [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAsInternal(onoff)

	def SetAsExternal(self, onoff:int) -> int:
		"""
		:onoff [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAsExternal(onoff)

	def IsInternal(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsInternal()

	def IsExternal(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsExternal()

	def AssignTo(self, pinids:list[int]) -> int:
		"""
		:pinids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AssignTo(pinids)

	def SetPhysicalConnectionType(self, conntyp:int) -> int:
		"""
		:conntyp [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPhysicalConnectionType(conntyp)

	def GetAssignedOptionExpressions(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressions(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def SetNetSegmentPathIds(self, netsegids:list[int]) -> int:
		"""
		:netsegids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.SetNetSegmentPathIds(netsegids)
		return ret[0]

	def GetDevicePinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetDevicePinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetOverbraidId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetOverbraidId()

	def GetRelativePermittivity(self) -> tuple[int, float]:
		"""
		:relativepermittivity [OUT]: float
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		dummy=0
		return self._obj.GetRelativePermittivity(dummy)

	def GetLossAngle(self) -> tuple[int, float]:
		"""
		:lossangle [OUT]: float
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		dummy=0
		return self._obj.GetLossAngle(dummy)

	def UnassignFrom(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.UnassignFrom(id)

	def ResetLength(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.ResetLength()

	def DeleteForced(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.DeleteForced()

	def GetOuterDiameter(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.00
		"""
		return self._obj.GetOuterDiameter()

	def GetFunctionalPortID(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetFunctionalPortID()

	def GetBlockConnectionNumber(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetBlockConnectionNumber()

	def SetOuterDiameter(self, newval:float) -> float:
		"""
		:newval [IN]: float
		:Return: float

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetOuterDiameter(newval)

	def SetOptionExpressions(self, expressions:list[str]) -> int:
		"""
		:expressions [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 9.12
		"""
		return self._obj.SetOptionExpressions(expressions)

	def GetAssignedOptionExpressionsEx(self, Term:int=0) -> tuple[int, tuple[str,...]]:
		"""
		:expressions [OUT]: tuple[str,...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 9.23
		"""
		dummy=0
		ret, expressions = self._obj.GetAssignedOptionExpressionsEx(dummy, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def GetDefinedOuterDiameter(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 9.30
		"""
		return self._obj.GetDefinedOuterDiameter()

	def LockObject(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.LockObject()

	def UnlockObject(self, password:str) -> int:
		"""
		:password [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.UnlockObject(password)

	def IsLocked(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.IsLocked()

	def SetInterruptSignalFlow(self, sigflow:int=1) -> int:
		"""
		:sigflow [IN]: int Default value =1
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetInterruptSignalFlow(sigflow)

	def GetInterruptSignalFlow(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetInterruptSignalFlow()

	def GetCoreManufacturingLength(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetCoreManufacturingLength()

	def GetNumberOfWindings(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetNumberOfWindings()

	def GetHarnessId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetHarnessId()

	def GetCoreWeight(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetCoreWeight()

	def GetCoreCost(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetCoreCost()

	def SetCoreCost(self, value:str) -> int:
		"""
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetCoreCost(value)

	def GetWireKindId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetWireKindId()

	def GetMergeSegment(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetMergeSegment()

	def SetMergeSegment(self, bSet:bool) -> int:
		"""
		:bSet [IN]: bool
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetMergeSegment(bSet)

	def GetConnectedPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		dummy=0
		ret, ids = self._obj.GetConnectedPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GenerateNewWireNames(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 10.20
		"""
		return self._obj.GenerateNewWireNames(ids)

	def GetConnectedNodeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.20
		"""
		dummy=0
		ret, ids = self._obj.GetConnectedNodeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CalculateFittingForWires(self, wirids:list[int]) -> tuple[int, tuple[int,...]]:
		"""
		:wirids [IN]: list[int]
		:fittinglst [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.23
		"""
		dummy=0
		ret, fittinglst = self._obj.CalculateFittingForWires(wirids, dummy)
		fittinglst = fittinglst[1:] if type(fittinglst) == tuple and len(fittinglst) > 0 else tuple()
		return ret, fittinglst

	def GetTranslatedSignalName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 11.00
		"""
		return self._obj.GetTranslatedSignalName()

	def GetVariantObjectProperties(self, iObjectType:int, sAttributeName:str) -> tuple[int, tuple[typing.Union[tuple[str,int,str],tuple[str,int,str,int]],...]]:
		"""
		:iObjectType [IN]: int
		:sAttributeName [IN]: str
		:arr [OUT]: tuple[typing.Union[tuple[str,int,str],tuple[str,int,str,int]],...]
		:Return: int

		Available since TLB-Versions: 11.11, 10.46
		"""
		dummy=0
		ret, arr = self._obj.GetVariantObjectProperties(iObjectType, sAttributeName, dummy)
		arr = arr[1:] if type(arr) == tuple and len(arr) > 0 else tuple()
		return ret, arr

	def GetTemplateSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 11.21, 14.00, 11.30
		"""
		dummy=0
		ret, ids = self._obj.GetTemplateSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def AddEndAttributeValue(self, which:int, name:str, value:str) -> int:
		"""
		:which [IN]: int
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 11.30
		"""
		return self._obj.AddEndAttributeValue(which, name, value)

	def GetCoreChangeIds(self, optids:list[int]=pythoncom.Empty) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:optids [IN]: list[int] Default value =pythoncom.Empty
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		dummy=0
		ret, ids = self._obj.GetCoreChangeIds(dummy, optids)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def SetCoreChangeId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.SetCoreChangeId(id)

	def GetFittingIds(self, optids:list[int]=pythoncom.Empty) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:optids [IN]: list[int] Default value =pythoncom.Empty
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		dummy=0
		ret, ids = self._obj.GetFittingIds(dummy, optids)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def SetFittingId(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 15.00
		"""
		return self._obj.SetFittingId(id)

	def SetPhysicalMaxConnections(self, conncount:int) -> int:
		"""
		:conncount [IN]: int
		:Return: int

		Available since TLB-Versions: 15.20
		"""
		return self._obj.SetPhysicalMaxConnections(conncount)

	def GetAssignedOptionExpressionsWithFlags(self, Term:int=0) -> tuple[int, tuple[tuple[str,int],...]]:
		"""
		:expressions [OUT]: tuple[tuple[str,int],...]
		:Term [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 17.00
		"""
		var_expressions = VARIANT(pythoncom.VT_TYPEMASK, 0)
		ret, expressions = self._obj.GetAssignedOptionExpressionsWithFlags(var_expressions, Term)
		expressions = expressions[1:] if type(expressions) == tuple and len(expressions) > 0 else tuple()
		return ret, expressions

	def SetOptionExpressionsWithFlags(self, expressions:list[tuple[str,int]]) -> int:
		"""
		:expressions [IN]: list[tuple[str,int]]
		:Return: int

		Available since TLB-Versions: 17.00
		"""
		expressions = [("",0)] + expressions
		return self._obj.SetOptionExpressionsWithFlags(expressions)

	def GetPinIndex(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 17.01, 16.13
		"""
		return self._obj.GetPinIndex()

	def SetDisableAutomaticFittingSelection(self, onoff:bool) -> int:
		"""
		:onoff [IN]: bool
		:Return: int

		Available since TLB-Versions: 17.13, 16.19
		"""
		return self._obj.SetDisableAutomaticFittingSelection(onoff)

	def GetDisableAutomaticFittingSelection(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 17.13, 16.19
		"""
		return self._obj.GetDisableAutomaticFittingSelection()

	def GetAllNetSegmentIds(self, flags:int) -> tuple[int, tuple[int,...], tuple[int,...], tuple[int,...], tuple[tuple[int,...],...]]:
		"""
		:flags [IN]: int
		:views [OUT]: tuple[int,...]
		:types [OUT]: tuple[int,...]
		:viewcounts [OUT]: tuple[int,...]
		:ids [OUT]: tuple[tuple[int,...],...]
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		dummy=0
		ret, views, types, viewcounts, ids = self._obj.GetAllNetSegmentIds(flags, dummy, dummy, dummy, dummy)
		views = views[1:] if type(views) == tuple and len(views) > 0 else tuple()
		types = types[1:] if type(types) == tuple and len(types) > 0 else tuple()
		viewcounts = viewcounts[1:] if type(viewcounts) == tuple and len(viewcounts) > 0 else tuple()
		return ret, views, types, viewcounts, ids

	def GetCavityPartIds(self, _type:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:_type [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		dummy=0
		ret, ids = self._obj.GetCavityPartIds(dummy, _type)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def SetOneTerminalPerCore(self, onoff:bool) -> int:
		"""
		:onoff [IN]: bool
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.SetOneTerminalPerCore(onoff)

	def GetOneTerminalPerCore(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.GetOneTerminalPerCore()

	def SetAllowMultipleWireCrimps(self, onoff:bool) -> int:
		"""
		:onoff [IN]: bool
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.SetAllowMultipleWireCrimps(onoff)

	def GetAllowMultipleWireCrimps(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.GetAllowMultipleWireCrimps()

	def GetValidWireSeals(self) -> tuple[int, tuple[str,...]]:
		"""
		:validWireSeals [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		dummy=0
		ret, validWireSeals = self._obj.GetValidWireSeals(dummy)
		validWireSeals = validWireSeals[1:] if type(validWireSeals) == tuple and len(validWireSeals) > 0 else tuple()
		return ret, validWireSeals

	def SetOuterDiameterByDescription(self, description:str) -> int:
		"""
		:description [IN]: str
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		return self._obj.SetOuterDiameterByDescription(description)

	def CalculateCavityPartsForWires(self, wirids:list[int]) -> tuple[int, tuple[str,...], tuple[str,...]]:
		"""
		:wirids [IN]: list[int]
		:fittinglst [OUT]: tuple[str,...]
		:wireseallst [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		dummy=0
		ret, fittinglst, wireseallst = self._obj.CalculateCavityPartsForWires(wirids, dummy, dummy)
		fittinglst = fittinglst[1:] if type(fittinglst) == tuple and len(fittinglst) > 0 else tuple()
		wireseallst = wireseallst[1:] if type(wireseallst) == tuple and len(wireseallst) > 0 else tuple()
		return ret, fittinglst, wireseallst

	def GetCavityPartsFromPinByCore(self, coreid:int, _type:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:coreid [IN]: int
		:cavityParts [OUT]: tuple[int,...]
		:_type [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 18.00
		"""
		dummy=0
		ret, cavityParts = self._obj.GetCavityPartsFromPinByCore(coreid, dummy, _type)
		cavityParts = cavityParts[1:] if type(cavityParts) == tuple and len(cavityParts) > 0 else tuple()
		return ret, cavityParts

	def IsLockedByAccessControl(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.IsLockedByAccessControl()

	def GetEndCavityPartIds(self, which:int, _type:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:which [IN]: int
		:cavities [OUT]: tuple[int,...]
		:_type [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		dummy=0
		ret, cavities = self._obj.GetEndCavityPartIds(which, dummy, _type)
		cavities = cavities[1:] if type(cavities) == tuple and len(cavities) > 0 else tuple()
		return ret, cavities

	def SetMultipleWireCrimps(self, conncount:int) -> int:
		"""
		:conncount [IN]: int
		:Return: int

		Available since TLB-Versions: 20.00, 19.01
		"""
		return self._obj.SetMultipleWireCrimps(conncount)

	def GetMultipleWireCrimps(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 20.00, 19.01
		"""
		return self._obj.GetMultipleWireCrimps()

	def AddDefaultWireEx(self, wiregroup:str, wirename:str) -> int:
		"""
		:wiregroup [IN]: str
		:wirename [IN]: str
		:Return: int

		Available since TLB-Versions: 20.00, 19.12
		"""
		return self._obj.AddDefaultWireEx(wiregroup, wirename)

	def DeleteDefaultWireEx(self, wiregroup:str, wirename:str) -> int:
		"""
		:wiregroup [IN]: str
		:wirename [IN]: str
		:Return: int

		Available since TLB-Versions: 20.00, 19.12
		"""
		return self._obj.DeleteDefaultWireEx(wiregroup, wirename)

	def GetWireKindDescription(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 20.00
		"""
		return self._obj.GetWireKindDescription()

	def PlugWithMatingPin(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		return self._obj.PlugWithMatingPin()

	def UnplugFromMatingPin(self) -> tuple[int, tuple[int,...]]:
		"""
		:pinIds [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		dummy=0
		ret, pinIds = self._obj.UnplugFromMatingPin(dummy)
		pinIds = pinIds[1:] if type(pinIds) == tuple and len(pinIds) > 0 else tuple()
		return ret, pinIds

	def GetPlugStatus(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		return self._obj.GetPlugStatus()

	def GetOverbraidIdEx(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 20.70, 20.01, 19.24
		"""
		return self._obj.GetOverbraidIdEx()

	def GetRootOverbraidId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 20.70, 20.01, 19.24
		"""
		return self._obj.GetRootOverbraidId()

	def SetLogicalEquivalenceID(self, equivalenceId:int, flags:int=0) -> int:
		"""
		:equivalenceId [IN]: int
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 20.71, 20.13
		"""
		return self._obj.SetLogicalEquivalenceID(equivalenceId, flags)

	def DeleteEx(self, list:list[int], forced:bool=False) -> int:
		"""
		:list [IN]: list[int]
		:forced [IN]: bool Default value =False
		:Return: int

		Available since TLB-Versions: 21.01, 20.22, 19.20
		"""
		ret = self._obj.DeleteEx(list, forced)
		return ret[0]

	def GetSymbolName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 21.01, 20.22
		"""
		return self._obj.GetSymbolName()

	def ResetHighlightPanelPath(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.11
		"""
		return self._obj.ResetHighlightPanelPath()

	def HighlightPanelPath(self, colour:int, width:float, flags:int) -> int:
		"""
		:colour [IN]: int
		:width [IN]: float
		:flags [IN]: int
		:Return: int

		Available since TLB-Versions: 21.11
		"""
		return self._obj.HighlightPanelPath(colour, width, flags)

	def GetPinGender(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.GetPinGender()

	def SetPinGender(self, gender:int) -> int:
		"""
		:gender [IN]: int
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.SetPinGender(gender)

	def GetWireHoseTubeStyle(self, flags:int=0) -> tuple[int, int, int, str, int, int, int, int, int]:
		"""
		:colour_code [OUT]: int
		:descr_type [OUT]: int
		:descr [OUT]: str
		:colour [OUT]: int
		:line_type [OUT]: int
		:Rvalue [OUT]: int
		:Gvalue [OUT]: int
		:Bvalue [OUT]: int
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 22.01, 21.30
		"""
		dummy=0
		return self._obj.GetWireHoseTubeStyle(dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy, flags)

	def IsCoreEndLockedPermanent(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		return self._obj.IsCoreEndLockedPermanent()

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def SetGID(self, gid:str) -> str:
		"""
		:gid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGID(gid)

	def GetGUID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGUID()

	def SetGUID(self, guid:str) -> str:
		"""
		:guid [IN]: str
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetGUID(guid)

	def AssignBusbar(self, ids:list[int], flags:int=0) -> int:
		"""
		:ids [IN]: list[int]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		return self._obj.AssignBusbar(ids, flags)

	def DeAssignBusbar(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		return self._obj.DeAssignBusbar(flags)

	def IsBusbar(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		return self._obj.IsBusbar()

	def GetInternalColourDescription(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 24.00
		"""
		return self._obj.GetInternalColourDescription()

	def ChangeAssignedOptionExpression(self, oldval:str, newval:str, oldflags:int=0, newflags:int=0) -> int:
		"""
		:oldval [IN]: str
		:newval [IN]: str
		:oldflags [IN]: int Default value =0
		:newflags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.01, 23.31
		"""
		return self._obj.ChangeAssignedOptionExpression(oldval, newval, oldflags, newflags)

	def GetRoutingOffset(self, flags:int=0) -> tuple[int, float, float, float]:
		"""
		:x [OUT]: float
		:y [OUT]: float
		:z [OUT]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.00
		"""
		dummy=0
		return self._obj.GetRoutingOffset(dummy, dummy, dummy, flags)

	def SetRoutingOffset(self, x:float, y:float, z:float, flags:int=0) -> int:
		"""
		:x [IN]: float
		:y [IN]: float
		:z [IN]: float
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.00
		"""
		return self._obj.SetRoutingOffset(x, y, z, flags)

	def GetWiringDirection(self, pin_item:int, carrierid:int=0, flags:int=0) -> tuple[int, float, float]:
		"""
		:pin_item [IN]: int
		:angle_1 [OUT]: float
		:angle_2 [OUT]: float
		:carrierid [IN]: int Default value =0
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.00, 24.31, 23.51
		"""
		dummy=0
		return self._obj.GetWiringDirection(pin_item, dummy, dummy, carrierid, flags)

	def GetColourDescriptionByInstallationLanguage(self, installationLanguage:int, flags:int=0) -> str:
		"""
		:installationLanguage [IN]: int
		:flags [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 25.00
		"""
		return self._obj.GetColourDescriptionByInstallationLanguage(installationLanguage, flags)

	def GetOriginalCoreName(self, flags:int=0) -> str:
		"""
		:flags [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 25.12, 24.43
		"""
		return self._obj.GetOriginalCoreName(flags)

	def IsUnmeasured(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.12, 24.45
		"""
		return self._obj.IsUnmeasured(flags)

	def GetComponentPinId(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 25.23
		"""
		return self._obj.GetComponentPinId(flags)

	def Get3DTransparency(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 27.00
		"""
		return self._obj.Get3DTransparency()

	def Set3DTransparency(self, mode:int) -> int:
		"""
		:mode [IN]: int
		:Return: int

		Available since TLB-Versions: 27.00
		"""
		return self._obj.Set3DTransparency(mode)

# -------------------- IJobInterface--------------------
class Job:
	def __init__(self, obj: typing.Any) -> None:
		try:
			obj
		except AttributeError:
			raise OSError("Cannot initialize Job. Use Create-methods of other objects to create an instance.")
		self._obj = obj

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def DumpItem(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DumpItem(id)

	def GetItemType(self, id:int) -> int:
		"""
		:id [IN]: int
		:Return: int, Enum type Available: e3series.types.ItemType.

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetItemType(id)

	def New(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.New(name)

	def Open(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Open(name)

	def ExportDrawing(self, name:str, shtids:list[int], options:int) -> int:
		"""
		:name [IN]: str
		:shtids [IN]: list[int]
		:options [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.ExportDrawing(name, shtids, options)
		return ret[0]

	def ImportDrawing(self, name:str, unique:int, posx:float=-950309, posy:float=-950309) -> int:
		"""
		:name [IN]: str
		:unique [IN]: int
		:posx [IN]: float Default value =-950309
		:posy [IN]: float Default value =-950309
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ImportDrawing(name, unique, posx, posy)

	def LoadPart(self, name:str, version:str, unique:int) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:unique [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.LoadPart(name, version, unique)

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def GetPath(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPath()

	def GetType(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetType()

	def Save(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Save()

	def SaveAs(self, name:str, compressed:bool=True) -> int:
		"""
		:name [IN]: str
		:compressed [IN]: bool Default value =True
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SaveAs(name, compressed)

	def Close(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Close()

	def IsChanged(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsChanged()

	def CreateSheetObject(self) -> Sheet:
		"""
		:Return: Sheet

		Available since TLB-Versions: 8.50
		"""
		return Sheet(self._obj.CreateSheetObject())

	def GetSheetCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSheetCount()

	def GetSheetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSheetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateDeviceObject(self) -> Device:
		"""
		:Return: Device

		Available since TLB-Versions: 8.50
		"""
		return Device(self._obj.CreateDeviceObject())

	def GetAllDeviceCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAllDeviceCount()

	def GetAllDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAllDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetDeviceCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDeviceCount()

	def GetDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetCableCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCableCount()

	def GetCableIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCableIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetBlockCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockCount()

	def GetBlockIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetBlockIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetConnectorCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConnectorCount()

	def GetConnectorIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetConnectorIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTerminalCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTerminalCount()

	def GetTerminalIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTerminalIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateComponentObject(self) -> Component:
		"""
		:Return: Component

		Available since TLB-Versions: 8.50
		"""
		return Component(self._obj.CreateComponentObject())

	def GetAllComponentCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAllComponentCount()

	def GetAllComponentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAllComponentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetComponentCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetComponentCount()

	def GetComponentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetComponentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetCableTypeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCableTypeCount()

	def GetCableTypeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetCableTypeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreatePinObject(self) -> Pin:
		"""
		:Return: Pin

		Available since TLB-Versions: 8.50
		"""
		return Pin(self._obj.CreatePinObject())

	def CreateGraphObject(self) -> Graph:
		"""
		:Return: Graph

		Available since TLB-Versions: 8.50
		"""
		return Graph(self._obj.CreateGraphObject())

	def CreateSymbolObject(self) -> Symbol:
		"""
		:Return: Symbol

		Available since TLB-Versions: 8.50
		"""
		return Symbol(self._obj.CreateSymbolObject())

	def GetSymbolCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSymbolCount()

	def GetSymbolIds(self, symnam:str="", level:int=-1, view:int=-1) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:symnam [IN]: str Default value =""
		:level [IN]: int Default value =-1
		:view [IN]: int Default value =-1
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSymbolIds(dummy, symnam, level, view)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateFieldObject(self) -> Field:
		"""
		:Return: Field

		Available since TLB-Versions: 8.50
		"""
		return Field(self._obj.CreateFieldObject())

	def GetFieldCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFieldCount()

	def GetFieldIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetFieldIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetFieldTextTemplate(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFieldTextTemplate()

	def SetFieldTextTemplate(self, newname:str) -> str:
		"""
		:newname [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFieldTextTemplate(newname)

	def CreateBundleObject(self) -> Bundle:
		"""
		:Return: Bundle

		Available since TLB-Versions: 8.50
		"""
		return Bundle(self._obj.CreateBundleObject())

	def GetBundleCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBundleCount()

	def GetBundleIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetBundleIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateTextObject(self) -> Text:
		"""
		:Return: Text

		Available since TLB-Versions: 8.50
		"""
		return Text(self._obj.CreateTextObject())

	def CreateAttributeObject(self) -> Attribute:
		"""
		:Return: Attribute

		Available since TLB-Versions: 8.50
		"""
		return Attribute(self._obj.CreateAttributeObject())

	def GetAttributeCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeCount()

	def GetAttributeIds(self, attnam:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:attnam [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeIds(dummy, attnam)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def AddAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddAttributeValue(name, value)

	def GetAttributeValue(self, name:str) -> str:
		"""
		:name [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeValue(name)

	def SetAttributeValue(self, name:str, value:str) -> int:
		"""
		:name [IN]: str
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeValue(name, value)

	def DeleteAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttribute(name)

	def HasAttribute(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.HasAttribute(name)

	def CreateConnectionObject(self) -> Connection:
		"""
		:Return: Connection

		Available since TLB-Versions: 8.50
		"""
		return Connection(self._obj.CreateConnectionObject())

	def GetConnectionCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConnectionCount()

	def GetConnectionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetConnectionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAllConnectionCount(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAllConnectionCount(flags)

	def GetAllConnectionIds(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAllConnectionIds(dummy, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateNetSegmentObject(self) -> NetSegment:
		"""
		:Return: NetSegment

		Available since TLB-Versions: 8.50
		"""
		return NetSegment(self._obj.CreateNetSegmentObject())

	def CreateSignalObject(self) -> Signal:
		"""
		:Return: Signal

		Available since TLB-Versions: 8.50
		"""
		return Signal(self._obj.CreateSignalObject())

	def GetSignalCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSignalCount()

	def GetSignalIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSignalIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateModuleObject(self) -> Module:
		"""
		:Return: Module

		Available since TLB-Versions: 8.50
		"""
		return Module(self._obj.CreateModuleObject())

	def GetRootModuleId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetRootModuleId()

	def GetModuleIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetModuleIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateModulePortObject(self) -> ModulePort:
		"""
		:Return: ModulePort

		Available since TLB-Versions: 8.50
		"""
		return ModulePort(self._obj.CreateModulePortObject())

	def ExportForeign(self, format:str, file:str) -> int:
		"""
		:format [IN]: str
		:file [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ExportForeign(format, file)

	def GetTextCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTextCount()

	def GetTextIds(self, txttyp:int=0, search_string:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:txttyp [IN]: int Default value =0
		:search_string [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTextIds(dummy, txttyp, search_string)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetGraphTextCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphTextCount()

	def CreateExternalDocumentObject(self) -> ExternalDocument:
		"""
		:Return: ExternalDocument

		Available since TLB-Versions: 8.50
		"""
		return ExternalDocument(self._obj.CreateExternalDocumentObject())

	def GetExternalDocumentCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetExternalDocumentCount()

	def GetExternalDocumentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetExternalDocumentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetGraphLevel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphLevel()

	def SetGraphLevel(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphLevel(value)

	def GetGraphColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphColour()

	def SetGraphColour(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphColour(value)

	def GetGraphWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphWidth()

	def SetGraphWidth(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphWidth(value)

	def GetGraphArrows(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphArrows()

	def SetGraphArrows(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphArrows(value)

	def GetGraphStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphStyle()

	def SetGraphStyle(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphStyle(value)

	def GetGraphTextFontName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphTextFontName()

	def SetGraphTextFontName(self, newname:str) -> str:
		"""
		:newname [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphTextFontName(newname)

	def GetGraphTextStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphTextStyle()

	def SetGraphTextStyle(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphTextStyle(value)

	def GetGraphTextMode(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphTextMode()

	def SetGraphTextMode(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphTextMode(value)

	def GetGraphTextSize(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphTextSize()

	def SetGraphTextSize(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphTextSize(value)

	def GetGraphTextColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphTextColour()

	def SetGraphTextColour(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphTextColour(value)

	def GetGraphTextLevel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphTextLevel()

	def SetGraphTextLevel(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphTextLevel(value)

	def GetGraphHatchPattern(self) -> tuple[int, float, float]:
		"""
		:angle1 [OUT]: float
		:angle2 [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetGraphHatchPattern(dummy, dummy)

	def SetGraphHatchPattern(self, value:int, angle1:float, angle2:float) -> int:
		"""
		:value [IN]: int
		:angle1 [IN]: float
		:angle2 [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphHatchPattern(value, angle1, angle2)

	def GetGraphHatchStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphHatchStyle()

	def SetGraphHatchStyle(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphHatchStyle(value)

	def GetGraphHatchWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphHatchWidth()

	def SetGraphHatchWidth(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphHatchWidth(value)

	def GetGraphHatchDistance(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphHatchDistance()

	def SetGraphHatchDistance(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphHatchDistance(value)

	def GetGraphHatchColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphHatchColour()

	def SetGraphHatchColour(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphHatchColour(value)

	def GetMeasure(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetMeasure()

	def SetMeasure(self, measure:str) -> int:
		"""
		:measure [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetMeasure(measure)

	def GetSelectedSheetCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedSheetCount()

	def GetSelectedSheetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedSheetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedDeviceCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedDeviceCount()

	def GetSelectedDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedCableCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedCableCount()

	def GetSelectedCableIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedCableIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedTerminalCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedTerminalCount()

	def GetSelectedTerminalIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedTerminalIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedConnectorCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedConnectorCount()

	def GetSelectedConnectorIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedConnectorIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedBlockCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedBlockCount()

	def GetSelectedBlockIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedBlockIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedAllDeviceCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedAllDeviceCount()

	def GetSelectedAllDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedAllDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedGraphCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedGraphCount()

	def GetSelectedGraphIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedGraphIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedTextCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedTextCount()

	def GetSelectedTextIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedTextIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedSymbolCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedSymbolCount()

	def GetSelectedSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedBundleCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedBundleCount()

	def GetSelectedBundleIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedBundleIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedConnectionCount(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedConnectionCount(flags)

	def GetSelectedConnectionIds(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedConnectionIds(dummy, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedNetSegmentCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedNetSegmentCount()

	def GetSelectedNetSegmentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedNetSegmentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedSignalCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSelectedSignalCount()

	def GetSelectedSignalIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedSignalIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetDeviceNameSeparator(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDeviceNameSeparator()

	def SetDeviceNameSeparator(self, newsep:str) -> str:
		"""
		:newsep [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDeviceNameSeparator(newsep)

	def GetLocationSeparator(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLocationSeparator()

	def SetLocationSeparator(self, newsep:str) -> str:
		"""
		:newsep [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLocationSeparator(newsep)

	def GetAssignmentSeparator(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAssignmentSeparator()

	def SetAssignmentSeparator(self, newsep:str) -> str:
		"""
		:newsep [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAssignmentSeparator(newsep)

	def GetLanguages(self) -> tuple[int, tuple[int,...]]:
		"""
		:languages [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, languages = self._obj.GetLanguages(dummy)
		languages = languages[1:] if type(languages) == tuple and len(languages) > 0 else tuple()
		return ret, languages

	def SetLanguages(self, languages:list[int]) -> int:
		"""
		:languages [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.SetLanguages(languages)
		return ret[0]

	def GetDisplayConnectionMode(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayConnectionMode()

	def SetDisplayConnectionMode(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayConnectionMode(value)

	def CreateVariantObject(self) -> Variant:
		"""
		:Return: Variant

		Available since TLB-Versions: 8.50
		"""
		return Variant(self._obj.CreateVariantObject())

	def GetVariantCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetVariantCount()

	def GetVariantIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetVariantIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetActiveVariantId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetActiveVariantId()

	def SetActiveVariantId(self, vari:int) -> int:
		"""
		:vari [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetActiveVariantId(vari)

	def CreateOptionObject(self) -> Option:
		"""
		:Return: Option

		Available since TLB-Versions: 8.50
		"""
		return Option(self._obj.CreateOptionObject())

	def GetOptionCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetOptionCount()

	def GetOptionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetOptionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetActiveOptionCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetActiveOptionCount()

	def GetActiveOptionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetActiveOptionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def SetActiveOptionIds(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.SetActiveOptionIds(ids)
		return ret[0]

	def ActivateOptionIds(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.ActivateOptionIds(ids)
		return ret[0]

	def DeactivateOptionIds(self, ids:list[int]) -> int:
		"""
		:ids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.DeactivateOptionIds(ids)
		return ret[0]

	def CreateOutlineObject(self) -> Outline:
		"""
		:Return: Outline

		Available since TLB-Versions: 8.50
		"""
		return Outline(self._obj.CreateOutlineObject())

	def PrintOut(self, scale:float, shtids:list[int]) -> int:
		"""
		:scale [IN]: float
		:shtids [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.PrintOut(scale, shtids)
		return ret[0]

	def GetCurrentUserNames(self) -> tuple[int, tuple[str,...]]:
		"""
		:names [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, names = self._obj.GetCurrentUserNames(dummy)
		names = names[1:] if type(names) == tuple and len(names) > 0 else tuple()
		return ret, names

	def NewMultiuser(self, name:str, description:str, filename:str, checkin:int, unlock:int=0) -> int:
		"""
		:name [IN]: str
		:description [IN]: str
		:filename [IN]: str
		:checkin [IN]: int
		:unlock [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.NewMultiuser(name, description, filename, checkin, unlock)

	def OpenMultiuser(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.OpenMultiuser(name)

	def ResetHighlight(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ResetHighlight()

	def GetLineColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLineColour()

	def SetLineColour(self, newcol:int) -> int:
		"""
		:newcol [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLineColour(newcol)

	def GetLineStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLineStyle()

	def SetLineStyle(self, newstl:int) -> int:
		"""
		:newstl [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLineStyle(newstl)

	def SetLineWidth(self, newwid:float) -> int:
		"""
		:newwid [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLineWidth(newwid)

	def GetLineLevel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLineLevel()

	def SetLineLevel(self, newlev:int) -> int:
		"""
		:newlev [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLineLevel(newlev)

	def SetBusLineColour(self, newcol:int) -> int:
		"""
		:newcol [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBusLineColour(newcol)

	def SetBusLineStyle(self, newstl:int) -> int:
		"""
		:newstl [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBusLineStyle(newstl)

	def SetBusLineWidth(self, newwid:float) -> int:
		"""
		:newwid [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBusLineWidth(newwid)

	def SetBusLineLevel(self, newlev:int) -> int:
		"""
		:newlev [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBusLineLevel(newlev)

	def GetPartExtension(self, part:str, vers:str) -> tuple[int, float, float, float, float, int, float, float, int]:
		"""
		:part [IN]: str
		:vers [IN]: str
		:xl [OUT]: float
		:yl [OUT]: float
		:xh [OUT]: float
		:yh [OUT]: float
		:shtcnt [OUT]: int
		:xp [OUT]: float
		:yp [OUT]: float
		:subcircuitType [OUT]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetPartExtension(part, vers, dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy)

	def GetGridSize(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGridSize()

	def SetGridSize(self, newsize:float) -> float:
		"""
		:newsize [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGridSize(newsize)

	def GetTrapSize(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTrapSize()

	def SetTrapSize(self, newsize:float) -> float:
		"""
		:newsize [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetTrapSize(newsize)

	def EnablePointGridDisplay(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.EnablePointGridDisplay()

	def DisablePointGridDisplay(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DisablePointGridDisplay()

	def GetPointGridSize(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPointGridSize()

	def SetPointGridSize(self, newsize:float) -> float:
		"""
		:newsize [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPointGridSize(newsize)

	def EnableRulerGridDisplay(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.EnableRulerGridDisplay()

	def DisableRulerGridDisplay(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DisableRulerGridDisplay()

	def GetRulerGridSize(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetRulerGridSize()

	def SetRulerGridSize(self, newsize:float) -> float:
		"""
		:newsize [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetRulerGridSize(newsize)

	def ExportPDF(self, file:str, shtids:list[int], options:int, password:str="") -> int:
		"""
		:file [IN]: str
		:shtids [IN]: list[int]
		:options [IN]: int
		:password [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.ExportPDF(file, shtids, options, password)
		return ret[0]

	def ImportDDSC(self, file:str, options:int, level:int=0) -> int:
		"""
		:file [IN]: str
		:options [IN]: int
		:level [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ImportDDSC(file, options, level)

	def GetGraphTextHeight(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGraphTextHeight()

	def SetGraphTextHeight(self, value:float) -> float:
		"""
		:value [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGraphTextHeight(value)

	def GetFileVersion(self, filename:str) -> int:
		"""
		:filename [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFileVersion(filename)

	def RepairCheckExtended(self, mode:int) -> int:
		"""
		:mode [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.RepairCheckExtended(mode)

	def GetOutbarText(self, index:int) -> tuple[int, tuple[str,...]]:
		"""
		:index [IN]: int
		:lst [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, lst = self._obj.GetOutbarText(index, dummy)
		lst = lst[1:] if type(lst) == tuple and len(lst) > 0 else tuple()
		return ret, lst

	def GetHighlightColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetHighlightColour()

	def SetHighlightColour(self, colour:int) -> int:
		"""
		:colour [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetHighlightColour(colour)

	def GetHighlightLineWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetHighlightLineWidth()

	def SetHighlightLineWidth(self, width:float) -> float:
		"""
		:width [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetHighlightLineWidth(width)

	def GetHighlightKeep(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetHighlightKeep()

	def SetHighlightKeep(self, keep:int) -> int:
		"""
		:keep [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetHighlightKeep(keep)

	def ExportImageItems(self, format:str, version:int, file:str, items:list[int], percentage:int, width:int, height:int, clrdepth:int, gray:int, dpiX:int, dpiY:int, compressionmode:int) -> int:
		"""
		:format [IN]: str
		:version [IN]: int
		:file [IN]: str
		:items [IN]: list[int]
		:percentage [IN]: int
		:width [IN]: int
		:height [IN]: int
		:clrdepth [IN]: int
		:gray [IN]: int
		:dpiX [IN]: int
		:dpiY [IN]: int
		:compressionmode [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.ExportImageItems(format, version, file, items, percentage, width, height, clrdepth, gray, dpiX, dpiY, compressionmode)
		return ret[0]

	def SaveLevelConfiguration(self, file:str) -> int:
		"""
		:file [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SaveLevelConfiguration(file)

	def LoadLevelConfiguration(self, file:str) -> int:
		"""
		:file [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.LoadLevelConfiguration(file)

	def GetLevels(self) -> tuple[int, tuple[int,...], tuple[int,...], tuple[int,...], tuple[int,...], tuple[int,...], tuple[int,...], tuple[int,...], tuple[str,...]]:
		"""
		:symarr [OUT]: tuple[int,...]
		:sgraarr [OUT]: tuple[int,...]
		:stxtarr [OUT]: tuple[int,...]
		:semtarr [OUT]: tuple[int,...]
		:graarr [OUT]: tuple[int,...]
		:txtarr [OUT]: tuple[int,...]
		:cxarr [OUT]: tuple[int,...]
		:names [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, symarr, sgraarr, stxtarr, semtarr, graarr, txtarr, cxarr, names = self._obj.GetLevels(dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy)
		symarr = symarr[1:] if type(symarr) == tuple and len(symarr) > 0 else tuple()
		sgraarr = sgraarr[1:] if type(sgraarr) == tuple and len(sgraarr) > 0 else tuple()
		stxtarr = stxtarr[1:] if type(stxtarr) == tuple and len(stxtarr) > 0 else tuple()
		semtarr = semtarr[1:] if type(semtarr) == tuple and len(semtarr) > 0 else tuple()
		graarr = graarr[1:] if type(graarr) == tuple and len(graarr) > 0 else tuple()
		txtarr = txtarr[1:] if type(txtarr) == tuple and len(txtarr) > 0 else tuple()
		cxarr = cxarr[1:] if type(cxarr) == tuple and len(cxarr) > 0 else tuple()
		names = names[1:] if type(names) == tuple and len(names) > 0 else tuple()
		return ret, symarr, sgraarr, stxtarr, semtarr, graarr, txtarr, cxarr, names

	def SetLevels(self, symarr:list[int], sgraarr:list[int], stxtarr:list[int], semtarr:list[int], graarr:list[int], txtarr:list[int], cxarr:list[int], names:list[str]) -> int:
		"""
		:symarr [IN]: list[int]
		:sgraarr [IN]: list[int]
		:stxtarr [IN]: list[int]
		:semtarr [IN]: list[int]
		:graarr [IN]: list[int]
		:txtarr [IN]: list[int]
		:cxarr [IN]: list[int]
		:names [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.SetLevels(symarr, sgraarr, stxtarr, semtarr, graarr, txtarr, cxarr, names)
		return ret[0]

	def SetLevel(self, lev:int, onoff:bool) -> int:
		"""
		:lev [IN]: int
		:onoff [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLevel(lev, onoff)

	def GetDisplayConnectionType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayConnectionType()

	def SetDisplayConnectionType(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayConnectionType(newval)

	def DeleteMultiuser(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteMultiuser(name)

	def ExportMultiuser(self, file:str, fileformat:int, name:str) -> int:
		"""
		:file [IN]: str
		:fileformat [IN]: int
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ExportMultiuser(file, fileformat, name)

	def ImportMultiuser(self, file:str, name:str) -> int:
		"""
		:file [IN]: str
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ImportMultiuser(file, name)

	def DisableSuffixSuppression(self) -> None:
		"""

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DisableSuffixSuppression()

	def EnableSuffixSuppression(self) -> None:
		"""

		Available since TLB-Versions: 8.50
		"""
		return self._obj.EnableSuffixSuppression()

	def SetDeviceNameSuffixSeparator(self, newsep:str) -> None:
		"""
		:newsep [IN]: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDeviceNameSuffixSeparator(newsep)

	def GetDeviceNameSuffixSeparator(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDeviceNameSuffixSeparator()

	def SetLocationSuffixSeparator(self, newsep:str) -> None:
		"""
		:newsep [IN]: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLocationSuffixSeparator(newsep)

	def GetLocationSuffixSeparator(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLocationSuffixSeparator()

	def SetAssignmentSuffixSeparator(self, newsep:str) -> None:
		"""
		:newsep [IN]: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAssignmentSuffixSeparator(newsep)

	def GetAssignmentSuffixSeparator(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAssignmentSuffixSeparator()

	def Create(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Create(name)

	def RecalcWireLength(self, bundlesequence_attribute:str, length_attribute:str) -> int:
		"""
		:bundlesequence_attribute [IN]: str
		:length_attribute [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.RecalcWireLength(bundlesequence_attribute, length_attribute)

	def Verify(self, mode:int, logfile:str="") -> int:
		"""
		:mode [IN]: int
		:logfile [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Verify(mode, logfile)

	def FindPanelPath(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.FindPanelPath()

	def SetDefaultWire(self, wiregroup:str, wirename:str) -> int:
		"""
		:wiregroup [IN]: str
		:wirename [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDefaultWire(wiregroup, wirename)

	def GetDefaultWire(self) -> tuple[int, str, str]:
		"""
		:wiregroup [OUT]: str
		:wirename [OUT]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetDefaultWire(dummy, dummy)

	def GetItemSheetIds(self, item:int) -> tuple[int, tuple[int,...]]:
		"""
		:item [IN]: int
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetItemSheetIds(item, dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def IsMultiuserProject(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsMultiuserProject()

	def ShowPartPreview(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ShowPartPreview(name)

	def CreateSlotObject(self) -> Slot:
		"""
		:Return: Slot

		Available since TLB-Versions: 8.50
		"""
		return Slot(self._obj.CreateSlotObject())

	def UpdateConfiguration(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateConfiguration()

	def UpdateComponent(self, cmpnam:str, withSymbol:bool=True) -> int:
		"""
		:cmpnam [IN]: str
		:withSymbol [IN]: bool Default value =True
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateComponent(cmpnam, withSymbol)

	def UpdateSymbol(self, symnam:str) -> int:
		"""
		:symnam [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateSymbol(symnam)

	def UpdateAllComponents(self, withSymbol:bool=True) -> int:
		"""
		:withSymbol [IN]: bool Default value =True
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateAllComponents(withSymbol)

	def UpdateAllSymbols(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateAllSymbols()

	def PurgeUnused(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PurgeUnused()

	def GetPurgeUnusedBeforeSave(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPurgeUnusedBeforeSave()

	def SetPurgeUnusedBeforeSave(self, purge:bool) -> int:
		"""
		:purge [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPurgeUnusedBeforeSave(purge)

	def GetReloadAttributesOnUpdate(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetReloadAttributesOnUpdate()

	def SetReloadAttributesOnUpdate(self, reload:bool) -> int:
		"""
		:reload [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetReloadAttributesOnUpdate(reload)

	def GetKeepSymbolTextVisibilityOnUpdate(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetKeepSymbolTextVisibilityOnUpdate()

	def SetKeepSymbolTextVisibilityOnUpdate(self, keep:bool) -> int:
		"""
		:keep [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetKeepSymbolTextVisibilityOnUpdate(keep)

	def GetKeepModelTextVisibilityOnUpdate(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetKeepModelTextVisibilityOnUpdate()

	def SetKeepModelTextVisibilityOnUpdate(self, keep:bool) -> int:
		"""
		:keep [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetKeepModelTextVisibilityOnUpdate(keep)

	def GetKeepSymbolTextParametersOnUpdate(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetKeepSymbolTextParametersOnUpdate()

	def SetKeepSymbolTextParametersOnUpdate(self, keep:bool) -> int:
		"""
		:keep [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetKeepSymbolTextParametersOnUpdate(keep)

	def GetKeepModelTextParametersOnUpdate(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetKeepModelTextParametersOnUpdate()

	def SetKeepModelTextParametersOnUpdate(self, keep:bool) -> int:
		"""
		:keep [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetKeepModelTextParametersOnUpdate(keep)

	def GetRestoreChangedPinNamesOnUpdate(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetRestoreChangedPinNamesOnUpdate()

	def SetRestoreChangedPinNamesOnUpdate(self, restore:bool) -> int:
		"""
		:restore [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetRestoreChangedPinNamesOnUpdate(restore)

	def GetKeepConnectorSymbolsOnUpdate(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetKeepConnectorSymbolsOnUpdate()

	def SetKeepConnectorSymbolsOnUpdate(self, keep:bool) -> int:
		"""
		:keep [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetKeepConnectorSymbolsOnUpdate(keep)

	def GetKeepActiveCounterpartOnUpdate(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetKeepActiveCounterpartOnUpdate()

	def SetKeepActiveCounterpartOnUpdate(self, keep:bool) -> int:
		"""
		:keep [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetKeepActiveCounterpartOnUpdate(keep)

	def GetKeepActiveFittingOnUpdate(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetKeepActiveFittingOnUpdate()

	def SetKeepActiveFittingOnUpdate(self, keep:bool) -> int:
		"""
		:keep [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetKeepActiveFittingOnUpdate(keep)

	def GetNewSheetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewSheetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewAllDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewAllDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewCableIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewCableIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewTerminalIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewTerminalIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewConnectorIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewConnectorIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewBlockIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewBlockIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewGraphIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewGraphIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewTextIds(self, txttyp:int=0, search_string:str="") -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:txttyp [IN]: int Default value =0
		:search_string [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewTextIds(dummy, txttyp, search_string)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewBundleIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewBundleIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewNetSegmentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewNetSegmentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewSignalIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewSignalIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewConnectionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewConnectionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetNewCoreIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewCoreIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetRedlinedGraphTextIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetRedlinedGraphTextIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetRedlinedGraphIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetRedlinedGraphIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def ConvertMultiByteToWideChar(self, code_page:int) -> int:
		"""
		:code_page [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ConvertMultiByteToWideChar(code_page)

	def GetDisplayDuctFillSize(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayDuctFillSize()

	def SetDisplayDuctFillSize(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayDuctFillSize(newval)

	def GetDisplayDuctDockingPoints(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayDuctDockingPoints()

	def SetDisplayDuctDockingPoints(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayDuctDockingPoints(newval)

	def GetDisplayIntExtRepresentation(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayIntExtRepresentation()

	def SetDisplayIntExtRepresentation(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayIntExtRepresentation(newval)

	def GetDisplayConnectPoints(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayConnectPoints()

	def SetDisplayConnectPoints(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayConnectPoints(newval)

	def GetDisplayUnconnectedNodes(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayUnconnectedNodes()

	def SetDisplayUnconnectedNodes(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayUnconnectedNodes(newval)

	def GetDisplayViewNumbers(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayViewNumbers()

	def SetDisplayViewNumbers(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayViewNumbers(newval)

	def GetDisplayRotatedTextAccStandard(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayRotatedTextAccStandard()

	def SetDisplayRotatedTextAccStandard(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayRotatedTextAccStandard(newval)

	def GetDisplayAltCompCode(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayAltCompCode()

	def SetDisplayAltCompCode(self, newval:str) -> str:
		"""
		:newval [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayAltCompCode(newval)

	def GetLastModifiedItems(self, _type:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:_type [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetLastModifiedItems(dummy, _type)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetLastAddedItems(self, _type:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:_type [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetLastAddedItems(dummy, _type)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def RemoveUndoInformation(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.RemoveUndoInformation()

	def CreateNetObject(self) -> Net:
		"""
		:Return: Net

		Available since TLB-Versions: 8.50
		"""
		return Net(self._obj.CreateNetObject())

	def GetNetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetActiveSheetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetActiveSheetId()

	def GetAnyAttributeIds(self, attnam:str) -> tuple[int, tuple[int,...]]:
		"""
		:attnam [IN]: str
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAnyAttributeIds(attnam, dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def DeleteAttributeDefinition(self, attnam:str) -> int:
		"""
		:attnam [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteAttributeDefinition(attnam)

	def UpdateCompleteProject(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateCompleteProject()

	def UpdateTextsInProject(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateTextsInProject()

	def UpdateAutoShtrefs(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateAutoShtrefs()

	def UpdateCores(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateCores()

	def UpdateConnectionTargets(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateConnectionTargets()

	def GetDisplayOptionsColoured(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayOptionsColoured()

	def SetDisplayOptionsColoured(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayOptionsColoured(newval)

	def GetGidOfId(self, id:int) -> str:
		"""
		:id [IN]: int
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGidOfId(id)

	def GetIdOfGid(self, gid:str) -> int:
		"""
		:gid [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetIdOfGid(gid)

	def SetNetSegmentLengthSplittingRule(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetNetSegmentLengthSplittingRule(newval)

	def SetNetSegmentAttributeSplittingRule(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetNetSegmentAttributeSplittingRule(newval)

	def CreateStructureNodeObject(self) -> StructureNode:
		"""
		:Return: StructureNode

		Available since TLB-Versions: 8.50
		"""
		return StructureNode(self._obj.CreateStructureNodeObject())

	def GetStructureNodeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetStructureNodeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def UpdateLanguageDatabase(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateLanguageDatabase()

	def SetChanged(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetChanged(newval)

	def GetActiveSheetTreeID(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetActiveSheetTreeID()

	def SetActiveSheetTreeID(self, treeid:int) -> int:
		"""
		:treeid [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetActiveSheetTreeID(treeid)

	def LoadStructureTemplate(self, structure_file:str) -> int:
		"""
		:structure_file [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.LoadStructureTemplate(structure_file)

	def CreateTreeObject(self) -> Tree:
		"""
		:Return: Tree

		Available since TLB-Versions: 8.50
		"""
		return Tree(self._obj.CreateTreeObject())

	def GetTreeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTreeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def UpdateMultiuser(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateMultiuser()

	def GetMergeUsingExactCoreConnectionOnImport(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetMergeUsingExactCoreConnectionOnImport()

	def SetMergeUsingExactCoreConnectionOnImport(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetMergeUsingExactCoreConnectionOnImport(newval)

	def PurgeUnplacedPinViews(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PurgeUnplacedPinViews()

	def SetPurgeUnplacedPinViewsBeforeSave(self, purge:bool) -> int:
		"""
		:purge [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPurgeUnplacedPinViewsBeforeSave(purge)

	def SetDynamicSymbolOriginInUpperLeft(self, bTopLeft:bool) -> int:
		"""
		:bTopLeft [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDynamicSymbolOriginInUpperLeft(bTopLeft)

	def SetFieldOriginInUpperLeft(self, bTopLeft:bool) -> int:
		"""
		:bTopLeft [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFieldOriginInUpperLeft(bTopLeft)

	def ResetAttributeHighWaterMark(self, attname:str) -> int:
		"""
		:attname [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ResetAttributeHighWaterMark(attname)

	def GetWireRange(self) -> tuple[int, int, int]:
		"""
		:_from [OUT]: int
		:to [OUT]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetWireRange(dummy, dummy)

	def SetWireRange(self, _from:int, to:int) -> int:
		"""
		:_from [IN]: int
		:to [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetWireRange(_from, to)

	def GetSymbolForConnectorsWithoutCompcode(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSymbolForConnectorsWithoutCompcode()

	def SetSymbolForConnectorsWithoutCompcode(self, new_sym:str) -> bool:
		"""
		:new_sym [IN]: str
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetSymbolForConnectorsWithoutCompcode(new_sym)

	def GetSymbolForBlockConnectorsWithoutCompcode(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSymbolForBlockConnectorsWithoutCompcode()

	def SetSymbolForBlockConnectorsWithoutCompcode(self, new_sym:str) -> bool:
		"""
		:new_sym [IN]: str
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetSymbolForBlockConnectorsWithoutCompcode(new_sym)

	def GetGapToPlaceSinglePins(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetGapToPlaceSinglePins()

	def SetGapToPlaceSinglePins(self, new_gap:float) -> float:
		"""
		:new_gap [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetGapToPlaceSinglePins(new_gap)

	def GetDetermineConnectorSymbol(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDetermineConnectorSymbol()

	def SetDetermineConnectorSymbol(self, determine:int) -> int:
		"""
		:determine [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDetermineConnectorSymbol(determine)

	def GetPinViewSymbolForDevicePins(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPinViewSymbolForDevicePins()

	def SetPinViewSymbolForDevicePins(self, new_sym:str) -> bool:
		"""
		:new_sym [IN]: str
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPinViewSymbolForDevicePins(new_sym)

	def GetPinViewSymbolForConnectorPins(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPinViewSymbolForConnectorPins()

	def SetPinViewSymbolForConnectorPins(self, new_sym:str) -> bool:
		"""
		:new_sym [IN]: str
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPinViewSymbolForConnectorPins(new_sym)

	def GetPinViewSymbolForBlockConnectorPins(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPinViewSymbolForBlockConnectorPins()

	def SetPinViewSymbolForBlockConnectorPins(self, new_sym:str) -> bool:
		"""
		:new_sym [IN]: str
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPinViewSymbolForBlockConnectorPins(new_sym)

	def GetDetermineConnectorViewSymbol(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDetermineConnectorViewSymbol()

	def SetDetermineConnectorViewSymbol(self, determine:int) -> int:
		"""
		:determine [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDetermineConnectorViewSymbol(determine)

	def RenameMultiuser(self, oldname:str, newname:str, newdesc:str="") -> int:
		"""
		:oldname [IN]: str
		:newname [IN]: str
		:newdesc [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.RenameMultiuser(oldname, newname, newdesc)

	def GetPanelGridSize(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPanelGridSize()

	def SetPanelGridSize(self, newsize:float) -> float:
		"""
		:newsize [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPanelGridSize(newsize)

	def GetPanelTrapSize(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPanelTrapSize()

	def SetPanelTrapSize(self, newsize:float) -> float:
		"""
		:newsize [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPanelTrapSize(newsize)

	def GetTypeName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTypeName()

	def ReloadSettings(self, filename:str) -> bool:
		"""
		:filename [IN]: str
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ReloadSettings(filename)

	def ExportTemplate(self, filename:str) -> bool:
		"""
		:filename [IN]: str
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ExportTemplate(filename)

	def SetFieldOutlineWidth(self, width:float) -> float:
		"""
		:width [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFieldOutlineWidth(width)

	def GetFieldOutlineWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFieldOutlineWidth()

	def SetFieldOutlineColour(self, newcol:int) -> int:
		"""
		:newcol [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFieldOutlineColour(newcol)

	def GetFieldOutlineColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFieldOutlineColour()

	def SetFieldOutlineStyle(self, newstyle:int) -> int:
		"""
		:newstyle [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFieldOutlineStyle(newstyle)

	def GetFieldOutlineStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFieldOutlineStyle()

	def GetFieldHatchPattern(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFieldHatchPattern()

	def SetFieldHatchPattern(self, newpat:int) -> int:
		"""
		:newpat [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFieldHatchPattern(newpat)

	def GetFieldHatchLineWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFieldHatchLineWidth()

	def SetFieldHatchLineWidth(self, newwid:float) -> float:
		"""
		:newwid [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFieldHatchLineWidth(newwid)

	def GetFieldHatchColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFieldHatchColour()

	def SetFieldHatchColour(self, newcol:int) -> int:
		"""
		:newcol [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFieldHatchColour(newcol)

	def GetFieldHatchLineDistance(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFieldHatchLineDistance()

	def SetFieldHatchLineDistance(self, newdist:float) -> float:
		"""
		:newdist [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFieldHatchLineDistance(newdist)

	def GetBlockTextFont(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockTextFont()

	def SetBlockTextFont(self, newfont:str) -> str:
		"""
		:newfont [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockTextFont(newfont)

	def GetBlockTextStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockTextStyle()

	def SetBlockTextStyle(self, newstyle:int) -> int:
		"""
		:newstyle [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockTextStyle(newstyle)

	def GetBlockTextSize(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockTextSize()

	def SetBlockTextSize(self, newsize:float) -> float:
		"""
		:newsize [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockTextSize(newsize)

	def GetBlockTextColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockTextColour()

	def SetBlockTextColour(self, newcol:int) -> int:
		"""
		:newcol [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockTextColour(newcol)

	def GetBlockTextRatio(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockTextRatio()

	def SetBlockTextRatio(self, newratio:int) -> int:
		"""
		:newratio [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockTextRatio(newratio)

	def GetBlockTextAlignment(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockTextAlignment()

	def SetBlockTextAlignment(self, newalign:int) -> int:
		"""
		:newalign [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockTextAlignment(newalign)

	def GetBlockReferenceType(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockReferenceType()

	def SetBlockReferenceType(self, newtype:int) -> int:
		"""
		:newtype [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockReferenceType(newtype)

	def GetBlockReferenceTextGap(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockReferenceTextGap()

	def SetBlockReferenceTextGap(self, newgap:float) -> float:
		"""
		:newgap [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockReferenceTextGap(newgap)

	def GetBlockReferenceTextLevel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockReferenceTextLevel()

	def SetBlockReferenceTextLevel(self, newlev:int) -> int:
		"""
		:newlev [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockReferenceTextLevel(newlev)

	def GetBlockReferenceTextRotate(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockReferenceTextRotate()

	def SetBlockReferenceTextRotate(self, rotate:int) -> int:
		"""
		:rotate [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockReferenceTextRotate(rotate)

	def GetBlockReferenceTextDirection(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockReferenceTextDirection()

	def SetBlockReferenceTextDirection(self, newdir:int) -> int:
		"""
		:newdir [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockReferenceTextDirection(newdir)

	def GetBlockCopyGraphicInSplit(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBlockCopyGraphicInSplit()

	def SetBlockCopyGraphicInSplit(self, copy:int) -> int:
		"""
		:copy [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetBlockCopyGraphicInSplit(copy)

	def GetImportUseItemDesignationSuffix(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetImportUseItemDesignationSuffix()

	def SetImportUseItemDesignationSuffix(self, use:int) -> int:
		"""
		:use [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetImportUseItemDesignationSuffix(use)

	def GetImportItemDesignationSuffix(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetImportItemDesignationSuffix()

	def SetImportItemDesignationSuffix(self, newsuffix:str) -> str:
		"""
		:newsuffix [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetImportItemDesignationSuffix(newsuffix)

	def GetImportMergeExistingDevices(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetImportMergeExistingDevices()

	def SetImportMergeExistingDevices(self, merge:int) -> int:
		"""
		:merge [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetImportMergeExistingDevices(merge)

	def GetImportMergeExistingAssemblies(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetImportMergeExistingAssemblies()

	def SetImportMergeExistingAssemblies(self, merge:int) -> int:
		"""
		:merge [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetImportMergeExistingAssemblies(merge)

	def GetImportMergeExistingTerminalStrips(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetImportMergeExistingTerminalStrips()

	def SetImportMergeExistingTerminalStrips(self, merge:int) -> int:
		"""
		:merge [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetImportMergeExistingTerminalStrips(merge)

	def GetImportMergeAttributes(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetImportMergeAttributes()

	def SetImportMergeAttributes(self, merge:int) -> int:
		"""
		:merge [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetImportMergeAttributes(merge)

	def GetImportMergeConnectLines(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetImportMergeConnectLines()

	def SetImportMergeConnectLines(self, merge:int) -> int:
		"""
		:merge [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetImportMergeConnectLines(merge)

	def GetCreateUniqueSheetNames(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCreateUniqueSheetNames()

	def SetCreateUniqueSheetNames(self, uniquenames:int) -> int:
		"""
		:uniquenames [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetCreateUniqueSheetNames(uniquenames)

	def GetExportWithCablesAndWires(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetExportWithCablesAndWires()

	def SetExportWithCablesAndWires(self, cablesandwires:int) -> int:
		"""
		:cablesandwires [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetExportWithCablesAndWires(cablesandwires)

	def GetExportWithCablesAndWiresOption(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetExportWithCablesAndWiresOption()

	def SetExportWithCablesAndWiresOption(self, option:int) -> int:
		"""
		:option [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetExportWithCablesAndWiresOption(option)

	def UpdateAllTerminalPlans(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.UpdateAllTerminalPlans()

	def GetSchematicTypeDescription(self, _type:int) -> str:
		"""
		:_type [IN]: int
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSchematicTypeDescription(_type)

	def JumpToID(self, jumpid:int) -> bool:
		"""
		:jumpid [IN]: int
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.JumpToID(jumpid)

	def ExportSymbolToDB(self, SymbolName:str, SymbolVersion:str, bOverwrite:int) -> int:
		"""
		:SymbolName [IN]: str
		:SymbolVersion [IN]: str
		:bOverwrite [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ExportSymbolToDB(SymbolName, SymbolVersion, bOverwrite)

	def ExportAllSymbolsToDB(self, bOverwrite:int) -> int:
		"""
		:bOverwrite [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ExportAllSymbolsToDB(bOverwrite)

	def ExportComponentToDB(self, CompName:str, CompVersion:str, bOverwrite:int) -> int:
		"""
		:CompName [IN]: str
		:CompVersion [IN]: str
		:bOverwrite [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ExportComponentToDB(CompName, CompVersion, bOverwrite)

	def ExportAllComponentsToDB(self, bOverwrite:int) -> int:
		"""
		:bOverwrite [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ExportAllComponentsToDB(bOverwrite)

	def ExportToDB(self, bOverwrite:int) -> int:
		"""
		:bOverwrite [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ExportToDB(bOverwrite)

	def GetNextWireNumber(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetNextWireNumber()

	def FreeWireNumber(self, number:int) -> int:
		"""
		:number [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.FreeWireNumber(number)

	def GetCursorPosition(self) -> tuple[int, tuple[int,...], tuple[int,...]]:
		"""
		:xpos [OUT]: tuple[int,...]
		:ypos [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, xpos, ypos = self._obj.GetCursorPosition(dummy, dummy)
		xpos = xpos[1:] if type(xpos) == tuple and len(xpos) > 0 else tuple()
		ypos = ypos[1:] if type(ypos) == tuple and len(ypos) > 0 else tuple()
		return ret, xpos, ypos

	def GetShortcutPosition(self) -> tuple[int, tuple[int,...], tuple[int,...]]:
		"""
		:xpos [OUT]: tuple[int,...]
		:ypos [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, xpos, ypos = self._obj.GetShortcutPosition(dummy, dummy)
		xpos = xpos[1:] if type(xpos) == tuple and len(xpos) > 0 else tuple()
		ypos = ypos[1:] if type(ypos) == tuple and len(ypos) > 0 else tuple()
		return ret, xpos, ypos

	def GetTreeSelectedDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTreeSelectedCableIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedCableIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTreeSelectedTerminalIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedTerminalIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTreeSelectedConnectorIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedConnectorIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTreeSelectedBlockIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedBlockIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTreeSelectedAllDeviceIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedAllDeviceIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTreeSelectedSymbolIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedSymbolIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTreeSelectedBundleIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedBundleIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTreeSelectedPinIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedPinIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTreeSelectedStructureNodeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedStructureNodeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetActiveTreeID(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetActiveTreeID()

	def GetTreeSelectedSheetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedSheetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetMergeSheetReferences(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetMergeSheetReferences()

	def SetMergeSheetReferences(self, bMerge:int) -> int:
		"""
		:bMerge [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetMergeSheetReferences(bMerge)

	def GetMergeAlphanumericReferences(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetMergeAlphanumericReferences()

	def SetMergeAlphanumericReferences(self, bMerge:int) -> int:
		"""
		:bMerge [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetMergeAlphanumericReferences(bMerge)

	def GetAltGridSize(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAltGridSize()

	def SetAltGridSize(self, newsize:float) -> float:
		"""
		:newsize [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAltGridSize(newsize)

	def GetPanelAltGridSize(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPanelAltGridSize()

	def SetPanelAltGridSize(self, newsize:float) -> float:
		"""
		:newsize [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPanelAltGridSize(newsize)

	def GetAddDeviceDesignationOfConnectionTarget(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAddDeviceDesignationOfConnectionTarget()

	def SetAddDeviceDesignationOfConnectionTarget(self, bMerge:int) -> int:
		"""
		:bMerge [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAddDeviceDesignationOfConnectionTarget(bMerge)

	def ExportModelToDB(self, CompName:str, CompVersion:str, bOverwrite:int) -> int:
		"""
		:CompName [IN]: str
		:CompVersion [IN]: str
		:bOverwrite [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ExportModelToDB(CompName, CompVersion, bOverwrite)

	def ExportAllModelsToDB(self, bOverwrite:int) -> int:
		"""
		:bOverwrite [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ExportAllModelsToDB(bOverwrite)

	def GetLastDeletedAttributeValues(self) -> tuple[int, tuple[int,...], tuple[str,...], tuple[str,...]]:
		"""
		:owner_ids [OUT]: tuple[int,...]
		:attribute_names [OUT]: tuple[str,...]
		:attribute_values [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, owner_ids, attribute_names, attribute_values = self._obj.GetLastDeletedAttributeValues(dummy, dummy, dummy)
		owner_ids = owner_ids[1:] if type(owner_ids) == tuple and len(owner_ids) > 0 else tuple()
		attribute_names = attribute_names[1:] if type(attribute_names) == tuple and len(attribute_names) > 0 else tuple()
		attribute_values = attribute_values[1:] if type(attribute_values) == tuple and len(attribute_values) > 0 else tuple()
		return ret, owner_ids, attribute_names, attribute_values

	def GetRGBValue(self, index:int) -> tuple[int, int, int, int]:
		"""
		:index [IN]: int
		:r [OUT]: int
		:g [OUT]: int
		:b [OUT]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetRGBValue(index, dummy, dummy, dummy)

	def SetRGBValue(self, index:int, r:int, g:int, b:int) -> int:
		"""
		:index [IN]: int
		:r [IN]: int
		:g [IN]: int
		:b [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetRGBValue(index, r, g, b)

	def GetSymbolTypeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSymbolTypeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def ExportCGM(self, file:str, shtids:list[int], options:int) -> int:
		"""
		:file [IN]: str
		:shtids [IN]: list[int]
		:options [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.ExportCGM(file, shtids, options)
		return ret[0]

	def ClearItemCollectors(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ClearItemCollectors()

	def SetTerminalPlanSettings(self, settings:dict[str,str]) -> bool:
		"""
		:settings [IN]: dict[str,str]
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		settings = _dict_to_variant(settings)
		ret = self._obj.SetTerminalPlanSettings(settings)
		return ret[0]

	def GetTerminalPlanSettings(self, settings:dict[str,str]=pythoncom.Empty) -> tuple[bool, dict[str,str]]:
		"""
		:settings [IN/OUT]: dict[str,str] Default value =pythoncom.Empty
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		settings = _dict_to_variant(settings)
		ret, settings = self._obj.GetTerminalPlanSettings(settings)
		settings = _variant_to_dict(settings)
		return ret, settings

	def CreateDimensionObject(self) -> Dimension:
		"""
		:Return: Dimension

		Available since TLB-Versions: 8.50
		"""
		return Dimension(self._obj.CreateDimensionObject())

	def SetDefaultJumper(self, jumpergroup:str, jumpername:str) -> int:
		"""
		:jumpergroup [IN]: str
		:jumpername [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDefaultJumper(jumpergroup, jumpername)

	def GetDefaultJumper(self) -> tuple[int, str, str]:
		"""
		:jumpergroup [OUT]: str
		:jumpername [OUT]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetDefaultJumper(dummy, dummy)

	def IsFileReadonly(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsFileReadonly()

	def GetConnectorPinTerminalParameterOverwriteModelPin(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConnectorPinTerminalParameterOverwriteModelPin()

	def SetConnectorPinTerminalParameterOverwriteModelPin(self, bValue:int) -> int:
		"""
		:bValue [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetConnectorPinTerminalParameterOverwriteModelPin(bValue)

	def GetPortNameSeparator(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPortNameSeparator()

	def SetPortNameSeparator(self, newsep:str) -> str:
		"""
		:newsep [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPortNameSeparator(newsep)

	def GetImportMergeOptions(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetImportMergeOptions()

	def SetImportMergeOptions(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetImportMergeOptions(newval)

	def SetIEC61346Setting(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetIEC61346Setting(newval)

	def GetIEC61346Setting(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetIEC61346Setting()

	def SetUsePinAttributesOnAssign(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetUsePinAttributesOnAssign(newval)

	def GetUsePinAttributesOnAssign(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetUsePinAttributesOnAssign()

	def SetUsePinAttributesOnImport(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetUsePinAttributesOnImport(newval)

	def GetUsePinAttributesOnImport(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetUsePinAttributesOnImport()

	def SetDeletePinAttributesOnUnplace(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDeletePinAttributesOnUnplace(newval)

	def GetDeletePinAttributesOnUnplace(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDeletePinAttributesOnUnplace()

	def SetDefaultHoseTube(self, HoseTube:str) -> int:
		"""
		:HoseTube [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDefaultHoseTube(HoseTube)

	def GetDefaultHoseTube(self) -> tuple[int, str]:
		"""
		:HoseTube [OUT]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetDefaultHoseTube(dummy)

	def GetOutdatedAllComponentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetOutdatedAllComponentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetOutdatedComponentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetOutdatedComponentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetOutdatedCableTypeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetOutdatedCableTypeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetOutdatedSymbolTypeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetOutdatedSymbolTypeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetViewSymbolForTerminalStrips(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetViewSymbolForTerminalStrips()

	def SetViewSymbolForTerminalStrips(self, new_sym:str) -> bool:
		"""
		:new_sym [IN]: str
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetViewSymbolForTerminalStrips(new_sym)

	def GetMultiuserPath(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetMultiuserPath()

	def GetDisplayMILStandard(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayMILStandard()

	def SetDisplayMILStandard(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayMILStandard(newval)

	def SetMILGraphicLineWidth(self, width:float) -> float:
		"""
		:width [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetMILGraphicLineWidth(width)

	def GetMILGraphicLineWidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetMILGraphicLineWidth()

	def SetMILGraphicLineColour(self, newcol:int) -> int:
		"""
		:newcol [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetMILGraphicLineColour(newcol)

	def GetMILGraphicLineColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetMILGraphicLineColour()

	def SetMILGraphicLineStyle(self, newstyle:int) -> int:
		"""
		:newstyle [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetMILGraphicLineStyle(newstyle)

	def GetMILGraphicLineStyle(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetMILGraphicLineStyle()

	def GetKeepActiveConnectorPinTerminalOnUpdate(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetKeepActiveConnectorPinTerminalOnUpdate()

	def SetKeepActiveConnectorPinTerminalOnUpdate(self, keep:bool) -> int:
		"""
		:keep [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetKeepActiveConnectorPinTerminalOnUpdate(keep)

	def GetUseBlockDesignation(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetUseBlockDesignation()

	def SetUseBlockDesignation(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetUseBlockDesignation(newval)

	def SetConnectionInclinationAngle(self, angle:float) -> float:
		"""
		:angle [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetConnectionInclinationAngle(angle)

	def GetConnectionInclinationAngle(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConnectionInclinationAngle()

	def SetConnectionInclinationDistance(self, destination:float) -> float:
		"""
		:destination [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetConnectionInclinationDistance(destination)

	def GetConnectionInclinationDistance(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConnectionInclinationDistance()

	def SetConnectionMode(self, mode:int) -> int:
		"""
		:mode [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetConnectionMode(mode)

	def GetConnectionMode(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConnectionMode()

	def GetHoseIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetHoseIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTubeIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTubeIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetProjectProperty(self, what:str) -> typing.Union[dict[str,str],str]:
		"""
		:what [IN]: str
		:Return: typing.Union[dict[str,str],str]

		Available since TLB-Versions: 8.50
		"""
		ret = self._obj.GetProjectProperty(what)
		if type(ret) is CDispatch:
			ret = _variant_to_dict(ret)
		return ret

	def SetDeleteSignalOnDelCline(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDeleteSignalOnDelCline(newval)

	def GetDeleteSignalOnDelCline(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDeleteSignalOnDelCline()

	def SetUnconnectCoresOnDelCline(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetUnconnectCoresOnDelCline(newval)

	def GetUnconnectCoresOnDelCline(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetUnconnectCoresOnDelCline()

	def SetDeleteCoresOnDelCline(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDeleteCoresOnDelCline(newval)

	def GetDeleteCoresOnDelCline(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDeleteCoresOnDelCline()

	def CreateGroupObject(self) -> Group:
		"""
		:Return: Group

		Available since TLB-Versions: 8.50
		"""
		return Group(self._obj.CreateGroupObject())

	def GetGroupIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetGroupIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAvailableLanguages(self) -> tuple[int, tuple[str,...]]:
		"""
		:languages [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, languages = self._obj.GetAvailableLanguages(dummy)
		languages = languages[1:] if type(languages) == tuple and len(languages) > 0 else tuple()
		return ret, languages

	def GetDisplayFormboardUnconnectedCores(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayFormboardUnconnectedCores()

	def SetDisplayFormboardUnconnectedCores(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayFormboardUnconnectedCores(newval)

	def GetDisplayAppendFormboardNameToDeviceName(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayAppendFormboardNameToDeviceName()

	def SetDisplayAppendFormboardNameToDeviceName(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayAppendFormboardNameToDeviceName(newval)

	def GetDisplayFormboardTableSubsidiaryLines(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayFormboardTableSubsidiaryLines()

	def SetDisplayFormboardTableSubsidiaryLines(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayFormboardTableSubsidiaryLines(newval)

	def GetDisplayFormboardMarkDifferenLength(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayFormboardMarkDifferenLength()

	def SetDisplayFormboardMarkDifferenLength(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayFormboardMarkDifferenLength(newval)

	def GetDisplayFormboardEffectiveDirection(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayFormboardEffectiveDirection()

	def SetDisplayFormboardEffectiveDirection(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayFormboardEffectiveDirection(newval)

	def GetDisplayFormboardNodes(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetDisplayFormboardNodes()

	def SetDisplayFormboardNodes(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDisplayFormboardNodes(newval)

	def GetTableSymbol(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTableSymbol()

	def SetTableSymbol(self, newval:str) -> str:
		"""
		:newval [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetTableSymbol(newval)

	def GetFormboardAutoplaceTableSymbol(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFormboardAutoplaceTableSymbol()

	def SetFormboardAutoplaceTableSymbol(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFormboardAutoplaceTableSymbol(newval)

	def GetFormboardAutorotateConnectorSymbols(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFormboardAutorotateConnectorSymbols()

	def SetFormboardAutorotateConnectorSymbols(self, newval:bool) -> bool:
		"""
		:newval [IN]: bool
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFormboardAutorotateConnectorSymbols(newval)

	def GetFormboardBranchAngleStep(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFormboardBranchAngleStep()

	def SetFormboardBranchAngleStep(self, newval:int) -> int:
		"""
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetFormboardBranchAngleStep(newval)

	def GetSettingValue(self, name:str) -> typing.Union[str,int]:
		"""
		:name [IN]: str
		:Return: typing.Union[str,int]

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSettingValue(name)

	def SetSettingValue(self, name:str, value:typing.Union[str,int]) -> typing.Union[str,int]:
		"""
		:name [IN]: str
		:value [IN]: typing.Union[str,int]
		:Return: typing.Union[str,int]

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetSettingValue(name, value)

	def GetLevelName(self, level:int) -> str:
		"""
		:level [IN]: int
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLevelName(level)

	def GetLevelIndex(self, value:str) -> int:
		"""
		:value [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLevelIndex(value)

	def GetNewFieldIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetNewFieldIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetCadstarCrossProbing(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetCadstarCrossProbing()

	def GetLastDeletedItems(self, _type:int) -> tuple[int, tuple[int,...]]:
		"""
		:items [OUT]: tuple[int,...]
		:_type [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, items = self._obj.GetLastDeletedItems(dummy, _type)
		items = items[1:] if type(items) == tuple and len(items) > 0 else tuple()
		return ret, items

	def GetHyperlinkTextIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetHyperlinkTextIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAttributeNotInheritable(self, attnam:str) -> int:
		"""
		:attnam [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetAttributeNotInheritable(attnam)

	def SetAttributeNotInheritable(self, attnam:str, newval:int) -> int:
		"""
		:attnam [IN]: str
		:newval [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetAttributeNotInheritable(attnam, newval)

	def GetTerminalPlanSheetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTerminalPlanSheetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def FinalizeTransaction(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.FinalizeTransaction()

	def GetNextWireNumberFormatted(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetNextWireNumberFormatted()

	def GetAllOptionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetAllOptionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetOptionAliases(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetOptionAliases(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetOptionTerms(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetOptionTerms(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetOptionTermDescription(self, alias:str) -> str:
		"""
		:alias [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetOptionTermDescription(alias)

	def AddOptionAlias(self, name:str, description:str) -> int:
		"""
		:name [IN]: str
		:description [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AddOptionAlias(name, description)

	def DeleteOptionAlias(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.DeleteOptionAlias(name)

	def GetTreeSelectedExternalDocumentIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedExternalDocumentIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetOuterDiameter(self) -> tuple[float, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetOuterDiameter(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def SetExclusiveMode(self, mode:int) -> int:
		"""
		:mode [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetExclusiveMode(mode)

	def GetExclusiveMode(self, name:str) -> tuple[int, str]:
		"""
		:name [IN]: str
		:user [OUT]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetExclusiveMode(name, dummy)

	def ImportRuplan(self, parameters:list[str]) -> int:
		"""
		:parameters [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.ImportRuplan(parameters)

	def UpdateSubCircuit(self, cmpnam:str) -> int:
		"""
		:cmpnam [IN]: str
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.UpdateSubCircuit(cmpnam)

	def UpdateAllSubCircuits(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.UpdateAllSubCircuits()

	def UpdatePart(self, filename:str) -> int:
		"""
		:filename [IN]: str
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.UpdatePart(filename)

	def UpdateAllParts(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.UpdateAllParts()

	def StoreVariantVisibility(self, filename:str) -> int:
		"""
		:filename [IN]: str
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.StoreVariantVisibility(filename)

	def RestoreVariantVisibility(self, filename:str) -> int:
		"""
		:filename [IN]: str
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.RestoreVariantVisibility(filename)

	def CreateInlineConnectorsEx(self, flags:int, fromPinIDs:list[int], toPinIDs:list[int], viewNumbers:list[int], fBSheetIDs:list[int], compName:str, compVersion:str) -> tuple[int, tuple[int,...], tuple[int,...], tuple[tuple[int,int,int,int],...]]:
		"""
		:newCoreIDs [OUT]: tuple[int,...]
		:newDeviceIDs [OUT]: tuple[int,...]
		:flags [IN]: int
		:fromPinIDs [IN]: list[int]
		:toPinIDs [IN]: list[int]
		:viewNumbers [IN]: list[int]
		:fBSheetIDs [IN]: list[int]
		:compName [IN]: str
		:compVersion [IN]: str
		:newSymbolIDs [OUT]: tuple[tuple[int,int,int,int],...]
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		dummy=0
		ret, newCoreIDs, newDeviceIDs, newSymbolIDs = self._obj.CreateInlineConnectorsEx(dummy, dummy, flags, fromPinIDs, toPinIDs, viewNumbers, fBSheetIDs, compName, compVersion, dummy)
		newCoreIDs = newCoreIDs[1:] if type(newCoreIDs) == tuple and len(newCoreIDs) > 0 else tuple()
		newDeviceIDs = newDeviceIDs[1:] if type(newDeviceIDs) == tuple and len(newDeviceIDs) > 0 else tuple()
		newSymbolIDs = newSymbolIDs[1:] if type(newSymbolIDs) == tuple and len(newSymbolIDs) > 0 else tuple()
		return ret, newCoreIDs, newDeviceIDs, newSymbolIDs

	def GetCurrentUserName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 9.01, 8.52
		"""
		return self._obj.GetCurrentUserName()

	def GetTreeSelectedSheetIdsByFolder(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedSheetIdsByFolder(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTreeSelectedExternalDocumentIdsByFolder(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedExternalDocumentIdsByFolder(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTreeSelectedAllDeviceIdsByFolder(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedAllDeviceIdsByFolder(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateFunctionalUnitObject(self) -> FunctionalUnit:
		"""
		:Return: FunctionalUnit

		Available since TLB-Versions: 9.10
		"""
		return FunctionalUnit(self._obj.CreateFunctionalUnitObject())

	def CreateFunctionalPortObject(self) -> FunctionalPort:
		"""
		:Return: FunctionalPort

		Available since TLB-Versions: 9.10
		"""
		return FunctionalPort(self._obj.CreateFunctionalPortObject())

	def GetFunctionalUnitIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		dummy=0
		ret, ids = self._obj.GetFunctionalUnitIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetGetterOptionHandlingMode(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.GetGetterOptionHandlingMode()

	def SetGetterOptionHandlingMode(self, mode:int) -> int:
		"""
		:mode [IN]: int
		:Return: int

		Available since TLB-Versions: 9.10
		"""
		return self._obj.SetGetterOptionHandlingMode(mode)

	def ActivateOptionAlias(self, alias:str) -> int:
		"""
		:alias [IN]: str
		:Return: int

		Available since TLB-Versions: 9.13
		"""
		return self._obj.ActivateOptionAlias(alias)

	def CreateConnectLineObject(self) -> ConnectLine:
		"""
		:Return: ConnectLine

		Available since TLB-Versions: 9.22
		"""
		return ConnectLine(self._obj.CreateConnectLineObject())

	def GetAllSheetIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 9.30
		"""
		dummy=0
		ret, ids = self._obj.GetAllSheetIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def SetConnectionTargetFormat(self, txttyp:int, flags:int, entire_prefix:str, entire_suffix:str, count:int, prefix:list[str], name:list[str], funct:list[int]) -> int:
		"""
		:txttyp [IN]: int
		:flags [IN]: int
		:entire_prefix [IN]: str
		:entire_suffix [IN]: str
		:count [IN]: int
		:prefix [IN]: list[str]
		:name [IN]: list[str]
		:funct [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetConnectionTargetFormat(txttyp, flags, entire_prefix, entire_suffix, count, prefix, name, funct)

	def GetConnectionTargetFormat(self, txttyp:int) -> tuple[int, int, str, str, int, tuple[str,...], tuple[str,...], tuple[int,...]]:
		"""
		:txttyp [IN]: int
		:flags [OUT]: int
		:entire_prefix [OUT]: str
		:entire_suffix [OUT]: str
		:count [OUT]: int
		:prefix [OUT]: tuple[str,...]
		:name [OUT]: tuple[str,...]
		:funct [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, flags, entire_prefix, entire_suffix, count, prefix, name, funct = self._obj.GetConnectionTargetFormat(txttyp, dummy, dummy, dummy, dummy, dummy, dummy, dummy)
		prefix = prefix[1:] if type(prefix) == tuple and len(prefix) > 0 else tuple()
		name = name[1:] if type(name) == tuple and len(name) > 0 else tuple()
		funct = funct[1:] if type(funct) == tuple and len(funct) > 0 else tuple()
		return ret, flags, entire_prefix, entire_suffix, count, prefix, name, funct

	def SetUnlockPassword(self, oldval:str, newval:str) -> int:
		"""
		:oldval [IN]: str
		:newval [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetUnlockPassword(oldval, newval)

	def SetConnectorSymbolFormat(self, texttypes:list[int], dispflags:list[int]) -> int:
		"""
		:texttypes [IN]: list[int]
		:dispflags [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.SetConnectorSymbolFormat(texttypes, dispflags)

	def GetConnectorSymbolFormat(self) -> tuple[int, tuple[int,...], tuple[int,...]]:
		"""
		:texttypes [OUT]: tuple[int,...]
		:dispflags [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, texttypes, dispflags = self._obj.GetConnectorSymbolFormat(dummy, dummy)
		texttypes = texttypes[1:] if type(texttypes) == tuple and len(texttypes) > 0 else tuple()
		dispflags = dispflags[1:] if type(dispflags) == tuple and len(dispflags) > 0 else tuple()
		return ret, texttypes, dispflags

	def GetHarnessIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, ids = self._obj.GetHarnessIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateSignalClassObject(self) -> SignalClass:
		"""
		:Return: SignalClass

		Available since TLB-Versions: 10.00
		"""
		return SignalClass(self._obj.CreateSignalClassObject())

	def GetSignalClassIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		dummy=0
		ret, ids = self._obj.GetSignalClassIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def StoreOptionVisibility(self, filename:str) -> int:
		"""
		:filename [IN]: str
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.StoreOptionVisibility(filename)

	def RestoreOptionVisibility(self, filename:str) -> int:
		"""
		:filename [IN]: str
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.RestoreOptionVisibility(filename)

	def GetOptionLockID(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.GetOptionLockID()

	def LoadOptionStructure(self, filename:str) -> int:
		"""
		:filename [IN]: str
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.LoadOptionStructure(filename)

	def SaveOptionStructure(self, filename:str) -> int:
		"""
		:filename [IN]: str
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.SaveOptionStructure(filename)

	def SaveSheetsAsSingleUser(self, name:str, shtids:list[int], compressed:bool=True, completeName:str="", completeCompressed:bool=True) -> int:
		"""
		:name [IN]: str
		:shtids [IN]: list[int]
		:compressed [IN]: bool Default value =True
		:completeName [IN]: str Default value =""
		:completeCompressed [IN]: bool Default value =True
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.SaveSheetsAsSingleUser(name, shtids, compressed, completeName, completeCompressed)

	def GetOptionLockIDs(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		dummy=0
		ret, ids = self._obj.GetOptionLockIDs(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def LoadSignalStructure(self, filename:str) -> int:
		"""
		:filename [IN]: str
		:Return: int

		Available since TLB-Versions: 10.20
		"""
		return self._obj.LoadSignalStructure(filename)

	def GetSignalStructureNodeId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.20
		"""
		return self._obj.GetSignalStructureNodeId()

	def RunUnitTests(self, tests:list[str]) -> tuple[int, int, int, int, tuple[str,...], tuple[str,...]]:
		"""
		:tests [IN]: list[str]
		:fixtures [OUT]: int
		:testcases [OUT]: int
		:succeeded [OUT]: int
		:failed [OUT]: tuple[str,...]
		:inconclusive [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 10.20
		"""
		dummy=0
		ret, fixtures, testcases, succeeded, failed, inconclusive = self._obj.RunUnitTests(tests, dummy, dummy, dummy, dummy, dummy)
		failed = failed[1:] if type(failed) == tuple and len(failed) > 0 else tuple()
		inconclusive = inconclusive[1:] if type(inconclusive) == tuple and len(inconclusive) > 0 else tuple()
		return ret, fixtures, testcases, succeeded, failed, inconclusive

	def LockVariantStructure(self, password:str) -> int:
		"""
		:password [IN]: str
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		return self._obj.LockVariantStructure(password)

	def UnlockVariantStructure(self, password:str) -> int:
		"""
		:password [IN]: str
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		return self._obj.UnlockVariantStructure(password)

	def SetUnlockVariantStructurePassword(self, oldval:str, newval:str) -> int:
		"""
		:oldval [IN]: str
		:newval [IN]: str
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		return self._obj.SetUnlockVariantStructurePassword(oldval, newval)

	def GetParentSheetIds(self, flags:int) -> tuple[int, tuple[int,...]]:
		"""
		:flags [IN]: int
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		dummy=0
		ret, ids = self._obj.GetParentSheetIds(flags, dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAllParentSheetIds(self, flags:int) -> tuple[int, tuple[int,...]]:
		"""
		:flags [IN]: int
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		dummy=0
		ret, ids = self._obj.GetAllParentSheetIds(flags, dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def ImportForeignProject(self, parameters:list[str]) -> int:
		"""
		:parameters [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 10.30
		"""
		return self._obj.ImportForeignProject(parameters)

	def PlacePartInteractively(self, name:str, version:str) -> tuple[int, float, float, float]:
		"""
		:name [IN]: str
		:version [IN]: str
		:x [OUT]: float
		:y [OUT]: float
		:rot [OUT]: float
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		dummy=0
		return self._obj.PlacePartInteractively(name, version, dummy, dummy, dummy)

	def ImportDrawingEx(self, name:str, unique:int, flags:int, posx:float=-950309, posy:float=-950309) -> int:
		"""
		:name [IN]: str
		:unique [IN]: int
		:flags [IN]: int
		:posx [IN]: float Default value =-950309
		:posy [IN]: float Default value =-950309
		:Return: int

		Available since TLB-Versions: 11.00, 10.46
		"""
		return self._obj.ImportDrawingEx(name, unique, flags, posx, posy)

	def GetLineWidthEx(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 11.00
		"""
		return self._obj.GetLineWidthEx()

	def PlacePartInteractivelyEx(self, name:str, version:str, flags:int) -> tuple[int, float, float, float]:
		"""
		:name [IN]: str
		:version [IN]: str
		:flags [IN]: int
		:x [OUT]: float
		:y [OUT]: float
		:rot [OUT]: float
		:Return: int

		Available since TLB-Versions: 11.01
		"""
		dummy=0
		return self._obj.PlacePartInteractivelyEx(name, version, flags, dummy, dummy, dummy)

	def GetDisplayOptionsAll(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 11.21, 14.00
		"""
		return self._obj.GetDisplayOptionsAll()

	def SetDisplayOptionsAll(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 11.21, 14.00
		"""
		return self._obj.SetDisplayOptionsAll(newval)

	def GetDisplayOptionsNone(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 11.21, 14.00
		"""
		return self._obj.GetDisplayOptionsNone()

	def SetDisplayOptionsNone(self, newval:bool) -> int:
		"""
		:newval [IN]: bool
		:Return: int

		Available since TLB-Versions: 11.21, 14.00
		"""
		return self._obj.SetDisplayOptionsNone(newval)

	def HighlightAttribute(self, attnam:str, attvalue:str, colour:int, width:float) -> int:
		"""
		:attnam [IN]: str
		:attvalue [IN]: str
		:colour [IN]: int
		:width [IN]: float
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		return self._obj.HighlightAttribute(attnam, attvalue, colour, width)

	def ResetHighlightAttribute(self, attnam:str, attvalue:str) -> int:
		"""
		:attnam [IN]: str
		:attvalue [IN]: str
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		return self._obj.ResetHighlightAttribute(attnam, attvalue)

	def GetUnplacedGroupIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		dummy=0
		ret, ids = self._obj.GetUnplacedGroupIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def ExportXVL(self, file:str, ids:list[int]=pythoncom.Empty) -> int:
		"""
		:file [IN]: str
		:ids [IN]: list[int] Default value =pythoncom.Empty
		:Return: int

		Available since TLB-Versions: 11.80
		"""
		return self._obj.ExportXVL(file, ids)

	def GetResultText(self, index:int) -> tuple[int, tuple[str,...]]:
		"""
		:index [IN]: int
		:lst [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 11.80
		"""
		dummy=0
		ret, lst = self._obj.GetResultText(index, dummy)
		lst = lst[1:] if type(lst) == tuple and len(lst) > 0 else tuple()
		return ret, lst

	def GetSelectedDimensionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 14.01
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedDimensionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def LoadOptionStructureEx(self, filename:str, flags:int) -> int:
		"""
		:filename [IN]: str
		:flags [IN]: int
		:Return: int

		Available since TLB-Versions: 14.12
		"""
		return self._obj.LoadOptionStructureEx(filename, flags)

	def ExportSVGBySheet(self, file:str, shtIds:list[int]) -> int:
		"""
		:file [IN]: str
		:shtIds [IN]: list[int]
		:Return: int

		Available since TLB-Versions: 14.70
		"""
		ret = self._obj.ExportSVGBySheet(file, shtIds)
		return ret[0]

	def ExportSVGByArea(self, file:str, shtId:int, xMin:float, yMin:float, xMax:float, yMax:float, originX:float, originY:float, selectionMode:int) -> int:
		"""
		:file [IN]: str
		:shtId [IN]: int
		:xMin [IN]: float
		:yMin [IN]: float
		:xMax [IN]: float
		:yMax [IN]: float
		:originX [IN]: float
		:originY [IN]: float
		:selectionMode [IN]: int
		:Return: int

		Available since TLB-Versions: 14.70
		"""
		return self._obj.ExportSVGByArea(file, shtId, xMin, yMin, xMax, yMax, originX, originY, selectionMode)

	def ExportSVGBySheetEx(self, file:str, options:int) -> tuple[int, list[int]]:
		"""
		:file [IN]: str
		:shtIds [OUT]: list[int]
		:options [IN]: int
		:Return: int

		Available since TLB-Versions: 15.01
		"""
		dummy=0
		ret, shtIds = self._obj.ExportSVGBySheetEx(file, dummy, options)
		shtIds = shtIds[1:] if type(shtIds) == list and len(shtIds) > 0 else []
		return ret, shtIds

	def ExportPDFEx(self, file:str, shtids:list[int], options:int, itemListType:int, items:list[int], alternativeColour:int, imageBrightness:int, password:str="") -> int:
		"""
		:file [IN]: str
		:shtids [IN]: list[int]
		:options [IN]: int
		:itemListType [IN]: int
		:items [IN]: list[int]
		:alternativeColour [IN]: int
		:imageBrightness [IN]: int
		:password [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 16.00
		"""
		ret = self._obj.ExportPDFEx(file, shtids, options, itemListType, items, alternativeColour, imageBrightness, password)
		return ret[0]

	def SetOptionExpressions(self, itemarray:list[int], expressions:list[str]) -> int:
		"""
		:itemarray [IN]: list[int]
		:expressions [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 16.70
		"""
		return self._obj.SetOptionExpressions(itemarray, expressions)

	def GetBomPartList(self, consumer:str, outputFormatVersion:str, flags:int, keyAttribut:str, quantityAttribut:str, lengthAttribut:str, additionalAttributes:list[str]) -> tuple[int, tuple[tuple[typing.Union[str,int],...],...]]:
		"""
		:consumer [IN]: str
		:outputFormatVersion [IN]: str
		:flags [IN]: int
		:keyAttribut [IN]: str
		:quantityAttribut [IN]: str
		:lengthAttribut [IN]: str
		:additionalAttributes [IN]: list[str]
		:result [OUT]: tuple[tuple[typing.Union[str,int],...],...]
		:Return: int

		Available since TLB-Versions: 17.01, 16.13
		"""
		dummy=0
		return self._obj.GetBomPartList(consumer, outputFormatVersion, flags, keyAttribut, quantityAttribut, lengthAttribut, additionalAttributes, dummy)

	def GetBooleanState(self, expression:str) -> int:
		"""
		:expression [IN]: str
		:Return: int

		Available since TLB-Versions: 17.01, 16.13
		"""
		return self._obj.GetBooleanState(expression)

	def SaveProjectWithoutVariants(self, name:str, compressed:bool=True) -> int:
		"""
		:name [IN]: str
		:compressed [IN]: bool Default value =True
		:Return: int

		Available since TLB-Versions: 17.13
		"""
		return self._obj.SaveProjectWithoutVariants(name, compressed)

	def CreateAttributeDefinitionObject(self) -> AttributeDefinition:
		"""
		:Return: AttributeDefinition

		Available since TLB-Versions: 17.13, 16.19, 15.31
		"""
		return AttributeDefinition(self._obj.CreateAttributeDefinitionObject())

	def GetAttributeDefinitionIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 17.13, 16.19, 15.31
		"""
		dummy=0
		ret, ids = self._obj.GetAttributeDefinitionIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetGeneratedWireNameFormatEx(self) -> tuple[int, tuple[str,...], tuple[int,...], tuple[str,...]]:
		"""
		:attPrefix [OUT]: tuple[str,...]
		:attType [OUT]: tuple[int,...]
		:attName [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 17.80
		"""
		dummy=0
		ret, attPrefix, attType, attName = self._obj.GetGeneratedWireNameFormatEx(dummy, dummy, dummy)
		attPrefix = attPrefix[1:] if type(attPrefix) == tuple and len(attPrefix) > 0 else tuple()
		attType = attType[1:] if type(attType) == tuple and len(attType) > 0 else tuple()
		attName = attName[1:] if type(attName) == tuple and len(attName) > 0 else tuple()
		return ret, attPrefix, attType, attName

	def SetGeneratedWireNameFormatEx(self, attPrefix:list[str], attType:list[int], attName:list[str]) -> int:
		"""
		:attPrefix [IN]: list[str]
		:attType [IN]: list[int]
		:attName [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 17.80
		"""
		return self._obj.SetGeneratedWireNameFormatEx(attPrefix, attType, attName)

	def GetCavityPartIds(self, _type:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:_type [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 17.80
		"""
		dummy=0
		ret, ids = self._obj.GetCavityPartIds(dummy, _type)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateCavityPartObject(self) -> CavityPart:
		"""
		:Return: CavityPart

		Available since TLB-Versions: 17.80
		"""
		return CavityPart(self._obj.CreateCavityPartObject())

	def SaveTableConfiguration(self, file:str, table:int) -> int:
		"""
		:file [IN]: str
		:table [IN]: int
		:Return: int

		Available since TLB-Versions: 18.80
		"""
		return self._obj.SaveTableConfiguration(file, table)

	def LoadTableConfiguration(self, file:str, table:int) -> int:
		"""
		:file [IN]: str
		:table [IN]: int
		:Return: int

		Available since TLB-Versions: 18.80
		"""
		return self._obj.LoadTableConfiguration(file, table)

	def RemoveAccessControlInformation(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.RemoveAccessControlInformation()

	def IsVariantStructurePasswordProtected(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 19.00
		"""
		return self._obj.IsVariantStructurePasswordProtected()

	def GetClipboardIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 19.00, 18.30
		"""
		dummy=0
		ret, ids = self._obj.GetClipboardIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateClipboardObject(self) -> Clipboard:
		"""
		:Return: Clipboard

		Available since TLB-Versions: 19.00, 18.30
		"""
		return Clipboard(self._obj.CreateClipboardObject())

	def GetGUIDOfId(self, id:int) -> str:
		"""
		:id [IN]: int
		:Return: str

		Available since TLB-Versions: 20.00
		"""
		return self._obj.GetGUIDOfId(id)

	def GetIdOfGUID(self, guid:str) -> int:
		"""
		:guid [IN]: str
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		return self._obj.GetIdOfGUID(guid)

	def SaveAsGranularDesignProject(self, folder:str, options:int) -> int:
		"""
		:folder [IN]: str
		:options [IN]: int
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		return self._obj.SaveAsGranularDesignProject(folder, options)

	def OpenGranularDesignProject(self, folder:str, options:int) -> int:
		"""
		:folder [IN]: str
		:options [IN]: int
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		return self._obj.OpenGranularDesignProject(folder, options)

	def ImportDrawingForProjectGeneration(self, name:str, unique:int, flags:int, substitutes:list[tuple[str,str]], allowedTexttypes:list[str]=pythoncom.Empty, allowedAttributenames:list[str]=pythoncom.Empty, posx:float=-950309, posy:float=-950309) -> tuple[int, tuple[typing.Union[str,int],...]]:
		"""
		:name [IN]: str
		:unique [IN]: int
		:flags [IN]: int
		:substitutes [IN]: list[tuple[str,str]]
		:allowedTexttypes [IN]: list[str] Default value =pythoncom.Empty
		:allowedAttributenames [IN]: list[str] Default value =pythoncom.Empty
		:resultArray [OUT]: tuple[typing.Union[str,int],...]
		:posx [IN]: float Default value =-950309
		:posy [IN]: float Default value =-950309
		:Return: int

		Available since TLB-Versions: 20.00, 19.04
		"""
		dummy=0
		substitutes = [("","")] + substitutes
		substitutes = [tuple((None,) + i0) for i0 in substitutes]
		ret, resultArray = self._obj.ImportDrawingForProjectGeneration(name, unique, flags, substitutes, allowedTexttypes, allowedAttributenames, dummy, posx, posy)
		resultArray = () if resultArray is None else resultArray
		return ret, resultArray

	def GetSelectedConnectLineIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 20.00, 19.04
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedConnectLineIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetProjectStructureLocking(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 20.00, 19.12
		"""
		return self._obj.GetProjectStructureLocking()

	def SetProjectStructureLocking(self, lock:int) -> int:
		"""
		:lock [IN]: int
		:Return: int

		Available since TLB-Versions: 20.00, 19.12
		"""
		return self._obj.SetProjectStructureLocking(lock)

	def GetActiveAlias(self) -> tuple[int, str]:
		"""
		:name [OUT]: str
		:Return: int

		Available since TLB-Versions: 20.00, 19.12
		"""
		dummy=0
		return self._obj.GetActiveAlias(dummy)

	def CreateInlineConnectorsOnConnectionLine(self, flags:int, LineIDs:list[int], compName:str, compVersion:str) -> tuple[int, tuple[int,...], tuple[int,...], tuple[tuple[int,int,int,int],...]]:
		"""
		:newCoreIDs [OUT]: tuple[int,...]
		:newDeviceIDs [OUT]: tuple[int,...]
		:flags [IN]: int
		:LineIDs [IN]: list[int]
		:compName [IN]: str
		:compVersion [IN]: str
		:newSymbolIDs [OUT]: tuple[tuple[int,int,int,int],...]
		:Return: int

		Available since TLB-Versions: 20.00, 19.12
		"""
		dummy=0
		ret, newCoreIDs, newDeviceIDs, newSymbolIDs = self._obj.CreateInlineConnectorsOnConnectionLine(dummy, dummy, flags, LineIDs, compName, compVersion, dummy)
		newCoreIDs = newCoreIDs[1:] if type(newCoreIDs) == tuple and len(newCoreIDs) > 0 else tuple()
		newDeviceIDs = newDeviceIDs[1:] if type(newDeviceIDs) == tuple and len(newDeviceIDs) > 0 else tuple()
		newSymbolIDs = () if newSymbolIDs is None else newSymbolIDs
		newSymbolIDs = newSymbolIDs[1:] if type(newSymbolIDs) == tuple and len(newSymbolIDs) > 0 else tuple()
		return ret, newCoreIDs, newDeviceIDs, newSymbolIDs

	def UndoAfterExecution(self, newval:bool=True) -> int:
		"""
		:newval [IN]: bool Default value =True
		:Return: int

		Available since TLB-Versions: 20.00, 19.13
		"""
		return self._obj.UndoAfterExecution(newval)

	def ResetSelection(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		return self._obj.ResetSelection()

	def GetSelectedEmbeddedObjectIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 21.00
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedEmbeddedObjectIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def CreateEmbeddedObject(self) -> EmbeddedObject:
		"""
		:Return: EmbeddedObject

		Available since TLB-Versions: 21.00
		"""
		return EmbeddedObject(self._obj.CreateEmbeddedObject())

	def OverwriteMultiuser(self, name:str, filename:str, unlock:int) -> int:
		"""
		:name [IN]: str
		:filename [IN]: str
		:unlock [IN]: int
		:Return: int

		Available since TLB-Versions: 22.00, 21.01
		"""
		return self._obj.OverwriteMultiuser(name, filename, unlock)

	def OptimizeMemory(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 22.00, 21.01, 20.25, 19.46, 19.20
		"""
		return self._obj.OptimizeMemory(flags)

	def GetTreeSelectedSlotIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 22.00, 21.12
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedSlotIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def ExportJT(self, file:str, ids:list[int]=pythoncom.Empty, flags:int=1) -> int:
		"""
		:file [IN]: str
		:ids [IN]: list[int] Default value =pythoncom.Empty
		:flags [IN]: int Default value =1
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.ExportJT(file, ids, flags)

	def CreateStateObject(self) -> State:
		"""
		:Return: State

		Available since TLB-Versions: 22.10
		"""
		return State(self._obj.CreateStateObject())

	def GetTextTypes(self) -> tuple[int, dict[int,tuple[tuple[str,str],...]]]:
		"""
		:textTypeDefinitions [OUT]: dict[int,tuple[tuple[str,str],...]]
		:Return: int

		Available since TLB-Versions: 22.11
		"""
		dummy=0
		ret, textTypeDefinitions = self._obj.GetTextTypes(dummy)
		textTypeDefinitions = _variant_to_dict(textTypeDefinitions)
		for i0 in textTypeDefinitions.keys():
			textTypeDefinitions[i0] = textTypeDefinitions[i0][1:] if type(textTypeDefinitions[i0]) == tuple and len(textTypeDefinitions[i0]) > 0 else tuple()
			textTypeDefinitions[i0] = tuple( i1[1:] if type(i1) == tuple and len(i1) > 0 else tuple() for i1 in textTypeDefinitions[i0])
		return ret, textTypeDefinitions

	def UpdateComponentVersion(self, name:str, version:str, withSymbol:bool=True) -> int:
		"""
		:name [IN]: str
		:version [IN]: str
		:withSymbol [IN]: bool Default value =True
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		return self._obj.UpdateComponentVersion(name, version, withSymbol)

	def GetInvertDisplayColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetInvertDisplayColour()

	def SetInvertDisplayColour(self, value:bool) -> int:
		"""
		:value [IN]: bool
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		return self._obj.SetInvertDisplayColour(value)

	def GetGID(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 23.00
		"""
		return self._obj.GetGID()

	def GetBusbarIds(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		dummy=0
		ret, ids = self._obj.GetBusbarIds(dummy, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetTreeSelectedBusbarIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		dummy=0
		ret, ids = self._obj.GetTreeSelectedBusbarIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetSelectedBusbarIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		dummy=0
		ret, ids = self._obj.GetSelectedBusbarIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetAllBusbarConnectionIds(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 23.00
		"""
		dummy=0
		ret, ids = self._obj.GetAllBusbarConnectionIds(dummy, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetCursorPositionInteractively(self, flags:int=0, boxWidth:float=0, boxHeight:float=0) -> tuple[int, float, float, int, str, str, str]:
		"""
		:xpos [OUT]: float
		:ypos [OUT]: float
		:flags [IN]: int Default value =0
		:keysAndMouseButtons [OUT]: int
		:grid [OUT]: str
		:gridX [OUT]: str
		:gridY [OUT]: str
		:boxWidth [IN]: float Default value =0
		:boxHeight [IN]: float Default value =0
		:Return: int

		Available since TLB-Versions: 23.01, 22.21
		"""
		dummy=0
		return self._obj.GetCursorPositionInteractively(dummy, dummy, flags, dummy, dummy, dummy, dummy, boxWidth, boxHeight)

	def UpdateComponentAttributes(self, name:str, version:str="") -> int:
		"""
		:name [IN]: str
		:version [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 24.00
		"""
		return self._obj.UpdateComponentAttributes(name, version)

	def SaveSheetsAsSingleUserEx(self, name:str, shtids:list[int], completeName:str="", flags:int=0) -> int:
		"""
		:name [IN]: str
		:shtids [IN]: list[int]
		:completeName [IN]: str Default value =""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.00, 23.21, 22.41
		"""
		return self._obj.SaveSheetsAsSingleUserEx(name, shtids, completeName, flags)

	def FocusOnIds(self, focusIds:list[int], focushighlight:bool=False, focushighlightColour:int=-1) -> bool:
		"""
		:focusIds [IN]: list[int]
		:focushighlight [IN]: bool Default value =False
		:focushighlightColour [IN]: int Default value =-1
		:Return: bool

		Available since TLB-Versions: 24.41
		"""
		return self._obj.FocusOnIds(focusIds, focushighlight, focushighlightColour)

	def CreateProjectConfiguratorObject(self) -> ProjectConfigurator:
		"""
		:Return: ProjectConfigurator

		Available since TLB-Versions: 26.00
		"""
		return ProjectConfigurator(self._obj.CreateProjectConfiguratorObject())

	def UpdateAllComponentsAttributes(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 26.00, 25.11
		"""
		return self._obj.UpdateAllComponentsAttributes()

	def HasLockedObjects(self, flags:int=0) -> int:
		"""
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00, 25.23
		"""
		return self._obj.HasLockedObjects(flags)

	def GetLockedObjects(self, flags:int=0) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00, 25.23
		"""
		dummy=0
		ret, ids = self._obj.GetLockedObjects(dummy, flags)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def ImportRedlinerInformation(self, fileName:str, flags:int=0) -> int:
		"""
		:fileName [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00, 25.22
		"""
		return self._obj.ImportRedlinerInformation(fileName, flags)

	def ExportRedlinerInformation(self, fileName:str, flags:int=0) -> int:
		"""
		:fileName [IN]: str
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 26.00, 25.22
		"""
		return self._obj.ExportRedlinerInformation(fileName, flags)

# -------------------- IApplicationInterface--------------------
class Application:
	def __init__(self, pid: typing.Optional[int]=None) -> None:
		if pid is None:
			pid = _get_default_app()
		if pid is None:
			raise RuntimeError('No instance of E3.series is currently running')
		self._obj = _raw_connect_app(pid)

	def __del__(self) -> None:
		try:
			del self._obj
		except:
			pass	# If there is no object there is no need to delete it

	def GetName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetName()

	def GetVersion(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetVersion()

	def GetFullName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetFullName()

	def GetId(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetId()

	def Quit(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Quit()

	def Sleep(self, msec:int) -> int:
		"""
		:msec [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Sleep(msec)

	def Minimize(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Minimize()

	def Maximize(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Maximize()

	def Display(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Display()

	def CreateJobObject(self) -> Job:
		"""
		:Return: Job

		Available since TLB-Versions: 8.50
		"""
		return Job(self._obj.CreateJobObject())

	def ShowNormal(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ShowNormal()

	def GetJobCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetJobCount()

	def GetJobIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetJobIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def PutMessage(self, text:str, item:int=0) -> int:
		"""
		:text [IN]: str
		:item [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PutMessage(text, item)

	def PutInfo(self, ok:int, text:str, item:int=0) -> int:
		"""
		:ok [IN]: int
		:text [IN]: str
		:item [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PutInfo(ok, text, item)

	def PutWarning(self, ok:int, text:str, item:int=0) -> int:
		"""
		:ok [IN]: int
		:text [IN]: str
		:item [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PutWarning(ok, text, item)

	def PutError(self, ok:int, text:str, item:int=0) -> int:
		"""
		:ok [IN]: int
		:text [IN]: str
		:item [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.PutError(ok, text, item)

	def GetTestMark(self, num:int) -> int:
		"""
		:num [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTestMark(num)

	def SetTestMark(self, num:int, value:int) -> int:
		"""
		:num [IN]: int
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetTestMark(num, value)

	def GetPrinterName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPrinterName()

	def SetPrinterName(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPrinterName(name)

	def GetPrinterMargins(self) -> tuple[int, float, float, float, float]:
		"""
		:top [OUT]: float
		:bottom [OUT]: float
		:left [OUT]: float
		:right [OUT]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetPrinterMargins(dummy, dummy, dummy, dummy)

	def SetPrinterMargins(self, top:float, bottom:float, left:float, right:float) -> int:
		"""
		:top [IN]: float
		:bottom [IN]: float
		:left [IN]: float
		:right [IN]: float
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPrinterMargins(top, bottom, left, right)

	def GetPrinterColour(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPrinterColour()

	def SetPrinterColour(self, colour:int) -> int:
		"""
		:colour [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPrinterColour(colour)

	def GetPrinterLinewidth(self) -> float:
		"""
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPrinterLinewidth()

	def SetPrinterLinewidth(self, linewidth:float) -> float:
		"""
		:linewidth [IN]: float
		:Return: float

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPrinterLinewidth(linewidth)

	def GetInstallationPath(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetInstallationPath()

	def GetInstallationLanguage(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetInstallationLanguage()

	def EnableLogfile(self, en:int) -> int:
		"""
		:en [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.EnableLogfile(en)

	def GetComponentDatabase(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetComponentDatabase()

	def GetConfigurationDatabase(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConfigurationDatabase()

	def GetSymbolDatabase(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSymbolDatabase()

	def GetLicense(self, feature:str) -> int:
		"""
		:feature [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLicense(feature)

	def FreeLicense(self, feature:str) -> int:
		"""
		:feature [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.FreeLicense(feature)

	def GetServerName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetServerName()

	def GetServerPort(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetServerPort()

	def GetInfoCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetInfoCount()

	def GetWarningCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetWarningCount()

	def GetErrorCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetErrorCount()

	def SetPrinterCopies(self, copies:int) -> int:
		"""
		:copies [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPrinterCopies(copies)

	def SetPrinterCollate(self, col:int) -> int:
		"""
		:col [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetPrinterCollate(col)

	def GetScriptArguments(self) -> tuple[str,...]:
		"""
		:Return: tuple[str,...]

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetScriptArguments()

	def SortArrayByIndex(self, array:list[typing.Any], rows:int, columns:int, sortindex1:int, sortindex2:int) -> tuple[int, list[typing.Any]]:
		"""
		:array [IN/OUT]: list[typing.Any]
		:rows [IN]: int
		:columns [IN]: int
		:sortindex1 [IN]: int
		:sortindex2 [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SortArrayByIndex(array, rows, columns, sortindex1, sortindex2)

	def FullName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.FullName()

	def ScriptArguments(self) -> tuple[str,...]:
		"""
		:Return: tuple[str,...]

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ScriptArguments()

	def IsCable(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsCable()

	def IsSchema(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsSchema()

	def IsMultiuser(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsMultiuser()

	def IsPanel(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsPanel()

	def IsWire(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsWire()

	def IsSmallBusiness(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsSmallBusiness()

	def IsDemo(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsDemo()

	def IsViewer(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsViewer()

	def IsViewPlus(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsViewPlus()

	def IsStudent(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsStudent()

	def GetBuild(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetBuild()

	def SortArrayByIndexEx(self, array:list[typing.Any], options:list[typing.Any]) -> tuple[int, list[typing.Any]]:
		"""
		:array [IN/OUT]: list[typing.Any]
		:options [IN]: list[typing.Any]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SortArrayByIndexEx(array, options)

	def GetRegistryVersion(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetRegistryVersion()

	def GetLanguageDatabase(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLanguageDatabase()

	def GetMultiuserProjects(self) -> tuple[int, tuple[str,...]]:
		"""
		:name [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, name = self._obj.GetMultiuserProjects(dummy)
		name = name[1:] if type(name) == tuple and len(name) > 0 else tuple()
		return ret, name

	def IsRedliner(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsRedliner()

	def ClearOutputWindow(self) -> None:
		"""

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ClearOutputWindow()

	def AvoidAutomaticClosing(self, avoid:bool=True) -> bool:
		"""
		:avoid [IN]: bool Default value =True
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.AvoidAutomaticClosing(avoid)

	def ScriptFullName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ScriptFullName()

	def ScriptName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.ScriptName()

	def GetPluginObject(self, Plugin:typing.Any) -> typing.Any:
		"""
		:Plugin [IN]: typing.Any
		:Return: typing.Any

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetPluginObject(Plugin)

	def Include(self, text:str) -> int:
		"""
		:text [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Include(text)

	def CreateMenuItemObject(self) -> UserMenuItem:
		"""
		:Return: UserMenuItem

		Available since TLB-Versions: 8.50
		"""
		return UserMenuItem(self._obj.CreateMenuItemObject())

	def GetSystemMenuItemIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetSystemMenuItemIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetUserMenuItemIds(self) -> tuple[int, tuple[int,...]]:
		"""
		:ids [OUT]: tuple[int,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, ids = self._obj.GetUserMenuItemIds(dummy)
		ids = ids[1:] if type(ids) == tuple and len(ids) > 0 else tuple()
		return ret, ids

	def GetLogfileName(self, index:int=0) -> str:
		"""
		:index [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLogfileName(index)

	def SetLogfileName(self, logfile:str, index:int=0) -> int:
		"""
		:logfile [IN]: str
		:index [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLogfileName(logfile, index)

	def GetWorkspaceName(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetWorkspaceName()

	def GetActualDatabase(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetActualDatabase()

	def SetActualDatabase(self, dbname:str) -> int:
		"""
		:dbname [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetActualDatabase(dbname)

	def GetDefinedDatabases(self) -> tuple[int, tuple[str,...]]:
		"""
		:dbnames [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, dbnames = self._obj.GetDefinedDatabases(dummy)
		dbnames = dbnames[1:] if type(dbnames) == tuple and len(dbnames) > 0 else tuple()
		return ret, dbnames

	def GetDefinedDatabaseConnectionStrings(self, dbname:str) -> tuple[int, str, str, str]:
		"""
		:dbname [IN]: str
		:cmp_cs [OUT]: str
		:sym_cs [OUT]: str
		:cnf_cs [OUT]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetDefinedDatabaseConnectionStrings(dbname, dummy, dummy, dummy)

	def SetDefinedDatabaseConnectionStrings(self, dbname:str, cmp_cs:str, sym_cs:str, cnf_cs:str) -> int:
		"""
		:dbname [IN]: str
		:cmp_cs [IN]: str
		:sym_cs [IN]: str
		:cnf_cs [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetDefinedDatabaseConnectionStrings(dbname, cmp_cs, sym_cs, cnf_cs)

	def SetLanguageDatabase(self, dbname:str) -> int:
		"""
		:dbname [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetLanguageDatabase(dbname)

	def SetTemplateFile(self, templatefilename:str) -> int:
		"""
		:templatefilename [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetTemplateFile(templatefilename)

	def GetTemplateFile(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTemplateFile()

	def SetTemplateFileDBE(self, templatefilename:str) -> int:
		"""
		:templatefilename [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetTemplateFileDBE(templatefilename)

	def GetTemplateFileDBE(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTemplateFileDBE()

	def GetUseSheetOrientation(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetUseSheetOrientation()

	def SetUseSheetOrientation(self, set:bool) -> int:
		"""
		:set [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetUseSheetOrientation(set)

	def GetProjectLifecycle(self, project:str) -> str:
		"""
		:project [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetProjectLifecycle(project)

	def SetProjectLifecycle(self, project:str, lifecycle:str) -> int:
		"""
		:project [IN]: str
		:lifecycle [IN]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetProjectLifecycle(project, lifecycle)

	def IsScriptRunning(self) -> bool:
		"""
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsScriptRunning()

	def GetMultiuserFolderPath(self) -> tuple[bool, str]:
		"""
		:path [OUT]: str
		:Return: bool

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetMultiuserFolderPath(dummy)

	def SetTriggerReturn(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetTriggerReturn(value)

	def GetTriggerReturn(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTriggerReturn()

	def GetComponentDatabaseTableSchema(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetComponentDatabaseTableSchema()

	def GetConfigurationDatabaseTableSchema(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetConfigurationDatabaseTableSchema()

	def GetSymbolDatabaseTableSchema(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetSymbolDatabaseTableSchema()

	def GetLanguageDatabaseTableSchema(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetLanguageDatabaseTableSchema()

	def CreateDllObject(self) -> Dll:
		"""
		:Return: Dll

		Available since TLB-Versions: 8.50
		"""
		return Dll(self._obj.CreateDllObject())

	def GetProcessProperty(self, what:str) -> str:
		"""
		:what [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetProcessProperty(what)

	def IsFluid(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsFluid()

	def IsFormboard(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsFormboard()

	def GetTrigger(self, name:str) -> tuple[int, str]:
		"""
		:name [IN]: str
		:filename [OUT]: str
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		return self._obj.GetTrigger(name, dummy)

	def SetTrigger(self, name:str, filename:str, active:int) -> int:
		"""
		:name [IN]: str
		:filename [IN]: str
		:active [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetTrigger(name, filename, active)

	def IsEconomy(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsEconomy()

	def GetAvailableLanguages(self) -> tuple[int, tuple[str,...]]:
		"""
		:languages [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		dummy=0
		ret, languages = self._obj.GetAvailableLanguages(dummy)
		languages = languages[1:] if type(languages) == tuple and len(languages) > 0 else tuple()
		return ret, languages

	def GetTranslatedText(self, text:str, language:str) -> str:
		"""
		:text [IN]: str
		:language [IN]: str
		:Return: str

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetTranslatedText(text, language)

	def Run(self, filename:str, arguments:list[str]) -> int:
		"""
		:filename [IN]: str
		:arguments [IN]: list[str]
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.Run(filename, arguments)

	def SetScriptReturn(self, value:int) -> int:
		"""
		:value [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetScriptReturn(value)

	def GetScriptReturn(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetScriptReturn()

	def GetEnableInteractiveDialogs(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetEnableInteractiveDialogs()

	def SetEnableInteractiveDialogs(self, value:bool) -> int:
		"""
		:value [IN]: bool
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetEnableInteractiveDialogs(value)

	def IsWireWorks(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.IsWireWorks()

	def SetModalWindow(self, hWnd:int) -> int:
		"""
		:hWnd [IN]: int
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.SetModalWindow(hWnd)

	def GetModalWindow(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.GetModalWindow()

	def BeginForeignTask(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.BeginForeignTask()

	def EndForeignTask(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 8.50
		"""
		return self._obj.EndForeignTask()

	def IsFunctionalDesign(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		return self._obj.IsFunctionalDesign()

	def GetProjectInformation(self, filename:str) -> tuple[int, str, int, int]:
		"""
		:filename [IN/OUT]: str
		:_type [OUT]: int
		:is_dbe [OUT]: int
		:Return: int

		Available since TLB-Versions: 9.00
		"""
		dummy=0
		return self._obj.GetProjectInformation(filename, dummy, dummy)

	def GetProvider(self, dbname:str) -> str:
		"""
		:dbname [IN]: str
		:Return: str

		Available since TLB-Versions: 9.22
		"""
		return self._obj.GetProvider(dbname)

	def ResetInfoCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.ResetInfoCount()

	def ResetWarningCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.ResetWarningCount()

	def ResetErrorCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.ResetErrorCount()

	def GetLicensePermanent(self, feature:str) -> int:
		"""
		:feature [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.GetLicensePermanent(feature)

	def FreeLicensePermanent(self, feature:str) -> int:
		"""
		:feature [IN]: str
		:Return: int

		Available since TLB-Versions: 10.00
		"""
		return self._obj.FreeLicensePermanent(feature)

	def ResetVerifyCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.ResetVerifyCount()

	def GetVerifyCount(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.GetVerifyCount()

	def PutVerify(self, ok:int, text:str, item:int=0) -> int:
		"""
		:ok [IN]: int
		:text [IN]: str
		:item [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.PutVerify(ok, text, item)

	def GetPrintSplitPages(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.GetPrintSplitPages()

	def SetPrintSplitPages(self, set:bool) -> int:
		"""
		:set [IN]: bool
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.SetPrintSplitPages(set)

	def GetPrintCropMarks(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.GetPrintCropMarks()

	def SetPrintCropMarks(self, set:bool) -> int:
		"""
		:set [IN]: bool
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.SetPrintCropMarks(set)

	def GetPrintPageNumbers(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.GetPrintPageNumbers()

	def SetPrintPageNumbers(self, set:bool) -> int:
		"""
		:set [IN]: bool
		:Return: int

		Available since TLB-Versions: 10.10
		"""
		return self._obj.SetPrintPageNumbers(set)

	def SetPrintSheetOrder(self, set:int) -> int:
		"""
		:set [IN]: int
		:Return: int

		Available since TLB-Versions: 10.20
		"""
		return self._obj.SetPrintSheetOrder(set)

	def GetPrintSheetOrder(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 10.20
		"""
		return self._obj.GetPrintSheetOrder()

	def SelectComponentFromTable(self) -> tuple[int, str, str]:
		"""
		:ComponentName [OUT]: str
		:ComponentVersion [OUT]: str
		:Return: int

		Available since TLB-Versions: 11.00
		"""
		dummy=0
		return self._obj.SelectComponentFromTable(dummy, dummy)

	def GetDatabaseTableSelectedComponents(self) -> tuple[int, tuple[str,...], tuple[str,...]]:
		"""
		:ComponentArray [OUT]: tuple[str,...]
		:VersionArray [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		dummy=0
		ret, ComponentArray, VersionArray = self._obj.GetDatabaseTableSelectedComponents(dummy, dummy)
		ComponentArray = ComponentArray[1:] if type(ComponentArray) == tuple and len(ComponentArray) > 0 else tuple()
		VersionArray = VersionArray[1:] if type(VersionArray) == tuple and len(VersionArray) > 0 else tuple()
		return ret, ComponentArray, VersionArray

	def GetDatabaseTreeSelectedComponents(self) -> tuple[int, tuple[str,...], tuple[str,...]]:
		"""
		:ComponentArray [OUT]: tuple[str,...]
		:VersionArray [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		dummy=0
		ret, ComponentArray, VersionArray = self._obj.GetDatabaseTreeSelectedComponents(dummy, dummy)
		ComponentArray = ComponentArray[1:] if type(ComponentArray) == tuple and len(ComponentArray) > 0 else tuple()
		VersionArray = VersionArray[1:] if type(VersionArray) == tuple and len(VersionArray) > 0 else tuple()
		return ret, ComponentArray, VersionArray

	def GetDatabaseTreeSelectedSymbols(self) -> tuple[int, tuple[str,...], tuple[str,...]]:
		"""
		:SymbolArray [OUT]: tuple[str,...]
		:VersionArray [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		dummy=0
		ret, SymbolArray, VersionArray = self._obj.GetDatabaseTreeSelectedSymbols(dummy, dummy)
		SymbolArray = SymbolArray[1:] if type(SymbolArray) == tuple and len(SymbolArray) > 0 else tuple()
		VersionArray = VersionArray[1:] if type(VersionArray) == tuple and len(VersionArray) > 0 else tuple()
		return ret, SymbolArray, VersionArray

	def GetDatabaseTreeSelectedModels(self) -> tuple[int, tuple[str,...]]:
		"""
		:ModelArray [OUT]: tuple[str,...]
		:Return: int

		Available since TLB-Versions: 11.70
		"""
		dummy=0
		ret, ModelArray = self._obj.GetDatabaseTreeSelectedModels(dummy)
		ModelArray = ModelArray[1:] if type(ModelArray) == tuple and len(ModelArray) > 0 else tuple()
		return ret, ModelArray

	def ClearResultWindow(self) -> None:
		"""

		Available since TLB-Versions: 11.80
		"""
		return self._obj.ClearResultWindow()

	def PutMultiuserLogMessage(self, source:str, text:str) -> int:
		"""
		:source [IN]: str
		:text [IN]: str
		:Return: int

		Available since TLB-Versions: 11.90
		"""
		return self._obj.PutMultiuserLogMessage(source, text)

	def BringToForeground(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 12.00
		"""
		return self._obj.BringToForeground()

	def PutErrorEx(self, flags:int, text:str, item:int, red:int, green:int, blue:int) -> int:
		"""
		:flags [IN]: int
		:text [IN]: str
		:item [IN]: int
		:red [IN]: int
		:green [IN]: int
		:blue [IN]: int
		:Return: int

		Available since TLB-Versions: 12.00
		"""
		return self._obj.PutErrorEx(flags, text, item, red, green, blue)

	def PutWarningEx(self, flags:int, text:str, item:int, red:int, green:int, blue:int) -> int:
		"""
		:flags [IN]: int
		:text [IN]: str
		:item [IN]: int
		:red [IN]: int
		:green [IN]: int
		:blue [IN]: int
		:Return: int

		Available since TLB-Versions: 12.00
		"""
		return self._obj.PutWarningEx(flags, text, item, red, green, blue)

	def PutInfoEx(self, flags:int, text:str, item:int, red:int, green:int, blue:int) -> int:
		"""
		:flags [IN]: int
		:text [IN]: str
		:item [IN]: int
		:red [IN]: int
		:green [IN]: int
		:blue [IN]: int
		:Return: int

		Available since TLB-Versions: 12.00
		"""
		return self._obj.PutInfoEx(flags, text, item, red, green, blue)

	def PutVerifyEx(self, flags:int, text:str, item:int, red:int, green:int, blue:int) -> int:
		"""
		:flags [IN]: int
		:text [IN]: str
		:item [IN]: int
		:red [IN]: int
		:green [IN]: int
		:blue [IN]: int
		:Return: int

		Available since TLB-Versions: 12.00
		"""
		return self._obj.PutVerifyEx(flags, text, item, red, green, blue)

	def PutMessageEx(self, flags:int, text:str, item:int, red:int, green:int, blue:int) -> int:
		"""
		:flags [IN]: int
		:text [IN]: str
		:item [IN]: int
		:red [IN]: int
		:green [IN]: int
		:blue [IN]: int
		:Return: int

		Available since TLB-Versions: 12.00
		"""
		return self._obj.PutMessageEx(flags, text, item, red, green, blue)

	def ActivateOutputWindow(self, windowId:int) -> int:
		"""
		:windowId [IN]: int
		:Return: int

		Available since TLB-Versions: 12.00
		"""
		return self._obj.ActivateOutputWindow(windowId)

	def SetChildWindowState(self, state:int) -> int:
		"""
		:state [IN]: int
		:Return: int

		Available since TLB-Versions: 17.70
		"""
		return self._obj.SetChildWindowState(state)

	def ShowPluginWindow(self, bShowPluginWindow:bool, guid:str) -> int:
		"""
		:bShowPluginWindow [IN]: bool
		:guid [IN]: str
		:Return: int

		Available since TLB-Versions: 17.70
		"""
		return self._obj.ShowPluginWindow(bShowPluginWindow, guid)

	def ShowWindow(self, windowId:int, show:bool) -> int:
		"""
		:windowId [IN]: int
		:show [IN]: bool
		:Return: int

		Available since TLB-Versions: 17.70
		"""
		return self._obj.ShowWindow(windowId, show)

	def SetMultiuserServer(self, server:str) -> int:
		"""
		:server [IN]: str
		:Return: int

		Available since TLB-Versions: 17.70
		"""
		return self._obj.SetMultiuserServer(server)

	def SetComponentDataView(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 18.01
		"""
		return self._obj.SetComponentDataView(name)

	def GetComponentDataView(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 18.01
		"""
		return self._obj.GetComponentDataView()

	def SetSymbolDataView(self, name:str) -> int:
		"""
		:name [IN]: str
		:Return: int

		Available since TLB-Versions: 18.01
		"""
		return self._obj.SetSymbolDataView(name)

	def GetSymbolDataView(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 18.01
		"""
		return self._obj.GetSymbolDataView()

	def SaveWorkspaceConfiguration(self, name:str="") -> int:
		"""
		:name [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 18.10
		"""
		return self._obj.SaveWorkspaceConfiguration(name)

	def DeleteWorkspaceConfiguration(self, name:str="") -> int:
		"""
		:name [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 18.10
		"""
		return self._obj.DeleteWorkspaceConfiguration(name)

	def RestoreWorkspaceConfiguration(self, name:str="") -> int:
		"""
		:name [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 18.10
		"""
		return self._obj.RestoreWorkspaceConfiguration(name)

	def GetWorkspaceConfigurations(self, path:str="") -> tuple[int, tuple[str,...]]:
		"""
		:names [OUT]: tuple[str,...]
		:path [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 18.10
		"""
		dummy=0
		ret, names = self._obj.GetWorkspaceConfigurations(dummy, path)
		names = names[1:] if type(names) == tuple and len(names) > 0 else tuple()
		return ret, names

	def LoadWorkspaceConfigurationFromFile(self, name:str, path:str) -> int:
		"""
		:name [IN]: str
		:path [IN]: str
		:Return: int

		Available since TLB-Versions: 18.10
		"""
		return self._obj.LoadWorkspaceConfigurationFromFile(name, path)

	def GetCurrentWorkspaceConfiguration(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 18.10
		"""
		return self._obj.GetCurrentWorkspaceConfiguration()

	def GetMultiuserServer(self) -> str:
		"""
		:Return: str

		Available since TLB-Versions: 19.01
		"""
		return self._obj.GetMultiuserServer()

	def CloneWithProject(self, ppid:int, com:str="", data:str="") -> int:
		"""
		:ppid [IN]: int
		:com [IN]: str Default value =""
		:data [IN]: str Default value =""
		:Return: int

		Available since TLB-Versions: 20.00
		"""
		return self._obj.CloneWithProject(ppid, com, data)

	def GetCloningInformation(self, what:str) -> str:
		"""
		:what [IN]: str
		:Return: str

		Available since TLB-Versions: 20.00
		"""
		return self._obj.GetCloningInformation(what)

	def CalculateCircumcircleDiameter(self, dias:list[int]) -> float:
		"""
		:dias [IN]: list[int]
		:Return: float

		Available since TLB-Versions: 20.11, 19.20
		"""
		ret = self._obj.CalculateCircumcircleDiameter(dias)
		return ret[0]

	def IsDistDesign(self) -> int:
		"""
		:Return: int

		Available since TLB-Versions: 22.00
		"""
		return self._obj.IsDistDesign()

	def SuppressMessages(self, suppress:bool, flags:int=0) -> int:
		"""
		:suppress [IN]: bool
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 23.01
		"""
		return self._obj.SuppressMessages(suppress, flags)

	def SetConfigFile(self, processType:int, filepath:str, flags:int=0) -> str:
		"""
		:processType [IN]: int
		:filepath [IN]: str
		:flags [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 24.11
		"""
		return self._obj.SetConfigFile(processType, filepath, flags)

	def GetConfigFile(self, processType:int, flags:int=0) -> str:
		"""
		:processType [IN]: int
		:flags [IN]: int Default value =0
		:Return: str

		Available since TLB-Versions: 24.11
		"""
		return self._obj.GetConfigFile(processType, flags)

	def GetComponentList(self, additionalAttributes:list[str]=pythoncom.Empty, flags:int=0) -> tuple[int, tuple[tuple[typing.Union[str,int],...],...]]:
		"""
		:result [OUT]: tuple[tuple[typing.Union[str,int],...],...], Enum types Available: e3series.types.ComponentType, ComponentSubType.
		:additionalAttributes [IN]: list[str] Default value =pythoncom.Empty
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		dummy=0
		return self._obj.GetComponentList(dummy, additionalAttributes, flags)

	def GetModelList(self, additionalAttributes:list[str]=pythoncom.Empty, flags:int=0) -> tuple[int, tuple[tuple[typing.Union[str,int],...],...]]:
		"""
		:result [OUT]: tuple[tuple[typing.Union[str,int],...],...], Enum type Available: e3series.types.ModelType.
		:additionalAttributes [IN]: list[str] Default value =pythoncom.Empty
		:flags [IN]: int Default value =0
		:Return: int

		Available since TLB-Versions: 24.11
		"""
		dummy=0
		return self._obj.GetModelList(dummy, additionalAttributes, flags)


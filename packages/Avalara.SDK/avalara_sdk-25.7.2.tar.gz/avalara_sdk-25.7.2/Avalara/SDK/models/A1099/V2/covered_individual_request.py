# coding: utf-8

"""
AvaTax Software Development Kit for Python.

   Copyright 2022 Avalara, Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

    Avalara 1099 & W-9 API Definition
    ## 🔐 Authentication  Use **username/password** or generate a **license key** from: *Avalara Portal → Settings → License and API Keys*.  [More on authentication methods](https://developer.avalara.com/avatax-dm-combined-erp/common-setup/authentication/authentication-methods/)  [Test your credentials](https://developer.avalara.com/avatax/test-credentials/)  ## 📘 API & SDK Documentation  [Avalara SDK (.NET) on GitHub](https://github.com/avadev/Avalara-SDK-DotNet#avalarasdk--the-unified-c-library-for-next-gen-avalara-services)  [Code Examples – 1099 API](https://github.com/avadev/Avalara-SDK-DotNet/blob/main/docs/A1099/V2/Class1099IssuersApi.md#call1099issuersget) 

@author     Sachin Baijal <sachin.baijal@avalara.com>
@author     Jonathan Wenger <jonathan.wenger@avalara.com>
@copyright  2022 Avalara, Inc.
@license    https://www.apache.org/licenses/LICENSE-2.0
@version    25.7.2
@link       https://github.com/avadev/AvaTax-REST-V3-Python-SDK
"""

from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class CoveredIndividualRequest(BaseModel):
    """
    CoveredIndividualRequest
    """ # noqa: E501
    first_name: Optional[StrictStr] = Field(default=None, alias="firstName")
    middle_name: Optional[StrictStr] = Field(default=None, alias="middleName")
    last_name: Optional[StrictStr] = Field(default=None, alias="lastName")
    name_suffix: Optional[StrictStr] = Field(default=None, alias="nameSuffix")
    tin: Optional[StrictStr] = None
    birth_date: Optional[datetime] = Field(default=None, alias="birthDate")
    covered_month_indicator0: Optional[StrictBool] = Field(default=None, alias="coveredMonthIndicator0")
    covered_month_indicator1: Optional[StrictBool] = Field(default=None, alias="coveredMonthIndicator1")
    covered_month_indicator2: Optional[StrictBool] = Field(default=None, alias="coveredMonthIndicator2")
    covered_month_indicator3: Optional[StrictBool] = Field(default=None, alias="coveredMonthIndicator3")
    covered_month_indicator4: Optional[StrictBool] = Field(default=None, alias="coveredMonthIndicator4")
    covered_month_indicator5: Optional[StrictBool] = Field(default=None, alias="coveredMonthIndicator5")
    covered_month_indicator6: Optional[StrictBool] = Field(default=None, alias="coveredMonthIndicator6")
    covered_month_indicator7: Optional[StrictBool] = Field(default=None, alias="coveredMonthIndicator7")
    covered_month_indicator8: Optional[StrictBool] = Field(default=None, alias="coveredMonthIndicator8")
    covered_month_indicator9: Optional[StrictBool] = Field(default=None, alias="coveredMonthIndicator9")
    covered_month_indicator10: Optional[StrictBool] = Field(default=None, alias="coveredMonthIndicator10")
    covered_month_indicator11: Optional[StrictBool] = Field(default=None, alias="coveredMonthIndicator11")
    covered_month_indicator12: Optional[StrictBool] = Field(default=None, alias="coveredMonthIndicator12")
    __properties: ClassVar[List[str]] = ["firstName", "middleName", "lastName", "nameSuffix", "tin", "birthDate", "coveredMonthIndicator0", "coveredMonthIndicator1", "coveredMonthIndicator2", "coveredMonthIndicator3", "coveredMonthIndicator4", "coveredMonthIndicator5", "coveredMonthIndicator6", "coveredMonthIndicator7", "coveredMonthIndicator8", "coveredMonthIndicator9", "coveredMonthIndicator10", "coveredMonthIndicator11", "coveredMonthIndicator12"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of CoveredIndividualRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if first_name (nullable) is None
        # and model_fields_set contains the field
        if self.first_name is None and "first_name" in self.model_fields_set:
            _dict['firstName'] = None

        # set to None if middle_name (nullable) is None
        # and model_fields_set contains the field
        if self.middle_name is None and "middle_name" in self.model_fields_set:
            _dict['middleName'] = None

        # set to None if last_name (nullable) is None
        # and model_fields_set contains the field
        if self.last_name is None and "last_name" in self.model_fields_set:
            _dict['lastName'] = None

        # set to None if name_suffix (nullable) is None
        # and model_fields_set contains the field
        if self.name_suffix is None and "name_suffix" in self.model_fields_set:
            _dict['nameSuffix'] = None

        # set to None if tin (nullable) is None
        # and model_fields_set contains the field
        if self.tin is None and "tin" in self.model_fields_set:
            _dict['tin'] = None

        # set to None if birth_date (nullable) is None
        # and model_fields_set contains the field
        if self.birth_date is None and "birth_date" in self.model_fields_set:
            _dict['birthDate'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CoveredIndividualRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "firstName": obj.get("firstName"),
            "middleName": obj.get("middleName"),
            "lastName": obj.get("lastName"),
            "nameSuffix": obj.get("nameSuffix"),
            "tin": obj.get("tin"),
            "birthDate": obj.get("birthDate"),
            "coveredMonthIndicator0": obj.get("coveredMonthIndicator0"),
            "coveredMonthIndicator1": obj.get("coveredMonthIndicator1"),
            "coveredMonthIndicator2": obj.get("coveredMonthIndicator2"),
            "coveredMonthIndicator3": obj.get("coveredMonthIndicator3"),
            "coveredMonthIndicator4": obj.get("coveredMonthIndicator4"),
            "coveredMonthIndicator5": obj.get("coveredMonthIndicator5"),
            "coveredMonthIndicator6": obj.get("coveredMonthIndicator6"),
            "coveredMonthIndicator7": obj.get("coveredMonthIndicator7"),
            "coveredMonthIndicator8": obj.get("coveredMonthIndicator8"),
            "coveredMonthIndicator9": obj.get("coveredMonthIndicator9"),
            "coveredMonthIndicator10": obj.get("coveredMonthIndicator10"),
            "coveredMonthIndicator11": obj.get("coveredMonthIndicator11"),
            "coveredMonthIndicator12": obj.get("coveredMonthIndicator12")
        })
        return _obj



#
# (c) 2025, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from typing import Dict, Any

from nexium_database import BaseModel
from sqlmodel import SQLModel


class BaseDbModel(BaseModel):
    def model_dump(
        self,
        **kwargs
    ) -> Dict[str, Any]:
        result = {}
        for field_name, field_value in self.__dict__.items():
            if field_name == '_sa_instance_state':
                continue
            if isinstance(field_value, SQLModel):
                result[field_name] = field_value.model_dump()
            else:
                result[field_name] = field_value
        return result

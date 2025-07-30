# import datetime
# from typing import Any, Generic, List, Optional, Type, TypeVar

# from fastapi import Depends
# from pydantic import BaseModel
# from sqlalchemy import (
#     ScalarResult,
#     and_,
#     asc,
#     case,
#     delete,
#     desc,
#     func,
#     update,
# )
# from sqlalchemy.exc import NoResultFound
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlalchemy.orm import load_only

# from cores.component.sqlalchemy import Base
# from cores.model.paging import PagingDTO

# # @as_declarative()
# # class Base(SQLModel):
# #     id: Mapped[str] = mapped_column(primary_key=True)
# #     active: Mapped[Optional[datetime]] = mapped_column(
# #         DateTime, nullable=True
# #     )


# # class CondBase(SQLModel):
# #     except_ids: str
# #     exist_ids: str


# # Define generic types
# Entity = TypeVar("Entity", bound=Base)
# Cond = TypeVar("Cond")
# UpdateDTO = TypeVar("UpdateDTO", bound=BaseModel)
# CreateDTO = TypeVar("CreateDTO", bound=BaseModel)


# class BaseQueryRepositorySQLAlchemy(Generic[Entity, Cond]):
#     def __init__(self, session: AsyncSession, model: Type[Entity]):
#         self.session = session
#         self.model = model

#     async def get(
#         self,
#         id: str | int,
#         options=[],
#         columns: list = [],
#         with_trash: bool = False,
#     ) -> Optional[Entity]:
#         query = (
#             select(self.model)
#             .where(self.model.id == id)  # type: ignore
#             .options(*options)
#         )

#         if columns:
#             query = query.options(load_only(*columns))

#         if not with_trash and hasattr(self.model, "active"):
#             query = query.where(self.model.active.is_(True))
#         result = await self.session.execute(query)

#         try:
#             entity = result.scalar()
#             return entity
#         except NoResultFound:
#             return None

#     async def get_by_ids(
#         self,
#         ids: list[int],
#         options=[],
#         columns: list = [],
#         with_trash: bool = False,
#     ) -> ScalarResult:
#         query = (
#             select(self.model)
#             .where(self.model.id.in_(ids))  # type: ignore
#             .options(*options)
#         )

#         if columns:
#             query = query.options(load_only(*columns))

#         if not with_trash and hasattr(self.model, "active"):
#             query = query.where(self.model.active.is_(True))  # type: ignore
#         result = await self.session.execute(query)
#         return result.scalars()

#     async def find_by_cond(
#         self,
#         cond: dict | list,
#         options=[],
#         columns: list = [],
#         with_trash: bool = False,
#         exact: bool = False,
#     ) -> Optional[Entity]:
#         """
#         Tìm kiếm và trả về một đối tượng Entity dựa trên các điều kiện được chỉ định.

#         Args:
#             cond (Union[dict, list]): Các điều kiện tìm kiếm. Có thể là một dict hoặc một list.
#                 - Nếu là dict, mỗi khóa là tên cột và mỗi giá trị là giá trị tìm kiếm.
#                 - Nếu là list, mỗi phần tử là một dict với các khóa "column", "operator" và "value".
#             options (list): Các tùy chọn cho câu lệnh SQL.
#             columns (list): Danh sách các cột cần lấy.
#             with_trash (bool): Có bao gồm các bản ghi đã bị xóa hay không.

#         Returns:
#             Optional[Entity]: Đối tượng Entity tìm thấy hoặc None nếu không tìm thấy.

#         Ví dụ:
#             - Tìm kiếm một đối tượng Entity với tên là "John" và tuổi là 30:
#                 cond = {"name": "John", "age": 30}
#                 result = await self.find_by_cond(cond)
#             - Tìm kiếm một đối tượng Entity với tên là "John" và tuổi nhỏ hơn hoặc bằng 30:
#                 cond = [
#                     {"column": "name", "operator": "==", "value": "John"},
#                     {"column": "age", "operator": "<=", "value": 30}
#                 ]
#                 result = await self.find_by_cond(cond)
#         """
#         query = select(self.model).options(*options)

#         if isinstance(cond, dict) and exact is True:
#             query = query.filter_by(**cond)
#         elif isinstance(cond, dict) and exact is False:
#             for key, value in cond.items():
#                 if isinstance(
#                     value, str
#                 ):  # Chỉ áp dụng với giá trị dạng string
#                     query = query.filter(
#                         func.lower(getattr(self.model, key)).ilike(
#                             f"%{value.lower()}%"
#                         )
#                     )
#                 elif isinstance(value, datetime.date):
#                     query = query.filter(getattr(self.model, key) == value)
#                 else:
#                     query = query.filter(
#                         getattr(self.model, key) == value
#                     )  # Các kiểu khác giữ nguyên
#         elif isinstance(cond, list):
#             conditions_sql = []
#             for condition in cond:
#                 column = getattr(self.model, condition["column"], None)
#                 if column is None:
#                     raise ValueError(
#                         f"Column '{condition['column']}' not found"
#                     )

#                 if condition["operator"] == "==":
#                     conditions_sql.append(column == condition["value"])
#                 elif condition["operator"] == "!=":
#                     conditions_sql.append(column != condition["value"])
#                 elif condition["operator"] == ">":
#                     conditions_sql.append(column > condition["value"])
#                 elif condition["operator"] == "<":
#                     conditions_sql.append(column < condition["value"])
#                 elif condition["operator"] == ">=":
#                     conditions_sql.append(column >= condition["value"])
#                 elif condition["operator"] == "<=":
#                     conditions_sql.append(column <= condition["value"])
#                 else:
#                     raise ValueError(
#                         f"Invalid operator '{condition['operator']}'"
#                     )

#             query = query.where(and_(*conditions_sql))

#         if columns:
#             query = query.options(load_only(*columns))

#         if not with_trash and hasattr(self.model, "active"):
#             query = query.where(self.model.active.is_(True))  # type: ignore

#         return await self.session.scalar(query)

#     async def get_all_by_cond(
#         self,
#         cond: Cond | None = None,
#         options=[],
#         columns: list = [],
#         with_trash: bool = False,
#     ) -> list[Entity]:

#         query = select(self.model).options(*options)

#         if cond:
#             query = self.apply_filter(cond, query)

#         if not with_trash and hasattr(self.model, "active"):
#             query = query.where(self.model.active.is_(True))

#         if columns:
#             query = query.options(load_only(*columns))

#         result = await self.session.execute(query)
#         return list(result.scalars())

#     async def get_paging_list(
#         self,
#         cond: Cond,
#         paging: PagingDTO,
#         options=[],
#         columns: list = [],
#         with_trash: bool = False,
#     ) -> list[Entity]:
#         base_query = select(self.model).options(*options)

#         # Xử lý các tham số tìm kiếm nếu có
#         if cond is not None:
#             base_query = self.apply_filter(cond, base_query)

#         if not with_trash and hasattr(self.model, "active"):
#             base_query = base_query.where(self.model.active.is_(True))

#         # Sắp xếp và phân trang
#         query = self.apply_pagination(paging, base_query)

#         # Loại trừ các id đã nhập nếu có
#         if hasattr(cond, "except_ids") and getattr(cond, "except_ids"):
#             except_ids = list(map(int, getattr(cond, "except_ids").split(",")))
#             query = query.where(
#                 self.model.id.not_in(except_ids)  # type: ignore
#             )

#         # Bao gồm các id đã nhập nếu có
#         if hasattr(cond, "exist_ids") and getattr(cond, "exist_ids"):
#             exist_ids = list(map(int, getattr(cond, "exist_ids").split(",")))
#             query = query.where(self.model.id.in_(exist_ids))  # type: ignore

#         query = self.apply_sorting(paging, query)

#         if columns:
#             query = query.options(load_only(*columns))
#         return await self.execute_pagination_query(paging, base_query, query)

#     def apply_filter(self, cond, base_query):
#         for key, param in cond:
#             if param:
#                 column = getattr(self.model, key, None)
#                 if column:
#                     if isinstance(param, int):
#                         base_query = base_query.where(column == param)
#                     elif isinstance(param, datetime.date) or isinstance(
#                         param, datetime.datetime
#                     ):
#                         base_query = base_query.where(column == param)
#                     elif isinstance(param, str):
#                         base_query = base_query.where(
#                             func.lower(column).ilike(f"%{param.lower()}%")
#                         )
#                     else:
#                         base_query = base_query.where(
#                             func.lower(column).ilike(f"%{param.lower()}%")
#                         )
#         return base_query

#     async def execute_pagination_query(
#         self, paging: PagingDTO, base_query, query
#     ) -> tuple[list[Entity], int]:
#         result = await self.session.execute(query)
#         entities = list(result.scalars())

#         # Calculate total count
#         total_query = select(func.count()).select_from(base_query)

#         total_result = await self.session.execute(total_query)
#         total_items = total_result.scalar_one()
#         return entities, total_items

#     def apply_sorting(self, paging: PagingDTO, query):
#         if hasattr(paging, "order"):
#             direction = desc if paging.order == "desc" else asc
#             query = query.order_by(
#                 direction(getattr(self.model, paging.sort_by))
#             )
#         return query

#     def apply_pagination(self, paging: PagingDTO, base_query):
#         query = base_query.limit(paging.page_size).offset(
#             (paging.page - 1) * paging.page_size
#         )
#         return query


# class BaseCommandRepositorySQLAlchemy(Generic[Entity, CreateDTO, UpdateDTO]):
#     def __init__(self, session: AsyncSession, model: Type[Entity]):
#         self.session = session
#         self.model = model

#     async def insert(
#         self, data: Entity | CreateDTO, with_commit=True, model_validate=True
#     ) -> Entity:
#         if isinstance(data, BaseModel):
#             data = self.model(**data.model_dump())
#         self.session.add(data)

#         await self.session.flush()  # Lấy ID nếu cần
#         if with_commit:  # Nếu không dùng Transaction Block, tự động commit
#             await self.session.commit()
#             await self.session.refresh(data)  # Làm mới dữ liệu từ DB
#         return data

#     async def update(
#         self, id: str | int, data: UpdateDTO | dict, with_commit=True
#     ) -> bool:
#         if not isinstance(data, dict):
#             data = data.model_dump(exclude_none=True)

#         query = (
#             update(self.model)
#             .where(self.model.id == id)  # type: ignore
#             .values(**data)
#             .execution_options(synchronize_session="fetch")
#         )
#         await self.session.execute(query)

#         if with_commit:
#             await self.session.commit()

#         return True

#     async def update_by_condition(
#         self, condition: dict, data: dict, with_commit: bool = True
#     ) -> bool:
#         """
#         Cập nhật bản ghi dựa trên điều kiện.

#         :param condition: Dict chứa điều kiện lọc bản ghi cần cập nhật.
#         :param data: Dict chứa dữ liệu cần cập nhật.
#         :param with_commit: Nếu True, commit thay đổi ngay sau khi cập nhật.
#         :return: True nếu cập nhật thành công.
#         """
#         if not isinstance(data, dict):
#             raise ValueError("Data must be a dictionary.")

#         filters = [
#             getattr(self.model, key) == value
#             for key, value in condition.items()
#         ]

#         query = (
#             update(self.model)
#             .where(and_(*filters))
#             .values(**data)
#             .execution_options(synchronize_session="fetch")
#         )

#         await self.session.execute(query)

#         if with_commit:
#             await self.session.commit()

#         return True

#     async def soft_update(
#         self, old_entity: Entity, data: UpdateDTO | dict, with_commit=True
#     ) -> Entity:
#         old_entity.active = False

#         # Convert Pydantic DTO to dict if necessary
#         if not isinstance(data, dict):
#             data = data.model_dump(exclude_none=True)

#         # Merge old data and new data
#         update_data = {
#             **{
#                 k: v
#                 for k, v in old_entity.__dict__.items()
#                 if k != "_sa_instance_state"
#             },
#             **data,
#             "id": None,  # Tạo bản ghi mới -> để None để DB tự tạo ID
#             "active": True,  # Đánh dấu bản ghi mới là active
#         }

#         # Tạo bản ghi mới từ dữ liệu đã cập nhật
#         new_entity = type(old_entity)(**update_data)

#         self.session.add(new_entity)

#         await self.session.flush()  # Lấy ID nếu cần
#         if with_commit:  # Nếu không dùng Transaction Block, tự động commit
#             await self.session.commit()
#             await self.session.refresh(new_entity)  # Làm mới dữ liệu từ DB
#         return new_entity

#     async def update_or_create(
#         self, defaults: dict[str, Any] | None = None, with_commit=True, **cond
#     ) -> Entity:
#         """
#         - Nếu bản ghi tồn tại → cập nhật
#         - Nếu không tồn tại → tạo mới
#         Args:
#             defaults (Optional[Dict[str, Any]]): Giá trị mặc định cần cập nhật
#             kwargs: Điều kiện tìm kiếm
#         Returns:
#             Tuple[model, bool]: (instance, created)
#         """

#         defaults = defaults or {}

#         # Tìm bản ghi hiện có
#         statement = select(self.model).filter_by(**cond)
#         instance = await self.session.scalar(statement)

#         if instance:
#             # Cập nhật các trường từ defaults
#             for key, value in defaults.items():
#                 setattr(instance, key, value)
#         else:
#             # Tạo mới nếu không tồn tại
#             instance = self.model(**cond, **defaults)
#             self.session.add(instance)
#             await self.session.flush()

#         if with_commit:
#             await self.session.commit()
#         return instance

#     async def delete(
#         self, id: str | int, is_hard: bool = False, with_commit=True
#     ) -> bool:
#         query = None
#         if is_hard:
#             query = (
#                 delete(self.model)
#                 .where(self.model.id == id)  # type: ignore
#                 .execution_options(synchronize_session="fetch")
#             )
#         elif hasattr(self.model, "active"):
#             query = (
#                 update(self.model)
#                 .where(self.model.id == id)  # type: ignore
#                 .values(active=False)
#                 .execution_options(synchronize_session="fetch")
#             )
#         if query is None:
#             raise ValueError(
#                 "Cannot delete: Model does not support soft delete."
#             )

#         await self.session.execute(query)

#         if with_commit:
#             await self.session.commit()

#         return True

#     async def delete_by_condition(
#         self, condition: dict, is_hard: bool = False, with_commit: bool = True
#     ) -> bool:
#         """
#         Xóa bản ghi dựa trên điều kiện.

#         :param condition: Dict chứa điều kiện để xóa.
#         :param is_hard: Nếu True, xóa cứng; nếu False, xóa mềm (nếu có `active`).
#         :param with_commit: Nếu True, commit thay đổi ngay sau khi xóa.
#         :return: True nếu xóa thành công.
#         """
#         query = None
#         filters = []

#         for key, value in condition.items():
#             if isinstance(value, dict):
#                 for op, val in value.items():
#                     if op == "in":
#                         filters.append(getattr(self.model, key).in_(val))
#             else:
#                 filters.append(getattr(self.model, key) == value)

#         if is_hard:
#             query = (
#                 delete(self.model)
#                 .where(and_(*filters))
#                 .execution_options(synchronize_session="fetch")
#             )
#         elif hasattr(self.model, "active"):
#             query = (
#                 update(self.model)
#                 .where(and_(*filters))
#                 .values(active=False)
#                 .execution_options(synchronize_session="fetch")
#             )

#         if query is None:
#             raise ValueError(
#                 "Cannot delete: Model does not support soft delete."
#             )

#         await self.session.execute(query)

#         if with_commit:
#             await self.session.commit()

#         return True

#     def bulk_insert(self, entities: list[Entity]):
#         self.session.add_all(entities)

#     async def bulk_update(
#         self, ids: List[int] = [], data: dict = {}, with_commit: bool = True
#     ) -> bool:
#         """
#         Update với 2 trường hợp:
#         1. Nếu ids có giá trị, cập nhật các bản ghi theo ids, với giá trị là data (cho trường hợp data update giống nhau)
#         2. Nếu ids rỗng, cập nhật các bản ghi gvới data như sau
#                data = {
#                    "id_1": {"key_1": value_1},
#                    "id_2": {"key_2": value_2}
#                }
#         """
#         if not isinstance(data, dict):
#             raise ValueError("Data must be a dictionary.")

#         if not ids:
#             ids = list(data.keys())
#             updates = {}

#             # Lấy danh sách tất cả các cột cần update
#             all_columns = set()
#             for changes in data.values():
#                 all_columns.update(changes.keys())

#             for col in all_columns:
#                 updates[col] = case(
#                     *(
#                         (self.model.id == id_, values[col])
#                         for id_, values in data.items()
#                         if col in values
#                     ),
#                     else_=getattr(self.model, col),
#                 )
#             data = updates
#         if not data:
#             return False
#         query = (
#             update(self.model)
#             .where(self.model.id.in_(ids))
#             .values(**data)
#             .execution_options(synchronize_session="fetch")
#         )
#         await self.session.execute(query)

#         if with_commit:
#             await self.session.commit()

#         return True

#     async def save_change(self) -> bool:
#         try:
#             await self.session.commit()  # Commit toàn bộ thay đổi
#             return True
#         except Exception as e:
#             await self.session.rollback()  # Rollback nếu xảy ra lỗi
#             raise e

#     async def refresh(self, entity: Entity):
#         await self.session.refresh(entity)

#     async def flush(self):
#         await self.session.flush()


# QueryRepo = TypeVar("QueryRepo", bound=BaseQueryRepositorySQLAlchemy)
# CMDRepo = TypeVar("CMDRepo", bound=BaseCommandRepositorySQLAlchemy)


# class BaseRepositorySQLAlchemy(
#     Generic[Entity, Cond, CreateDTO, UpdateDTO, QueryRepo, CMDRepo]
# ):
#     def __init__(
#         self,
#         query_repo: QueryRepo = Depends(BaseQueryRepositorySQLAlchemy),
#         cmd_repo: CMDRepo = Depends(BaseCommandRepositorySQLAlchemy),
#     ):
#         self.query_repo = query_repo
#         self.cmd_repo = cmd_repo

#     async def get(
#         self,
#         id: str | int,
#         options=[],
#         columns: list = [],
#         with_trash: bool = False,
#     ) -> Optional[Entity]:
#         return await self.query_repo.get(id, options, columns, with_trash)

#     async def get_by_ids(
#         self,
#         ids: list[int],
#         options=[],
#         columns: list = [],
#         with_trash: bool = False,
#     ) -> ScalarResult:
#         return await self.query_repo.get_by_ids(
#             ids, options, columns, with_trash
#         )

#     async def find_by_cond(
#         self,
#         cond: dict,
#         options=[],
#         columns: list = [],
#         with_trash: bool = False,
#     ) -> Optional[Entity]:
#         return await self.query_repo.find_by_cond(
#             cond, options, columns, with_trash
#         )

#     async def list(
#         self,
#         cond: Cond,
#         paging: PagingDTO,
#         options=[],
#         columns: list = [],
#         with_trash: bool = False,
#     ) -> tuple[list[Entity], int]:
#         return await self.query_repo.get_paging_list(
#             cond, paging, options, columns, with_trash
#         )

#     async def insert(self, data: Entity | CreateDTO, with_commit=True) -> bool:
#         return await self.cmd_repo.insert(data, with_commit)

#     async def update(
#         self, id: str | int, data: UpdateDTO, with_commit=True
#     ) -> bool:
#         return await self.cmd_repo.update(id, data, with_commit)

#     async def delete(
#         self, id: str | int, is_hard: bool = False, with_commit=True
#     ) -> bool:
#         return await self.cmd_repo.delete(id, is_hard, with_commit)

#     async def save_change(self) -> bool:
#         return await self.cmd_repo.save_change()

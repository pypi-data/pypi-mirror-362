import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import and_, asc, case, delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from cores.model.paging import PagingDTO

# Giả sử Base và PagingDTO được định nghĩa ở đâu đó
# from cores.component.sqlalchemy import Base
# from cores.model.paging import PagingDTO


# Định nghĩa tạm để code có thể chạy
class Base:
    id: Any
    active: Any


Entity = TypeVar("Entity", bound=Base)
Schema = TypeVar("Schema", bound=BaseModel)


class BaseSQLAlchemyRepository(Generic[Entity]):
    """
    Lớp Repository cơ sở cho SQLAlchemy, được tối ưu hóa về tính rõ ràng và nhất quán.
    - Session được inject vào constructor và được sử dụng trong toàn bộ class.
    - Giữ lại đầy đủ các phương thức logic gốc, nhưng được dọn dẹp và thêm tài liệu.
    """

    def __init__(self, session: AsyncSession, model: Type[Entity]):
        self.session = session
        self.model = model

    # --------------------------------------------------------------------------
    # HÀM TRUY VẤN (GET/FIND)
    # --------------------------------------------------------------------------

    async def get(
        self,
        id: str | int,
        *,
        options: Optional[List] = None,
        columns: Optional[List[str]] = None,
        with_trash: bool = False,
    ) -> Optional[Entity]:
        """Lấy một đối tượng duy nhất theo ID."""
        query = select(self.model).where(self.model.id == id)

        if options:
            query = query.options(*options)
        if columns:
            query = query.options(load_only(*columns))
        if not with_trash and hasattr(self.model, "active"):
            query = query.where(self.model.active.is_(True))

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_ids(
        self,
        ids: List[int | str],
        *,
        options: Optional[List] = None,
        columns: Optional[List[str]] = None,
        with_trash: bool = False,
    ) -> List[Entity]:
        """Lấy danh sách các đối tượng theo danh sách ID."""
        query = select(self.model).where(self.model.id.in_(ids))

        if options:
            query = query.options(*options)
        if columns:
            query = query.options(load_only(*columns))
        if not with_trash and hasattr(self.model, "active"):
            query = query.where(self.model.active.is_(True))

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def find_one_by(
        self,
        *,
        with_trash: bool = False,
        options: Optional[List] = None,
        **conditions: Any,
    ) -> Optional[Entity]:
        """Tìm một bản ghi đầu tiên khớp với các điều kiện (dạng key=value)."""
        query = select(self.model).filter_by(**conditions)

        if options:
            query = query.options(*options)

        if not with_trash and hasattr(self.model, "active"):
            query = query.where(self.model.active.is_(True))

        result = await self.session.execute(query.limit(1))
        return result.scalar_one_or_none()

    async def find_all_by(
        self, *, with_trash: bool = False, **conditions: Any
    ) -> List[Entity]:
        """Tìm tất cả các bản ghi khớp với điều kiện (dạng key=value)."""
        query = select(self.model).filter_by(**conditions)

        if not with_trash and hasattr(self.model, "active"):
            query = query.where(self.model.active.is_(True))

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_paging_list(
        self,
        paging: PagingDTO,
        options: Optional[List] = None,
        with_trash: bool = False,
        **conditions: Any,
    ) -> list[Entity]:
        """
        Hàm lấy danh sách có phân trang, sắp xếp, tìm kiếm và trả về tổng số.
        Đây là hàm cốt lõi thay thế cho get_paging_list, get_all_by_cond,...
        """
        base_query = select(self.model)

        if options:
            base_query = base_query.options(*options)
        # Áp dụng bộ lọc (filter)
        base_query = self.apply_filter(base_query, **conditions)

        if not with_trash and hasattr(self.model, "active"):
            base_query = base_query.where(self.model.active.is_(True))
        # Sắp xếp và phân trang
        query = self.apply_pagination(paging, base_query)

        query = self.apply_sorting(paging, query)
        return await self.execute_pagination_query(paging, base_query, query)

    def apply_filter(self, base_query, **cond):
        for key, param in cond.items():
            if param:
                column = getattr(self.model, key, None)
                if column:
                    if isinstance(param, int):
                        base_query = base_query.where(column == param)
                    elif isinstance(param, datetime.date) or isinstance(
                        param, datetime.datetime
                    ):
                        base_query = base_query.where(column == param)
                    elif isinstance(param, str):
                        base_query = base_query.where(
                            func.lower(column).ilike(f"%{param.lower()}%")
                        )
                    else:
                        base_query = base_query.where(
                            func.lower(column).ilike(f"%{param.lower()}%")
                        )
        return base_query

    async def execute_pagination_query(
        self, paging: PagingDTO, base_query, query
    ) -> list[Entity]:
        result = await self.session.execute(query)
        entities = list(result.scalars())

        # Calculate total count
        total_query = select(func.count()).select_from(base_query)

        total_result = await self.session.execute(total_query)
        paging.total = total_result.scalar()
        return entities

    def apply_sorting(self, paging: PagingDTO, query):
        if hasattr(paging, "order"):
            direction = desc if paging.order == "desc" else asc
            query = query.order_by(
                direction(getattr(self.model, paging.sort_by))
            )
        return query

    def apply_pagination(self, paging: PagingDTO, base_query):
        query = base_query.limit(paging.page_size).offset(
            (paging.page - 1) * paging.page_size
        )
        return query

    # --------------------------------------------------------------------------
    # HÀM GHI DỮ LIỆU (CREATE/UPDATE/DELETE)
    # --------------------------------------------------------------------------

    async def insert(
        self, data: Entity | BaseModel, with_commit=True, model_validate=True
    ) -> Entity:
        if isinstance(data, BaseModel):
            data = self.model(**data.model_dump())
        self.session.add(data)

        await self.session.flush()
        return data

    def bulk_insert(self, entities: list[Entity]):
        self.session.add_all(entities)

    async def update(
        self, id: str | int, data_in: Schema | Dict[str, Any]
    ) -> bool:
        """Cập nhật nhiều trường của một bản ghi dựa trên ID (dùng `update().values()`)."""
        if isinstance(data_in, BaseModel):
            data_dict = data_in.model_dump(exclude_unset=True)
        else:
            data_dict = data_in

        if not data_dict:
            return False  # Không có gì để cập nhật

        query = (
            update(self.model).where(self.model.id == id).values(**data_dict)
        )
        result = await self.session.execute(query)
        return result.rowcount > 0

    async def delete(self, id: str | int, is_hard: bool = False) -> bool:
        """Xóa một bản ghi theo ID (hỗ trợ xóa mềm và xóa cứng)."""
        if is_hard:
            query = delete(self.model).where(self.model.id == id)
        elif hasattr(self.model, "active"):
            query = (
                update(self.model)
                .where(self.model.id == id)
                .values(active=False)
            )
        else:
            raise ValueError(
                "Model does not support soft delete, and hard delete was not requested."
            )

        result = await self.session.execute(query)
        return result.rowcount > 0

    async def update_or_create(
        self, defaults: Optional[Dict[str, Any]] = None, **conditions: Any
    ) -> Entity:
        """Tìm bản ghi theo `conditions`, nếu có thì cập nhật, không thì tạo mới."""
        defaults = defaults or {}

        instance = await self.find_one_by(**conditions)
        if instance:
            if defaults:
                for key, value in defaults.items():
                    setattr(instance, key, value)
            return instance
        else:
            instance = self.model(**conditions, **defaults)
            return await self.insert(instance)

    # --------------------------------------------------------------------------
    # HÀM LOGIC ĐẶC THÙ (ĐƯỢC GIỮ LẠI THEO YÊU CẦU)
    # --------------------------------------------------------------------------

    async def soft_update(
        self, old_entity: Entity, data_in: Schema | Dict[str, Any]
    ) -> Entity:
        """
        Logic "versioning": Vô hiệu hóa bản ghi cũ và tạo một bản ghi mới với dữ liệu cập nhật.
        LƯU Ý: Đây là logic nghiệp vụ đặc thù, không phải là một hàm CRUD thông thường.
        """
        old_entity.active = False

        # Convert Pydantic DTO to dict if necessary
        if not isinstance(data_in, dict):
            data_in = data_in.model_dump(exclude_none=True)

        # Merge old data and new data
        update_data = {
            **{
                k: v
                for k, v in old_entity.__dict__.items()
                if k != "_sa_instance_state"
            },
            **data_in,
            "id": None,  # Tạo bản ghi mới -> để None để DB tự tạo ID
            "active": True,  # Đánh dấu bản ghi mới là active
        }

        # Tạo bản ghi mới từ dữ liệu đã cập nhật
        new_entity = type(old_entity)(**update_data)

        self.session.add(new_entity)

        await self.session.flush()  # Lấy ID nếu cần
        return new_entity

    async def bulk_update(
        self, ids: List[int], updates: Dict[int | str, Dict[str, Any]], with_commit: bool = True
    ) -> bool:
        """
        Cập nhật nhiều bản ghi với dữ liệu khác nhau cho mỗi bản ghi.
        Nếu chỉ truyền ids và updates là dict các trường chung, sẽ update tất cả ids với cùng giá trị.
        Nếu updates là dict với key là id, value là dict các trường, sẽ update từng bản ghi với giá trị riêng.
        Sử dụng câu lệnh `CASE` của SQL để hiệu năng cao.

        Args:
            updates (Dict): Dict với key là ID của bản ghi và value là một dict chứa các thay đổi,
                            hoặc dict các trường chung cho tất cả ids.
                            Ví dụ: {1: {"status": "done"}, 2: {"status": "failed", "retries": 3}}
                            hoặc {"status": "done"}
        """
        if not updates:
            return False

        # Nếu updates là dict các trường chung (không phải dict id -> dict)
        if all(not isinstance(v, dict) for v in updates.values()):
            # update tất cả ids với cùng giá trị
            query = (
                update(self.model)
                .where(self.model.id.in_(ids))
                .values(**updates)
            )
            result = await self.session.execute(query)
            return result.rowcount > 0

        # Ngược lại, updates là dict id -> dict các trường riêng
        all_columns_to_update = set()
        for changes in updates.values():
            all_columns_to_update.update(changes.keys())

        values_to_set = {}
        for col_name in all_columns_to_update:
            case_statement = case(
                *(
                    (self.model.id == id_, new_values[col_name])
                    for id_, new_values in updates.items()
                    if col_name in new_values
                ),
                else_=getattr(self.model, col_name),
            )
            values_to_set[col_name] = case_statement

        query = (
            update(self.model)
            .where(self.model.id.in_(ids))
            .values(**values_to_set)
        )
        result = await self.session.execute(query)
        return result.rowcount > 0

    async def delete_by_condition(
        self, condition: dict, is_hard: bool = False
    ) -> bool:
        """
        Xóa bản ghi dựa trên điều kiện.

        :param condition: Dict chứa điều kiện để xóa.
        :param is_hard: Nếu True, xóa cứng; nếu False, xóa mềm (nếu có `active`).
        :param with_commit: Nếu True, commit thay đổi ngay sau khi xóa.
        :return: True nếu xóa thành công.
        """
        query = None
        filters = []

        for key, value in condition.items():
            if isinstance(value, dict):
                for op, val in value.items():
                    if op == "in":
                        filters.append(getattr(self.model, key).in_(val))
            else:
                filters.append(getattr(self.model, key) == value)

        if is_hard:
            query = (
                delete(self.model)
                .where(and_(*filters))
                .execution_options(synchronize_session="fetch")
            )
        elif hasattr(self.model, "active"):
            query = (
                update(self.model)
                .where(and_(*filters))
                .values(active=False)
                .execution_options(synchronize_session="fetch")
            )

        if query is None:
            raise ValueError(
                "Cannot delete: Model does not support soft delete."
            )

        await self.session.execute(query)

        return True

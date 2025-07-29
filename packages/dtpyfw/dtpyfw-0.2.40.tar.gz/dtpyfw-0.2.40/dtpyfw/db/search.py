from typing import Any
from math import ceil
from sqlalchemy import func, distinct as distinct_func
from sqlalchemy.orm import Session

from .search_utils.free_search import free_search
from .search_utils.make_condition import make_condition
from .search_utils.filter_values import get_filters_value
from .search_utils.selected_filters import make_selected_filters


__all__ = ("get_list",)



def get_list(
    current_query: dict,
    db: Session,
    model: Any,
    joins: list[dict] = None,
    pre_conditions: list = None,
    filters: list = None,
    searchable_columns: list = None,
    exact_search: bool = True,
    search_tokenizer: bool = False,
    search_similarity_threshold: float = 0.2,
    options: list = None,
    distinct=None,
    primary_column: str = "id",
    get_function_parameters: dict = None,
    return_available_filters: bool = True,
    return_selected_filters: bool = True,
    export_mode: bool = False,
):
    if joins is None:
        joins = []

    if filters is None:
        filters = []

    if searchable_columns is None:
        searchable_columns = []

    if pre_conditions is None:
        pre_conditions = []

    if options is None:
        options = []

    if get_function_parameters is None:
        get_function_parameters = {}

    page = current_query.get("page") or 1
    items_per_page = current_query.get("items_per_page") or 30

    # Create Initial Model Query
    main_query = db.query(model)

    if distinct is True:
        count_query = db.query(
            func.count(distinct_func(getattr(model, primary_column)))
        )
    elif distinct:
        count_query = db.query(func.count(distinct_func(distinct)))
    else:
        count_query = db.query(func.count(getattr(model, primary_column)))

    for join_item in joins:
        main_query = main_query.join(**join_item)
        count_query = count_query.join(**join_item)

    main_query = main_query.filter(*pre_conditions)
    count_query = count_query.filter(*pre_conditions)

    # Initialize rows and conditions
    conditions = []

    names_conditions = {}
    for filter_item in filters:
        names_conditions[filter_item.get("name")] = []

    for filter_item in filters:
        name = filter_item.get("name")
        columns = filter_item.get("columns")
        values = current_query.get(name)
        if not columns or not name or not values:
            continue

        target_condition = make_condition(filter_item=filter_item, values=values)
        if target_condition is not None:
            conditions.append(target_condition)
            for inner_name, inner_name_values in names_conditions.items():
                if inner_name != name:
                    inner_name_values.append(target_condition)

    if conditions:
        main_query = main_query.filter(*conditions)
        count_query = count_query.filter(*conditions)

    if search_query := current_query.get("search"):
        search_conditions, search_sort = free_search(
            columns=searchable_columns,
            query=search_query,
            threshold=search_similarity_threshold,
            exact=exact_search,
            tokenize=search_tokenizer,
        )
        main_query = main_query.filter(*search_conditions)
        count_query = count_query.filter(*search_conditions)
    else:
        search_sort = None

    if distinct is True:
        main_query = main_query.distinct()
    elif distinct:
        main_query = main_query.distinct(distinct)

    if options:
        main_query = main_query.options(*options)

    if search_sort is not None:
        final_query = main_query.order_by(*search_sort)
    elif sorting := (current_query.get("sorting") or []):
        order_by_list = []
        for item in sorting:
            sort_by = item.get("sort_by")
            if not sort_by:
                continue

            if hasattr(sort_by, "value"):
                sort_by = sort_by.value

            order_by = item.get("order_by")
            if not order_by:
                continue

            if hasattr(order_by, "value"):
                order_by = order_by.value

            order_by_list.append(getattr(getattr(model, sort_by), order_by)())

        final_query = main_query.order_by(*order_by_list)
    else:
        final_query = main_query

    if items_per_page and page:
        final_query = final_query.limit(items_per_page).offset(
            (page - 1) * items_per_page
        )

    rows = list(map(lambda x: x.get(**get_function_parameters), final_query.all()))

    if export_mode:
        return rows
    else:
        count = count_query.first()[0]
        current_query["total_row"] = count

        # Calculate pagination-related information
        if items_per_page and page:
            last_page = ceil(count / items_per_page)
            current_query["last_page"] = last_page
            current_query["has_next"] = last_page > page
            current_query["page"] = page
            current_query["items_per_page"] = items_per_page

        result = {
            "rows_data": rows,
            "payload": current_query,
        }

        if return_available_filters:
            result['available_filters'] = get_filters_value(
                db=db,
                pre_conditions=pre_conditions,
                joins=joins,
                filters=filters,
                names_conditions=names_conditions,
            ) if filters is not None else []

        if return_selected_filters:
            result['selected_filters'] = make_selected_filters(
                current_query=current_query,
                filters=filters,
            )

        # Return a dictionary containing the filter/sort options, current query data, and rows of data
        return result

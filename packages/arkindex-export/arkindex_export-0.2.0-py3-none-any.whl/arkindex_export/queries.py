from arkindex_export.models import Element, ElementPath
from peewee import Select


def list_children(parent_id):
    # First, build the base query to get direct children
    base = (
        ElementPath.select(ElementPath.child_id, ElementPath.ordering)
        .where(ElementPath.parent_id == parent_id)
        .cte("children", recursive=True, columns=("child_id", "ordering"))
    )

    # Then build the second recursive query, using an alias to join both queries on the same table
    EP = ElementPath.alias()
    recursion = EP.select(EP.child_id, EP.ordering).join(
        base, on=(EP.parent_id == base.c.child_id)
    )

    # Combine both queries, using UNION and not UNION ALL to deduplicate parents
    # that might be found multiple times with complex element structures
    cte = base.union(recursion)

    # And load all the elements found in the CTE
    query = (
        Element.select()
        .with_cte(cte)
        .join(cte, on=(Element.id == cte.c.child_id))
        .order_by(cte.c.ordering.asc())
    )

    return query


def list_parents(child_id):
    """
    List an element's parents, including itself
    """
    # Include the element itself in the list
    base = (
        Select().select(child_id).cte("parents", recursive=True, columns=("parent_id",))
    )

    # Recurse on ElementPaths
    recursion = ElementPath.select(ElementPath.parent_id).join(
        base, on=(ElementPath.child_id == base.c.parent_id)
    )

    # Combine both queries, using UNION and not UNION ALL to deduplicate parents
    # that might be found multiple times with complex element structures
    cte = base.union(recursion)

    # And load all the elements found in the CTE
    query = Element.select().with_cte(cte).join(cte, on=(Element.id == cte.c.parent_id))

    return query

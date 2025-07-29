def query_existing_processes(pks: list[int]) -> list[int]:
    """Query all existing processes from the database."""
    from aiida import orm

    qb = orm.QueryBuilder()
    qb.append(
        orm.ProcessNode,
        filters={"id": {"in": pks}},
        project=["id"],
    )
    results = qb.all()
    existing_pks = [res[0] for res in results]
    return existing_pks


def query_terminated_processes(pks: list[int]) -> list[int]:
    """Query all terminated processes from the database."""
    from aiida import orm

    qb = orm.QueryBuilder()
    qb.append(
        orm.ProcessNode,
        filters={
            "id": {"in": pks},
            "attributes.process_state": {"in": ["killed", "finished", "excepted"]},
        },
        project=["id"],
    )
    results = qb.all()
    terminated_pks = [res[0] for res in results]
    return terminated_pks

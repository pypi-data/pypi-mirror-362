from h2o_engine_manager.clients.dai_engine import expression
from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState


def test_filter_versions():
    builder = expression.FilterBuilder()
    version = expression.Version().EqualTo("1.10.3")
    builder = builder.WithFilter(version)

    buildstr = builder.Build()
    assert buildstr == "version = 1.10.3"

    version = expression.Version().NotEqualTo("1.10.3")
    buildstr = expression.FilterBuilder().WithFilter(version).Build()
    assert buildstr == "version != 1.10.3"


def test_filter_state():
    state = expression.State().EqualTo(DAIEngineState.STATE_RUNNING)
    fil = expression.FilterBuilder().WithFilter(state)
    assert "state = STATE_RUNNING" == fil.Build()

    state = expression.State().NotEqualTo(DAIEngineState.STATE_RUNNING)
    fil = expression.FilterBuilder().WithFilter(state)
    assert "state != STATE_RUNNING" == fil.Build()


def test_filter_engine():
    testuid = "3d055b46-6903-4ce6-b665-5d48c4d93d18"

    uid = expression.Uid().EqualTo(testuid)
    fil = expression.FilterBuilder().WithFilter(uid)
    assert 'uid = "' + testuid + '"' == fil.Build()

    testcreator = "user/testuser"

    creator = expression.Creator().EqualTo(testcreator)

    fil = expression.FilterBuilder().WithFilter(creator)
    assert 'creator = "' + testcreator + '"' == fil.Build()

    fil = expression.FilterBuilder().WithFilter(uid).WithFilter(creator)
    assert 'uid = "' + testuid + '" AND creator = "' + testcreator + '"' == fil.Build()


def test_filter_memory():
    mem = expression.MemoryBytes().EqualTo("1Ki")
    fil = expression.FilterBuilder().WithFilter(mem)

    assert "memory_bytes = 1024" == fil.Build()

    mem = expression.MemoryBytes().EqualTo("1k")
    fil = expression.FilterBuilder().WithFilter(mem)

    assert "memory_bytes = 1000" == fil.Build()

    gt = expression.MemoryBytes().GreaterThan("1")
    lt = expression.MemoryBytes().LessThanOrEqualTo("1Ki")
    fil = expression.FilterBuilder().WithFilter(gt).WithFilter(lt)

    assert "memory_bytes > 1 AND memory_bytes <= 1024" == fil.Build()

    f1 = expression.MemoryBytes().GreaterThanOrEqualTo("1Gi")
    f2 = expression.MemoryBytes().LessThan("2Gi")
    filter_str = expression.FilterBuilder().WithFilter(f1).WithFilter(f2).Build()

    assert filter_str == "memory_bytes >= 1073741824 AND memory_bytes < 2147483648"

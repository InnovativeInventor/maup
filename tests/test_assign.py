import pandas
from numpy import nan

from spatial_ops import assign


def test_assign_assigns_geometries_when_they_nest_neatly(
    four_square_grid, squares_within_four_square_grid
):
    result = assign(squares_within_four_square_grid, four_square_grid)
    assert len(list(result)) == len(squares_within_four_square_grid)


def test_assign_returns_iterable(four_square_grid, squares_within_four_square_grid):
    result = assign(squares_within_four_square_grid, four_square_grid)
    assert iter(result)


def test_assignment_has_dtype_of_target_geom_index(
    four_square_grid, squares_within_four_square_grid
):
    target = four_square_grid.set_index("ID")

    result = assign(squares_within_four_square_grid, target)

    assert result.dtype == target.index.dtype


def test_assign_gives_expected_answer_when_geoms_nest_neatly(
    four_square_grid, squares_within_four_square_grid
):
    result = set(
        assign(
            squares_within_four_square_grid, four_square_grid.set_index("ID")
        ).items()
    )

    assert result == {(0, "a"), (1, "a"), (2, "b"), (3, "d")}


def test_assigns_na_to_geometries_not_fitting_into_any_others(
    left_half_of_square_grid, squares_within_four_square_grid
):
    result = set(
        assign(
            squares_within_four_square_grid, left_half_of_square_grid.set_index("ID")
        ).items()
    )

    assert result == {(0, "a"), (1, "a"), (2, "b"), (3, nan)}


def test_assign_can_be_used_with_groupby(four_square_grid, squares_df):
    assignment = assign(squares_df, four_square_grid.set_index("ID"))

    result = squares_df.groupby(assignment)

    assert set(result.groups.keys()) == {"a", "b", "d"}
    assert set(result.indices["a"]) == {0, 1}
    assert set(result.indices["b"]) == {2}
    assert set(result.indices["d"]) == {3}


def test_assign_can_be_used_with_groupby_and_aggregate(four_square_grid, squares_df):
    assignment = assign(squares_df, four_square_grid.set_index("ID"))

    result = squares_df.groupby(assignment)["data"].sum()

    expected = pandas.Series([2, 1, 1], index=["a", "b", "d"])
    assert (expected == result).all()